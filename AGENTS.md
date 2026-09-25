<!-- blueprint-project-layout:v1:start -->
# Blueprint v2.2 project layout (highest precedence)

- `blueprint-project.json` is the physical-layout authority.
- Canonical graph, inventory, submissions, and audit history are under `blueprint/`.
- Raw inputs and generated artifacts are under `research/`; disposable work is under `research/work/`.
- Do not run or copy project-local Python tools. Resolve the active plugin's `runtime/blueprintctl.py`, then run `ensure` once and use that gateway.
- Any legacy `statistics/.../tools/...` command below is documentation only and is superseded by this block.
<!-- blueprint-project-layout:v1:end -->

# 项目维护

## 2026-09-26 第十一轮审计修缮 (修订与验收完成)

用户提供 "C:\Users\HuangZY\Downloads\sl_audit_round11", 指定 math-research-workflow 2.0.1, 后补充 "重新看一眼". 目录首次不可见, 再查已到位. 基线4f6b35c, 15077个tracked、134个原untracked和6项原dirty已记录到F:/tools/math-audit-round11-20260926/baseline.json. 报告及全阶余有限补证均作为待核实证据.

本轮工作方法: 复现并修正残差Jacobian交叉分块和经过坐标转换的中心差分方向, 核查实际调用链; 单独推敲0<=s<7/2余有限闭包补证及临界迹门槛. 相关活动程序、附件隔离副本与必要局部Lean可用于本轮验证, 不运行旧Blueprint维护器或写canonical. 解析作者、形式化作者和最终全新fork_context:false检验者分离; 保存原生身份、真实回执及失败记录. 工具纠错使用已安装原版API, 保留旧证据/旧Lean和原未提交内容. 更新地图、理解、工具和续接后按origin先于fork推送. 具体对话与方法记录于state/AGENTS_SESSION_LOG.md.

第十一轮完成: 两项Jacobian/差分错误已在真实模型中复现, 三个活动程序及四张卡修正. 独立解析补齐固定c>0、0<=s<7/2余有限分类, 含三个临界点和原族非基推论; 12页新PDF、A12/B9地图及理解同步. 六个独立无状态检验通过, 局部Lean14定理/12定义、37声明导出和13项根不等于完整分析形式化. 8张纠错/续审卡19项义务经原版API放行, 新增1卡与8条版本批注; 实际查询90可用/1原撤回, 历史失效记录保留. 原51份Lean、canonical、旧证据及134原untracked/6dirty按字节保护. 插件未改. 精确发布见本轮报告及外部DELIVERY, origin先于fork.

## 2026-09-25 第十轮审计修缮 (修订与验收完成)

用户原话: "C:\Users\HuangZY\Downloads\sl_audit_round10 进行修订", 指定 math-research-workflow 2.0.1. 基线5bb6b260, 13818个原tracked、134个原untracked和6项dirty已按字节记录至 F:/tools/math-audit-round10-20260925/baseline.json. 已用真实旧源码复现漏掉低频根, 并核对反射全索引赋值不是投影. 输入报告和附带程序按待核实证据处理.

本轮限定授权涵盖共享谱引擎、反射种子、实际调用的局部程序测试和隔离副本回放, 不执行旧Blueprint维护器或改写canonical. 谱序号由连续提升的Pruefer相位定位, 高精度细化保持同一指标. 两种反射投影必须检查转换后的实际接口和可行步长. 解析/数值/形式化分开登记; 作者与最终fork_context:false检验者分离, 保留真实执行与退回记录. 工具纠错通过已安装原版模块, 历史证据保持原字节. 完成后维护研究地图、理解与续接入口, 沿用origin后fork同步授权. 详细对话见state/AGENTS_SESSION_LOG.md.

第十轮完成：真实旧源码复现漏根和投影混淆，共享连续相位按谱指标括根，mp/FD保持同一指标；两种反射投影检查真实可行接口，并撤回旧反对称网格的破缺解释。四个默认变分配置及实际侦察重算，5个新无状态检验分别完成解析、未变卡续审、软件执行、38声明盲读和独立Lean编译/语义核验。局部Lean为22定理/6定义、21项合取根，不是完整Sturm或Python形式化。8张卡15项事项放行、5条版本批注，实际查询89可用/1原撤回；历史失效回执保留。5页PDF、B8研究节点、理解、导航与续接同步。原50份Lean、canonical、旧证据、134原untracked/6dirty按字节保护；插件未改。精确发布与双远端身份以本轮报告、外部DELIVERY及实际Git为准。

