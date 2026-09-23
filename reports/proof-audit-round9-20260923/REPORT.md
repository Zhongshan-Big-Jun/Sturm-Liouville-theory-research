# 第九轮审计修订报告

日期: 2026-09-23. 基线: `2a81b608d53e3decee04c46716a8d8f8c2d9b1b4`.

四项报告发现及本轮独立复核追加发现均已修复. 数学修订、未变卡片续检、数值程序、Lean 盲读和独立编译/语义核查共五份最终隔离检验通过; 首次退回完整保留. 工具库已恢复78项可用、1项原有撤回. 本报告限定于下述修复, 不代表全项目证明认证.

用户提供 `C:/Users/HuangZY/Downloads/sl_audit_round9`, 要求继续修复, 并指定 math-research-workflow 2.0.1. 附件作为待核实证据. [原始十文件](../../research/artifacts/proof-audit-round9-20260923/submitted/)逐字节归档; 清单中九个工件哈希及十二个来源文件/Git blob 与基线一致, 见[接收记录](../../research/artifacts/proof-audit-round9-20260923/source-intake.json). 未将报告中的建议当成新的用户指令.

## 四项发现与实际修复

| 发现 | 核实结果 | 当前修复与适用范围 |
| --- | --- | --- |
| F01 不等宽块投影 | 对块平均 g_i=A_i/L_i 作普通欧氏投影不能保证 b·A=0. n=2,R=4 时, 以精确块积分代入旧投影公式, 真实一阶变分约为 −1.24684769078 | [活动程序](../../scripts/_gapn2_second_variation_probe.py)用真实块积分 A; 可选块宽加权度量. A=0 时保持原方向, 再以独立直接积分检查切向性. 不将正密度局部方向自动当作饱和盒约束可行方向 |
| F02 Green 对角发散 | 一维正则 Dirichlet 问题的去简单极点 Green 核连续有界. 原发散解释和据此声称的路线封闭不成立 | [解析修复 V3–V4](../../research/artifacts/proof-audit-round9-20260923/analytic-repair.md)证明有限核及集中极限. 移动界面仍有有限加速度项 −Σs_i d_i²f′(a_i), 对 Q 要除以二. 不据此解决 G1′ |
| F03 归一化导数缺核项 | h=rho 时准确导数为 −u/2, 普通约化逆特解却为零 | V1 用 Volterra 解析射击、简单根与加权归一化补齐核分量; 保留正确的 lambda′′ 谱公式. 区分普通 L2 约化逆与加权谱有限部分 |
| F04 物理世俗函数误称对称 | 物理 F 的频率 omega 随 y 变化, F(pi−y)=y/(pi−y) F(y) | [固定 n 文稿](../../docs/SL_fixed_n_supremum.tex)改为 Fhat=omega F 的严格反射对称, 物理根反射与根计数保留. 综述仅改 B3 三处相关表述 |

rho=1、单位质量脉冲集中到中点时, 完整无限谱的控制收敛给出 lambda1′′→6pi²、lambda2′′→0、Q=半谱隙二阶变分→−3pi². 这不是有限截断的推测. 一般带符号集中脉冲须同时满足总变差一致有界、支集集中和总质量趋于 q, 才能取得 q² 倍核点值的极限. 首轮独立审查发现工具卡漏写质量收敛; [修复说明](../../research/artifacts/proof-audit-round9-20260923/review-f1-repair.md)保存双子列反例. 原解析证明已包含该前提; 被退回的卡片版本和回执保留.

## 新补证与尚未解决的问题

对固定 R>1、整数 n>=1, 置 s=sqrt(R), delta=1/s. 规定平衡交替配置对应的 n 阶 Jacobi 矩阵首对角为 −delta、其余对角为零、副对角为1. 完整特征多项式和端点二次型给出全部 2n 个简单相位根. 主子矩阵嵌入与末行递推给出最小特征值 z_n 严格下降, 试探向量给出 −2<z_n≤−2+(2−delta)/n, 因而 z_n→−2.

由此 **规定平衡候选** c_n=((pi−y_n)/y_n)² 严格下降到 ((pi−phi)/phi)², phi=arccos((s−1)/(s+1)). [当前五页 PDF](../../docs/SL_fixed_n_supremum.pdf)含完整解析证明. 研究地图新增 B3-CANDIDATE-LIMIT; B3 总问题保持 PARTIAL. 等宽平衡候选是否达到完整容许族的全局最大, 以及真正上确界序列的同类性质, 仍属 O1/O2, 没有随候选谱计算完成.

