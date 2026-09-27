---
title: 平衡相位方法
tags: [mathtool, self-developed]
source: 自研 (会话 5)
status: 数值验证 (1e-15)
created: 2026-08-04
---

# 平衡相位方法

## 解析
对对称两跳配置, 设各块承载相同相位 $p=\sqrt{\lambda\rho}\cdot\text{块宽}$, 把 secular 方程化为纯三角方程.

上确界配置 $[1,R,1]$ (块宽 $st,t,st$, $s=\sqrt{R}$, $t=1/(2s+1)$):
$$\sin p\Bigl((2s+1)\cos^2 p - s^2\sin^2 p\Bigr)=0 \Rightarrow p=\theta,\ \pi-\theta,\quad \theta=\arccos\frac{s}{s+1},$$
$$\lambda_1=\Bigl(\frac{(2s+1)\theta}{s}\Bigr)^2,\quad \lambda_2=\Bigl(\frac{(2s+1)(\pi-\theta)}{s}\Bigr)^2,\quad \nu(R)=\Bigl(\frac{\pi-\theta}{\theta}\Bigr)^2.$$

下确界配置 $[R,1,R]$ (块宽 $c,sc,c$, $c=1/(s+2)$):
$$\tan^2 p = s(s+2) \Rightarrow p=\varphi,\ \pi-\varphi,\quad \varphi=\arccos\frac{1}{s+1},\quad \mu(R)=\Bigl(\frac{\pi-\varphi}{\varphi}\Bigr)^2.$$

## 适用范围
- 适用: 对称两跳/平衡周期配置的闭式谱; 特征值比极值的闭式常数推导 (本项目 $\nu(R),\mu(R)$).
- 边界情形: 非平衡配置无此闭式; 高阶特征值对应 $p=k\pi$ 型根, 需按 Sturm 指标排序.
- 不适用: 非对称配置; 直接给出极值的完备刻画 (需要配合极值理论证明配置确实极值).

## 验证与备注
- 角度恒等式 $\sqrt{\lambda_1}\,st=\theta$, $\sqrt{\lambda_1}=(2s+1)\theta/s$, $\sqrt{\lambda_2}\,st=\pi-\theta$; 下确界同理 ($\sqrt{\lambda_1}=(s+2)\varphi/s$), 对 R=2,4,10 验证到 1e-15.
- 注意: 交接摘要曾误写 $\sqrt{\lambda_1}=2(s+1)\varphi/s$ (仅 R=4 巧合相等).
- 脚本: `scripts/num_formula.py`; 推导见 docs/SL_ratio_proof.tex.
