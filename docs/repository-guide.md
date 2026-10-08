# 目录, 文档与复现

[中文首页](../README.md) | [English](../README_EN.md) | [数学阅读导航](research-guide.md) | [当前续接](../state/RESUME.md)

## 文档与目录职责

首页负责介绍, [research_map](../research_map.md) 负责当前问题/结果/缺口, [研究导航](research-guide.md) 负责选择证明和前置材料. [PROJECT](../PROJECT.md) 说明定位, [AGENTS](../AGENTS.md) 说明工作规则, [RESUME](../state/RESUME.md)/[current.json](../state/current.json) 承担人工/机器续接; [会话日志](../state/AGENTS_SESSION_LOG.md) 保存详细过程. [项目理解](PROJECT_UNDERSTANDING.md) 保留数学理解和人的批注, 不作另一份状态台账.

| 位置 | 内容与使用者 |
| --- | --- |
| [docs](./) | 活动数学源文稿, 既有 PDF, 同目录 build 历史镜像; 按版本证据选择阅读版 |
| [tools](../tools/README.md), `knowledge/tools/`, [research/library](../research/library/) | 当前卡片, 旧管理布局空目录, 版本/原文/批注/审查纠错库; [工具说明](../tools/README.md) 给消费者, 三者不合并 |
| [index](../index/) | 文献/任务/run/工件及工具的派生或历史索引; 旧记录不等于当前运行中 |
| [blueprint](../blueprint/) | canonical 图, inventory, submissions, 审查和接收历史 |
| [research/artifacts](../research/artifacts/), [research/runs](../research/runs/), [runs](../runs/) | 活动/冻结工件及不同布局时期的 run; 各路径可能被证据精确绑定 |
| [scripts](../scripts/README.md), [misc](../misc/) | 数值诊断, 有理证书, 历史实现; 当前/退役用途见脚本导航 |
| [lean-proof](../lean-proof/STATUS.md) | 形式化片段, 条件接口及脚手架; 对照具体根声明和依赖 |
| [papers](../papers/), [literature](../literature/), [research_cache](../research_cache/) | 来源及读取资料, 保留版本/许可/实际读取范围 |
| [collaborator_min_direction_verification](../collaborator_min_direction_verification/) | 合作者最小方向结果的核验上下文 |
| [state](../state/), [reports](../reports/), [docs/history](history/) | 续接/历史状态, 实际交付/失败记录, 未覆盖的原字节快照 |

[blueprint-project.json](../blueprint-project.json) 是物理布局依据. 本轮保留所有目录与研究工件原路径, 不迁移 docs/runs/research/blueprint.

## 源文件与 PDF 对应

同名或修改时间不能证明源/PDF一致. 下表用实际文件哈希和现存构建记录核对; 没有重新编译或进行本轮 PDF 版面验收.

| 当前源/主题 | 阅读版与对应依据 | 限制 |
| --- | --- | --- |
| [n>=2 局部框架源](SL_gap_nge2_symmetry_local_proof.tex) | [根 PDF](SL_gap_nge2_symmetry_local_proof.pdf) 与 build PDF 字节相同; 源和两 PDF 均匹配 [R14 构建绑定](../research/artifacts/proof-audit-round14-20261004/pdf-verification.json), 16 页 | 含 G2 活动框架补证; 原完整 [G2 Markdown](SL_G2_compactness_proof.md) 无独立同名 PDF |
| [综述源](SL_spectral_topics_summary.tex) | [根 PDF](SL_spectral_topics_summary.pdf) 匹配 R15 发布清单与 [23 页最终阅读版记录](../research/artifacts/proof-audit-round15-20261005/compilation/visual-check.json); 源匹配 R15 最终解析输入 | build PDF 仍匹配 R14 的 22 页旧版, 与根 PDF 不同. 综述不是 R16 两项完整证明的 PDF |
| [A12 余有限源](SL_cofinite_all_orders.tex) | [根 PDF](SL_cofinite_all_orders.pdf), [R11 报告](../reports/proof-audit-round11-20260926/REPORT.md) 的既有阅读版 | A11 任意保留集推广另读 R15 完整 Markdown, 不以此 PDF 覆盖推广 |
| [Hc2 删项](SL_H2_arbitrary_deletion_proof.md), [全窗口删项/有限约束](SL_full_window_deletions_and_finite_constraints.md) | 当前完整证明是 Markdown, 未找到独立同名 TeX/PDF | 根综述 PDF 可作概览, 不能替代完整证明 |
| [整数阶 Riesz](SL_integer_left_definite_riesz_systems.md), [有界方向谱尾](SL_bounded_direction_spectral_tail.md) | 当前完整证明是 Markdown; R16 明记没有 TeX/PDF 编译 | 没有独立同名 PDF, 不用旧阅读版冒充 |
| 比值, 固定 n 候选, n=1 主证明和 INF 极限 | 根 PDF 与 build PDF 现场哈希均不同; 推荐从 [主题导航](research-guide.md) 的活动 TeX 与审查范围进入 | 本轮未逐一证明这些不同阅读版与现行源同步, 不按文件名/时间猜测 |
| [Hs 旧稿](SL_hs_orthogonal_systems_proof.tex) | 根与 build 的同名 PDF 字节相同, build 副本起点为未跟踪文件 | 一致的两个 PDF 不证明与源同步或全阶结论成立; 配合 A7 域障碍读取, 原未跟踪副本保留 |

