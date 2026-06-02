在svcomp测试集上autospec通过9/21，在autospec后接一个纯神经的方法的卡点分析通过18/21。下面这个表是对autospec上不通过的12个案例的具体结果。

| Dataset | File  | Status | autospec   |
| ------- | ----- | ------ | ---------- |
| svcomp  | 247.c | PASS   | Invalid    |
| svcomp  | 248.c | FAIL   | Fail_13_14 |
| svcomp  | 241.c | PASS   | Invalid    |
| svcomp  | 246.c | PASS   | Invalid    |
| svcomp  | 244.c | FAIL   | Fail_16_17 |
| svcomp  | 240.c | FAIL   | Fail_8_9   |
| svcomp  | 232.c | PASS   | Invalid    |
| svcomp  | 238.c | PASS   | Invalid    |
| svcomp  | 234.c | PASS   | Invalid    |
| svcomp  | 250.c | PASS   | Invalid    |
| svcomp  | 251.c | PASS   | Invalid    |
| svcomp  | 239.c | PASS   | Fail_10_11 |

但我感觉这样比较是不对的，因为autospec的输出有很多是invalid导致的不通过，而不是proof obligation的fail。而且这样看很不直观。所以我现在的设计是抛弃掉autospec，直接和llm only以及llm+feedback比较。



# spec_generation_abduction

当前已实现：

- `baseline1（LLM直接生成）`: 直接让 LLM 为原始 AutoBench 程序生成 ACSL/spec，每题最多独立调用 LLM 5 次，不把 verifier feedback 放回 prompt，每次生成后运行 Frama-C/WP，只要任意一次 WP Pass，该题算通过。

- `baseline2（LLM+verifier feedback）`: 每题最多 5 轮，把上一轮及历史 Frama-C/WP feedback 放回 prompt 让 LLM 迭代修复；任意一轮 WP Pass 即停止并计为通过。

- `baseline3（纯神经的卡点分析，assertion probe + spec rewrite）`: 先按 baseline1 生成初始 C+ACSL，WP Fail时不是像baseline2一样直接重生成，而是解析 failed PO(proof obligation)。

  提取失败PO的目标和上下文（提取proof obligation是什么，已知事实，已知变量）

  ​     ↓

  LLM判断一下是直接rewrite spec还是生成assertion探针（如果它认为spec大体正确，只是缺少中间证明事实，就进入assertion probing。如果它认为spec本身可能需要调整，就进入 rewrite分支。）

  ​     ↓

  用abduction思想生成源码级assertion candidates（目前只是prompt中使用abduction的思想，已知条件+缺失事实H =>目标成立，没有直接使用符号工具）

  ​     ↓

  逐个插入临时文件，用WP测试（分为几类，successful_probe，proved_but_only_improves，proved_but_not_helpful，useful_but_unproved，unproved_and_not_helpful。其中比较重要的是useful_but_unproved，表示这个assertion自己暂时不能证明，但如果把它作为事实加入，原目标可以被解决。后续它被rewrite成invariant之类的以后再去证明他就可以了。）

  ​     ↓

  收集有帮助的probe evidence

  ​     ↓

  进行rewrite：LLM根据evidence生成spec rewrite proposals（可能会modify_loop_invariant，modify_requires，modify_ensures，add_lemma，add_ghost）

  ​     ↓

  逐个应用到临时文件，用WP验证

  ​     ↓

  若full WP pass，则成功



当前未实现：

- `符号方法abduction的卡点分析+ spec rewrite`: 在baseline3的基础上，生成源码级assertion candidates的时候通过abduction得到关键缺失条件（已知条件+缺失事实H =>目标成立）。



Baseline3 = direct generation + failure diagnosis + abduction-guided repair



    1. invalid：ACSL/C语法、类型、未定义标识符、unsupported construct
    2. wrong spec：这句规格本身不成立
    3. 缺少spec：缺少loop invariant、assigns、callee contract、bridge fact
    4. 缺少proof gap：WP需要中间断言、分解事实、局部lemma 才能证明



initial direct generation (like baseline1) -> run WP

if Pass:
    save success

