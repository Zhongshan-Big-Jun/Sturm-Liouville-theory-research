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
