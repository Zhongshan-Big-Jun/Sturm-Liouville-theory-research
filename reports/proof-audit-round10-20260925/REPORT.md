# 第十轮审计修订

已核实并修复两项程序错误：固定网格漏掉近邻低频根后的谱编号错配，以及把反射作用误当作扇区投影。共享根引擎、同指标高精度细化、真实反射种子、当前工具卡和研究入口已同步；解析、软件、形式化的验收范围分别列在下文。全局 O1/O2/G1′、有限反差唯一性仍开放。

用户输入为 `C:/Users/HuangZY/Downloads/sl_audit_round10`，基线为 `5bb6b2605122d2daf472863b4bec0f35a9c192e1`。附件按待核实证据读取，原字节、manifest 校验和正常/`-O` 回放见[输入与回放](../../research/artifacts/proof-audit-round10-20260925/)。附带程序两次各通过 23 组检查；这些是有限诊断，不是 23 个新定理。

## 1. 问题与修复

| 问题 | 核实结果 | 当前行为 |
| --- | --- | --- |
| R10-01 低根被跳过 | 真实旧 `roots_of` 在块长 `(0.02,0.96,0.02)`、密度 `(10000,1,10000)` 上，把约 `3.2671480773` 标作首根；其前至少存在报告给出的四个根 | 连续提升 Prüfer 相位保留整圈信息，对每个 `n*pi` 独立二分；每项保存编号、相位水平、括区和残差。精度不足或根不可分辨时明确失败 |
| 高精度细化及 FD 继承错号 | 小残差、正根、排序均不能识别漏根 | `checked_roots` 检验实际相位指标；mp 细化和所有有限差分端点显式传入同一一基谱指标 |
| R10-02 反射扇区混淆 | 旧全索引赋值只是 `-Jv`，不是投影；物理反射是 `R(x)=1-Jx` | 保持投影 `(I-J)/2`，破缺投影 `(I+J)/2`；检查参数转换后真实接口位移，使用有界重采样和步长回退，记录拒绝原因 |
| 文稿传播 | 旧 `(a,-reverse(a))` 和“反对称坐标平面”都保持几何对称，不能充当纯破缺探索 | 撤回该解释；标签只指初始种子，不约束后续优化轨迹。列状态从左向右传播应为 `P_new*M_old`，早期未保存变体的失败原因不再猜测 |

核心实现为 [_sl_prufer.py](../../scripts/_sl_prufer.py)、[reflection_seeds.py](../../scripts/reflection_seeds.py)、[侦察入口](../../scripts/_gapn2_symmetry_recon.py)与[二阶变分入口](../../scripts/_gapn2_second_variation_probe.py)。原 `npts` 参数保留兼容，但不再决定根编号。

[解析契约](../../research/artifacts/proof-audit-round10-20260925/analytic-repair.md)推导正分块密度下相位的频率严格单调性、零/无穷端点、逐项 Dirichlet 指标、密度比较括区及块间坐标转换。实现保留最后一块的局部相位；它是参考相位的正角度变换，固定全部 `n*pi` 水平。避免反复转换到密度 1 的坐标，减少极端常密度的数值损失。

双精度和 mp 实现共享相位思想，其一致性不算独立枚举证据；独立检查另外使用物理解 `A cos+B sin` 的实际零点计数和有限有理端点符号包围。一般求解器输出明确标 `certified:false`，尚无全参数严格区间认证。

## 2. 实际执行与旧结果的边界

作者/协调器回归：241 项谱检查、21 项反射检查，均在正常和 `-O` 下通过。包括高反差反例、前缀至 2001 模、常密度/缩放/反射/分块不变性、错号根表和不可分辨输入、真实坐标转换、零投影与不可行步长。

另一个 `fork_context:false` 软件检验者亲自重跑上述两组，新增 122 项对抗检查和 263 项产物/来源检查。它独立重建了四个端点括区的有理 Taylor 包围，分别处理理想有理块长与实际 binary64 块长；这些只认证相应有限括区的根存在性。私有执行的实际模块来源、子进程、失败记录和哈希见[独立软件执行](../../research/artifacts/proof-audit-round10-20260925/software-execution/)。

