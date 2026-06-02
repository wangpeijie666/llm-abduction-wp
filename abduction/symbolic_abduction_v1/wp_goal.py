from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .linear import Atom, ParseError, parse_atom, split_conjunction


@dataclass
class ParsedGoal:
    """从一个 WP failed goal 中抽出的 abduction 输入。

    assumptions 是 A，goal 是 G；raw_* 字段保留原始文本，方便调试解析问题。
    """

    assumptions: List[Atom]
    goal: Atom
    raw_assumptions: str
    raw_goal: str


def parse_wp_goal_text(goal_text: str) -> ParsedGoal:
    """解析 V1 abduction 后端需要的 WP goal 小片段。"""

    # WP 详细输出通常是：
    #   Assume { ... }
    #   Prove: ...
    #   Prover ... returns ...
    # 这里用正则只取 Assume 和 Prove 的主体。
    assume_match = re.search(r"Assume\s*\{(?P<body>.*?)\}\s*Prove:", goal_text, re.DOTALL)
    prove_match = re.search(r"Prove:\s*(?P<body>.*?)(?:\nProver|\Z)", goal_text, re.DOTALL)
    if not prove_match:
        raise ParseError("missing Prove block")
    raw_assumptions = assume_match.group("body") if assume_match else ""
    raw_goal = prove_match.group("body").strip()
    assumptions: List[Atom] = []
    for line in raw_assumptions.splitlines():
        stripped = line.strip()
        # V1 只使用 Have: 行；Type:、注释和复杂 predicate 暂时跳过。
        if not stripped.startswith("Have:"):
            continue
        body = stripped.split("Have:", 1)[1].strip()
        for part in split_conjunction(body):
            try:
                assumptions.append(parse_atom(part))
            except ParseError:
                # 不支持的 ACSL/WP 片段不要近似翻译，直接跳过，避免引入错误语义。
                continue
    return ParsedGoal(assumptions=assumptions, goal=parse_atom(raw_goal), raw_assumptions=raw_assumptions, raw_goal=raw_goal)


def extract_first_failed_goal_text(wp_txt: str) -> str:
    """从 wp.txt 中抽取第一个 Failed/Timeout/Unknown 的详细 Goal block。"""

    blocks: List[str] = []
    current: List[str] = []
    for line in wp_txt.splitlines():
        # WP 输出以 Goal ... 开始一个证明目标，以分隔线或下一个 Goal 结束。
        if line.startswith("Goal "):
            if current:
                blocks.append("\n".join(current).strip())
            current = [line]
        elif current:
            if line.startswith("------------------------------------------------------------"):
                blocks.append("\n".join(current).strip())
                current = []
            else:
                current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    for block in blocks:
        if re.search(r"returns\s+(Failed|Timeout|Unknown)", block, re.IGNORECASE):
            return block
    raise ParseError("no failed Goal block found")


def load_first_failed_goal(path: Path) -> ParsedGoal:
    """从文件加载并解析第一个失败目标。"""
    return parse_wp_goal_text(extract_first_failed_goal_text(path.read_text(encoding="utf-8", errors="replace")))
