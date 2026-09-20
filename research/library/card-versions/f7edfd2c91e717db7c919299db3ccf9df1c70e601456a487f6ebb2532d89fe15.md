---
title: 蓝图与 DAG 状态追踪
tags: [workflow, orchestration, ai4math]
created: 2026-08-12
status: 文献引用 (LeanMarathon / Archon-Horizon, 2026-08-12 核实)
---

# 蓝图与 DAG 状态追踪 (Blueprint and Proof-DAG Tracking)

## 解析

LeanMarathon 的方法: 把自然语言证明转化为 Lean 4 蓝图, 蓝图 = **形式骨架 + 自然语言证明图 + 系统记录**.
两阶段编排:
- 阶段 1: Blueprinter 生成初始蓝图 (目标契约 + 引理依赖图), Target-Reviewer 审查目标陈述 (合理解读/问题打包为 issue), Refiner 修复, 直到蓝图 CI 绿并入 main.
- 阶段 2: 按证明 DAG 自叶向上并行派发 Worker, 每个 worker 证明一个动态叶节点, 失败则提交 blocker issue; 每轮结束后合并, CI 门控; 多轮迭代.
- 角色由分支模式与交付物契约限定, 通过 GitHub 工作树/仓库管理, 审计日志保留.

Archon-Horizon 的补充: workspace 为工作单元; 只读 Ground helper 在收尾/长跑中段/策略转向后做**新鲜上下文收敛检查** (从 ledger/报告/路线图/inbox/图/Lean 状态重建, 判断是否收敛, 只写 issue 不改源码); 团队通过共享 roadmap board / inbox / commit ledger 异步协调; 软冻结保护基础签名不被悄悄改动.

## 适用范围

- 适用: 跨会话长研究; 多依赖并行任务; 需要状态可恢复的工作流.
- 边界: 单 agent 串行时蓝图价值主要在状态追踪与可恢复性, 并行收益有限.
- 不适用: 单步快速任务.

## 来源

- LeanMarathon: https://github.com/YuanheZ/LeanMarathon (README + docs, 2026-08-12 读取)
- Archon-Horizon: https://github.com/frenzymath/Archon-Horizon (README + docs/architecture, 2026-08-12 读取)

## 采纳建议

- manage-math-research-program 增加"蓝图"概念: 研究任务包先写目标契约 + 引理依赖图 + 每节点状态 (待证/候选/已证/阻塞), 跨会话读取.
- 会话收尾做新鲜上下文收敛检查: 不读对话历史, 只从 AGENTS.md 会话记录 / tools 索引 / 文档重建现状, 判断收敛还是发散, 发现的分叉登记为待办.
- 软冻结: 已批准陈述/已归档工具文件不随意改, 改动必须登记.
