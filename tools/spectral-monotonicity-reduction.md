---
title: 谱单调性归约
tags: [mathtool, self-developed]
source: 自研 (会话 5)
status: 定理已证
created: 2026-08-04
---

# 谱单调性归约

## 解析
固定 $\rho$, 特征值序列严格递增, 且 $n+1\le 2n$, 故
$$\lambda_{n+1}(\rho)\le\lambda_{2n}(\rho) \Rightarrow \frac{\lambda_{n+1}}{\lambda_n}\le\frac{\lambda_{2n}}{\lambda_n}.$$
与 [[mw-periodic-extension]] (Lemma 2: $\sup_\rho\lambda_{2n}/\lambda_n=\nu(R)$) 组合, 得相邻比值上确界定理:
$$\sup_{n\ge1}\sup_{1\le\rho\le R}\frac{\lambda_{n+1}}{\lambda_n}=\nu(R)=\left(\frac{\arccos(-\sqrt{R}/(\sqrt{R}+1))}{\arccos(\sqrt{R}/(\sqrt{R}+1))}\right)^2.$$

## 适用范围
- 适用: 上确界方向 (把相邻比值归约到倍指标比值); 与任何已知的 $\lambda_{2n}/\lambda_n$ 极值定理组合即可.
- 边界情形: 下确界方向不适用: $\inf\lambda_{n+1}/\lambda_n$ 与 $\inf\lambda_{2n}/\lambda_n$ 无关 (反例: R=4, $\lambda_5/\lambda_4=1.0838<\mu(4)=2.4092$).
- 不适用: 需要 $\lambda_{2n}/\lambda_n$ 极值已知; 对固定 $n$ 的最优常数 $c_n$ 不给出.

## 验证与备注
- 完整证明见 docs/SL_ratio_proof.tex (9 页总结: docs/SL_ratio_summary.tex).
- 依赖 MW Lemma 2 (文献引理, 未独立重证).
