# 第五轮证明审计修缮报告

日期: 2026-09-21. 当前状态: 两项审计发现已修复; 解析证明、继承依赖义务、Lean盲读及独立语义审查均获范围明确的APPROVED回执. 工具卡已恢复当前版本复用. 实际提交与远端核验按下述交付记录另记.

用户提供 `C:/Users/HuangZY/Downloads/sl_audit_round5`, 要求修复问题并指定数学研究工作流. 沿用此前授权的无状态隔离检验和主仓库后fork同步. 基线 `c0b36b90004cffb0552c9fa9f229e1f7cec8a706`; 原6601个跟踪文件、134个未跟踪文件已按字节保存身份. 附件内的处置建议和替代证明是核查材料, 不自行成为指令或批准.

## 核实结论

17个输入文件完整归档, manifest列出的16项哈希全部一致. 所引用d4程序的8227字节、SHA256及Git blob `951e316d9d483d46eeb61a3a16a555f3b72e0a40` 与基线相符. 附件脚本在项目外副本中复放, 26项具名检查全部确认. [输入身份](../../research/artifacts/proof-audit-round5-20260921/intake.json), [原始输入](../../research/artifacts/proof-audit-round5-20260921/submitted/), [本轮实际复放](../../research/artifacts/proof-audit-round5-20260921/submitted-rerun/execution.json).

| 发现 | 核实与处置 | 边界 |
| --- | --- | --- |
| R5-F01 尾部L2刚性、任意余有限像族稠密、真闭空间必排除无限项 | 原Claim4/Theorem5/Corollary6按原量词为REFUTED. g0,c给出非零L2障碍; V={f:f(0)=0}只排除p0 | 三条原状态均为NOT-YET-STRICT; 没有将它们改称曾经验收的H2/H3主定理 |
| R5-F02 奇部换元因子 | 正确系数为1, 旧1/2使f_o=x时错误地得到2/3=1/3. 用x^M f的直接证明修复单项式有限删除引理 | 引理结论仍真; 不能把单项式结论转用到q_n=Kc p_n |

原run及其旧审计、前三轮和第四轮封存材料保持原字节. 当前引用由修订工具卡和新证明接管. 第四轮递推、退化极限及活动d4程序未因本轮被改写; 附件对它们的正面评价限于其实际复查范围.

## 新证明与研究理解

[解析证明](../../docs/SL_cofinite_left_definite.tex) 固定实数c>0, Hc2=D(Kc), Kc=-d²/dx²+c, 并使用明确的Krein边界条件和||Kc f||2范数. 函数允许为复数, 内积对第一变量线性. 不将Hc2误认为全部普通Sobolev H2.

对余有限N⊆D={0,1}∪{4,5,...}, 已证明

