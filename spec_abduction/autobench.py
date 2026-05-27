from __future__ import annotations

import re
from pathlib import Path
from typing import List, Tuple

from .types import Case


def natural_key(path: Path) -> Tuple[int, str]:
    """按题号数字排序，例如 2.c 排在 10.c 前面。"""

    match = re.search(r"\d+", path.name)
    return (int(match.group(0)) if match else 10**9, path.name)


def selected_datasets(root: Path, selector: str) -> List[str]:
    """根据 `--datasets` 参数选择需要运行的数据集。"""

    available = sorted(path.name for path in root.iterdir() if path.is_dir())
    if selector == "all":
        return available
    wanted = [item.strip() for item in selector.split(",") if item.strip()]
    missing = [item for item in wanted if item not in available]
    if missing:
        raise ValueError(f"Unknown datasets {missing}; available={available}")
    return wanted


def discover_cases(root: Path, selector: str, dataset_limit: int, limit: int) -> List[Case]:
    """枚举 AutoBench 题目。

    重要约束：只保留纯数字题号的 `.c` 文件。
    例如 `180.c` 会被纳入，`180_marked.c`、`180_infilled.c` 会被忽略。
    这保证派生样例不会被当作独立题目统计。
    """

    cases: List[Case] = []
    for dataset in selected_datasets(root, selector):
        files = sorted(
            [path for path in (root / dataset).glob("*.c") if re.fullmatch(r"\d+\.c", path.name)],
            key=natural_key,
        )
        if dataset_limit > 0:
            files = files[:dataset_limit]
        cases.extend(Case(dataset, path.name, path) for path in files)
    if limit > 0:
        cases = cases[:limit]
    return cases

