from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, List, Sequence

from .linear import Atom, LinExpr, collect_vars
from .smt import Z3Cli
from .wp_goal import ParsedGoal


@dataclass
class AbductiveFact:
    """一个 abduction 输出候选。

    predicate 是候选事实 H 的文本；size 表示 H 中包含几个 literal。
    sufficient/consistent/already_known/restates_goal 分别记录 SMT 检查结果。
    """

    predicate: str
    sufficient: bool
    consistent: bool
    already_known: bool
    restates_goal: bool
    size: int
    score: float
    reason: str


def _const_range(goal: ParsedGoal) -> List[int]:
    """根据当前 VC 里出现的常数，构造一个小的候选常数范围。"""

    constants = {0, -1, 1, 2}
    for atom in [*goal.assumptions, goal.goal]:
        constants.add(atom.left.const)
        constants.add(atom.right.const)
    low = min(constants) - 3
    high = max(constants) + 3
    return list(range(low, high + 1))


def generate_abducibles(goal: ParsedGoal, visible_identifiers: Sequence[str] | None = None) -> List[Atom]:
    """生成有限的 GPiD-style QF_LIA 候选 literal 空间。

    V1 不做无限制模板搜索，只枚举变量之间的 <、<= 关系，以及变量与常数边界。
    """

    variables = list(visible_identifiers or collect_vars([*goal.assumptions, goal.goal]))
    constants = _const_range(goal)
    candidates: List[Atom] = []
    # 枚举变量两两之间的差分约束，例如 i + k <= j、j + k < i。
    for left_var, right_var in combinations(variables, 2):
        left = LinExpr.var(left_var)
        right = LinExpr.var(right_var)
        for offset in constants:
            candidates.append(Atom(left + LinExpr.num(offset), "<=", right))
            candidates.append(Atom(right + LinExpr.num(offset), "<=", left))
            candidates.append(Atom(left + LinExpr.num(offset), "<", right))
            candidates.append(Atom(right + LinExpr.num(offset), "<", left))
    # 枚举单变量上下界，例如 0 <= i、i <= 10。
    for var in variables:
        expr = LinExpr.var(var)
        for bound in constants:
            candidates.append(Atom(LinExpr.num(bound), "<=", expr))
            candidates.append(Atom(expr, "<=", LinExpr.num(bound)))
    # 把目标本身也放入候选，便于标记“只是重述目标”的解释。
    candidates.append(goal.goal)
    unique = {}
    for atom in candidates:
        unique.setdefault(atom.normalized_key(), atom)
    return list(unique.values())


def _check(
    solver: Z3Cli,
    atoms: Iterable[Atom],
    extra_assertions: Iterable[str] = (),
    variables: Iterable[str] | None = None,
) -> str:
    """调用 Z3 检查 atoms 和额外 SMT assertion 的可满足性。"""

    atom_list = list(atoms)
    # 有些变量只出现在候选或 goal 里，不一定出现在 assumptions 里；
    # 因此调用方可以显式传入完整变量集合。
    declared = list(variables) if variables is not None else collect_vars(atom_list)
    return solver.check([*(atom.smt() for atom in atom_list), *extra_assertions], declared)


def _score(atom: Atom, goal: ParsedGoal, already_known: bool, restates_goal: bool) -> float:
    """给单 literal 候选打一个启发式分数，用于排序输出。"""

    shared_goal_vars = len(set(atom.vars()) & set(goal.goal.vars()))
    coeff_size = sum(abs(coeff) for expr in (atom.left, atom.right) for _, coeff in expr.coeffs)
    const_size = abs(atom.left.const) + abs(atom.right.const)
    score = 10.0 + shared_goal_vars * 2.0 - coeff_size * 0.2 - const_size * 0.05
    if already_known:
        score -= 5.0
    if restates_goal:
        score -= 3.0
    return score


def _score_combo(atoms: Sequence[Atom], goal: ParsedGoal, already_known: bool, restates_goal: bool) -> float:
    """给多 literal 合取候选打分，并轻微惩罚更大的解释。"""

    if not atoms:
        return 0.0
    score = sum(_score(atom, goal, False, False) for atom in atoms) / len(atoms)
    score -= (len(atoms) - 1) * 1.5
    if already_known:
        score -= 5.0
    if restates_goal:
        score -= 3.0
    return score


def _predicate_text(atoms: Sequence[Atom]) -> str:
    """把 H1, H2, ... 格式化成 ACSL 风格的合取文本。"""

    return " /\\ ".join(atom.acsl() for atom in atoms)


def _combo_key(atoms: Sequence[Atom]) -> frozenset[str]:
    """把一个候选合取转成无序 key，用于去重和最小性过滤。"""

    return frozenset(atom.normalized_key() for atom in atoms)