旧 R206 记录和旧 B3 研究包不改写. 后续 B3 研究本来已经使用归一化函数, 其正确根计数不因早期文稿错误而一并撤回. `_gapn2_k_global_rank2.py` 仅修正说明, 不重新认证它的 K 实现或全局恒等式. 上轮 INF、M3、KP 及历史全局极大子结构证明均保留其原有范围.

## 程序执行与证据层次

附件 `checks.py` 的隔离副本在普通模式和 `-O` 下实际执行, 各20组确认, 见[附件重放](../../research/artifacts/proof-audit-round9-20260923/submitted-replay/). 协调器重放不等于独立数学认可.

软件作者在项目外修复后交付, 首轮候选源码 SHA256 为 `53c5ccd85c28f1a5a1e2e37a4eed4e8dc450025eaf313aae15df028eb1f9d31e`. [集成身份](../../research/artifacts/proof-audit-round9-20260923/software-integration.json)、[作者证据](../../research/artifacts/proof-audit-round9-20260923/software-author/REPORT.md)和[隔离复现方法](../../research/artifacts/proof-audit-round9-20260923/software-reproduction.md)分别记录. 当前程序保留 R=1 和原位置参数, 修复了首次候选过严的 R>1 限制; 该早期失败没有删除.

实际求积按密度和方向断点分段, 使用真实加权归一化及无权谱配对; 一阶变分另以高精度直接积分复算. 有限差分不截断或夹紧负密度, 而是拒绝不可行步长. P2b 原本使用积分约束, 不被误列为块平均错误的反例; P3 的有限宽脉冲与界面加速度分别记录.

作者普通/优化模式各6组回归含41项非法输入检查, 历史投影负对照实际返回非零, 新投影通过. 四个有限 CLI 案例为 n2R4SUP、n3R4SUP、n2R10SUP、n2R4INF. 使用精确块积分构造同类旧错误投影时约为 −1.24684769078; 独立执行历史网格积分原代码时约为 −1.24682507619, 差别来自旧离散积分. 新 n2R4 方向的直接一阶变分约为 −2.04e−15. 谱截止31/61/121/241、求积和差分步长检查均保留原输出: 过小的双精度步长有消减误差; INF 的一个小方向在61模态约0.501%相对误差, 241模态降至约0.00478%. 没有严格无限谱尾界, 没有将采样同号改称负定性定理. 作者数据须与下方新的独立执行结论分开使用.

## 独立检验与工具纠错

所有验收会话均以 `fork_context:false` 新建, 只提供冻结文件、明确的义务及精确哈希, 不继承作者对话. 作者本人不担任自己工件的验收者. 原生派发、实际完成回执及拒收保存于本轮证据与 `research/library/reviews/`.

首次数学审查对归一化、真实切向、有限核解析证明和 B3 候选证明均给出明确肯定, 但因卡片遗漏质量收敛返回 CHANGES_REQUIRED. 二阶变分卡已生成新的精确版本并通过另一独立会话的再次审查; 首次混合结果不作为整体通过凭据.

综述整文件哈希变化使十二张数学内容未变的旧卡的22项旧释放回执失效. 新的无状态审查检查126个输入、112项未变绑定、三处 B3 差异及22项修订义务, 确认左定/INF 原证明不依赖改动的 B3 段落. 其有限精确算术复验重现19组结果并拒绝14个负对照; 未称历史全部测试或 Lean 都重跑. 同版本续发须通过原纠错模块逐事项处理, 不覆盖旧回执或改写未变卡.

第二次数学审查由另一新会话完成, 32个冻结输入、9项义务均 APPROVED; 包括集中质量条件、双子列反例、两份当前文稿和三张卡的摘要/依赖. 首次退回不覆盖也不充当最终认可.

首轮软件独立审查重现四组默认输出、普通/-O回归、敏感性数据, 另外检查72组高精度投影、独立自适应归一化/配对、傅里叶恒等式和界面形状项. 它返回 CHANGES_REQUIRED: 正的极小脉冲半宽1e−20会在浮点坐标中完全塌缩, 1e−16也有部分质量损失. 原程序仍退出0并打印错误零贡献. [真实执行归档](../../research/artifacts/proof-audit-round9-20260923/software-review1/)保留该发现.

协调器据此新增支持宽度/实际求积节点的分辨率检查, 不能分辨时明确拒绝; 数值阈值不是严格求积误差证书. 新作者回归普通/-O各7组通过, 两个极小宽度CLI均返回2而不打印P3贡献. 四组默认数据与日志逐项不变.

