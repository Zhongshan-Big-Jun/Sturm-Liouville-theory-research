# 第三轮证明审计修缮报告

日期: 2026-09-20. 输入: 用户提供的 `proof_audit_round3_20260920.md`, SHA-256 `a5fa0e1ba64627c9d1b04e46e1add3e013b0ab94bf9a93b0b9e2623e192cb548`. 用户要求核实、修复并推送云端. 报告的建议作为待核查材料, 没有替代实际验证.

三项主要发现均已核实并修复. 一般递推保留充分性和实际解判据, 撤回错误的增长分类与无条件基扰动结论. 商空间的完备性结论保留, 证明改为谱截断. 本轮还修正五个活动程序、两张工具卡及直接状态指针. 这不是全仓库数学认证.

[原始报告](../../research/artifacts/proof-audit-round3-20260920/submitted-audit.md) | [修订前原字节](../../research/artifacts/proof-audit-round3-20260920/before/) | [当前证据清单](MANIFEST.json) | [Lean 范围](../../lean-proof/STATUS.md)

## 1. 核实结果与修复

| 发现 | 核实依据 | 当前修复 |
| --- | --- | --- |
| R3-F1: 一般递推下界误作等式及完整分类 | c0=1,A=3,B=2 时 eps=0,S=0, 实际解却为 2^m-1. A=3+2/m,B=2 时 u2=4, 乘积模型仅为2 | 保留含 B/c0*(u_prev-u_prevprev) 的精确分解; 一般情形只给乘积下界. 以实际偶、奇基本解的两个级数给出对角空间充要判据. C/k 与 C/(k log k) 的显式分类明确限定 B=Bprime=0; Gamma 分母修为 Gamma(2+C) |
| R3-F2: 基扰动漏掉 B 的变化, 无条件稳健性错误 | c=3,m=4,delta=1 时 A=63,B=70, 差=-7, 旧式为23. P2=(3x²-1)/2 给出整个形式像族的非零正交元 | 同时计算两个系数并核对真正算子域. 构造有界且趋零的扰动反例. 加入对所有 m>=2、两侧均有 \|delta\|<=1/(8m) 的充分条件; 不将最终成立改写为全指标成立 |
| R3-F3: 商映射下使用了错误的函数像, 遗漏仿射模态 | h=x 满足旧证明所列正交条件但范数非零; 它与真实 T[cos(pi*x)] 的配对为 -2 | 写出 T[cos(n*pi*x)]=-n*pi*sin(n*pi*x), T[sin(mu*x)]=mu*cos(mu*x)-sin(mu). 固定 c>0, 在 D(Kc^(1/2))=H1 的形式范数中谱截断, 再用商范数受其控制得到稠密性; 1,x 的商类均为零 |

矩跳跃的当前证明与 PDF: [TeX](../../docs/SL_stability_moment_jump.tex), [PDF](../../docs/SL_stability_moment_jump.pdf). 商空间的当前证明与 PDF: [TeX](../../docs/SL_krein_c0_limit.tex), [PDF](../../docs/SL_krein_c0_limit.pdf).

扰动反例具体为

```
delta_m = 6m(2m+5)/((m-1)(2m+3)(4m²-6m-7)), m>=2.
delta_2=-36/7, delta_3=1, delta_m ~ 3/(2m²).
```

保留原奇侧, 偶侧令 alpha_m=m/(m-1)+delta_m. 则 P2 与 q0=3,q1=3x 及所有形式像正交, 且 ||P2||²=2/5. 前缀 alpha2=-22/7 导致 B2<0, 所以它不反驳正确的全指标增长定理. 非零基扰动一般也不满足 Krein 边界条件; “形式微分像”与“真正算子作用”在文稿和工具卡中分别说明.

沿域条件追踪时, 还修正 `krein-sobolev-polynomials` 中一阶边界误写为二阶导数、H2 完备性仍标开放、以及算子传输被误称为全阶多项式系的残留. 该卡其它既有文献摘要未在本轮重新审计. `constrained-denseness-runs` 只引用正确的条件增长引理, 不依赖此次撤回的分类或扰动断言, 保留原字节.

## 2. 程序与检验退回

五个活动程序已修复: `d3_stability_verify.py`, `d3_stability_verify2.py`, `op12_dichotomy_verify.py`, `op12_threshold_verify.py`, `op12_sparse_check.py`. 修正包括 c0 归一化、实际扰动系数、巨大有理数的对数、u0=0、起始指标2、Gamma(2+C)、实际 log(k), 以及真正的 2^(2^j) 跳点. 有限部分和只作诊断; C=2,beta=2.4 的无穷级数实际发散.

第一次程序独立检验返回 **CHANGES_REQUIRED**. 旧的局部16-ulp防护没有计入前步相减误差:

- A2=1,A3=22,A4=1; B2=0,B3=21,B4=1, c0=1. 精确序列为 0,1,1,1,0, 旧实现却返回有限 log(u4).
- A2=1,A3=3,A4=1; B2=0,B3=3071/1024,B4=1/1024+2^(-54). 所有系数可用二进制浮点精确表示, 但旧实现把精确负值判成正值.

最终实现对所提供的系数作精确 Fraction 转换, 递推真实比值 r2=A2/c0、r_m=(A_m-B_m/r_(m-1))/c0, 用精确符号判断决定是否继续. 浮点仅用于输出近似对数. 这不会恢复系数输入前已丢失的精度, 也不是区间证书; 精确分母可能随下标增大. 原错误回执与第一版证据保留, 新修订交由另一全新会话检验.

[第一版程序证据](../../research/artifacts/proof-audit-round3-20260920/script-checks/) | [最终程序证据](../../research/artifacts/proof-audit-round3-20260920/script-checks-revision2/)

## 3. 验证证据与实际边界

| 层次 | 实际结果 | 不包含的结论 |
| --- | --- | --- |
| 协调器精确检查 | 53 项符号恒等式、有理函数极限及有限精确交叉检查通过. 数学检验 agent 重放其中51项, 另两项商空间检查属另一包 | 有限样本不证明无穷维完备性; 通用结论使用解析证明 |
| 商空间作者检查 | 18 项精确积分/复数形式检查通过. 独立检验环境缺少 SymPy, 因而没有重跑该原脚本; 它另以标准库精确有理数检验64个实/虚单项式有序对, 并核对解析证明 | 不把替代核查说成同一个18项脚本的重跑; 不认证后文单位归一化草图 |
| 最终程序 | 五个实际程序退出0; 17项行为测试和5项原始回归通过. 包括1,000个首步精确零例、两个检验发现的多步反例、27个构造的多步比值例以及10个注入失败的非零退出 | 不从浮点曲线或部分和推断一般增长与级数敛散 |
| 局部 Lean | 24 个定理、10 个定义, Lean 4.31.0 原生编译通过. 协调器在新目录中重放, 根对象、实际声明及定义导出逐字节一致. 两个旧公式负对照均退出1 | 没有形式化 P2 的积分识别、完整完备性、谱截断、Gamma 渐近或全指标小扰动界; 没有重建历史全库和依赖二进制 |
| 声明与公理 | 实际导出34个目标, 检查其8032个依赖节点; 无缺失或 unsafe 常量, 传递公理限于 propext/Classical.choice/Quot.sound. 盲回译和语义对照由不同新会话完成 | 语义认可不代替编译, 基础库与本地编译器仍是信任边界 |
| PDF | 3份重建并解析: 6页稳定性、5页退化极限、20页综述. 修订证明页已查看. 前两份零警告; 综述有一处第三阶递推段的 Underfull hbox, 无缺字、溢出或未解析引用 | 文档编译不证明数学正确 |

原外部报告提到的 `check_round3.py` 与其结果文件没有随附件提供, 本轮没有运行或复述其“34项检查”为自己的执行结果.

[本轮 Lean 源码](../../lean-proof/SL/AuditRound3.lean) | [局部目标契约](../../research/artifacts/proof-audit-round3-20260920/lean/contract.md) | [机器重放](../../research/artifacts/proof-audit-round3-20260920/lean/replay/RESULT.json)

## 4. 独立复核

每次验收均使用新的原生子 agent, 显式 `fork_context:false`, 只提供冻结文件包及限定目标, 不继承作者对话. 真实 spawn、完成回复、输入哈希和回执保存于库内. 下表为具体范围的验收, 不是全文件或全项目认证.

