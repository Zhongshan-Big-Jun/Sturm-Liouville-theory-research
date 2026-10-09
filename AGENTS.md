<!-- blueprint-project-layout:v1:start -->
# Blueprint v2.2 project layout (highest precedence)

- `blueprint-project.json` is the physical-layout authority.
- Canonical graph, inventory, submissions, and audit history are under `blueprint/`.
- Raw inputs and generated artifacts are under `research/`; disposable work is under `research/work/`.
- Do not run or copy project-local Python tools. Resolve the active plugin's `runtime/blueprintctl.py`, then run `ensure` once and use that gateway.
- Any legacy `statistics/.../tools/...` command in historical records is documentation only and is superseded by this block.
<!-- blueprint-project-layout:v1:end -->

# 研究协作与维护

## 目标与范围

维护 Sturm-Liouville 边值问题的两条长期研究线: 左定空间/正交系及特征值比值/谱隙极值. 区分既有文献, 合作者工作和项目推导. 当前问题编号, 范围, 依赖和未闭合项统一读 [research_map.md](research_map.md); 选证明读 [研究导航](docs/research-guide.md), 接手读 [RESUME](state/RESUME.md). 本文件不另维护逐轮数学状态.

## 每次进入与交付

1. 先读根及适用子目录 AGENTS.md/AGENTS.override.md, [物理布局](blueprint-project.json), [仓库说明](docs/repository-guide.md) 和 [归档规则](docs/archive-policy.md). 检查实际分支, HEAD 与工作树, 保留既有未提交/未跟踪内容.
2. 根据本次用户请求界定动作. 分析请求不授权编辑; 已完成阶段的派发/发布要求按当时范围读取. 本次明确指令优先于冲突的历史授权, 不自动重启旧任务或扩大提交范围.
3. 引用数学结果时读取实际陈述及依赖; 目录/状态标签/最新日期不能替代证明. 本地修改完成后按请求做相称验证, 如实报告失败和未执行项.
4. 每组连贯改动后在本文件留简短有日期的请求/决定/结果摘要, 详细具体对话与操作追加到 [state/AGENTS_SESSION_LOG.md](state/AGENTS_SESSION_LOG.md). 保持原历史前缀字节, 不为记录更新再递归记日志.
5. [RESUME](state/RESUME.md) 顶部只呈现当前接续, [current.json](state/current.json) 维持兼容摘要; ID, run, 预算与接收状态必须有实际来源. 无派发的维护任务不伪造 Q-/R- 身份.

## 数学与证据纪律

- 明确对象, 量词, 假设及非平凡推论. 不为闭合结果偷偷加假设, 弱化目标或省略情形. 创意路线可提出, 但标注为猜想/候选.
- 分开登记解析证明, 数值观察, 精确证书, 独立审查, 软件测试, 工具库接收, Blueprint 接收, Lean 和发布. STRICT 只适用于确切陈述及版本; NO_RETURN/超时不构成数学反例.
- 数值优化成功或绝对残差小不建立驻点; 有限样本不证明全参数符号/无限维结论. 证书需有覆盖域, 严格误差及计算到定理的桥.
- 实质研究修补沿现行插件使用作者之外的全新上下文审查, 冻结最小输入, 保存真实调用/完成回执及首次退回. 普通导航维护不制造数学审查/形式化回执.
- 工具卡保存与检索可用不等于自动验收. 错误纠正按原版 issue/version/review/release 机制, 不以手改状态或复制批准标签解除隔离. 格式适配失败记录真实原因.
- 文献与新颖性判断核对实际 primary source 和读取位置; 未找到先例不证明没有先例. 数学理解, 直觉和失败路线分析写在 [项目理解](docs/PROJECT_UNDERSTANDING.md), 保留人的批注, 不改成工作日志.
- 失败路线保留具体障碍, 有效部分和再次研究所需的新条件. 旧误判标为 superseded 并链接修正, 原记录不重写.

## 文件与工程方法

