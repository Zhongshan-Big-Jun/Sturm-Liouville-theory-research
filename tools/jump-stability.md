---
title: 跳变稳定性 (jump stability)
tags: [mathtool, self-developed, completeness, moments, stability]
source: 自研 (会话 11, 方向 3)
status: 定理已证 + 精确有理数/对数空间数值验证
created: 2026-08-05
---

# 跳变稳定性 (Jump Stability)

## 解析

矩跳跃完备性判据的稳定性理论. 对二阶跳变递推 $c_0 u_m = A_m u_{m-1} - B_m u_{m-2}$
($u_0=0$, $u_1=1$, $B_m \geq 0$, $A_m \geq B_m$), 增长引理 (定量形式):
$u_m$ 单调且
$$u_m \geq \prod_{k=2}^m \frac{A_k - B_k}{c_0} = \prod_{k=2}^m (1+\varepsilon_k),
\quad \varepsilon_k = \frac{A_k-B_k-c_0}{c_0} \geq 0.$$

**稳定性定理**: 若 $\sum_{k \leq m} \min(\varepsilon_k, 1) = \omega(\log m)$, 则
$u_m$ 超多项式增长 ($u_m/m^\beta \to \infty$, 一切 $\beta$), 从而任意满足
(H1) 多项式稠密 + (H2) 矩良定 + 单幂范数界 $\|x^k\|_H \leq C k^\beta$ 的空间
$H$ 中, 跳变族 $q_{2m} = c_0 x^{2m} - A_m x^{2m-2} + B_m x^{2m-4}$
($q_0 = c_0$, $q_1 = c_0 x$, 缺 2, 3 次) 完备.

**尖锐性**: $\varepsilon_k = C/k$ 时 $u_m = m^C/\Gamma(1+C)(1+o(1))$ 仅多项式,
对角空间 $H_\beta$ ($\beta > C+1/2$) 中族不完备 (显式 $w = \sum u_m (2m+1)^{-2\beta} x^{2m}$).
门槛 $\omega(\log m)$ 精确.

**Krein 余量**: $A_m - B_m = 4m + cm/(m-1) \geq 4m + c$,
$\varepsilon_m \sim (4/c)m$, 超阶乘余量; 常数扰动 $c \to c+\delta$ ($\delta > -c$)
与基系数有界扰动均保持完备性.

## 适用范围

- 适用: 矩跳跃框架下的任何系数扰动问题; 关键只要求 $u_m$ 超多项式
  (具体幂次/常数不重要, 见会话 10 经验 3); 门槛以``有效超出量''
  $\sum \min(\varepsilon_k,1)$ 的发散阶给出.
- 边界情形: $B_m = 0$ 时增长引理为等式; $B_m > 0$ 时用单调性;
  $\varepsilon_k = 1/\log k$ 恰好满足条件 ($\sum \sim m/\log m = \omega(\log m)$);
  $\varepsilon_k = 1/k$ 为反例临界线.
- 不适用: 系数使 $A_m - B_m < c_0$ 时单调性丢失; 需要 Schauder/Riesz 基等
  强于稠密性的结论; 变系数算子 $K = -D^2 + c(x)$ 破坏跳变结构 (开放问题 S3).

## 验证与备注

- 增长引理下界逐项精确 ($\varepsilon_k = k^{-1/2}, k^{-1}, k^{-3/2}$, $m \leq 200$);
  增长速率分类 $\alpha = 0.5$ 超多项式 / $\alpha = 1$ 多项式 (指数 0.88) /
  $\alpha = 1.5$ 有界; 对角反例部分和收敛阈值 $\beta > C+1/2$; Krein 对数空间
  余量 $1200$--$1900$; 临界 $\varepsilon = 1/\log k$ 窗口.
- 脚本: `scripts/d3_stability_verify.py`, `scripts/d3_stability_verify2.py`.
- 文档: `docs/SL_stability_moment_jump.pdf` (5 页, 零警告).
- 相关: [[moment-jump-completeness]], [[left-definite-moment-recurrence]],
  [[denseness-criteria]].
- 开放: 门槛线上系数族完整分类 (S1); 一般 $H$ 的可表示性门槛 (S2).
