from __future__ import annotations

import json
from typing import Dict, List

from ..types import Case
from .few_shot import BASELINE1_FEW_SHOTS


def build_direct_generation_prompt(case: Case, source_code: str, attempt: int) -> List[Dict[str, str]]:
    """
    构造 baseline1 的直接生成 prompt。注意这里没有 verifier feedback,也不会提及上一轮失败原因。
    """

    system = """
    You are an expert in ACSL and Frama-C/WP.
    Your job is to add sound, verification-oriented ACSL annotations to a C program.
    This is a direct-generation baseline: no verifier feedback is available.
    You must preserve the executable C program exactly and only add, remove, or repair ACSL comments.
    Return JSON only. Do not output markdown, explanations, or code fences.
    """
    user = {
        "task": (
            "Baseline1 direct ACSL generation: given source_code only, return a complete "
            "annotated C file with ACSL specifications that help Frama-C/WP prove the "
            "target assertions, without using verifier feedback."
        ),
        "rules": [
            "Return the complete C file as JSON field code.",
            "Return valid JSON only.",
            "Preserve executable C code exactly. Only add, remove, or repair ACSL comments.",
            "Do not use verifier feedback; this is a direct-generation baseline.",
            "Correct malformed assertions written as '// @ assert P;' to '//@ assert P;'.",
            "Do not remove, weaken, rename, or replace target assertions.",
            "Do not turn target assertions into assumptions.",
            "Do not add impossible or contradictory annotations such as requires \\false, assumes \\false, assert \\false, or contradictory invariants.",
            "Do not restrict nondeterministic inputs unless explicitly required by the original source code or target property.",
            "For unknown_int or similar nondeterministic helpers, prefer assigns \\nothing; and avoid strong ensures clauses.",
            "Add valid function contracts when useful, especially assigns clauses.",
            "Add non-empty loop invariant and loop assigns blocks before every for/while loop.",
            "Every loop invariant should be inductive: true before the loop and preserved by one iteration.",
            "If an assertion after a loop needs a fact, prefer adding that fact as a loop invariant.",
            "Loop assigns must include every variable or memory location modified by the loop body.",
            "Do not use \\old inside loop invariants.",
            "Do not use WP internal SSA/memory names.",
            "Do not add loop variant/decreases clauses; this baseline checks partial correctness.",
            "Prefer concise source-level invariants: bounds, loop-counter relations, frame conditions, and simple quantified array facts.",
            "If unsure, generate conservative invariants that are likely true rather than strong unsound invariants.",
            "Use valid ACSL syntax accepted by Frama-C/WP.",
            "Never output empty ACSL blocks."
        ],
        "few_shot_examples": BASELINE1_FEW_SHOTS,
        "output_schema": {"code": "complete annotated C file", "notes": "optional short note"},
        "source_code": source_code,
    }
    return [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(user, ensure_ascii=False)}]



def build_prompt(case: Case, source_code: str, attempt: int) -> List[Dict[str, str]]:
    return build_direct_generation_prompt(case, source_code, attempt)
