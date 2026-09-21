---
title: 带状自洽极值判据
tags: [mathtool, self-developed]
source: 自研 (会话 13)
status: 机制严格推导 + 数值验证 (1e-9..1e-12)
created: 2026-08-05
---

# 带状自洽极值判据 (gap-band-extremals)

## 解析
对无质量约束的逐点界类 $1 \le \rho \le R$ 上的 Dirichlet 弦 $-y''=\lambda\rho y$, 相邻间距
$D_n(\rho)=\lambda_{n+1}-\lambda_n$ 的驻点配置满足 **带状自洽**:

设 $u_k$ 为 $L^2(\rho)$-归一化特征函数, $f=\lambda_n u_n^2-\lambda_{n+1}u_{n+1}^2$.
由 Feynman-Hellmann 公式, $\delta D = \int \delta\rho\, f\, dx$, 故:
- 极大化配置 (SUP): $\rho=R$ 于 $\{f>0\}$, $\rho=1$ 于 $\{f<0\}$, $f=0$ 于跳变点;
- 极小化配置 (INF): $\rho=1$ 于 $\{f>0\}$, $\rho=R$ 于 $\{f<0\}$, $f=0$ 于跳变点.

反之, 若 bang-bang 配置满足 (i) $f$ 在全部跳变点为零, (ii) $\operatorname{sgn} f$ 与密度带
一致, 则该配置是 $D_n$ 的驻点. 观测到的极值配置均为 $2n+1$ 块对称配置:
SUP $[1,R,1,\dots,1]$, INF $[R,1,R,\dots,R]$.

**Feynman-Hellmann 对称加倍**: 移动第 $j$ 个跳变点连同其镜像 $\varepsilon$ 时,
$\frac{d\lambda_k}{d\varepsilon}=-\lambda_k(\rho_L-\rho_R)u_k(x_j)^2\cdot 2$,
其中 $\rho_L,\rho_R$ 为该跳变点两侧密度, 因子 2 来自镜像移动.
于是 $\frac{dD}{d\varepsilon}=(\rho_L-\rho_R)f(x_j)$: 自洽条件 $f(x_j)=0$ 恰为间距驻点条件.

## 适用范围
- 适用: 无质量约束的逐点界密度类 (如 $1\le\rho\le R$); 相邻指标 $(\lambda_{n+1},\lambda_n)$;
  可与 R 续延法配合做分支追踪.
- 边界情形: 近简并对 ($\lambda_{n+1}\approx\lambda_n$) 时最小二乘病态 (n=12 INF 残差 1.6e-3);
  R 很大时 SUP 分支退化 ($v\to0$), 需特定种子或续延.
- 不适用: 有总质量/范数约束的类 (如 $L^1$ 球, MDE 类), 极值可能含原子测度, 判据需改用
  测度微分方程; 此时参见 [[mde-extremal]].
- 判据只给出驻点, 不自动给出全局极值性/块数最小性/对称性 (需黑塞定号 + 全局搜索佐证).

## 验证与备注
- 机制推导严格 (Feynman-Hellmann 一阶变分); 数值解满足残差 1e-9..1e-12 与带匹配 = 1.0000.
- FH 数值检验: R=4, n=2 SUP, 移动边 1 (两侧 1,4): 数值导数 157.665 vs FH 157.664 (1e-6);
  移动边 2 (两侧 4,1): -109.289 vs -109.290; n=4 SUP 对称参数化 dlam12=dlam13=375.1,
  单侧 FH -187.55 (因子 2 精确).
- 黑塞: INF 全正定, SUP 全负定; 全局搜索 (2n+3 块) 不超越 2n+1 块自洽解.
- 数值结果: R=4, n=1..12 主表, R 扫描 (n=1) 与 R=2 全表, 极限 (SUP R->inf 时 D->4pi^2;
  INF R->inf 时 D*R->24.943866), 见 docs/SL_gap_extremals.tex.
- 脚本: scripts/op03_gap_fixed.py (转移矩阵, 传播顺序已修正), scripts/_tmp_fast_solver.py
  (向量化 fast 求解器), scripts/op03_gap_table.json (R=4 数据).
- 失败经验: 旧传播顺序 bug (M_new = P*M_old 而非 M_old*P) 产生伪解; 伪临界点 (n=4 INF
  11.697) 需同时检查残差与带匹配; 不动点迭代发散, 用 R 续延 + least_squares 稳定.
