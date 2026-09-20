# 第二轮审计 Lean 作者交付

角色: 数学形式化作者. 本报告给出作者实际编译和公理检查结果, 不代表最终验收或独立语义审计. 独立、无状态隔离 review 仍待执行.

## 交付结果

- 主模块: `/mnt/f/LaTeX/BVE research/lean-proof/SL/AuditRound2.lean`.
- 主模块包含 12 个定义和 25 个定理, 原生 Windows Lean 4.31.0 实际编译成功, 退出 0, 无编译警告.
- `InspectAuditRound2.lean` 实际导入该新产物, 对所有 25 个定理执行 `#print` 和 `#print axioms`, 退出 0. 定义的实际展开也已打印.
- `BridgeToExistingSL.lean` 另有 5 个与既有 SL 定义的等价性定理, 实际检查成功, 退出 0. 它是外部作者工件, 不进入主模块导入链.
- 上述 30 个目标的传递公理均属于 `{propext, Classical.choice, Quot.sound}`. 没有 `sorryAx`, 新增公理或 `native_decide` 证明. 25 不表示 25 个完整谱定理通过.
- 主文件 SHA-256: `5a8708c3a756e1bb86974fb887b30458290498ad0cde0fd452bdcaf250b2f050`.
- 新编译 `AuditRound2.olean` SHA-256: `5ee031678967d2a9da02d4a850ffba6edc61a67ff898d31aba78d944b88bff84`.

类型与公理原始输出在 `logs/14-print-types-axioms.stdout.txt`, 结构化提取在 `declaration-evidence.json`. 兼容性证明输出在 `logs/16-existing-sl-bridge-merged.stdout.txt`, 传递公理汇总在 `bridge-evidence.json`.

## 来源与输入固定

实际读取材料为:

1. 用户提供的 `/mnt/c/Users/HuangZY/Downloads/proof_audit_round2_20260920.md`, 重点 B05、B06、B07.
2. 根 `AGENTS.md`, 以及外部工具目录的适用指令. 本轮明确的可写范围优先于通用的 AGENTS 维护要求.
3. `docs/SL_third_order_K1_proof.tex`, “Exact factorization” 与 “Finite backward solutions and the fixed-index limit”.
4. `docs/SL_mw_lemma_reproof.tex`, affine invariance 与 cell extension.
5. `docs/SL_ratio_proof.tex`, 主定理证明和第 3 节平衡相位候选计算.
6. `lean-proof/SL/ThirdOrder.lean`, `ThirdOrderClosedForms.lean`, `BalancedPhase.lean` 的相关定义.

`source-baseline.json` 固定进入时读取的 51 个文件的 SHA-256. `source-snapshot/` 保存审计输入、三份相关 TeX 和相关 SL 源文件的初始字节. 本轮输入是工作区实际内容, 不能把审计附件写出的历史固定提交号误认为当前未提交工作区的完整状态.

本轮没有重做审计 B01-B04/B08, 也没有把附件提到的 `ratio_first_pair_repair.md` 变分证明纳入形式化.

## B07: K1 终端差分

定义使用实际二阶差分和阶乘缩放:

\[
d_j=v_j-2v_{j-1}+v_{j-2},\qquad v_j=\mu_j/(2j)!.
\]

| 声明 | 精确支持范围 |
| --- | --- |
| `terminal_difference` | 在任意域中, `v N=0` 与 `v (N-1)=0` 推出 `d N=v (N-2)`. 不能推出零. |
| `difference_step_iff` | 缩放三阶等式与 `d_j=c_j d_{j-1}` 的单步代数等价. |
| `solution_difference_step` | 将该代数等价用于一个明确的三阶递推谓词, 对所有 `n+3` 给出差分递推. |
| `factorial_shift_four` | 精确的四步阶乘展开, 非数值近似. |
| `k1_terminal_value` | 对任意 `n : Nat`, 令 `N=n+3`, 从三个终端值和原始 `j=N+1` 的递推等式推出 `d_N=N/((N+1)(2N)!)`. |
| `k1_terminal_formula_pos` | 上述闭式对所有 `N=n+3` 严格为正. |
| `k1_n3_last_equation`, `k1_n3_difference`, `k1_n3_difference_ne_zero` | 一个确实满足最后一步原递推的 N=3 终端片段给出 `d_3=1/960 != 0`. |