## 状态接口与历史程序

`state/current.json` 继续作为 v1 机器摘要. 已安装 manage 插件的 assets/current-state.template.json 定义数组身份, lifecycle_state, current_objective, latest_checkpoint_path 与 updated_at; init_project.py 生成此文件, validate_project.py 检查存在性/project_id 和 checkpoint 提示. 本项目还含旧别名 project_lifecycle_state/objective/latest_checkpoint/last_updated 和单个 active 字段. 本轮保留旧键及类型, 增补模板键并同步别名; 无本轮派发时活动 ID 清空, 旧 ID/状态原文保存在 [原状态快照](history/current.pre-organization-20261008.txt). 历史预算数值不作为当前预算.

仓库 scripts/_json_update.py 和 _tmp_update_state.py 是旧一次性写入器, _act.py/_agents.py 含当时记录. workflow 的 research_state.py 管理另行版本绑定的进度/checkpoint, 未找到其以 state/current.json 为当前读写入口的代码. 本轮未创建另一份 current 文件, 未改 checkpoint/progress 原快照, 也未启动旧状态写入器.

旧 validate_project.py 仍期待 knowledge/ 下旧 canonical 文件和旧目录职责; v2.2 布局按顶部 gateway 生效. 本轮不以该旧全项目检查给当前布局制造通过标签, 只验证本次状态 JSON 的字段/类型/别名及实际指针. 不把预算, ID 或 schema 兼容性检查当作任务运行状态验证.

## 复现和构建

复现数学结果先读原 run 的合同, 冻结源码和 repro manifest, 确认输入/精度/依赖, 输出另存. [脚本导航](../scripts/README.md) 区分当前数值诊断, 精确证书与历史实现. 本轮未重跑它们.

编辑某个 TeX 后可在有中文字体的既有 XeLaTeX 环境按该文稿的构建约定运行, 例如:

```bash
cd docs
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build SL_ratio_proof.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build SL_ratio_proof.tex
```

实际构建前检查是否会覆盖被绑定的 build/PDF/日志, 为新版本选独立输出位置. [归档规则](archive-policy.md) 要求保留证据日志; 本轮未编译任何文稿.

Blueprint 读取与维护通过当前安装插件的 runtime/blueprintctl.py: 先 ensure, 再按具体任务 query/validate. 本轮只核对 runtime 绑定, 不提交/接收命题或执行退役项目内维护器. Lean 复现遵循 [工程状态](../lean-proof/STATUS.md), toolchain 与具体审核合同; 构建成功不建立全部数学形式化.

## 历史入口

[2026-09-09 整理报告](../reports/repository-cleanup-20260909/REPORT.md) 与 [旧清单](../reports/repository-cleanup-20260909/cleanup-manifest.json) 保留当时删除/保护记录. 本轮没有删除文件. [2026-10-08 维护记录](../state/AGENTS_SESSION_LOG.md#2026-10-08-仓库入口与续接整理) 和 [原字节快照清单](history/entry-snapshots-20261008.json) 保存本次范围, 引用/绑定检查和验证结果; [最早中文](history/README.pre-v2.zh.txt)/[英文](history/README.pre-v2.en.txt) 快照不覆盖. 历史未提交/未发布状态保持当时语境, 后续发布看 [RESUME](../state/RESUME.md).
