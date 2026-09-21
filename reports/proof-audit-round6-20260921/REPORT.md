# 第六轮审计修缮报告

当前状态: 三项审计发现已修复, 原完整稀疏族的非负分数阶窗口已补证. 两份解析证明、九卡传播及局部Lean分别完成独立验收. 本文件记录提交前已验收的候选; 实际提交与双远端HEAD核验写入项目外交付回执, 不在提交内预称推送成功.

用户提供 `C:/Users/HuangZY/Downloads/sl_audit_round6`, 要求使用 math-research-workflow 继续修复. 本轮以 `92d46e99e36cc0a74e8f7bb13430749c222ee54f` 为基线. 十份附件按原字节保存在[输入目录](../../research/artifacts/proof-audit-round6-20260921/submitted/), 其中九份清单哈希均匹配. 八份被引用源码已与本地实际 Git blob 比对, 不再只依赖外部连接器给出的身份. [输入核验](../../research/artifacts/proof-audit-round6-20260921/intake.json).

附件中的修复建议与补证均按待核查数学材料处理. 本轮不重审全部历史研究、不写 canonical、不编辑插件源码或安装配置; 先保存全部7510个跟踪文件和134个原未跟踪文件的哈希, 原六项未提交变更单独保护.

## 已核实的问题与准确修复

| 项目 | 原问题 | 当前替代 |
| --- | --- | --- |
| R6-F01 | 把稀疏族的代数包当作全部多项式, 从而过强地断言投影族稠密及“只检验排除项” | 补入投影的 x²,x³, 或另证 V intersect M^perp={0}; 整个原空间的稀疏总性只是充分特例 |
| R6-F02 | F 要求有限矩测试在含完整无限尾部的 V 上单射, 前提彼此不相容; G 沿用该含混条件 | 有限测试只作用于真正的有限维尾部正交障碍; 另给一般三角尾部的完整判据 |
| R6-F03 | 一个表示元同时检测到两个矩, 被误解释成分别把两个矩钉零 | 必须有 span{x²,x³} 包含在全部约束表示元的线性包中 |
| R6-C01 | 附件提出补齐此前未判定的3<s<7/2 | 逐一核查两支全指标成员阈值, 再通过四迹多项式图核心和谱截断证明密度 |

完整投影/矩修复见[证明源码](../../docs/SL_projection_moment_repairs.tex)及[PDF](../../docs/SL_projection_moment_repairs.pdf).

在所有多项式均稠密地包含于复 Hilbert 空间 H 的契约下, 令 M=closure span{p_n}. 正确投影条件为 `closure span{P_V p_n}=V iff V intersect M^perp={0}`. 一般恒等式是 `Pi=span({p_n} union {x²,x³})`, 原稀疏包在Pi中余维2. 正交投影连续满射把整个稠密多项式空间投到V内稠密的正确结论仍然保留.

反例使用对角系数空间 H_beta, beta=2, `V=ker M0`. 非零向量 `w=sum_(m>=1) m/(2m+1)^4*x^(2m)` 的平方范数为收敛正级数, 满足M_(2m)=m、M0=0和全部奇矩为零. 它属于V并正交于全部投影p_n; 唯一排除项p0的投影却为0. 这是实际 Hilbert 向量, 不只是未验证可表示性的形式矩序列. beta=2不表示第二左定空间.

F 的问题须准确称为“无适用实例”, 不能说已找到满足它全部前提但结论错误的反例. r个低测试加两个矩构成到C^(r+2)的线性映射, 任取r+3个不同次数的保留尾部多项式就给出非零核. 修复在beta<1范数增长假设下令L=2m0-2, 证明尾部正交补恰为 `Z_L={w:M_k(w)=0 for all k>=L}`, 维数至多L. 真正需检查的是V与Z_L之交上的低测试核. 一般全次数三角尾部q_n (n>=N且首系数非零) 的障碍维数至多N, 同样有必要充分的有限测试. 这不声称任意H的矩可表示性已自动可计算.

F03用H_0中的v=x²+x³和w=x²-x³说明: v同时与x²,x³非正交, 但w属于v的正交补, 两个矩为1,-1. 一个线性关系与两个分别为零的条件不同. 原正交补主判据、独立具体Krein低阶证明及第五轮s=2两迹证明没有被这些反例推翻. 原A-E其它分类保留其历史范围, 不再以整组A-H STRICT冒充本轮复审.

## 分数阶窗口与新的研究理解

在每个固定实c>0下, 对指定的自伴Krein算子Kc, 定义复空间Hc^s=D(Kc^(s/2)), 范数为||Kc^(s/2)f||2, s>=0. [完整证明](../../docs/SL_fractional_left_definite.tex)与[11页PDF](../../docs/SL_fractional_left_definite.pdf)证明: 原完整命名族在全部0<=s<7/2稠密. 每个非仿射命名成员当且仅当s<7/2时属于该空间, 仿射成员1,x则属于全部非负幂域. 因而s>=7/2的原完整命名族不能作为该空间内的稠密族. 该结论经过新的隔离数学审查, 没有扩大到删除分类或任意闭子空间.

