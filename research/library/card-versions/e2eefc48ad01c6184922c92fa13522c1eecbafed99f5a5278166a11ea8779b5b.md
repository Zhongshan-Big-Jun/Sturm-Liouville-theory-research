---
title: 转移矩阵与 secular 方程
tags: [mathtool, spectral]
source: 经典数值方法
status: 已验证 (本项目全部数值)
created: 2026-08-04
---

# 转移矩阵与 secular 方程

## 解析
对分段常值系数问题 $-y''=\lambda\rho y$, 在每块 $\rho\equiv c$ (宽度 $w$) 上, 相位 $q=\sqrt{\lambda c}\,w$, 传播矩阵
$$T(q;\lambda,c)=\begin{pmatrix}\cos q & \sin q/\sqrt{\lambda c}\\ -\sqrt{\lambda c}\sin q & \cos q\end{pmatrix}$$
把块左端的 $(y,y')$ 映射到块右端. 总矩阵为各块矩阵按顺序之积, Dirichlet 条件 $y(1)=0$ 等价于总矩阵的 $(0,1)$ 元素为零 (secular 方程). 数值上对 $s=\sqrt{\lambda}$ 做网格扫描找变号点, 再逐根二分加密.

## 适用范围
- 适用: 分段常值 (两值/多值阶梯) 密度与势; 特征值定位与比值计算; 周期结构 (胞元乘积).
- 边界情形: 高指标特征值需要更细网格与更多次二分 (本项目用 `num_*.py`, 见 [[cell-merging]] 中网格伪值教训).
- 不适用: 光滑系数问题的直接闭式; 此时宜用 Liouville 变换或打靶法.

## 验证与备注
- 复现 $\nu(R), \mu(R)$ 闭式至 8 位小数 (R=1.5..100); 角度恒等式至 1e-15.
- 脚本: `scripts/num_formula.py`, `scripts/num_mw_ext.py`.
