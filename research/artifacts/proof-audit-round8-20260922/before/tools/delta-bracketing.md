---
title: 相位括号 (delta-bracketing)
tags: [mathtool, self-developed]
source: 自研 (会话 30)
status: 已证 (初等单调函数夹逼)
created: 2026-08-07
---

# 相位括号 (delta-bracketing)

## 解析
对对称阱族 $[R,1,R]$ 的相邻模态, 相位 $\delta_k$ 满足精确方程 $\tan\delta_1=\varepsilon\tan z_1$, $\tan\delta_2=\varepsilon\cot z_2$, $z_k=(\pi/2\pm\delta_k)\varepsilon\ell/u$. 当 $R\ge1500$, $u\ge2\varepsilon$ ($w\ge2$) 时得到双端括号:
- $0\le\delta_1\le\delta_1^+:=\arctan(\varepsilon\tan((\pi/2)\varepsilon\ell/u))\le\varepsilon\tan(\pi/8)<0.011$;
- $0\le\delta_2\le\delta_2^+:=\arctan(2u/(\pi\ell))$;
- $z_2\le\pi/8$ (用 $h(x)=x(\pi/2+\arctan(2\varepsilon/(\pi x)))$ 在 $(0,1/4-\varepsilon]$ 单调, $h(1/4-\varepsilon)\le\pi/8$; 关键恒等式 $(1/4-\varepsilon)=(1/4)(1-4\varepsilon)$);
- $\psi_2:=\bar\theta_2-\theta_2\ge0$: 用单调函数 $g(\theta)=\theta-\pi/2-\arctan(\varepsilon\cot(\theta\varepsilon\ell/u))$, $g'>0$, 且 $g(\bar\theta_2)\ge\bar\theta_2-\pi/2-\arctan(u/(\bar\theta_2\ell))=0$.

## 适用范围
- 适用: 两区常密度 + 对称性的相位估计; 把隐式 secular 根换成显式初等括号 (证明引理 A'' 与 INF 极限定理 T1 上界的必备工具).
- 边界情形: $R$ 下限 1500 是人为门槛 (保证 $\varepsilon$ 小); $u\to1/2$ 时 $\ell\to0$, $\delta_2^+$ 发散, 但 $\theta_2$ 分支仍在 $(\pi/2,\pi)$, 此时改用其他估计; $w<2$ 进入深 sliver 区, 括号不再适用.
- 不适用: 垒族 (相位分支在 $(0,\pi/2)$); 高阶模态 ($z_k$ 进入更高分支); 需要 $\delta_1$ 下界的场合 (另用 $\arctan x\ge x-x^3/3$, 见 [[lemma-A-doubleprime]]).

## 验证与备注
- 相位括号在 4x61 采样点验证 (脚本 19 v2); $g'>0$ 与 $h'>0$ 为初等导数符号证明; $h(1/4-\varepsilon)\le\pi/8$ 的代数恒等式已逐项复核.
- 相关: [[lemma-A-doubleprime]], [[cot-series-certificate]], [[transfer-matrix-secular]].