- 被 manifest/hash, 审查, checkpoint, 证书或复现程序绑定的工件保留原路径与字节. 编辑当前文档前检查路径与版本引用; 新版本不能继承旧审查覆盖. 原 byte snapshot 写入已有 [docs/history](docs/history/) 并记录原路径/哈希, 不覆盖旧快照.
- 清理依 [archive-policy](docs/archive-policy.md), 不按年代, mtime, scratch/build 名称或重复字节删除. 保留原始失败日志与编译证据. 日常导航不需复制全部台账, 不大规模移动物理布局.
- canonical 操作只走顶部 gateway; 历史项目内 Blueprint Python 不执行. 普通清点可用 shell/独立临时检查程序. 外部临时工具或仓库放 `F:/tools/`.
- 文档使用英文标点. 新代码用 tab 缩进, 多词函数 snake_case, 多词变量 PascalCase; 适用语言大括号独占行, if/for/while/switch 与左括号不留空格. C++ main 末三句为 cout << endl;, system("pause");, return 0;.
- 源与 PDF 按构建/版本证据核对, 不把旧 PDF 当成新证明阅读版. 不为导航整理重编全仓. [脚本导航](scripts/README.md) 是当前计算/证书/历史入口; 不执行旧一次性补丁来维护状态.
- 只在适用的提交/发布授权下精确暂存, 正常快进推 origin 再 fork, 并读回身份/字节. 历史“全上传”不扩大新的任务范围; 本轮后续“上传”授权仅覆盖本轮整理清单. 强推, 改写历史和破坏性清理另需明确授权.

## 2026-10-08 仓库入口与续接整理

用户最初要求直接完成本地整理, 以入口清晰, 职责明确, 状态一致为目标; 不改数学, 不扩研究, 不重构算法, 当时不提交或推送. 后续“上传”授权见下文. 起点 main/d311bb410cb5e425ac7f7ac4879a4decaa5f0540 已现场核实. 旧 PROJECT 的 n=1 状态原已修正, 未重复当作缺陷.

本次将首页改为读者介绍, 研究导航按数学问题接入 G2/全窗口删项/有限约束/整数替代系/有界谱尾, 脚本按用途置顶. 地图保留问题编号及依赖, PROJECT 只解释定位和文档职责, current.json 继续兼容原 v1 与现行模板字段. 根 AGENTS/RESUME 及入口原文存入 [原字节快照清单](docs/history/entry-snapshots-20261008.json), 历史决定和当轮授权按日期读取.

