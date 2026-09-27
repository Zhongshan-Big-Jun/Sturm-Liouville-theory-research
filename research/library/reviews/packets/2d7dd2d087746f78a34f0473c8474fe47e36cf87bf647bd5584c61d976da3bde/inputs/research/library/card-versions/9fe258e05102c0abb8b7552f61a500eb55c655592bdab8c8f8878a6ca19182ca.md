---
dependencies: [{"location": "tools/ratio-first-pair-variational.md", "sha256": "0a92348158f098dd0114fecf3c5ed320476ed9bcafe42af97d7766695380b33a"}]
title: 平衡相位方法
source: docs/SL_ratio_proof.tex, balanced-phase calculation
status: 候选谱解析计算; 全局极值另依赖变分证明
tags: [mathtool, self-developed]
created: 2026-08-04
---

# 平衡相位方法

对 Dirichlet 权重问题 `-u''=lambda*rho*u`, 在长为 1 的区间上取
`R>=1`, `s=sqrt(R)`. 三个块相位均为 p 时, 转移矩阵给出候选谱:

- `[1,R,1]`, 块宽 `(s,1,s)/(2s+1)`: 令
  `theta=arccos(s/(s+1))`, 则
  `lambda1=((2s+1)*theta/s)^2`,
  `lambda2=((2s+1)*(pi-theta)/s)^2`,
  `C_plus=((pi-theta)/theta)^2`.
- `[R,1,R]`, 块宽 `(1,s,1)/(s+2)`: 令
  `phi=arccos(1/(s+1))`, 则
  `lambda1=((s+2)*phi/s)^2`,
  `lambda2=((s+2)*(pi-phi)/s)^2`,
  `C_minus=((pi-phi)/phi)^2`.

第一种的方程为 `sin(p)*((2s+1)*cos(p)^2-s^2*sin(p)^2)=0`;
第二种非整周期根满足 `tan(p)^2=s*(s+2)`. 须按零点数确认上述是首两个
特征值, 不能只选两个形式根. `R=1` 两式均给出 4.

这些计算直接证明候选值 C_plus/C_minus 被达到. 只有加入
[[ratio-first-pair-variational]] 的全局变分证明, 才能写
`nu(R)=C_plus`, `mu(R)=C_minus`. MW 倍指标传递本身不能补出这个全局上界.

适用: 平衡两跳候选的闭式谱; 非平衡或非对称配置须重新求 secular 方程.
高阶根必须按 Sturm 指标排序, 不可套用 `lambda_k=k^2*lambda1`.
历史数值脚本 `scripts/num_formula.py` 仅为辅助, 本轮未用其输出代替解析证明.
历史交接中 `sqrt(lambda1)=2*(s+1)*phi/s` 是错误的, 正式值为上列 `(s+2)*phi/s`.
当前独立检验见 [第二轮报告](../reports/proof-audit-round2-20260920/REPORT.md).
