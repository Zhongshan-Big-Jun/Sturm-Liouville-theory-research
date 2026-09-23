---
{"author_ids": ["01a06f46-dd03-7c83-9267-32048412c359", "01a0c2d0-78b9-7f73-be52-f9bb55841fcc", "01a0c2d0-7dec-77b3-894f-a0427000a837"], "created": "2026-08-04", "dependencies": [{"location": "tools/spectral-domain-checks.md", "sha256": "eb65a8a7e076bd2299695b3e1d3dbaf012d822a311bfd5b890c480c68a50e9c7"}], "evidence_status": "ROUND6_SCOPED_ANALYTIC_REPAIR; REUSE_REQUIRES_EXACT_CORRECTION_RECEIPT", "source": "自研 (会话 9), 用于 [4, Section 6] 开放问题", "sources": [{"locator": "Sixth-round range/dependency update only; unchanged earlier branches keep their own scope", "path": "docs/SL_fractional_left_definite.tex", "sha256": "30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186"}], "status": "定理已证 + 精确有理数验证", "tags": ["mathtool", "self-developed", "completeness", "moments"], "title": "矩跳跃完备性判据 (moment-jump completeness)", "tool_id": "moment-jump-completeness"}
---

# 矩跳跃完备性判据 (Moment-Jump Completeness)

## 解析

设 $(H, (\cdot,\cdot)_H)$ 为 Hilbert 空间, $T: H \to L^2(-1,1)$ 为等距同构
(例如 $T = K_c$: 见 [[left-definite-theory]]). 给定代数不完备的多项式列
$\{p_n\}$ (缺若干次数 $d \in D$), 若满足:

1. 所有 $p_n\in H$. 低阶正交条件钉住 $\mu_0=\mu_1=0$;
   偶、奇两条递推分别仅留下 $\mu_2,\mu_3$ 一个自由参数.
   $T p_n$ 的系数结构为 ``三阶跳变'': 对 $n \geq4$,
   $$T p_n = c_0 x^n - A_n x^{n-2} + B_n x^{n-4},$$
   其中 $c_0>0$. 分别按每条奇偶递推的步数 $j\ge2$ 重编号后,
   要求 $B_j\ge0$ 且 $A_j-B_j\ge4j+c_0$.
2. 矩 $\mu_k = \langle g, x^k \rangle$ 满足 Cauchy-Schwarz 上界
   $|\mu_k| \le \|g\|_2 \sqrt{2/(2k+1)}$;

则 $\{p_n\}$ 在 $H$ 中解析完备. 机制: 正交条件 $\langle g, T p_n\rangle = 0$
化为递推 $c_0 \mu_n = A_n \mu_{n-2} - B_n \mu_{n-4}$; 缺次数 $d \in D$ 使
对应矩为自由参数, 但递推把这些矩向后传播为阶乘级增长序列, 与有界性矛盾,
故自由参数被迫为零, 全部矩为零, Weierstrass 稠密性给出 $g = 0$;
Hahn-Banach 推论给出完备性.

增长引理 (核心): $u_0=0, u_1=1$, $c_0 u_j = A_j u_{j-1} - B_j u_{j-2}$ 的解满足
$$u_j \geq (4/c_0)^{j-1} j!,$$
这里假设 $c_0>0$, $B_j\ge0$ 且 $A_j-B_j\ge4j+c_0$ 对每个 $j\ge2$ 成立.
证明: 先由较弱的 $A_j - B_j \geq c_0$ 归纳单调性 $0 < u_{j-1} \le u_j$,
再由比值 $r_j = u_j/u_{j-1} \geq (A_j - B_j)/c_0 \geq 4j/c_0$ 连乘.
注意: 逐项下界 $u_j \geq (A_j/c_0)u_{j-1}$ 一般**不**成立
例如偶数 Krein 递推取 $c=3$, $u_0=0,u_1=1$ 时,
$u_2=6,u_3=63,A_4=60,B_4=40$, 因而
$u_4=(60\cdot63-40\cdot6)/3=1180<1260=(A_4/3)u_3$.
必须用单调性 + 比值方法.

## 适用范围

- 适用: 多项式基 + 边界条件约束的 Hilbert 空间 (左定空间); 代数缺陷 (缺次数)
  不破坏解析完备性的情形; 等距同构 $T$ 使 $T p_n$ 为稀疏 (三系数) 多项式时.
- 边界情形: 单调性只需 $B_j\ge0$, $A_j-B_j\ge c_0$; 本卡阶乘下界需要
  更强的 $A_j-B_j\ge4j+c_0$. 缺次数须与自由参数
  一一对应; 等距同构与 $0 \notin \sigma$ 是关键前提.
- 不适用: 无等距结构的空间; $T p_n$ 系数稠密 (非三系数) 的基; 需要正交性
  (Schauder 基 / Riesz 基) 的更强结论 (本判据只给稠密性).
- 局限: 只判解析完备 (密度), 不构造显式正交系, 不给收敛速率.
- 推广范围 (2026-09-20): H3 用良定的 H1 矩, 再由谱截断得到同一族在 $0\le s\le3$ 中稠密.
  $p_4\notin H^s$ 对所有 $s\ge7/2$ 成立, 撤回旧任意阶推广; 第六轮的独立四迹图核证明已覆盖同族的整个 $0\le s<7/2$, 不把本卡矩跳跃方法未经验证地推广至新域. 精确阈值见 [[spectral-domain-checks]]. 见 [[left-definite-moment-recurrence]].

## 验证与备注

- 应用: 移位 Krein Laplacian 第二左定空间 $H^2[-1,1]$, 基
  $\{1, x, p_4, p_5, \dots\}$ ($p_{2n} = x^{2n} - \frac{n}{n-1}x^{2n-2}$),
  $T = K_c$, 缺次数 $\{2,3\}$. 结论: 解析完备 (是). 见
  `docs/SL_h2_completeness_proof.pdf`.
- 精确有理数验证 (c=1,3,5): 等距恒等式逐对精确成立; 增长下界对 $j\le24$ 成立;
  $x^2, x^3$ 投影残差超指数衰减到 0. 脚本: `scripts/num_h2_proof_check.py`.
- 文献: [4] Axioms 14 (2025) 115, Section 6 开放问题 (原文已核对,
  `papers/axioms14_115.pdf`).
