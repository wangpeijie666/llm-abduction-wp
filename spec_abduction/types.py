from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Case:
    """一个待处理的 benchmark 题目。"""

    dataset: str
    filename: str
    source_path: Path


@dataclass
class WPResult:
    """一次 Frama-C/WP 验证的完整结果。

    除了粗粒度的 `result_type`，还保留 stdout/stderr 内容和完整命令，
    这样失败时可以把必要的 WP 输出写入最终目录。
    """

    result_type: str
    stdout_path: str
    stderr_path: str
    stdout: str
    stderr: str
    elapsed_sec: float
    command: List[str]


@dataclass
class AttemptRecord:
    """单个题目的某一次 LLM 生成 attempt 的结果记录。

    baseline1 允许每题多次独立生成；每个 attempt 都会生成一个临时 C 文件并跑 WP。
    最终会根据 `score` 选择最佳 attempt，但不会持久化每次 LLM 生成文件。
    """

    dataset: str
    filename: str
    attempt: int
    generated_file: str
    wp_result_type: str
    wp_stdout_path: str
    wp_stderr_path: str
    status: str
    score: float
    wp_stdout: str = ""
    wp_stderr: str = ""
    wp_command: Optional[List[str]] = None
    code: str = ""
    error: str = ""
