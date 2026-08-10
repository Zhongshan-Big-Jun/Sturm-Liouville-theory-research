---
title: FH 带特征值因子 + Hessian/分支斜率归约 (fh-hessian-branch-reduction)
tags: [mathtool, self-developed]
source: 自研 (O3a, run R-20260806T011500Z-o3abranch-E8E56F)
status: 定理已证 (P1, P2, P3) + 数值/区间验证; 全局负定性被否证
created: 2026-08-06
---

# FH 带特征值因子 + Hessian/分支斜率归约 (fh-hessian-branch-reduction)

## 解析
对 Dirichlet 弦 -y'' = lambda*rho*y (y(0)=y(1)=0) 与归一化
int rho u^2 = 1 (u 为 L^2(rho)-归一化特征函数), 微扰
rho_eps = 1 + eps*chi_(a,b) 的 Feynman-Hellmann 公式必须带特征值因子:

    d lambda_k / d eps = -lambda_k * int (d rho/d eps) u_k^2 dx.

对跳变族 rho_(a,b) = R 于 (a,b), 1 于其余处:

    d lambda_k/da = (R-1) lambda_k u_k(a)^2,
    d lambda_k/db = -(R-1) lambda_k u_k(b)^2.

于是 D = lambda_2 - lambda_1 满足 dD/da = -(R-1) R1, dD/db = +(R-1) R2,
其中 R1 = f(a), R2 = f(b), f = lambda_1 u_1^2 - lambda_2 u_2^2. 这是 T3
(残差闭合恒等式 dR1/db = -dR2/da, 见 [[residual-exactness]]) 的前提.

在好根 (R1 = R2 = 0) 处, 令 A = dR1/da, B = dR2/da, C = dR2/db:

- A = -D_aa/(R-1), B = D_ab/(R-1), C = D_bb/(R-1);
- 分支斜率 g1' = A/B = -D_aa/D_ab, g2' = -B/C = -D_ab/D_bb,
  h' = g1' - g2' = -D_aa/D_ab + D_ab/D_bb;
- 若 D_aa < 0, D_bb < 0, D_ab > 0, D_aa*D_bb > D_ab^2 (即 D 的 Hessian
  在该点负定), 则 g1' > g2' > 0;
- 在对称不动点 (a, 1-a) 处由反射不变性 A = -C, 故 g1'*g2' = 1.

## 适用范围
- 适用: 跳变族上临界点的局部结构 (斜率分裂, 分支交点计数); 把分支单调性归约到
  二阶谱量 (第二阶敏感性问题) 的代数框架.
- 边界情形: 需要 D 为 C^2 (谱单重 + secular 实解析), 以及分母 D_ab != 0,
  D_bb != 0.
- 不适用 (本 run 的否证): D 的 Hessian 并非在整个三角域上负定 (小 a 附近
  D_bb > 0 有违例), 所以全局 Hessian 论证不成立; 只能做分支限制符号论证. 而且
  分支上的 h' = g1' - g2' 在 R >= ~1350 时会变负 (O3a Lemma A 被证伪, 见
  [[interval-ad-certificate]] 与 run 的 counterexample_log CE-1).

## 验证与备注
- 来源: run R-20260806T011500Z-o3abranch-E8E56F 的 P1-P3 (candidate_proof.md),
  含完整推导; FH 数值验证 (0.42, 0.56, R=4) 处 d lambda_1/da = 16.739,
  d lambda_2/da = 55.627 (FD 一致, 1e-6).
- 教训: 无特征值因子的朴素 FH 公式是错的 (初版自测矛盾, ledger R-101); 必须用
  -lambda_k * int rho_eps u_k^2.
- 相关: [[residual-exactness]], [[gap-n1-reduction]]; 脚本
  runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/reproducibility/audit_fh_t3.py,
  audit3_hessian.py, closed_deriv.py.