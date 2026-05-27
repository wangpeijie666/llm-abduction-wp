from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Callable, Dict, List


# 本文件只负责“构造给 LLM 的 messages”，不做解析、不做文件修改、不跑 WP。
# 这样 prompt 文案、输出 schema 和 baseline3 主流程可以分开维护。
# 所有函数都返回 OpenAI-compatible chat messages:
#   [{"role": "system", ...}, {"role": "user", json.dumps(payload)}]

"""
构造 assertion probe candidate 生成 prompt。
使用场景：
- handle_fail 诊断为 proof_gap/missing_spec/ambiguous 后，会先尝试插入局部 `//@ assert ...;` 来观察 WP 结果是否改善。
输入重点：
- goal_context: 从 WP 输出中抽取的 assumptions/prove_statement/goal_text
- visible_identifiers: 插入点之前源码可见的变量名，限制 LLM 不要发明变量
- markers: `PROBE_HERE` 插入点,LLM 可以指定 preferred_marker
- baseline_wp: 当前失败 WP 日志,用于理解卡住的 PO。

输出要求：
- JSON array
- 每项只是一条可插入的 ACSL assertion,不直接生成 invariant/ensures。
"""
def build_assertion_candidate_prompt(
    source_code: str,
    target: Any,
    goal_context: Dict[str, Any],
    visible_identifiers: List[str],
    markers: List[Any],
    max_candidates: int,
    baseline_wp: str,
    clip_text: Callable[[str, int], str],
) -> List[Dict[str, str]]:

    system = "You generate abductive ACSL assertion probes for Frama-C/WP. Output JSON array only."
    user = {
        "task": "Use abduction to generate assertion candidates for one failed proof obligation.",
        "abduction_task": (
            "Given the failed proof obligation, its assumptions, and the prove statement, "
            "infer one or more missing source-level facts H such that the assumptions should make H provable "
            "at a probe marker, and assumptions plus H would help prove the target."
        ),
        "abduction_steps": [
            "Read failed_po, prove_goal, prove_statement, and assumptions.",
            "Identify the logical gap between assumptions and prove_statement.",
            "Propose a small bridge fact H over source-level variables only.",
            "Check mentally that H is plausible at the chosen marker and not merely a restatement of the target.",
            "Write H as a single ACSL assertion insertable as //@ assert <predicate>;",
        ],
        "constraints": [
            "Only generate ACSL assertions insertable as //@ assert ...;",
            "Do not generate requires/ensures/loop invariant/lemma.",
            "Each candidate must be a single assertion.",
            "Do not introduce undefined logic functions.",
            "Use only source-level identifiers listed in source_visible_identifiers plus ACSL built-ins.",
            "Never use Frama-C/WP internal SSA names such as j_1, k_1, x_2, tmp_3.",
            "The assertion must represent the abducted bridge fact H.",
            "When a source-level ordering fact appears in WP-internal form, translate it back to source-level variable names.",
            "Prefer facts connecting variables that appear in both assumptions and the prove statement.",
            "Do not merely restate the target prove statement unless it is independently justified at the marker.",
            "Prefer small bridge facts that are likely provable at the marker and help the target.",
        ],
        # 明确拆出 abduction 所需的核心证明信息，避免 LLM 只看大段 goal_text。
        "failed_po": target.__dict__,
        "prove_goal": goal_context.get("goal_header", ""),
        "prove_statement": goal_context.get("prove_statement", ""),
        "assumptions": goal_context.get("assumptions", ""),
        # target_po 和 goal_context 保留完整上下文，兼容后续 prompt 调试和扩展。
        "target_po": target.__dict__,
        "goal_context": goal_context,
        # 只允许使用源码层面可见标识符，避免 LLM 把 WP 内部 SSA 名字写进 ACSL。
        "source_visible_identifiers": visible_identifiers,
        "markers": [{"name": m.name, "line_no": m.line_no, "raw_line": m.raw_line} for m in markers],
        "max_candidates": max_candidates,
        "code_excerpt": clip_text(source_code, 12000),
        "wp_feedback_excerpt": clip_text(baseline_wp, 12000),
        "output_schema": [
            {
                "assertion": "//@ assert <predicate>;",
                "preferred_marker": "marker name or null",
                "source_level_fact": "the abducted bridge fact H in source-level variable names only",
                "rationale": "which gap between assumptions and prove_statement this H bridges, and why H should hold at the marker",
            }
        ],
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]

