---
title: 比值能量不变量 ratio-energy-invariant
tags: [mathtool, self-developed, extremal, ratio, nge2]
source: 自研 (run R-20260822T220000Z-b3-baseline)
status: 定理已证 (STRICT)
created: 2026-08-22
---

# 比值能量不变量 (ratio-energy-invariant)

## 解析

对 Dirichlet 弦 `-u'' = lambda rho u`, `u(0)=u(1)=0`, `1<=rho<=R` 和固定 n,
定义比 `Lambda_n = lambda_{n+1}/lambda_n`。设 `u_n,u_{n+1}` 按
`int rho u_k^2 = 1`, `u_k'(0)>0` 归一化。令

    H = u_n^2 - u_{n+1}^2.

Feynman-Hellmann 给出

    d/deps Lambda_n(rho+eps h) = Lambda_n(rho) int h H dx.

因此在盒约束下, 全局极大子满足完全饱和:
`H>0 -> rho=R`, `H<0 -> rho=1`。

在常密度块 r 上, 定义

    E = b(u_n'^2 + a r u_n^2) - a(u_{n+1}'^2 + b r u_{n+1}^2),
    a=lambda_n, b=lambda_{n+1}.

E 在块内为常数。由于极值子开关处 H=0, E 在开关处无跳跃, 故 E 全局常数。
积分并用 `int rho u_k^2=1`, `int u_k'^2=lambda_k` 得 `E=0`。端点给

    |u_{n+1}'(0)/u_n'(0)| = |u_{n+1}'(1)/u_n'(1)| = sqrt(b/a).

配合定向给出 `q0 = 1/c`, `q1 = -1/c` (`c=sqrt(a/b)`), 从而 H 的零点数收紧为
`2n`, 每个全局比值极大子为 `[1,R,1,...,1]` 的 2n 开关 bang-bang 配置。

## 适用范围

- 适用: 固定 n 比值极大子结构; 任意可测盒权; Dirichlet 边界; R>1.
- 不适用: 非盒约束; 比值极小子结构 (需要符号反转, 但能量不变仍可用于类似分析);
  未给出开关位置/块长或最优值.

## 验证与备注

- 推导 STRICT; 数值 EVIDENCE (R=2,4,10, n=1..5): q0=1/c, q1=-1/c 到显示精度;
  E 近似常数且接近 0; H 内部零点数 2n.
- 脚本: runs/plugin-perf-eval2/R-20260822T220000Z-b3-baseline/probe_ratio_structure3.py,
  verify_ratio_invariant.py.

## 独立审计 (2026-08-22)

- Audit: `runs/plugin-perf-eval2/R-20260822T230000Z-b3-audit/audit_report.md`
  (Part A no repair needed; Part B repaired in baseline proof).