"""
寻找 bounded-size 的事实 H,使得 assumptions ∧ H 可以推出 goal。
"""
def generate_abductive_facts(
    goal: ParsedGoal,
    visible_identifiers: Sequence[str] | None = None,
    max_results: int = 20,
    max_size: int = 2,
    max_combo_candidates: int = 40,
    z3_path: str = "/opt/z3-4.7.1/bin/z3",
) -> List[AbductiveFact]:

    if max_size < 1:
        raise ValueError("max_size must be at least 1")
    if max_combo_candidates < 1:
        raise ValueError("max_combo_candidates must be at least 1")

    solver = Z3Cli(z3_path)
    results: List[AbductiveFact] = []
    base = goal.assumptions
    candidates = generate_abducibles(goal, visible_identifiers)
    sufficient_keys: List[frozenset[str]] = []
    combo_pool: List[Atom] = []

    # 第一阶段：逐个检查单 literal H。
    # 这里会找出已经足够的解释，也会筛掉矛盾或已知事实。
    for candidate in candidates:
        combo = (candidate,)
        combo_keys = _combo_key(combo)
        variables = collect_vars([*base, candidate, goal.goal])
        # consistent: A /\ H 必须 SAT，否则 H 与已知假设冲突。
        consistent = _check(solver, [*base, candidate], variables=variables) == "sat"
        if not consistent:
            continue
        # already_known: 如果 A /\ not(H) UNSAT，说明 H 已经被 A 蕴含。
        already_known = _check(solver, base, [candidate.neg_smt()], variables=variables) == "unsat"
        restates_goal = candidate.normalized_key() == goal.goal.normalized_key()
        # sufficient: A /\ H /\ not(G) UNSAT，等价于 A /\ H => G。
        sufficient = _check(solver, [*base, candidate], [goal.goal.neg_smt()], variables=variables) == "unsat"
        if sufficient:
            sufficient_keys.append(combo_keys)
            reason = "assumptions and this abducible make the negated goal unsatisfiable"
            if restates_goal:
                reason += "; this fact contains the goal and should be treated cautiously"
            elif already_known:
                reason += "; this fact is already entailed by assumptions"
            results.append(
                AbductiveFact(
                    predicate=candidate.acsl(),
                    sufficient=sufficient,
                    consistent=consistent,
                    already_known=already_known,
                    restates_goal=restates_goal,
                    size=1,
                    score=_score(candidate, goal, already_known, restates_goal),
                    reason=reason,
                )
            )
        elif not already_known:
            # 单独不够强、但 consistent 且非 already-known 的 literal，才进入多 literal 组合池。
            combo_pool.append(candidate)

    # 为了控制组合爆炸，只保留启发式分数最高的一部分 literal 做 H1 /\ H2 搜索。
    combo_pool.sort(key=lambda atom: _score(atom, goal, False, atom.normalized_key() == goal.goal.normalized_key()), reverse=True)
    combo_pool = combo_pool[:max_combo_candidates]

    # 第二阶段：搜索 H1 /\ H2 / ... 形式的多 literal 候选。
    for size in range(2, max_size + 1):
        for combo in combinations(combo_pool, size):
            combo_keys = _combo_key(combo)
            # 如果某个子集已经足够，当前 combo 只是它的超集，不再输出。
            if any(known.issubset(combo_keys) for known in sufficient_keys):
                continue
            variables = collect_vars([*base, *combo, goal.goal])
            consistent = _check(solver, [*base, *combo], variables=variables) == "sat"
            if not consistent:
                continue
            # combo_pool 已经过滤掉单 literal already-known；这里暂不额外证明整个合取 already-known。
            already_known = False
            restates_goal = goal.goal.normalized_key() in combo_keys
            sufficient = _check(solver, [*base, *combo], [goal.goal.neg_smt()], variables=variables) == "unsat"
            if not sufficient:
                continue
            sufficient_keys.append(combo_keys)
            reason = "assumptions and this abducible conjunction make the negated goal unsatisfiable"
            if restates_goal:
                reason += "; this fact contains the goal and should be treated cautiously"
            elif already_known:
                reason += "; this fact is already entailed by assumptions"
            results.append(
                AbductiveFact(
                    predicate=_predicate_text(combo),
                    sufficient=sufficient,
                    consistent=consistent,
                    already_known=already_known,
                    restates_goal=restates_goal,
                    size=size,
                    score=_score_combo(combo, goal, already_known, restates_goal),
                    reason=reason,
                )
            )
    results.sort(key=lambda item: item.score, reverse=True)
    return results[:max_results]
