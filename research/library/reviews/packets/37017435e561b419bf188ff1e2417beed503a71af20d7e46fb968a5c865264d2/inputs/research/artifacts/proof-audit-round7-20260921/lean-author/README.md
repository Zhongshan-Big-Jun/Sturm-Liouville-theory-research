# Round 7 local Lean author candidate

本包只提供局部作者候选及作者侧机器执行证据. 后续独立执行和语义复核待新 agent 完成. 本目录所有说明均非独立审查 verdict.

## 文件与重放

- `snapshot/SL/AuditRound7.lean`: 唯一新数学模块, 完整定义和结论可直接 readback.
- `replay.py`, `run_lean.py`: 独立重放入口和保留原始命令/日志的执行辅助程序.
- `positive-contract.json`: 根声明的完整显式类型; `wrong-target-contract.json`: 故意把 n=2 中点值写成 -6*pi, 保留曾启动的维护版负向扫描契约.
- `controls/WrongWronskianTarget.lean`, `controls/WrongMirrorFactor.lean`: 最终协议的两个直接编译负对照, 分别错误使用 -6*pi 和遗漏镜像因子 2.
- `runtime-config.json`, `freeze.json`: 实际环境位置和输入身份. `snapshot/` 内三份配置是只读原配置的小型副本, 不写原配置.
- `evidence.json`: 最终交付入口. 各运行目录保存原始日志、退出码、输入快照、olean、逐声明类型/公理和维护版 verifier 清单.
- `development/`: 增量编译的失败与成功历史; 这些失败日志不充当最终结果.
- `source-stability.json`: 数学源码与正/负契约自首次成功精确根检查起保持相同 SHA 的记录.
- `final-inputs.zip`: 按最终 freeze 生成的 12 文件小型输入包 (11 个冻结输入及 freeze.json), 不含作者输出、审查结论或旧运行证据. 可供新的执行者复制后使用默认 replay 命令, 输出路径相应改到复制后的包目录内.

在 WSL 使用已安装的 Windows Lean 4.31.0 与现有 mathlib 缓存运行:

```bash
python3 -B /mnt/f/tools/math-audit-round7-20260921/lean-author/replay.py /mnt/f/tools/math-audit-round7-20260921/lean-author/replay-independent-01
```

输出目录必须是本交付目录内尚不存在的新子目录. 程序拒绝覆盖已有运行, 校验冻结输入, 直接调用现有编译器及未修改的 lean-verify 2.0.0, 不下载依赖或执行 `lake build`. 默认流程是一次完整精确正向根检查、直接正对照、全部声明导出、根 import 解析和两次预期失败的 Lean 编译. `-B` 防止向依赖区写 Python 缓存. 新执行者应保留自己的真实命令和回执; 本作者 runner 本身不会自动授予独立性或语义通过结论.

`--resume-positive` 只用于本作者导出器修复后的续接: 校验原正向清单 SHA 及源码/配置/契约/运行时/工具/已编译对象, 使用原库调试导出器, 不重复根证明或全 import 哈希扫描. 它不刷新原环境清单的时间范围. 新 agent 独立执行应使用上面的默认命令, 不带该参数. 全环境首次哈希可能耗时数分钟, 可由执行者在自己可持续运行的终端启动, 保留进程与日志.

mathlib 外部 olean 只读复用, 不复制全库. 维护版 verifier 记录实际加载模块、解析路径及 artifact 哈希, 并绑定根对象. 这仍信任本机 Lean 和外部编译依赖, 不构成另一个内核对 mathlib 源码的全量重编译.

## 数学 readback

`n : Nat`, 实变量与系数均为 `Real`. 本文件未导入任何旧项目模块, 所有局部名称位于 `SL.AuditRound7`.

1. `normalized_mode n x = sqrt(2)*sin(n*pi*x)`, `normalized_mode_slope n x = sqrt(2)*(n*pi)*cos(n*pi*x)`. `normalized_mode_has_deriv` 真正证明 `HasDerivAt`; `wronskian_is_derivative_expression` 连接显式斜率与 `deriv`. 名称中的 normalized 对应这个明确公式; 本包未证明积分归一化或它作为谱问题本征函数的身份.
2. Wronskian 方向固定为 `u_n*u'_(n+1) - u'_n*u_(n+1)`. `wronskian_product_to_sum` 给出 `pi*(sin((2n+1)*pi*x)-(2n+1)*sin(pi*x))`. 中间的 `trig_product_to_sum` 对任意实数频率参数成立.
3. `sin_square_sum n t` 是 `sum (j=0,...,n-1) sin((j+1)*t)^2`. `finite_sin_square` 对全部自然数 n 和全部实数 t 证明 `sin((2n+1)*t)-(2n+1)*sin(t) = -4*sin(t)*sin_square_sum n t`. 证明以奇数角相邻差分归纳, 不是数值扫描. n=0 是空和, 等式为 0=0; 严格负性另要求 n>0 及 0<x<1.
4. `wronskian_finite_sum` 将两式连接. `wronskian_neg` 用和中 j=0 即 sin(t)^2 的正项证明内部严格负性. `wronskian_two_half` 得到 -4*pi; `old_wronskian_two_half` 计算旧式为 -6*pi; `old_wronskian_counterexample` 证明二者不等.
5. `endpoint_coefficient n = 2*pi^4*(n^4-(n+1)^4)`. `endpoint_coefficient_algebra` 从 `(n*pi)^2*(sqrt(2)*n*pi)^2` 与下一指标项之差得到它. `endpoint_coefficient_expanded` 展开为 `-2*pi^4*(4*n^3+6*n^2+4*n+1)`, `endpoint_coefficient_neg` 证明对全部自然数 n 严格为负. 这是系数代数, 未断言此系数属于任何已证明的 Taylor 展开.
6. `fh_term(lambda,jump,value,velocity) = -lambda*jump*value^2*velocity`. `mirrored_pair_from_single_interface` 的前提明确给出左贡献等于速度 +1/跳量 jump 的单界面式, 右贡献等于速度 -1/跳量 -jump 的单界面式, 以及镜像值平方相等. 结论是两贡献和等于 `-2*lambda*jump*leftValue^2`. 这些前提并非待证明的结论换名, 而是两个分别给定的单界面贡献; 在任意实参数下可取相同左右值和定义给出的贡献使前提满足.
7. `gap_switch(lower,upper,a,b) = lower*a^2-upper*b^2`. `mirrored_gap_from_single_interface` 分别对上下两模态假设四个单界面式和两个平方镜像关系, 得到 `upperPair-lowerPair = 2*jump*gap_switch`. `mirrored_stationarity_iff` 还要求 jump 非零, 此时驻点等价于 switch=0. 未把谱导数存在、FH 定理或对称本征函数的结论藏入无条件声明.
8. `old_mirror_factor_counterexample` 是可检查的实数代数实例 (jump=-3, lower=1, upper=4, 两左值均为 1), 得到 18 不等于 9. 它不是审计报告中真实三段权谱数据的形式化.

