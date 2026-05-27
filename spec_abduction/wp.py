from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

from .types import WPResult


SUBPROCESS_TIMEOUT = 500

"""
对一个生成的 C+ACSL 文件运行 Frama-C/WP。这里使用和原 AutoSpec/probe 实验接近的 WP 参数：
- `-wp-precond-weakening`
- `-wp-no-callee-precond`
- 指定 prover 和 timeout
stdout/stderr 会写入文件，便于后续分析某个 attempt 为什么失败。
"""
def run_wp(frama_c: str, c_file: Path, out_dir: Path, label: str, wp_timeout: int, provers: str) -> WPResult:

    out_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = out_dir / f"{label}_wp_stdout.txt"
    stderr_path = out_dir / f"{label}_wp_stderr.txt"
    command = [
        frama_c,
        "-wp",
        "-wp-precond-weakening",
        "-wp-no-callee-precond",
        "-wp-prover",
        provers,
        "-wp-prop=-@terminates,-@variant,-@decreases",
        "-wp-print",
        "-wp-timeout",
        str(wp_timeout),
        str(c_file),
    ]
    start = dt.datetime.now()
    try:
        # 不使用 check=True，因为 Frama-C 返回非零并不一定代表脚本层面崩溃；
        # 需要读取 stdout 来判断 Pass/Fail/Invalid。
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=SUBPROCESS_TIMEOUT, check=False)
        stdout = proc.stdout.decode("utf-8", errors="replace")
        stderr = proc.stderr.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired as exc:
        # 这是整个 frama-c 进程超时，不是单个 prover 的 -wp-timeout。
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace") + f"\nsubprocess timeout after {SUBPROCESS_TIMEOUT}s"
    elapsed = (dt.datetime.now() - start).total_seconds()
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return WPResult(get_result_type(stdout + "\n" + stderr), str(stdout_path), str(stderr_path), stdout, stderr, elapsed, command)

"""
把 Frama-C/WP stdout 解析成粗粒度结果。
返回值：
- `Pass_x_y`: y 个 goal 中 x 个证明成功，且 x == y
- `Fail_x_y`: 有 WP goal,但未全部证明
- `Invalid`: ACSL/C 输入非法,Frama-C 无法正常验证；
- `UK`: 输出格式无法识别。
"""
def get_result_type(wp_stdout: str) -> str:

    for line in wp_stdout.splitlines():
        if (
            "[kernel] Frama-C aborted:" in line
            or "[kernel] Plug-in wp aborted" in line
            or "[wp] Warning: No goal generated" in line
            or "error: invalid preprocessing directive" in line
            or "warning annot-error treated as fatal error" in line
        ):
            return "Invalid"
        if "[wp] Proved goals:" in line:
            left, right = line.split(":")[-1].split("/")
            proved, total = int(left.strip()), int(right.strip())
            if proved == total:
                return f"Pass_{proved}_{total}"
            return f"Fail_{proved}_{total}"
    return "UK"

"""
给 attempt 排序用的分数。
Pass 永远最高,Fail 根据 proved/total 比例排序,Invalid 比 Fail 低。
这样即使 5 次都不通过，也能保存一个最接近通过的版本对应的 WP 输出。
"""
def result_score(result_type: str) -> float:

    if result_type.startswith("Pass_"):
        return 10000.0
    match = re.match(r"Fail_(\d+)_(\d+)", result_type)
    if match:
        proved, total = int(match.group(1)), int(match.group(2))
        return 1000.0 + (proved / total if total else 0.0)
    if result_type == "UK":
        return 100.0
    if result_type == "Invalid":
        return 0.0
    return -1.0

"""把 WP result_type 映射成用户报告中的状态。"""
def attempt_status(result_type: str) -> str:

    if result_type.startswith("Pass_"):
        return "Pass"
    if result_type.startswith("Fail_"):
        return "Fail"
    if result_type == "Invalid":
        return "Invalid"
    return "Error"

