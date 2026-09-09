# 成果仓库整理记录

日期: 2026-09-09. 状态: 已在工作树完成, 未 commit/push.

作用域仅为 Sturm-Liouville-theory-research 本体. 没有进入或修改 `_xsoc1_work/`, 没有启动子 agent, 没有接收 canonical 数学变更. 插件 2.0 的实现与发布由并行任务负责; 本报告只说明成果仓库部分.

## 交付内容

| 文件 | 改动 |
| --- | --- |
| [中文首页](../../README.md), [English README](../../README_EN.md) | 明确本仓库是研究插件的使用成果仓库. 区分文献, 合作者贡献与人机推导; 以研究方向, 导航, 有范围的成果, 开放问题和形式化状态组织内容 |
| [研究导航](../../docs/research-guide.md) | 把旧首页中的详细证明入口整理到专页, 说明固定 n 根计数的后续结果, KP-DET 的最新分支范围及 G2 历史状态差异 |
| [项目理解](../../docs/PROJECT_UNDERSTANDING.md) | 人可以直接修改的研究解释与批注入口. 从既有工具卡和 run 提炼成功/失败路线经验, 标明再检视条件与待检验的解释 |
| [目录与复现](../../docs/repository-guide.md), [脚本导航](../../scripts/README.md) | 说明目录职责, 实际证据等级及文档/Lean 的复现范围, 保留原工件路径 |
| [AGENTS](../../AGENTS.md), [会话归档](../../state/AGENTS_SESSION_LOG.md) | 根说明从 40,054 bytes 缩短到约 4.6 KB; 旧根文件全文按原字节追加到会话归档, 归档原有前缀字节保持不变 |
| [.gitignore](../../.gitignore), [归档规则](../../docs/archive-policy.md) | 只忽略 docs/build 中的可再生中间物, PDF 可见. 保留哈希绑定日志的例外; 旧 mtime 归档程序不作为当前入口 |

中文首页从 11,360 bytes 缩短到 5,296 bytes, 英文从 11,924 bytes 缩短到 6,204 bytes. 完整旧文分别保存在 [中文快照](../../docs/history/README.pre-v2.zh.txt) 与 [英文快照](../../docs/history/README.pre-v2.en.txt), SHA256 与整理前完全相等. 旧首页中的路径按原仓库根解释.

## 数学状态的依据

- 本地 [sequence-26][kp-whiteboard] 及对应接受包: 完整约束下 `0<c<=2/3` 的 KP-DET 分支经审计 PASS; P20-P21 是经审计的精确求积约化. 本地主 run 的 Q9 仍为 OPEN. P1-P4 的 pivot/phase 部分已进入 canonical; 后续接受包与 canonical 接收分开登记.
- 插件公开 [Q9 对照报告][q9] 另有三份完整证明及匿名外审 PASS, 报告同时明确未做 Lean 形式化和主项目集成. 导航把它列为可接续的外部成果, 没有升级主项目全局状态.
- [M3 工具说明](../../tools/m3-largeR-closure.md) 限定为 n=2 对称 INF large-R 有限非零内部 chart. 旧 staged mass 的 odd/log 障碍保留为 SUPERSEDED 历史.
- 特定 G2 增补与较新的 chart 外 all-R 状态表述不一致, 本轮没有重新审计以统一其定义和量词. 首页没有声称完整 G1'/G2 或全局 n>=2 结论已闭合.
- [Lean 脚手架登记](../../lean-proof/formalization_progress.md) 与源码表明存在 `sorry` 和条件化接口. 首页撤下旧的全库零命中和构建 job 数, 不把历史日志当作当前整个工程的形式化结论.

以上是文档整理与来源核对, 本轮没有产生新数学证明或新的 Lean 验证裁决.

## 删除与保留

共删除 125 个文件, 1,199,252 bytes, 包括 10 个过时维护程序和 115 个可再生 TeX 中间物. 每一项的完整路径, 删除理由, 原始 SHA256, 字节数及基线 Git blob 均在 [cleanup-manifest.json](cleanup-manifest.json). 清单先生成并完成引用与哈希核对, 再逐项执行删除, 没有按目录批量删除研究内容.

