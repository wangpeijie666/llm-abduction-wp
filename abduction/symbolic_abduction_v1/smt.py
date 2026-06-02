from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List

from .linear import Atom, collect_vars


class Z3Cli:
    """通过命令行调用 Z3。

    当前环境没有依赖 Python z3-solver，因此这里生成临时 .smt2 文件，
    再调用外部 z3 可执行文件做 check-sat。
    """

    def __init__(self, executable: str = "/opt/z3-4.7.1/bin/z3") -> None:
        """记录 Z3 可执行文件路径。"""
        self.executable = executable

    def check(self, assertions: Iterable[str], variables: Iterable[str]) -> str:
        """检查一组 SMT assertion 的可满足性。

        assertions 是已经转好的 SMT-LIB 布尔表达式字符串；
        variables 是需要声明成 Int 的变量名。返回 sat/unsat/unknown。
        """

        script = ["(set-logic QF_LIA)"]
        for var in sorted(set(variables)):
            script.append(f"(declare-const {var} Int)")
        script.extend(f"(assert {assertion})" for assertion in assertions)
        script.append("(check-sat)")
        # NamedTemporaryFile(delete=False) 让 Z3 可以通过路径读取文件；
        # finally 中会手动删除，避免留下临时 .smt2。
        with tempfile.NamedTemporaryFile("w", suffix=".smt2", delete=False, encoding="utf-8") as handle:
            handle.write("\n".join(script) + "\n")
            temp_path = Path(handle.name)
        try:
            completed = subprocess.run(
                [self.executable, str(temp_path)],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        finally:
            temp_path.unlink(missing_ok=True)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
        return completed.stdout.strip().splitlines()[0]


def atom_vars(atoms: Iterable[Atom]) -> List[str]:
    """兼容性小包装：收集一组 Atom 中的变量。"""
    return collect_vars(atoms)
