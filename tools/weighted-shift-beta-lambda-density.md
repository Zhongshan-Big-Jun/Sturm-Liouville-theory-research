---
slug: weighted-shift-beta-lambda-density
title: 加权移位族 H_{beta,lambda} 的稀疏族稠密性判据
tags: [稠密性, 非对角, 加权移位, O1']
status: STRICT (RIGOROUS_PARTIAL_RESULT, 一般 O1' 仍开放)
source: R-20260823T000000Z-o1p-lightreuse (plugin perf eval round 3)
related: ["[[constrained-denseness-runs]]", "[[denseness-criteria]]", "[[moment-jump-completeness]]"]
---

# 加权移位族 H_{beta,lambda} 的稀疏族稠密性判据

## 解析

设 beta >= 0, |lambda| < 1, 实 l^2(N_0) 中

    x^k = (k+1)^beta e_k + lambda e_{k+1}.

对有限多项式 representer, O1' 的判定为

    closure(span Q_sp) = V  <=>  ker(T|B_adm) = {0},

其中 B_adm 包含所有有限游程自由基, 并且当且仅当 beta > 3/2 时还包含无穷游程
自由基 (此时无穷游程矩向量可实现在 H_{beta,lambda} 中).

## 与已有子类的关系

- lambda = 0 回归对角 H_beta; beta > 3/2 的无穷游程可实现性门槛与
  H_beta 已知结果一致.
- beta = 0 回归 H_lambda (带宽 1); B_adm 退化为 B_fin.
- 该族与稳定带 Toeplitz 族 H_shift(m,lambda) 互补:
  H_shift 拓宽移位带宽但在稳定 Toeplitz 可逆矩映射下工作;
  H_{beta,lambda} 在对角加权下允许无界矩映射, 但带宽仍为 1.

## 验证状态

- 独立审计 (R-20260823T010000Z-o1p-audit): REPAIRABLE_GAP 1 处 (Lemma 3
  渐近/可实现性证明不严), 已由 repair agent 修复为严格双端估计 + 收敛性证明.
  Baseline 部分审计无缺口.
- Lean scaffold: 见 lean-proof/SL/DensBCO1p3WeightedShift_Scaffold.lean (sorry, 未验证).
- 证据: candidate_proof.md (run R-20260823T000000Z-o1p-lightreuse),
  audit_report.md, reuse_summary.md.
