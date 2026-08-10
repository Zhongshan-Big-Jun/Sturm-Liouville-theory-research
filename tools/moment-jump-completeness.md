---
title: 矩跳跃完备性判据 (moment-jump completeness)
tags: [mathtool, self-developed, completeness, moments]
source: 自研 (会话 9), 用于 [4, Section 6] 开放问题
status: 定理已证 + 精确有理数验证
created: 2026-08-04
---

# 矩跳跃完备性判据 (Moment-Jump Completeness)

## 解析

设 $(H, (\cdot,\cdot)_H)$ 为 Hilbert 空间, $T: H \to L^2(I)$ ($I$ 有界区间) 为等距同构
(例如 $T = K_c$: 见 [[left-definite-theory]]). 给定代数不完备的多项式列
$\{p_n\}$ (缺若干次数 $d \in D$), 若满足:

1. $T p_n$ 的系数结构为 ``三阶跳变'': 对 $n \geq n_0$,
   $$T p_n = c_0 x^n - A_n x^{n-2} + B_n x^{n-4},$$
   且 $A_n - B_n \geq c_0$ (或类似下界), $B_n \geq 0$;
2. 矩 $\mu_k = \langle g, x^k \rangle$ 满足 Cauchy-Schwarz 上界
   $|\mu_k| \le \|g\|_2 \sqrt{2/(2k+1)}$;

则 $\{p_n\}$ 在 $H$ 中解析完备. 机制: 正交条件 $\langle g, T p_n\rangle = 0$
化为递推 $c_0 \mu_n = A_n \mu_{n-2} - B_n \mu_{n-4}$; 缺次数 $d \in D$ 使
对应矩为自由参数, 但递推把这些矩向后传播为阶乘级增长序列, 与有界性矛盾,
故自由参数被迫为零, 全部矩为零, Weierstrass 稠密性给出 $g = 0$;
Hahn-Banach 推论给出完备性.

增长引理 (核心): $u_0=0, u_1=1$, $c_0 u_j = A_j u_{j-1} - B_j u_{j-2}$ 的解满足
$$u_j \geq (4/c_0)^{j-1} j!,$$
证明: 先由 $A_j - B_j \geq c_0$ 归纳单调性 $0 < u_{j-1} \le u_j$,
再由比值 $r_j = u_j/u_{j-1} \geq (A_j - B_j)/c_0 \geq 4j/c_0$ 连乘.
注意: 逐项下界 $u_j \geq (A_j/c_0)u_{j-1}$ 一般**不**成立
($c=3$ 时 $u_4=3700 < 3780 = (A_4/c)u_3$), 必须用单调性 + 比值方法.

## 适用范围

- 适用: 多项式基 + 边界条件约束的 Hilbert 空间 (左定空间); 代数缺陷 (缺次数)
  不破坏解析完备性的情形; 等距同构 $T$ 使 $T p_n$ 为稀疏 (三系数) 多项式时.
- 边界情形: 递推必须有 $B_j \geq 0$ 与 $A_j - B_j \geq c_0$; 缺次数须与自由参数
  一一对应; 等距同构与 $0 \notin \sigma$ 是关键前提.
- 不适用: 无等距结构的空间; $T p_n$ 系数稠密 (非三系数) 的基; 需要正交性
  (Schauder 基 / Riesz 基) 的更强结论 (本判据只给稠密性).
- 局限: 只判解析完备 (密度), 不构造显式正交系, 不给收敛速率.
- 推广: 对任意整数 $s \geq 1$ 的左定空间 $H^s$, 取矩内积改为与正交条件同源的
  $(\cdot,\cdot)_s$, 递推系数不变, 上界为多项式增长, 结论同样成立 (会话 10).
  见 [[left-definite-moment-recurrence]].

## 验证与备注

- 应用: 移位 Krein Laplacian 第二左定空间 $H^2[-1,1]$, 基
  $\{1, x, p_4, p_5, \dots\}$ ($p_{2n} = x^{2n} - \frac{n}{n-1}x^{2n-2}$),
  $T = K_c$, 缺次数 $\{2,3\}$. 结论: 解析完备 (是). 见
  `docs/SL_h2_completeness_proof.pdf`.
- 精确有理数验证 (c=1,3,5): 等距恒等式逐对精确成立; 增长下界对 $j\le24$ 成立;
  $x^2, x^3$ 投影残差超指数衰减到 0. 脚本: `scripts/num_h2_proof_check.py`.
- 文献: [4] Axioms 14 (2025) 115, Section 6 开放问题 (原文已核对,
  `papers/axioms14_115.pdf`).
