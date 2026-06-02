from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class LinExpr:
    """简单整数线性表达式，例如 i、10、i + 1、i - j + 2。

    coeffs 保存变量系数，const 保存常数项。比如 i - 2*j + 3 表示为：
    coeffs=(("i", 1), ("j", -2)), const=3。
    """

    coeffs: Tuple[Tuple[str, int], ...] = ()
    const: int = 0

    @staticmethod
    def var(name: str) -> "LinExpr":
        """构造一个变量表达式。"""
        return LinExpr(((name, 1),), 0)

    @staticmethod
    def num(value: int) -> "LinExpr":
        """构造一个整数常量表达式。"""
        return LinExpr((), value)

    def __add__(self, other: "LinExpr") -> "LinExpr":
        """合并两个线性表达式，并把同名变量系数相加。"""
        values: Dict[str, int] = dict(self.coeffs)
        for name, coeff in other.coeffs:
            values[name] = values.get(name, 0) + coeff
        return LinExpr(tuple(sorted((name, coeff) for name, coeff in values.items() if coeff)), self.const + other.const)

    def __neg__(self) -> "LinExpr":
        return LinExpr(tuple((name, -coeff) for name, coeff in self.coeffs), -self.const)

    def __sub__(self, other: "LinExpr") -> "LinExpr":
        return self + (-other)

    def vars(self) -> List[str]:
        """返回表达式里出现过的变量名。"""
        return [name for name, _ in self.coeffs]

    def smt(self) -> str:
        """把表达式转成 SMT-LIB 语法，供 Z3 使用。"""
        parts: List[str] = []
        for name, coeff in self.coeffs:
            if coeff == 1:
                parts.append(name)
            elif coeff == -1:
                parts.append(f"(- {name})")
            else:
                parts.append(f"(* {coeff} {name})")
        if self.const:
            parts.append(str(self.const))
        if not parts:
            return "0"
        if len(parts) == 1:
            return parts[0]
        return f"(+ {' '.join(parts)})"

    def acsl(self) -> str:
        """把表达式转成接近 ACSL 的文本，供输出候选事实使用。"""
        pieces: List[str] = []
        for name, coeff in self.coeffs:
            if coeff == 1:
                pieces.append(name)
            elif coeff == -1:
                pieces.append(f"-{name}")
            else:
                pieces.append(f"{coeff}*{name}")
        if self.const:
            pieces.append(str(self.const))
        if not pieces:
            return "0"
        text = " + ".join(pieces)
        return text.replace("+ -", "- ")


@dataclass(frozen=True)
class Atom:
    """一个线性原子谓词，例如 i + 1 <= j 或 j == 10。"""

    left: LinExpr
    op: str
    right: LinExpr

    def vars(self) -> List[str]:
        """返回谓词左右两边出现过的变量名。"""
        return sorted(set(self.left.vars() + self.right.vars()))

    def smt(self) -> str:
        """把原子谓词转成 SMT-LIB assertion 里的布尔表达式。"""
        op = "=" if self.op == "==" else self.op
        return f"({op} {self.left.smt()} {self.right.smt()})"

    def acsl(self) -> str:
        """把原子谓词转成接近 ACSL 的可读文本。"""
        op = "==" if self.op in {"=", "=="} else self.op
        return f"{self.left.acsl()} {op} {self.right.acsl()}"

    def neg_smt(self) -> str:
        """返回该谓词在 SMT-LIB 中的否定形式。"""
        return f"(not {self.smt()})"

    def normalized_key(self) -> str:
        """生成去空格的稳定 key，用于去重和判断是否重述目标。"""
        return self.acsl().replace(" ", "")


class ParseError(ValueError):
    pass


def _strip_outer_parens(text: str) -> str:
    """去掉包住整个表达式的最外层括号。"""
    text = text.strip()
    while text.startswith("(") and text.endswith(")"):
        depth = 0
        balanced = True
        for index, char in enumerate(text):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0 and index != len(text) - 1:
                    balanced = False
                    break
        if not balanced:
            break
        text = text[1:-1].strip()
    return text


def _split_top_level(text: str, operator: str) -> Optional[Tuple[str, str]]:
    """只在顶层按 operator 切分，避免切开括号内部的表达式。"""
    depth = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif depth == 0 and char == operator:
            return text[:index], text[index + 1 :]
    return None


def parse_linexpr(text: str) -> LinExpr:
    """解析当前原型支持的简单线性整数表达式。"""
    text = _strip_outer_parens(text)
    if not text:
        raise ParseError("empty expression")
    # 先处理顶层加减法，再落到数字或变量；这里不是完整 parser，只覆盖 WP 常见小片段。
    split = _split_top_level(text, "+")
    if split is not None:
        return parse_linexpr(split[0]) + parse_linexpr(split[1])
    split = _split_top_level(text, "-")
    if split is not None and split[0].strip():
        return parse_linexpr(split[0]) - parse_linexpr(split[1])
    if text.startswith("-"):
        return -parse_linexpr(text[1:])
    if text.lstrip("-").isdigit():
        return LinExpr.num(int(text))
    if text.isidentifier():
        return LinExpr.var(text)
    raise ParseError(f"unsupported linear expression: {text}")


def parse_atom(text: str) -> Atom:
    """解析一个线性比较谓词。"""
    text = _strip_outer_parens(text.strip().rstrip(".;"))
    for op in ("<=", ">=", "==", "=", "<", ">"):
        depth = 0
        for index in range(len(text) - len(op) + 1):
            char = text[index]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            if depth == 0 and text[index : index + len(op)] == op:
                left = text[:index]
                right = text[index + len(op) :]
                return Atom(parse_linexpr(left), "==" if op == "=" else op, parse_linexpr(right))
    raise ParseError(f"unsupported atom: {text}")


def split_conjunction(text: str) -> List[str]:
    """按顶层 /\\ 拆分合取公式，括号内部的 /\\ 不会被拆开。"""
    parts: List[str] = []
    current: List[str] = []
    depth = 0
    index = 0
    while index < len(text):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
        if depth == 0 and text[index : index + 2] == "/\\":
            part = "".join(current).strip()
            if part:
                parts.append(part)
            current = []
            index += 2
            continue
        current.append(text[index])
        index += 1
    part = "".join(current).strip()
    if part:
        parts.append(part)
    return parts


def collect_vars(atoms: Iterable[Atom]) -> List[str]:
    """收集一组原子谓词中出现过的所有变量名。"""
    names = set()
    for atom in atoms:
        names.update(atom.vars())
    return sorted(names)
