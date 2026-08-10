---
title: Krein-Sobolev 正交多项式
tags: [mathtool, left-definite, orthogonal-polynomials]
source: Littlejohn-Quintero-Roba 2025 (OPSFA-16, DOI 10.1007/978-3-031-90135-5_7); 姊妹论文 Jones-Littlejohn-Quintero Roba, Axioms 14 (2025) 115
status: 姊妹论文全文还原 (基准论文全文未获取)
created: 2026-08-04
---

# Krein-Sobolev 正交多项式

## 解析
移位 Krein Laplacian $K_c$ (边界 $f''(\pm1)=(f(1)-f(-1))/2$) 的第一左定空间为 $(H^1[-1,1],(\cdot,\cdot)_{1,c})$. 对其作 Gram-Schmidt 正交化得到 Krein-Sobolev 多项式 $\{K_n\}$: 在 $H^1$ 中完备正交, 根全实单且位于 $(-1,1)$; 偶次 $K_{2n}$ 与 Althammer (Sobolev-Legendre) 多项式重合; 显式系数由超几何求和给出; 对偶恒等式 $(f,g)_{1,c}=c\langle f,g\rangle_{1/c}$.

## 适用范围
- 适用: 左定空间中构造完备正交多项式基; 研究代数完备与解析完备的区别.
- 边界情形: $H^2[-1,1]$ (边界约束) 中多项式基 $\{p_n\}$ 缺 2,3 次项, 代数不完备; 其解析完备性是开放问题.
- 不适用: 不能直接用于特征值比值问题 (那是主题 2).

## 与完备性证明基 {p_n} 的区别 (重要)

完备性证明 (会话 9-10) 使用的稀疏基 {p_n} (p_{2n} = x^{2n} - n/(n-1)x^{2n-2}, 缺 2,3 次)
**不是** Krein-Sobolev 多项式 {K_n}: 例如 (p_4, p_6)_1 = 128/105 + 181c/693 != 0.
{p_n} 的选择动机是 K_c p_{2m} 为三系数跳变多项式 (矩跳跃机制), 而非正交性.
{K_n} 是 (H^1, (·,·)_1) 中 Gram-Schmidt 化单幂基的完备正交系.
对 s >= 2 的 H^s, 完备正交多项式系需经传输算子 K_c^{-floor(s/2)} 搬运
(见 [[left-definite-orthogonal-systems]]).

## 验证与备注
- 会话 2 依据 Axioms 姊妹论文完整还原; 基准论文全文受版权保护未获取.
- 详细公式: docs/SL_spectral_topics_summary.tex 主题一.