`local_algebra_root` 是源码中十项明确结论的合取, 包含完整全称量词与 FH 前提, 没有空 `True` 目标. 精确契约只检查它与保存的 Lean 类型是否一致; 契约的数学适切性仍需独立语义复核. 全部公开声明另行 `#check`/`#print axioms`, 定义另行 `#print`.

## 明确未形式化

全部无限维 Volterra 估计、端点一致邻域、Taylor 余项、一般指标谱极限、min-max/薄质量构造、本征值可微性、单界面 FH 定理、谱归一化、全 R 分支及旧轮证明均不在本包形式化范围. 未加入可选 thin-mass 目标.

## 输入与执行边界

数学问题来源是用户提供的 `/mnt/c/Users/HuangZY/Downloads/proof_audit_round7_20260921.md`. 已读取项目 `AGENTS.md` 和用户指定的 lean-verify SKILL 及 `references/v2-verification.md`. 前轮仅只读 `replay.py` 与 `run_lean.py` 识别运行环境, 没有重验证前轮证明. 未读取解析作者新稿.

只写本 `lean-author` 目录, 未改主库旧源/config、插件或前轮证据, 未 commit. 局部维护过程记在本目录 `AGENTS.md`.

## 作者机器执行结果

数学 source SHA-256 为 `c1b464f60cc7cef7a1052a0cf97cde4cacd01b36f69a83ac94056128a7fb8af6`. 从首次成功整文件编译、`author-run-01` 根检查到最终交付, 数学 source 与正/负契约均未更改. 后续调整均为导出器和执行流程.

| 检查 | 实际记录 | 结果 |
| --- | --- | --- |
| Lean 4.31.0 新源码整文件编译 | `development/logs/04-special-value-conversion.json` | exit 0 |
| lean-verify 精确根及闭包 | `author-run-01/positive/run-manifest.json` | exit 0, exact_root_passed=true, semantic=not_reviewed |
| 直接正对照 | `author-run-04/logs/03-positive-control.json` | exit 0 |
| 27 项公开声明 #check/#print axioms 和 JSON 导出 | `author-run-04/logs/04-all-declarations.json`, `author-run-04/public-declarations.json` | exit 0, 20 定理/7 定义 |
| 根 import 解析 | `author-run-04/logs/05-import-resolution.json`, `author-run-04/root-artifact.json` | exit 0, 命中原已核验的同 SHA 根库 |
| 旧 Wronskian target | `author-run-04/logs/06-wrong-target.json` | 预期失败, exit 1, -4*pi 与 -6*pi 类型不匹配 |
| 旧镜像因子 | `author-run-04/logs/07-old-mirror-factor.json` | 预期失败, exit 1, 因子 2 与 1 类型不匹配 |

根及全部公开声明的传递公理并集只有 `propext`, `Classical.choice`, `Quot.sound`. 原正向清单绑定 4,365 个实际加载模块及 13,089 个外部编译 artifact 身份. 该 import 哈希清单属于原精确正向运行; 作者续接没有声称重新刷新它. 原根对象哈希、当前源码身份和续接时的实际 import 解析均保留.

`author-run-01` 的 JSON 导出器因误用关键字 Type 失败, `author-run-02` 因漏开 Lean.Meta 命名空间失败. `author-run-03` 的公开导出已成功, 但额外维护版负向扫描的外层执行 exit 143, 终止来源未知, 没有产出最终清单; 该扫描仅记为 INCOMPLETE. 其已完成的 Lean 类型提取显示 mismatched, 但本包不把它补写为完整维护版负向回执. 最终两个负对照以上表直接编译记录为准. 全部旧回执、源码快照和分阶段 freeze 均保留.

最终输入身份以 `freeze.json` 为准, 汇总与原始证据文件哈希见 `evidence.json`. 最终 runner 的公共导出及两负对照已经实际运行; 默认完整模式复用已执行成功的根检查路径, 导出器修复后未再重复全根扫描. 独立执行和语义复核仍待新 agent 针对最终 freeze 完成. 用户此前复制的旧包不属于本作者的独立批准证据, 本作者未读取其执行输出.