本轮实际通过462个本地链接/14个锚点, 9份原字节快照及19801个编辑范围外原路径保护, git diff --check通过; 库查询34项原阻断保持. 本地整理交付时未提交/推送; 后续授权另记. 版本绑定影响, 源/PDF对应及具体限制见 [本次详细记录](state/AGENTS_SESSION_LOG.md#2026-10-08-仓库入口与续接整理). 这次导航新版本没有新数学审查或接收; 冻结证明/证据, canonical, 卡片/索引, 人的批注及无关研究工作按起点保护.

## 历史决定的读取方式

[会话日志](state/AGENTS_SESSION_LOG.md) 保存完整具体请求及执行记录; [整理前根文件](docs/history/AGENTS.pre-organization-20261008.txt) 保存所有根文件历史正文和旧规则原字节. 路径按原根目录解释. 2026-09-09 的更早快照仍在日志中. 已结束轮次的审查/冻结/停步边界继续保护其工件, 当轮派发与发布动作不作为当前待办. 长期有效的证据分层, 字节保护及 origin-first 顺序保留在上文.


## 2026-10-08 本轮整理发布 (用户明确授权)

用户在本地整理与验证完成后要求“上传”, 授权提交并同步本轮23项入口/状态/历史快照与清单, 不纳入原KP-DET脏稿或134个原未跟踪文件. 发布前现场origin/fork main均为d311bb410cb5e425ac7f7ac4879a4decaa5f0540. 按精确清单暂存, 核对Git过滤后的blob与原字节快照, 正常快进推origin后fork并读回两边commit/tree及每项blob. 实际提交与推送结果以本机 [DELIVERY.json](<F:/tools/sl-repository-organize-20261008/publication/DELIVERY.json>) 和真实远端为准; 此处不预先宣称尚未完成的推送. 完整授权与操作追加在 [会话日志](state/AGENTS_SESSION_LOG.md#2026-10-08-本轮整理上传授权). 不新增数学审查/接收或重写历史批准.


## 2026-10-08 研究 Lean 与插件联合开发 (本地, 进行中)

用户明确授权同时修改研究工程与插件 lean-verify, 完成真实证明开发和相互验证; 保留四组件及原验证器, 不提交/推送/发布/全局安装/canonical 写入. 已核对研究 main/f3b78f4 与插件 codex/plugin-v2-implementation-20260909/9e0da0c, 保留 KP-DET 脏稿及原未跟踪文件. 原入口/状态字节见 [快照清单](docs/history/lean-joint-entry-snapshots-20261008.json).

本轮按主题扩展 lean-proof: 复区间 L2 共享基础, 一般 L2 二阶导数的 Krein 积分代表/迹及算子代表无关性, 有界可测密度的加权模型. 稳定数学引理由新 lean_develop.py 入口试验/反馈/修订/保存; 当前编译反馈不是最终验收. 常密度 DD 全正整数模态及多项式域/能量桥仍在组合和正式核验中. H2 弱定义等价, 自伴性/真幂域, 完备谱与开放 ND/G1 不据此宣称完成.

真实 SL 联调发现同前缀本地 import 的临时库遮蔽缺陷; 插件改用共享导入库并加入非 SL 回归. 同时修补 warm Python 载入代码与磁盘代码身份, Windows 按用户新增“将cmd隐式调用”采用隐藏子进程. 实际执行的是本轮冻结源码 F:/tools/lean-joint-20261008/plugin/source-freeze-v1, 不代表已安装 skill 已升级. 后续精确目标, 独立盲读/比对及旧全库构建将分开留证. 具体请求/命令/失败位置见 [会话日志](state/AGENTS_SESSION_LOG.md#2026-10-08-研究-lean-与插件联合开发).


## 2026-10-09 联合核验与独立退回后的修补

三个实际合取根共14项已由冻结v2新入口完成精确机器核验, job `sl-exact-roots-20261009` 为 SUCCEEDED/exit0, batch current=true, 每项 existing-verifier/evidence exact_root_passed=true. [真实汇总](research/artifacts/lean-development-20261008/verification/development-result.json). 独立审查另行保留: 盲读 APPROVED; 首次语义比对确认源码合同相符并批准常密度/一般范数桥, 但两项 Krein 的 actual_type 打印含省略符, 因证据缺项 CHANGES_REQUIRED. 不据机器成功提前报告语义验收.

软件v1首次退回两个 late-save/batch 缺陷, v2实际7项generic/17+12 portable/28 workflow/81 validator通过后, 新身份审查又在真实Lean中复现 output=project漏子目录源码及common epoch漏guard/schema两个缺陷, 再次CHANGES_REQUIRED. 已交作者修补冻结v3, 同时修长类型打印; v1/v2原冻结和负面回执不改写. 旧全库真实build FAILED/exit1, 原字节 B3GeneralAlternatingChebyshev_Scaffold.lean:56未闭合注释; 单独正式入口build成功. 本轮本地边界及旧53份SL源码保护继续有效. 实际当前接续见state/RESUME.md; 详细记录追加在会话日志.


### 2026-10-09 Lean 当前入口同步 (审查修补中)

本轮将 lean-proof/README.md, STATUS.md, LEMMA_INDEX.md 与 formalization_progress.md 的现行块同步为真实模型/三根范围及 v3 审查修补状态. 历史正文和原九份字节快照保留; 索引声明名称按实际源码与根证明核对. 旧连续 g 的矩湮灭没有提升为一般 L2 或完整真实幂域结论. 默认全库构建失败, SLVerified 构建成功, v2 三根机器通过及独立退回分别列出; 没有新增数学批准/接收.


## 2026-10-09 v3 冻结与真实联合重核验启动

针对真实独审退回, 冻结插件v3: 241文件, SOURCE-MANIFEST SHA256 518b3b386de997d14dcc4488f9f1e344d974e1f0125be32e5d9c65306a12bcf5, lean-verify2.1.2/manage与workflow2.0.2/rigorous2.0.1. 本次逐项检查冻结字节通过. 实际新入口启动 sl-exact-roots-v3-20261009, 使用原锁定Lean/mathlib, timeout600/job-timeout7200, 输出verification-v3, 命令隐藏运行. 同时作者在独立临时工程执行冻结版真实正负/便携/续接/validator; working smoke不是最终验收. 数学源码及预写expected types不改; targets只换3个输出指针并存原v2清单, 不覆盖旧机器证据. 新独审与最终核验仍待完成.


## 2026-10-09 联合 Lean 开发的本地最终增量

用户要求在研究及插件两个既有仓库实际构造证明、反馈修订及重新核验, 后续要求cmd隐式调用. 本轮增加10主题Lean模块及三个非空真实合取根(8/4/2), 实际L2 Krein域/原多项式桥/Green能量与任意可测正有界密度范数桥/全部常DD归一化解. 新lean_develop入口复用原反馈、精确验证、路线、workflow; 完成真实试写/修订/保存及根合成. 初轮v1回路、v3严格核验与最终v4同字节trial/save/status均留证, 30份v3/v4运行代码SHA相同, 不伪称旧测试重跑. 三根最终exact/current=true, 全新完整类型盲读/另人原文合同比对/软件修补分别APPROVED且经既有receiver接收; 原退回与失败不改写.

v4实跑开发11、便携21+12、workflow28及validate81通过; 原真实15为v3执行通过, manage87沿用先前相同源执行. 正式入口构建成功, 默认旧全库因原B3注释未闭合失败, 草稿入口未单独构建. 范围、开放连接、实际版本和重放见 [联调入口](research/artifacts/lean-development-20261008/README.md), 具体过程见 [会话日志](state/AGENTS_SESSION_LOG.md#2026-10-09-联合-lean-开发最终验收与续接). 逆向弱H2、完整幂域/自伴正性、完整及一般密度谱与后续问题链仍开放. 原工作/冻结证据/canonical保护, 本轮未提交/推送/安装/接收或发布.


本轮最终维护校验实跑通过: 16份研究源码/配置配对, 47个新增/当前链接及2个锚点, 精确范围git diff --check和插件diff检查. 原53份SL及135捕获未跟踪条目(134原文件加本轮锁), 原日志/AGENTS前缀、KP-DET/插件旧dirty、canonical/inventory均保护. 原始输出见 [final-validation.json](<F:/tools/lean-joint-20261008/final-validation.json>); 此检查不构成新内核重放或发布.


## 2026-10-09 manage 问题知识复用改进 (本地, 验证中)

用户要求实际改进既有 manage 的检索/条件展示/经验复用/知识包, 与真实 SL 及前轮 Lean 成果联调. 本轮只改相关插件源码与研究非冻结元数据/生成区域, 不提交/推送/发布/全局安装/canonical 写入, cmd 隐式调用偏好继续有效. 起点 main/f3b78f4 与插件 codex/plugin-v2-implementation-20260909/9e0da0c 已核实; 前轮 Lean 已完成状态及原 dirty/冻结回执保留.

当前扩展原 query/read/index/compare, 增加有范围的 context 和显式选中 Lean 收据重查. 实数/复数、有限/无限维、固定/一致及 Sobolev/算子幂域由原文和显式字段保留, 词匹配不作假设蕴含证明. 实际新增两条可复用路线经验与 weighted-DD 局部 Lean 候选卡, 原工具隔离不因新卡登记解除. 人的理解页原文保留, 只追加生成区域. [入口原字节快照](docs/history/manage-context-entry-snapshots-20261009.json) 与 [本轮具体记录](state/AGENTS_SESSION_LOG.md#2026-10-09-manage-问题知识复用改进) 保留版本边界. 冻结测试、真实五问和新上下文独审尚在完成, 不据开发中结果宣称最终验收.

### 2026-10-09 首次 manage 独审退回与实跑 Lean 消费

冻结v3已完成五问及108便携通过/1Q9跳过, 源仓库Q9另实跑通过, 库7项/gateway/validator81通过. 两个实际fork_turns=none审查分别退回旧条件上下文计分和路径别名/隔离关系依据旁路, 原报告与native完成已由原receiver接收为CHANGES_REQUIRED. 已修补并通过26项新行为检查, 新冻结和独审接续中. 选中weighted-DD真实保存收据已通过v3新入口调用原lean-verify重查: current/exact=true, 语义身份重查通过; 这不是新的内核编译或库/canonical接收. 负面回执及具体源码边界见本轮入口与会话日志.


## 2026-10-09 manage 独立退回与 v5 修补

真实 v3 独审退回继承条件上下文命中、等价引用路径及关系依据门禁三处; v4 全新两人确认三处修正, 又独立复现正文单词命中被泛化上下文挤掉及 warm Python 将新磁盘源码误记为旧代码生产者. 原始 v3/v4 packet、完整 native FINAL_ANSWER、receiver 负面回执在 F:/tools/manage-context-20261009/review-project 保留, 不覆盖为批准.

当前 v5 按实际查询词、目标词、纯上下文分层选择, 在 Python 载入时绑定源码/版本并在生成与导出重查, 源更新要求新进程. 实际28项 context 回归通过; 冻结244文件 SHA3b06bac8d04ff29048a1cdd7d34e767c834d24b3b8ea7b7335d2b459f5e73b8e, manage2.1.0, 便携115项为114通过/1可选Q9跳过, 源仓库Q9另实跑通过, 库7项/gateway/validate81通过. 新原生独审 /root/manage_software_review_v5 与 /root/manage_forward_review_v5 已实际 fork_turns=none 派发, 完成结果待后续追加. 五问同一12卡语料重跑, 不把旧检索已有正确命中归功于新增能力.


## 2026-10-09 manage 捕获来源门禁修补 (v6)

fresh /root/manage_forward_review_v5 对所供五问及同语料增量 APPROVED, 限定研究复用而非重批证明. 独立 /root/manage_software_review_v5 又复现 source_id 不查捕获组成文件的 P1 旁路并 CHANGES_REQUIRED, 已由原 receiver 接收完整真实回执, v5 不作为最终软件批准. v6 将 source.json/raw.bin/text.txt 的精确实时门禁聚合到 source_id, 当前比较/理解页、关系/影响与导出一致; 原 source_id/捕获字节/纠错 release 协议不改.

29项 context 及最终冻结116项实际通过(115通过/1可选Q9跳过); 源仓库Q9另执行通过, 库7/gateway/validate81通过. 测试最初将三个组成文件案例用相同原文字节串联, 第三案因之前 raw 隔离正确拦截而失败; 保留原失败log, 用不同字节区分三案并另加同字节新捕获ID不可逃逸检查, 没有弱化门禁. 冻结v6 244文件 SHA d0bf6ee821769d5050d74faf8277a7af9209bdf49f98db6f3c8459afef4e7764. fresh /root/manage_software_review_v6 的原生最小包10项输入已实际派发, 最终结果待后续追加. SL原文/12卡语料不变, v6五问重跑与v5取回相同材料, 原34项门禁阻断保留.


## 2026-10-09 manage 捕获标题别名修补 (v7, 独审中)

fresh /root/manage_software_review_v6 确认三份捕获文件各自门禁修补, 又实际复现仅改标题产生新 source_id 可绕过旧 source.json 隔离, 因而 CHANGES_REQUIRED. 原完整负面 native 完成及 receiver 回执保留. v7 以原 URL/version/raw/text 的精确四元组查已登记元数据版本快照, 对 source_id 和等价 source.json 路径统一门禁; 标题/阅读标注不解除旧义务, 不同来源或版本的元数据不合并. 原 source_id 计算、捕获字节及 release 协议不变.

30项 context 实际通过, 冻结244文件 SHA 2f7a4740dcb7bc9a78b19c0b8318b636524b587c055218d916923d2c103ce049; 117项便携为116通过/1可选Q9跳过, 源仓库Q9另实跑通过, 库7/gateway/validate81通过. 同一12卡/11原文五问已用v7重跑; 主库原34项阻断、历史替代及默认Lean未知实查通过. 实际 fork_turns=none 派发 /root/manage_software_review_v7, 原生最小包11项输入, 当前软件最终结果待完成; v5五问正向批准的版本/范围另保留. 本轮仍只本地, 原数学/冻结证据不改.


## 2026-10-09 manage 双重选择与登记身份修补 (v8, 独审中)

fresh /root/manage_software_review_v7 确认捕获标题/路径与耐久快照修补, 又实际退回两项: path优先使source_id聚合门禁被压制; 元数据正常登记后共同隐式文件名source被误作工具身份. 完整negative native完成及原receiver回执保留. v8对path/source_id独立绑定并拒绝矛盾, 对捕获元数据按原URL/version/raw/text投影身份, 不改旧登记字节或release义务. 相同捕获别名及其精确依赖仍受影响, 不同来源/版本正常登记后及其消费者不再误合并.

最终冻结244文件 SHA872931bf222dc54915d80ffd412c8a98d3d1a987781c05e71847257fa0de5aa3, manage2.1.0. 实际119项便携=118通过+1缺材料Q9跳过, 含32项context; source Q9另实跑通过, 库7/gateway/validate81通过. 本轮两项新回归覆原/标题别名的source_id+自身raw/text、错误sha/矛盾路径、比较读回/理解页/关系impact/导出, 以及登记前后不同URL/version、同捕获别名依赖及旧记录字节. 五问v8同原语料已重跑. fresh /root/manage_software_review_v8 实际fork_turns=none派发, 原生12项输入, 当前最终软件结果仍待完成; v5正向批准限其当时范围. v7全量保护检查已通过, 本轮新修补后的最终保护另核对. 没有新数学证明、全局安装/发布或canonical/原工具release.


## 2026-10-09 manage 捕获成员与首次纠错导出修补 (v11, 独审中)

作者实际复现v8缓存identity投影字段可压制已知隔离, v9改由绑定材料重建. fresh v8独审随后真实退回两项: path-only raw/text逃逸捕获metadata/别名义务; 首个issue未改变预登记catalog/自定义index时旧知识包仍可导出reuse/impact. 完整negative native回执已由原receiver接收, 不以测试通过解除退回. 当前v11统一识别三个捕获成员路径, 绑定纠错状态的存在/缺失及版本, 导出重查来源与关系许可; 旧导出与纠错协议保持原字节. 两项新回归实跑通过, 新冻结244项SHA9312ce7ae3abb217a7808df9e348c96289b874efe9bdcea5e28e73dfb8ddc088. full测试/最终软件独审正在完成; v9/v10的真实派发已中止且没有完成/批准, 不能据此宣称验收.


## 2026-10-09 manage 当前声明与耐久身份修补 (v13, 独审中)

fresh v11独审完整CHANGES_REQUIRED已由原receiver接收: cache.tool_id覆盖当前声明, 正常reindex还会登记错误耐久ID, 随后无缓存read仍放行. 当前读取/增量刷新以源码显式tool_id/slug优先; live gate另从精确Markdown快照同时保留原耐久ID与源码声明ID的各项义务, 不改旧绑定字节或自动release. 缓存计算字段均不能替代该投影; 仅索引声明的旧ID兼容继续保留. 三项针对性回归4.566s通过, 冻结v13为244项SHA3a18b98aefb24764b4d038aa705a1787316cc7a82c6543d1d5894dd9b5087f74. 全122项及新上下文软件独审正在完成, v12只有作者中间冻结、没有审查派发/完成. 本条不作提前验收; 数学范围/本地边界与原34项隔离不变.


## 2026-10-09 manage 问题知识复用本地增量完成

manage2.1.0最终冻结v13与工作树244文件逐字节配对; 实际便携122项为121通过/1缺材料Q9跳过, source Q9另实跑通过, 库7/gateway/validate81通过. 同12卡/11原文五问、原34项阻断、精确历史替代导航和默认Lean未知实查. fresh五问正向v5及最终软件v13分别APPROVED并经原receiver接收, 所审版本/范围分开, v3-v8/v11真实退回及v9/v10未完成中止保留. [实际结果与重放](research/artifacts/manage-context-20261009/README.md) 为当前入口. 最终源码、原文、测试、真实回执与未做检查见SOURCE-PAIRING; 未将软件批准当新数学证明/完整形式化. 只本地, 未提交/推送/发布/全局安装/canonical或解除原纠错义务. 已有续接与理解页保留人的原字节和开放连接; 最终保护结果单独链接.


本轮最终保护检查实跑通过: 研究21782份、插件1233份起点文件逐项SHA核对, 原文件无丢失及范围外变化; 原正文/人的前缀与续接历史字节、主index、唯一review适配器、canonical/inventory和Git HEAD/分支/暂存均保持. 当前244份源码与v13冻结配对. [实际保护结果](<F:/tools/manage-context-20261009/preservation-final-v13.json>) 单列; 最后追加的说明另做小范围字节/链接检查, 不据此增加数学批准或发布.


## 2026-10-09 最新插件与研究仓库上传授权

用户在Lean和manage两项本地验收后明确要求"上传推送最新版本插件与研究仓库", 本轮授权覆盖两项联合增量, 精确提交并按origin后fork正常快进推送. 原KP-DET及原未跟踪工作不纳入. 18份超限JSON保持原路径/原字节, 按SHA去重gzip发布并附完整还原映射和拒绝覆盖的还原器; 不截短或改写旧机器/语义证据. 源码与回执引用副本、README和续接指针同步, 不修改全局安装或canonical、不自动续跑研究. [实际打包与范围](research/artifacts/lean-development-20261008/PUBLICATION.md) 保留命令. 精确提交/推送/远端读回以F:/tools/joint-publication-20261009/DELIVERY.json和真实远端为准; 本条不预先宣称发布完成.
