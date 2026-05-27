from __future__ import annotations

import re
from typing import List, Optional


class GeneratedCodeError(ValueError):
    """LLM 返回了代码，但代码不满足实验约束。"""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.code = code


def strip_c_comments(source: str) -> str:
    """移除 C/ACSL 注释，用于比较真实 C 语句是否被改动。"""

    without_blocks = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)
    return re.sub(r"//.*", "", without_blocks)


def normalize_assertion(text: str) -> str:
    """把 ACSL assertion 谓词规范化，便于比较是否被保留。"""

    normalized = re.sub(r"\s+", "", text).rstrip(";")
    while has_wrapping_parentheses(normalized):
        normalized = normalized[1:-1]
    return normalized


def has_wrapping_parentheses(text: str) -> bool:
    """判断最外层括号是否包住整个表达式。"""

    if not (text.startswith("(") and text.endswith(")")):
        return False
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(text) - 1:
                return False
            if depth < 0:
                return False
    return depth == 0


def extract_acsl_assertions(source: str, allow_malformed_line_marker: bool = False) -> List[str]:
    """提取源码中的 ACSL assert 谓词。"""

    assertions: List[str] = []
    line_marker = r"//[ \t]*@" if allow_malformed_line_marker else r"//@"
    for match in re.finditer(rf"(?m)^[ \t]*{line_marker}[ \t]*assert\s*(.*?);", source):
        assertions.append(normalize_assertion(match.group(1)))
    for match in re.finditer(r"/\*@\s*assert\s*(.*?);\s*\*/", source, flags=re.DOTALL):
        assertions.append(normalize_assertion(match.group(1)))
    return [item for item in assertions if item]


def function_body_fingerprints(source: str) -> List[str]:
    """提取顶层函数体并做空白无关的指纹。

    该校验允许 LLM 添加 ACSL 注释、函数契约、include 或 prototype，但不允许
    改写函数体中的可执行 C 语句。
    """

    text = strip_c_comments(source)
    bodies: List[str] = []
    depth = 0
    start: Optional[int] = None
    for index, char in enumerate(text):
        if char == "{":
            if depth == 0:
                prefix = text[:index].rstrip()
                if prefix.endswith(")") or re.search(r"\)\s*$", prefix):
                    start = index + 1
                else:
                    start = None
            depth += 1
        elif char == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    bodies.append(re.sub(r"\s+", "", text[start:index]))
                    start = None
    return bodies


def validate_executable_code_unchanged(original: str, generated: str) -> None:
    """确认 LLM 没有改写函数体中的真实 C 代码。"""

    original_bodies = function_body_fingerprints(original)
    generated_bodies = function_body_fingerprints(generated)
    if original_bodies != generated_bodies:
        raise ValueError("LLM changed executable C code; only ACSL/comments are allowed")


def validate_original_assertions_preserved(original: str, generated: str) -> None:
    """确认原始 ACSL assertions 没有被 LLM 删除或改写。"""

    original_assertions = extract_acsl_assertions(original, allow_malformed_line_marker=True)
    generated_assertions = extract_acsl_assertions(generated, allow_malformed_line_marker=False)
    missing = [item for item in original_assertions if item not in generated_assertions]
    if missing:
        raise ValueError(f"LLM removed or changed original ACSL assertions: {missing[:3]}")


def validate_generated_code(source_code: str, code: str) -> None:
    """校验 LLM 生成代码满足 baseline 的基本约束。"""

    try:
        validate_executable_code_unchanged(source_code, code)
        validate_original_assertions_preserved(source_code, code)
    except ValueError as exc:
        raise GeneratedCodeError(str(exc), code) from exc


def add_probe_markers(source: str) -> str:
    """可选地给循环前插入 PROBE_HERE marker。

    baseline1 本身不依赖 assertion probe；这个功能只用于后续你想把某个
    baseline1 生成结果继续交给 baseline3/abduction 流程时定位插入点。
    默认不开启，只有传 `--add-probe-markers` 才会使用。
    """

    if "PROBE_HERE" in source:
        return source if source.endswith("\n") else source + "\n"
    out: List[str] = []
    loop_index = 0
    for line in source.splitlines():
        if not line.strip().startswith(("//", "/*", "*")) and re.search(r"\b(?:for|while)\s*\(", line):
            loop_index += 1
            indent = re.match(r"\s*", line).group(0)
            out.append(f"{indent}/* PROBE_HERE:loop{loop_index}_before */")
        out.append(line)
    return "\n".join(out) + "\n"