`k1_terminal_value` 的假设是 `mu_(N+1)=1`, `mu_N=mu_(N-1)=0`, 以及含 P、Q、R 的最后一条原递推. 证明先导出 `mu_(N-2)=1/R_(N+1)`, 再展开阶乘. 它没有把 `d_N` 的目标值作为假设. 三个系数显式定义为源中 c=1 的有理数公式.

索引 `N=n+3` 覆盖全部 N>=3, 避免在关键计算中误用自然数截断减法. 通用 `terminal_difference` 的定义在自然数上使用截断减法, 但 K1 实例只用于 N>=3.

N=3 片段用于验证最后的 j=4 方程, 并未声称 `k1_n3_segment` 在所有指标都解整个递推; 尤其它没有构造源中的 `mu_0=11/480`. 不应把这一局部片段误读成完整有限解.

**未证明:** 对任意 N 的完整向后解构造与唯一性, 全部阶乘缩放等式的装配, 源式 (7) 的有限和式, 固定指标极限, 最小解唯一性, 正项级数与尾项估计, 或 `K(1)=e/4`. 本轮修正的是实际终端代数桥.

## B06: MW 有符号 cell 传输与尺度

设左、右端点斜率为 L、R, L!=0, 定义 `b=R/L`. 这里不假设 b 为正.

`mw_signed_slope_matching` 证明对每个自然数 j、任意实数尺度 a:

\[
b^j a R=b^{j+1}aL.
\]

`cell_branch` 定义实际分支

\[
u_j(x)=b^j y(a(x-x_j)-1/2).
\]

`cell_branch_has_deriv` 用链式法则得到 `b^j a y'`. `mw_cell_interface` 在 a!=0、L!=0、原函数两端取零且两端存在指定导数的假设下, 证明相邻两个分支在 `x_j+1/a` 的函数值和实际 `deriv` 相等. 这比只检查斜率常数的乘法恒等式更直接.

`mw_affine_has_deriv` 与 `mw_affine_ode` 从真实 `HasDerivAt` 假设推导

\[
-y''=\lambda\rho y
\quad\Longrightarrow\quad
-(A y(cx+d))''=(c^2\lambda)\rho(cx+d)\,A y(cx+d).
\]

因此拉回到新区间时的系数是 `c^2*lambda`. `mw_scaled_ratio` 在 c!=0 时证明两个系数同比缩放后比值不变. 这里的除法是 Lean 实数上的总除法; 若要把它解释为谱比值, 仍须另外提供正特征值等谱前提.

`second_sine_mode_endpoint_slopes` 实际证明 `y(x)=sin(2*pi*(x+1/2))` 的两端导数均为 `2*pi`. `second_sine_mode_transmission` 因而得到 `b=1`, 旧约定 `-R/L=-1`. 没有把第二模态端点斜率的错误符号写入假设.

**未证明:** 从有限个相邻分支构造全局 C1 函数的拼接定理, 分段系数的弱解接口, 端点初值唯一性, 传输后非零性和完整零点计数, Sturm 振荡, doubling 定理, 截断共同零点情况, 零点参数运动, 或密度类之间的谱连续性推广.

`mw_affine_ode` 的假设是原函数和其导数在实线上具有给定导数, 因而适用于这里的光滑 cell 模型; 它没有伪装成分段密度在所有接口处都 C2 的定理. 它也允许 A=0, 所以仅凭该微分等式不能宣称已经构造非零特征函数.

## B05: 候选达到、doubling 与缺少的上界

`attained_le_sup` 对非空性的具体见证 `C in S` 和 `BddAbove S` 证明 `C<=sSup S`. `balanced_candidate_le_sup` 在 s>0 时, 将源中两个平衡相位平方表达式的比值化为

\[
C(s)=\left(\frac{\pi-\arccos(s/(s+1))}{\arccos(s/(s+1))}\right)^2
\]

并仅推出其不超过集合的上确界. “此比值属于实际谱比值集合”仍是明确的成员假设, 本文件没有定义该谱集合或把成员关系当作已证谱定理.

