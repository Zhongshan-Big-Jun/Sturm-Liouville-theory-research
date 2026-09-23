---
title: 交替平衡世俗多项式 2n 根计数 (secular-chebyshev-jacobi-rootcount)
tags: [mathtool, self-developed, secular, chebyshev, jacobi, fixed-n]
source: 自研 (run R-20260822T220000Z-b3-baseline)
status: 定理已证 (STRICT)
created: 2026-08-22
---

# 交替平衡世俗多项式根计数 (secular-chebyshev-jacobi-rootcount)

## 解析

对交替 bang-bang 配置 `[1,R,1,...,1]` (2n+1 块, 宽度平衡
`w_1/w_2=sqrt(R)`, `t=1/((n+1)sqrt(R)+n)`), 设 `s=sqrt(R)`, 世俗函数
`F_n(y)` (`y = omega s t`). 有

    G_n = w (T_end T_cell^n)_{01},
    G_n = tau G_{n-1} - G_{n-2}   (n>=2),
    tau = 2 cos^2 y - (s+1/s) sin^2 y.

令 `F_n = sin y Q_n(cos y)`. 在 `x=C^2` 下, `P_n(x)=Q_n(sqrt(x))` 满足

    P_0=1, P_1=A x-s,
    P_n=(A x-B)P_{n-1}-P_{n-2},
    A=(s+1)^2/s, B=(s^2+1)/s=A-2.

令 `t=(A x-B)/2`, `delta=1/s`, 则

    P_n(x) = U_n(t) + delta U_{n-1}(t),

即 `p_n(z)+delta p_{n-1}(z)`, `z=2t` 是 n×n 对称三对角 Jacobi 矩阵
(对角 0, 次对角 1, 末对角 -delta) 的特征多项式. 该矩阵有 n 个互异实特征值,
且全部在 `(-2,2)` 内 (用 z>2, z<-2 的双曲表示直接排除外部零点).
因此 `P_n` 在 `(0,1)` 有 n 个根, `Q_n(C)` 在 `(-1,1)` 有 2n 个根,
`F_n(y)` 在 `(0,pi)` 有 2n 个简单根.

## 适用范围

- 适用: 交替平衡配置的 2n 根计数; 任何 R>1, n>=1.
- 不适用: 非平衡宽度 (各块相位不同) 的世俗根计数; 非交替或非 bang-bang 配置.

## 验证与备注

- 推导 STRICT; 符号验证 `G_n = tau G_{n-1}-G_{n-2}` 对 n=2..5 PASS;
  数值验证闭式 `P_n=U_n+delta U_{n-1}` (s=3, n=1..6) 机器精度.
- 脚本: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/symbol_polys2.py,
  candidate_proof.md Part B.

## 独立审计 (2026-08-22)

- Audit: `runs/plugin-perf-eval2/R-20260822T230000Z-b3-audit/audit_report.md`
  (REPAIRABLE_GAP: endpoints z=±2 and simplicity of F_n roots repaired).
