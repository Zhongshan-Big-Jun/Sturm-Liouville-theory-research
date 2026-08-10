---
title: 残差闭合恒等式 (residual exactness)
tags: [mathtool, self-developed]
source: 自研 (O3a, 2026-08-05)
status: 定理已证 (FH + Schwarz) + 数值验证 (~1e-7)
created: 2026-08-05
---

# 残差闭合恒等式 (residual-exactness)

## 解析
设 Dirichlet 弦 $-y''=\lambda\rho y$ ($y(0)=y(1)=0$) 的密度属于双参数跳变族
$\rho_{(a,b)}=R$ 于 $(a,b)$, $1$ 于其余处, $0<a<b<1$. 定义残差

$$R_1(a,b)=f(a;a,b),\qquad R_2(a,b)=f(b;a,b),\qquad f=\lambda_1 u_1^2-\lambda_2 u_2^2,$$

其中 $u_k$ 为 $L^2(\rho)$-归一化特征函数. 则有**精确恒等式**

$$\frac{\partial R_1}{\partial b}\equiv-\frac{\partial R_2}{\partial a}.$$

**证明**: 由 Feynman-Hellmann 跳变公式 (O1b), 移动跳变点 $a$ 使 $(a,a+da)$ 上的密度
从 $R$ 降为 $1$, 得 $\partial D/\partial a=-(R-1)R_1$; 移动 $b$ 得
$\partial D/\partial b=+(R-1)R_2$, 其中 $D=\lambda_2-\lambda_1$. 因 $D$ 在
$0<a<b<1$ 上为 $C^2$ (secular 方程实解析 + Dirichlet 谱单重 + 隐函数定理), 由
Schwarz 定理 $\partial^2D/\partial b\partial a=\partial^2D/\partial a\partial b$
即得恒等式.

## 推论 (临界点斜率分裂)
在残差零点 $(R_1=R_2=0)$ 处, 残差 Jacobian 有结构

$$J_{\mathrm{res}}=\begin{pmatrix} R_{1a} & -R_{2a} \\ R_{2a} & R_{2b} \end{pmatrix},\qquad
\det J_{\mathrm{res}}=R_{1a}R_{2b}+R_{2a}^2.$$

两条零点曲线 $\Gamma_1=\{R_1=0\}$, $\Gamma_2=\{R_2=0\}$ 的斜率满足
$g_1'=R_{1a}/R_{2a}$, $g_2'=-R_{2a}/R_{2b}$. 若进一步
$\det J_{\mathrm{res}}<0$ 且 $R_{2a}R_{2b}>0$, 则 $g_1'-g_2'>0$, 两曲线至多相交一次.

## 适用范围
- 适用: 密度逐点界类上的双参数 (或 $2n$ 参数) 跳变族; 间距/比值泛函的临界点唯一性;
  分支交点计数 (Route A); 自洽映射 $T$ 不动点唯一性分析.
- 边界情形: 需 $D$ 的 $C^2$ 光滑性 (远离 $a=0$, $b=1$, $a=b$ 退化配置; 谱单重).
- 不适用: 特征值重数退化处; 非 FH 型扰动 (如质量约束类) 需重新验证公式.

## 验证与备注
- 来源: O3a run 从 Feynman-Hellmann 公式 + Schwarz 定理推导; 数值验证
  (Richardson 外推中心差分, 4 个点, 残差 ~1e-7, 即有限差分 + 特征值求解器精度).
- FH 公式本身直接数值验证: $(0.42,0.56,R=4)$ 处 $\partial D/\partial a=38.887310=-(R-1)R_1$,
  $\partial D/\partial b=-26.476919=+(R-1)R_2$ (精度 1e-6).
- 相关脚本: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentB_lib.py,
  agentB_crossing.py; 文档 agentB_O3a_fixed_point.md (定理 T3).
- 局限: 恒等式本身已证; 用它推出分支单调性 ($g_1'>g_2'>0$) 已被否证 - O3a 的
  Lemma A 对 R >= ~1350 为假 (run R-20260806T011500Z-o3abranch-E8E56F, 区间证书,
  见 [[interval-ad-certificate]] 与 counterexample_log CE-1).