---
title: hub-and-spoke 角色契约
tags: [workflow, orchestration, ai4math]
created: 2026-08-12
status: 文献引用 (MMAT / LeanMarathon, 2026-08-12 核实)
---

# hub-and-spoke 角色契约 (Hub-and-Spoke Role Contract)

## 解析

多 agent 研究采用 hub-and-spoke: 中心 orchestrator **只路由不证明**, 各 specialist 通过文件交接, 不互相直接命令.
一个角色如果依赖另一个角色的产物, 写交接工件 (目标文件, 上下文路径, 阻塞点, 接受条件), 由 orchestrator 派发下一角色.

核心角色分工:
- **sketcher**: 读问题, 写 target_contract (主断言与显示条件分离, 记录等价/特征的所需方向, 记录边界约定与退化情形审计), 分解为引理 DAG.
- **generator**: 独立证明单个引理 (在隔离 scratchpad).
- **verifier**: 以"第一次见到证明"的身份独立审稿, 无先前记忆; 内置自动 FAIL 清单.
- **auditor / ce-hunter / explorer / synthesizer / regulator**: 定义审计, 反例搜索, 路线探索, 计划综合, 失败分类与路由.
- **refiner / integrator**: 计划简化与证明缩短; 唯一合并路径.

硬路由原则:
- 证明候选必须由 generator/refiner 产出, orchestrator 不代笔; 合并前必须有新 verifier 审查包 PASS; 先前 PASS 只覆盖被查的精确工件, 任何后续改动需要重新验证.
- 验证失败路由到**最小责任角色** (计划/来源/定义/装配/路线策略/目标障碍各有归属), 不让同一证明者重写同一失败路线.
- 反例/障碍候选必须先过证明审查流程与 regulator 路由, 才能最终使用.
- 每个周期前读长期负约束记忆与压缩索引 (不重扫全量工作区).

## 适用范围

- 适用: 复杂多步研究任务, 需要独立审稿; 长周期项目跨会话协作.
- 边界: 需要固定任务分工而不是单一 agent 自由发挥时; 角色过细会增加交接开销, 小任务不必全开.
- 不适用: 简单单步查询; 无独立验证需求的琐碎修改.

## 来源

- MMAT nl-prover orchestration: https://github.com/MechMath/MechMath-agent-team/tree/main/nl-prover/prompts/orchestration.md (2026-08-12 读取)
- MMAT verifier 自动 FAIL 清单: https://github.com/MechMath/MechMath-agent-team/tree/main/nl-prover/prompts/verifier.md
- LeanMarathon 角色契约: https://github.com/YuanheZ/LeanMarathon (Blueprinter/Target-Reviewer/Refiner/Worker)

## 采纳建议

- rigorous-open-math-research 采纳三角色最小集: 草稿者 (分解与契约) / 证明者 (逐引理) / 验证者 (无记忆独立审稿, 用自动 FAIL 清单).
- 失败路由: 审查包指出阻塞类别后, 派对应角色而不是原路重试.
- 会话收尾前加"新鲜上下文收敛检查" (只从文档重建现状, 判断收敛/发散), 对应 Archon-Horizon Ground helper 思想.
