---
canonical_key: second-variation-weighted-eigenvalues (lambda'' formula + pitfalls + gap second variation Q)
title: 加权特征值二阶变分: lambda'' 公式与两种错误框架陷阱
tags: [mathtool, self-developed, perturbation-theory, second-variation, hessian, gap-extremals, nge2]
source: 自研 (R-206, 2026-08-13; 承接 docs/SL_gap_nge2_symmetry_local_proof.tex 的 (G1')/(G2) 框架)
status: lambda'' 公式 STRICT (完整推导); P1/P2/P3 数值证据; 交接二阶系数路线否证 (STRICT 机制)
created: 2026-08-13
updated: 2026-08-13
---

# 加权特征值二阶变分 (lambda'' 公式)

## 解析

### 主公式 (STRICT, 完整推导)

设定: $-u''=\lambda\rho u$ 于 $(0,1)$, $u(0)=u(1)=0$, $\rho$ 有界正,
本征函数按 $\int\rho u_k^2=1$ 归一. 摄动 $\rho_\varepsilon=\rho+\varepsilon dr$,
$dr$ 为任意 $L^\infty$ 摄动 (不必分段常数). 记
$u_k(\varepsilon)=u_k+\varepsilon v_k+\frac{\varepsilon^2}{2}w_k$,
$\lambda_k(\varepsilon)=\lambda_k+\varepsilon\lambda'+\frac{\varepsilon^2}{2}\lambda''$, 则

\begin{equation*}
  \lambda'=-\lambda\langle dr,u^2\rangle,\qquad
  \lambda''=2\lambda\langle dr,u^2\rangle^2
  -2\lambda^2\sum_{l\ne k}\frac{\langle dr\,u,u_l\rangle^2}{\lambda_l-\lambda},
\end{equation*}

其中一切配对为**不加权** $L^2(dx)$ 配对
$\langle dr,\phi\rangle=\int dr\,\phi\,dx$, 两个求和的公分母都是
$\lambda_l-\lambda$.

推导四步 (固定空间广义特征问题 $A=-d^2/dx^2$, $B=\times\rho$ 于 $H_0^1$,
约束 $\langle u_\varepsilon,B_\varepsilon u_\varepsilon\rangle=1$):
1. Rayleigh 商展开 + 精确约束 (一阶与二阶约束导数均消失) 给出
   $\lambda''=2\int(v')^2+2\int u'w'$.
2. 一阶方程 $-v''=\lambda'\rho u+\lambda\,dr\,u+\lambda\rho v$ 与 $u$ 配对
   (用一阶约束导数 $\langle\rho u,v\rangle=-\frac12\langle dr,u^2\rangle$):
   $\int u'v'=\lambda'+\frac\lambda2\langle dr,u^2\rangle$; 与 $v$ 配对:
   $\int(v')^2=\lambda'\langle\rho u,v\rangle+\lambda\langle dr\,u,v\rangle
   +\lambda\langle\rho v,v\rangle$.
3. 二阶方程 $-w''=\lambda''\rho u+2\lambda'\,dr\,u+2\lambda'\rho v
   +2\lambda\,dr\,v+\lambda\rho w$ 与 $u$ 配对, 并用二阶约束导数
   $\langle\rho u,w\rangle=-2\langle dr\,u,v\rangle-\langle\rho v,v\rangle$ 消去
   $w$: $\int u'w'=\lambda''+\lambda'\langle dr,u^2\rangle-\lambda\langle\rho v,v\rangle$.
4. 代入得 $-\lambda''=2\langle v,(A-\lambda B)v\rangle+2\lambda'\langle dr,u^2\rangle$,
   再代入 $\lambda'=-\lambda\langle dr,u^2\rangle$ 与
   $v=\lambda R_\lambda^\perp[(dr-\rho\langle dr,u^2\rangle)u]$
   ($R_\lambda^\perp$ 为 $A-\lambda B$ 在 $L^2(dx)$ 中的约化预解; 因
   $\langle\rho u,u_l\rangle=\delta_{kl}$, $\rho\langle dr,u^2\rangle u$ 项对
   $l\ne k$ 无贡献; $v$ 的 $u_k$ 分量由约束确定但不进入 $(A-\lambda B)v$).
   QED.

相邻谱隙 $D_n=\lambda_{n+1}-\lambda_n$ 在驻点处的二阶变分:

\begin{equation*}
  Q(dr)=\tfrac12\frac{d^2D_n}{d\varepsilon^2}
  =\lambda_{n+1}\langle dr,u_{n+1}^2\rangle^2-\lambda_n\langle dr,u_n^2\rangle^2
  +\lambda_n^2\sum_{l\ne n}\frac{\langle dr\,u_n u_l\rangle^2}{\lambda_l-\lambda_n}
  -\lambda_{n+1}^2\sum_{l\ne n+1}\frac{\langle dr\,u_{n+1}u_l\rangle^2}
  {\lambda_l-\lambda_{n+1}},
\end{equation*}

切空间条件 $\langle dr,f\rangle=0$, $f=\lambda_n u_n^2-\lambda_{n+1}u_{n+1}^2$.

### 两个错误框架陷阱 (已登记, 勿重犯)

- **移动空间框架错误**: 在 $L^2(\rho dx)$ 中处理算子
  $A(\rho)=-(1/\rho)d^2/dx^2$ 时内积随 $\varepsilon$ 变化, 推导产生伪项
  $4\lambda\langle dr^2/\rho,u^2\rangle$. 必须用固定空间广义特征问题
  $A=-d^2/dx^2$, $B=\times\rho$, 约束 $\langle u_\varepsilon,B_\varepsilon u_\varepsilon\rangle=1$.
- **宽度路径的 delta' 边界层 (交接路线否证机制, STRICT)**: 宽度族
  $\rho(x;w+\varepsilon dw)$ 对 $\rho$ 非线性, 二阶密度变分为
  $d^2\rho=\sum_i s_i dw_i^2\,\delta'(x-x_i)$ (Heaviside 位移展开), 是主阶
  边界层项, naive 公式完全遗漏; 且 bump 正则化的 naive 公式在对角 Green
  求和中随 bump 宽趋于 0 发散. 故 "naive 二阶变分 = 宽度 Hessian + 可控余项"
  的交接提议不成立 (P3 符号级否证).

## 适用范围

- **适用**: 有界正密度下 Dirichlet 谱的单参数可微摄动 (任意 $L^\infty dr$);
  驻点处 $D_n$ 的二阶方向导数的谱表示; 固定空间框架下含约束归一化的
  广义特征值二阶摄动.
- **边界情形**: 常数弦 $\rho=1$ 取反对称阶梯 $dr$ 时 $\lambda'=0$ 精确,
  $\lambda_1''$ 闭式可算, 是最小检验例; 谱截断 $N$ 增大时对角 Green 求和收敛
  慢, 需要用高 $N$ 或多重截断对比.
- **不适用 / 注意**: 不直接给出 bang-bang 宽度 Hessian (见 delta' 陷阱);
  INF 侧无一致余量 ($\det K\to0+$, R-202), 本工具不能独立完成 INF 定号;
  本公式是局部二阶信息, 不能替代全局极值性论证; 数值符号检验仅是 EVIDENCE.

## 验证与备注

- 来源: 自研 (R-206, 2026-08-13); 运行笔记
  runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/
  run_notes_addendum_2026-08-13c.md; 脚本
  scripts/_gapn2_second_variation_probe.py (P1/P2/P3),
  scripts/_gapn2_k_global_rank2.py (修正后的全局 Kp 恒等式).
- 数值验证 (EVIDENCE): 常数弦反对称阶梯 $\lambda_1''$ 公式 vs FD 相对误差
  1.7e-5 (N=40); n=2 SUP R=4 逐特征值 4e-3/5e-2 (N=60), $Q$ 相对误差 1e-3;
  P2 SUP 切空间负定 (n=2,3 R=4; n=2 R=10, 分段常数与三角方向), INF n=2 R=4
  不定; P3 与宽度 Hessian 符号全部不符 (否证, 机制如 delta' 陷阱所述).
- 诚实登记: 公式推导为 STRICT 自足; 一切符号/收敛检验为 EVIDENCE;
  (G1') 仍开放, 精确形式为全局恒等式
  $Kp=\operatorname{diag}(d)+(2\lambda_n D/\lambda_{n+1}^2)vv^T$ 加两个
  $\varepsilon$-masked 约化预解项 (见 [[green-half-inertia]] 与
  _gapn2_k_global_rank2.py).
- 相关: [[feynman-hellmann]] (一阶), [[gap-band-extremals]] (带自洽判据与
  FH 对称加倍), [[green-half-inertia]] ((G1') Green 化归),
  [[bang-bang]] (极值结构), [[switch-saturation-k-invariant]] (块能量
  不变量).