## 2026-09-23 文献吸收 (研究与接入完成)

用户提供 selected_references.bib 与 absorption_plan.md，原话“依照方案在项目中吸收文献”，指定 math-research-workflow 2.0.1。基线902d2a931；原13442个tracked、134个untracked和6项dirty的身份在 F:/tools/sl-literature-absorption-20260923/baseline.json。来源和计划中的断言须与原文及当前模型分别核实。

方法：13篇来源按实际版本、读取位置、原件/提取哈希记录；原文缓存使用已安装插件的capture/read接口，公开原创笔记明确标secondary并保留原件指针。三位作者负责域、近似/删项、界面，独立验收另启fork_context:false新会话。按具体假设接入工具卡、版本批注与研究地图，获取不到完整定义的来源保留为线索。书目改动也检查整文件审查绑定并续发所需回执；现有canonical、旧形式化及无关未提交工作按字节保护。续接先读上述外部CURRENT与[吸收入口](literature/absorption-20260923/README.md)，核对实际任务、来源和回执，不重启已完成作者。详细对话见state/AGENTS_SESSION_LOG.md；最终交付按origin后fork顺序。

13项来源完成分级吸收：12项原文定点阅读、L13仅元数据/不完整预览；11新卡、16版本批注，实际检索89可用/1原撤回。四份最终隔离审查通过；P0的L1/L∞混淆和P1的仿射例外/页码/无依据日期首次退回均保留并另审修复。s=3三迹余有限闭包、分数域字典、固定c的Legendre替代系、有限局部界面二阶公式及两个无限删项子类按精确范围登记。全局O1/O2/G1′、L13模型及一般删项仍开放。新增Lean为零，50旧源保护；canonical未修改。书目PDF重建且正文不变，3项已有卡义务续发。索引保存后退出120以query-only续接，真实退出和新结果分别留存。详细记录见[交付报告](reports/literature-absorption-20260923/REPORT.md)；最终发布身份仍以外部DELIVERY和实际双远端为准。

2026-09-23续接：用户原话“继续完成这轮任务”。暂停时已完成研究、入库和检验，尚未提交；续接只核对已保存身份、完善输入绑定检查点和最终导航检查，再做精确提交及origin/fork同步，不重跑已完成作者或重新宣称新证明。

发布范围复核明确：P0冻结审查包按原版机制含仓库已有L02/L12原PDF，P1–P4私有审查导出不携带新取得的整篇原文。报告的此前笼统表述已澄清；旧checkpoint原样保留，当前checkpoint绑定最终报告。

## 2026-09-23 第九轮审计修缮 (研究与验收完成)

用户原话: "C:\Users\HuangZY\Downloads\sl_audit_round9 继续修复", 指定 math-research-workflow 2.0.1. 核对附件和基线2a81b608后修复真实积分投影、有限Green核、归一化导数核项、物理世俗函数频率因子; 新补证仅闭合规定平衡候选序列的单调性与极限, O1/O2、G1仍开放. 两份PDF、研究地图、理解、导航、工具注释和续接记录同步. 详见[本轮报告](reports/proof-audit-round9-20260923/REPORT.md).

方法: 附件作为待核实证据; 作者与无状态fork_context:false检验者分离, 冻结精确输入, 保存原生调用和真实回执. 两次首次退回另修: 卡片集中极限遗漏质量收敛, 极窄脉冲在浮点坐标中塌缩. 五份最终独立检验通过; Lean59声明经盲读及另一个新会话亲自编译/语义核查, 仅认证局部代数接口. 使用已安装2.0.1原版纠错模块释放3张修订卡, 12张未变卡完成22项续发; 实际检索78可用/1原撤回. 保留57条历史失效回执, 不绕过门禁.

保护基线12666个tracked、134个原untracked、6项既有dirty, 49份旧Lean源、历史证据及canonical. 不改插件/cache或全局环境. 外部F:/tools/math-audit-round9-20260923保存真实执行与发布状态; 中断后先核对CURRENT/DELIVERY、实际双远端和原工作树, 不重跑已完成研究者. 精确暂存, origin先于fork推送; 具体对话与操作见state/AGENTS_SESSION_LOG.md.

