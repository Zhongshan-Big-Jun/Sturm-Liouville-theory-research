---
title: 三阶递推积分解理论 (third-order product-solution theory)
tags: [mathtool, self-developed, recurrence, poincare-perron, minimal-solution]
source: 自研 (会话 11, 方向 4), 路线 A 副产品系统化
status: 定理已证 + 符号/精确/高精度数值验证
created: 2026-08-05
---

# 三阶递推积分解理论 (Third-Order Recurrence Theory)

## 解析

三阶线性递推 $z_j = a_1(j)z_{j-1} + a_2(j)z_{j-2} + a_3(j)z_{j-3}$
(Poincar\'e 型, $a_i \to (2,-1,0)$, 极限特征根 $0,1,1$) 的显式结构理论,
来源为会话 10 路线 A 的 $L^2$-矩三阶系统
($z_j = \mu_j/((j!)^2(4/c)^j)$, $c > 0$). 四个结果:

1. **积分解分类**: $E_j(\beta) = \prod_{k=1}^j(1+\beta/(2k))$ 满足比值固定点
   恒等式 (等价地解递推, $j \geq 3$) 当且仅当偶次 $\beta \in \{1,-1\}$,
   奇次 $\beta \in \{3,1\}$. 证明: 有理恒等式通分 $\to$ $j$ 的多项式系数条件
   $\to$ $\beta$ 方程组 (sympy 求解).
2. **$\mu$-闭式**: 偶次 $\mu_j^+ = (2j+1)!/c^j$, $\mu_j^- = (2j)!/c^j$;
   奇次 $\mu_j^+ = (2j+3)!/(6(j+1)c^j)$, $\mu_j^- = (2j+1)!/c^j$;
   一切 $c > 0$, $j \geq 3$ 精确.
3. **精确降阶**: 已知解 $E$ 时, $s_j = z_j/E_j - z_{j-1}/E_{j-1}$ 满足二阶
   $s_j = A_j s_{j-1} + B_j s_{j-2}$, $A_j = -(a_2 E_{j-2} + a_3 E_{j-3})/E_j$,
   $B_j = -a_3 E_{j-3}/E_j$ (任意解 $z$, 奇偶, 精确).
4. **第三解与最小解**: 变差常数给第三基解的和式
   $s^{\mathrm{ind}}_j = s^-_j \sum_{k=2}^j w_k$, $w_j = -B_j(s^-_{j-2}/s^-_j)w_{j-1}$;
   向后迭代收敛到最小解 $h^*$ ($h^*_0 = 1$), 渐近
   $h^*_{j+1}/h^*_j = (c/4)/j^2 (1+O(1/j))$, $h^*_j = K(c/4)^j j^{-3}/(j!)^2(1+o(1))$.

## 适用范围

- 适用: 带显式积分解的 Poincar\'e 型三阶递推 (特征根含 $0$ 与重根时最小解
  构造); 路线 A 类 $L^2$-矩系统; 需要三个基解或最小解渐近的问题.
- 边界情形: $j=2$ 基始不满足积分解 (三阶递推初值自由, 标准现象);
  $E^+$/$E^-$ 的比值 $1/(2j+1)$ (偶) 与 $3/(2j+3)$ (奇) 给出 $s$-递推显式特解;
  Casoratian 非零.
- 不适用: 无积分解的一般三阶递推 (分类未完成); 需要最小解闭式
  ($K$ 常数未闭式化, 开放); 盒式归纳的退化配置排除 (路线 A 缺口, 开放).

## 验证与备注

- **更正**: 旧脚本 `scripts/h3_v56_odd_explicit.py` 第 (A) 段的 $s$-递推公式
  不正确 (精确复算 $j=3$ 即失败); 正确公式为本条目第 3 点. 该错误未进入
  任何已交付证明.
- 验证: $\beta$-分类符号级 (sympy) + 精确 ($j \leq 60$, $c \in \{1,3,10,100\}$);
  闭式精确 ($j \leq 30$); 降阶公式精确 ($j \leq 119$); 第三解残差
  $\leq 10^{-105}$; 最小解 $h^*_{20}$ 对 $N = 100,200,400$ 稳定到 12 位,
  组合拟合残差 $\leq 10^{-118}$; 局部指数 $\to -3$, $j^2$-比值 $\to c/4$.
- 脚本: `scripts/d4_third_order_theory.py`, `scripts/d4_verify2.py`,
  `scripts/d4_verify3.py`, `scripts/d4_verify4.py`.
- 文档: `docs/SL_third_order_recurrence_theory.pdf` (5 页, 零警告).
- 相关: [[left-definite-moment-recurrence]], [[moment-jump-completeness]].
- 开放: 最小解闭式与渐近常数 $K$; 一般系数族积分解分类;
  盒式归纳封闭 ($d_j \geq 0$ 的退化配置).

## 2026-08-22 更新: A6 root-1 高阶有理积分解排除 (RIGOROUS_PARTIAL_RESULT)

- **新结果 (论文级 partial, 独立审计 REPAIRABLE_GAP 已修复)**: 对 z-尺度三阶递推的
  root-1 分支 ($e_j \to 1$), 偶/奇两族与一切 $c>0$, 一切有理乘积比值 $e_j$ 的
  既约次数至多为 2; 因此不存在高次 (次数 > 2) 有理乘积解. 已知族 $E^{(\tau)}$
  与 $E^-$ 是 root-1 分支仅有的有理乘积比值.
- **机制**: 渐近分类 + 固定点恒等式的高阶对三角性 + 对径系数引理
  (偶 $D_m=2u-(m-1)$, 奇 $D_m=2u-(m+1)$) + 有理函数由无穷处 Laurent 展开唯一决定.
- **证据**: 候选证明
  `runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/candidate_proof.md`;
  独立审计 `runs/plugin-perf-eval/R-20260822T000000Z-a6-audit/audit_report.md`
  (0 fatal, 2 repairable, 已修复); 符号脚本
  `runs/plugin-perf-eval/R-20260822T000000Z-a6-reuse/reproducibility/verify_diagonal_coefficient.py`.
- **仍开放**: root-0/最小解分支的有理排除未成完整定理; 最小解闭式常数 $K$ 与
  盒式归纳源项控制仍开放 (原 A6 开放项).
