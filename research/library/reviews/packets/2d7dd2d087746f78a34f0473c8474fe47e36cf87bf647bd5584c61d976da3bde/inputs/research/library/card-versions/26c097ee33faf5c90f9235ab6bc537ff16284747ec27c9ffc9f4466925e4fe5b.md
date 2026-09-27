---
title: 引理 A'' 下界 (gap-n1-inflimit)
tags: [mathtool, self-developed]
source: 自研 (会话 30, run R-20260806T200000Z-inflimit-5B2C7D)
status: 已证 (解析证明, 仅三个显式常数需区间认证)
created: 2026-08-07
---

# 引理 A'' 下界 (lemma-A-doubleprime)

## 解析
对 Dirichlet 弦 $-y''=\lambda\rho y$ 的对称阱族 $[R,1,R]$ ($\rho=R$ on $(0,u)\cup(1-u,1)$, $\rho=1$ on $(u,1-u)$), 记 $D_R(u)=\lambda_2-\lambda_1$, $\mu_k=R\lambda_k$, $G(R,u)=\mu_2-\mu_1$, 缩放极限 $\bar D(u)=\bar\mu_2-\bar\mu_1$. 设 $R\ge1500$, $w:=u\sqrt R\ge2$, 则

    G(R,u) = mu_2 - mu_1 >= Dbar(u).           (引理 A'')

证明结构 (相位坐标):
- 相位: $\theta_k=\sqrt{\mu_k}\,u$, $z_k=\sqrt{\lambda_k}\,\ell$, $\ell=1/2-u$, $\varepsilon=1/\sqrt R$; secular 方程 $\tan\delta_1=\varepsilon\tan z_1$, $\tan\delta_2=\varepsilon\cot z_2$, $\theta_1=\pi/2-\delta_1$, $\theta_2=\pi/2+\delta_2$.
- 恒等式: $G-\bar D=(\mathsf{def}_1-\mathsf{def}_2)/u^2$, $\mathsf{def}_1=\pi\delta_1-\delta_1^2$, $\mathsf{def}_2=(\bar\theta_2-\theta_2)(\bar\theta_2+\theta_2)$, $\bar\theta_2=a(u)$ 为 $\tan a=-a\ell/u$ 的唯一根.
- $\mathsf{def}_1$ 下界: $\delta_1\ge(\pi/2)c_1c_2\alpha$, $\alpha=(\ell/u)\varepsilon^2$, $c_1=0.99319..$, $c_2=0.99996..$; 故 $\mathsf{def}_1\ge(3\pi^2/8)(\ell/u)\varepsilon^2 c_1c_2$.
- $\mathsf{def}_2$ 上界: $\psi_2=\bar\theta_2-\theta_2$ 满足 $\psi_2[\frac{\tan\psi_2}{\psi_2}(1+AB)+\frac{u}{\bar\theta_2\theta_2\ell}]=\varepsilon R(z_2)$, $A=\tan(\bar\theta_2-\pi/2)=u/(\bar\theta_2\ell)$, $B=\tan\delta_2=\varepsilon\cot z_2$; 用余切级数余项 $R(z)=1/z-\cot z\le C_zz$, $C_z=R(\pi/8)/(\pi/8)<0.337$ ($z_2\le\pi/8$) 得 $\mathsf{def}_2\le C_z\theta\varepsilon^2(\ell/u)(t+\theta)/(1+v(v+1)/(t\theta)-\delta)$, $v=u/\ell=-t\cot t$, $\delta\le4.5\cdot10^{-4}$.
- 比值: $\mathsf{def}_2/\mathsf{def}_1\le(4C_z/(3\pi(\pi/2-\delta_1^+)c_2))\,B(\theta)\,(1+4.6\cdot10^{-4})\le0.8256<1$, 其中 $B(\theta)\le B(t)=2t^4/(t^2+v^2+v)\le9$.

## 适用范围
- 适用: 对称阱族 $[R,1,R]$ 的相邻间距下界; $R\ge1500$, $w\ge2$ (深 sliver 用分段下界另行处理); 是 INF 极限定理 T1 的 $\liminf$ 部分的关键工具.
- 边界情形: $w=2$ 处所有估计连续; 显式常数 (0.8256, 25) 使 margin 鲁棒; 不覆盖 $w\le2$.
- 不适用: 非对称阱族, 垒族 ($[1,R,1]$ 侧需另证), 更高指标间距 ($n\ge2$ 无 $\theta_2\in(\pi/2,\pi)$ 分支的同类结构).
- 注意: $v$ 的正确表达式是 $v=u/\ell=-t\cot t$ (不是 $-\cot t$); 早期草稿与脚本 19 v1 用错 $v$, 因 $f$ 关于 $v$ 递减, 数值界仍成立, 但公式必须更正.

## 验证与备注
- 解析证明完整 (docs/SL_gap_n1_inf_limit_proof.tex 第 2.3 节, 10 页 PDF 零警告); 三个常数 $C_z<0.337$, $f(t)\le9$, 比值 $\le0.8256$ 由脚本 19 v2 区间方向舍入认证 (PASS, 8 秒; 修正 $v$ 后 $f$ 最坏上界 5.4225).
- 恒等式 $G-\bar D=(\mathsf{def}_1-\mathsf{def}_2)/u^2$ 在 480 点验证到 1e-42; 逐点 $G-\bar D\ge0$ 最小余量 3.97e-10 (数值证据, 非证明).
- 相关: [[cot-series-certificate]], [[delta-bracketing]], [[inf-limit-comparison]].