## 2026-09-22 第八轮审计修缮 (本轮完成)

用户原话: "C:\Users\HuangZY\Downloads\sl_audit_round8 继续修订", 指定 math-research-workflow 2.0. 读取报告、解析补证、checks.py 及原失败/成功记录; 附件是待核查证据. 基线 d1462eb, 10236 个原跟踪文件、134 个原未跟踪文件与 6 项既有脏文件已保存字节身份到 F:/tools/math-audit-round8-20260922/baseline.json. 审计包十个清单哈希及六份被引用源码的原始 Git blob 身份核对一致.

本轮修复 n=1 INF 极限的根像端点、区间超越函数、连续薄层区域覆盖、相位分支和固定 u 收敛率, 并扩查余切级数下标、相位括号极限与失效证书引用. 历史 run 05/16/19 及封存回执保留原字节; 新证书和解析替代另写. 协调器负责当前文档、工具纠错、导航与交付; 解析、精确算术和局部 Lean 作者在项目外分工. 最终验收另启 fork_context:false 子 agent, 冻结精确输入并保留原生调用/实际完成回执. 使用已有维护版插件运行时处理四张相关卡的隔离、版本修订与逐事项释放; 不以旧缓存中的缺失接口代替纠错门禁. 暂不改变 canonical 或 n>=2 / 左定结果. 沿用主仓库后 fork 推送授权, 保留其它未提交工作.

第八轮F01-F05及P01-P03直接传播已修订. 连续展开相位给出全R>=1统一谱隙下界, 覆盖完整薄层域; 大w初等正余量比较与T2解析结构闭合T1, 不再依赖旧网格或T3数值. 固定内部u的首项为C(u)/R, 在u*处C严格正; 最优值满足非负O(1/R)误差. 精确最优系数与参数速度未在本轮证明. 新证书只以有理数、Machin/Taylor误差和显式守卫作证明运算. 独立证书重放及56次预期失败负对照、独立解析审阅、局部Lean新编译/盲读/语义核对均分别留证; Lean不等于完整谱论或隐函数展开形式化.

四卡放行后的实际查询暴露综述整文件绑定问题: 70可用/9隔离. 只有INF段落变化, 但八张未变的左定卡的第六轮审查已失效; 保留失败状态, 对18项既有事项义务另启新无状态审查, 原卡/证明字节不变, 以新审查续发同一修订的回执. 最终78可用/1原隔离, 四改动卡加八原字节卡共22项义务. 35个历史失效回执保留: 17项后继版本、18项同版本新审查; 逐张核对当前检索摘要/哈希/依赖. 今后修改综合文档应检查所有绑定它的有效审查, 不能只检索直接数学依赖. 随后实际摘要检查又发现三张原卡的索引继承了过时摘要, 其中Krein仍有错误边界条件和开放状态. 通过已有from-index恢复流程, 从已审查的当前卡正文重建摘要, 另一个新隔离会话检查后替换派生索引; 卡片及纠错门禁状态不变. 对无显式summary的旧卡比较正文导出的摘要, 而不是要求它们凭空新增字段. 数量恢复不是摘要正确的证据.

三PDF重建为11/17/20页, 主文全页与伴随改动页检查; 研究地图新增B4-INF-LIMIT, 维持B4总体PARTIAL, 更新项目理解、双语首页、研究/工具/脚本导航、Lean状态和续接. 研究经验另存精确版本批注, 更多层的相位传播明确为待证想法. 作者早期失败、检验器三次失败及修正、作者通知/排队跟进造成的等待超时均留原始证据, 不伪造完成回执. 六次最终检验均为新fork_context:false会话. 48份旧SL Lean源、canonical、冻结旧证据和原无关工作按基线保护. 本轮未改插件源码/缓存或全局环境. 精确提交范围与主仓库后fork交付以第八轮报告及项目外DELIVERY.json为准.

## 2026-09-21 第七轮审计修缮 (本轮完成)