| 范围 | 新检验 agent | 结果 | 原始回复 |
| --- | --- | --- | --- |
| 递推、扰动及两卡纠错 | `01a0bf18-56b8-7cc3-b51f-62357be1766c` | APPROVED | [回执](../../research/library/reviews/runs/2e50083373a4e569456525fa8c05ac809f3383dfcd7adff26cb7b721cefcfd58-01a0bf18-56b8-7cc3-b51f-62357be1766c/report.json) |
| 商空间证明与证据范围 | `01a0bf15-13ae-7f40-9308-47dafe86c6c7` | APPROVED | [回执](../../research/library/reviews/runs/10e4db313f0b3f150291b7d747cbcb538c5ef450cb80234a15c3f6cbb6e6d1e5-01a0bf15-13ae-7f40-9308-47dafe86c6c7/report.json) |
| 程序第一次检验 | `01a0bf15-2470-7c21-bb16-e679aa45bee9` | CHANGES_REQUIRED | [回执](../../research/library/reviews/runs/02089f63240fab3a512269599ddd21eeb381d994e8c95c075d73128032a5cf59-01a0bf15-2470-7c21-bb16-e679aa45bee9/report.json) |
| 程序修订后的全新检验 | `01a0bf21-38f7-7832-8124-2b03830827e3` | APPROVED | [回执](../../research/library/reviews/runs/d98e7b19c097b6a4e8a8de74ddaa2550532a92c24bbd68d3683ab7bcde1f2dec-01a0bf21-38f7-7832-8124-2b03830827e3/report.json) |
| 34项形式声明盲回译 | `01a0bf17-6866-78b3-8e7b-ce6056975a29` | APPROVED | [回执](../../research/library/reviews/runs/d78ce34c974ce004c8335e4a6bb8e561be0ccfc64c821fd6286c2536e0a7be2a-01a0bf17-6866-78b3-8e7b-ce6056975a29/report.json) |
| 形式化首次语义与证据检验 | `01a0bf21-40c9-7d63-bd60-8b9b983ff165` | INCOMPLETE | [回执](../../research/library/reviews/runs/1e7bbef38036354f9c5459401622a1bbfb221eeb4c9d3a82738d7b0b3ca794f1-01a0bf21-40c9-7d63-bd60-8b9b983ff165/report.json) |
| 补齐证据后的全新检验 | `01a0bf30-1fc6-7203-8400-dd74ee483944` | APPROVED | [回执](../../research/library/reviews/runs/963d4c4f1fc49e72de71f1ce0cd5917182c79eb0a18c150925cd50a511de6b8b-01a0bf30-1fc6-7203-8400-dd74ee483944/report.json) |

形式化首次语义对照已认可声明与契约一致, 但因检验包漏附负对照源码、执行记录及独立声明导出的调用记录而返回 INCOMPLETE. 补充冻结源码及真实日志后, 又在新输出位置执行了带根编译对象前后哈希的声明导出、导入路径解析及两项负对照, 并另启新会话检验. 没有把“报告了失败”当作已经证明该负对照实际运行.

回执的信任类型是 `COORDINATOR_ATTESTED_TOOL_TRANSCRIPT`. 它证明协调器保存了相应原生调用与内容绑定, 不声称具有操作系统隔离或外部密码学身份认证. 原生回执的调度路径仍指向本机工作区; 迁移时应核对冻结文件, 不能直接改写回执路径与哈希.

## 5. 工具库纠错与长期研究记忆

两个问题先登记并隔离旧版本, 再保存新卡、提出版本修订并经上述数学复核释放. 默认查询已实际核对, 两张新卡可检索, 错误旧版本保留为历史, 不作为默认复用内容. 已撤回的 `left-definite-orthogonal-systems` 继续隔离.

当前指针表: 78张可用、1张隔离; 94个历史版本、30条纠错事件, 既有有效释放无校验问题.

新增一条绑定当前稳定性卡版本的候选经验批注: 下界与增长分类不同、扰动要同时计算两个系数、有限前缀与算子域不能略去. 批注帮助检索和继续研究, 不是 canonical 接收. 本轮未改 Blueprint canonical.

[稳定性卡](../../tools/jump-stability.md) | [Krein-Sobolev 卡](../../tools/krein-sobolev-polynomials.md) | [指针表](../../tools/README.md) | [当前纠错与查询](library-state.json)

## 6. 保存、续接与发布范围

基线提交为 `aac44f5a5831d9c4b7140027a09a06e8af4250f5`. 提交前保护检查覆盖5149个原跟踪文件和134个原未跟踪文件. 修订前证明/PDF、两卡和五个原程序按原字节归档. 旧封存审计、canonical、未分配研究草稿及其哈希绑定内容保持原样; 43个既有 SL 源文件未改. 旧 `_patch_stability12*.py` 含已撤回陈述, 已在脚本导航明确列为历史文本补丁, 仅保留溯源, 不是活动验证或更新入口.

本次精确暂存本轮改动与必要证据, 不使用 `git add -A`. 使用已授权的顺序推送成果主仓库, 再同步其 fork. 实际远端提交核对由本次交付记录和最终回复给出; 本报告中的数学验证不依赖推送是否成功. 插件源码本轮没有修改, 使用的是已同步的2.0.1纠错与检验工具, 不将本轮数学修缮冒称插件新版本发布.

原稀疏族在 3<s<7/2 的稠密性、一般非对角矩可表示性、变系数推广及商空间文稿后文单位归一化的完整证明, 均不因本轮修缮而自动闭合. 续接入口已更新于 `state/RESUME.md`, 具体对话与方法已记入 `state/AGENTS_SESSION_LOG.md`.
