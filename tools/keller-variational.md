---
title: Keller 变分条件
tags: [mathtool, extremal]
source: Keller 1976, SIAM J. Appl. Math. 31, DOI 10.1137/0131042
status: 文献 + 数值 (1e-11)
created: 2026-08-04
---

# Keller 变分条件

## 解析
对 $-y''=\lambda\rho y$, $0<a\le\rho\le A$, 特征值比 $\lambda_j/\lambda_k$ 的极值配置满足:
1. 逐段常值, 取值只有 $a$ 与 $A$ (Keller 定理 0, 与 [[bang-bang]] 一致);
2. 在跳点处的一阶变分条件 (Keller (3.8)(3.9)): 对任意 $j,k$ 形式相同, 内容为权重归一化 $\int\rho y^2=1$ 下的匹配条件 (跳点两侧 $|y_j|$ 与 $|y_k|$ 的平衡);
3. 极值函数逐段常数: 极小化 $\lambda_2/\lambda_1$ 时 $\rho=a$ 于 $(-x_0,x_0)$, $=A$ 于其余 (区间 $[-1/2,1/2]$ 版本).

## 适用范围
- 适用: 逐点夹逼类 $0<a\le\rho\le A$ 中任意特征值比 $\lambda_j/\lambda_k$ 的极值问题; 是推导极值配置结构的统一起点.
- 边界情形: $a\to 0$ 时跳点 $x_0\sim 1/2-\sqrt{a}$ (数值复算 $(0.5-x_0)/\sqrt{a}\to 1$); $\mu(a)$ 从 1 增到 4.
- 不适用: $L^p$/全变差约束类 (见 [[mde-extremal]]); 不给出比值本身的最优常数 (需要配合闭式方法如 [[balanced-phase]]).

## 验证与备注
- 会话 4-5: 对固定 $n$ 猜想候选配置, 跳点处变分条件符号级验证 (1e-11), 见 `scripts/num_keller_check.py`.
- 文献: keller1976.pdf (papers/).
