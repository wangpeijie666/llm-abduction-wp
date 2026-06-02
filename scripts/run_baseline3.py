from __future__ import annotations

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Baseline3 experiment entry."""

from pathlib import Path
import sys

EXPERIMENT_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(EXPERIMENT_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_ROOT_FOR_IMPORTS))

import argparse
import json
import re
import shutil
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from spec_abduction.acsl import GeneratedCodeError, extract_acsl_assertions, normalize_assertion, validate_generated_code
from spec_abduction.autobench import discover_cases
from spec_abduction.config import DEFAULT_AUTOBENCH_DIR, DEFAULT_CONFIG, EXPERIMENT_ROOT, load_model_config
from spec_abduction.llm import LLMClient, extract_code_response
from spec_abduction.logging import RunLogger
from spec_abduction.outputs import (
    case_record,
    failed_case_dir,
    failed_file_path,
    failure_wp_output_path,
    save_failed_file,
    save_failure_wp_output,
    successful_file_path,
)
from spec_abduction.prompts.baseline1 import build_direct_generation_prompt as build_initial_prompt
from spec_abduction.prompts.baseline3 import (
    build_assertion_candidate_prompt,
    build_failure_diagnosis_prompt,
    build_invalid_repair_prompt,
    build_missing_spec_prompt,
    build_wrong_spec_repair_prompt,
)
from spec_abduction.types import AttemptRecord, Case, WPResult
from spec_abduction.wp import attempt_status, result_score, run_wp


DEFAULT_OUT_ROOT = EXPERIMENT_ROOT / "results" / "baseline3_assertion_probe"
FEEDBACK_CHAR_LIMIT = 10000


@dataclass
class ProofObligation:
    name: str
    status: str
    raw_line: str
    line_no: int
    failure_mode: str
    profile: str
    goal_header: str = ""
    goal_text: str = ""
    assumptions: str = ""
    prove_statement: str = ""
    prover_output: str = ""
    source_file: str = ""
    source_line: Optional[int] = None


@dataclass
class ProbeMarker:
    name: str
    line_no: int
    raw_line: str
    indentation: str


@dataclass
class AssertionCandidate:
    assertion: str
    predicate: str
    marker: Optional[str]
    rationale: str
    source: str
    source_level_fact: str = ""
    recommended_integration: str = ""

"""
一次 WP 失败/Invalid 的诊断结果。先把WP 结果归因到一个较粗的类别，再根据类别选择 repair action。
字段约定：
- category: 固定取 invalid/wrong_spec/missing_spec/proof_gap/ambiguous 之一
- target_kind: 当前失败目标类型，例如 assertion、assigns、postcondition
- reason: 诊断理由，优先给 LLM prompt 和日志阅读使用；
- suspect_text: 可疑 ACSL 文本或失败目标摘要；
- source_line: 如果能从 WP 输出定位源码行号，则记录 1-based 行号；
- recommended_action: 固定 repair action 枚举之一；
- raw: 保留规则解析或 LLM 原始 JSON，便于后续调试。
"""
@dataclass
class FailureDiagnosis:

    category: str
    target_kind: str
    reason: str
    suspect_text: str = ""
    source_line: Optional[int] = None
    recommended_action: str = ""
    raw: Optional[Dict[str, Any]] = None

"""
一个可应用到当前 C+ACSL 文件上的修复提案。

这里统一承载 Invalid repair、wrong_spec repair、missing_spec repair 的LLM 输出。实际应用时会强制 original_text 唯一匹配，并调用
validate_generated_code，防止 LLM 修改可执行 C 代码或删除原始目标断言。
    """
@dataclass
class RepairProposal:

    action: str
    original_text: str
    replacement_text: str
    reason: str
    risk: str
    raw: Dict[str, Any]


@dataclass
class RepairApplicationResult:

    path: Optional[Path]
    reason: str
    details: List[str]
    applied_index: Optional[int] = None

"""
    源码中一段 ACSL annotation 的位置和属性。
    Invalid 修复时需要从 Frama-C 报错行号反查附近 annotation。这个结构记录annotation 的起止行、原文、粗粒度类型，以及它是否属于原始 benchmark 的target assertion。target assertion 不能被删除，只允许格式修复或等价重写。
"""
@dataclass
class AnnotationSpan:

    start_line: int
    end_line: int
    text: str
    kind: str
    is_original_target: bool

"""
一次 assertion probe 的完整证据。

- local assertion 已证明且解决目标：可直接保留；
- local assertion 未证明但目标解决：更像 missing_spec，需要 promote；
- 目标只改善未解决：可作为 rewrite/missing_spec prompt 的 evidence。
"""
@dataclass
class ProbeResult:

    file_path: Path
    wp: WPResult
    candidate: AssertionCandidate
    marker: ProbeMarker
    classification: str
    evidence: Dict[str, Any]


def is_comment_only_line(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith(("//", "/*", "*"))


def probe_marker_line(indent: str, name: str) -> str:
    return f"{indent}/* PROBE_HERE:{name} */"


def infer_body_indent(lines: List[str], source_index: int, loop_indent: str) -> str:
    for next_line in lines[source_index + 1 : source_index + 6]:
        if not next_line.strip():
            continue
        next_indent = re.match(r"\s*", next_line).group(0)
        if len(next_indent) > len(loop_indent):
            return next_indent
        break
    return loop_indent + "    "

"""
在loops的前面和loop body的开头插入占位符
"""
def add_probe_markers(source: str) -> str:
    if "PROBE_HERE" in source:
        return source if source.endswith("\n") else source + "\n"
    output: List[str] = []
    pending_loop_body: Optional[Tuple[int, str]] = None
    loop_index = 0
    lines = source.splitlines()
    for line_index, raw_line in enumerate(lines):
        loop_match = None
        if not is_comment_only_line(raw_line):
            loop_match = re.search(r"\b(?:for|while)\s*\(", raw_line)
        if loop_match is not None:
            loop_index += 1
            indent = re.match(r"\s*", raw_line).group(0)
            output.append(probe_marker_line(indent, f"loop{loop_index}_before"))
            output.append(raw_line)
            if "{" in raw_line:
                output.append(probe_marker_line(infer_body_indent(lines, line_index, indent), f"loop{loop_index}_body_entry"))
            else:
                pending_loop_body = (loop_index, indent)
            continue
        output.append(raw_line)
        if pending_loop_body is not None and "{" in raw_line and not is_comment_only_line(raw_line):
            pending_index, loop_indent = pending_loop_body
            output.append(probe_marker_line(loop_indent + "    ", f"loop{pending_index}_body_entry"))
            pending_loop_body = None
    return "\n".join(output) + "\n"

#参数解析函数
def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Baseline3 assertion probing over AutoBench.")
    parser.add_argument("--autobench-dir", default=str(DEFAULT_AUTOBENCH_DIR), help="Local AutoBench root.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="models_config.yaml.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="Output root.")
    parser.add_argument("--datasets", default="SyGuS,frama-c-problem,svcomp,46_fib", help="Comma-separated dataset names, or all.")
    parser.add_argument("--model", "--override-model", dest="model", default="gpt-4o", help="Model name in config.")
    parser.add_argument("--override-base-url", help="Runtime base_url override.")
    parser.add_argument("--attempts", type=int, default=3, help="Initial LLM spec generations per case.")
    parser.add_argument("--max-llm-candidates", type=int, default=5, help="Assertion candidates per failed PO.")
    parser.add_argument("--max-repair-rounds", type=int, default=7, help="Repair rounds after each initial generation.")
    parser.add_argument("--max-invalid-repairs", type=int, default=4, help="Maximum invalid-input repairs per initial generation.")
    parser.add_argument("--delete-invalid-after-fail", action="store_true", help="Allow deleting generated invalid annotations after repair fails.")
    parser.add_argument("--limit", type=int, default=0, help="Global case limit; 0 means no limit.")
    parser.add_argument("--dataset-limit", type=int, default=0, help="Per-dataset case limit; 0 means no limit.")
    parser.add_argument("--temperature", type=float, default=0.4, help="Initial spec LLM temperature.")
    parser.add_argument("--candidate-temperature", type=float, default=0.3, help="Assertion candidate LLM temperature.")
    parser.add_argument("--max-tokens", type=int, default=8192, help="LLM max completion tokens.")
    parser.add_argument("--frama-c", default="frama-c", help="frama-c executable.")
    parser.add_argument("--wp-timeout", type=int, default=8, help="WP prover timeout.")
    parser.add_argument("--provers", default="Alt-Ergo,Z3", help="WP prover list.")
    parser.add_argument("--resume", action="store_true", help="Skip cases with existing final output.")
    parser.add_argument("--overwrite", action="store_true", help="Remove out-root before running.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected cases without LLM/WP.")
    parser.add_argument("--trace-steps", action="store_true", help="Save per-case intermediate files, WP results, diagnoses, probes, and repair proposals.")
    return parser.parse_args(argv)


def trace_case_dir(out_root: Path, case: Case) -> Path:
    """返回某个 case 的可选中间步骤保存目录。"""

    return out_root / "traces" / case.dataset / Path(case.filename).stem


def jsonable(value: Any) -> Any:
    """把 dataclass、Path 等对象转成可 JSON 序列化的结构。"""

    if is_dataclass(value):
        return jsonable(asdict(value))
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def write_trace_json(trace_dir: Optional[Path], filename: str, data: Any) -> None:
    """如果 trace 开启，写一个 JSON 文件。"""

    if trace_dir is None:
        return
    trace_dir.mkdir(parents=True, exist_ok=True)
    (trace_dir / filename).write_text(json.dumps(jsonable(data), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_trace_text(trace_dir: Optional[Path], filename: str, text: str) -> None:
    """如果 trace 开启，写一个文本文件。"""

    if trace_dir is None:
        return
    trace_dir.mkdir(parents=True, exist_ok=True)
    (trace_dir / filename).write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def copy_trace_file(trace_dir: Optional[Path], filename: str, source: Path) -> None:
    """如果 trace 开启，复制一个已生成的文件。"""

    if trace_dir is None or not source.exists():
        return
    trace_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, trace_dir / filename)


def write_trace_wp(trace_dir: Optional[Path], wp: WPResult) -> None:
    """保存一次 WP 调用的命令、结果和 stdout/stderr。"""

    if trace_dir is None:
        return
    write_trace_json(
        trace_dir,
        "wp_result.json",
        {
            "result_type": wp.result_type,
            "elapsed_sec": wp.elapsed_sec,
            "command": wp.command,
            "stdout_path": wp.stdout_path,
            "stderr_path": wp.stderr_path,
        },
    )
    write_trace_text(trace_dir, "wp_stdout.txt", wp.stdout)
    write_trace_text(trace_dir, "wp_stderr.txt", wp.stderr or "")


def clip_text(text: str, limit: int = FEEDBACK_CHAR_LIMIT) -> str:
    if len(text) <= limit:
        return text
    head = limit // 2
    tail = limit - head
    return text[:head] + "\n\n... [truncated] ...\n\n" + text[-tail:]


def parse_json_array(text: str) -> List[Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[A-Za-z0-9_-]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        start, end = stripped.find("["), stripped.rfind("]")
        if start < 0 or end <= start:
            return []
        try:
            parsed = json.loads(stripped[start : end + 1])
        except json.JSONDecodeError:
            return []
    return parsed if isinstance(parsed, list) else []


def parse_json_object(text: str) -> Dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```[A-Za-z0-9_-]*\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        start, end = stripped.find("{"), stripped.rfind("}")
        if start < 0 or end <= start:
            return {}
        try:
            parsed = json.loads(stripped[start : end + 1])
        except json.JSONDecodeError:
            return {}
    return parsed if isinstance(parsed, dict) else {}

"""从 WP 输出中切分所有 `Goal ...` 详细块。"""
def extract_wp_goal_blocks(wp_output: str) -> List[Dict[str, str]]:

    blocks: List[Dict[str, str]] = []
    current: Optional[List[str]] = None
    for line in wp_output.splitlines():
        if line.startswith("Goal "):
            if current:
                blocks.append({"header": current[0].strip(), "text": "\n".join(current).strip()})
            current = [line]
        elif current is not None:
            if line.startswith("------------------------------------------------------------"):
                blocks.append({"header": current[0].strip(), "text": "\n".join(current).strip()})
                current = None
            else:
                current.append(line)
    if current:
        blocks.append({"header": current[0].strip(), "text": "\n".join(current).strip()})
    return blocks

"""把一个详细 Goal block 挂到对应的 ProofObligation 上。"""
def attach_goal_block_to_obligation(obligation: ProofObligation, block: Dict[str, str]) -> None:

    text = block.get("text", "")
    header = block.get("header", "")
    assume_match = re.search(r"Assume\s*\{(?P<body>.*?)\}\s*Prove:", text, re.DOTALL)
    prove_match = re.search(r"Prove:\s*(?P<body>.*?)(?:\nProver|\Z)", text, re.DOTALL)
    prover_match = re.search(r"\n(?P<body>Prover .*?)\Z", text, re.DOTALL)
    location_match = re.search(r"\(file\s+(?P<file>.*?),\s+line\s+(?P<line>\d+)\)", header)
    obligation.goal_header = header
    obligation.goal_text = text
    obligation.assumptions = assume_match.group("body").strip() if assume_match else ""
    obligation.prove_statement = prove_match.group("body").strip() if prove_match else ""
    obligation.prover_output = prover_match.group("body").strip() if prover_match else ""
    if location_match:
        obligation.source_file = location_match.group("file").strip()
        obligation.source_line = int(location_match.group("line"))

"""
从 Frama-C/WP 输出中提取未证明成功的 proof obligation。
WP 输出里每个目标通常长这样：
    [wp] [Failed] typed_array_assert ...
    [wp] [Timeout] some_loop_invariant ...
    [wp] [Qed] some_trivial_goal ...
