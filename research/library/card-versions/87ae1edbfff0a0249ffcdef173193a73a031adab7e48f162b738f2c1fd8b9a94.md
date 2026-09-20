---
title: 首错定位与错误分类
tags: [workflow, audit, lean, ai4math]
created: 2026-08-12
status: 文献引用 (FaithSieve / FormalRx, 2026-08-12 核实)
---

# 首错定位与错误分类 (First-Error Localization and Error Taxonomy)

## 解析

两个互补机制:
- **首错定位** (FaithSieve): 问题-证明对标注 `first_error_step` - 第一个出错的证明步骤下标 (全对则标 correct). 审稿/诊断只定位首错, 不泛泛给意见, 使修复可操作.
- **错误分类法** (FormalRx): SCI (Semantic, Categorization, Interpretation) 错误分类法把自动形式化错误分为 **28 类** 带严格优先级; 四个诊断能力: **判定** (对齐判定) / **分类** (错误类别) / **定位** (错误位置) / **修正** (给出修改). 8B 诊断模型在 56,287 NL-FL 对上训练; 报告指标: 判定 F1 0.88, 分类 F1 0.71, 定位准确率 0.75, 修正准确率 0.73 (OpenAlex 摘要, 非本项目复算).

## 适用范围

- 适用: 形式化错误诊断; 审稿报告写作; 任何"失败反馈要可行动"的场景.
- 边界: FormalRx 分类法是文献声明, 未在本项目复算; 采纳其思想 (分类-定位-修正四步) 而非依赖其模型.
- 不适用: 需要人工判断语义是否忠于源文献时 (分类法不替代语义复核).

## 来源

- FaithSieve (匿名稿): https://github.com/TropicalFatFish/anonymous-faithsieve (proofloc_olympiad 350 条 / proofloc_university 200 条, 2026-08-12 核实)
- FormalRx: https://github.com/LARK-AI-Lab/formalrx ; 论文 arXiv:2607.04655 (摘要经 OpenAlex 获取, 2026-08-12)

## 采纳建议

- 审计报告模板固化: 每条失败 = 错误位置 (首错) + 错误类别 (陈述层/证明层/依赖层/边界约定) + 修正动作.
- lean-verify 错误诊断按 判定 -> 分类 -> 定位 -> 修正 四步执行, 分类清单可参考 28 类思想自建轻量版 (编译错误/类型错误/超假设/方向错误/遗漏情形/依赖误用/语义不符).
