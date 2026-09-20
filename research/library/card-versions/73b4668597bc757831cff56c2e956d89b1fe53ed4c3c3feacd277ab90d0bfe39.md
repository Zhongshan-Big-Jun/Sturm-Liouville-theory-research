---
title: 单阱/单垒交点计数法
tags: [mathtool, extremal]
source: Hedhly 2021 (arXiv:2111.01728), Huang 1999 (Proc. AMS)
status: 全文核验
created: 2026-08-04
---

# 单阱/单垒交点计数法

## 解析
对单阱密度 (对称, 中段小), 用两个特征函数 $y_m,y_n$ 的交点计数与 Sturm 比较证明比值上界:
$$\frac{\lambda_n}{\lambda_m}\le\left(\frac{n}{m}\right)^2 \quad(n>m, \text{单阱}),$$
对称单垒给出反向 $\ge$ 下界 (Kiss 2006 转述级). Huang 1999: 凹密度下 $\lambda_2/\lambda_1\ge 4$, 等号仅当密度常数 a.e.

## 适用范围
- 适用: 单阱/单垒/凹密度的形状约束类; 物理起源的势能形状约束.
- 边界情形: 等号情形需识别 (常数密度); 与逐点夹逼类 $1\le\rho\le R$ 不同 (形状类更窄).
- 不适用: 一般两值密度 (比值可更大, 见 [[balanced-phase]] 的 $\nu(R)\ge 4$).

## 验证与备注
- 会话 4 全文核对; 对相邻比值给出 $\lambda_{n+1}/\lambda_n\le((n+1)/n)^2$, 全序列上确界 4, 弱于本项目 $\nu(R)$ (当 $R>1$).
- 文献: hedhly_2111.01728.pdf/.txt, huang1999.txt (papers/).
