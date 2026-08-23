---
title: 一般等宽交替世俗 Chebyshev 表示 (general-alternating-secular-chebyshev)
tags: [mathtool, self-developed, secular, chebyshev, fixed-n, alternating]
source: 自研 (run R-20260823T060000Z-b3-current)
status: 定理已证 (STRICT; 尚未独立审计)
created: 2026-08-23
---

# 一般等宽交替世俗 Chebyshev 表示

## 解析

对等宽交替族 `[1,R,1,...,1]` (2n+1 块, 所有 1-块等宽 a, 所有 R-块等宽 b,
`r = a/b`, `s = sqrt(R)`), 令 `p = r x`, `q = s x`, `x = omega b`, 其中
`omega = sqrt(lambda)`。用归一化转移矩阵 `A(p)=T_1`, `B(q)=T_R`,
`C = A B`, `M_n = C^n A`, 则 Dirichlet 条件 `(M_n)_{01}=0` 可写成

    (M_n)_{01} = sin(p) [ U_n(m) + delta U_{n-1}(m) ],

其中

    m = tr(C)/2 = cos p cos q - (s+1/s)/2 * sin p sin q,
    delta = sin q / (s sin p),

`U_k` 为第二类 Chebyshev 多项式。该式由 Cayley-Hamilton 直接得到:
`C^n = U_{n-1} C - U_{n-2} I` 与
`C00 sin p + C01 cos p = (2m+delta) sin p`。

当 `|m|<1` 时令 `m=cos theta`, 根方程等价于

    sin((n+1) theta) + delta sin(n theta) = 0.

平衡情形 `r=s` 退化为 `delta=1/s`, 回到
[[secular-chebyshev-jacobi-rootcount]] 的 `U_n+delta U_{n-1}` 形式。

## 适用范围

- 适用: 等宽交替族的 secular 函数显式表示; 任何 R>1, r>0, n>=1; O2 的 route reduction.
- 边界情形: `sin p = 0` 时 delta 需按连续性理解; 中央 pair 一般 `sin p != 0`.
- 不适用: 非等宽 (各块宽度不同) 的 `[1,R,1,...,1]` 族; 该表示不直接给出 O1/O2.

## 验证与备注

- 推导 STRICT; 数值 EVIDENCE (s=2, r in {1,1.5,2,2.5,3}, n=1..5, 最大误差 ~1e-14).
- 相关 Lean scaffold: `lean-proof/SL/B3GeneralAlternatingChebyshev_Scaffold.lean`
  (仅 scaffold, 未验证).
- O1/O2 仍开放; 未声称闭合.
