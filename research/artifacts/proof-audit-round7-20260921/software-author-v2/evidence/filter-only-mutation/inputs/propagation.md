# 第七轮直接代码用途调查

本报告由检查作者撰写, 不承担最终审稿. 主库没有被本任务修改或执行. 所有 path:line 均对应原提交 `636dac87c269795a520824101f1b2abd2c583c9b` 的原字节; `inputs/source-scan/` 保留本文使用的原文件. 与工作树一致的文件记录为当前代码证据, 不一致文件只使用原提交作修订前定位.

## 取证范围与版本

- 用 rg 定向扫描 scripts/、tools/、docs/ 的导数、梯度、Jacobian/Hessian、4pi^2 和 FH 上游引用. 主要模式、完整 argv、cwd、退出码、结果哈希见 `receipts/source-scan-manifest.json`; 原始命中为 `receipts/rg-*.txt`.
- 初次工作树扫描意外命中并行修改中的 `docs/SL_gap_extremals.tex`. 其候选命中未被用于结论, 原日志保留. 随后按原提交逐文件比较字节, 对 845 个相同的已跟踪源码/文本路径重扫. 排除当时已变化的 `docs/SL_gap_extremals.tex`, `tools/README.md`, `tools/feynman-hellmann.md`; 对这些路径仅取原提交快照. 不评价其它作者的修订候选.
- 这不是全库依赖审计. 未运行活动程序、旧 Blueprint 程序、历史冻结包、Lean 或历史全套证书; 没有改写任何旧结果. 未跟踪文件、动态 import、由外部驱动的调用以及未列明的 M3/KP 链不在肯定性结论内.
- 保存的程序是只读源码取证快照, 不是运行依赖. 独立 `checks.py` 只导入标准库、SymPy、mpmath.

## R7-F04: 参数约定与可执行用途

固定 `f=lambda_n*u_n^2-lambda_(n+1)*u_(n+1)^2`, 归一化 `int rho*u_k^2=1`, `s_i=rho_right-rho_left`.

| 位置 | 实际参数/调用 | 直接结论 |
|---|---|---|
| tools/gap-band-extremals.md:24-27 | 一个参数令 x_j+=eps、镜像-=eps. lambda 导数有 2, D 导数遗漏 2. | 原式需改为 `2(rho_L-rho_R)f`. 驻点零集不变. |
| scripts/op03_gap_fh.py:4,7-22 | `Df_at(u)` 创建宽度 `(u,1-2u,u)`, 比较 `Df_at(u+-eps)`, 但打印 `(1-R)f`. | 当前目录的诊断脚本确实含半值比较式, 应为 `2(1-R)f`. 不是仅文档错误. |
| scripts/op03_gap_fh10.py:12-20 | 宽度从 `(u,v0,u)` 改为 `(u+eps,v0-eps,u)`, 仅左接口右移. | `-lambda*(1-R)*u_k(u)^2` 不应再乘 2. |
| scripts/op03_gap_fh9.py:21-28 | 插入宽 eps 的低密度片, 右接口固定, 预测是特征值增量, 已乘 eps. | 单接口系数约定正确; 本轮未运行其数值实现. |
| scripts/gap_n1_grad.py:10-14,26-33,37-44 | a,b 为前两块宽, 接口 `(a,a+b)`; `num_grad` 对宽度作差分. | SUP 的 `((R-1)(f2-f1),(R-1)f2)` 是链式法则结果, 无统一加倍. 同一表达式直接用于 INF 时应整体换号, 当前诊断未分模式. |
| scripts/_tmp_fh_paradox.py:6-8,23-28 | `(u,1-2u,u)` 双接口移动; `fh=(R-1)(f_left-f_right)` 在对称点抵消. | 旧诊断的两个接口符号未随运动方向正确相乘. `fh2=-2(R-1)f_left` 对 SUP 合适, 对 INF 应换号. |
| scripts/tmp_fh_test.py:6-8,14,20-30 | 明确调用 INF `[R,1,R]` 双接口族; 用正的 `lambda*(R-1)*sum(u^2)` 预测. | 此特征值导数符号相反; INF 应为负, gap 应为 `+2(R-1)f`. 属当前保留诊断的符号问题, 不假定它进入求解器. |
| scripts/tmp_verify_endpoints.py:9-16,19,30 | 同一双接口族; `INF:-2(R-1)f, SUP:+2(R-1)f`. | 两模式符号均反. 这不是缺 2; 后续根求解仍直接用 f=0 (行 34-36). |
| scripts/op03_gap_limit3.py:15-27 | e 为左半接口, full=`(e,1-e[::-1])`; least_squares 接收 f 的前 n 项. | 实際求解的是零点残差, 没有把半值导数传为谱隙梯度, 缺 2 不改变此残差方程. |
| scripts/_gapn2_symmetry_recon.py:122-137,168 | `f_at` 用正确两特征值, `residual=f/lambda_(n+1)`; least_squares 接收 residual. | 是归一化零点方程; 不把工具卡的 D 导数当作 optimizer 的解析 jac 参数. |
| scripts/_gapn2_jacobian_probe.py:15-28 | 先以自由宽度 u 的差分形成 Ju, 末块为 1-sum(u), 接口 x=L*u, 返回 `Ju@inv(L)`. | 得到 2n 个独立接口的 Jx, 不是镜像约束后的 n 参数梯度. |
| scripts/_gapn2_hess_sign_and_bigR.py:20-42 | 自由宽度上直接对谱隙二阶差分, 再以 `inv(L).T@H@inv(L)` 转为接口 Hessian. | 差分本身不用错误镜像系数. 其后解析对照有下表的数组乘法问题. |
| scripts/tmp_hess.py:10-23 | a,b 为块宽, 直接对 `D=lambda_2-lambda_1` 差分. tmp_hess2.py:13-22、tmp_hess3.py:13-22 同类. | 未见由工具卡遗漏 2 直接传入这几个有限差分 Hessian 的路径; 不等于本轮验证了其数值精度. |

