---
slug: leftdef-o1pld-l2-structural
title: 左定 O1'LD 的 L^2 降维结构定理 (有限支撑矩刚性/奇偶分解/μ_4 非稠密例)
tags: [稠密性, 左定, L2, 矩问题, O1pLD]
status: STRICT 部分结果 + 一个 NOT-YET-STRICT 条件定理 (RIGOROUS_PARTIAL_RESULT; 一般 O1'LD 仍开放)
source: R-20260823T030000Z-leftdef-o1pld
related: ["[[constrained-denseness-runs]]", "[[denseness-criteria]]", "[[left-definite-moment-recurrence]]"]
---

# 左定 O1'LD 的 L^2 降维结构定理

## 解析

设 s=2, 等距同构 K_c : H^2 -> L^2, q_n = K_c p_n.

- **有限支撑 L^2 矩刚性 (STRICT)**: L^2(-1,1) 中若有 f 的矩
  (f,x^k) 只对有限个 k 非零, 则 f=0. 证明用 Müntz-Szász 的 L^p 形式
  **在 Lebesgue 测度上的 L^2(0,1)**:
  - 偶部 h(y)=y^{-1/4} f_e(√y) ∈ L^2(0,1), 矩化归为 ∫ h(y)y^{m-1/4}dy;
  - 奇部 t(y)=y^{1/4} h_o(y) ∈ L^2(0,1), 矩化归为 ∫ t(y)y^{m+1/4}dy;
  两个指数集都是删去有限点后仍发散倒数和的, 故相应单项式族稠密.
- **Cauchy-Schwarz 矩界 (STRICT)**: |(f,x^k)| <= ||f||_2 sqrt(2/(2k+1)).
  **但不再把 DensBC O1 的两项游程代数用于 L^2/H^1 降维**; 实际 q_n 矩满足
  三项递推 c M_{2m}=A_m M_{2m-2}-B_m M_{2m-4} 及奇对应.
- **尾部 L^2 刚性 (NOT-YET-STRICT)**: 若 m>=m0 的尾部三项递推成立,
  则非零 L^2 可实现矩应不存在. 支配解阶乘增长已被经典 SL_h2 增长引理覆盖,
  但附加的最小解 (多项式衰减) 情形尚未在此修复中完全排除.
- **cofinite-N 稠密定理 (NOT-YET-STRICT)**: 若 N 在 D 中余有限, 则
  span{q_n:n∈N} 在 L^2 中稠密. 证明已改写成基于实际三项递推 + 尾部刚性;
  由于尾部刚性未 STRICT, 该定理暂不注册为 STRICT.
- **奇偶分解 (STRICT)**: closure(span Q_sp) = closure(span 偶保留)
  ⊕ closure(span 奇保留). 这由偶/奇子空间正交得到.
- **例子 (STRICT)**: 约束 L(f)=∫(K_c f) x^4 在 H^2 上给出非稠密:
  Q_sp 为奇稀疏族 {1} ∪ {2m+1:m>=2}, 其闭包是奇子空间, 严格小于 V.
  奇侧稠密性用 SL_h2 奇增长引理 + q_1 给出 M_1=0.

## 适用范围

- 适用: s=2 的 O1'LD 降维; 一般 L^2 中稀疏族子列稠密性的结构性判断.
- 不适用: 不直接给出任意 W 的完整判据; 不适用于 H^1 无限游程不可实现
  (已降级为 EVIDENCE/plausible) 与 H^1 有限游程可实现性 (开放).

## 验证状态

- STRICT 陈述与证明见 run R-20260823T030000Z-leftdef-o1pld/candidate_proof.md.
- NOT-YET-STRICT: 尾部刚性 Claim 4; cofinite-N 定理与真子空间非余有限推论.
- EVIDENCE 脚本 reproducibility/o1pld_l2_mu4.py (sympy 精确).
- 独立审计 R-20260823T040000Z-leftdef-o1pld-audit 的修复项已落实:
  Müntz 加权化、移除 DensBC O1 游程代数、μ_4 奇侧增长论证、依赖命名修正.
- Lean scaffold 未验证.

## Repair log (tool entry)
本工具页在独立审计后更新: 不再宣称 cofinite-N 为 STRICT;
尾部刚性标记 NOT-YET-STRICT; H^1 无限游程降级; 依赖命名修正.
