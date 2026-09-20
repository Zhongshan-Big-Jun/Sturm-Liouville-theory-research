---
title: M2F 陈述冻结
tags: [workflow, lean, ai4math]
created: 2026-08-12
status: 文献引用 (M2F/ReasBook, 2026-08-12 核实)
---

# M2F 陈述冻结 (Statement Compilation and Freeze)

## 解析

文献级形式化的两阶段方法 (M2F):
- **阶段 1 陈述编译**: 把非形式数学陈述翻译为 Lean 声明骨架; 修复命名空间/类型/签名一致性保证项目级可编译; **允许临时证明空洞 (sorry)** 以最大化结构覆盖, 先不追求证明.
- **阶段 2 证明修复**: **冻结陈述签名**防止目标漂移; 用验证器反馈迭代补证明; 在固定声明下优化证明成功率.

关键点: 陈述与证明解耦 - 陈述未批准前不动证明; 陈述批准后 (f-reviewer 核准) 任何修改需要重新核准 + 新 guard 快照, 然后才恢复证明工作.

文档级结果 (README 声明): 479 页长文档语料 -> 153,853 行 Lean; FATE-H (100 题) 全自动 96% PSR, 轻监督 97%, 阶段 2 匹配陈述 100% PSR.

## 适用范围

- 适用: 从论文/教材逐条形式化的批量任务; 任何"陈述结构完整性优先"的场景.
- 边界: 需要人在环 - 人工核对自然语言抽取与原文一致, 核对形式化陈述与 NL 对应.
- 不适用: 陈述本身含糊未定时 (应先审计定义与边界约定, 见 target_contract).

## 来源

- M2F: https://github.com/optsuite/M2F (README, 2026-08-12 读取)
- ReasBook (产物): https://github.com/optpku/ReasBook
- Quokka 在线系统: https://quokka.reaslab.io/

## 采纳建议

- lean-verify 工作流: 先逐条冻结陈述 (全部声明可编译, 允许 sorry), 再进入证明轮; 已批准陈述的修改必须重新过审 (对应 FL-Prover statement-guard).
- 项目 lean-proof/ 批量形式化时按此顺序, 避免边写陈述边写证明导致签名漂移.
