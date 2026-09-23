# R9-F01 software-author handoff

本交付是软件作者的修订候选与实际运行证据. 不提供最终独立审计通过判定. 本作者只写 `/mnt/f/tools/math-audit-round9-20260923/software-author`, 未修改仓库/插件, 未 commit/push, 未改变全局 Python 环境.

## Candidate and source identity

- 可直接替换 `scripts/_gapn2_second_variation_probe.py` 的候选: `/mnt/f/tools/math-audit-round9-20260923/software-author/_gapn2_second_variation_probe.py`.
- 候选 SHA-256: `53c5ccd85c28f1a5a1e2e37a4eed4e8dc450025eaf313aae15df028eb1f9d31e`.
- `replacement.patch` 提供同一候选相对当前原脚本的补丁.
- 当前原脚本 Git blob `bbba622840a3992d45a2ff11cef24e489656a06e` 与审计包 `source_manifest.json` 的 R9-F01 源码身份相同.
- 实际读取的代码依赖: `_gapn2_symmetry_recon.py` 的 Recon/roots_of/eigfun, `_gapn2_jacobian_probe.py` 的 symmetric_root/jac_fd, `_gapn2_jacobian_analytic.py` 的 eigen_data/uv_at. 它们的相关实现和 `op03_gap_table.json` 已读取. 未调用该模块的 regularized_green 或其它 Blueprint 维护代码.
- `input_manifest.json` 记录初始输入及运行环境, `source_preservation.json` 记录结束时身份. 目标脚本、三个导入依赖、输入表和本次记录的审计材料均保持原哈希. 根 AGENTS.md 在运行间发生了本作者写入范围外的变更, 已记录前后身份, 不声称整个并行工作仓库未变.

## Changes and numerical methods

1. 对每个真实块计算 `A[i] = integral f`, 默认欧氏投影 `b -= (b.A)/(A.A) * A`. 可选 `--metric width-weighted` 使用 `diag(widths)`, 等价于沿 `A/widths` 修正并以 `A.(A/widths)` 为分母. 零法向量返回独立拷贝, 有限性、维度、正宽度与度量参数均检查. 用缩放和扩展精度减少大/小法向量的中间溢出或下溢.
2. 两个目标本征频率以 mpmath 从原传递矩阵根估计精化. 在输入浮点块长定义的真实端点上, 通过分块三角原函数计算归一化质量及 A, 默认 60 位工作精度. 浮点块长代表的总长可能与 1 相差最后若干位, 不把十进制表当作精确驻点证书.
3. `direct_residual` 使用单独的 tanh-sinh 求积, 在每个真实块内直接积分 `f*h`. 它不把已投影的 `b.A` 当作验证. 输出保留投影内积和此独立机制的残差.
4. 谱配对使用逐段 Gauss-Legendre 积分, 在所有密度端点和 P3 脉冲端点处分段. 消除了旧均匀网格截取后漏掉区间两端的机制. 默认每段 64 节点, 保留 61 本征函数, 与旧 `N_MODES=60` 的包含上界循环相同.
5. P1 使用真正的线性密度路径. 高精度中心差分默认步长 1e-2/1e-3/1e-4, 同时记录最后步长的双精度结果. 非正密度端点直接拒绝, 不再用 `max(...,1e-8)` 改写路径. 输出绝对/相对误差, 无宽松 FD PASS 阈值.
6. 历史 P1 PASS、P2 definite、P3 NEGATIVE 均降为历史标签. P1 的公式比较不要求切向; 原切向标签错误不等于全部旧 P1 二阶比较无效. P2 只报告八个固定种子样本. P2b 原本已经对积分向量投影, 本轮仅共享输入健壮处理和更准确的分段积分, 未将它归入平均值投影错误.
7. P3 保持半宽 5e-4 的有限脉冲探索. 同时报告线性密度 `Q`, 接口路径 Hessian, 以及半加速度贡献 `-0.5*sum(s_i*d_i**2*fprime(a_i))`. 因为移动接口路径还有 `rho''=sum(s_i*d_i**2*delta'_i)`, 这两类 Hessian 不可直接等同. 固定宽度差值、符号不同和有限分辨率不作为发散或证明否证.
8. 保留 `[n] [R] [mode]` 位置参数、默认值、样本数量和随机种子 20260813. 保留 R=1 常密度退化情形; 初稿过严的 R>1 守卫已通过实际旧 CLI 对照发现并修正. 增加可选数值参数和 `--output`. 新代码使用 tab 缩进.

## Actual checks

`/usr/bin/python3`, NumPy 2.5.2, SciPy 1.18.1, mpmath 1.3.0. 所有执行均使用 `-B`, 运行 cwd 明确为 `/mnt/f/LaTeX/BVE research`. `execution_manifest.json` 记录最终候选的 14 条命令、实际退出码、用时和日志哈希; 三个非法 CLI 用例的预期退出码为 2. 其它记录包括四个请求案例、R=1、原脚本基线、正常/-O 测试与敏感性.

