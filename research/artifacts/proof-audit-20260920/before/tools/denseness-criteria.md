---
title: 稠密性准则 (denseness criteria)
tags: [mathtool, self-developed, completeness, moments, hilbert-spaces]
source: 自研 (会话 11), 方向 2: 边界约束 Hilbert 空间多项式稠密的一般准则
status: 定理已证 + 精确有理数验证
created: 2026-08-05
---

# 稠密性准则 (Denseness Criteria)

## 解析

设 $H$ 为 $[-1,1]$ 上函数的 Hilbert 空间, 满足 (H1) 所有多项式 $\Pi \subset H$
且 $\Pi$ 在 $H$ 中稠密; (H2) 矩泛函良定 ($M_k = (w, x^k)_H$ 由 Cauchy-Schwarz
自动成立). 研究对象是稀疏基 $p_0 = 1$, $p_1 = x$,
$p_{2m} = x^{2m} - \frac{m}{m-1}x^{2m-2}$, $p_{2m+1} = x^{2m+1}$
- $\frac{m}{m-1}x^{2m-1}$ ($m \geq 2$, 缺 2, 3 次). 三个通用判据:

1. **矩刻画 (充要, 定理 2)**: $\{p_n\}$ 在 $H$ 中完备 $\iff$ 不存在非零
   $w \in H$ 使矩满足 $M_0 = M_1 = 0$, $M_{2m} = mM_2$,
   $M_{2m+1} = mM_3$. 完备性被归结为矩量问题的可表示性.
2. **一阶矩准则 (定理 3)**: 若 $\|x^k\|_H \leq C k^\beta$ 且 $\beta < 1$,
   则 $\{p_n\}$ 完备. 证明: 正交条件化为一阶递推 $M_{2m} = mM_2$,
   与 $|M_{2m}| \leq \|w\|_H \|x^{2m}\|_H = O(m^\beta)$ 矛盾.
3. **跳变矩准则 (定理 5)**: 若 $\{q_n\} \subset \Pi$ 满足三系数跳变
   $q_{2m} = c_0 x^{2m} - A_m x^{2m-2} + B_m x^{2m-4}$ ($c_0 > 0$,
   $B_m \geq 0$, 且 $A_m - B_m$ 的下界给出超阶乘增长引理, 见
   [[moment-jump-completeness]]), $\|x^k\|_H \leq Ck^\beta$ 为任意多项式阶,
   则 $\{q_n\}$ 完备.

**对角临界指数**: 对角空间 $H_\beta$ (内积 $(x^j, x^k) = \delta_{jk}(k+1)^{2\beta}$)
中 $\{p_n\}$ 完备 $\iff \beta \leq 3/2$. $\beta > 3/2$ 时显式反例
$w = \sum_{m \geq 1} m(2m+1)^{-2\beta} x^{2m}$ 满足矩条件
($M_{2m} = mM_2$, $M_2 = 1$; $\|w\|^2 = \sum m^2/(2m+1)^{2\beta} < \infty$
当且仅当 $\beta > 3/2$). 故``单幂范数多项式增长''是充分非必要.

**左定应用 (定理 8, 修正版)**: 移位 Krein Laplacian 的左定空间族 $H^s$
中, $\|x^k\|_s \sim k^{s-1/2}$ (故 $s < 3/2$ 时一阶准则直接适用);
$s \geq 2$ 时用 $K_c p_{2m}$ 的跳变 ($s$-无关的多项式恒等式) +
等距传输 $K_c: H^t \to H^{t-2}$ 取 $H^{s-2}$-矩. 结论: $\{p_n\}$ 在
**一切整数** $s \geq 0$ 的 $H^s$ 中完备. 此证明更正会话 10 推论 6.2:
$K_c^{s/2}p_{2m}$ 的三单项式结构对 $s \geq 4$ 不成立 ($K_c^2 p_{2m}$ 4 项,
$K_c^3 p_{2m}$ 5 项), 正确机制见 [[left-definite-moment-recurrence]] 第 3 步.

## 适用范围

- 适用: (H1)(H2) 成立的任意 Hilbert 空间; 缺次数 2, 3 的稀疏三角基;
  判据只依赖矩的增长界与跳变结构, 不依赖具体边界条件.
- 边界情形: $\beta < 1$ (一阶); 任意多项式 $\beta$ (跳变 + 超阶乘);
  对角族临界 $\beta = 3/2$ 精确且可达; $s = 0, 1$ (L^2, H^1) 由一阶准则,
  $s \geq 2$ 由跳变 + 传输, 覆盖全部整数 $s$.
- 不适用: 需要 Schauder/Riesz 基等强于稠密性的结论; 无跳变结构且
  $\beta \geq 1$ 的范数增长 (一般 $H$ 由定理 2 的矩量问题刻画, 无闭式判据);
  分数阶 $3/2 \leq s < 2$ 的窗口 (开放问题 O1, 猜测完备, 需插值或高阶矩机制).

## 验证与备注

- 精确有理数: `scripts/d2_criterion_verify.py` - 跳变恒等式对 $s = 0..5$,
  $w \in \{x^2, x^3, 1+x+x^5, x^2+x^4\}$ 逐项精确 (240 项);
  对角临界部分和: $\beta = 1.0, 1.4, 1.5$ 发散, $\beta = 1.51, 1.6, 2.0$ 收敛;
  $\beta = 2$ 截断 $w$ 与 $p_{2m}$ 内积 $\leq 8.9\times10^{-16}$.
- 浮点: `scripts/d2_v4_float.py` - $\|x^k\|_s$ 数值指数 $s = 0..5$:
  $-0.50, 0.49, 1.51, 2.53, 3.58, 4.65$ ($\cong s - 1/2$);
  $\{K_c p_n\}$ 在 $H^s$ ($s = 0..4$) 投影残差 $N \geq 10$ 达机器精度;
  $K_c^{s/2}p_{2m}$ 非零项数 $3, 4, 5$ ($s = 2, 4, 6$), 证实更正.
- 文档: `docs/SL_denseness_criteria.pdf` (7 页, 零警告). 相关工具:
  [[left-definite-moment-recurrence]], [[moment-jump-completeness]],
  [[left-definite-theory]], [[left-definite-orthogonal-systems]].
- 诚实边界: 对角族给出精确临界指数, 但仅对对角 (正交单幂) 空间;
  一般 $H$ 的充要判据即定理 2 的矩量问题, 可表示性无一般闭式.
