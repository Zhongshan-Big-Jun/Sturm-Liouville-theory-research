---
title: MW 周期延拓与倍指标恒等式
tags: [mathtool, extremal]
source: Mahar-Willner 1976, CPAM 29, DOI 10.1002/cpa.3160290505
status: 数值复现 (1e-8)
created: 2026-08-04
---

# MW 周期延拓与倍指标恒等式

## 解析
若 $\phi_0$ 极值化 $\lambda_2/\lambda_1$, 定义 $\phi_n(x)=\phi_0\bigl(n(x+1/2)-1/2\bigr)$ 并以周期 $1/n$ 延拓到 $[-1/2,1/2]$, 则
$$\frac{\lambda_{2n}(\phi_n)}{\lambda_n(\phi_n)}=\frac{\lambda_2(\phi_0)}{\lambda_1(\phi_0)},$$
且 (合并胞界后) $\lambda_n=n^2\lambda_1^{(\text{cell})}$, $\lambda_{2n}=n^2\lambda_2^{(\text{cell})}$. 由此 MW 定理 3: $\phi_n$ 极值化 $\lambda_{2n}/\lambda_n$ (与 $\phi_0$ 同方向).

## 适用范围
- 适用: 把 $\lambda_{2n}/\lambda_n$ 的极值化归到 $\lambda_2/\lambda_1$; 与 [[spectral-monotonicity-reduction]] 组合得到相邻比值上确界定理.
- 边界情形: 胞元边界同值块必须合并 (见 [[cell-merging]]), 否则出现伪跳点.
- 平方律仅对 $k=1,2$ 成立: $\lambda_{kn}\ne k^2\lambda_n$ 对 $k\ge3$, 不可外推.
- 不适用: 相邻指标 $\lambda_{n+1}/\lambda_n$ (n>=2); MW 定理不覆盖相邻比值.

## 验证与备注
- 会话 5: R=4 时 $\lambda_{2n}/\lambda_n=\nu(4)=7.48153339$ 对 n=1..6 (1e-8), 见 `scripts/num_mw_ext.py`.
- 文献: mw1976.pdf (papers/).