if Invalid: （Invalid 应该优先处理）
    diagnose_invalid()
    rewrite or delete (parse stderr、stdout，locate error line，根据行号找到对应的那一句，重写或者删除)
    rerun WP
    if still Invalid:
        regenerate(到达一定次数还是重写不出来就delete？)
    continue

if Fail:
    extract failed proof obligations
    for each failed PO:
        diagnose_failed_po()
        if wrong spec:
            rewrite / delete
        elif 缺少spec:
            add missing invariant / assigns / contract
        elif 缺少proof_gap:
            promote useful assertion
        else ambiguous:
            try conservative assertion probe first, then rewrite

 

1. assertion / postcondition failed

先尝试 assertion probe，如果某个 assertion 能被证明并让 target solved，说明原目标大概率没错，是 proof gap。

如果 assertion 本身证明不了但能让 target solved，说明它可能是缺失的强规格，需要变成 invariant/ensures/requires，而不是临时 assert。

如果怎么 probe 都不改善，再考虑已有 generated spec 是否误导 WP 或太弱。

    2. loop invariant establishment failed

先怀疑 invariant 本身写错。

    3. loop invariant preservation failed

要么invariant 本身不归纳，写错或太强；要么invariant 基本对，但缺少辅助 invariant

4. assigns failed

通常是spec 写错。extract modified variables，rewrite assigns clause

    5. callee precondition / requires failed

callee requires 太强，caller 缺少能证明 requires 的事实。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            



  现在没有真正调用 SMT/符号工具去计算 H。  目前是：

  WP failed goal
      -> LLM 根据 assumptions/prove_statement 猜 H
      -> 插入 H 跑 WP 验证其帮助程度
      -> 根据 probe evidence 生成 repair

LLM-guided abduction + WP validation



## 目录

```text
spec_generation_abduction/
  configs/models_config.yaml
  data/AutoBench/
  scripts/run_baseline1.py
  scripts/run_baseline2.py
  scripts/run_baseline3.py
  results/
```

`data/AutoBench` 是从原 AutoSpec 仓库复制出来的数据集副本。

## 环境

需要：

```bash
pip install openai pyyaml
```

还需要 `frama-c` 在 `PATH` 中，或运行时用 `--frama-c` 指定路径。

模型 API key 支持两种配置方式。推荐使用 `configs/models_config.yaml` 中配置的环境变量；
例如当前 `gpt-4o` 映射使用 `OPENAI_API_KEY`：

```bash
export OPENAI_API_KEY=...
```

也可以直接写在 `configs/models_config.yaml` 的模板或模型映射里：

```yaml
ConfigTemplates:
  Yunwu_Config:
    platform: "yunwu"
    api_key: "sk-..."
    base_url: "https://api.apiplus.org/v1"
    timeout: 300
```

直接写入配置文件时，不要把包含真实 key 的文件提交到版本库。





## Run Baseline1

四个主数据集：

`--resume` 会跳过已有最终输出，console 日志追加，summary 重新生成。
如果验证逻辑或 prompt 有改动，应不加 `--resume` 或加 `--overwrite` 重新跑。

```bash
python3 scripts/run_baseline1.py \
  --datasets SyGuS,frama-c-problem,svcomp,46_fib \
  --model gpt-4o \
  --attempts 5 \
  --wp-timeout 8 \
  --resume
```

全部 AutoBench 子数据集：

```bash
python3 scripts/run_baseline1.py \
  --datasets all \
  --model gpt-4o \
  --attempts 5 \
  --wp-timeout 8 \
  --resume
```

baseline1 的 WP 检查按 partial correctness 口径运行，会排除 `@terminates`、
`@variant` 和 `@decreases` 目标；未提供或未证明 `loop variant` 不计入通过/失败。

默认输出：

```text
results/baseline1_llm_direct/
```

重要文件：

- `baseline1_summary.md`: 总体、分数据集、逐题统计。
- `baseline1_console.txt`: 命令行进度输出留痕，包括每题编号和 LLM start/done/error。
- `successful_files/<dataset>/<file>.c`: 通过 WP 的文件。
- `failed_cases/<dataset>/<case>/`: 未通过题目的输出目录，包含最佳失败 attempt 的 C 文件和 `wp.txt`。

