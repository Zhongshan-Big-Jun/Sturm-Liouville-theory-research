# 第七轮审计修订

本轮报告中的四项错误及核查时发现的直接传播问题已修订. 当前解析修订、五张工具卡、程序修订及局部 Lean 均有各自范围明确的独立验收. 研究地图、项目理解、工具指针和续接入口已同步. 下文区分分析证明、有限计算、形式化片段与历史内容.

## 输入与结论

用户提供 [proof_audit_round7_20260921.md](../../research/artifacts/proof-audit-round7-20260921/submitted/proof_audit_round7_20260921.md), 原话“继续修订”, 指定 math-research-workflow. 输入 SHA256 为 `da832b1ae27e76958145ccf37bbd5a56f8e27ac860695c35d10ef1dbfbd58cb0`. 附件作为待核查证据; 文中提及的 `spectral_repairs.md` 与 `checks.py` 未提供, 本轮没有声称读取或重放它们. 补证与检查由当前源码重新构造. [接收记录](../../research/artifacts/proof-audit-round7-20260921/intake.json)保留来源身份.

| 项目 | 核实与修订 |
| --- | --- |
| R7-F01 | 一般指标的常密度 Wronskian 改为正确有限和, 端点二次系数补足 pi². 原 n=2 根公式正确; 非退化性补充精确行列式. |
| R7-F02 | 撤回跨跳点全局 C3 及依赖首块宽度的统一 Taylor 论证. 改用可测盒密度的全区间 Volterra 估计、权归一化、两端负性及 C1 根隔离, 补齐整个升序区域 U 中的弱反差唯一性和整块符号. |
| R7-F03 | 4pi² 限于 n=1. 证明任意固定 n>=1 的可测盒类及不限块数的有限分块类上确界极限为 (n+1)²pi²; 不将其等同于一条未经全 R 延拓证明的自洽分支. |
| R7-F04 | 镜像接口反向成对移动的导数补因子2; 单接口公式保持原系数. 用非驻点而非驻点残差检验. |
| R7-P01 | FH 工具卡区分固定 L2 势扰动与变权弦. 广义特征问题始终使用真实分母; 常系数 rho=2 的势扰动例直接反驳旧混用. |
| R7-P02 | 修正相邻后段及三卡的行列式/惯性混同、漏 lambda、行列式符号冲突及不同 ODE 解之间的错误 Cauchy 唯一性推断. 区分正的极限间距与尚未证明的定量盒类下界. |
| R7-P03 | 五卡显式保存与正文一致的新 summary, 清除检索预览继承的旧归一化与范围声明. 默认查询逐张核对正文版本、摘要与依赖. |
| R7-P04 | 协调器最初遗漏三张下游卡在上游 FH 纠错事项下的独立复核义务, 导致局部释放后仍受阻. 补齐三项精确版本修订, 经另一个新隔离会话审查后释放; 原受阻结果保留. |
| R7-SW-001 | 首次软件审查发现验证器先过滤外部模块再检查隔离. 修复为完整文件模块来源记录、必需模块的路径/哈希校验, 并增加真实外部导入与缺失模块对照. |

数学主入口为 [局部对称性证明](../../docs/SL_gap_nge2_symmetry_local_proof.tex)及其 [15页 PDF](../../docs/SL_gap_nge2_symmetry_local_proof.pdf). 同步修订 [谱隙总结](../../docs/SL_gap_extremals.tex)与 [侦察总结](../../docs/SL_gap_nge2_symmetry_recon.tex), PDF 分别为8页和5页. 三份均实际重建, 修改页作视觉检查, 全页文本及边界检查见 [PDF 证据](../../research/artifacts/proof-audit-round7-20260921/pdf-evidence/manifest.json).

谱隙数值总结保留原历史推导和数值记录. 其中旧的未乘2导数显示式已由首页第七轮更正声明取代, 不能作为当前有效公式引用; 当前公式与参数定义以修订后的谱隙工具卡为准.

## 数学修订的精确范围

令 theta=pi*x, 常密度归一化为 u_k=sqrt(2)sin(k*pi*x). 修正为

