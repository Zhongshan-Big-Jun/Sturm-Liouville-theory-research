---
title: 首对谱比值的全局变分极值证明
source: docs/SL_ratio_proof.tex, first-pair global extremal structure
status: 解析证明; 当前独立检验见第二轮报告
tags: [mathtool, variational, extremal, correction]
created: 2026-09-20
---

# 首对谱比值的全局变分极值证明

在长为 1 的区间上考虑 Dirichlet 问题 `-u''=lambda*rho*u`,
`1<=rho<=R`, `R>1`. 允许有界可测密度, 按几乎处处相等识别.
令 `s=sqrt(R)`. 首对比值的最大者为 `[1,R,1]`, 块宽为
`(s,1,s)/(2s+1)`; 最小者为 `[R,1,R]`, 块宽为 `(1,s,1)/(s+2)`.
区间中心固定时, 两个极值密度各自按 a.e. 意义唯一. `R=1` 单独给出比值 4.

可以复用的证明结构:

1. 密度盒类 weak* 紧. 在 H1_0 上用
   `a(T_rho u,v)=integral rho*u*v` 定义紧正算子. 单位球在连续函数空间的紧嵌入
   将 weak* 收敛升级为 T_rho 的算子范数收敛, 从而极值存在.
2. 按 `integral rho*u_i^2=1` 归一化. 首变分
   `d log(lambda2/lambda1)[h]=integral h*(u1^2-u2^2)` 给出 bang-bang 条件.
   取 u1>0, u2 在左端为正, Wronskian 说明 `u2/u1` 严格下降, 两个切换点来自
   `u2/u1=1,-1`; 不能仅从某个候选被达到跳到全局最优.
3. 写 `F=u1^2-u2^2`, 取分段线性 g 使 `g'(F)=rho` 且 `g(F)=rho*F`.
   能量 `E=u1'^2/lambda1-u2'^2/lambda2+g(F)` 的导数 a.e. 为零;
   归一化及分部积分给出 `integral E=0`, 因而 E 恒为零.
4. 端点斜率关系、切换点两模态的等振幅与导数匹配推出两外块等宽,
   再推出每块相位相等. 完整分支范围与唯一性计算见源证明.
5. 最后才用 [[balanced-phase]] 中的三角计算求极值常数.
   有界可测、分段连续及有限阶梯密度的极值相同, 由保界逼近和谱连续性说明.

源证明是解析论证. 局部 Lean 的候选达到、上确界和缩放引理不替代这里的
紧性、首变分及全局最优性证明. 本卡不推出固定 n>=2 的相邻比值极值.
复核及纠错记录见 [第二轮报告](../reports/proof-audit-round2-20260920/REPORT.md).