这里只保留 Timeout/Failed/Unknown 三类失败目标，忽略 Qed/Valid/Passed之类已经证明成功的目标。
"""
def extract_failed_proof_obligations(wp_output: str) -> List[ProofObligation]:

    obligations: List[ProofObligation] = []
    for line_no, line in enumerate(wp_output.splitlines(), 1):
        # 匹配 WP 目标摘要行：
        # - status: 方括号里的证明状态，例如 Failed/Timeout/Unknown/Qed
        # - name:   proof obligation 名称，取状态后第一个非空白字段
        # - profile:剩余的 prover/profile 信息，原样保存用于诊断
        match = re.match(r"^\[wp\]\s+\[(?P<status>[^\]]+)\]\s+(?P<name>\S+)\s*(?P<profile>.*)$", line.strip())
        if not match:
            # 非 WP 目标摘要行，例如普通日志、warning、空行，直接跳过。
            continue
        status = match.group("status").strip()
        if status.lower() not in {"timeout", "failed", "unknown"}:
            # 已成功证明或与失败无关的状态不进入 repair 流程。
            continue
        obligations.append(
            ProofObligation(
                # PO 名称用于判断目标类型，例如 assertion、loop invariant、assigns 等。
                name=match.group("name").strip(),
                # 保留原始状态文本，方便日志和后续 prompt 使用。
                status=status,
                # 保存完整摘要行，便于调试和输出可读上下文。
                raw_line=line.strip(),
                # 这是 WP 输出中的行号，不是 C 源码行号。
                line_no=line_no,
                # failure_mode 使用小写状态，便于规则判断。
                failure_mode=status.lower(),
                # profile 是该行剩余信息，通常包含 prover 结果或耗时等细节。
                profile=match.group("profile").strip(),
            )
        )
    # WP 的详细 proof context 不在摘要行里，而是在后面的 Goal blocks 中。
    # 把失败的 Goal block 按目标类型和出现顺序挂回对应 PO，避免后续只拿到摘要。
    failed_blocks = [block for block in extract_wp_goal_blocks(wp_output) if re.search(r"returns\s+(Timeout|Failed|Unknown)", block["text"], re.IGNORECASE)]
    used_block_indexes: set[int] = set()
    for obligation_index, obligation in enumerate(obligations):
        selected_index: Optional[int] = None
        obligation_kind = goal_kind_for_po(obligation)
        for block_index, block in enumerate(failed_blocks):
            if block_index in used_block_indexes:
                continue
            if goal_block_kind(block["header"]) == obligation_kind:
                selected_index = block_index
                break
        if selected_index is None and obligation_index < len(failed_blocks) and obligation_index not in used_block_indexes:
            selected_index = obligation_index
        if selected_index is not None:
            used_block_indexes.add(selected_index)
            attach_goal_block_to_obligation(obligation, failed_blocks[selected_index])
    return obligations


def goal_kind_for_po(po: ProofObligation) -> str:
    name = po.name.lower()
    if "assert" in name:
        return "assertion"
    if "loop_invariant" in name and "preserved" in name:
        return "invariant_preservation"
    if "loop_invariant" in name and "established" in name:
        return "invariant_establishment"
    if "assigns" in name:
        return "assigns"
    if "ensures" in name or "post" in name:
        return "postcondition"
    return "unknown"


def goal_block_kind(header: str) -> str:
    lowered = header.lower()
    if "goal assertion" in lowered:
        return "assertion"
    if "preservation of invariant" in lowered:
        return "invariant_preservation"
    if "establishment of invariant" in lowered:
        return "invariant_establishment"
    if "loop assigns" in lowered or "assigns" in lowered:
        return "assigns"
    if "post-condition" in lowered or "postcondition" in lowered or "ensures" in lowered:
        return "postcondition"
    return "unknown"

"""把 ProofObligation 中已解析好的 Goal block 转成 prompt 使用的上下文。"""
def goal_context_from_po(target: ProofObligation) -> Dict[str, Any]:

    kind = goal_kind_for_po(target)
    return {
        "po_name": target.name,
        "po_status": target.status,
        "goal_kind": kind,
        "goal_header": target.goal_header,
        "assumptions": target.assumptions,
        "prove_statement": target.prove_statement,
        "prover_output": target.prover_output,
        "source_file": target.source_file,
        "source_line": target.source_line,
        "goal_text": clip_text(target.goal_text, 6000) if target.goal_text else "",
    }


def summarize_blocking_point(po: ProofObligation) -> str:
    name = po.name
    if "loop_invariant" in name and "preserved" in name:
        return "loop invariant preservation failed; likely missing a bridge fact after loop-body updates."
    if "loop_invariant" in name and "established" in name:
        return "loop invariant establishment failed; likely missing an initialization fact before entering the loop."
    if "assigns" in name:
        return "assigns/frame condition failed; likely missing a modifiable-set or range fact."
    if "ensures" in name or "post" in name:
        return "postcondition failed; likely missing a final-state bridge fact."
    if "assert" in name:
        return "assertion failed; likely needs a smaller provable intermediate fact or a stronger surrounding spec."
    return f"{po.name} failed with {po.failure_mode}; prover profile: {po.profile}."


def extract_wp_internal_identifiers(goal_text: str, source_identifiers: Iterable[str]) -> List[str]:
    source_set = set(source_identifiers)
    return sorted({ident for ident in re.findall(r"\b[A-Za-z_]\w*_\d+\b", goal_text) if ident not in source_set})


def extract_marker_loop_context(source_code: str, markers: List[ProbeMarker]) -> List[Dict[str, Any]]:
    lines = source_code.splitlines()
    contexts: List[Dict[str, Any]] = []
    for marker in markers:
        marker_index = max(marker.line_no - 1, 0)
        loop_index: Optional[int] = None
        for idx in range(marker_index, -1, -1):
            if re.search(r"\b(?:for|while)\s*\(", lines[idx]):
                loop_index = idx
                break
        annotation_start: Optional[int] = None
        if loop_index is not None:
            for idx in range(loop_index - 1, -1, -1):
                stripped = lines[idx].strip()
                if "/*@" in stripped:
                    annotation_start = idx
                    break
                if stripped and not stripped.startswith(("//@", "loop ", "*/", "*")):
                    break
        annotation_text = ""
        if annotation_start is not None and loop_index is not None:
            annotation_text = "\n".join(lines[annotation_start:loop_index])
        contexts.append(
            {
                "marker": marker.name,
                "marker_line": marker.line_no,
                "marker_raw_line": marker.raw_line,
                "enclosing_loop_line": (loop_index + 1) if loop_index is not None else None,
                "enclosing_loop": lines[loop_index].strip() if loop_index is not None else "",
                "preceding_acsl_block": annotation_text,
                "integration_hint": "Facts needed across loop iterations usually belong in the preceding loop invariant block.",
            }
        )
    return contexts

"""
扫描代码,找出assertion probe 可以插入的位置
"""
def find_probe_markers(source_code: str) -> List[ProbeMarker]:
    markers: List[ProbeMarker] = []
    pattern = re.compile(r"/\*\s*PROBE_HERE(?::(?P<name>[A-Za-z0-9_.-]+))?\s*\*/")
    for line_no, line in enumerate(source_code.splitlines(), 1):
        match = pattern.search(line)
        if not match:
            continue
        markers.append(
            ProbeMarker(
                name=match.group("name") or "default",
                line_no=line_no,
                raw_line=line,
                indentation=re.match(r"\s*", line).group(0),
            )
        )
    return markers


def extract_predicate(assertion: str) -> str:
    text = assertion.strip()
    text = text.replace("/*@", "").replace("*/", "").strip()
    text = re.sub(r"^//@\s*", "", text).strip()
    text = re.sub(r"^assert\s+", "", text).strip()
    if ":" in text:
        maybe_label, rest = text.split(":", 1)
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", maybe_label.strip()):
            text = rest.strip()
    text = text.rstrip(";").strip()
    if not text or re.search(r"\bassume\b", text):
        return ""
    return text


def format_assertion(predicate: str) -> str:
    return f"//@ assert {predicate.rstrip(';').strip()};"


VALID_DIAGNOSIS_CATEGORIES = {"invalid", "wrong_spec", "missing_spec", "proof_gap", "ambiguous"}
VALID_REPAIR_ACTIONS = {
    "delete_annotation",
    "rewrite_annotation",
    "add_invariant",
    "rewrite_assigns",
    "add_contract",
    "add_assertion",
    "promote_assertion",
    "regenerate",
}

"""
根据 annotation 文本粗略分类。
这个分类服务于 repair action 的默认选择:assigns 失败优先改 frame condition,loop invariant 失败优先 rewrite/weaken invariant,assertion失败通常进入 proof_gap/missing_spec 流程。
"""
def annotation_kind(text: str) -> str:

    lowered = text.lower()
    if "loop invariant" in lowered:
        return "loop_invariant"
    if "loop assigns" in lowered or re.search(r"\bassigns\b", lowered):
        return "assigns"
    if "requires" in lowered:
        return "requires"
    if "ensures" in lowered:
        return "ensures"
    if "assert" in lowered:
        return "assertion"
    if "assumes" in lowered:
        return "assumes"
    return "annotation"

"""
判断一段 annotation 是否包含原始 benchmark 的 target assertion。
这是一条安全边界:LLM 生成的 helper assertion 可以删除,但原始输入里的target assertion 是验证目标，不能因为修复 Invalid 或 Fail 被删除/弱化。
"""
def line_in_original_target_assertion(original_source: str, text: str) -> bool:

    if "assert" not in text:
        return False
    generated_assertions = extract_acsl_assertions(text, allow_malformed_line_marker=True)
    original_assertions = set(extract_acsl_assertions(original_source, allow_malformed_line_marker=True))
    return any(assertion in original_assertions for assertion in generated_assertions)

    
"""
根据 Frama-C 报错行号定位当前行的 ACSL annotation。
只返回报错行本身，不向上下扩展完整 /*@ ... */ block，也不回溯到前面的 annotation。
定位失败时返回 None,后续会退化为 LLM minimal repair 或 regenerate。
"""
def locate_annotation_by_line(source_code: str, line_no: int, original_source: str = "") -> Optional[AnnotationSpan]:

    lines = source_code.splitlines()
    if line_no < 1 or line_no > len(lines):
        print(f"ERROR: unable to locate ACSL annotation: line {line_no} is outside source range", file=sys.stderr)
        return None
    index = line_no - 1
    text = lines[index]
    acsl_tokens = ("/*@", "//@", "// @", "loop invariant", "loop assigns", "requires", "ensures", "assigns", "assert", "assumes")
    if not any(token in text for token in acsl_tokens):
        print(f"ERROR: unable to locate ACSL annotation at reported line {line_no}: {text.strip()}", file=sys.stderr)
        return None
    return AnnotationSpan(line_no, line_no, text, annotation_kind(text), line_in_original_target_assertion(original_source, text))

"""从 WP stdout/stderr 中抽取最可能的源码行号。"""
def extract_error_line(text: str) -> Optional[int]:

    patterns = [
        r":(?P<line>\d+):\s*(?:Warning|Error|user error|syntax error)",
        r"line\s+(?P<line>\d+)",
        r"\(file\s+[^,]+,\s+line\s+(?P<line>\d+)\)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group("line"))
    return None

"""压缩 Invalid 输出，只保留和语法/类型/annotation 错误相关的行。"""
def invalid_reason(text: str) -> str:

    interesting = []
    for line in text.splitlines():
        lowered = line.lower()
        if any(token in lowered for token in ("user error", "syntax error", "unbound", "typing", "annot-error", "frama-c aborted", "invalid")):
            interesting.append(line.strip())
    return "\n".join(interesting[:8]) or clip_text(text, 2000)

"""
提取 Invalid 修复需要的上下文。
Invalid 通常不是证明能力不足，而是当前 C+ACSL 无法被 Frama-C/WP 接受。
这里仅从 WP 输出中提取报错行、错误摘要，并定位该行对应的 ACSL annotation
"""
def diagnose_invalid(source_code: str, original_source: str, wp_result: WPResult) -> FailureDiagnosis:

    wp_text = wp_result.stdout + "\n" + wp_result.stderr
    #定位到行号
    line_no = extract_error_line(wp_text)
    #用 locate_annotation_by_line() 找到报错行对应的 ACSL annotation
    span = locate_annotation_by_line(source_code, line_no, original_source) if line_no is not None else None
    reason = invalid_reason(wp_text)
    if span is None:
        return FailureDiagnosis("invalid", "unknown", reason, source_line=line_no)
    return FailureDiagnosis(
        "invalid",
        span.kind,
        reason,
        suspect_text=span.text,
        source_line=span.start_line,
        raw={"annotation_span": asdict(span)},
    )

"""
给 failed PO 提供规则默认诊断。LLM 诊断前先根据 PO 名字做一个偏置，避免完全依赖模型：
assigns 失败默认改 assigns,invariant establishment 默认是 wrong_spec
assertion/postcondition 默认先当 proof_gap,看是否需要 assertion probe。
"""
def diagnosis_defaults_for_po(po: ProofObligation) -> Tuple[str, str]:

    kind = goal_kind_for_po(po)
    lowered = po.name.lower()
    if kind == "assigns" or "assigns" in lowered:
        return "wrong_spec", "rewrite_assigns"
    if kind == "invariant_establishment":
        return "wrong_spec", "rewrite_annotation"
    if kind == "invariant_preservation":
        return "missing_spec", "add_invariant"
    if "requires" in lowered or "precondition" in lowered:
        return "missing_spec", "add_contract"
    if kind in {"assertion", "postcondition"}:
        return "proof_gap", "add_assertion"
    return "ambiguous", "add_assertion"

"""
诊断一个 failed proof obligation 并选择下一步 repair action。
1. `diagnosis_defaults_for_po` 给出基于 PO 类型的保守默认值；
2. LLM 读取 goal_context/WP 日志/current code 后输出 category/action。
LLM 输出只在枚举范围内才被接受；否则回退到规则默认值。这样即使 LLM输出格式漂移,也不会把主流程带到未知 action。
"""
def diagnose_failed_po(
    client: LLMClient,
    source_code: str,
    original_source: str,
    po: ProofObligation,
    goal_context: Dict[str, Any],
    markers: List[ProbeMarker],
    wp_text: str,
    args: argparse.Namespace,
) -> FailureDiagnosis:
    #先用规则给默认诊断
    default_category, default_action = diagnosis_defaults_for_po(po)
    base = FailureDiagnosis(
        default_category,
        goal_context.get("goal_kind") or goal_kind_for_po(po),
        summarize_blocking_point(po),
        suspect_text=goal_context.get("goal_header", ""),
        recommended_action=default_action,
        raw={"rule_default": True},
    )
    try:
        #调 LLM 进一步诊断
        messages = build_failure_diagnosis_prompt(
            source_code,
            original_source,
            po,
            goal_context,
            markers,
            wp_text,
            asdict(base),
            clip_text,
        )
        raw = client.chat(messages, args.candidate_temperature, args.max_tokens, f"baseline3_diagnose_{po.name}")
        parsed = parse_json_object(raw)
    #如果 LLM 调用失败，直接返回默认诊断
    except Exception:
        return base
    #解析 LLM 输出
    category = str(parsed.get("category") or default_category)
    action = str(parsed.get("recommended_action") or default_action)
    target_kind = str(parsed.get("target_kind") or base.target_kind)
    #校验 category 和 action 是否在允许集合里
    if category not in VALID_DIAGNOSIS_CATEGORIES:
        category = default_category
    if action not in VALID_REPAIR_ACTIONS:
        action = default_action
    return FailureDiagnosis(
        category,
        target_kind,
        str(parsed.get("reason") or base.reason),
        suspect_text=str(parsed.get("suspect_text") or base.suspect_text),
        recommended_action=action,
        raw=parsed,
    )


def source_visible_identifiers(source_code: str, markers: List[ProbeMarker]) -> List[str]:
    max_line = max((marker.line_no for marker in markers), default=len(source_code.splitlines()))
    prefix = "\n".join(source_code.splitlines()[:max_line])
    identifiers = set()
    type_pattern = r"char|short|int|long|float|double|size_t|bool|_Bool"
    for match in re.finditer(rf"\b(?:{type_pattern})\s+([^;()]+);", prefix):
        for part in match.group(1).split(","):
            name_match = re.search(r"[*\s]*([A-Za-z_]\w*)", part.strip())
            if name_match:
                identifiers.add(name_match.group(1))
    for match in re.finditer(rf"\b(?:{type_pattern})\s+([A-Za-z_]\w*)\s*\(([^)]*)\)", prefix):
        params = match.group(2).strip()
        if not params or params == "void":
            continue
        for part in params.split(","):
            name_match = re.search(r"([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?$", part.strip())
            if name_match:
                identifiers.add(name_match.group(1))
    for match in re.finditer(r"\bfor\s*\(\s*(?:int|long|unsigned|size_t)\s+([A-Za-z_]\w*)\b", prefix):
        identifiers.add(match.group(1))
    return sorted(identifiers)


ACSL_ALLOWED = {
    "assert", "true", "false", "NULL", "INT_MIN", "INT_MAX", "UINT_MAX", "SIZE_MAX",
    "valid", "valid_read", "separated", "old", "at", "result", "forall", "exists",
    "integer", "real",
}


def assertion_unknown_identifiers(predicate: str, visible: Iterable[str]) -> List[str]:
    visible_set = set(visible) | ACSL_ALLOWED
    unknown = []
    for ident in re.findall(r"(?<!\\)\b[A-Za-z_]\w*\b", predicate):
        if ident not in visible_set and not ident.startswith("autospec_probe_"):
            unknown.append(ident)
    return sorted(set(unknown))

#直接llm生成一份c+acsl(同baseline1)
def generate_initial_code(client: LLMClient, case: Case, attempt: int, temperature: float, max_tokens: int) -> str:
    source_code = case.source_path.read_text(encoding="utf-8", errors="replace")
    raw = client.chat(build_initial_prompt(case, source_code, attempt), temperature, max_tokens, f"{case.dataset}_{case.filename}_initial{attempt}")
    code = extract_code_response(raw)
    if not code:
        raise ValueError("LLM returned empty code")
    #确保可执行C代码和用于检验正确性的assertion没有被修改
    validate_generated_code(source_code, code)
    #给循环前和循环体入口插入：/* PROBE_HERE:loop1_before */ /* PROBE_HERE:loop1_body_entry */
    code = add_probe_markers(code)
    return code if code.endswith("\n") else code + "\n"


def normalize_preferred_marker(value: Any) -> Optional[str]:
    marker = "" if value is None else str(value).strip()
    return None if marker.lower() in {"", "null", "none"} else marker


def parse_assertion_candidate_item(item: Any, visible: Iterable[str]) -> Optional[AssertionCandidate]:
    """把 LLM 返回的单个 JSON item 清洗成 AssertionCandidate。"""

    if not isinstance(item, dict):
        return None
    predicate = extract_predicate(str(item.get("assertion", "")))
    if not predicate or assertion_unknown_identifiers(predicate, visible):
        return None
    return AssertionCandidate(
        assertion=format_assertion(predicate),
        predicate=predicate,
        marker=normalize_preferred_marker(item.get("preferred_marker")),
        rationale=str(item.get("rationale", "")),
        source="llm",
        source_level_fact=str(item.get("source_level_fact", "")),
        recommended_integration=str(item.get("recommended_integration", "")),
    )

"""
为当前 failed PO 生成 assertion probe 候选。
这里生成的不是最终 spec,而是临时插入到 PROBE_HERE 位置的 `//@ assert ...;`。
后续 collect_assertion_probe_evidence() 会把这些 candidate 写进临时文件并跑 WP,
用结果判断该中间事实是否有助于修复。
"""
def generate_assertion_candidates(
    client: LLMClient,
    source_code: str,
    target: ProofObligation,
    target_index: int,
    baseline_wp: str,
    markers: List[ProbeMarker],
    max_candidates: int,
    temperature: float,
    max_tokens: int,
    trace_dir: Optional[Path] = None,
) -> List[AssertionCandidate]:

    # 从 ProofObligation 中取出已解析好的 Goal block 信息，包括 assumptions、prove_statement、prover_output 等，作为 LLM 生成中间事实的主要依据。
    goal_context = goal_context_from_po(target)
    # 收集 marker 之前源码层面可见的变量名，用来约束 LLM 不要生成 WP 内部变量或未定义标识符。
    visible = source_visible_identifiers(source_code, markers)
    # 构造 assertion candidate prompt。prompt 会要求 LLM 只输出 JSON array，每项是一条可插入的 ACSL assertion。
    messages = build_assertion_candidate_prompt(source_code, target, goal_context, visible, markers, max_candidates, baseline_wp, clip_text)
    write_trace_json(trace_dir, "assertion_candidate_prompt.json", messages)
    # 调 LLM 生成候选 assertion。
    raw = client.chat(
        messages,
        temperature,
        max_tokens,
        f"baseline3_candidates_{target.name}",
    )
    write_trace_text(trace_dir, "assertion_candidate_raw.txt", raw)
    # LLM 应返回 JSON array；解析失败时 parse_json_array 会返回空列表。
    parsed = parse_json_array(raw)
    write_trace_json(trace_dir, "assertion_candidate_parsed.json", parsed)
    candidates: List[AssertionCandidate] = []
    for item in parsed:
        candidate = parse_assertion_candidate_item(item, visible)
        if candidate is None:
            continue
        candidates.append(candidate)
        if len(candidates) >= max_candidates:
            # 防止 LLM 返回过多 candidate 导致 WP probe 数量失控。
            break
    write_trace_json(trace_dir, "assertion_candidates.json", candidates)
    return candidates

"""
把 LLM repair 输出统一解析成 RepairProposal 列表。
Invalid repair prompt 输出 JSON object,而 missing/wrong spec prompt 输出JSON array。这里同时兼容两种形态,后续应用逻辑只处理 RepairProposal。
"""
def parse_repair_proposals(raw: str) -> List[RepairProposal]:

    parsed_items: List[Any]
    obj = parse_json_object(raw)
    if obj:
        parsed_items = [obj]
    else:
        parsed_items = parse_json_array(raw)
    proposals: List[RepairProposal] = []
    for item in parsed_items:
        if not isinstance(item, dict):
            continue
        action = str(item.get("action") or item.get("rewrite_type") or "rewrite_annotation")
        proposals.append(
            RepairProposal(
                action=action,
                original_text=str(item.get("original_text", "")),
                replacement_text=str(item.get("replacement_text", "")),
                reason=str(item.get("reason", "")),
                risk=str(item.get("risk", "")),
                raw=item,
            )
        )
    return proposals

"""让 LLM 针对“已有 spec 错了/过强/形状不好”生成修复提案。"""
def generate_wrong_spec_repair_proposals(
    client: LLMClient,
    source_code: str,
    original_source: str,
    target: ProofObligation,
    diagnosis: FailureDiagnosis,
    goal_context: Dict[str, Any],
    wp_text: str,
    args: argparse.Namespace,
    trace_dir: Optional[Path] = None,
) -> List[RepairProposal]:

    messages = build_wrong_spec_repair_prompt(source_code, target, diagnosis, goal_context, wp_text, original_source, clip_text)
    write_trace_json(trace_dir, "wrong_spec_prompt.json", messages)
    raw = client.chat(messages, args.candidate_temperature, args.max_tokens, f"baseline3_wrong_spec_{target.name}")
    write_trace_text(trace_dir, "wrong_spec_raw.txt", raw)
    proposals = parse_repair_proposals(raw)
    write_trace_json(trace_dir, "wrong_spec_proposals.json", proposals)
    return proposals

"""
让 LLM 针对“缺少 spec”生成补充型提案。

