---
title: Sturm 振荡理论
tags: [mathtool, spectral]
source: 经典理论
status: 文献引用
created: 2026-08-04
---

# Sturm 振荡理论

## 解析
正则 SL 问题 $-y''=\lambda\rho y$ (Dirichlet) 的特征值严格递增且简单: $\lambda_1<\lambda_2<\cdots$; 第 $m$ 个特征函数 $y_m$ 在 $(0,1)$ 内恰有 $m-1$ 个内零点. Sturm 比较定理: 若 $\rho_1\le\rho_2$ 逐点, 则对应特征值满足 $\lambda_k(\rho_1)\ge\lambda_k(\rho_2)$.

## 适用范围
- 适用: 指标与节点数对应; 单调性比较; 构造反例 (节点位置); 零点截断 (见 [[mw-zero-truncation]]).
- 边界情形: 半正定/奇异问题需要一般化 (Sturm-Liouville 理论的扩展).
- 不适用: 复杂边界条件 (非分离型) 下简单性可能失效.

## 验证与备注
- 支撑平凡不等式 $\lambda_{n+1}\le\lambda_{2n}$ (见 [[spectral-monotonicity-reduction]]).