`op03_gap_fh.py` 使用 `op03_gap_precise.py`, 后者原逐块乘法见 `scripts/op03_gap_precise.py:13`; 工具卡当前推荐的是另一个 `op03_gap_fixed.py`. `op03_gap_fixed.py:13,41` 为 P*M, `45-69` 用分块闭式 L2rho 归一化. 这里仅确认依赖身份, 不把旧诊断的历史输出当成新复现.

对 `op03_gap_fh`, `_tmp_fh_paradox`, `gap_n1_grad`, `_gapn2_hess_verify` 做限定的 Python `import/from` 调用搜索没有命中 (rg 实际退出 1). 这仅排除扫描范围内的显式 import, 不排除作为主程序手工运行或外部动态调用.

镜像约束的正确矩阵接口是 `g_reduced=B.T*g_full`, `H_reduced=B.T*H_full*B`, 其中 B 的各列为 `e_j-e_mirror(j)`. 不应把所有 full-interface Jacobian/Hessian 无差别乘 2.

## R7-P01: 归一化混淆的直接上游

| 原位置 | 实际内容及传播 | 处置边界 |
|---|---|---|
| tools/feynman-hellmann.md:12-14,18 | 固定 L2 的 `H=-d²+tau*rho` 与 `int rho*y²=1` 混用. | 常 rho=2 的精确反例: 旧式 1, 真导数 2. 卡需改为广义特征对公式或区分 Hilbert 空间. |
| docs/SL_gap_extremals.tex:95-100 | 直接引用该卡, 文稿自身写的是权弦导数 `-lambda int delta-rho*u²`. | 引用上游不适配, 但此处权弦公式本身不因上游混淆变错. 应修引用依据/约定, 不能把它改成固定 L2 势导数. |
| tools/band-selfconsistency-equivariance.md:92; tools/green-half-inertia.md:103; tools/half-problem-regularized-green.md:252 | 显式链接 FH 卡为一阶/跳点来源. | 是已查到的引用传播, 不是运行时自动导入 Markdown 的代码证据. |
| scripts/_gapn2_symmetry_recon.py:61-91; scripts/op03_gap_fixed.py:45-69 | 权弦特征函数除以 `sqrt(int rho*y²)`; residual 使用 lambda 因子. | 与权弦模型匹配, 不需改成普通 L2 归一化. 未找到这条链直接使用 `H=-d²+tau*rho` 错式的运行代码. |