"""
构造 failed PO 诊断 prompt。这个 prompt 不直接要求 LLM 修代码，而是要求它在固定枚举里选择：
- category: wrong_spec/missing_spec/proof_gap/ambiguous
- target_kind: 失败目标类型
- recommended_action: 下一步 repair action
"""
def build_failure_diagnosis_prompt(
    source_code: str,
    original_source: str,
    target: Any,
    goal_context: Dict[str, Any],
    markers: List[Any],
    wp_text: str,
    rule_default: Dict[str, Any],
    clip_text: Callable[[str, int], str],
) -> List[Dict[str, str]]:
    system = "You diagnose failed Frama-C/WP proof obligations. Output JSON only."
    user = {
        "task": "Diagnose why this proof obligation failed and choose the next repair action.",
        "allowed_category": ["wrong_spec", "missing_spec", "proof_gap", "ambiguous"],
        "allowed_recommended_action": [
            "delete_annotation",
            "rewrite_annotation",
            "add_invariant",
            "rewrite_assigns",
            "add_contract",
            "add_assertion",
            "promote_assertion",
            "regenerate",
        ],
        "target_kind_values": [
            "assertion",
            "postcondition",
            "invariant_establishment",
            "invariant_preservation",
            "assigns",
            "precondition",
            "unknown",
        ],
        # rule_default 来自代码侧规则诊断。LLM 应该在它基础上修正，而不是完全自由发挥。
        "rule_default": rule_default,
        "category_definitions": {
            "wrong_spec": (
                "An existing ACSL annotation is likely false, too strong, non-inductive, malformed for the code behavior, "
                "or otherwise responsible for creating an unprovable obligation. Prefer rewrite/delete actions."
            ),
            "missing_spec": (
                "The current annotations are plausible but insufficient as persistent specifications. "
                "The program likely needs an additional invariant, contract, assigns clause, or other durable ACSL fact."
            ),
            "proof_gap": (
                "The specification may already be essentially right, but the prover needs a local intermediate assertion "
                "or bridge fact at a specific program point. Prefer assertion probes before changing durable specs."
            ),
            "missing_spec_vs_proof_gap": (
                "Use missing_spec when the missing fact should remain as part of the program specification across calls or loop iterations, "
                "such as a loop invariant or function contract. Use proof_gap when a local assertion is enough to help the prover "
                "derive the target without changing the intended specification."
            ),
            "ambiguous": "The evidence is insufficient to confidently choose wrong_spec, missing_spec, or proof_gap.",
        },
        "target_po": asdict(target),
        "goal_context": goal_context,
        "markers": [{"name": m.name, "line_no": m.line_no, "raw_line": m.raw_line} for m in markers],
        "wp_log_excerpt": clip_text(wp_text, 12000),
        "current_code_excerpt": clip_text(source_code, 16000),
        "original_source_excerpt": clip_text(original_source, 12000),
        # 这些 bias 和 run_baseline3.py 里的规则默认值保持一致，用来稳定诊断方向。
        "diagnosis_guidance": {
            "loop invariant preservation diagnosis": "diagnose non_inductiveness before diagnosing missing specifications",
            "assigns failed":"usually wrong_spec or missing_spec; prefer rewrite_assigns or delete",
            "invariant establishment failed": "usually wrong_spec; prefer rewrite_annotation or delete",
            "invariant preservation failed": "usually wrong_spec or missing_spec",
            "assertion/postcondition failed": "usually missing_spec or proof_gap",
            "callee precondition failed": "wrong_spec if generated requires is suspicious, otherwise missing_spec",
        },
        "output_schema": {
            "category": "wrong_spec | missing_spec | proof_gap | ambiguous",
            "target_kind": "assertion | postcondition | invariant_establishment | invariant_preservation | assigns | precondition | unknown",
            "suspect_text": "verbatim suspect annotation or short description",
            "reason": "short reason",
            "recommended_action": "delete_annotation | rewrite_annotation | add_invariant | rewrite_assigns | add_contract | add_assertion | promote_assertion | regenerate",
        },
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]

"""
构造“缺少规格”修复 prompt。

适用于目标失败不是因为现有 annotation 明显错误，而是缺少 invariant、function contract、ensures/requires 等可帮助 WP 推理的规格。
该 prompt可以使用 assertion probe evidence，把局部有用事实提升成持久 spec。
"""
def build_missing_spec_prompt(
    source_code: str,
    target: Any,
    diagnosis: Any,
    goal_context: Dict[str, Any],
    marker_loop_context: List[Dict[str, Any]],
    probe_evidence: List[Dict[str, Any]],
    original_source: str,
    clip_text: Callable[[str, int], str],
) -> List[Dict[str, str]]:

    system = "You turn abducted missing facts into minimal ACSL specifications for Frama-C/WP. Output JSON array only."
    user = {
        "task": "Use the key missing facts found by abduction/probe evidence to add the missing ACSL specification needed for a failed proof obligation.",
        "abducted_fact_usage": [
            "Read probe_evidence as candidate abducted facts H that may bridge assumptions to the prove statement.",
            "Prefer facts whose classification shows the probe solved, improved, or plausibly helped the target.",
            "Promote a useful local assertion H into the right durable ACSL form: loop invariant for facts needed across iterations, contract/ensures/requires for function-level facts, assigns for frame facts.",
            "Do not add unrelated specifications; the new spec should correspond to a key missing fact supported by the failed goal or probe evidence.",
        ],
        "constraints": [
            "Do not modify executable C code.",
            "Do not remove or weaken target assertions from the original source.",
            "Each proposal must include original_text that appears verbatim and uniquely in current_code.",
            "replacement_text should include original_text plus the added or repaired ACSL specification when appropriate.",
            "Prefer loop invariants for facts needed across loop iterations.",
            "Prefer function contracts for facts about helper/callee functions.",
            "Use only source-level identifiers; never use WP internal SSA names.",
        ],
        "allowed_actions": ["add_invariant", "add_contract", "rewrite_assigns", "add_requires", "add_ensures"],
        # probe_evidence 允许 LLM 把“局部 assertion 有帮助”转化为 invariant/contract。
        "target_po": asdict(target),
        "diagnosis": asdict(diagnosis),
        "goal_context": goal_context,
        "marker_loop_context": marker_loop_context,
        "probe_evidence": probe_evidence,
        "current_code": clip_text(source_code, 16000),
        "original_source_excerpt": clip_text(original_source, 12000),
        "output_schema": [
            {
                "action": "add_invariant | add_contract | rewrite_assigns | add_requires | add_ensures",
                "original_text": "verbatim anchor from current_code",
                "replacement_text": "replacement text",
                "reason": "why this missing spec should help",
                "risk": "low | medium | high",
            }
        ],
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]