\[
W_n(x)=\pi\bigl[\sin((2n+1)\pi x)-(2n+1)\sin(\pi x)\bigr]
=-4\pi\sin(\pi x)\sum_{j=1}^{n}\sin^2(j\pi x)<0
\]

其中 n>=1, 0<x<1. n=2,x=1/2 时值为 -4pi, 旧式给 -6pi. 端点二次系数是 `2*pi^4*(n^4-(n+1)^4)`. n=2 的根 `t=(11±2sqrt(10))/36` 保留; 对 F=f/(9pi²), 精确四接口行列式为 `7030400000*pi^4/4782969`.

统一端点引理对所有可测 `1<=rho<=1+epsilon` 成立, 不要求最短块宽为正. 射击解与其导数由 Volterra 方程一致控制, 权范数有统一正下界, 从而归一化特征函数在 C1 中接近常密度解. 端点斜率间隙给出一致负性, 内区间根隔离排除合并或新增零点, 再接隐函数定理得到每个图案在整个 U 中的弱反差唯一解. 这不是全 R 唯一性定理.

一般上确界证明取 `h=1/(n+1)`, `delta=min(h/12,R^(-2/3))`, 在 jh 周围放置半宽 delta、密度 R 的 n 个薄重层. n 维平台空间与中心取零的余维 n 空间分别给出

\[
\lambda_n\le\frac{12}{5hR\delta},\qquad
\lambda_{n+1}\ge\left(\frac{h^2}{\pi^2}+\frac{(R-1)\delta^2}{2}\right)^{-1}.
\]

结合普遍上界 lambda_(n+1)<=(n+1)²pi² 得到所述极限. 不需要有限 R 上确界取到, 也不需要构造满足自洽驻点方程. [研究地图](../../research_map.md)新增 B4-SUP-LIMIT 子问题, B4 仍为 PARTIAL; 有限 R 全局唯一性、完整 G1'/G2 和 INF 分类没有因此闭合.

## 分离的验证证据

最终审阅会话均以 `fork_context:false` 启动, 只接收冻结材料; 数学作者、独立执行与语义审阅分开. 原生调用及实际完成文本按字节保留, 它们是协调器记录的工具信封, 不是密码学服务证明. 下表同时保留补证前的 formal/INCOMPLETE, 当前形式化验收以 formal-v2 的精确回执为准.

| 审阅 | 会话 ID | 实际结论 | 证据 |
| --- | --- | --- | --- |
| math | `01a0c42a-ba6a-7392-a5ab-7a802f3b111b` | APPROVED | [绑定回执](../../research/artifacts/proof-audit-round7-20260921/reviews/math-review-receipt.json) |
| formal-v2 | `01a0c429-7e99-7a72-9098-a59e2cc321f8` | APPROVED | [绑定回执](../../research/artifacts/proof-audit-round7-20260921/reviews/formal-v2-review-receipt.json) |
| propagation | `01a0c472-537b-7750-83c9-bcc63703a8b0` | APPROVED | [绑定回执](../../research/artifacts/proof-audit-round7-20260921/reviews/propagation-review-receipt.json) |
| formal | `01a0c405-7e28-7693-833b-75338d4d5773` | INCOMPLETE | [绑定回执](../../research/artifacts/proof-audit-round7-20260921/reviews/formal-review-receipt.json) |

- [独立有限检查](../../research/artifacts/proof-audit-round7-20260921/numerical-review-v2/EXECUTION.json): 39个输入哈希核对, 普通与 -O 均为25/25组, 完整数值细节一致, 两次旧 FH 公式对照均退出1. 独立审阅者另用半区间特征方程、权积分及隐函数微分重建非驻点例. n=1,R=4,a=1/4 时谱隙导数约53.8809721602405715, 旧公式恰为一半. 高精度浮点样本不是区间证明.
- 解析审阅者另执行同一检查器的24项数学组, 普通/-O结果与所给结果一致, 并重新推导非驻点特征方程. 该解析审阅包没有执行harness和本地输入清单, 因而它没有重跑第25项记账检查; 上一项25/25来自另一个完整数值包的新会话, 两者不混记.
- [软件独立复验](../../research/artifacts/proof-audit-round7-20260921/software-review-v2/REVIEW.json): 十个程序修订及运行验证器通过其声明范围的审查. 正常和 -O 的候选117项有限检查通过; 原版本各79项失败. 实际 op03 CLI 的4个比较点与源码函数/AST检查分开记录; 8个模块来源/缺失绑定对照必须因预期原因拒收. 来源门禁是执行后观察与验收机制, 不是操作系统沙箱或恶意 sys.modules 修改防护.
- [局部 Lean 源](../../lean-proof/SL/AuditRound7.lean)含20个定理、7个定义. [新隔离执行](../../research/artifacts/proof-audit-round7-20260921/independent-execution-v2/EXECUTION.json)实际重新编译, 核对十部分根目标、全部显式声明、自己的新 olean 及导入解析. 传递依赖允许的公理为 propext、Classical.choice、Quot.sound; 两个错误目标对照实际退出1. 记录4365个已加载模块与13089个外部工件的哈希; 这些是环境记录, 不是最小证明依赖集.