精确 checker 包含原特征方程代入、普通/加权范数、旧式与真导数, 以及广义公式在两个模型中的代入. 这是新写的反例检查.

## R7-P02: 后段矩阵推理与直接代码问题

| 原位置 | 可核实问题/约定 | 建议的最小修订 |
|---|---|---|
| docs/SL_gap_nge2_symmetry_local_proof.tex:574-582 (`prop:K`) | 将 detK>0 等同 Hessian 定号. | 删除无条件等价; 定性需主子式/惯性, 或明确连接分支+已知起始惯性+沿途非退化. |
| tools/band-selfconsistency-equivariance.md:109-111 | 重复 `detJ=(R-1)^(2n)(-1)^n detK`, 接着写 `detK>0 iff 每个临界点 Hess 正定`. | 直接重复错误, 且把 SUP 的 Hess 负定也写成正定. |
| 同卡:175-176,228 | “主元符号恒定 iff G1'” 和扇区正/负定 iff G1'. | 区分充分的惯性判据与 bare determinant 条件. 若诉诸沿分支延拓, 必须补齐条件. |
| tools/half-problem-regularized-green.md:149-155; tools/green-half-inertia.md:56-73 | 把 G1' 的归约表述成两个扇区定号/单扇区定号障碍. | 当前段落应明确所讨论的是更强的定性判据, 或列出使其等价的分支条件. 本轮没有重审 Green、M3/KP 证明. |
| tools/fh-hessian-branch-reduction.md:27-34 | n=1 二维判据同时假定 D_aa<0,D_bb<0,detH>0. | 没有 bare det=>定号错误; 不能因卡名含 Hessian 就统一撤回. |
| tools/band-selfconsistency-equivariance.md:116 | SUP n=2..4 写 `sgn detJ=(+1)^n`, 与同卡 110 及 evK 全正矛盾. | 更正冲突的历史描述/加勘误; 未重新运行那些历史扫描. |
| 同卡:122,152-154; 文稿:623-624 (`prop:pf` 末行) | `f'/s` 少 lambda_(n+1). | 恢复该因子; 已归一化的 `f'/(s lambda_(n+1))` 和 K 对角项不再乘一次. |
| scripts/_gapn2_jacobian_analytic.py:208-226 | `fprime_id=-2*lam_np1*eps*c*W`, 最终 J 除以 lam_np1. | 这一实际代码已保留 lambda, 没有沿用漏因子的 f'/s. |
| scripts/_gapn2_hp_scan.py:35,45 | 直接求 fprime, 再除 lam_np1. | 同样不能在修文档时向这段代码再乘 lambda. |
| scripts/_gapn2_hess_verify.py:37-45,57-62 | 用 lam_np1 同时乘 u_n²、u_(n+1)²; 比较 +s*f 和 +lam*diag(s)@J. | f 第一项应使用 lam_n, 当前独立右移坐标应比较 -s*f、-lam*diag(s)@J. 原测试在驻点运行, 不可用其旧日志认证新公式. |
| scripts/_gapn2_hess_sign_and_bigR.py:55-60 | J 为 ndarray, `sign*np.diag(s)*lam*J` 全为逐元素乘法. | 如需继续使用诊断, 应保留 full Hessian 非对角元, 用 `(sign*lam*np.diag(s))@J`. |
| scripts/_gapn2_jacobian_analytic.py:285-290 | `H=-np.diag(s)*lam_np1*Jfd`, `eigvalsh(H)`. | 同一逐元素错误, 行 285 注释还缺负号. 修乘法后重新产生新输出; 不修改旧输出. |
| scripts/_gapn2_o3_scan.py:65-75 | K 用 `@` 正确保留矩阵结构, evH 却用 `-np.diag(s)*lam_np1*J`. 该脚本 K 另含 lam_np1 缩放. | 修 evH 的矩阵乘法, 比较 K 数值时注明缩放差异; `sign_ok` 实际检查的是 `(-1)^n`. |
| scripts/_gapn2_second_variation_probe.py:212 | Hess 的同一逐元素表达式. | 仅登记这个直接 Hessian 计算点, 未展开其全部二阶变分试验. |