与 wrong_spec repair 不同，这个 prompt 允许 add_invariant/add_contract/add_ensures 等“补缺失规格”的动作，并会把 probe evidence 作为依据传入。
"""
def generate_missing_spec_repair_proposals(
    client: LLMClient,
    source_code: str,
    original_source: str,
    target: ProofObligation,
    diagnosis: FailureDiagnosis,
    goal_context: Dict[str, Any],
    markers: List[ProbeMarker],
    probe_evidence: List[Dict[str, Any]],
    args: argparse.Namespace,
    trace_dir: Optional[Path] = None,
) -> List[RepairProposal]:

    marker_context = extract_marker_loop_context(source_code, markers)
    messages = build_missing_spec_prompt(source_code, target, diagnosis, goal_context, marker_context, probe_evidence, original_source, clip_text)
    write_trace_json(trace_dir, "missing_spec_prompt.json", messages)
    raw = client.chat(messages, args.candidate_temperature, args.max_tokens, f"baseline3_missing_spec_{target.name}")
    write_trace_text(trace_dir, "missing_spec_raw.txt", raw)
    proposals = parse_repair_proposals(raw)
    write_trace_json(trace_dir, "missing_spec_proposals.json", proposals)
    return proposals

"""
让 LLM 对报错行的 Invalid annotation 做最小修复。LLM 负责判断删除该 ACSL 行还是生成替代 ACSL 语句。
"""
def generate_invalid_repair_proposal(
    client: LLMClient,
    source_code: str,
    original_source: str,
    diagnosis: FailureDiagnosis,
    args: argparse.Namespace,
    trace_dir: Optional[Path] = None,
) -> Optional[RepairProposal]:

    span = None
    if diagnosis.raw and isinstance(diagnosis.raw.get("annotation_span"), dict):
        data = diagnosis.raw["annotation_span"]
        span = AnnotationSpan(
            int(data.get("start_line", 0)),
            int(data.get("end_line", 0)),
            str(data.get("text", "")),
            str(data.get("kind", "annotation")),
            bool(data.get("is_original_target", False)),
        )
    messages = build_invalid_repair_prompt(diagnosis.source_line or 0, diagnosis.reason, span, source_code, original_source, clip_text)
    write_trace_json(trace_dir, "invalid_repair_prompt.json", messages)
    raw = client.chat(messages, args.candidate_temperature, args.max_tokens, "baseline3_invalid_repair")
    write_trace_text(trace_dir, "invalid_repair_raw.txt", raw)
    proposals = parse_repair_proposals(raw)
    write_trace_json(trace_dir, "invalid_repair_proposals.json", proposals)
    return proposals[0] if proposals else None


def expand_candidate_marker_pairs(candidates: List[AssertionCandidate], markers: List[ProbeMarker], limit: int) -> List[Tuple[AssertionCandidate, ProbeMarker]]:
    marker_by_name = {marker.name: marker for marker in markers}
    if "default" in marker_by_name:
        marker_by_name.setdefault("PROBE_HERE", marker_by_name["default"])
        marker_by_name.setdefault("/* PROBE_HERE */", marker_by_name["default"])
    pairs: List[Tuple[AssertionCandidate, ProbeMarker]] = []
    for candidate in candidates:
        if candidate.marker:
            marker = marker_by_name.get(str(candidate.marker))
            if marker is not None:
                pairs.append((candidate, marker))
        else:
            pairs.extend((candidate, marker) for marker in markers)
        if len(pairs) >= limit:
            break
    return pairs[:limit]


def make_probe_label(po_index: int, candidate_index: int, marker: ProbeMarker) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", marker.name).strip("_") or "marker"
    return f"autospec_probe_{po_index + 1}_{candidate_index + 1}_{safe}"


def create_temp_file_with_assertion(source_code: str, candidate: AssertionCandidate, marker: ProbeMarker, label: str, temp_file: Path) -> None:
    lines = source_code.splitlines()
    insertion_index = marker.line_no
    assertion_line = f"{marker.indentation}//@ assert {label}: {candidate.predicate};"
    updated = lines[:insertion_index] + [assertion_line] + lines[insertion_index:]
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_text("\n".join(updated) + "\n", encoding="utf-8")


def find_po(obligations: Iterable[ProofObligation], name: str) -> Optional[ProofObligation]:
    for obligation in obligations:
        if obligation.name == name:
            return obligation
    return None


def is_assertion_proved(label: str, result_type: str, wp_output: str) -> bool:
    if result_type == "Invalid":
        return False
    for failed_po in extract_failed_proof_obligations(wp_output):
        if label in failed_po.name or label in failed_po.raw_line:
            return False
    return True


def is_target_solved(target: ProofObligation, probe_wp_output: str, probe_result_type: str) -> bool:
    if probe_result_type.startswith("Pass_"):
        return True
    if probe_result_type == "Invalid":
        return False
    for failed_po in extract_failed_proof_obligations(probe_wp_output):
        if failed_po.name == target.name:
            return False
    return True


def target_improvement_reason(target: ProofObligation, baseline_wp_output: str, probe_wp_output: str, probe_result_type: str) -> Tuple[bool, str]:
    if is_target_solved(target, probe_wp_output, probe_result_type):
        return True, "target_solved"
    baseline_target = find_po(extract_failed_proof_obligations(baseline_wp_output), target.name)
    probe_target = find_po(extract_failed_proof_obligations(probe_wp_output), target.name)
    if baseline_target is None or probe_target is None:
        return False, "no_comparable_target"
    if baseline_target.failure_mode != probe_target.failure_mode:
        return True, f"failure_mode {baseline_target.failure_mode} -> {probe_target.failure_mode}"
    if baseline_target.profile != probe_target.profile:
        return True, f"profile {baseline_target.profile} -> {probe_target.profile}"
    baseline_names = {po.name for po in extract_failed_proof_obligations(baseline_wp_output)}
    probe_names = {po.name for po in extract_failed_proof_obligations(probe_wp_output) if "autospec_probe_" not in po.name}
    if baseline_names != probe_names:
        return True, "failed PO set changed"
    return False, "no_observable_shift"


def classify_assertion_probe(assertion_proved: bool, target_solved: bool, target_improved: bool) -> str:
    if assertion_proved and target_solved:
        return "successful_probe"
    if assertion_proved and target_improved:
        return "proved_but_only_improves"
    if assertion_proved and not target_improved:
        return "proved_but_not_helpful"
    if not assertion_proved and target_improved:
        return "useful_but_unproved"
    return "unproved_and_not_helpful"

"""
把一次 assertion probe 的结果整理成给 repair prompt 使用的 evidence。

