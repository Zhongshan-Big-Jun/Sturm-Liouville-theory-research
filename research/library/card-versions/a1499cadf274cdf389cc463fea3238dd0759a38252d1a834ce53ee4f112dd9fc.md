---
title: hash 寻址知识库与 wiki 编译
tags: [workflow, knowledge-base, ai4math]
created: 2026-08-12
status: 文献引用 (KB-Manager, 2026-08-12 核实)
---

# hash 寻址知识库与 wiki 编译 (Hash-Addressed Raw Sources + Wiki Compilation)

## 解析

MMAT KB-Manager 的知识库双层结构:
- **原始层**: 研究者供给原始资料, 存放于 `raw_sources/<sha256_12>/` - hash 寻址, 不可变, 保留原始文件名与附件; 待下载队列/来源清单登记.
- **编译层**: 读取/抽取/交叉引用后编译为 `wiki/` 可复用知识; `index.md` 是全局目录 (查询先读它), `log.md` 是只追加操作日志.
- **卡片类型**: `Analysis_*` (完整分析) / `PartialProof_*` (部分证明) / `Obstruction_*` (受阻路径) 显式区分; 先前部分进展与排除路线也是知识库正式成员.
- **回答规则**: researcher 只从 wiki 回答, 区分 直接陈述 / 逻辑推断 / 缺口, 引用用 wiki 内链; 除非允许否则不用外部来源.

## 适用范围

- 适用: 长期项目资料积累; 检索前先查库避免重复追溯; 需要可追溯的证据链.
- 边界: 原始资料不可变意味着更新 = 新 hash 条目 + 重新编译, 不适合频繁变动的小笔记 (小笔记走 wiki 层).
- 不适用: 一次性任务.

## 来源

- KB-Manager: https://github.com/MechMath/MechMath-agent-team/tree/main/kb-manager (README + prompts/researcher.md, ingester.md, 2026-08-12 读取)

## 采纳建议

- manage-math-research-program 项目结构借鉴双层: 论文/资料入不可变原始区 (本项目的 papers/ 与 research_cache/ 保留原样文件), 编译摘要入知识层 (tools/ + reports/).
- tools/ 卡片增加状态字段与来源链接 (现有 frontmatter 已含 status; 来源链接与 关联问题 字段补上).
- 查询流程: 先读 tools/README 索引与 reports/, 再回溯原始资料; 失败尝试与排除路线登记为知识 (项目会话记录已实践, 保持).