第二次软件审查由新的无状态会话完成, 40个冻结输入、3项义务均 APPROVED. 实际复跑普通/-O回归、32组高精度投影、独立积分/傅里叶检查及求积、谱截止和差分敏感性; 四次极小宽度 CLI 均退出2且标准输出为空, 高阶求积节点塌缩也被拒绝. 默认脉冲质量误差小于1.2e−13. 保留[108文件真实执行归档](../../research/artifacts/proof-audit-round9-20260923/software-review2/execution-archive.json). 这次运行使用 Python3.14.4、NumPy2.5.2、SciPy1.18.1、mpmath1.3.0; 未证明其他平台或任意参数下的数值误差界. 未使用的 analytic_jacobian/term_breakdown 依赖未提供的历史模块, 不在此次执行认证范围内.

最终活动程序 SHA256 为 `f846705159ed2ec559a368ab65eddeb8184b7d62b1cbd553e368868374c5a3ab`. 先接收旧版本的真实退回回执, 再接入这一精确获批版本; [当前项目位置的实际 CLI 重放](../../research/artifacts/proof-audit-round9-20260923/software-final-integration.json)退出0, 数值负载与获批候选一致. 最终工具放行和 Lean 独立执行结果另见下文, 不从软件通过推断数学全局结论.

## 最终回执与当前检索

| 独立义务 | 实际结论 | 原始结构化报告 |
| --- | --- | --- |
| 数学首次退回 | CHANGES_REQUIRED | [01a0cbfa](../../research/library/reviews/runs/4c03e92e23cd550ef387a9e6eceb12d193ec68f426adaf9c3a1e6ef928f556dc-01a0cbfa-7e78-7b03-8255-4ee3c7a10834/report.json) |
| 数学修订最终复核 | APPROVED | [01a0cc08](../../research/library/reviews/runs/a8535d90fa5816b56bc3cef9a9d090b0134e0d85a768ea1b0284056fa91a3689-01a0cc08-556e-7cd0-bb4b-751a35d9c749/report.json) |
| 12张未变卡续检 | APPROVED | [01a0cbf6](../../research/library/reviews/runs/23baba3b81aa31cf7beda511ee13bf8115c1468c30bb869cc9ffe764ba5ebe3c-01a0cbf6-e557-7031-9a4d-c72ceefb48ec/report.json) |
| 数值程序首次退回 | CHANGES_REQUIRED | [01a0cc01](../../research/library/reviews/runs/d87ca0b49d112b45e235724cbfe9790a5584af9546f0065410a74188bb8210f2-01a0cc01-fdb9-7b52-92f0-36d95f648e01/report.json) |
| 数值程序最终复核 | APPROVED | [01a0cc18](../../research/artifacts/proof-audit-round9-20260923/software-review2/research/library/reviews/runs/e8853bf3b24cb634e2bec6d557e3f6c7bbe374d50d7ac9a5101aea00a8a2381f-01a0cc18-b9bd-76a1-8479-754f0bcc2174/report.json) |
| 形式声明盲读 | APPROVED | [01a0cc16](../../research/artifacts/proof-audit-round9-20260923/formal-review/research/library/reviews/runs/bbe6410e6e958d392918fd8c023ae49c7e796ca361449684b91ed1e52359e61d-01a0cc16-7a4f-74a0-b80b-2413e676193e/report.json) |
| 独立编译与语义核查 | APPROVED | [01a0cc20](../../research/artifacts/proof-audit-round9-20260923/formal-review/research/library/reviews/runs/0480ca86b1aa481aaf4477e9864fbe3520f4470556eced893d9006da14800f6b-01a0cc20-968f-7f91-b030-1f216c592dcc/report.json) |

三个修订版本已由原纠错模块逐项 RELEASED; 十二张未改数学内容的卡片完成22项同版本续发. [实际工具检索](../../research/artifacts/proof-audit-round9-20260923/current-tool-query.json)及[最终门禁核对](../../research/artifacts/proof-audit-round9-20260923/library-final-check.json)确认78可用、1项原有撤回, 并逐一核对15张当前卡的内容哈希、摘要、依赖和来源状态. 三张修订卡各有版本绑定研究注释.

保留57条历史 REVIEW_NO_LONGER_VALID 警告: 40条对应已重新审查的同一当前版本, 17条对应被替代版本. 这些历史警告不能当作当前复用授权, 也不能为让页面显得干净而删除. 当前复用由新回执决定.