collect_assertion_probe_evidence() 会保存完整 ProbeResult,但后续missing_spec/wrong_spec prompt 不需要 WPResult 全量对象，只需要知道：
候选事实是什么、插在哪里、是否证明、是否帮助了当前目标，以及这个事实更适合被提升成 invariant/contract/assertion 还是只作为局部证据。
"""
def build_probe_evidence(
    candidate: AssertionCandidate,
    marker: ProbeMarker,
    classification: str,
    assertion_proved: bool,
    target_solved: bool,
    target_improved: bool,
    improved_reason: str,
    goal_context: Dict[str, Any],
) -> Dict[str, Any]:

    return {
        # 优先使用 LLM 给出的源码层事实描述；没有时退回 predicate/assertion。
        "fact": candidate.source_level_fact or candidate.predicate or candidate.assertion,
        # 实际插入临时文件的 ACSL assertion 文本。
        "assertion": candidate.assertion,
        # probe 分类，例如 successful_probe / useful_but_unproved 等。
        "classification": classification,
        # 该 assertion 本身是否被 WP 证明。
        "proved_as_assertion": assertion_proved,
        # 原 failed PO 是否已经被这个 probe 解决。
        "target_solved": target_solved,
        # 即使未完全解决，目标失败状态或 failed PO 集合是否有可观察改善。
        "target_improved": target_improved,
        # 记录改善原因，例如 target_solved、failure_mode changed、failed PO set changed。
        "target_improved_reason": improved_reason,
        # assertion 插入的 marker 名称和行号，供后续决定如何集成该事实。
        "marker": marker.name,
        "marker_line": marker.line_no,
        # LLM 对该事实最终应如何集成的建议，例如 invariant/contract/assertion。
        "recommended_integration": candidate.recommended_integration or "unknown",
        # LLM 生成该 candidate 时给出的理由。
        "rationale": candidate.rationale,
        # 当前 failed PO 原本要证明的目标，用于 repair prompt 对齐上下文。
        "target_to_prove": goal_context.get("prove_statement"),
        # 当前目标类型，例如 invariant_preservation / assertion / postcondition。
        "goal_kind": goal_context.get("goal_kind"),
    }

"""
Probe 的目标不是直接生成最终修复，而是在当前 failed PO 附近临时插入LLM 给出的中间 assertion,再跑 WP 观察：
- assertion 本身能不能证明；
- 原失败目标是否解决；
- 即使没解决,失败状态/失败集合是否有改善。
这些结果会作为 evidence 传给后续 missing_spec/wrong_spec repair prompt。
"""
def collect_assertion_probe_evidence(
    args: argparse.Namespace,
    client: LLMClient,
    source_code: str,
    target: ProofObligation,
    target_index: int,
    baseline_wp: WPResult,
    goal_context: Dict[str, Any],
    temp_dir: Path,
    trace_dir: Optional[Path] = None,
) -> List[ProbeResult]:

    # 先找当前源码里可插入 probe assertion 的占位符。
    markers = find_probe_markers(source_code)
    if not markers:
        return []
    # baseline WP 输出代表“插 probe 前”的失败状态，后面用它和 probe 后结果对比。
    feedback_text = baseline_wp.stdout + "\n" + baseline_wp.stderr
    try:
        # 让 LLM 基于当前失败目标、WP goal context 和 marker 位置生成候选中间事实。
        # 这些 candidate 是临时中间事实，不一定最终加入代码，只用于探测 proof gap /missing spec
        candidates = generate_assertion_candidates(
            client,
            source_code,
            target,
            target_index,
            feedback_text,
            markers,
            args.max_llm_candidates,
            args.candidate_temperature,
            args.max_tokens,
            trace_dir,
        )
    except Exception:
        candidates = []
    results: List[ProbeResult] = []
    # 把 candidate 和具体 marker 配对：
    # - candidate 指定 marker 时，只插到该 marker；
    # - 未指定 marker 时，会尝试插到所有 marker；
    # - 总数量受 max_llm_candidates 限制，避免 probe 爆炸。
    pairs = expand_candidate_marker_pairs(candidates, markers, args.max_llm_candidates)
    for candidate_index, (candidate, marker) in enumerate(pairs):
        # 交给 WP 实测候选 assertion 是否有用。
        # 给临时 assertion 打稳定 label，后面从 WP 输出中识别该 assertion 是否失败。
        label = make_probe_label(target_index, candidate_index, marker)
        probe_file = temp_dir / f"probe_{target_index + 1}_{candidate_index + 1}.c"
        # 在 marker 后插入一条 //@ assert label: predicate; 生成临时 C 文件。
        create_temp_file_with_assertion(source_code, candidate, marker, label, probe_file)
        # 对插入 probe assertion 后的临时文件重新跑 WP。
        probe_wp = run_wp(args.frama_c, probe_file, temp_dir / "wp_logs", f"probe_{target_index + 1}_{candidate_index + 1}", args.wp_timeout, args.provers)
        probe_trace_dir = trace_dir / f"probe_{candidate_index + 1:02d}" if trace_dir is not None else None
        copy_trace_file(probe_trace_dir, "probe.c", probe_file)
        write_trace_wp(probe_trace_dir, probe_wp)
        probe_feedback = probe_wp.stdout + "\n" + probe_wp.stderr
        # 判断 probe assertion 本身是否被证明：
        # 如果 WP 输出里没有该 label 对应的失败 PO,就认为 assertion 已证明。
        assertion_proved = is_assertion_proved(label, probe_wp.result_type, probe_feedback)
        # 判断原来的目标 PO 是否已经不再失败。
        target_solved = is_target_solved(target, probe_feedback, probe_wp.result_type)
        # 即使目标未完全解决，也检查失败模式、profile 或 failed PO 集合是否发生改善。
        target_improved, improved_reason = target_improvement_reason(target, feedback_text, probe_feedback, probe_wp.result_type)
        # 根据 assertion 是否证明、目标是否解决/改善，对 probe 结果分类。
        classification = classify_assertion_probe(assertion_proved, target_solved, target_improved)
        # 构造给后续 repair prompt 使用的结构化 evidence。
        evidence = build_probe_evidence(
            candidate,
            marker,
            classification,
            assertion_proved,
            target_solved,
            target_improved,
            improved_reason,
            goal_context,
        )
        # 保存完整 probe 结果，包括临时文件、WP 结果、candidate、marker 和 evidence。
        results.append(ProbeResult(probe_file, probe_wp, candidate, marker, classification, evidence))
        write_trace_json(probe_trace_dir, "probe_result.json", results[-1])
    write_trace_json(trace_dir, "probe_results.json", results)
    return results

"""
从 probe 结果中挑出可直接采用的 local assertion。