两支谱系数必须分别证明: 普通多项式为O(k^-2), 满足第一层Krein边界条件后为O(k^-4). 全指标的非零下一层残差分别是4m(4m-5)和4m(4m-3), 给出端点7/2的调和级数发散. 正弦模态使用正确范数, 两个仿射低模态完整保留.

密度证明另有关键结构: 令T取f及f''的四个边界残差. 它在x²,x³,x4,x5上的矩阵行列式为15360, 存在固定有界多项式右逆R. 用四次积分构造普通H4多项式逼近r_j后, `r_j-RT r_j` 满足全部四条迹, 从而在Kc²图范数中逼近. 再作谱截断和连续嵌入, 传到目标非负窗. 这不是从H3直接向高阶传递稠密性.

“逐个选取域内命名成员”和“先有限相加再检验域”不同. 例如p4、p6分别不属于Hc4, 但 `p6-(7/2)p4=x6-5x4+7x²` 属于D(Kc²). 第一种筛选在s>=7/2只剩1,x; 第二种能利用残差抵消形成稠密图核心. 这一差别是可继续复用的研究信息, 并不恢复旧的全阶命名族断言.

第五轮余有限删除分类仍限于s=2. 一般非对角O1'/O1'LD、其它阶的删除分类、Riesz/Schauder基、参数c一致的估计及完整分数阶域边界分类不由本轮结论给出. 旧H3证明、研究总结和稳定性稿中的当时“尚未判定”记录, 现按本轮分数阶证明更新状态; 其封存证据及原证明主体不改写.

## 检查、形式化与独立验收

原附件检查脚本已在隔离副本中以普通Python和`-O`分别重放, 两次均确认全部21组, 退出0. [普通重放](../../research/artifacts/proof-audit-round6-20260921/submitted-replay/normal/execution.json), [优化模式重放](../../research/artifacts/proof-audit-round6-20260921/submitted-replay/optimized/execution.json). 组数包含确认反例、有限样本和符号恒等式, 不等于21项无限维定理被机器证明. 原脚本关于外部审计环境的局限文字保持原样, 本轮本地源码身份核验另见intake.

投影作者的16组检查及分数窗作者的55项检查完成. 后者区分39项精确代数/符号检查和16项静态/身份检查; 这些数字不表示无限维定理的机器证明数量. 分数窗首个检查因协调器同时更新准则文档的三句范围说明而在第53项失败. 已核实所引代数段落原字节不变, 修正身份检查的归属范围后重跑通过, 原失败记录保留. [投影作者范围](../../research/artifacts/proof-audit-round6-20260921/projection-author/AUTHOR_NOTES.md), [分数窗作者范围](../../research/artifacts/proof-audit-round6-20260921/fractional-author/AUTHOR_NOTES.md).

四份PDF已实际构建. 新投影证明12页、分数阶证明11页及准则文档6页全部渲染检查; 20页综述检查了第13-20页, 含本轮改动. 全部49页另作文字/边界结构检查. 投影稿首次构建缺mathtools, 使用本机既有TeX Live2024的包后成功, 未修改冻结源码或安装新包. 三处路径引用的underfull提示保留, 未发现溢出版面、缺字或未定义引用. [实际版面范围与PDF哈希](../../research/artifacts/proof-audit-round6-20260921/pdf-checks/visual-check.json).

新增[AuditRound6.lean](../../lean-proof/SL/AuditRound6.lean), SHA256 `f765205b55ee454261a1a365e157ffa4f4f0202662c450b8a9c92328820a7c3e`. 导出36个公共声明, 其中21个定理. 精确根为`SL.AuditRound6.local_algebra_root`, 覆盖真实实多项式上的全指标补x²,x³张成、稀疏包缺x²、四迹线性映射/矩阵/行列式15360/两侧逆、任意多项式迹修正、p6-(7/2)p4的残差抵消, 及真正二维内积空间中的检测反例. 不用假设所求结论的布尔包装代替证明.

维护版验证器在Windows PE Lean4.31.0中实际执行, 通过WSL调用. 旧AuditRound5源从原字节重新编译到本次输出, 排除旧项目对象. 作者精确正目标和编译正对照通过; 故意设置的错误期望类型真实得到target_mismatch. 传递公理只允许propext、Classical.choice、Quot.sound. 作者首个尝试退出143且未形成完整回执, 原因未确认, 保留中断证据; 后续完整尝试单独记录. 另一无状态执行者在新目录亲自重编译并完成25项执行/结构检查, 核对正目标、公理和对象身份; 它没有再次执行作者的错误期望类型负对照. 再由盲读会话回译实际类型/可达定义, 最后交给不同会话比较契约、解析语义与全部证据. 原始机器回执的semantic.status保持not_reviewed, 本轮独立语义批准由下表单独绑定的审查回执给出. [作者执行记录](../../research/artifacts/proof-audit-round6-20260921/lean-author/REPORT.md), [独立执行报告](../../research/artifacts/proof-audit-round6-20260921/independent-execution/REPORT.md).

