---
title: 左定传输正交系 (left-definite transfer orthogonal systems)
tags: [mathtool, self-developed, left-definite, orthogonal-polynomials, completeness]
source: 自研 (会话 11), 方向 1: H^s 显式完备正交多项式系
status: 定理已证 + 855 项精确有理数验证
created: 2026-08-05
---

# 左定传输正交系 (Left-Definite Transfer Orthogonal Systems)

## 解析

对移位 Krein Laplacian $K_c$ (边界 $f'(\pm1)=(f(1)-f(-1))/2$) 的每个整数阶左定
空间 $(H^s, (\cdot,\cdot)_s)$, 显式构造完备正交多项式系 (后续方向 1). 关键机制
是**传输**: 左定内积满足
$$(f,g)_{2r} = (K_c^r f, K_c^r g)_{L^2}, \qquad (f,g)_{2r+1} = (K_c^r f, K_c^r g)_1,$$
且 $K_c^{-1}$ 是多项式空间 $\Pi$ 上的显式三角算子 (形式幂级数,
$K_c^{-r} = c^{-r}(1-c^{-1}D^2)^{-r} = c^{-r}\sum_j \binom{r+j-1}{j}c^{-j}D^{2j}$):
$$K_c^{-r} x^k = \sum_{j=0}^{\lfloor k/2 \rfloor} \binom{r+j-1}{j} c^{-(r+j)} \frac{k!}{(k-2j)!}\, x^{k-2j}.$$

**主定理**: 对整数 $s \geq 1$,
- $s = 2r$ (偶): $Q_n^{(2r)} := K_c^{-r} P_n$ (Legendre), 完备正交,
  $\|Q_n\|_s^2 = 2/(2n+1)$;
- $s = 2r+1$ (奇): $Q_n^{(2r+1)} := K_c^{-r} K_n$ (Krein-Sobolev), 完备正交,
  $\|Q_n\|_s^2 = (2c/(2n+1)) a_n a_{n+2}$ ($a$ 系数见 [[krein-sobolev-polynomials]]).

系数全为闭式: Legendre 显式系数 + Krein-Sobolev 超几何系数 + $K_c^{-r}$ 单和公式
(有限双重和). 证明: 等距同构 $K_c^r: H^{2r} \to L^2$ (偶) 与 $K_c^r: H^{2r+1}
\to H^1$ (奇) 把基底正交系 (Legendre / Krein-Sobolev) 搬运到目标空间.

**根的行为** (重要, 诚实结论): 实根性质 ($s=1$ 时根全实单于 $(-1,1)$,
文献 [2, Theorem 4]) 不随 $s$ 保持. 精确命题 ($s=2$, $n=4$): $Q_4^{(2)}$ 的根
当 $0<c<c_1$ 为纯虚, $c_1<c<c_2$ 为非实复根, $c>c_2$ 为 $(-1,1)$ 内四实根,
其中 $c_1 = (35-7\sqrt{15})/2 \approx 3.944$, $c_2 = (35+7\sqrt{15})/2
\approx 31.055$ (判别式 + Vieta 符号精确推导). 大 $c$ 时 $K_c^{-1} \approx
\mathrm{id}/c$, 实根性恢复 (扰动论). 数值: $s \in \{2,3,4\}$,
$n \in \{4,6,8\}$, $c \in \{1,3,10\}$ 均无实根.

## 适用范围

- 适用: 左定空间族 $H^s$ 中构造显式完备正交多项式系; 回答"同一组多项式能否在
  一切 $H^s$ 中完备正交" (答案: 不能, 系随 $s$ 变化); 与问题 1 的多项式方向对接.
- 边界情形: $r=0$ 还原文献 ($s=1$ Krein-Sobolev; $s=0$ 即 Legendre);
  $c>0$ 本质 (正定性, $0 \notin \sigma$); $\deg Q_n = n$ 保证三角性与唯一性
  (度分次正交多项式系唯一, 差常数因子).
- 不适用: 无等距结构的空间; 需要根在区间内实的强结论 ($s \geq 2$ 一般不成立);
  非多项式算子 ($K_c^{-r}$ 的闭式依赖 $K_c$ 保持 $\Pi$ 不变).
- 局限: 根行为的完整刻画 ($s \geq 2$ 一般 $n$) 未完成, 仅精确 $n=4, s=2$ 与
  数值证据; 与 [[moment-jump-completeness]] 的区别: 该工具只判稠密 (不完备), 
  本工具给出显式完备正交系.

## 验证与备注

- 精确有理数 855 项检查全过 (脚本 `scripts/orthogonal_systems_verify.py`):
  $K_c^{-r}$ 公式 ($c \in \{1,3,5\}$, $r \le 3$, $k \le 8$); $a$ 闭式 vs 递推
  ($m \le 11$, $c \in \{1,3,5,10\}$); 正交性与范数 ($s \le 4$, $n \le 8$,
  $c \in \{1,3,5\}$); 还原论文 $s=1$ 前几项; 偶阶闭式 (15).
- 根实验: numpy, $s=1$ 全实根于 $(-1,1)$; $s \geq 2$ 无实根; 阈值 $c_1, c_2$
  数值一致.
- 文档: `docs/SL_hs_orthogonal_systems_proof.pdf` (7 页, 零警告).
- 前序工具: [[left-definite-theory]], [[krein-sobolev-polynomials]],
  [[moment-jump-completeness]], [[left-definite-moment-recurrence]].
