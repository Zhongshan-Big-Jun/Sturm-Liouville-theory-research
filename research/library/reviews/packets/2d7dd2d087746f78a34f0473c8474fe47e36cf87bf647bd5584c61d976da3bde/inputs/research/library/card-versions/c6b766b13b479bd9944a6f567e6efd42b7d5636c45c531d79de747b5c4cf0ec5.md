---
dependencies: [{"location": "tools/spectral-domain-checks.md", "sha256": "8deeec4e940472b96a502a78ea8a600bb9570547c9819b378199d006233625d4"}]
title: 左定矩跳跃 (left-definite moment recurrence)
tags: [mathtool, self-developed, completeness, left-definite, moments]
source: 自研 (会话 10), H3 完备性证明的核心机制
status: 定理已证 + 精确有理数验证
created: 2026-08-04
---

# 左定矩跳跃 (Left-Definite Moment Recurrence)

## 解析

对移位 Krein Laplacian $K_c$ 的真正左定空间 $H^s=D(K_c^{s/2})$,
本工具直接适用于 $s=2,3$. 先验证 $p_n\in H^s$ 及取矩单项式在 $H^{s-2}$ 中.

1. 等距同构 $K_c:H^s\to H^{s-2}$ 将正交条件变为
   $(K_cw,K_cp_n)_{s-2}=0$.
2. 多项式恒等式 $K_cp_{2m}=cx^{2m}-A_mx^{2m-2}+B_mx^{2m-4}$,
   $A_m=2m(2m-1)+cm/(m-1)$, $B_m=2m(2m-3)$, 给出良定的矩递推
   $cM_{2m}=A_mM_{2m-2}-B_mM_{2m-4}$, 奇次同理.
3. $B_m\ge0$ 和 $A_m-B_m\ge c$ 先保证钉住解单调;
   本例更强的 $A_m-B_m\ge4m+c$ 才给出阶乘下界;
   $L^2$ 或 $H^1$ 矩的多项式上界迫使自由参数 $M_2,M_3$ 为零.
4. 多项式在取矩空间中稠密, 所以湮灭元为零.

## 适用范围

- H2/H3 主证明可用. 谱截断与连续嵌入进一步给出同一族在 $0\le s\le3$ 中稠密.
- 原任意整数阶推广于 2026-09-20 撤回. $p_4\in H^s$ 当且仅当 $s<7/2$ (非负阶), 所以所有 $s\ge7/2$ 的原同族断言为假.
- $3<s<7/2$ 的同族稠密性本次不判定. 精确谱系和成员阈值见 [[spectral-domain-checks]]. 形式微分展开、代数多项式逆和自伴算子幂域必须分开.
- 方法推广必须先核对所有成员关系, 不能把未定义的 $(w,x^k)_t$ 当作矩.
- 本方法给出稠密性, 不自动给出 Schauder/Riesz 基性质.

## 验证与备注

- 应用: H2 的 L2 矩与 H3 的 H1 矩主链. 旧全阶推广被算子域反例否定.
- 推广: 一般的``多项式稠密 Hilbert 空间 + 矩刻画''理论见 [[denseness-criteria]].
- 精确有理数验证: 恒等式 $c M_{2m} - A_m M_{2m-2} + B_m M_{2m-4}
  = (w, K_c p_{2m})_1$ 对 $w \in \{x^2, x^3, x^2+x^4, 1+x+x^5\}$, $c=3$ 逐项
  精确; 增长下界 $u_m \geq (4/c)^{m-1}m!$ 精确到 $m=30$, $c \in \{1,3,10,50\}$;
  $H^1$ 投影残差在次数 $\leq 26$ 达机器精度. 脚本:
  `scripts/h3_v69b_h1moments.py`, `scripts/h3_v68_bases_min.py`.
- 文档: `docs/SL_h3_completeness_proof.pdf` (证明), `docs/SL_h3_research_summary.pdf`
  (过程与失败路线, 含 $L^2$-矩三阶系统探索).
- 前段探索 (未用于证明): $L^2$-矩三阶递推的显式积分解、比值固定点、最小解,
  见总结文档第 2 节与脚本 `scripts/h3_v53c_symbolic.py`, `scripts/h3_v56_odd_explicit.py`.