明确没有形式化复Hilbert/Sobolev空间、投影正交补恒等式、尾部障碍维数引理、加权无穷级数反例、四迹的Sobolev连续性、图核心、谱系数渐近、7/2阈值或无限维稠密性; 也没有宣称稀疏包与整个多项式Krein核的等式已在Lean根中建立. 代数零迹不能自行升级为无界算子域成员性. 未重建完整Lake工程. 大型原始回执和导出采用无损gzip并附原始字节哈希与映射, 可读索引只作导航, 不替代原始机器证据.

最终审稿会话均另起fork_context:false, 与作者分开; 调度和完成对象保留. 首次盲读因读取了项目记忆及包外流程技能, 隔离条件未满足而记INCOMPLETE; 不用其逐项结论放行. 重新隔离盲读的批准另列. 范围批准不等于全仓数学认证.

| 审查 | 结果 | 原始回执 |
| --- | --- | --- |
| 投影卡首轮 | CHANGES_REQUIRED | [报告](../../research/library/reviews/runs/d9b6e034ae2da775210fe8fc63d7547d4ea4af670953f7d73f4f5fb62b8cbd6f-01a0c2e7-7571-7021-9efe-f1758f7dc25c/report.json) |
| 投影/矩证明及修正卡 | APPROVED | [报告](../../research/library/reviews/runs/8745105609c2c6510214f605cf3be515b8692db5d4eb55e3e89c6a0261c97fe5-01a0c312-aeca-7663-9688-989cb1ba3aa1/report.json) |
| 分数窗与18项继承/新纠错义务 | APPROVED | [报告](../../research/library/reviews/runs/6cfa44fcc5affefbd1d2e98ff03210c8b0e0660bbf3ce0029f9c000d53ad5b1f-01a0c30f-4d13-7e60-9aca-1e305297d663/report.json) |
| 首次盲读隔离不完整 | INCOMPLETE | [报告](../../research/library/reviews/runs/c1987508542ce8e956138cf733ddf84e82517f204d31743fda4b986ee2566e1d-01a0c30f-e373-7873-af86-eeb258d713e1/report.json) |
| 重新隔离的形式声明盲读 | APPROVED | [报告](../../research/library/reviews/runs/c1987508542ce8e956138cf733ddf84e82517f204d31743fda4b986ee2566e1d-01a0c31a-a4ab-7fe3-b440-73bfcfbf178a/report.json) |
| 形式语义与执行证据 | APPROVED | [报告](../../research/library/reviews/runs/6c4399798a03768a4598bc4ea83f1287ab58e0af843644d2a80c0ab097a9787f-01a0c32a-6c37-77b1-82bc-f0fed908b511/report.json) |

首轮投影审查准确发现协调器工具卡中的量词错误: 把M=H写成省去补充测试的必要条件. 完整新TeX已正确使用较弱的V intersect M^perp={0}. 卡片修正后新增版本和纠错义务, 交给另一个全新会话复检通过. 原CHANGES_REQUIRED包按原字节保留, 其旧卡绑定已经过时, 不能被当作当前卡的复用批准. 此次并非重新把独立作者的正确证明判错.

## 工具库纠错、证据保护与交付

外部问题注册为round6-projection-moments; 新分数窗及版本传播复核注册为round6-fractional-window. 九张相关当前卡先隔离, 原版本和自由批注保留. 继承的round2至round5纠错义务需要随新版本明确复核, 编辑文本或重建索引不能自行放行. 当前证明以精确哈希绑定源和依赖; 旧run、旧PASS和旧回执按原字节保存.

九张当前卡及其19项继承/新纠错义务按依赖顺序绑定独立审查并释放. 默认检索实查78张可用、1张仍隔离(left-definite-orthogonal-systems). 最终查询初次以limit=60调用, 超过接口1..50而被拒绝; 保留已完成的19项释放、两条批注和索引, 仅用limit=50续做查询并通过核验. [协调器恢复记录](../../research/artifacts/proof-audit-round6-20260921/coordinator-recovery/README.md). 旧版回执失效的提示逐条按已审查的新修订识别为历史记录, 没有删掉旧警告或用旧PASS替代新验收. 增加两条绑定新版本的候选研究经验批注: 有限维尾部障碍与必要/充分条件的区别, 以及成员资格与组合残差抵消的区别. [最终工具库状态](../../research/artifacts/proof-audit-round6-20260921/library-final.json).

当前README、中英文导航、研究理解、Lean范围、AGENTS和续接入口均已更新. 本轮证据目录与发布报告目录单独提交-text属性, 保留源码、日志和清单的精确字节, 不依赖用户原本未提交的根属性设置. 原46个SL Lean源、第五轮两迹TeX/PDF、旧run/审计/纠错历史及canonical保持原字节. 插件源码和安装配置未编辑. 原六项未提交工作与134个既有未跟踪文件不纳入本轮提交. 发布前核验源码与回执身份、文档链接、全部原文件保护边界以及实际Git暂存blob; [发布候选清单](publication-manifest.json)记录精确文件范围. 已获授权按origin主仓库后fork顺序推送; 实际完成状态另见`F:/tools/math-audit-round6-20260921/DELIVERY.json`, 保持候选身份与事后交付回执分开.