| 当前实际程序 | 执行范围 | 结果与限制 |
| --- | --- | --- |
| 二阶变分 CLI，协调器 | `n2 R4 SUP/INF`、`n3 R4 SUP`、`n1 R1 SUP`，默认 61 模、64 点求积、60 位细化 | 全部成功；这四种配置的新旧前 61 个频率最大差约 `5.7e-14`。不能据高反差反例断言所有旧 R4 数值错误 |
| 二阶变分 CLI，独立检验者 | `2 4 sup`、`2 4 inf`、`2 1 sup`，相同当前默认参数 | 实际重算通过；所查直接块积分切向残差最大约 `5.86e-15`，仍受谱截断、求积和有限步长限制 |
| 侦察 CLI，协调器 | `2 4 16 both 4`；SUP/INF 各 112 个破缺种子、24 个保持种子、16 个普通随机种子 | 纯扇区输入全部通过几何检查；SUP 有 16 个种子缩小步长。SUP/INF 分别有 110/113 个求解成功，只是此次有限探索 |
| 侦察 CLI，独立检验者 | 两种图案各 14 个破缺、6 个保持、2 个普通随机种子；另试不对称基点 | 实际入口运行成功；不对称基点每种图案的 10 个扇区请求全部明确拒绝。Linux 私有临时目录修复了审查环境 Unix socket 问题，原失败保留 |

静态[调用闭包](../../research/artifacts/proof-audit-round10-20260925/caller-inventory.json)含 76 项；共享引擎会改变其下次执行，但本轮没有重跑全部历史 Green/Jacobian/扫描。原数值 JSON、旧证书和旧冻结 run 保留原字节。有限符号样本或未找到非对称解均不能证明 Hessian 定性、G1′或全局唯一性。

更早的 `docs/SL_gap_extremals.tex` 按工具卡标注保留为历史数值来源，其传播故障归因没有在本轮核实，也不因本次更新成为当前证明。脚本导航另加了明确说明；本轮修订的当前侦察总结是 `SL_gap_nge2_symmetry_recon.tex`。

## 3. 独立审查与局部 Lean

所有最终检验者均通过实际 `fork_context:false` 调用，以冻结最小材料启动；作者不担任验收者。原生调用、返回值、精确包哈希、当前输入绑定和接收验证见[审查索引](../../research/artifacts/proof-audit-round10-20260925/review-summary.json)。信任界限是插件记录的 `COORDINATOR_ATTESTED_TOOL_TRANSCRIPT`，不声称 OS 沙箱或服务端密码学见证。

| 检验 | 新隔离会话 | 结论 |
| --- | --- | --- |
| 解析修复与4张卡的11项义务 | `01a0d77d-175b-7591-9683-1f6f8dae4c15` | [APPROVED](../../research/library/reviews/runs/f2452b35e015b16a26ed6cf4e476a6b3e1f833a42b6d2ebc2603df84b3e26fc4-01a0d77d-175b-7591-9683-1f6f8dae4c15/report.json) |
| 4张未变卡的4项续审义务 | `01a0d77d-c885-7532-ae36-d32f820ee134` | [APPROVED](../../research/library/reviews/runs/665b4761a3d8b19dd39eaaa343a600d53a0e8893f7a3b0422069da5add70db3a-01a0d77d-c885-7532-ae36-d32f820ee134/report.json) |
| 真实程序、根编号、反射种子与实际入口 | `01a0d73c-92aa-7ff2-8a20-d96d6bc32340` | [APPROVED](../../research/artifacts/proof-audit-round10-20260925/software-review/research/library/reviews/runs/8b23fae8c1c87a24a4abbfae81a47b0eabd492562c2fdc54f43f961c720a6f33-01a0d73c-92aa-7ff2-8a20-d96d6bc32340/report.json) |
| 38项声明盲读；不构成语义放行 | `01a0d74b-2c67-7a52-b0b8-f43dd64f1c31` | [APPROVED](../../research/artifacts/proof-audit-round10-20260925/formal-readback/research/library/reviews/runs/860efb04a2090bd7739ab0ad6e0c3ff259fa9ee0d3f8fde33d4192a3d66f01d1-01a0d74b-2c67-7a52-b0b8-f43dd64f1c31/report.json) |
| 独立重编译、类型/定义/公理及合同保真 | `01a0d758-ba63-7c90-afcf-448c39dd27a9` | [APPROVED](../../research/artifacts/proof-audit-round10-20260925/formal-comparison/research/library/reviews/runs/708d2046047362d43699651aecc53275635c346d55e27618ddbd00b692ba147a-01a0d758-ba63-7c90-afcf-448c39dd27a9/report.json) |

新增 [AuditRound10.lean](../../lean-proof/SL/AuditRound10.lean)，22 个具名定理、6 个定义/缩写，完整导出 38 项声明（含编译器辅助项），根目标为 21 项显式合取。固定 Windows PE Lean 4.31.0 经 WSL 运行；作者原版验证器的最终固定快照 `exact-root-02` 成功，预期类型/绑定器/宇宙参数匹配，根传递公理仅 `propext`、`Classical.choice`、`Quot.sound`。独立检验者在新目录亲自重编译、核对类型/定义与公理，并检查三个错误目标和其精确否定的正证明。

