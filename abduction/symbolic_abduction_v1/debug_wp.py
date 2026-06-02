from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .backend import generate_abductive_facts
from .wp_goal import load_first_failed_goal


def main() -> int:
    """命令行调试入口：读取 wp.txt，输出 abduction 候选 JSON。"""

    parser = argparse.ArgumentParser(description="Run isolated symbolic abduction on a saved wp.txt.")
    parser.add_argument("wp_txt", type=Path)
    parser.add_argument("--visible", default="", help="Comma-separated source-level identifiers.")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--max-size", type=int, default=2, help="Maximum number of abducible literals in one conjunction.")
    parser.add_argument("--max-combo-candidates", type=int, default=40, help="Top nontrivial literals kept for conjunction search.")
    parser.add_argument("--z3", default="/opt/z3-4.7.1/bin/z3")
    args = parser.parse_args()

    # 先把 WP failed goal 解析成 A 和 G，再把用户显式给出的变量作为候选生成范围。
    goal = load_first_failed_goal(args.wp_txt)
    visible = [item.strip() for item in args.visible.split(",") if item.strip()] or None
    facts = generate_abductive_facts(goal, visible, args.max_results, args.max_size, args.max_combo_candidates, args.z3)
    # ensure_ascii=False 保留中文 reason 或后续中文字段时的可读性。
    print(json.dumps([asdict(fact) for fact in facts], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