Lean 覆盖真实三角函数导数、一般 n 的 Wronskian 恒等式与负性、旧 n=2 公式反例、端点系数代数, 以及显式单接口假设下的标量镜像合并和非零跳跃驻点等价. **没有形式化完整 Volterra 估计、谱可微性、权归一化积分、Taylor 余项、精确 n=2 行列式或无限维 min-max 极限.** 此次语义读回带有非形式化源码上下文, 不称盲读认证. 未运行全工程 Lake build;47个旧 Lean 源及旧环境配置保持原字节.

十个改动程序及其前后哈希见 [集成清单](../../research/artifacts/proof-audit-round7-20260921/software-integration.json). 已知 `op03_gap_precise.py` 的传播顺序会损坏权归一化; 当前 `op03_gap_fh.py` 使用既有 fixed 后端, 并经独立有限例核对. 其它依赖 precise 的历史程序保留, [脚本导航](../../scripts/README.md)已明确其限制. 本轮没有认证全部解析 Jacobian 后端、旧 Green/M3/KP 推导、历史大规模扫描或旧区间证书.

## 工具库、指针与研究经验

两条精确版本纠错记录为 `round7-gap-spectral` 和 `round7-inertia-and-propagation`. 五张当前卡通过最终解析审阅包逐项检查. 其中三张下游卡还同时受上游 FH 事项影响, 初次局部释放返回 STILL_BLOCKED; 补齐这三个继承义务并通过新的 propagation 隔离审阅后再释放. 共五卡、八项卡片/事项复核义务, 不混记原释放结果. 第一批未审候选因摘要问题被新版本取代, 不曾释放; 原错误版本和历史回执保留.

| 当前卡 | SHA256 |
| --- | --- |
| [feynman-hellmann](../../tools/feynman-hellmann.md) | `da33642d9b86de9587760ffc635f9b4e655fc86c6610b75c1732dc0920095611` |
| [gap-band-extremals](../../tools/gap-band-extremals.md) | `754852deebb0668b9ecb6c39386d91c050e5e6bf62c92a50c05c778b0f6bd723` |
| [band-selfconsistency-equivariance](../../tools/band-selfconsistency-equivariance.md) | `4328725971dd14adf1ad0774635100392bb235fd166bb82390ddb50acd67e331` |
| [half-problem-regularized-green](../../tools/half-problem-regularized-green.md) | `171764c0b23512ca48a7d3dfe410e506a9131ace5ce163aa3c65b1472012ea15` |
| [green-half-inertia](../../tools/green-half-inertia.md) | `8db06474e9d3fa790e6b62eacf8043cbd16237322cfebe1fe21d9bc775ce33b2` |

[实际默认查询](../../research/artifacts/proof-audit-round7-20260921/default-query.json)和[最终库状态](../../research/artifacts/proof-audit-round7-20260921/library-final.json)确认78卡可用、1卡仍隔离, 本轮五卡返回当前精确版本及显式新摘要. 库中保留 119 个版本、127 条纠错事件. 查询返回的34条旧复核告警记录对应17条不同的历史回执, 均逐项确认为被后续修订取代, 未删除或冒充当前批准. 原隔离项仍是 `left-definite-orthogonal-systems`.

