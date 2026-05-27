from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

from ..types import AttemptRecord, Case
from .few_shot import BASELINE2_FEW_SHOTS


FEEDBACK_CHAR_LIMIT = 12000


def is_failed_goal_block(block: str) -> bool:
    """判断一个 -wp-print goal block 是否值得反馈给 LLM。"""

    if not re.search(r"\breturns\s+(Failed|Timeout|Unknown)\b", block):
        return False
    if re.search(r"(?m)^\s*Prove:\s*true\.\s*$", block):
        return False
    return True


def compact_wp_stdout_for_feedback(stdout: str) -> str:
    """压缩 Frama-C/WP stdout, 只保留汇总和未证明 goal 的细节。"""

    if not stdout.strip():
        return ""
    summary_lines: List[str] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if (
            "[kernel]" in line
            or "[wp] Warning:" in line
            or "[wp] [Failure]" in line
            or "[wp] [Timeout]" in line
            or "[wp] [Unknown]" in line
            or "[wp] Proved goals:" in line
            or re.match(r"^(Failed|Timeout|Unknown):\s+", stripped)
        ):
            summary_lines.append(line)

    failed_blocks = [
        block.strip()
        for block in re.split(r"\n-{20,}\n", stdout)
        if is_failed_goal_block(block)
    ]
    parts: List[str] = []
    if summary_lines:
        parts.append("WP summary and warnings:\n" + "\n".join(summary_lines).strip())
    if failed_blocks:
        parts.append("Unproved goal details:\n" + "\n\n---\n\n".join(failed_blocks))
    return "\n\n".join(parts) if parts else stdout


"""限制反馈长度，避免 prompt 被单次 WP 输出撑爆。"""
def truncate_feedback(text: str, limit: int = FEEDBACK_CHAR_LIMIT) -> str:

    if len(text) <= limit:
        return text
    head = limit // 2
    tail = limit - head
    return text[:head] + "\n\n... [feedback truncated] ...\n\n" + text[-tail:]

"""把一次 attempt 转成可放进下一轮 prompt 的 verifier feedback。"""
def feedback_entry(record: AttemptRecord) -> Dict[str, Any]:

    feedback = {
        "status": record.status,
        "wp_result_type": record.wp_result_type,
        "wp_stdout": truncate_feedback(compact_wp_stdout_for_feedback(record.wp_stdout)),
        "wp_stderr": truncate_feedback(record.wp_stderr),
    }
    if record.error:
        feedback["error"] = record.error
    return feedback

"""构造 baseline2 的 feedback-guided prompt。"""
def build_feedback_repair_prompt(
    case: Case,
    source_code: str,
    attempt: int,
    previous_code: str,
    verifier_feedback: Optional[Dict[str, Any]],
) -> List[Dict[str, str]]:

    system = "You are an expert in ACSL and Frama-C/WP.Your job is to repair ACSL annotations using Frama-C/WP verifier feedback.You must preserve the executable C program exactly and only add, remove, or repair ACSL comments.Return JSON only. Do not output markdown, explanations, or code fences."
    user = {
        "task": (
        "Baseline2 feedback-guided ACSL repair: given source_code, previous_code, "
        "and verifier_feedback for previous_code, return a complete annotated C file "
        "whose ACSL specifications help Frama-C/WP prove the target assertions."
    ),
        "rules": [
        "Do not remove, weaken, or replace target assertions.",
        "Do not add impossible preconditions such as requires \\false.",
        "Do not restrict unknown_int or other nondeterministic inputs unless justified by the original task.",
        "If an assertion after a loop fails, repair the preceding loop invariant rather than changing the assertion.",
        "If invariant preservation fails, make the invariant inductive.",
        "Every loop must have  non-empty loop invariant and loop assigns.",
        "Do not use \\old inside loop invariants.",
        "For unknown_int, prefer assigns \\nothing and avoid strong ensures.",
        "Prefer minimal repairs to previous_code.",
        "Before returning, check ACSL syntax, target assertions, assigns clauses, and absence of WP internal names."
    ],
        "few_shot_examples": BASELINE2_FEW_SHOTS,
        "output_schema": {"code": "complete annotated C file", "notes": "optional short note"},
        "source_code": source_code,
        "previous_code": previous_code,
        "verifier_feedback": verifier_feedback or {},
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]



def build_feedback_prompt(
    case: Case,
    source_code: str,
    attempt: int,
    previous_code: str,
    verifier_feedback: Optional[Dict[str, Any]],
) -> List[Dict[str, str]]:
    return build_feedback_repair_prompt(case, source_code, attempt, previous_code, verifier_feedback)