当前实现先保守地返回整文件 Pass 或 successful_probe 的文件。未来如果要做promote_assertion,可以在这里把 useful_but_unproved 的 assertion 提升到
invariant/ensures/requires 后再返回。
"""
def apply_successful_probe_or_promote(probe_results: List[ProbeResult]) -> Optional[Tuple[Path, WPResult]]:

    for result in probe_results:
        if attempt_status(result.wp.result_type) == "Pass" or result.classification == "successful_probe":
            return result.file_path, result.wp
    return None

"""
根据 Invalid 诊断生成一个修复后的临时文件。
Invalid repair 有单独次数上限 max_invalid_repairs,防止某个语法错误在 repair loop中无限尝试。这里不做规则特判:只把报错行对应的 ACSL 和错误信息交给 LLM,
由 LLM 判断删除该行还是生成替代 ACSL 语句,再经过 apply_repair_proposal 校验。
"""
def repair_invalid_annotation(
    original_source: str,
    current_code: str,
    diagnosis: FailureDiagnosis,
    client: LLMClient,
    args: argparse.Namespace,
    temp_dir: Path,
    repair_round: int,
    invalid_repairs: int,
    trace_dir: Optional[Path] = None,
) -> Optional[Path]:
    if invalid_repairs >= args.max_invalid_repairs:
        return None
    span: Optional[AnnotationSpan] = None
    if diagnosis.raw and isinstance(diagnosis.raw.get("annotation_span"), dict):
        data = diagnosis.raw["annotation_span"]
        span = AnnotationSpan(
            int(data.get("start_line", 0)),
            int(data.get("end_line", 0)),
            str(data.get("text", "")),
            str(data.get("kind", "annotation")),
            bool(data.get("is_original_target", False)),
        )
    if span is None:
        print("ERROR: cannot repair invalid annotation because no ACSL annotation was located", file=sys.stderr)
        return None
    try:
        #交给llm进行delete或者rewrite
        llm_proposal = generate_invalid_repair_proposal(client, current_code, original_source, diagnosis, args, trace_dir)
    except Exception:
        return None
    if llm_proposal is None:
        return None
    if current_code.count(span.text) != 1:
        return None
    action = llm_proposal.action.strip().lower()
    #如果需要delete
    if action in {"delete", "delete_annotation"}:
        if span.is_original_target or line_in_original_target_assertion(original_source, span.text):
            return None
        replacement = ""
    #如果需要rewrite
    elif action in {"rewrite", "rewrite_annotation"}:
        if not llm_proposal.replacement_text:
            return None
        replacement = llm_proposal.replacement_text
    else:
        return None
    rewritten = current_code.replace(span.text, replacement, 1)
    try:
        validate_generated_code(original_source, rewritten)
    except GeneratedCodeError:
        return None
    repair_file = temp_dir / f"invalid_repair_{repair_round:02d}_01.c"
    repair_file.parent.mkdir(parents=True, exist_ok=True)
    repair_file.write_text(rewritten if rewritten.endswith("\n") else rewritten + "\n", encoding="utf-8")
    write_trace_json(trace_dir, "invalid_repair_applied.json", llm_proposal)
    copy_trace_file(trace_dir, "invalid_repaired.c", repair_file)
    return repair_file

"""
Invalid 分支入口:
diagnose_invalid函数诊断 Invalid
然后repair_invalid_annotation函数repair尝试得到下一轮待验证文件。
"""
def handle_invalid(
    args: argparse.Namespace,
    client: LLMClient,
    original_source: str,
    current_code: str,
    wp: WPResult,
    temp_dir: Path,
    repair_round: int,
    invalid_repairs: int,
    trace_dir: Optional[Path] = None,
) -> Optional[Path]:

    diagnosis = diagnose_invalid(current_code, original_source, wp)
    write_trace_json(trace_dir, "invalid_diagnosis.json", diagnosis)
    return repair_invalid_annotation(original_source, current_code, diagnosis, client, args, temp_dir, repair_round, invalid_repairs, trace_dir)


def try_repair_proposals(
    original_source: str,
    current_code: str,
    proposals: List[RepairProposal],
    temp_dir: Path,
    prefix: str,
) -> RepairApplicationResult:
    """按顺序尝试应用一组 repair proposals，并记录不可应用原因。"""

    if not proposals:
        return RepairApplicationResult(None, "no_proposals", [])
    details: List[str] = []
    for index, proposal in enumerate(proposals, 1):
        if proposal.action == "regenerate" or not proposal.original_text:
            details.append(f"#{index} skipped: action={proposal.action!r}, missing exact original_text or regenerate")
            continue
        count = current_code.count(proposal.original_text)
        if count != 1:
            details.append(f"#{index} skipped: action={proposal.action!r}, original_text_count={count}")
            continue
        if proposal.action in {"delete_annotation", "delete"}:
            if line_in_original_target_assertion(original_source, proposal.original_text):
                details.append(f"#{index} skipped: refuses to delete original target assertion")
                continue
            replacement = ""
        else:
            replacement = proposal.replacement_text
        rewritten = current_code.replace(proposal.original_text, replacement, 1)
        try:
            validate_generated_code(original_source, rewritten)
        except GeneratedCodeError as exc:
            details.append(f"#{index} skipped: generated code rejected: {exc}")
            continue
        safe_action = re.sub(r"[^A-Za-z0-9_]+", "_", proposal.action).strip("_") or "repair"
        repair_file = temp_dir / f"{prefix}_{index:02d}_{safe_action}.c"
        repair_file.parent.mkdir(parents=True, exist_ok=True)
        repair_file.write_text(rewritten if rewritten.endswith("\n") else rewritten + "\n", encoding="utf-8")
        details.append(f"#{index} applied: action={proposal.action!r}, file={repair_file.name}")
        return RepairApplicationResult(repair_file, "applied", details, index)
    return RepairApplicationResult(None, "no_applicable_repair", details)


def log_repair_application(client: LLMClient, label: str, result: RepairApplicationResult, max_details: int = 4) -> None:
    if result.path is not None:
        client.log(f"baseline3 repair {label}: applied proposal #{result.applied_index} -> {result.path.name}")
        return
    client.log(f"baseline3 repair {label}: not applied ({result.reason})")
    for detail in result.details[:max_details]:
        client.log(f"  {detail}")
    remaining = len(result.details) - max_details
    if remaining > 0:
        client.log(f"  ... {remaining} more skipped proposal(s)")

"""
Fail 分支入口
1. extract_failed_proof_obligations() 从 WP 日志解析失败目标。
2. goal_context_from_po() 从 PO 中取出已解析好的 Goal block 信息。
3. diagnose_failed_po() 诊断失败类型。
4. 对 proof_gap / missing_spec / ambiguous 先跑 assertion probe。
5. 根据诊断类型生成 repair proposal。
6. try_repair_proposals() 尝试应用第一个合法 repair。
每个 repair round 只处理当前 WP 反馈中的第一个 failed PO;一旦生成 repair,外层会重新跑 WP 并重新解析 failed PO list,避免继续使用过期的证明上下文。
"""
def handle_fail(
    args: argparse.Namespace,
    client: LLMClient,
    original_source: str,
    current_code: str,
    wp: WPResult,
    temp_dir: Path,
    repair_round: int,
    trace_dir: Optional[Path] = None,
) -> Optional[Path]:

    feedback_text = wp.stdout + "\n" + wp.stderr
    #WP 日志解析失败目标PO
    failed_pos = extract_failed_proof_obligations(feedback_text)
    write_trace_json(trace_dir, "failed_pos.json", failed_pos)
    if not failed_pos:
        return None
    markers = find_probe_markers(current_code)
    #每轮只处理当前 WP 反馈中的第一个 failed PO。生成 repair 后外层会重新跑 WP，避免继续使用过期的证明上下文
    po_index = 0
    po = failed_pos[po_index]
    write_trace_json(trace_dir, "selected_po.json", po)
    #提取当前 PO 的 goal context
    goal_context = goal_context_from_po(po)
    #补充源码可见变量和 marker 上下文
    goal_context["source_visible_identifiers"] = source_visible_identifiers(current_code, markers)
    goal_context["forbidden_wp_internal_identifiers"] = extract_wp_internal_identifiers(goal_context.get("goal_text", ""), goal_context["source_visible_identifiers"])
    goal_context["marker_loop_contexts"] = extract_marker_loop_context(current_code, markers)
    write_trace_json(trace_dir, "goal_context.json", goal_context)
    #诊断失败类型
    diagnosis = diagnose_failed_po(client, current_code, original_source, po, goal_context, markers, feedback_text, args)
    write_trace_json(trace_dir, "diagnosis.json", diagnosis)
    probe_results: List[ProbeResult] = []
    successful_probe: Optional[Tuple[Path, WPResult]] = None
    #对部分类型例如proof_gap和missing_spec，说明可能缺一个中间事实
    if diagnosis.category in {"proof_gap", "missing_spec", "ambiguous"}:
        #让 LLM 生成一些候选 assertion，插到 PROBE_HERE marker 位置，跑 WP 看有没有帮助
        #符号的abduction是加在这一步的！！！！
        probe_trace_dir = trace_dir / "probes" if trace_dir is not None else None
        probe_results = collect_assertion_probe_evidence(args, client, current_code, po, po_index, wp, goal_context, temp_dir / f"round_{repair_round:02d}_probe", probe_trace_dir)
        #插到 PROBE_HERE marker 位置，跑 WP 看有没有帮助
        successful_probe = apply_successful_probe_or_promote(probe_results)
        #如果诊断是 proof_gap，并且某个 probe 文件直接让目标通过，就直接返回这个 probe 文件作为下一轮验证文件
        if successful_probe is not None and diagnosis.category == "proof_gap":
            return successful_probe[0]
    #筛选有用的 probe evidence：
    #- successful_probe: probe 让目标成功。
    #- useful_but_unproved: probe 自身可能没完全证明，但对目标有帮助。
    #- proved_but_only_improves: probe 能证明，且让结果有所改善但没完全解决。
    probe_evidence = [result.evidence for result in probe_results if result.classification in {"successful_probe", "useful_but_unproved", "proved_but_only_improves"}]
    write_trace_json(trace_dir, "probe_evidence_used.json", probe_evidence)
    repair_prefix = f"repair_{repair_round:02d}_{po_index + 1:02d}"

    def run_repair_kind(kind: str) -> RepairApplicationResult:
        kind_trace_dir = trace_dir / kind if trace_dir is not None else None
        try:
            if kind == "wrong_spec":
                proposals = generate_wrong_spec_repair_proposals(client, current_code, original_source, po, diagnosis, goal_context, feedback_text, args, kind_trace_dir)
            else:
                proposals = generate_missing_spec_repair_proposals(client, current_code, original_source, po, diagnosis, goal_context, markers, probe_evidence, args, kind_trace_dir)
        except Exception as exc:
            result = RepairApplicationResult(None, "proposal_generation_error", [f"{type(exc).__name__}: {exc}"])
            write_trace_json(kind_trace_dir, "repair_application.json", result)
            log_repair_application(client, f"{kind}_{po.name}", result)
            return result
        result = try_repair_proposals(original_source, current_code, proposals, temp_dir, f"{repair_prefix}_{kind}")
        write_trace_json(kind_trace_dir, "repair_application.json", result)
        if result.path is not None:
            copy_trace_file(kind_trace_dir, "repaired.c", result.path)
        log_repair_application(client, f"{kind}_{po.name}", result)
        return result

    # 根据诊断选择主 repair 分支；主分支 proposal 不可应用时，再试另一类 repair，避免一次 exact-text 失败就结束 attempt。
    if diagnosis.category == "wrong_spec":
        repair_order = ["wrong_spec", "missing_spec"]
    else:
        repair_order = ["missing_spec", "wrong_spec"]

    primary_result = run_repair_kind(repair_order[0])
    if primary_result.path is not None:
        return primary_result.path
    client.log(f"baseline3 repair fallback: trying {repair_order[1]} after {repair_order[0]} failed")
    fallback_result = run_repair_kind(repair_order[1])
    return fallback_result.path


def resumed_record(case: Case, out_root: Path) -> Optional[Dict[str, Any]]:
    success_file = successful_file_path(out_root, case)
    if success_file.exists():
        return {
            "dataset": case.dataset,
            "filename": case.filename,
            "source_path": str(case.source_path),
            "final_status": "Pass",
            "overall_success": True,
            "best_attempt": "",
            "best_result_type": "Pass",
            "successful_saved_file": str(success_file),
            "failed_saved_file": "",
            "failure_wp_output": "",
            "skipped_existing": True,
        }
    failure_output = failure_wp_output_path(out_root, case)
    failed_file = failed_file_path(out_root, case)
    if failure_output.exists() and failed_file.exists():
        result_type = ""
        status = "Fail"
        attempt = ""
        for line in failure_output.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("Final status: "):
                status = line.split(": ", 1)[1]
            elif line.startswith("Best attempt: "):
                attempt = line.split(": ", 1)[1]
            elif line.startswith("Best result: "):
                result_type = line.split(": ", 1)[1]
        return {
            "dataset": case.dataset,
            "filename": case.filename,
            "source_path": str(case.source_path),
            "final_status": status,
            "overall_success": False,
            "best_attempt": attempt,
            "best_result_type": result_type,
            "successful_saved_file": "",
            "failed_saved_file": str(failed_file),
            "failure_wp_output": str(failure_output),
            "skipped_existing": True,
        }
    return None

"""
运行单个 benchmark case。核心循环如下:
    1. 每次 attempt 调 generate_initial_code() 生成一份 C+ACSL(每个 case 最多做 args.attempts 次独立初始生成)
    2. 对当前文件调用 run_wp()
    3. Pass: 保存到 successful_files
    4. Invalid: handle_invalid()
    5. Fail: 走 handle_fail()
    6. 每个 attempt 最多 repair args.max_repair_rounds 轮
