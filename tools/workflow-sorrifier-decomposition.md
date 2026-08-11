---
title: sorrifier 分解
tags: [workflow, lean, ai4math]
created: 2026-08-12
status: 文献引用 (MechMath, 2026-08-12 核实)
---

# sorrifier 分解 (Sorrifier-Driven Decomposition)

## 解析

证明失败时的分解策略: 把失败的证明块替换为 `sorry`, 保留其余骨架继续验证,
从而得到**干净的子问题** (失败块独立可证/可拆), 再递归解决.
避免两类常见低效: 全量重新生成整个证明, 以及上下文无限膨胀.

配套机制 (MechMath 的 sorrifier 驱动形式化分解工作流):
- 失败块 sorry 化后, 编译器仍验证其余部分, 保证结构覆盖.
- 提取的子问题独立进入下一轮证明尝试.
- 与陈述冻结 (见 [[workflow-statement-freeze]]) 配合: 分解不改变陈述签名.

## 适用范围

- 适用: 长证明中单一子目标卡死; 证明重构时想保留已验证部分; 形式化文档级项目 (多声明多依赖).
- 边界: sorry 必须被追踪 - 提交/合并前 sorry 清零 (与四道闸的 sorry 扫描配合); 不把 sorry 化当终点.
- 不适用: 陈述本身错误时 (应先修陈述或重新形式化, 见 FormalRx 错误分类).

## 来源

- MechMath-v1 (sorrifier 工作流): https://github.com/MechMath/MechMath-v1 (repo 描述: Sorrifier-Driven Formal Decomposition Workflow for Automated Theorem Proving; 2026-08-12 核实)

## 采纳建议

- lean-verify 工作流写入: 失败 -> 失败块 sorry 化 -> 验证骨架仍编译 -> 提取子问题单独攻 -> 合并前 sorry 清零.
- 项目 lean-proof/ 中遇到卡点证明时优先采用, 而不是重写整个文件.
