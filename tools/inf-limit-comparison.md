---
title: 极限系统比较法 (INF R->inf 极限)
tags: [mathtool, self-developed]
source: 自研 (会话 30, run R-20260806T200000Z-inflimit-5B2C7D)
status: 已证 (定理 A, T1/T2/T3 全部闭合; 2026-08-12 独立复核通过, 缺口 (c) 解除)
created: 2026-08-07
updated: 2026-08-12
---

# 极限系统比较法 (inf-limit-comparison)

## 解析
对含大参数 $R$ 的相邻间距优化问题, 建立"极限系统 + 比较定理"三步框架:

- **T2 (极限系统单调结构)**: 令 $\varepsilon\to0$ 得极限特征值 $\bar\mu_1(u)=\pi^2/(4u^2)$, $\bar\mu_2(u)=a(u)^2/u^2$, $\tan a=-a\ell/u$ (唯一根 $a\in(\pi/2,\pi)$); $\bar D=\bar\mu_2-\bar\mu_1$. 自洽函数 $S(u)=\bar\mu_1\,2/u-\bar\mu_2\sin^2(a)/I_2(u)$, 且 $\bar D'(u)=S(u)$, $S(u(a))=-4(a-\tan a)^3/(a^3(2a-\sin2a))\,G(a)$. 符号链 $\widetilde K\to J\to G\to S$ ($\widetilde K=-a^2+3\sin^2a+\frac32 a\sin2a$, $J=4a^3\cot a+6a^2-\pi^2$, $G=8a^3\sin^2a-\pi^2(2a-\sin2a)$) 给出 $S$ 唯一变号, $\bar D$ 在 $u^*$ 全局严格极小.
- **T3 (验证值)**: 区间算术二分包住 $u^*$, $a(u^*)$, $\bar D(u^*)$ (宽度 2e-20), margin $3\pi^2-\bar D(u^*)\ge4.664947$.
- **T1 (收敛)**: $\limsup$ 用 $m_R\le D_R(u^*)$; $\liminf$ 分两区: $w\le2$ 深 sliver 分段下界 $G\ge25$ (脚本 16), $w\ge2$ 用引理 A'' $G\ge\bar D(u)\ge\bar D(u^*)$. 近极小化子收敛: $\bar D(u_R)\to\bar D(u^*)$ + 严格单调性 + 聚点论证.
- 结果: $\lim_R R\,m_R=\bar D(u^*)$, 且 $u_R\to u^*$.

## 适用范围
- 适用: 两参数 $(R,u)$ 极限问题, 其中 $u$ 决定极限配置而 $R$ 只缩放; 对称阱族相邻间距; 一般可推广到"固定形状 + 大振幅"的密度族.
- 边界情形: 需要 $u^*$ 的显式区间 (T3) 支撑 $25>\bar D(u^*)$ 的 margin; 深 sliver 区必须独立处理 (引理 A'' 仅在 $w\ge2$ 有效).
- 不适用: 非对称配置 (O3a/C1 未决: 对称族下确界 = 全盒类下确界未知); 垒族 (SUP 侧, 中心质量钉扎极限 $D\to4\pi^2$ 属另一框架); $n\ge2$ 相邻间距 (缺少 $\theta_2$ 分支结构).
- 经验: 文档中严格证明 (§2) 与数值证据 (§4) 必须分节标注; 认证脚本 16-19 给出三个显式常数的区间证书, 其余为解析.

## 验证与备注
- 完整证明: docs/SL_gap_n1_inf_limit_proof.pdf (10 页, 零警告); SL_gap_n1_proof.pdf 新增 INF 极限一节 (14 页, 零警告).
- 数值收敛 $R\,m_R$: 1500 -> 24.9542, 1e4 -> 24.9454, 1e6 -> 24.9439, 1e8 -> 24.943866 (误差 ~1/sqrt(R); 证据, 非证明).
- 独立复核 (2026-08-12, 会话 58 续作 3, EVIDENCE): scripts/_theoremA_recheck_t2t3.py (T2 符号链: sympy 验证 J'=4aK~/sin^2a 与 G'=4sin^2a J 恒等; u' 闭式; h'<0 扫描; 根 a1=1.63504, a*=1.98551, aG=2.27651; S 恒等式; T3: u* 与 Dbar(u*) 均落入文档区间, margin 4.664947/0.0561 复核通过) + scripts/_theoremA_recheck_lemAdp.py (引理 A'': 175 点 G>=Dbar 零失败, 最小余量 3.97e-10 与文档一致; sliver 600 点 G>=25 零失败, 最小值 91.7263 在 w=2 边界; T1 收敛 0.01038/1.56e-3/1.56e-5/1.56e-7; 常数链 C_z=0.336811<0.337, max f(t)=5.4017<=9, 比值 0.82505<=0.8256; secular 与有限差分互检 1e-5..1e-8). 全部数值为交叉检验, 不构成证明; 结论: 未发现错误.
- 相关: [[lemma-A-doubleprime]], [[delta-bracketing]], [[cot-series-certificate]], [[gap-band-extremals]], [[gap-n1-reduction]].