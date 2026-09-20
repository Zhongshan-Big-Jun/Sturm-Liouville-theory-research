---
title: bang-bang 原理
tags: [mathtool, extremal]
source: 最优控制经典原理
status: 文献引用
created: 2026-08-04
---

# bang-bang 原理

## 解析
在线性约束 (逐点夹逼 $a\le\rho\le A$) 下, 对 $\rho$ 仿射/单调的目标泛函, 极值逐点取到约束端点: $\rho(x)\in\{a,A\}$ 几乎处处. 配合极值存在性 ([[helly-compactness]]) 与结构定理 (Keller/MW), 无穷维优化化归为有限跳点阶梯函数.

## 适用范围
- 适用: 本项目全部极值候选 (两值阶梯); 特征值比值问题.
- 边界情形: 需证明目标对 $\rho$ 的一阶变分不变号/有确定符号, 否则中间值可能最优; 对多重极值点需注意非唯一性.
- 不适用: 光滑性约束 (如 $\rho$ 连续) 或 $L^p$ 约束类 (见 [[mde-extremal]]).

## 验证与备注
- Keller 定理 0 与 MW 定理 1 均为其在 SL 比值问题中的实现.