| 删除的维护程序 | 已核对的理由 |
| --- | --- |
| misc/_decode_tail.py | 针对 AGENTS 旧固定偏移的编码诊断, 当前目标为有效 UTF-8 |
| misc/_find_bad_byte.py | 旧逐字节诊断会把正常 UTF-8 续字节当作错误, 无调用或证据绑定 |
| misc/_find_bad2.py | 已完成编码修复的一次性诊断, 无调用或证据绑定 |
| misc/_find_bad3.py | 已完成编码修复的一次性诊断, 无调用或证据绑定 |
| misc/_locate_corruption.py | 针对旧 AGENTS 编码损坏的定位程序, 无调用或证据绑定 |
| misc/_repair_agents.py | 旧 GB18030 尾部修补器, 当前目标已可按 UTF-8 解码 |
| misc/_repair_tools.py | 旧工具卡/索引编码修补器, 两个目标均已可按 UTF-8 解码 |
| misc/_patch_readme.py | 旧固定锚点插入器, 所有目标工具卡和索引条目已存在 |
| misc/_patch_readme_well.py | 旧阱族卡片插入器, 卡片及索引条目已存在 |
| scripts/_ck.py | 一次性写入旧 checkpoint 的程序, 内嵌文本与保留 checkpoint 在换行归一化后相同 |

删除前检索了本体基线内每个可按 UTF-8 解码的非二进制文件, 按完整路径, 文件名和至少 16 位 SHA256 前缀查找引用, 并归一化 Windows 路径与 TeX 转义. 生成物相互间的编译引用不作为外部依赖. 每个已删 TeX 中间物都核对了同名 TeX 源和仍可读取的 PDF. 扫描没有进入独立插件仓库.

删除后又以完整单词检索了 10 个已退役程序的模块名, 覆盖不带 `.py` 的 import/调用形式, 在保留内容中未找到引用. 清理报告自身与历史首页快照不计入调用检查.

以下内容保留:

- **所有研究数学实现.** 14 组同字节代码副本全部保持原状, 详见 [retained-duplicates.json](retained-duplicates.json). 其中 DensBC 的 6 组同时承担 scripts 引用路径与 run 复现包职责. 冻结 scaffold 和 benchmark harness 副本也保留.
- **证据日志.** `docs/build/SL_gap_n1_O3a_phase_rigidity_proof.log` 的 SHA256 为 `c9be856046c73dca6f493e62e338895321c490baa0e7ff2c1f3a39ec8c614b1b`, 与旧复现清单绑定完全相同. 另保留旧迁移记录引用的 ratio 中间物, stability 通配记录涉及的文件, 以及来源不够明确的诊断日志. 逐项理由在 cleanup manifest 的 `retain_candidates`.
- **独有研究进展与 scratch.** `scratch_1d_numeric.py`, `scratch_1d_numeric2.py`, Route 09-11, sequence-21..26, 接受包, 审计与 checkpoint 字节不变. 其他未证实可安全移除的一次性历史程序也保留.
- **全部 TeX 与 PDF.** 包括此前未跟踪的 Hs PDF 和旧路径下的 PDF. 本次没有重编译或覆盖可读研究文档.

## 迁移与恢复位置

| 原内容 | 新位置 | 保留检查 |
| --- | --- | --- |
| 整理前 README.md | docs/history/README.pre-v2.zh.txt | 原始 SHA256 `fc50197a15bafc9c8513db74d3ee4a06505955c46542ecdbba8f142e92918dd1` |
| 整理前 README_EN.md | docs/history/README.pre-v2.en.txt | 原始 SHA256 `4a266b9bbde80191bfa60af9de2b603ed7a1a41b7c264cb8f17aece46a5c496c` |
| 整理前根 AGENTS.md | state/AGENTS_SESSION_LOG.md 的 pre-v2-agents-snapshot 段 | 该段原始 SHA256 `5431f472841ae55a7dbf9314385cd329cce2af8b89d236c79a4e67a79d610a61` |

基线 Git HEAD 为 `cae1b2dd6e0a9a27078d5de27c433ed72bf94168`. 已删除的已跟踪文件可从该 Git 版本取回. 清单同时记录工作树原始 SHA256; Git blob 与工作树可能有换行差异, 不把二者的字节哈希混同.

原有 68 项工作树内容在本轮开始前已备份到维护主机的 `F:\tools\math-plugin-v2-20260909\math-dirty-baseline.tar.gz` 和对应 JSON. 已删除的 7 个原有未提交 TeX 中间物也在该备份中. [baseline.json](baseline.json) 保存本体 4,523 个文件的原始 SHA256, 并复核了这 68 项全部与备份清单一致.

## 验证结果

[integrity-checks.json](integrity-checks.json) 记录逐项结果:

- 4,523 个基线文件中, 4,392 个原字节不变, 6 个在授权文档范围内修改, 125 个按清单删除, 意外变更为 0.
- 原有 68 项中, 56 项原字节不变, 5 项是授权修改的首页/AGENTS/ignore/会话记录, 7 项是已备份且可再生的中间物.
- `blueprint/` 18 个文件, `research/` 301 个文件, `runs/` 1,759 个文件, 合作者核验包 305 个文件, `lean-proof/` 53 个文件, `tools/` 82 个文件全部原字节不变. 全部 TeX 和 PDF 原字节不变.
- 两份旧首页快照与旧 AGENTS 快照的原始哈希一致. 会话归档的原有前缀原字节不变.
- 当前安装插件 gateway 的 canonical 校验 exit 0: 11 nodes, 13 edges, 4 inventory rows, 依赖类型/无环性/inventory links 有效. 这是结构与证据校验, 不替代独立数学审计. 实际命令及结果见 [blueprint-validation.json](blueprint-validation.json).
- 生成物 ignore 测试覆盖 8 类中间物; PDF 与绑定日志均未被忽略. 导航链接和当前文档格式检查记录在 [document-checks.json](document-checks.json).
- 文档目录的 61 份 PDF 全部通过 pypdf 严格解析, 包括每页尺寸与内容流读取. 文件字节另由哈希核对, 本项不表示重新进行视觉或数学审计. 结果见 [pdf-checks.json](pdf-checks.json).

本轮使用已有有效的 gateway 绑定, 没有重写运行时绑定或 canonical. 已保存的源码和审计记录没有因文档整理而升级状态.

## 中断后续接: 导航的发布依赖

本节只补充版本依赖与验证边界. 导航仍待协调器提交和推送. 上述 `document-checks.json`, `integrity-checks.json` 与 `worktree-status.txt` 保留原清理阶段的检查快照; 本次更新后的精确路径, SHA256, 依赖边和检查结果另存于 [publication-dependencies.json](publication-dependencies.json).

原链接检查只确认本机文件存在, 不能保证新 checkout 包含链接目标. 保留现有 sequence-26 导航时, 最小新增证据集合为 12 个既有未跟踪文件: sequence-26 白板 1 个, Route 09 接受包和重试审计 3 个, Route 10 直接证明, 首次审计, 修补, 复审及接受包 7 个, Route 11 无返回核对记录 1 个. 清单逐项记录原始 SHA256, 原 4,523 项基线及 dirty 备份的一致性, 以及引入该文件的来源. 这是把已有不可变证据纳入版本, 没有新证明, 新审计或 canonical 接收.

Route 10 的首次审计为 `REPAIRABLE_GAP`, 不能只发布最后的 `PASS` 或接受摘要. 必须保留最初的缺口, `e_binding_repair.md`, 窄范围复审的 JSON/Markdown 及直接证明. 修补所绑定的 Route 08 `prover_result.md` 和对应审计已经跟踪, 其现有 Git blob 满足所声明的 SHA256. Route 09 的 W14/W15 原证明, `whiteboard-20.md`, 早期接受包和审计也已跟踪, 不需要重复暂存. 白板列出的 Route 11 记录用于支持 `NO_RETURN` 的状态说明, 不作为数学结果.

依赖检查递归读取接受包, 审计 JSON, 文本中的 SHA256, run/route manifest, 已引用的 checkpoint/state/receipt 和上游证据. 路径分别按文档目录, run, 隔离 workspace 及 `blueprint-project.json` 的 research artifact root 解析. 新导航的相对链接按拟提交集合验证: 现有 HEAD 文件减去清单中的已跟踪删除项, 再叠加获准文档和这 12 个原始证据. 未暂存的其他工作树内容不能用来填补缺失文件.

本次共读取 157 个递归依赖文件, 核对 456 组唯一文件哈希绑定. Route 09/10 范围内的 57 组明确绑定全部精确匹配; 200 次当前导航相对链接检查全部通过. 12 个待纳入证据共 52,754 bytes, 均与原始基线和 dirty 备份清单一致, Git 现有属性不会在纳入时改写其字节. 原 4,523 项基线仍为 4,392 unchanged, 6 authorized document edits, 125 listed deletions, 0 unexpected changes; 本次续接没有扩大数学或代码改动范围.

递归读取也暴露了既有历史限制. 旧 Route 01/02 及早期 benchmark manifest 绑定过当时的 AGENTS 或路线登记, 当前 HEAD 的这些管理文件已演化. 旧 M3 输入中的 5 个原始 SHA256 对应 CRLF 字节, 当前 Git blob 为 LF, 逐项换行对照可以识别但不等于原始字节匹配. 另有历史 Blueprint/inventory 快照哈希及主机外插件路径. 清单分别保留这些检查结果, 不把本次发布依赖检查称为整个历史研究包的全量哈希复现 PASS, 不改写任何旧 manifest 或数学文件. Route 09/10 新增包本身的明确文件绑定均按精确字节核对.

sequence-21..25 白板和 sequence-21..26 的 closure/checkpoint/state, 以及 resume_receipt-20..25 不在这组导航及其递归文件依赖中. 它们作为已有恢复工作留在本机, 本次不宣称发布了 sequence-26 的完整恢复包. Hs 的未跟踪 PDF 和两个 scratch 同样不需要纳入导航发布. 所有这些文件及无关 CRLF dirty 保持原字节和未暂存状态.