"""
构造“已有规格错误/过强”修复 prompt。

适用于 generated invariant/requires/ensures/assigns 形状不对、过强或与程序行为不一致的情况。prompt 明确要求只处理 suspect_text 附近的 ACSL，
不修改可执行 C 代码，不删除原始 target assertion。
"""
def build_wrong_spec_repair_prompt(
    source_code: str,
    target: Any,
    diagnosis: Any,
    goal_context: Dict[str, Any],
    wp_text: str,
    original_source: str,
    clip_text: Callable[[str, int], str],
) -> List[Dict[str, str]]:

    system = "You repair wrong generated ACSL specifications for Frama-C/WP. Output JSON array only."
    user = {
        "task": "Rewrite or delete the suspect generated ACSL annotation causing this failed proof obligation.",
        "constraints": [
            "Only edit ACSL annotations near suspect_text.",
            "Do not modify executable C code.",
            "Do not delete target assertions from the original source.",
            "If an over-strong generated requires clause is suspicious, delete or weaken it.",
            "If invariant establishment fails, prefer weakening the invariant.",
            "Each proposal must include original_text that appears verbatim and uniquely in current_code.",
            "Use valid ACSL accepted by Frama-C/WP.",
        ],
        "allowed_actions": ["delete_annotation", "rewrite_annotation", "rewrite_assigns", "add_contract", "regenerate"],
        # diagnosis.suspect_text 会提示 LLM 聚焦可疑 generated spec，避免大范围重写。
        "target_po": asdict(target),
        "diagnosis": asdict(diagnosis),
        "goal_context": goal_context,
        "wp_log_excerpt": clip_text(wp_text, 12000),
        "current_code": clip_text(source_code, 16000),
        "original_source_excerpt": clip_text(original_source, 12000),
        "output_schema": [
            {
                "action": "delete_annotation | rewrite_annotation | rewrite_assigns | add_contract | regenerate",
                "original_text": "verbatim text from current_code",
                "replacement_text": "replacement text, or empty string for delete_annotation",
                "reason": "why this wrong spec repair should help",
                "risk": "low | medium | high",
            }
        ],
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]

"""
构造 Invalid 修复 prompt。
该 prompt 给 LLM 错误行、错误信息和定位到的 annotation span,只允许删除该 ACSL 行或生成替代 ACSL 语句。
"""
def build_invalid_repair_prompt(
    error_line: int,
    error_message: str,
    annotation_span: Any,
    current_code: str,
    original_source: str,
    clip_text: Callable[[str, int], str],
) -> List[Dict[str, str]]:
    system = "You repair invalid ACSL annotations. Output JSON object only."
    span_payload = asdict(annotation_span) if annotation_span is not None else None
    user = {
        "task": "Decide whether to delete or rewrite the reported ACSL annotation line that makes Frama-C/WP reject the current file.",
        "constraints": [
            "Do not modify executable C code.",
            "Do not delete target assertions from the original source.",
            "Prefer the smallest syntactic or typing repair.",
            "Only repair annotation_span.text. Do not repair a different annotation.",
            "If the reported annotation is a generated helper assertion and is invalid, choose delete.",
            "For rewrite, replacement_text must be the complete ACSL replacement line.",
        ],
        # error_line/error_message/annotation_span 是 Invalid repair 的核心定位信息。
        "error_line": error_line,
        "error_message": error_message,
        "annotation_span": span_payload,
        "current_code_excerpt": clip_text(current_code, 16000),
        "original_source_excerpt": clip_text(original_source, 12000),
        "output_schema": {
            "action": "rewrite | delete",
            "replacement_text": "complete replacement ACSL line, or empty string for delete",
            "reason": "why this fixes the invalid annotation line",
        },
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]
