---
canonical_key: two-block gap bounds 3*pi^2/R < D < 3*pi^2 (Dirichlet string box class)
title: 两块相位间距界 (two-block gap bounds)
tags: [mathtool, self-developed, estimate]
source: 自研 (Agent C, run R-20260805T000000Z-gapn1-a1b2c3)
status: 定理已证 (UPSTREAM_AUDITED 级: 完整证明 + 4000 点零违例)
created: 2026-08-05
---

# 两块相位间距界 (two-block-gap-bounds)

## 解析
对重右两块密度 $\rho=1$ on $[0,t]$, $R$ on $(t,1]$ (重左由镜像 $x\mapsto1-x$ 归入),
Dirichlet 弦前两个特征值间距满足

$$\frac{3\pi^2}{R}<D(t)<3\pi^2\qquad\forall\,t\in(0,1),\ R>1,$$

且两端仅作为极限达到: $t\to1^-$ 时 $D\to3\pi^2$, $t\to0^+$ 时 $D\to3\pi^2/R$.

## 证明机制 (相位坐标)
令 $\mu=\sqrt R$, $c=\mu(1-t)/t$, $\theta(x)=\arctan(\mu\tan x)$ (连续分支,
$\theta(x+\pi)=\theta(x)+\pi$), $x_1<x_2$ 为 $\theta(x)+cx=k\pi$ ($k=1,2$) 的前两根, 则
$$\lambda_k=\frac{x_k^2(\mu+c)^2}{\mu^2},\qquad
D=\frac{(\mu+c)^2}{\mu^2}(x_2^2-x_1^2).$$
- **下界**: $\theta'<\mu$ 严格 $\Rightarrow$ $x_1>\pi/(\mu+c)$, $x_2-x_1>\pi/(\mu+c)$
  $\Rightarrow$ $D>3\pi^2/R$.
- **上界**, 三区:
  - $c\ge1$: $x_1\le\pi/(1+c)$; $\theta'\ge1/\mu$ 给出 $x_2-x_1\le\pi\mu/(1+\mu c)$,
    $x_2\le2\pi\mu/(1+\mu c)$; 归约为 $D\le3\pi^2 G(\mu,c)$ 且 $dG/d\mu<0$,
    $G(1,c)=1$ (sympy 精确分解, $P\ge4>0$).
  - $1/3\le c\le1$: 弦/凸性 $\Rightarrow x_2^2-x_1^2\le3\pi^2/(1+c)^2$,
    用 $(\mu+c)^2<\mu^2(1+c)^2$.
  - $0<c\le1/3$: $\varepsilon_k=k\pi-x_k$, $s_k=\tan(cx_k)=\mu\tan\varepsilon_k$,
    证明 $W'(\mu,c)<0$, 故 $W<W(\mu,0)=3\pi^2\mu^2$.

## 适用范围
- 适用: 两块 (或经过拼接的) Dirichlet 弦, $D=\lambda_2-\lambda_1$ 的逐点界;
  相位坐标在极端 $R$ ($10^4$ 以上) 下数值稳定, 优于转移矩阵粗网格.
- 边界情形: $c\to0$ 与 $c\to\infty$ 两端均为极限; $\mu=1$ 退化 ($W'=0$) 需排除.
- 不适用: 不直接给出多块族的全局界 (仅两块); 需与归约定理配合.
- 注意: 上界证明中的 $dG/d\mu<0$ 对 $c\ge1$ 成立; 对 $c<1$ 用另外两区的论证.

## 验证与备注
- 来源: agentC_O3b_boundary.md (完整证明); 相位恒等式精度 1e-13;
  4000 点网格 (R 1.05..1e4 x t) 零违例, 下界余量 +1.25e-8, 上界余量 +1.28e-6;
  $W'<0$ 用 mpmath 60 位确认.
- 独立复核 (coordinator, 2026-08-05): 相位求解器扫描 0 违例, 最小相对余量 1.6e-9.
- 失败经验: 比值路线 ($\lambda_2/\lambda_1\le4$ 反例, 两块族可到 ~9) 失败;
  独立框定 $\varepsilon_k$ 失败 (端点界过粗); 全 $c$ 上 $W'<0$ 为假 (仅 $c\le1/3$).