`attained_sup_eq_iff_upper_bound` 精确陈述: 在达到和有界条件下, `sSup S=C` 当且仅当 `forall x in S, x<=C`. 这是对缺失义务的识别, 不是把这个全局上界假设输入后再宣传为最优性证明.

`adjacent_ratio_le_of_doubled` 说明一个已有的倍指标上界可以传给相邻指标, 所需条件显式为单调序列、n>=1、分母正. 它不计算这个上界的具体数值.

`attainment_doubling_countermodel` 给出任意 C 和任意待宣称的上界 U 的实际反模型:

\[
S=\{C,\max(C,U)+1\},\qquad D_n=S.
\]

机器证明 S 有上界、C 被达到、每个 n 的 doubling 上确界恒等式成立, 同时 `U<sSup S`. `no_candidate_upper_bound_from_doubling` 专门否定从这些抽象前提出发推出 `sSup S<=C` 的普遍推理规则.

**反模型边界:** 这是序论前提的反模型, 没有构造 Sturm-Liouville 权重, 不反驳具体候选闭式在实际谱问题中的正确性. 首对全局最优性的变分证明仍是未形式化的 gap.

## 与原 SL 定义的连接

为使主模块只导入所需 Mathlib, 主文件使用独立定义. 外部 `BridgeToExistingSL.lean` 已额外验证:

| 外部定理 | 检查的等式 |
| --- | --- |
| `recurrence_interface` | 本轮三阶递推谓词 = `SL.ThirdOrder.IsSolution`. |
| `p_at_one` | 本轮 `k1_p` = `SL.ThirdOrderClosedForms.PEven 1`. |
| `q_at_one` | 本轮 `k1_q` = `SL.ThirdOrderClosedForms.QEven 1`. |
| `r_at_one` | 本轮 `k1_r` = `SL.ThirdOrderClosedForms.REven 1`. |
| `theta_identity` | 本轮 `candidate_theta` = `SL.BalancedPhase.theta`. |

这是公式级机器连接. 为避免重建旧工程, 外部探针使用复制到外部目录的 3 个既有 SL 编译对象; 路径和 SHA-256 在 `existing-sl-cache-copies.json`. `SL.Basic` 单独从现有源码重新编译到外部目录. 原 SL 文件和项目缓存未被覆盖. 桥接日志同时打印了实际导入的旧定义展开, 但本轮不声称重新检查了所有历史 SL 证明体或全部原源文件与旧缓存的一致性.

## 环境、命令与真实失败

- 实际程序: `/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe`.
- 实测版本: Lean 4.31.0, `x86_64-w64-windows-gnu`, commit `68218e876d2a38b1985b8590fff244a83c321783`.
- 实际 Lake: 同目录 `lake.exe`, version `5.0.0-src+68218e8`, Lean 4.31.0.
- 项目与 Mathlib 的 `lean-toolchain` 均固定 4.31.0. Mathlib checkout 为 `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`, 与 lake-manifest 一致; 共 9 个包的 HEAD 全部匹配锁定 revision.
- 所有 Lean 程序 cwd 均为 `/mnt/f/LaTeX/BVE research/lean-proof`. `run_lean.py` 只在子进程中设置 Windows 格式的 `LEAN_PATH` 和相应 `WSLENV`; 未更改全局默认 toolchain 或环境.
- Lake 实际执行了版本与帮助检查. 编译使用上述原生 Lean 直接入口和已有 Lake/Mathlib 缓存, 没有调用 `lake build`, `lake update`, `lake env` 或 cache 下载, 没有下载或重建整个 Mathlib.
- `command-index.json` 和 `logs/*.json` 保存实际 argv、cwd、环境、退出码、耗时、输入前后 SHA-256 与 stdout/stderr SHA-256. `attempts/` 保留各轮输入源码, 失败日志未覆盖.