用户提供 proof_audit_round7_20260921.md, 原话“继续修订”, 指定 math-research-workflow. 基线636dac8; 原文件身份和未提交工作已保存在 F:/tools/math-audit-round7-20260921/baseline.json. 本轮收到的是单份报告, 其中提及的 spectral_repairs.md/checks.py 未提供, 不声称读过或重放这些附件. 核查R7-F01常密度公式、F02端点一致估计、F03一般指标SUP极限、F04镜像导数及直接传播. 用原始源码和独立推导验证报告, 新检验采用fork_context:false的隔离会话, 保留实际回执. 必要局部Lean和数值检查与完整分析证明分别报告. 旧冻结run/review及canonical保持原字节; 研究地图、当前工具卡与续接记录随修订同步. 沿用主仓库后fork推送授权, 其它未提交工作不纳入本轮提交.

第七轮直接传播扩查: 发现旧诊断脚本的镜像因子/符号以及Hessian逐元素乘法问题, 扩展到10个明确调用文件的局部修订与真实行为回归, 不重跑历史大规模扫描. 三张重复det/惯性等价的工具卡同步纠错, 当前侦察总结限制4pi²为n=1. 这些活动脚本的修复测试属于本轮授权; 旧冻结数值、证书和旧Blueprint程序不改写. 各作者输出仍先在项目外, 验收由新隔离会话完成.

第七轮检验中的二次纠错: 索引会继承旧summary, 因此本轮五卡通过版本API显式写入正确摘要, 最终必须核对默认查询实际返回的摘要和新FH依赖哈希. 第一轮软件独立检验发现测试harness先过滤外部模块再检查隔离, 拒收该保证; 数学十文件保持原候选字节, 仅修复harness并增加真实外部导入与缺失模块负对照, 重新交新会话检验. 作者自检、独立执行、语义审查和工具放行分别登记; 不改写首次拒收或早期Lean导出失败.

第七轮放行阶段发现协调器遗漏: 三张下游卡同时受直接事项与上游FH事项影响, 前者局部释放不消除后者复核义务. 保留原STILL_BLOCKED回执, 对同一当前卡字节补建三个继承事项修订, 另启新隔离会话审查; 最终实际查询通过才可交付. 后续维护应按“卡片精确版本 x 受影响事项”核对义务, 不能只按卡片数量计完成.

第七轮F01-F04及P01-P04直接传播已修订. 统一Volterra端点引理与一般SUP极限获新隔离解析审阅通过; 五卡八项事项义务按精确版本复核与释放, 原三项STILL_BLOCKED记录保留, 默认78可用/1原隔离, 显式摘要逐张核对. 十程序与来源验收器获独立复验, 117项有限检查正常/-O通过; 独立数学检查25/25并拒绝旧FH公式. 局部Lean20定理/7定义完成新编译、正负对照、完整声明/公理和隔离语义核对, 不称完整Volterra/min-max形式化. 三PDF重建, 研究地图新增B4-SUP-LIMIT而B4保持PARTIAL; 项目理解和续接入口同步. 早期导出失败、软件拒收、缺材料包、摘要继承错误及下游继承义务遗漏均保留实况. 47旧Lean与canonical/无关原工作保持原字节; 最终精确提交及主仓库后fork交付见第七轮报告和外部DELIVERY.json.

## 2026-09-21 第六轮审计修缮 (本轮完成)

用户原话: “C:\Users\HuangZY\Downloads\sl_audit_round6 继续修复”, 指定 math-research-workflow. 基线92d46e9, 原7510跟踪文件/134未跟踪文件及6项既有脏文件已按字节保存身份. 收到的报告、反例与分数窗补证先按待核实证据处理. 继续沿用无状态隔离检验和主仓库后fork同步授权.

本轮核查R6-F01投影稀疏族与排除项判据、F02空洞有限矩准则、F03表示元解释, 以及R6-C01的0<=s<7/2补证. 解析作者分别负责新的投影/矩修复文稿和当前分数阶文稿的版本化修订; 协调器保存旧版字节并处理工具库传播、导航和交付. 第五轮两迹证明及旧run/审计不改写. 可执行附件的隔离副本、必要新增局部检查与Lean编译, 不执行旧Blueprint维护程序、不写canonical. 最终检验另启fork_context:false会话, 保留真实回执并明确形式化范围. 插件源码和安装配置未编辑.

第六轮隔离记录: 首次形式化盲读因包外项目记忆/技能读取而INCOMPLETE, 未用于验收; 原回执保留, 另开全新会话完成盲读并由不同会话核对语义. 具体证据及边界见本轮报告.

