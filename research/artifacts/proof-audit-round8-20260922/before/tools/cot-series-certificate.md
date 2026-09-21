---
title: 余切级数余项证书
tags: [mathtool, analysis]
source: 自研 (会话 30)
status: 已证 (级数正系数 + 区间值)
created: 2026-08-07
---

# 余切级数余项证书 (cot-series-certificate)

## 解析
$\cot$ 的 Laurent 展开 $\cot z=1/z-\sum_{k\ge1}c_kz^{2k+1}$, $c_k=2^{2k}|B_{2k}|/(2k)!>0$. 令 $R(z)=1/z-\cot z=\sum c_kz^{2k+1}$. 则 $R(z)/z=\sum c_kz^{2k}$ 在 $(0,\pi)$ 上严格递增, 故对 $z\in[0,\pi/8]$:

    R(z) <= z * R(pi/8)/(pi/8) =: z Cz,
    Cz = (8/pi - (1+sqrt(2))) / (pi/8) = 0.33681139899.. < 0.337.

由此还得到余项下界: $\varepsilon\cot z_2\ge\varepsilon(1/z_2-C_zz_2)$.

## 适用范围
- 适用: 需要 $\cot$ 在 $(0,\pi/8]$ 上余项显式上界的一切估计; 相位方程的余项处理 (引理 A'' 的 $\mathsf{def}_2$ 上界); 也可用于 $\tan$ (用 $\tan z=z+z^3/3+r(z)$, $r(z)/z^4\le0.06$ on $[0,\pi/8]$).
- 边界情形: 级数在 $(0,\pi)$ 内一致收敛 (最近奇点在 $\pi$), 单调性结论在全区间成立; 数值 $C_z$ 用 $\cot(\pi/8)=1+\sqrt2$ 的精确值.
- 不适用: $z$ 接近 $\pi$ 的奇异区 (余项爆炸); 需要多阶余项符号的场合应直接用级数正系数论证.

## 验证与备注
- 区间值认证: $R(\pi/8)/(\pi/8)\in[0.336811398993,0.336811399011]<0.337$ (脚本 19 v2, 方向舍入); $R(z)/z$ 单调性由正系数级数解析保证 (另在 4000 点数值复核).
- 相关: [[delta-bracketing]], [[lemma-A-doubleprime]].