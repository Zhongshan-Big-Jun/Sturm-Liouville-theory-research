---
title: 左定矩跳跃 (left-definite moment recurrence)
tags: [mathtool, self-developed, completeness, left-definite, moments]
source: 自研 (会话 10), H3 完备性证明的核心机制
status: 定理已证 + 精确有理数验证
created: 2026-08-04
---

# 左定矩跳跃 (Left-Definite Moment Recurrence)

## 解析

对正自伴算子 $K_c$ 的左定空间族 $H^s = D(K_c^{s/2})$ (见 [[left-definite-theory]]),
判定多项式基 $\{p_n\}$ 在 $H^s$ 中的解析完备性. 关键步骤:

1. 等距同构: $K_c^{s/2}: H^s \to L^2$ (或 $K_c: H^{s+2} \to H^s$), 完备性等价于
   $\{K_c^{s/2} p_n\}$ 在 $L^2$ (或 $\{K_c p_n\}$ 在 $H^s$) 中完备.
2. **多项式跳变与 $s$ 无关**: $K_c p_{2m} = c x^{2m} - A_m x^{2m-2}
   + B_m x^{2m-4}$ ($m \geq 2$; $A_m = 2m(2m-1)+\frac{cm}{m-1},
   B_m = 2m(2m-3)$, 奇次同理) 是**多项式恒等式**, 与所在空间 $H^s$ 无关.
   (更正: 会话 10 初版称 $K_c^{s/2} p_{2m}$ 也是三单项式结构; 该命题对
   $s \geq 4$ 不成立: $K_c^2 p_{2m}$ 有 4 项, $K_c^3 p_{2m}$ 有 5 项,
   数值证实. 正确机制是下面第 3 步的等距传输, 而非对 $K_c^{s/2}$ 取矩.)
3. **等距传输取矩**: 对 $w \in H^s$, 等距同构 $K_c: H^s \to H^{s-2}$
   给出 $(w, p_{2m})_s = (K_c w, K_c p_{2m})_{s-2}$. 置
   $v = K_c w \in H^{s-2}$, $M_k := (v, x^k)_{s-2}$ (取矩的内积与
   正交条件同源), 则正交条件化为与 $H^2$ 情形**完全相同**的二阶跳变递推
   $$c M_{2m} = A_m M_{2m-2} - B_m M_{2m-4}.$$
   边界项 (如 $w(1)\pm w(-1)$) 被 $M_k$ 定义中内积自带的边界项吸收,
   这是递推降阶 (三阶 $\to$ 二阶) 的机制.
4. 增长引理: $M_{2m} = M_2 u_m$, $u_m \geq (4/c)^{m-1} m!$ (见 [[moment-jump-completeness]]).
5. 矩上界: $|M_k| \leq \|v\|_{s-2}\,\|x^k\|_{s-2} \leq C_s k^{s-3/2}$
   (Cauchy-Schwarz; $\|x^k\|_t$ 多项式增长 $\sim k^{t-1/2}$),
   与超阶乘增长矛盾, 迫使 $M_2 = M_3 = 0$, 全部矩为零, $w = 0$,
   完备性得证.
6. 基始: $m=1$ 时 $M_2, M_3$ 为自由参数 (对应缺次数 2, 3), 恰为矛盾论证起点;
   $c > 0$ 本质 ($0 \notin \sigma(K_c)$), $B_m \geq 0$ 与
   $A_m - B_m \geq c$ 必须成立.
## 适用范围

- 适用: 边界条件约束 Hilbert 空间 (左定空间 $H^s$, $s \geq 1$ 整数) 中的多项式基;
  $K_c p_n$ 为三系数跳变结构的算子 (Krein 型); $0 \notin \sigma(K_c)$;
  等距传输 $K_c: H^t \to H^{t-2}$ 可用 (左定理论标准结论).
- 边界情形: $m=1$ 时 $M_2, M_3$ 为自由参数 (对应缺次数 2, 3), 恰为矛盾论证起点;
  $c > 0$ 本质; $B_m \geq 0$ 与 $A_m - B_m \geq c$ 必须成立;
  $s = 2$ 时 $t = s-2 = 0$ (即 $L^2$), 与 [[moment-jump-completeness]] 一致.
- 不适用: 无等距结构; $K_c p_n$ 非三系数; 需要 Schauder/Riesz 基等强于稠密性的结论;
  对 $K_c^{s/2} p_{2m}$ 直接取矩 (其单项式数随 $s$ 增长, $s \geq 4$ 失效).
- 与 [[moment-jump-completeness]] 的关系: 后者是 $s=2$ ($L^2$-矩) 的特例;
  本文把方法推广到一切整数 $s \geq 1$, 且指出``取矩的内积''是自由选择,
  应取与正交条件同源者以吸收边界项.

## 验证与备注

- 应用: 移位 Krein Laplacian 左定空间族 $H^s$ (一切整数 $s \geq 0$):
  结论解析完备 (是), 用 $H^{s-2}$-矩 + 等距传输路线 (本页第 3 步),
  取代会话 10 对 $K_c^{s/2}$ 直接取矩的错误思路.
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