"""
def run_case(args: argparse.Namespace, client: LLMClient, case: Case, out_root: Path) -> Dict[str, Any]:

    if args.resume:
        record = resumed_record(case, out_root)
        if record is not None:
            trace_dir = trace_case_dir(out_root, case)
            if trace_dir.exists():
                record["trace_dir"] = str(trace_dir)
            return record
    original_source = case.source_path.read_text(encoding="utf-8", errors="replace")
    best: Optional[AttemptRecord] = None
    successful_file = ""
    case_trace_dir = trace_case_dir(out_root, case) if args.trace_steps else None
    if case_trace_dir is not None:
        if case_trace_dir.exists():
            shutil.rmtree(case_trace_dir)
        write_trace_text(case_trace_dir, "00_original.c", original_source)
        write_trace_json(case_trace_dir, "case.json", case)
    with tempfile.TemporaryDirectory(prefix="baseline3_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        generated_dir = temp_dir / "generated_specs"
        wp_dir = temp_dir / "wp_logs"
        generated_dir.mkdir(parents=True, exist_ok=True)
        wp_dir.mkdir(parents=True, exist_ok=True)
        #每个case最多args.attempts次尝试
        for attempt in range(1, args.attempts + 1):
            attempt_trace_dir = case_trace_dir / f"attempt_{attempt:02d}" if case_trace_dir is not None else None
            generated_file = generated_dir / f"attempt_{attempt:02d}.c"
            try:
                #复用 baseline1 的 direct generation
                code = generate_initial_code(client, case, attempt, args.temperature, args.max_tokens)
                generated_file.write_text(code, encoding="utf-8")
                write_trace_text(attempt_trace_dir, "initial.c", code)
                current_code = code
                current_file = generated_file
                invalid_repairs = 0
                #每次尝试最多repair次数为max_repair_rounds次
                for repair_round in range(0, args.max_repair_rounds + 1):
                    round_trace_dir = attempt_trace_dir / f"round_{repair_round:02d}" if attempt_trace_dir is not None else None
                    copy_trace_file(round_trace_dir, "current.c", current_file)
                    # repair_round == 0 表示初始生成文件的第一次 WP 检查；
                    # 后续 round 使用上一轮 repair 产出的 current_file。
                    wp = run_wp(
                        args.frama_c,
                        current_file,
                        wp_dir,
                        f"attempt_{attempt:02d}_round_{repair_round:02d}",
                        args.wp_timeout,
                        args.provers,
                    )
                    write_trace_wp(round_trace_dir, wp)
                    #得到status是fail还是pass还是invalid
                    status = attempt_status(wp.result_type)
                    record = AttemptRecord(
                        case.dataset,
                        case.filename,
                        attempt,
                        str(current_file),
                        wp.result_type,
                        wp.stdout_path,
                        wp.stderr_path,
                        status,
                        result_score(wp.result_type),
                        wp.stdout,
                        wp.stderr,
                        wp.command,
                        current_code,
                    )
                    if best is None or record.score > best.score:
                        best = record
                    #1. 如果pass直接写进sucessful_file里
                    if status == "Pass":
                        # 任意 attempt 的任意 repair round 通过，都作为该 case 成功。
                        target = successful_file_path(out_root, case)
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(current_file, target)
                        successful_file = str(target)
                        write_trace_json(round_trace_dir, "status.json", {"status": status, "result_type": wp.result_type, "saved_file": successful_file})
                        break
                    if repair_round >= args.max_repair_rounds:
                        write_trace_json(round_trace_dir, "status.json", {"status": status, "result_type": wp.result_type, "stop_reason": "max_repair_rounds"})
                        break
                    repair_dir = temp_dir / f"attempt_{attempt:02d}_repair_{repair_round + 1:02d}"
                    #2. 如果是invalid，表示Frama-C连当前C+ACSL文件都不能接受，通常是ACSL语法、类型、未绑定变量等、非法annotation等问题
                    if status == "Invalid":
                        # 先做Invalid-specific repair。
                        repaired_file = handle_invalid(
                            args,
                            client,
                            original_source,
                            current_code,
                            wp,
                            repair_dir,
                            repair_round + 1,
                            invalid_repairs,
                            round_trace_dir / "invalid_repair" if round_trace_dir is not None else None,
                        )
                        invalid_repairs += 1
                    #3. 如果是fail
                    else:
                        # Fail 表示 Frama-C/WP 接受了文件但仍有未证明目标；
                        # 先诊断 failed PO，再按 wrong_spec/missing_spec/proof_gap 分派。
                        repaired_file = handle_fail(
                            args,
                            client,
                            original_source,
                            current_code,
                            wp,
                            repair_dir,
                            repair_round + 1,
                            round_trace_dir / "fail_repair" if round_trace_dir is not None else None,
                        )
                    if repaired_file is None:
                        # 当前 WP 结果无法产生可应用 repair，结束该 attempt，
                        # 进入下一次独立 initial generation。
                        write_trace_json(round_trace_dir, "status.json", {"status": status, "result_type": wp.result_type, "stop_reason": "no_repair"})
                        break
                    copy_trace_file(round_trace_dir, "next.c", repaired_file)
                    write_trace_json(round_trace_dir, "status.json", {"status": status, "result_type": wp.result_type, "next_file": str(repaired_file)})
                    current_file = repaired_file
                    current_code = current_file.read_text(encoding="utf-8", errors="replace")
                if successful_file:
                    break
            except Exception as exc:
                code = exc.code if isinstance(exc, GeneratedCodeError) else generated_file.read_text(encoding="utf-8", errors="replace") if generated_file.exists() else ""
                record = AttemptRecord(
                    case.dataset,
                    case.filename,
                    attempt,
                    str(generated_file),
                    "Error",
                    "",
                    "",
                    "Error",
                    -1.0,
                    "",
                    "",
                    [],
                    code,
                    f"{type(exc).__name__}: {exc}",
                )
                if best is None or record.score > best.score:
                    best = record
                write_trace_json(attempt_trace_dir, "error.json", {"type": type(exc).__name__, "message": str(exc), "code": code})
    failure_wp_output = ""
    failed_file = ""
    if best and best.status != "Pass":
        failed_file = save_failed_file(out_root, case, best)
        failure_wp_output = save_failure_wp_output(out_root, case, best)
    record = case_record(case, best, False, successful_file, failed_file, failure_wp_output)
    if case_trace_dir is not None:
        record["trace_dir"] = str(case_trace_dir)
        write_trace_json(case_trace_dir, "final_record.json", record)
    return record


def write_reports(out_root: Path, records: List[Dict[str, Any]]) -> None:
    status_counts = Counter(record["final_status"] for record in records)
    dataset_counts: Dict[str, Counter] = {}
    for record in records:
        dataset_counts.setdefault(record["dataset"], Counter())[record["final_status"]] += 1
    lines = ["# Baseline3 Assertion Probe", "", "## Overall", "", "| Status | Count |", "| --- | ---: |"]
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## By Dataset", "", "| Dataset | Pass | Fail | Invalid | Error | Total |", "| --- | ---: | ---: | ---: | ---: | ---: |"])
    for dataset, counter in sorted(dataset_counts.items()):
        total = sum(counter.values())
        lines.append(f"| {dataset} | {counter.get('Pass', 0)} | {counter.get('Fail', 0)} | {counter.get('Invalid', 0)} | {counter.get('Error', 0)} | {total} |")
    lines.extend(["", "## Per Case", "", "| Dataset | File | Status | Best Attempt | Best Result | C File | WP Output | Trace |", "| --- | --- | --- | ---: | --- | --- | --- | --- |"])
    for record in records:
        c_file = record.get("successful_saved_file") or record.get("failed_saved_file", "")
        wp_output = record.get("failure_wp_output", "")
        trace_dir = record.get("trace_dir", "")
        lines.append(f"| {record['dataset']} | {record['filename']} | {record['final_status']} | {record.get('best_attempt', '')} | {record.get('best_result_type', '')} | {c_file} | {wp_output} | {trace_dir} |")
    (out_root / "baseline3_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_case_output(out_root: Path, case: Case) -> None:
    """Remove only the saved final output for one selected case."""

    success_file = successful_file_path(out_root, case)
    if success_file.exists():
        success_file.unlink()
    failure_dir = failed_case_dir(out_root, case)
    if failure_dir.exists():
        shutil.rmtree(failure_dir)
    trace_dir = trace_case_dir(out_root, case)
    if trace_dir.exists():
        shutil.rmtree(trace_dir)


def selected_dataset_label(cases: Iterable[Case]) -> str:
    """Return a stable filename label for the datasets included in one run."""

    datasets = sorted({case.dataset for case in cases})
    if not datasets:
        return "none"
    return "__".join(re.sub(r"[^A-Za-z0-9_.-]+", "_", dataset) for dataset in datasets)


def baseline3_console_path(out_root: Path, cases: Iterable[Case]) -> Path:
    """Console logs are scoped by dataset selection, not shared globally."""

    return out_root / f"baseline3_console_{selected_dataset_label(cases)}.txt"


def existing_output_records(autobench_dir: Path, out_root: Path, current_cases: Iterable[Case]) -> List[Dict[str, Any]]:
    """Load existing saved records for cases that were not part of this run."""

    current = {(case.dataset, case.filename) for case in current_cases}
    records: List[Dict[str, Any]] = []
    for case in discover_cases(autobench_dir, "all", 0, 0):
        if (case.dataset, case.filename) in current:
            continue
        record = resumed_record(case, out_root)
        if record is not None:
            trace_dir = trace_case_dir(out_root, case)
            if trace_dir.exists():
                record["trace_dir"] = str(trace_dir)
            records.append(record)
    return records


def main(argv: Optional[Sequence[str]] = None) -> int:
    #读取参数
    args = parse_args(argv)
    #找benchmark cases
    autobench_dir = Path(args.autobench_dir).resolve()
    out_root = Path(args.out_root).resolve()
    cases = discover_cases(autobench_dir, args.datasets, args.dataset_limit, args.limit)
    if args.dry_run:
        print(f"Selected {len(cases)} case(s)")
        for dataset, count in sorted(Counter(case.dataset for case in cases).items()):
            print(f"{dataset}: {count}")
        return 0
    out_root.mkdir(parents=True, exist_ok=True)
    console_path = baseline3_console_path(out_root, cases)
    if args.overwrite or not args.resume:
        for case in cases:
            clean_case_output(out_root, case)
        if console_path.exists():
            console_path.unlink()
    with RunLogger(console_path) as logger:
        client = LLMClient(load_model_config(Path(args.config).resolve(), args.model, args.override_base_url), logger.log)
        records: List[Dict[str, Any]] = existing_output_records(autobench_dir, out_root, cases)
        for index, case in enumerate(cases, 1):
            logger.log(f"[{index}/{len(cases)}] baseline3 {case.dataset}/{case.filename}")
            #每个case调用run_case函数
            records.append(run_case(args, client, case, out_root))
        #写最后的summary report
        write_reports(out_root, records)
        logger.log(f"Summary: {out_root / 'baseline3_summary.md'}")
        logger.log(f"Successful files: {out_root / 'successful_files'}")
        logger.log(f"Failed cases: {out_root / 'failed_cases'}")
        logger.log(f"Console log: {console_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