| Run | 结果与含义 |
| --- | --- |
| 01-03 | 原生 Lean/Lake 版本、帮助, 退出 0. |
| 05-basic | 全量 Mathlib 导入下编译原 `SL.Basic`, 退出 0, 422.65 秒. 该慢作业最终成功, 不能写成超时失败. |
| 06-third-order | 退出 1, 328.76 秒. 作者过早并行启动依赖作业, 外部 `SL.Basic.olean` 尚不存在; 保留真实顺序/解析失败. |
| 07-basic-deps | `lean --deps` 退出 0, 确认原生路径解析. |
| 08-minimal-probe | 最小 NormNum 实际证明, 退出 0, 16.28 秒. |
| 09-stop-uncompleted-full-imports | 停止旧作业的尝试退出 1, 因 PID 33976 已不存在. 以 05/06 实际退出结果为准, 不宣称两者均被成功终止. |
| 10-audit-draft | 退出 1. 实数除法定义缺 `noncomputable`, 导数表达式转换尚未闭合. |
| 11-audit-fixes | 退出 1. 正弦导数化简尚缺 `one_mul`. |
| 12-cell-interface | 退出 1. cell 函数需要先展开以匹配导数类型. |
| 13-interface-fix | 主文件实际编译退出 0, 18.96 秒, 无警告. |
| 14-print-types-axioms | 实际类型与传递公理提取退出 0, 18.62 秒. |
| 15-existing-sl-bridge | 退出 1. 优先命中的外部 SL 目录缺少旧模块对象; 原解析不会自动拼合两个 SL 命名空间目录. |
| 16-existing-sl-bridge-merged | 将 3 个既有对象复制至外部统一目录后, 5 个公式连接证明实际检查退出 0, 38.43 秒. |

原生编译的核心命令如下; 完整搜索路径以对应 JSON 记录为准:

```text
cwd: F:\LaTeX\BVE research\lean-proof
F:\DevCache\elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe -o F:\tools\math-audit-round2-20260920\lean-author\build\SL\AuditRound2.olean SL/AuditRound2.lean
F:\DevCache\elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe F:\tools\math-audit-round2-20260920\lean-author\InspectAuditRound2.lean
F:\DevCache\elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe F:\tools\math-audit-round2-20260920\lean-author\BridgeToExistingSL.lean
```

## 写入范围、复核入口与未决事项

本作者在项目内仅新建 `lean-proof/SL/AuditRound2.lean`; 其余写入均在本外部 `lean-author/` 目录. 42 个既有 SL 源文件、STATUS、lakefile、lean-toolchain、lake-manifest 的哈希均保持不变. 未改 canonical, 未 stage/commit/push.

`protected-source-comparison.json` 同时记录: 并行工作期间根 AGENTS 和三份相关 TeX 已发生字节变化. 这些不是本作者的写入, 也没有被回滚. 证明来源快照与这些并行变化分开保留, 不能宣称全工作区所有文件均未变化.

`loaded-modules.json` 由 Lean 实际加载环境导出. `imported-artifact-hashes.json` 对主模块检查所加载的每个模块及存在的 `.olean.private` / `.olean.server` 伴随对象记录 SHA-256. 该清单的范围是主模块类型/公理检查, 不是对全 Mathlib 或全工程定理的重新验收. 对象哈希在检查之后计算, 每个文件读取前后核对大小与修改时间; 本地编译器与已有依赖对象仍属于信任边界.

复核者可用唯一的新 run 名称运行以下命令. 脚本拒绝覆盖同名历史记录:

```bash
cd '/mnt/f/LaTeX/BVE research/lean-proof'
python3 '/mnt/f/tools/math-audit-round2-20260920/lean-author/run_lean.py' reviewer-build-01 SL/AuditRound2.lean
python3 '/mnt/f/tools/math-audit-round2-20260920/lean-author/run_external.py' reviewer-inspect-01 InspectAuditRound2.lean
python3 '/mnt/f/tools/math-audit-round2-20260920/lean-author/run_external.py' reviewer-bridge-01 BridgeToExistingSL.lean
```

这些命令用于机器复现, 不定义独立验收结论. 最终复核需重新阅读这里列明的假设与数学范围, 特别是 K1 无限极限、MW 完整谱链、首对全局最优性三个 gap. 本作者未对它们给出伪通过状态.

最终依赖清单: 3740 个实际加载模块, 11218 个对象文件, 2641846312 字节; 只读哈希耗时 248.93 秒. `FINAL_CHECKS.json` 保存作者收尾核对, `FILE_HASHES.sha256` 固定本次交付文件字节.