baseline1 不保存每次 attempt 的中间文件；每个题目最多只保留一个最终 C 文件。

## Run Baseline2

baseline2 使用相同的 WP partial correctness 口径，但每一轮会把 verifier feedback
反馈给下一轮 LLM 生成：

```bash
python3 scripts/run_baseline2.py \
  --datasets SyGuS,frama-c-problem,svcomp,46_fib \
  --model gpt-4o \
  --attempts 5 \
  --wp-timeout 8 \
  --resume
```

默认输出：

```text
results/baseline2_feedback/
```

重要文件：

- `baseline2_summary.md`: 总体、分数据集、逐题统计。
- `baseline2_console.txt`: 命令行进度输出留痕，包括每题编号和 LLM start/done/error。
- `successful_files/<dataset>/<file>.c`: 通过 WP 的文件。
- `failed_cases/<dataset>/<case>/`: 未通过题目的输出目录，包含最佳失败 round 的 C 文件和 `wp.txt`。

## Run Baseline3

baseline3 使用和 baseline1/2 相同的 WP partial correctness 口径。某次初始文件 WP 失败时，会基于 WP 失败目标先让 LLM 判断
`generate_assertions`、`rewrite_spec` 。assertion probing 会一次只插入一个 `//@ assert ...;` candidate，再重新运行 WP；若 assertion没解决，会把有用的 probe evidence 交给 rewrite 分支，让 LLM 生成独立的 ACSL spec rewrite proposal。
probe 或 rewrite 后的整个文件 WP Pass 才算通过。

```bash
python3 scripts/run_baseline3.py \
  --datasets SyGuS,frama-c-problem,svcomp,46_fib \
  --model gpt-4o \
  --attempts 3 \
  --max-repair-rounds 7 \
  --max-invalid-repairs 4 \
  --max-llm-candidates 5 \
  --wp-timeout 8 \
  --resume
```

当前 baseline3 默认每题最多 3 次独立初始生成；每次初始生成后最多 7 轮 repair；
Invalid 输入最多尝试 4 次 invalid-specific repair。

默认输出：

```text
results/baseline3_assertion_probe/
```

重要文件：

- `baseline3_summary.md`: 总体、分数据集、逐题统计。
- `baseline3_console_<dataset>.txt`: 命令行进度输出留痕，包括每题编号和 LLM start/done/error；多数据集同跑时 dataset 名用 `__` 连接。
- `successful_files/<dataset>/<file>.c`: 通过 WP 的最终文件，可能是初始生成文件、插入 successful assertion probe 后的文件，或 successful spec rewrite 后的文件。
- `failed_cases/<dataset>/<case>/`: 未通过题目的输出目录，包含最佳失败 attempt 的 C 文件和 `wp.txt`。

如需保存每个 case 的中间步骤，可以加 `--trace-steps`。默认关闭；打开后会额外写入：

```text
results/baseline3_assertion_probe/traces/<dataset>/<case>/
```

trace 目录包含 initial 文件、每轮 current/next C 文件、WP stdout/stderr/result、diagnosis、assertion probe candidates、repair proposals 和 repair application 结果。



### Experiment



## 一些问题notes

  - assertion probe 成功时，最终保存的是“插入了 probe assertion 的代码”，不是把assertion 提升成 loop invariant / ensures / requires 后再保存。
  - rewrite branch 只有在当前 PO 内使用前面积累的 probe_evidence，没有跨 PO 或跨attempt 累积经验。
  - 每个 assertion/rewrite 都是独立临时测试；没有把多个有帮助但单独不够的 probe组合起来。
  - decision_type == rewrite_spec 时先 rewrite，再 assertion；否则先 assertion，再 rewrite。
  - 成功标准很严格：只有某次 probe/rewrite 让整份文件 WP Pass，才算成功。局部improvement 不会保存为最终结果，只会作为 rewrite evidence。
  - baseline3 目前不会产出详细 probe 日志，只在最终 summary 记录 case 级结果；很多中间判断和候选不会持久化，后续分析会比较困难。
