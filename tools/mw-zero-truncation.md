---
title: 零点截断归纳
tags: [mathtool, extremal]
source: Mahar-Willner 1976 Lemma 2
status: 文献引用 (未独立重证)
created: 2026-08-04
---

# 零点截断归纳

## 解析
对极值化 $\lambda_{2(k+1)}/\lambda_{k+1}$ 的配置, 取 $\lambda_{k+1}$ 特征函数的第一个内零点 $z_0$ 与 $\lambda_{2(k+1)}$ 特征函数的相应零点, 用零点切出子区间构造新的边值问题, 再经仿射变换 $L(x)=\frac{2}{1+2z_0}(x+1/2)-1/2$ 拉回标准区间. 归纳得
$$\mu_{2n,n}(a)=\mu(a), \qquad \nu_{2n,n}(a)=\nu(a),$$
即 $\lambda_{2n}/\lambda_n$ 的极值常数与 $\lambda_2/\lambda_1$ 相同.

## 适用范围
- 适用: 倍指标比值的极值常数传递; 是 MW Lemma 2 的核心机制.
- 边界情形: 依赖 Sturm 零点计数 ([[sturm-oscillation]]); 两种情形 $z_0\le z_1$ 与 $z_1<z_0$ 分别处理.
- 不适用: 未证明可直接推广到相邻指标; 本项目上确界定理依赖此引理 (文献引用, 待独立重证).

## 验证与备注
- 结论由 [[mw-periodic-extension]] 的数值复现间接支持; 引理本身未在本项目内重证 (会话 5 待办).
- 文献: mw1976.txt (papers/), Section 5.
