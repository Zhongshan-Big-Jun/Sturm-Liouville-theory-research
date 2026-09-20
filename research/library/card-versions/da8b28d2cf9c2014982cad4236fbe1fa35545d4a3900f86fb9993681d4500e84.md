---
dependencies: [{"location": "tools/mw-zero-truncation.md", "sha256": "cd7de9d255facefed91efe8e5070f743462b268cdc55027da66c40018d53d25d"}]
title: MW 有符号胞延拓与倍指标传递
source: Mahar-Willner 1976; docs/SL_mw_lemma_reproof.tex
status: 解析重证; 当前独立检验见第二轮报告
tags: [mathtool, extremal]
created: 2026-08-04
---

# MW 有符号胞延拓与倍指标传递

在 `I=[-1/2,1/2]` 取正的有界密度 rho0, 将其压缩并重复 n 次得到 rhon.
对 rho0 的任意第 k 个 Dirichlet 特征函数 y, 令
`L=y'(-1/2)`, `R=y'(1/2)`, `b=R/L`. 两个端点斜率均非零.
第 j 个胞左端为 xj, 在该胞定义
`u_j(x)=b^j*y(n*(x-xj)-1/2)`, j=0,...,n-1.

胞界处函数值都为 0, 左右导数分别为 `n*b^j*R` 与 `n*b^(j+1)*L`,
因此匹配. b 必须保留符号; 不能改为 `-R/L` 或 `abs(R/L)`.
仿射拉回使特征值乘 n². 各胞内部共 n*(k-1) 个零点, 再加 n-1 个胞界,
由 Sturm 振荡得到对每个 k,n>=1 的精确恒等式
`lambda_(kn)(rhon)=n^2*lambda_k(rho0)`.

尤其 `lambda_(2n)(rhon)/lambda_n(rhon)=lambda2(rho0)/lambda1(rho0)`.
这是候选达到方向. 与 [[mw-zero-truncation]] 对任意密度的反向不等式结合,
才得到倍指标比值的全局极值等于首对极值.

这里 n² 是空间压缩因子; **不推出** `lambda_(kn)=k²*lambda_n`.
旧卡把两种平方律混淆并错误限制为 k=1,2, 已撤回.
第一、第二模态均适用有符号传输, 常密度第二模态给 b=1.
同值块可以合并以正确计跳点, 见 [[cell-merging]].
此构造不直接证明 n>=2 时相邻指标比值的极值.