独立检验回执的原生工具来源强度为 COORDINATOR_ATTESTED_TOOL_TRANSCRIPT. 分别归档实际派发、真实完成内容与插件接收结果; 不将其夸大为外部签名的数学证书. 软件最终复核和形式化复核使用本轮证据下各自的隔离审查项目; 主工具库的修订/续发保持单一写入者. [协调执行证据](../../research/artifacts/proof-audit-round9-20260923/coordinator/manifest.json)记录真实操作、早期失败和队列调整.

## 局部形式化的实际范围

新增 [AuditRound9.lean](../../lean-proof/SL/AuditRound9.lean), 源码 SHA256 `0668291e3ac37f2608483b009e4b5726fc9cd3deeb89849e0da8cc8c60ebd208`. 文件含25个具名定理、13个定义/缩写, 验收根为15项合取; 实际导出含辅助项共59声明. [作者合同与机器记录](../../research/artifacts/proof-audit-round9-20260923/lean-author/)保存 Lean4.31.0 Windows PE、Mathlib固定提交、精确根类型、完整定义/依赖闭包和三类负对照. 原始329文件压缩归档并逐字节验证, 没有丢弃失败执行.

新的盲读 agent 已核对四个冻结输入和全部59声明, 返回 APPROVED. 它只从实际形式声明回译所有量词、类型实例、非零前提、全定义除法、零维/零法向量和矩阵乘法次序, 没有借此声称编译或语义认证. 另一新 agent 在新目录亲自执行固定编译器和三个错误目标控制, 对照非形式合同及盲读结果后返回 APPROVED. [独立执行归档](../../research/artifacts/proof-audit-round9-20260923/formal-review/execution-archive.json)保存实际运行证据; 源码、类型/定义导出、根身份、传递公理和环境绑定分别核对, 不以作者机器报告替代独立执行.

独立正对照退出0; 错误归一化符号、缺失目标、额外 H:Prop/pending:H 前提分别退出1并留有具体拒收原因. 遍历16629个依赖声明后, 根只依赖 propext、Classical.choice、Quot.sound, 未出现 sorryAx、额外公理、unsafe 或未知依赖. 12505个绑定文件的执行前后内容与元数据一致, 其中12480个为导入工件. 35条实际编译器/运行时命令、8条包装器记录及全部265个输出逐字节归档; 未复用作者根对象, 也未声称重建全部依赖或使用第二套证明内核.

形式化覆盖有限实向量欧氏投影、线性归一化核修正、真实2×2矩阵的任意n反射和物理频率因子. 不覆盖可选宽度加权投影的形式证明, 不覆盖块积分的解析识别、本征函数可微性、无穷谱展开/约化逆/Green核、ODE来源、2n根计数、候选极限和全局极值. 这些结论不能因局部代数编译成功而被称为全部形式化.

作者早期编译及首次 positive 检查失败保留. 首次额外前提负对照的外层退出143, 原因未确认, 没有把它计为通过; 后续持久任务重新执行并在目标类型不匹配处正确拒收. 持久任务对预期的 strict-exit=1 记为 FAILED, 该状态与负对照达到预期属于不同层次.

## 阅读产物与保护范围

两份 PDF 已实际重建: 固定 n 文稿5页、综述20页. 固定 n 全5页及综述改动的11、12、17页均作图像版面检查. 综述的一个 overfull hbox 来自未改动的旧谱隙证明链文字, 不属于新增公式错误. 见[构建记录](../../research/artifacts/proof-audit-round9-20260923/pdf-build/)及[版面检查](../../research/artifacts/proof-audit-round9-20260923/pdf-inspection.json).

研究地图、项目理解、双语首页、研究/脚本导航、工具指针表、Lean 状态、AGENTS 和续接记录已随当前数学范围更新. 此次从错误路线提炼了投影度量与约束泛函的区别、规范变化的核分量、零集与函数值不变量的区别以及有限核路线的重新检验条件. 后续研究想法明确标为待证.

基线记录12666个原跟踪文件、134个原未跟踪文件、6项既有脏文件. 旧研究证据、旧 Lean 源、canonical 和无关工作按基线保护. Blueprint gateway 的实际 ensure 为 ALREADY_READY, 本轮没有 canonical 接收或全库重建, 没有修改插件源码/安装缓存或全局代理与环境. 交付使用精确路径清单与实际 Git blob 字节核对, 主仓库 origin 先推送, fork 后推送; [发布清单](publication-manifest.json)绑定本次全部文件. 提交后的实际双远端 HEAD 与原工作树恢复核对保存在外部工作目录 F:/tools/math-audit-round9-20260923/DELIVERY.json, 不在提交前预写推送成功或自引用提交哈希.
