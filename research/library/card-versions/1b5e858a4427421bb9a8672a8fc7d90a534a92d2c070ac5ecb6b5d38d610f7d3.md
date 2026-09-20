---
title: Morales-Ramis 理论与 Kovacic 算法
tags: [mathtool, extremal]
source: 微分 Galois 理论; 应用于 Tian-Zhang arXiv:2509.09250
status: 文献引用
created: 2026-08-04
---

# Morales-Ramis 理论与 Kovacic 算法

## 解析
Morales-Ramis 定理: 若带 Hamilton 结构的一阶变分方程系统亚纯可积, 则其线性化系统沿解曲线的微分 Galois 群必可解. Kovacic 算法判定二阶线性微分方程
$$y''+r(x)y=0$$
是否具有 Liouville 可解解 (通过计算 Galois 群的可能约化形式). 两者组合可证明特征值和优化临界系统非可积.

## 适用范围
- 适用: 证明极值问题临界系统 (特征值和优化的 Euler-Lagrange 系统) 非可积, 从而排除解析积分途径; Tian-Zhang 2026 用于 SL 谱优化.
- 边界情形: 只证非可积, 不给出谱信息; 需要先把问题化为标准 Hamiltonian 形式.
- 不适用: 直接用于本项目逐点夹逼类的极值刻画 (该类由变分+结构定理处理).

## 验证与备注
- 会话 1-2 检索记录; 相关综述见 docs/SL_spectral_topics_summary.tex 文末知识板块.