- `old_projection_red.log`: 从原 P1/P2 AST 中执行真实旧投影语句, 常密度不等宽例的旧打印内积为 0, 真正一阶变分为 -8.665090650287976, 测试退出 1. 同一回归在最终候选中残差 4.44e-16, 退出 0. 补充推导给出的具体旧方向也经直接求积核对.
- `tests.json` / `tests_optimized.json`: 正常及 -O 均完成 6 组作者回归检查. 每种模式实际拒绝 41 类非法参数. 覆盖欧氏/加权/零法向量/尺度不变性/维度与有限性, 常密度严格公式, 实际 n2/R4 端点, 自适应配对积分, 小于旧网格间距的脉冲, 以及解析已知的有限步长 FD.
- 实际 n2/R4 块积分另由 64 节点 Gauss 与 70 位解析积分交叉检查, 四个配对另由 SciPy 自适应积分比较. 更窄脉冲的质量在端点分段规则下恢复, 旧 4001 点网格的负对照给出零质量. 具体数值在 `tests.json`.

四组最终重跑均为 61 模态、每段 64 Gauss 节点、目标积分/FD 60 位精度. 下表 P1 误差是三条样本在 h=1e-4 时的最大值; 绝对与相对最大值未必来自同一样本. P2 符号只是八个样本的符号.

| case | max direct abs integral(fh), P1/P2 | max P1 absolute FD error | max P1 relative FD error | P2 sample signs |
|---|---:|---:|---:|---|
| n2R4SUP | 7.500e-15 | 8.733e-09 | 1.536e-05 | 8 negative / 0 positive |
| n3R4SUP | 5.163e-15 | 5.258e-08 | 1.626e-05 | 8 negative / 0 positive |
| n2R10SUP | 4.920e-15 | 6.264e-09 | 2.784e-06 | 8 negative / 0 positive |
| n2R4INF | 2.746e-16 | 3.204e-09 | 5.009e-03 | 1 negative / 7 positive |

每个案例有同名 `.log` 与 `.json`; 参数、系数、真实块积分、驻点残差、P1 各步长误差和 P2/P2b/P3 原数值均可复查. P2b 24 条样本的最大直接残差约 3.60e-13. 它们也只是有限浮点证据.

## Sensitivity and remaining error

`sensitivity.json` / `.log` 对相同 n2/R4/SUP 方向分别改变积分阶数和谱截断. 固定 61 模态时, 阶数 32/64/128 得到接近相同的残余 FD 差异. 固定阶数 128 时, 三条 P1 样本相对 70 位、h=1e-6 中心差分的最大误差如下.

| retained modes | max absolute error | max relative error |
|---:|---:|---:|
| 31 | 6.212e-08 | 1.296e-04 |
| 61 | 8.733e-09 | 1.536e-05 |
| 121 | 1.135e-09 | 1.963e-06 |
| 241 | 1.489e-10 | 2.316e-07 |

八条 P2 样本在这些有限设置下均为负, 仍不推出整个切空间负定. 相邻设置的稳定性也不是无限谱尾误差界.

FD 步长 1e-1 到 1e-6 的实测揭示双精度相减失稳. 例如 SUP 第一方向 h=1e-6 时, 双精度 Q_FD=-0.026645352591003757, 70 位工作精度结果约 -0.00019976747518421535. 70/90 位运行结果经转换为 double 后相同, 此记录不声称 70 位逐位一致或给出严格 FD 误差包络.

针对 INF 第三条小值样本另作定点复查: 61 模态相对差异 0.005009319859354132, 241 模态降至 0.00004779746684374021; 后者绝对差异仍为 2.0260689605534175e-11. 该误差未抹掉, 未设置 1% 或其它松阈值产生 PASS.

## Limits and handoff

- 无谱尾严格界, 无区间根枚举或驻点认证; 未证明任意方向的符号、密度盒可行性、极值或无限宽度/截断极限. MP 高精度与求积一致性不等同严格证书.
- 根枚举仍使用读取过的现有 `roots_of`; 本候选检查返回数量、正性与排序并精化目标根, 没有把它改造成全参数认证求解器. 只有已列参数的实际行为得到本次作者检查.
- P3 本轮为固定宽度, 表中差值仍含有限脉冲、截断和接口 Hessian 有限差分误差. 未据此宣称发散或推翻任何极限身份.
- 完整数学与文档传播交协调器. 本作者未提供最终独立检验结论. `pre_R1_compatibility/` 留存先前候选及所有当时结果; `smoke_n2R4SUP.*` 是更早初次冒烟记录, 其候选身份与最终运行分开.

复跑命令 (cwd 必须是上述仓库路径):

```bash
python3 -B /mnt/f/tools/math-audit-round9-20260923/software-author/run_evidence.py
```

单例候选仍可按原位置参数运行. 接收者可用 `replacement.patch` 或候选文件替换目标脚本; 本作者没有执行替换.