第六轮三项发现及完整分数窗补证已修订, 两份解析证明经新的无状态隔离审查通过. 九卡及继承纠错义务逐项绑定并恢复默认检索, 历史证据/批注保留. 新局部Lean覆盖真实实多项式全指标张成、四迹矩阵及修正、抵消例和检测反例, 经实际编译、正负对照、隔离重放、盲读及独立语义审查; 不称完整解析证明已形式化. 四份PDF重建, 新证明全页与其它修订页完成版面检查. 本轮证据目录与发布报告目录独立设置-text以保留哈希所绑定的原字节. 原未提交工作、旧46份Lean源、第五轮证明及canonical保持字节; 精确暂存和双远端核验见外部交付记录及本轮报告.

## 2026-09-21 第五轮审计修缮 (本轮完成)

用户原话: “C:\Users\HuangZY\Downloads\sl_audit_round5 新一轮审计报告, 修复问题”, 并指定 math-research-workflow. 基线 c0b36b9, 原6601个跟踪文件与134个未跟踪文件已保存哈希. 审计报告和附带替代证明是待核查材料. 沿用已授权的隔离检验与主仓库后fork推送.

本轮聚焦R5-F01尾部刚性/余有限像族/真闭子空间的三个原候选声明, 及R5-F02奇部换元系数. 保留旧run、H2/H3和第四轮已修主链原字节; 新写s=2余有限分类证明, 当前卡标明反证与替代范围. 可运行附件隔离副本和本轮必要局部Lean, 不运行旧Blueprint维护程序、不写canonical. 作者只修改分配文件, 最终审查另启fork_context:false会话, 保存实际回执; 工具库通过现有纠错模块隔离、修订、复核后恢复检索. 原未提交工作不纳入提交.

第五轮已核实并修复两项发现: 原三条NOT-YET-STRICT候选按原量词为REFUTED; 单项式引理保留结论并修正换元及证明. 新增复Hc2余有限两迹分类和完整Green障碍, 经新隔离数学检验通过. 37个局部Lean定理/22个定义经协调器重编译、独立执行者196项检查、59项盲读及另一会话语义审查; 不称完整Sobolev形式化. 新卡经精确纠错回执释放, 默认78可用/1隔离. 10页PDF构建与逐页版面检查完成, 旧源/封存证据/canonical和原未提交工作按字节保留. 索引中断从已提交修订续接, 遗留锁和接收适配错误保留实况. 具体对话、方法、检验边界和主仓库后fork交付见第五轮报告与会话日志.

## 2026-09-21 第四轮审计修缮 (本轮完成)

用户提供 `C:/Users/HuangZY/Downloads/sl_audit_round4_20260920`, 原话为“依据此处的审计报告继续改”, 并指定数学研究工作流. 延续已授权的修缮、无状态隔离检验与云端同步. 附件是待核实材料, 建设性补证不因随包提交而自动通过. 基线 `2e9bf3d`, 原5609个跟踪文件与134个未跟踪文件的哈希保存在 `F:/tools/math-audit-round4-20260921/baseline.json`.

本轮核查归一化代表/商类、三阶递推、参数分类和活动 d4 程序. 可运行本轮相关活动程序、附件的隔离副本与必要局部形式化检查; 此授权不包括旧 Blueprint 维护程序或 canonical 写入. 作者分工只修改指定活动文件, 最终验收另启 `fork_context:false` 子 agent, 保留真实调用、冻结包及退回记录. 既有 canonical、历史审计、未分配草稿及旧 Lean 源文件按原字节保留. 最终更新报告、工具库与续接入口, 按主仓库后 fork 顺序推送.

第四轮F01-F05及传播问题已修订, 两份解析证明经独立检验通过. 程序两次退回后补齐混合精确数值、包装函数和符号零处理, 最终独立复检通过. 局部Lean新增41个定理、23个定义, 实际编译、根对象/依赖哈希、正负对照、独立盲读及另一会话语义审核通过; 未把解析收敛、最小解或全部实数参数冒称已形式化. 三份PDF重建, 相关八卡获当前范围的释放/续接回执, 默认检索78卡可用、1卡仍隔离. 冻结旧材料与原未提交工作保持原字节. 具体对话、检验边界和交付记录见第四轮报告及会话日志.

## 2026-09-20 第三轮审计修缮 (本轮完成)