最后四行中的问题不是猜测数值误差: 两个 ndarray 间的 `*` 会把对角矩阵外的所有元素变成 0. 新 checker 用精确 2x2 对照确认这能把不定矩阵变成负定对角矩阵. 这是语义/代数检查, 不是对原程序的实际重跑. 其它命中中的 `scalar*np.diag(u)@M@np.diag(u)` 已正确使用矩阵乘法, 没有被误列为同一问题.

`lem:simplez` 的跨不同 lambda 方程 Cauchy 唯一性和 `thm:g2` 的差值下界问题按协调器指示记为待解析修订/未重新认证. 本 checker 没有用有限矩阵例否定零点简单性定理, 没有把 G2 标为通过.

## R7-F03: 4pi^2 的实际范围

| 原位置 | 范围证据 | 结论 |
|---|---|---|
| docs/SL_gap_nge2_symmetry_local_proof.tex:473-475 | 全文 n>=2, 开放条件注中宣称 SUP 分支 D->4pi². | 需要更正. 盒类上确界与某个待全局延拓的自洽分支应分开. |
| docs/SL_gap_nge2_symmetry_recon.tex:196-197 | 一般 n 的侦察总结同样写 4pi². | 直接文本传播, 需要限回 n=1 或替换为准确范围. |
| tools/band-selfconsistency-equivariance.md:63-65 | n>=2 工具卡同样无 n=1 限定. | 直接文本传播, 需要修订. |
| tools/gap-band-extremals.md:44-45 | 同行混列 n=1..12 数据、n=1 扫描与“极限”. | 明确 4pi²/24.943866 的原证据是 n=1, 一般 n 上确界另述. |
| scripts/op03_gap_limit3.py:34-38 | 真正打印 4*pi² 的 asymptotic loop 调用 `solve(R,1,True,[seed])`. | 代码明确 n=1, 没有把该常数用于 n>=2 求解. |
| docs/SL_gap_extremals.tex:272-290 | 三段、lambda_1 与 lambda_2 的中心钉扎解释. | 原局部分析实际是 n=1, 标题/摘要需显式限定, 不是把 n=1 值改掉. |
| docs/SL_spectral_topics_summary.tex:587-588,990 | 使用 lambda_1、lambda_2 的中心钉扎图像. | 同样保留 n=1 内容并明确范围; 不据 rg 命中就断言一般 n 程序错误. |

其余 4pi² 命中包含常密度第二特征值、纯代数证书和 n=1 专题, 未作为错误推广登记. 限定扫描没有发现将 4pi² 硬编码为 n>=2 谱隙极限的活动求解器调用; 这不构成全仓库排除性证明.

## 交付给协调器的更改路径

本任务只写 checks-author. 主库最小更改入口为以下原路径; 是否已由其它作者修好不在本报告判断中.

1. 数学原文及直接文档: `docs/SL_gap_nge2_symmetry_local_proof.tex`, `docs/SL_gap_nge2_symmetry_recon.tex`, `docs/SL_gap_extremals.tex`, `docs/SL_spectral_topics_summary.tex`.
2. 工具卡: `tools/gap-band-extremals.md`, `tools/feynman-hellmann.md` (R7-P01), `tools/band-selfconsistency-equivariance.md`, `tools/half-problem-regularized-green.md`, `tools/green-half-inertia.md` (R7-P02 范围/等价表述).
3. 当前仍可运行的旧诊断如继续保留为验证入口: `scripts/op03_gap_fh.py`, `scripts/gap_n1_grad.py`, `scripts/_tmp_fh_paradox.py`, `scripts/tmp_fh_test.py`, `scripts/tmp_verify_endpoints.py`, `scripts/_gapn2_hess_verify.py`.
4. Hessian 逐元素乘法: `scripts/_gapn2_hess_sign_and_bigR.py`, `scripts/_gapn2_jacobian_analytic.py`, `scripts/_gapn2_o3_scan.py`, `scripts/_gapn2_second_variation_probe.py`. 应新增实际回归及版本化输出后才引用其 Hessian 惯性结果.

旧冻结 run/review/历史 JSON 不在修改清单. 旧文稿插入维护器 `_aug_tex_insert.py` 中也保留过时文本, 本轮没有运行它, 它不应被重新用作当前修订入口.
