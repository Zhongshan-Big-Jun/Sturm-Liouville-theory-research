---
title: Prüfer 相位
tags: [mathtool, spectral]
source: 经典理论
status: 文献引用
created: 2026-08-04
---

# Prüfer 相位

## 解析
极坐标变换 $y=r\sin\theta$, $y'=r\cos\theta$ 把 $-y''=\lambda\rho y$ 化为相位方程
$$\theta' = \sqrt{\lambda\rho}\,\cos^2\theta + \frac{q}{\sqrt{\lambda\rho}}\sin^2\theta + \cdots$$
(有势时含 $q$ 项). 相位 $\theta$ 严格递增, 特征函数每穿过一个零点相位增加 $\pi$, 因此第 $m$ 个特征值对应 $\theta(1)=(m-1)\pi$ 附近的相位.

## 适用范围
- 适用: 节点计数, 特征值单调性与比较定理的证明, 能带分析, 大指标渐近.
- 边界情形: $\lambda\to 0$ 或 $\rho$ 退化时相位方程退化, 需单独处理.
- 不适用: 无法直接给出闭式特征值 (需要配平衡条件, 见 [[balanced-phase]]).

## 验证与备注
- 是 [[balanced-phase]] 方法的概念背景: 平衡相位即要求各块相位相等.