用户提供 `proof_audit_round3_20260920.md`, 原话为“核实并修复这个文件指出的问题, 别忘了推送到云端”, 并指定数学研究工作流. 附件作为待核查材料. 基线为 `aac44f5`, 5149 个原跟踪文件与 134 个原未跟踪文件的身份保存在 `F:/tools/math-audit-round3-20260920/`; 既有研究草稿和 canonical 保留.

R3-F1/F2 的一般递推、基扰动与 R3-F3 的商空间证明已核实修订, 直接传播到综述、两张工具卡、五个活动脚本与阅读入口. 作者按领域分工; 每次最终检验另启 `fork_context:false` 的无状态子 agent, 只提供冻结最小材料并保存真实回执. 程序首次独立检验发现多步相减仍可能误判符号, 改为输入系数的精确有理数比值递推并交新会话通过. 形式化首轮语义一致但证据包不全, 补齐负对照源码、原生执行/导出记录及根对象绑定后再由新会话通过. 原拒收、未完成回执及修订前原字节均保留.

最终五程序、17 项行为测试及5项原始回归通过; 53 项协调器精确检查与商空间18项作者检查的范围分别记录. 新 Lean 为24个局部定理与10个定义, 实际编译、逐声明公理导出和新目录重放通过; 两个旧公式负对照真实失败. P2 积分识别、完整完备性及谱截断没有因此全部形式化. 三份 PDF 重建. 两卡经独立数学复核释放并实查默认查询: 78张可用、1张隔离, 94个历史版本、30条纠错事件和一条新版本绑定经验批注.

本轮授权执行相关活动脚本与必要局部检查, 不授权旧 Blueprint 维护程序; 没有写 canonical 或重建历史全库. 旧 `_patch_stability12*.py` 仅保留溯源, 不作当前更新入口. 按主仓库、fork 顺序同步; 精确提交清单与交付核验另存. 详细对话、独立检验与剩余问题见 `reports/proof-audit-round3-20260920/REPORT.md` 和会话日志.

## 2026-09-20 云端同步

用户明确要求同步插件与本成果仓库. 本次提交两轮审计的活动修缮及其直接证据依赖, 包括证明/PDF、局部 Lean、工具卡与纠错历史, 并维护导航. 先核对主仓库与 fork 基线, 再逐文件暂存和核对提交 blob, 按主仓库后 fork 顺序推送. 不改 canonical、旧封存证明包或本轮独立检验输入; 其它实验草稿保留原字节. 插件的候选提交单独执行 CI, 不将同步或 CI 成功当作全仓库数学认证. 具体对话与方法记录在会话日志.

## 2026-09-20 第二轮审计修订 (本轮完成)

用户提供 `proof_audit_round2_20260920.md`, 要求修缮并增强工作流: 过程内形式化、无状态隔离检验子 agent、外部发现驱动的工具库纠错. 原报告的建议是待核查材料. 本轮保留第一轮及其它未提交变更, 原字节和基线保存在 `F:/tools/math-audit-round2-20260920/`. 数学作者与验收 agent 分开; 验收明确 `fork_context:false`, 仅给冻结证据包. Lean 片段通过不等于整项研究形式化.

谱域/K1、首对/MW 与局部 Lean 已分别获得新隔离会话的范围明确的批准. 中间否决发现的归一化、索引域、积分收敛、弱探针、摘要和递推算术问题均已修订, 原始否决保留. 软件的日志、恢复、下游误放行和依赖版本覆盖问题也经新会话验收关闭. 九卡已按依赖顺序恢复并逐张查询; 当前 78 张可用、1 张隔离, 92 个历史版本和三条新经验批注保留. Linux/Windows 各 84 项行为测试通过; 25 个局部 Lean 目标及五个缓存旧定义桥接已验证, 完整主定理未全部形式化. 原始 WSL 回执需在原调度路径消费. 详情见 `reports/proof-audit-round2-20260920/REPORT.md` 与会话日志. 维护不要改写旧封存审计或以历史 PASS 替代当前复核.

本轮将用户的程序修缮请求理解为包含必要的实际行为验证: 协调器可运行本轮修改的 `scripts/op10_verify_mechanism.py`、`scripts/op10_fractional_window.py` 及新 Lean 目标, 日志保存至项目外, 禁止写 canonical. 这项限定范围测试不使用项目旧 Blueprint 维护程序; canonical 操作继续走插件 gateway.

