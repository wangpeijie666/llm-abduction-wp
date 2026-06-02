# Symbolic Abduction V1

这是一个隔离版的符号 abduction 原型，用来在 Frama-C/WP 的失败证明目标上复现 GPiD-style abduction 的核心思想。

它目前没有接入 `scripts/run_baseline3.py`，也不会影响现有 baseline pipeline。这个目录的定位是实验沙盒：先把“从 failed VC 中符号化找缺失事实”这件事做清楚，再考虑接入 baseline3的spec repair替代baseline3里面用LLM找缺失事实的方法。

## 核心目标

给定一个 WP 失败目标：

```text
Assume {
  A
}
Prove:
  G
```

本原型搜索一个候选事实 `H`，使得：

```text
A /\ H => G
```

等价地，用 SMT 检查：

```text
A /\ H /\ not(G)  UNSAT
```

如果这个公式不可满足，说明补上 `H` 后，当前失败目标 `G` 可以被推出。

`H` 可以是单个 literal：

```text
i + 1 <= j
```

也可以是 bounded-size 合取：

```text
i <= j /\ j <= i
```

默认最大大小是 2，也就是搜索 `H` 和 `H1 /\ H2`。

## 目录结构

```text
abduction/symbolic_abduction_v1/
├── README.md
├── __init__.py
├── linear.py
├── wp_goal.py
├── smt.py
├── backend.py
└── debug_wp.py
```

各文件职责如下：

```text
linear.py
  定义简单线性整数表达式和原子谓词。
  负责把 WP 文本里的 i + 1 <= j 这类约束解析成内部结构，并能转成 SMT-LIB 或 ACSL 风格文本。

wp_goal.py
  从 wp.txt 中抽取第一个 Failed/Timeout/Unknown 的 Goal block。
  解析 Assume { Have: ... } 和 Prove: ...，得到 assumptions A 和 goal G。

smt.py
  封装 Z3 CLI。
  生成临时 .smt2 文件，调用 /opt/z3-4.7.1/bin/z3 做 check-sat。

backend.py
  abduction 主逻辑。
  生成候选 H，检查 consistent / already_known / sufficient / restates_goal，排序后输出候选事实。

debug_wp.py
  命令行调试入口。
  输入一个保存好的 wp.txt，输出 JSON 格式的 abduction 候选。
```

## 数据流

整体流程是：

```text
wp.txt
  -> extract_first_failed_goal_text
  -> parse_wp_goal_text
  -> ParsedGoal(assumptions=A, goal=G)
  -> generate_abducibles
  -> generate_abductive_facts
  -> JSON 输出
```

其中 `ParsedGoal` 是后端的主要输入：

```python
ParsedGoal(
    assumptions=[...],
    goal=...,
    raw_assumptions="...",
    raw_goal="...",
)
```

`assumptions` 对应 WP 里的 `A`，`goal` 对应 `G`。

## 支持的公式片段

当前版本只支持简单的整数线性片段，也就是 QF_LIA 的很小子集。

支持的表达式例子：

```text
i
j
10
-1
i + 1
j - 2
```

支持的原子谓词例子：

```text
i <= j
i < j
i == j
i + 1 <= j
j <= 10
0 <= i
```

支持解析 WP 中的 `Have:` 行，例如：

```text
Have: 0 < i.
Have: j <= 10.
Have: i <= (2 + j).
Prove: i < j.
```

不支持的 ACSL/WP 构造会被跳过，而不是近似翻译。这样做是为了避免把不理解的公式错误地转成另一个语义。

当前不支持：

```text
array
pointer
quantifier
function call
nonlinear arithmetic
复杂 ACSL predicate
完整 C/ACSL AST
```

## 候选 H 如何生成

`backend.py` 中的 `generate_abducibles()` 会生成有限的候选 literal 空间。

变量来源有两种：

```text
1. 用户通过 --visible 显式指定，例如 --visible i,j
2. 如果没有指定，则从 assumptions 和 goal 中自动收集
```

常数范围来自当前 VC 中出现过的常数附近。例如目标里出现 `0`、`1`、`2`，候选会在这些常数附近扩展一小段。

对变量 `i,j`，会生成类似：

```text
i + k <= j
j + k <= i
i + k < j
j + k < i
k <= i
i <= k
k <= j
j <= k
```

其中 `k` 是枚举出来的小范围整数常数。

此外，代码会把 `goal` 本身也加入候选集合，用来识别“只是重述目标”的候选。

## SMT 检查逻辑

对每个候选 `H`，主函数会做几个检查。

### consistent

```text
A /\ H  SAT ?
```

如果不可满足，说明 `H` 与当前 assumptions 冲突，直接丢弃。

### already_known

```text
A /\ not(H)  UNSAT ?
```

如果不可满足，说明：

```text
A => H
```

也就是说 `H` 已经被 assumptions 推出了，不是真正缺失的新事实。

### sufficient

```text
A /\ H /\ not(G)  UNSAT ?
```

如果不可满足，说明：

```text
A /\ H => G
```

这个 `H` 足以让当前 failed goal 成立。

### restates_goal

如果：

```text
H == G
```

则标记为 `restates_goal=True`。

这种候选虽然一定 sufficient，但通常价值很低，因为它只是把要证明的目标原样作为假设补回去了。

## Multi-literal Abduction

当前版本支持 bounded-size 合取搜索。

默认：

```text
--max-size 2
```

也就是先搜索单 literal：

```text
H
```

再搜索双 literal 合取：

```text
H1 /\ H2
```

搜索过程分两阶段。

第一阶段检查所有单 literal。对每个 `H`：