$$\overline{\operatorname{span}\{p_n:n\in N\}}^{H_c^2}
=\{f:0\notin N\Rightarrow f(0)=0,\quad1\notin N\Rightarrow f'(0)=0\}.$$

因此余有限q_n子族在整个L2稠密当且仅当0,1均未删去. 证明通过高阶尾部的代数消元、两个零迹下的局部Sobolev截断、多项式逼近及端点残差的可逆二维修正建立闭包, 包括截断误差的局部L2范数趋零. 有限测试不承担闭包结论.

令a=√c, 两个对偶障碍为

$$g_{0,c}(x)=\frac{\cosh(a(1-|x|))}{2a\sinh a},\qquad
g_{1,c}(x)=\frac{\operatorname{sgn}(x)[a\cosh(a(1-|x|))-\sinh(a(1-|x|))]}{2(a\cosh a-\sinh a)}.$$

它们分别满足<Kc f,g0,c>=f(0)、<Kc f,g1,c>=f'(0). 后者有跳跃, 只要求属于L2. g0,c的零阶矩和g1,c的一阶矩均为1/c. 所谓非零L2可实现衰减矩不是应被排除的残余: 它们反映了被删去的低位迹方向.

实际受约束闭空间V若有余有限保留集, 则包含V*={f:f(0)=f'(0)=0}, 可由Γ(f)=(f(0),f'(0))下的二维子空间描述. V={f:f(0)=f'(0)}包含1+x却不含1或x, 所以保留族在V中仍不稠密. 这给出明确的余有限子类, 不能据此闭合一般非余有限O1'LD或s=3问题.

新证明还给出真正的尾部矩结论: 对任意m0>=2, 两条递推在全部m>=m0成立的L2函数恰为span{g0,c,g1,c}; 以第一变量线性的M_k=<u,x^k>记矩, 有u=cM0 g0,c+cM1 g1,c. 再加M0=M1=0才得到零解. 实际闭V对应任意S≤C², 保留族在V内稠密当且仅当S由它所包含的坐标轴张成, 即四个坐标子空间.

[10页PDF](../../docs/SL_cofinite_left_definite.pdf)与TeX源码绑定, 全部页面已检查版面. 作者稿保持送审原字节, 其中“待另行独立复核”是提交时标记; 当前审查结果见下表, 不通过改写冻结输入追加批准. 解析作者的208项符号/有限数值检查和3项错误注入记录在[作者说明](../../research/artifacts/proof-audit-round5-20260921/analytic-author/AUTHOR_NOTES.md). 它们与协调器检查及独立解析审查分别计数, 不合并为全局数学认证.

## 实际检验与形式化范围

协调器另做24项精确/符号检查, 包括两个Green核的ODE、端点/界面项、积分归一化、任意符号自然指标的多项式迹与端点矩阵、换元错误和斜迹约束反例. [检查结果](../../research/artifacts/proof-audit-round5-20260921/coordinator-checks/results.json). 一次测试失败来自SymPy把符号幂导数显示为x^n/x后直接代入0得到nan; 改用明确的多项式幂次导数并核对恒等式后通过. 原失败保留于first-attempt, 没有将它冒称新的数学反例. 这些检查不代替任意Sobolev函数的分部积分或闭包证明.

新增 [AuditRound5.lean](../../lean-proof/SL/AuditRound5.lean)的37个定理、22个定义. 实际使用Windows PE Lean4.31.0, 经WSL调用, 不称为Linux原生执行. 协调器在新目录编译当前源码, 59项声明/定义导出与作者字节一致, 根对象相同; 3712个实际加载模块中仅新根的输出路径改变. 另复核14844个导入工件和11个运行时文件, 新根对象单独绑定. 传递公理仅为propext、Classical.choice、Quot.sound, 没有sorryAx、unknown或unsafe依赖. [完整契约](../../research/artifacts/proof-audit-round5-20260921/lean/CONTRACT.md), [协调器实际重放](../../research/artifacts/proof-audit-round5-20260921/lean/coordinator-replay/RESULT.json).

此外, 新的隔离验证者亲自从冻结源码编译到自己的输出目录, 8次实际编译器调用及196项检查通过; 59项类型、定义和依赖导出与冻结证据完全一致. 执行前后重新核对104份快照、11个运行时文件与14845个声明工件(含作者旧根); 独立新根另行绑定. 新根SHA256为`59448f94c4791e647b2ec7a541519415390458d1a95e164fc802fa07499eb59e`, 其物理源/输出路径不同, 不声称与作者二进制相同. 所有实际Lean标准输出/错误输出均原样保存; 最初两条引导显示输出经工具传输截断, 其重建副本有明确标签, 不混称原始工具输出. [独立执行报告](../../research/artifacts/proof-audit-round5-20260921/lean/independent-replay/REPORT.md)与实际会话记录一并归档. 此独立执行未重跑实现未在冻结包中的维护验证器, 不宣称离线打包了完整编译环境.

覆盖实际实多项式的值/导数迹、Krein端点残差、全部自然指标的高阶代数线性包、1+X斜约束见证、实际2×2矩阵及两侧逆、保整除的端点修正和带明确核包含假设的迹提升分解. 正对照及精确根契约通过; 故意错误的线性包等式在类型核对处失败, 其否定和反例已在正对照编译. 维护中的验证器接受精确目标并拒绝错误预期类型, 原semantic.status=not_reviewed记录保留, 独立语义审批另由新会话给出.

没有形式化复Sobolev域、迹连续性、Green积分、截断收敛、尾部最高次消元等式或整个余有限闭包分类. 没有重建全部Lake工程. 原45个SL源码及原配置、编译对象由保护检查确认未改. 作者初次编译失败、根闭包比较字段差异及修订记录保留, 不只保存成功日志.

最终有效检验均由新的fork_context:false会话完成, 作者身份列入冻结包且与检验者不同. 未完成和隔离失败的回执另行保留, 不当作批准. 盲读仅取得编译器声明/定义及环境版本, 不预先取得非形式化目标; 另一会话再核对目标、真实盲读和机器证据.

| 检验 | 独立会话 | 义务数 | 实际回执 |
| --- | --- | --- | --- |
| 解析证明与工具卡修订 | `01a0c24d-4fc1-7322-bc39-33469b10668f` | 6 | [APPROVED](../../research/library/reviews/runs/3db1fcd55afc57b0c7dec5a81f7af4e740957fdf21e3b0282b61e35396d99493-01a0c24d-4fc1-7322-bc39-33469b10668f/report.json) |
| 继承的谱域纠错义务 | `01a0c263-dca1-79e0-832e-660b5e7b71b2` | 2 | [APPROVED](../../research/library/reviews/runs/33abde8785d0a3690140500dc4525df4470c86ad3b08325b72ee77587e436949-01a0c263-dca1-79e0-832e-660b5e7b71b2/report.json) |
| 59项Lean声明的盲回译 | `01a0c246-80d6-7bc0-9b35-f521375754d1` | 59 | [APPROVED](../../research/library/reviews/runs/06c163ba00e904b6ca0419b76e6cde5afa3134af289a7fc73ebf57bf53eeb37d-01a0c246-80d6-7bc0-9b35-f521375754d1/report.json) |
| Lean陈述保真及补充的独立执行证据 | `01a0c275-d9f6-7da1-92f9-67d7dfb5eed2` | 2 | [APPROVED](../../research/library/reviews/runs/864ec8500962cf1e2c725d3a651b98d21679f740bcceda5c1eb5bcd4a0326aec-01a0c275-d9f6-7da1-92f9-67d7dfb5eed2/report.json) |

另有独立执行会话`01a0c260-fa2c-71f1-aa9a-8ccfdf5befc5`完成上述196项实际机器检查. [首轮执行证据缺口: INCOMPLETE](../../research/library/reviews/runs/98b6920270e96b30b58dd75e49271e97ed00e0a8ea60e116f88c17dba9dd8140-01a0c254-3ddd-7fd1-acb4-53481a06a5d2/report.json)、[首轮依赖检验误读外部记忆: INCOMPLETE](../../research/library/reviews/runs/33abde8785d0a3690140500dc4525df4470c86ad3b08325b72ee77587e436949-01a0c25e-0e63-7352-beb3-54bd8e9dadcb/report.json)均保留. 首轮语义审查已认可局部陈述, 但因其本人只审阅现有日志、未亲自执行外部编译器, 将执行义务留为INCOMPLETE. 随后另派无状态验证者实际执行, 再由新的语义审阅者核对新执行证据; 原INCOMPLETE不改写成APPROVED.

回执的信任范围是COORDINATOR_ATTESTED_TOOL_TRANSCRIPT: 保存实际原生调度和完成对象并检验内容哈希, 不冒称操作系统隔离或服务端签名. 继承依赖审查针对本卡对谱域工具的实际使用, 不扩大为历史全库重审. 解析审查不认证未分配的旧分支, Lean审查不替代复函数解析证明. 具体复放与未执行边界均保留于各回执limitations.

## 工具库与交付

原卡先按round5-o1pld登记隔离, 原错误文字不再进入默认复用. 新卡保留原身份, 区分原候选的反证、单项式引理的局部修复、s=2余有限分类和未复审的既有分支. 新版已经过精确版本的独立数学回执并由纠错模块释放. 相关元数据、指针、研究理解和续接入口同步维护.

默认检索已实际检查: 78张可用、1张仍隔离; 99个历史版本、63条纠错事件保留. 新卡精确版本为`f7fb9661112adbc744be991b923e39b9bd6bedec4dbbb89ced1cbc36962e7430`, 默认结果不再返回旧错误版本; 原全阶正交系卡仍隔离. 新增一条绑定本版本的研究经验批注. [检索结果](../../research/artifacts/proof-audit-round5-20260921/default-query.json), [库状态](../../research/artifacts/proof-audit-round5-20260921/library-final.json). 既有被后续版本替代的旧回执警告仍保留, 已按实际新批准版本分类, 不删除历史来消除提示.

续接过程中, 卡片保存及修订事件完成后, 索引刷新进程退出143, 原因未确定. 核对持久日志为60个完整事件且无pending事务后, 确认原进程不存在, 将遗留写锁移至外部证据, 沿用同一修订创建审查包. 没有重复版本、跳过审查或手改批准. 随后原第五轮义务虽获释放, 新增的明确依赖仍继承round2-spectrum, 模块返回STILL_BLOCKED. 在不改卡片或证明字节的前提下, 新建该继承义务的修订和独立审查, 批准后再由原模块释放. 这保留了上游纠错向下游传播的门禁. 首次依赖审查因误读外部记忆而自报隔离失败, 返回INCOMPLETE; 保留回执并由另一新会话重审同一冻结包, 未使用受污染回执放行. 一次接收适配错误来自将工具调用外层信封传给期望实际result对象的接口; 改为无损取出result后接收, 原调用和错误说明保留. 这些是协调器恢复事件, 不是数学退回或插件源码变更.

[保护核验](../../research/artifacts/proof-audit-round5-20260921/protection-result.json)对6601个原跟踪文件执行哈希比较, 仅允许本轮明确活动文件变更; 134个原未跟踪文件和6项原脏文件保持原字节. canonical、旧run/审计/工具卡快照、旧数学论文/PDF、原脚本与45份旧Lean源均保留. 插件源码和安装缓存本轮未改.

发布只暂存精确清单, 核对实际Git blob与工作树SHA256. 新增局部Git属性保护本轮输入/日志和三份受哈希绑定的新源/卡片, 不改已有脏的根属性文件. [发布前清单](publication-manifest.json)属于本提交; 提交后按主仓库origin、xsoc1 fork顺序推送并以实际ls-remote核验. 最终提交和双远端结果保存在项目外`F:/tools/math-audit-round5-20260921/DELIVERY.json`, 避免把包含自身提交号的记录再写回同一提交. 如推送中断, 先核对该记录和实时远端再续接, 不重跑已完成研究.

一般非余有限O1'LD、s=3对应分类以及原3<s<7/2同族稠密性问题未在本轮解决.