## 目标与入口

- 维护 Sturm-Liouville 边值问题的长期研究: 正交系/左定空间, 相邻特征值比值与间距极值.
- 本仓库是 [rigorous-open-math-research](https://github.com/xsoc1/rigorous-open-math-research) 的使用成果仓库. 归属区分既有文献, 合作者工作与人机合作推导.
- 研究入门读 [研究导航](docs/research-guide.md); 接续具体问题读 [research_map.md](research_map.md), 相应 run 和证据. 理解变化与人的批注写入 [项目理解](docs/PROJECT_UNDERSTANDING.md).
- 具体证明, 反例, 构造和严格审计使用研究插件. 工具卡及其索引在 [tools/README.md](tools/README.md); 形式化范围见 [lean-proof/STATUS.md](lean-proof/STATUS.md) 与脚手架登记.

## 工作方法

1. 进入项目先读根与相关子目录 AGENTS.md. 每次维护后在本文件写简短摘要, 具体对话与方法记入 [state/AGENTS_SESSION_LOG.md](state/AGENTS_SESSION_LOG.md).
2. 如实区分 STRICT, EVIDENCE, 待检验与 OPEN. 数值样本不能替代证明; NO_RETURN 和超时不构成数学失败. Lean 编译, 陈述保真, 假设闭合与 canonical 接收分别描述.
3. 从论文或路线提炼工具时记录实际来源版本, 可定位内容, 假设与用途. 成功, 反例, 方法局限和实现错误都可以记录; 自由批注注明来源与证据状态. 再检视旧路线时说明改变了什么条件或获得了什么新信息.
4. 保留被 hash manifest, 审计, checkpoint 或引用绑定的文件路径与字节. 新批注另写, 原始证明包保持可复核. 既有未提交工作先比较与备份, 按本轮 scope 修改.
5. 清理按 [归档规则](docs/archive-policy.md) 查引用和可再生性. 不按 mtime, 名称或重复字节删除研究内容. 常规导航与人类批注不需要复制整个研究台账.
6. canonical 操作使用顶部指定的插件运行时 gateway. 历史本地 Python 维护或 Blueprint 命令仅作记录, 不直接执行. 普通仓库清点可以用 shell 或独立临时检查程序.
7. 文档使用英文标点. 新代码 tab 缩进, 多词函数 snake_case, 多词变量 PascalCase; 适用语言中大括号独占行, if/for/while/switch 与左括号间无空格. C++ main 的末三句依次为 cout << endl;, system("pause");, return 0;.
8. 外部临时仓库放 F:\tools\. 数学结果引用文献时核对实际读取内容, 不凭摘要猜测定理.
9. 已授权同步时先推主仓库 Zhongshan-Big-Jun/Sturm-Liouville-theory-research, 再推 xsoc1/Sturm-Liouville-theory-research fork. 本轮并行成果仓库 agent 不 commit/push, 由协调器处理交付.

## 当前数学边界

- n=1 SUP/INF: 历史 STRICT/CLOSED 范围为归一化盒类 1<=rho<=R, 全部 R>1. 2026-09-20 修正 C1 包络、O1 自伴化、归一化证书接口和 good-root 引理; 本轮局部验证不等于重跑整条证明或 Lean. 详见 [审计修订报告](reports/proof-audit-20260920/REPORT.md).
- 原始稀疏多项式族: 第六轮四迹图核心补证给出固定c>0时0<=s<7/2稠密, 每个非仿射命名成员在s>=7/2出域. 仿射成员始终合格, 有限组合可以抵消边界残差. H2/H3主证明保留, 一般受约束或删除分类另计. 当前投影/有限矩条件见第六轮报告, 不沿用旧A-H整组STRICT.

- 第十一轮余有限分类: 固定c>0、复幂域0<=s<7/2, 必要保留指标依次为{}, {0}, {0,1}, {0,1,4}, 在s=1/2,3/2,5/2等号点取较少迹的一侧. 删除p6仍稠密, 原族经逐项非零缩放与重排仍非Schauder/Riesz基. 新解析证明已独立审查, 一般无限删项与完整Lean另计; 见docs/SL_cofinite_all_orders.pdf.

- M3: n=2 对称 INF large-R 有限非零内部 chart 内 STRICT 闭合, canonical 接收与独立复现已保存. 旧 staged D-side mass 的 odd/log 障碍已 SUPERSEDED.
- KP-DET: sequence-26 的完整 0<c<=2/3 分支与 P20-P21 求积约化经审计 PASS. P1-P4 的 pivot/phase 部分已 canonical 接收; 后续 run 包与 canonical 分开登记. 本地主 run 的 Q9 仍 OPEN.
- 插件公开 benchmark 另有三份 Q9 完整证明及匿名外审 PASS, 尚未接入本 canonical 或 Lean. 不据此宣称全局 G1', KO-DET 或完整 n>=2 极值问题已解决.
- 旧文档中 G2 的闭合范围表述存在差异, 需要按定义与量词对齐. 本轮维护不改写历史证明来消除差异.
- Lean 工程含已检查的证明片段, 条件化接口和带 sorry 的脚手架. 历史全库计数不得复述为当前形式化结论.

## 近期维护记录

- 2026-09-09: 补查归档的 Git clean 转换. Windows Git 的 autocrlf=true 会改写两份旧 README 和完整会话日志; 在 docs/history 与 state 新增只匹配这 3 个归档文件的 -text 属性. 原根 .gitattributes 保持不变. 通过独立对象目录的 hash-object/show 核对实际提交字节, 精确暂存集更新为 157 个路径, 未 stage/commit/push.
- 2026-09-09: 中断后续接导航发布依赖检查. [发布依赖清单](reports/repository-cleanup-20260909/publication-dependencies.json) 列出 12 个需按原字节纳入版本的既有 KP-DET 证据, 递归绑定检查, 历史绑定限制和协调器精确暂存范围. 只更新文档与报告, 未 stage/commit/push 或接收 canonical.
- 2026-09-09: 按用户 2.0 落地任务并行整理成果仓库. 重写中英文首页, 归档旧首页与长 AGENTS, 新建研究导航, 项目理解和脚本导航. 删除 10 个无引用的过时维护程序与 115 个可再生 TeX 中间物; 4,392 个原文件字节不变, 61 份文档 PDF 解析通过, canonical gateway 校验通过. 具体哈希, 原 68 项工作树保护和验证见 [清理报告](reports/repository-cleanup-20260909/REPORT.md). 未 commit/push.
- 2026-09-10: 核查插件版本并落地 2.0. 本机 checkout 原为 1.5.0, 云端 `origin/main` 为 2.0.0, 快进 `d1ca3ee` -> `4f75026` (16 提交); `validate_all.py` 51 项通过, `dsh-doctor.py` 需显式 `--python /usr/bin/python3`. 本项目 gateway `ensure` 返回 `ALREADY_READY`, canonical validate 为 11 nodes/13 edges/4 inventory rows, pipeline 为 `DATA_CHECKS_PASSED`. 深度理解插件与数学项目, 并核查封存 checkpoint: sequence-26 在保留 workspace 根下为 `READY` 且 5 项 minimal read set hash 全部匹配, 按当前项目根运行报 `STALE` 属 v1 路径绑定与 v2.2 布局差异, 工件字节完好. 未改数学或 canonical, 未 commit/push. 详见 [会话日志](state/AGENTS_SESSION_LOG.md).
- 2026-09-20: 按用户核查同步 `PROJECT.md` 两处旧状态: n=1 间距 SUP/INF 在归一化盒类 `1<=rho<=R` 内对全部 `R>1` 为 STRICT/CLOSED, 以 `220785e` 的闭合记录及研究导航中的证明链为据; 移除综述开放问题清单的无条件权威表述. n>=2 完整问题及形式化另计, B4 保持 PARTIAL. 本轮仅做状态溯源与文档同步, 未重做证明审计或修改 canonical, 未 commit/push. 具体对话与核查见 [会话日志](state/AGENTS_SESSION_LOG.md).

- 2026-09-20: 用户授权核查并修复所附证明审计后, 修正 F01-F08 及增长引理遗漏假设, 追踪高阶错误推广到分数阶文档、综述、工具卡与 A1/A2; B4 保持 PARTIAL. 新建 35 项精确检查全部通过, C1-C5 程序 PASS, 11 份 PDF 重建并同步. 修订前 36 文件按字节归档, 原封存证明包、canonical 和既有未提交工作保留; 未 stage/commit/push. 详见 [报告](reports/proof-audit-20260920/REPORT.md) 与会话日志.