形式化证明真实 `Fin(2*n)` 坐标反转、两种互补正交投影、仿射反射扰动，以及显式连续/严格单调/逐项括区前提下的唯一根和指标排序。`k=0`、零维、闭括区端点都在量词内；严格递增的指标序列可以跳号，只有另外选择连续指标并提供逐项括区才能表达相应覆盖。它不证明实际 Sturm ODE、相位提升、谱识别、比较括区的存在、浮点误差或 Python 实现正确性，也不证明物理接口可行性和全局极值。

[逐目标契约与作者执行](../../research/artifacts/proof-audit-round10-20260925/lean-author/)及[独立形式化审查](../../research/artifacts/proof-audit-round10-20260925/formal-comparison/)保留可重放证据。大体积原始 JSON 采用无损 gzip，同时登记压缩前后哈希。旧 50 份 SL Lean 源和原环境不覆盖；没有运行全项目 Lake build。

## 4. 工具库、地图与复用

使用已安装 2.0.1 原版纠错/审查/索引 API，先隔离数值支持的复用，再保存新卡、逐事项审核并按依赖顺序放行。四张直接修订卡为 `band-selfconsistency-equivariance`、`green-half-inertia`、`half-problem-regularized-green`、`second-variation-weighted-eigenvalues`。另外四张正文未变卡 `feynman-hellmann`、`gap-band-extremals`、`secular-chebyshev-jacobi-rootcount`、`bloch-band` 完成整包绑定变化所需的同版本续审。

共 15 项“精确版本 × 事项”义务完成；多事项卡在最后一项释放前出现的 `STILL_BLOCKED` 是按实际状态保留的正常中间结果。新增五条版本绑定的纠错经验批注。第五条对应 `gap-band-extremals` 卡第 46 行：该卡仍保留旧传播故障归因的历史文字，原实现缺失，不能认证这一归因。续审报告明确排除了它；当前检索同时返回更正批注，要求按已核实的列状态约定阅读，不把历史猜测作为可复用结论。批注沿用原模块的 `CANDIDATE_ANNOTATION` 标记，不充当新增数学证明或替代审查回执。

最终实际查询为 **89 张可用、1 张原撤回**，逐张核对当前哈希、摘要、来源/证据、依赖及五条新批注，不以数量代替内容核验。保留 75 条历史失效回执警告；没有删除历史或绕过门禁。见[当前库核验](../../research/artifacts/proof-audit-round10-20260925/integration/library-verification.json)。

[研究地图](../../research_map.md)新增 B8 数值探索支持节点，B4 总体仍为 PARTIAL；[项目理解](../../docs/PROJECT_UNDERSTANDING.md)、双语首页、前沿、工具/脚本入口、Lean 状态/声明索引、AGENTS 与续接记录均已更新。[侦察 PDF](../../docs/SL_gap_nge2_symmetry_recon.pdf)重建为 5 页，并检查修改页版面。既有文献吸收的域、三迹闭包、替代 Riesz 系和有限界面解析公式没有被本轮两项诊断错误否定，也没有在本轮被宣称整链重新认证。

## 5. 保留的失败与交付

首次独立数学审查返回 `CHANGES_REQUIRED`：可行步长的一侧上界漏写 `t>=0`，且文稿经验总结仍把未保存变体的失败归因于传播顺序。现明确基点宽度 `w_i>h`、非负步长条件，并补出完整有符号可行区间和精确反例；经验总结与详细段落统一为已核实的列状态乘积约定，历史失败原因保留未核实。新的源绑定卡和文稿另由全新检验者审查；四项先前已通过的未变卡续审也因输入变化重新绑定。首次退回与已过期的续审成功记录均保留。

软件检验对应未再改动的 Python 源和实际执行，不承担上述错误文档量词的验收；程序本来就要求正步长大小。初版相位坐标反复转换导致极端常密度回归失败，已修并保留原候选/日志；TeX 排版宏错误经 PDF 检查发现后修复，相关卡和审查包重新绑定，旧未派发包不算验收。Lean 开发失败、第一次根检查因开发目录变化被判 stale、打印截断后重导出，以及独立检验的环境临时目录失败均保留原记录。最终 fixed-root 成功不能倒改这些历史状态。

基线 13818 个 tracked、134 个原 untracked、6 项原 dirty 按字节保护；canonical、旧已发布证据、旧工具版本及旧 Lean 源不改写。本轮插件源码和安装缓存未变。精确发布清单见[publication-manifest.json](publication-manifest.json)，续接先读 `F:/tools/math-audit-round10-20260925/CURRENT.json`、实际持久任务和 `DELIVERY.json`，不重启已完成研究者。提交按已授权顺序同步 `origin/main` 后 `fork/main`；最终提交号和实际远端头以 Git 与外部交付记录为准。