```text
1. 如果 A /\ H 不可满足，丢弃
2. 如果 A => H，标记 already_known
3. 如果 A /\ H => G，输出 size=1 候选
4. 如果 H 单独不够，但 consistent 且不是 already_known，放入 combo_pool
```

第二阶段从 `combo_pool` 中组合：

```text
H1 /\ H2
```

然后检查：

```text
A /\ H1 /\ H2  SAT
A /\ H1 /\ H2 /\ not(G)  UNSAT
```

如果成立，就输出一个 `size=2` 的候选。

为了避免输出大量无意义超集，代码做了最小性过滤：

```text
如果 H1 已经足够推出 G，
则 H1 /\ H2 不再输出。
```

例如：

```text
i + 1 <= j
```

已经 sufficient，那么：

```text
i + 1 <= j /\ j <= 10
```

虽然也 sufficient，但不是更好的解释，会被跳过。

## 为什么需要 max_combo_candidates

多 literal 搜索会组合爆炸。

如果有 100 个候选 literal，那么二元组合数量是：

```text
100 * 99 / 2 = 4950
```

而当前实现每次 SMT 检查都会调用 Z3 CLI 进程，所以组合数过大时会很慢。

因此第二阶段只保留前 N 个非平凡候选：

```text
--max-combo-candidates 40
```

这些候选已经经过初步过滤：

```text
consistent
not already_known
not single-literal sufficient
```

再按启发式分数排序后截断。

## 命令行用法

示例：

```bash
 python3 -m abduction.symbolic_abduction_v1.debug_wp \
    abduction/symbolic_abduction_v1/wptest.txt \
    --max-size 1 \
    --max-results 5
```

参数说明：

```text
wp_txt
  保存好的 Frama-C/WP 输出文件。

--visible
  逗号分隔的源程序变量名。
  例如 --visible i,j。
  如果不传，则从解析出来的 assumptions 和 goal 自动收集变量。

--max-results
  最多输出多少个候选。

--max-size
  H 最多包含几个 literal。
  1 表示只搜索 H。
  2 表示搜索 H 和 H1 /\ H2。

--max-combo-candidates
  multi-literal 搜索阶段保留多少个单 literal 进入组合池。

--z3
  Z3 CLI 路径，默认 /opt/z3-4.7.1/bin/z3。
```

## 输出格式

输出是 JSON list，每个元素是一个 `AbductiveFact`。

例子：

```json
[
  {
    "predicate": "i + 1 <= j",
    "sufficient": true,
    "consistent": true,
    "already_known": false,
    "restates_goal": false,
    "size": 1,
    "score": 13.55,
    "reason": "assumptions and this abducible make the negated goal unsatisfiable"
  }
]
```

字段含义：

```text
predicate
  候选事实 H 的 ACSL 风格文本。

sufficient
  是否满足 A /\ H => G。

consistent
  是否满足 A /\ H 可满足。

already_known
  是否已经有 A => H。

restates_goal
  是否只是把目标 G 原样作为候选。

size
  H 中包含几个 literal。
  单 literal 是 1，H1 /\ H2 是 2。

score
  启发式排序分数。

reason
  简短解释为什么输出该候选。
```

## svcomp/235 示例

对 `results/baseline1_llm_direct/failed_cases/svcomp/235/wp.txt`，其中一个失败目标大致是：

```text
Assume {
  Have: 0 < i.
  Have: j <= 10.
  Have: i <= (2 + j).
  Have: i <= j.
  Have: j <= 11.
}
Prove:
  i < j.
```

运行本工具后，会得到类似：

```text
i + 1 <= j
i + 1 < j
i + 2 <= j
...
```

其中：

```text
i + 1 <= j
```

可以推出：

```text
i < j
```

所以它是当前 failed VC 的一个 sufficient abducible。

但需要注意：这只说明它能修当前证明目标，不说明它一定是合法 loop invariant。

## 当前能力边界

这个原型目前能做：

```text
1. 从 wp.txt 中提取第一个 failed/timeout/unknown goal
2. 解析简单线性整数 Have 和 Prove
3. 生成有限 abducible literal 空间
4. 检查单 literal H 是否 sufficient
5. 检查 H1 /\ H2 是否 sufficient
6. 过滤 inconsistent 候选
7. 标记 already_known 候选
8. 标记 restates_goal 候选
9. 用启发式分数排序输出
```

还不能做：

```text
1. 判断 H 是否 inductive
2. 检查 loop preservation
3. 自动插入 ACSL invariant
4. 处理数组、指针、量词和复杂 ACSL predicate
5. 调用 GPiD 外部工具
6. 对整个 C 程序做完整 repair
```

最重要的限制是：

```text
A /\ H => G
```

只表示 `H` 足以推出当前失败目标。

它不表示：

```text
H 是可建立的
H 被循环体保持
H 是最终正确的 invariant
```

因此当前输出更准确的定位是：

```text
候选缺失事实
```

而不是：

```text
已验证 loop invariant
```

## 后续方向

下一步最值得做的是 loop preservation / inductiveness 检查。

也就是对候选 `H` 继续验证：

```text
1. 初始化时 H 是否成立
2. 假设循环前 H 成立，执行循环体后 H 是否仍成立
3. 循环退出条件加 H 是否能推出最终 assert
```

这样才能把当前的“abduced fact”进一步升级成更接近可用的 invariant repair。

另一个重要方向是减少 Z3 CLI 调用开销。当前每次 `_check` 都会启动一个 Z3 进程，简单但慢。后续可以考虑：

```text
1. 使用 Python z3-solver
2. 批量生成 SMT 查询
3. 缓存重复 check 结果
4. 对候选空间做更强剪枝
```