协调器精确暂存集见清单的 `coordinator_stage_set`: 6 个已跟踪文档修改, 16 个新文档/报告, 12 个既有证据, 2 个局部归档属性文件, 121 个已跟踪删除, 合计 157 个路径. 首次依赖检查的 155 项结果保留在清单的历史检查记录中. 125 项清理中另有 4 个原本未跟踪的生成物, 已不存在且没有可暂存的删除; 清单单独列明. 只按该路径集处理, 不使用全仓 `git add -A`. 两个属性文件随归档一起纳入, 原根 .gitattributes 保持用户原有 dirty 字节; HEAD 和 index 保持原样.

### 追加检查: 归档提交字节

用户指出完整会话日志和旧首页快照也必须经过 Git clean 转换检查. 原检查证明了工作树字节和 12 个研究证据的过滤保真, 没有验证归档在 Windows Git 下的提交字节. 当前 WSL Git 默认不转换, 但实际 Windows Git 配置 `D:/Git/etc/gitconfig` 设置 `core.autocrlf=true`, 会把这 3 个归档中的 CRLF 改为 LF. `core.autocrlf=input` 也会改写它们.

新增 `docs/history/.gitattributes` 只给 `/README.pre-v2.zh.txt` 和 `/README.pre-v2.en.txt` 设置 `-text`; `state/.gitattributes` 只给 `/AGENTS_SESSION_LOG.md` 设置 `-text`. 不使用目录通配符, 不修改原根属性, 不覆盖旧归档字节. 完整会话日志只在末尾追加本次用户要求, 方法和验证说明, 追加前的整个前缀原字节保持.

验证在仓库外临时对象目录使用实际 `git hash-object -w --path` 生成 clean 后的 blob, 再以 `git show --no-ext-diff --no-textconv` 读取全部内容, 对照原始字节及 SHA256. 对 WSL 当前默认以及 autocrlf=true/input/false 四种配置, 3 个归档的 12 次完整 blob 对照均一致; 原生 Windows Git 得到相同的 blob ID. 两份旧 README 的原始 SHA256 不变. 完整日志按最终追加后的全部字节验证, 不是只验证其历史前缀.

发布依赖清单保存过滤前后的 blob ID, 原始与过滤后 SHA256, 原生 Windows 配置, 属性作用域检查及协调器前提. 原清理阶段的 JSON 报告保持不变; 首轮 155 项发布检查另标为历史. 当前 157 项集合可供协调器提交, 但仍保留前述历史研究包的 11 组原始哈希限制, 不升级为数学审计或全历史复现结论. 本轮未 stage/commit/push, 数学, 源码, TeX 与 PDF 原字节未变.

## 验证命令与工作树

从成果仓库根执行的主要命令:

```bash
python3 -B /mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/manage-math-research-program/1.8.1/runtime/blueprintctl.py validate --project .
git diff --check -- README.md README_EN.md AGENTS.md .gitignore docs/archive-policy.md
git -c core.whitespace=cr-at-eol diff --check -- state/AGENTS_SESSION_LOG.md
git check-ignore --no-index -- docs/build/cleanup-probe.aux docs/build/cleanup-probe.pdf docs/build/SL_gap_n1_O3a_phase_rigidity_proof.log
git status --porcelain=v1 -uall
```

哈希与链接核对使用本轮独立的 Python inline 检查, 没有执行项目本地 Python 工具. 哈希逐项对照 baseline, 只豁免上面列出的 6 个授权文档和明确删除清单; 其余文件缺失或哈希改变即失败.

会话归档的旧前缀含 CRLF, 按原字节保留. 使用 `cr-at-eol` 后仍有原第 1465 行的一个既有尾空格提示; 它在原始基线中已经存在, 没有为了通过格式检查改写历史字节. 当前重写的首页, 根 AGENTS, ignore 和归档规则通过普通 `git diff --check`.

HEAD 与分支保持原样. 最后工作树清单见 [worktree-status.txt](worktree-status.txt); 原有研究修改仍待协调器按整体任务处理. 本 agent 没有 commit, push 或修改 Git 远程.

[kp-whiteboard]: ../../research/runs/R-20260831T020156Z-g1p-kpdet/workspace/runs/rigorous-open-math-research/R-20260831T020156Z-g1p-kpdet/whiteboard-26.md
[q9]: https://github.com/xsoc1/rigorous-open-math-research/blob/f95627ca1b44aeb75692a5814e20050b0e6a40cb/benchmarks/codex-20260908-q9/CONCLUSIONS.md
