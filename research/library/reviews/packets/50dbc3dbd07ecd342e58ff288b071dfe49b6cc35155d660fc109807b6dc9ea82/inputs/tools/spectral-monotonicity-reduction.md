---
dependencies: [{"location": "tools/balanced-phase.md", "sha256": "9fe258e05102c0abb8b7552f61a500eb55c655592bdab8c8f8878a6ca19182ca"}, {"location": "tools/mw-periodic-extension.md", "sha256": "da8b28d2cf9c2014982cad4236fbe1fa35545d4a3900f86fb9993681d4500e84"}]
title: 谱单调性归约
source: docs/SL_ratio_proof.tex; docs/SL_mw_lemma_reproof.tex
status: 解析推论; 当前独立检验见第二轮报告
tags: [mathtool, self-developed]
created: 2026-08-04
---

# 谱单调性归约

对固定正密度, Dirichlet 特征值严格递增且为正. 对 n>=1,
`n+1<=2n` 给出 `lambda_(n+1)/lambda_n<=lambda_(2n)/lambda_n`.
令 `nu(R)=sup_(1<=rho<=R) lambda2/lambda1`.

MW 的截断与胞延拓证明 `sup_rho lambda_(2n)/lambda_n=nu(R)`.
因此 `sup_(n>=1) sup_rho lambda_(n+1)/lambda_n=nu(R)`,
其中下界直接取 n=1. 这是纯粹的归约, 尚未计算 nu(R).

另由 [[ratio-first-pair-variational]] 的全局首对证明及
[[balanced-phase]] 的候选谱计算, 才能代入
`nu(R)=((pi-theta)/theta)^2`, `theta=arccos(sqrt(R)/(sqrt(R)+1))`.
完整依赖为首对全局最优性 + 候选值 + MW 双向传递 + 谱单调性;
不能将候选达到和 doubling 恒等式循环用作首对全局上界.

适用于 R>=1 及有界正密度的相应可测、分段连续、有限阶梯类.
该结论的 n 是同时取上确界的指标, 不给固定 n>=2 的最优常数.
它也不提供相邻比值的下确界; 倍指标下界不能沿上述不等号倒推.
若同时对全部 n 取下确界, 常密度 rho=1 的比值 `((n+1)/n)^2` 趋于 1,
与简单谱的严格下界结合即得全序列下确界为 1, 有限 n 不取等.
本轮局部 Lean 已检查单调性归约的代数接口, 整个谱论链仍为解析证明.
