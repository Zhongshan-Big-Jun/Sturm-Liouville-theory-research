---
canonical_key: gap extremal reduction to two-parameter barrier/well families (Dirichlet string, box class 1<=rho<=R)
title: 两块族归约定理 (gap-n1 reduction)
tags: [mathtool, self-developed, reduction]
source: 自研 (O1, run R-20260805T000000Z-gapn1-a1b2c3)
status: CANDIDATE_COMPLETE_PROOF (2026-08-06 修复并自审, run R-20260806T140000Z-o1revise-2ED02A; 独立复审 Lemma 1/3 为关闭前置步骤); 前审计: R-20260806T011500Z-o1audit-422A69
created: 2026-08-05
---

# 两块族归约定理 (gap-n1-reduction)

## 解析
对 Dirichlet 弦 $-y''=\lambda\rho y$ ($y(0)=y(1)=0$, $1\le\rho\le R$ a.e.),
相邻间距 $D(\rho)=\lambda_2-\lambda_1$ 的上下确界可归约到两块密度族:

$$S(R)=\sup_{\rho}D(\rho)=\max_{0\le a\le b\le 1}D(\rho=R\text{ on }(a,b),\ 1\text{ 其余}),$$
$$I(R)=\inf_{\rho}D(\rho)=\min_{0\le a\le b\le 1}D(\rho=1\text{ on }(a,b),\ R\text{ 其余}).$$

## 证明机制 (七步)
1. **L1 连续性** (2026-08-06 修复, R1): $T_\rho=T_0M_\rho$ 在 $L^2$ 上非自伴, 不能直接套 Weyl; 改用对称 Hilbert-Schmidt 算子
   $S_\rho=M_{\sqrt{\rho}}T_0M_{\sqrt{\rho}}$ (核 $\sqrt{\rho(x)}G(x,t)\sqrt{\rho(t)}$, $G=\min(x,t)(1-\max(x,t))$),
   $S_\rho$ 与 $T_\rho$ 相似 (共轭 $M_{\sqrt{\rho}}$), $\mu_k(S_\rho)=1/\lambda_k(\rho)$; 由
   $\|S_\rho-S_\sigma\|_{HS}\le (R/4)\|\rho-\sigma\|_1^{1/2}$ (核展开 + $G\le 1/4$ + $\|\rho-\sigma\|_2^2\le R\|\rho-\sigma\|_1$) 与 Weyl,
   $\lambda_k$ 在 $L^1$ 拓扑连续 (模 $|\lambda_k(\rho)-\lambda_k(\sigma)|\le (R/4)(k\pi)^4\|\rho-\sigma\|_1^{1/2}$).
2. **N 跳紧性**: $\mathcal{K}_N$ 为闭单纯形与 $[1,R]^{N+1}$ 的连续像, 极值存在.
3. **FH 移动跳点**: 把 $x_j$ 处由 $c_-$ 到 $c_+$ 的跳点向右移动 $\varepsilon$,
   $dD/d\varepsilon|_0=-(c_+-c_-)f(x_j)$ (向左移动取 $+$), $f=\lambda_1u_1^2-\lambda_2u_2^2$.
   更正记录: 2026-08-06 审计 (R-20260806T011500Z-o1audit-422A69) 发现草稿符号相反; 零条件 $f(x_j)=0$ 不受影响.
   修复 R2/R4 (run R-20260806T140000Z-o1revise-2ED02A): 公式经平滑逼近 (AEH Lemma 2.1 + Dirac 族极限) 严格证明,
   $\varepsilon\mapsto D(\rho_\varepsilon)$ 的双侧导数在每个跳点存在 (审计括号 "仅当 f=0 时存在" 不精确); 向右/向左距离导数异号除非 $f(x_j)=0$.
4. **f 的结构** (Wronskian): $v=u_2/u_1$ 严格递减 (与 $\rho$ 无关), 故 $f$ 至多两零点,
   $\{f>0\}$ 为单区间.
5. **极值点至多两跳**: 每个有效跳点是 $f$ 的零点, 至多两个.
6. **阶梯稠密**: $M_N\to\sup_{\mathcal{K}}D$.
7. **bang-bang**: 全局极值点在 $\{f>0\}$ 取 $\rho=R$, $\{f<0\}$ 取 $\rho=1$
   (INF 相反), 由单区间性得单垒/单阱两块配置.

## 适用范围
- 适用: 逐点界类 $1\le\rho\le R$ 的 Dirichlet 弦, 前两个特征值间距 (及推广到
  $\lambda_{k+1}-\lambda_k$ 时需重证 f 的单区间结构); 与 [[keller-variational]],
  [[bang-bang]], [[single-well-intersection]] 配合.
- 边界情形: 两块族退化成员 ($a=0$, $b=1$, $a=b$) 在闭族内被自动覆盖.
- 不适用: 有质量/范数约束的类 ($L^p$ 球, MDE), 极值可含原子测度; 见 [[mde-extremal]].
- 注意: 归约只给出族上的极值, 不给出块内极值点的对称性/唯一性 (那是 O2/O3a 的义务).

## 验证与备注
- 来源: run R-20260805T000000Z-gapn1-a1b2c3 的 O1_reduction_draft.md (PROVED 草稿,
  各步均为初等论证; O1c Wronskian 一步与 AEH arXiv:2407.02459 Lemma 2.2 独立重导).
- 数值佐证: 对 $R\in\{1.05,\dots,1000\}$ 全景观测 SUP/INF 唯一临界点均在对称点, 无反例.
- 上游审计: 2026-08-06 独立逐行审计完成 (run R-20260806T011500Z-o1audit-422A69): O1a PARTIAL (T_rho 在 L^2 上非自伴, 需 S_rho 修正), O1b FAILED 如陈述 (符号错, 后果仍真), O1c-O1f PROVED; 总体 REPAIRABLE_GAP, 定理本身为真. 见该 run 的 audit_report.md.
- 修复与自审 (2026-08-06, run R-20260806T140000Z-o1revise-2ED02A): 重导全部七步; 自审发现并修复 F-001 (第 1 步 HS 常数推导一行算术错, 正确链为 (R/32)(||A||_2^2+||A||_1^2) <= (R^2/16)||A||_1, 最终界 (R/4)||A||_1^{1/2} 不变); 数值组 verify_*.py 全过, bangbang 与 smoothing 复跑逐位一致; 审计报告见该 run 的 audit_report.md, 状态 CANDIDATE_COMPLETE_PROOF (独立复审 Lemma 1/3 为关闭义务 O1 的前置步骤).