新增两条绑定当前卡版本的研究经验批注: 一是统一估计与薄重层双向谱控制, 二是导数坐标、真实分母、非驻点回归及矩阵乘法的检验方法. 批注仍是候选研究经验, 不自动升级为新定理. [项目理解](../../docs/PROJECT_UNDERSTANDING.md)、中英文 README、PROJECT、研究导航、研究地图、工具索引、Lean STATUS 和 RESUME 均已同步; canonical 本轮未接收新节点.

## 保留的失败与修复过程

1. Lean 作者最初两次声明导出失败, 后修复导出器; 作者曾复用同 SHA 的已编译正目标恢复. 这些记录与最终新会话的完整重新编译分开保留.
2. [早期独立执行](../../research/artifacts/proof-audit-round7-20260921/independent-execution/ARCHIVE.md)为 INCOMPLETE: 旧冻结导出器失败; 数值包由协调器漏带 inputs/manifest.json, 当时实际24/25. 补齐材料后交不同新会话重跑, 不改写旧结果.
3. [首次软件审查](../../research/artifacts/proof-audit-round7-20260921/software-review/REVIEW.json)为 CHANGES_REQUIRED: 外部模块先被过滤, 所谓隔离检查不可接受. 新验证器保留完整来源, 加入必需绑定及真实反例. 修复作者首次运行还发现 Python 启动钩子超出允许来源, 改用显式 -S 启动, 没有将无关钩子一概加入允许列表. 失败与旧过滤逻辑的敏感性实验均保存.
4. 首次形式化语义审阅认可局部陈述及新编译证据, 但因审阅包未带两次早期导出失败的原日志而 INCOMPLETE. 补齐原始退出记录与诊断后交新隔离会话审查; 未为此修改数学源或追加编译.
5. 修正正文后仍发现默认预览继承旧 FH 摘要. 通过现有版本 API 保存五卡显式摘要, 重新登记与审查, 最终核对实际查询结果. 插件源码及安装配置未变更; 本轮使用的三个既有运行时文件见 [运行时绑定](../../research/artifacts/proof-audit-round7-20260921/plugin-runtime.json).

6. 协调器最初只为三张下游卡登记了直接错误事项, 漏掉上游 FH 事项传播而来的独立义务. 既有门禁正确返回 STILL_BLOCKED, 没有自动清除. [传播纠错记录](../../research/artifacts/proof-audit-round7-20260921/correction-propagation-finding.json)保留原因及当时状态; 用既有 API 补齐新修订、独立审查与释放, 卡片字节和插件源码均不为此改变.

工具库事务初期在 WSL 挂载盘反复核验历史文件, 耗时较长. 后续使用项目外私有 POSIX 兼容 Python, 保留相同绝对路径并执行三个原插件模块. 原数学回执的45个输入由未修改验证器重新校验且结果逐字段一致; 初次环境/锁冲突与一次写入前的正常中断也记录, 中断前后纠错日志原字节一致. 这不是更换数学或 Lean 的验收运行时, 也不声称操作系统沙箱隔离. 来源、模块哈希与切换检查见 [库事务运行记录](../../research/artifacts/proof-audit-round7-20260921/library-runtime/README.md).

## 保存与交付

基线 `636dac87c269795a520824101f1b2abd2c583c9b`. [保护核对](../../research/artifacts/proof-audit-round7-20260921/protection-result.json)覆盖原8336个跟踪路径、134个原未跟踪文件和6项既有脏文件; 除本轮明确活动文件外保持原字节, 不纳入无关工作. [发布清单](publication-manifest.json)逐文件绑定本次候选, 暂存与提交后再读取真实 Git blob 核对. 大型原始证据以无损 gzip、去重对象和完整原路径映射归档;派生索引不会替代完整原始证据. 私有工作区 AGENTS 不是执行依赖, 保留本地及哈希, 不公开其正文.

本报告属于提交前的验收内容, 不伪造提交后或推送后的自指哈希. 实际交付顺序为主仓库 origin/main 后 fork/main; 提交及两个远端头、最终工作树原状的核验保存在项目外 `F:/tools/math-audit-round7-20260921/DELIVERY.json`. 恢复中断时先查该文件及 live remote heads, 不重复已完成作者、改写冻结包或绕过精确版本释放.
