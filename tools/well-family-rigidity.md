---
canonical_key: well-family phase-ratio rigidity (INF side, all R>1)
title: 阱族相位比刚性 (well-family phase rigidity, 全 R)
tags: [mathtool, self-developed, phase-ratio, gap-extremals]
source: 自研 (会话续作 2026-08-10; 承接 O3a 垒族相位比刚性, 见 [[phase-ratio-rigidity]])
status: 定理已证 STRICT (一切 R>1, 2026-08-10, docs/SL_gap_n1_well_rigidity_allR_proof.pdf, 14 页零警告); 总结 docs/SL_gap_n1_well_rigidity_allR_summary.pdf (8 页零警告); 全部数值为 EVIDENCE
created: 2026-08-10
updated: 2026-08-10
---

# 阱族相位比刚性 (well-family phase rigidity, 全 R)

## 解析
对 Dirichlet 弦 $-y''=\lambda\rho y$, 阱族
$\rho_{a,b}=R\cdot\mathbf1_{[0,a]\cup[b,1]}+\mathbf1_{(a,b)}$, 相位变量
$A=ms_1a$, $B=ms_1(1-b)$, $\tau=s_2/s_1>1$, $m=\sqrt R$, $q=R-1$,
$W(x)=\sin^2x+m^2\cos^2x$, $J(x)=\sin^2x/W(x)$,
$r_\tau(x)=J(\tau x)/J(x)$, $x_{mid}=\pi/(1+\tau)$.

**主定理 (STRICT, 2026-08-10)**: 对\emph{一切} $R>1$, 阱族的任意
sign-consistent good root 满足 $a+b=1$ (对称根).

全 R 证明链五步 (全部初等; 小 R 段 $1<R\le3/2$ 的旧机制 (Psi~'<0 全局单调)
为特例, 见下):
1. **相位范围 + 模态恒等式**: sign-consistency ($y_2(a)>0$, $y_2(b)<0$) 与
   Sturm 振荡给唯一零点 $z\in(a,b)$, 由阱区显式解得 $\tau A,\tau B<\pi$
   (即 $A,B\in(0,\pi/\tau)$); Pr\"ufer 角给
   $\alpha(A)+\psi+\alpha(B)=\pi$, $\alpha(\tau A)+\tau\psi+\alpha(\tau B)=2\pi$,
   $\alpha(x)=\arctan2(\sin x/m,\cos x)$ 严格递增, $\alpha'=m/W$.
2. **$\tau<2$**: 新 $\alpha$-凸性引理 $D(x)=\alpha(2x)-2\alpha(x)>0$ 于
   $(0,\pi/2)$ ($D'=2mq\sin^2x(4\cos^2x-1)/(W(x)W(2x))$, $D(0)=D(\pi/2)=0$);
   反设 $\tau\ge2$ 得 $\Phi(2s_1)>2\pi=\Phi(s_2)$ 与 $\Phi$ 严格递增矛盾.
   注意 $\tau<2$ 依赖 sign-consistency (一般配置 $\tau$ 可到 ~4.7).
3. **残差消元**: good root 的 $R_1=R_2=0$ 给出 $r_\tau(A)=r_\tau(B)$ 且
   $\Sigma_2/\Sigma_1=\tau^2r_\tau(A)$; 用传输能量守恒 $y(b)^2/y(a)^2=J(B)/J(A)$,
   右阱系数 $C_k^2=W(A_k)/W(B_k)$ 与三段积分范数闭式
   $\Phi(A,\psi,B)=\frac{W(A)}{2m^2}[\psi+\frac{mA}{W(A)}+\frac{mB}{W(B)}]$
   (在切形式约束下符号验证).
4. **$r_\tau$ 精确结构**: 因子分解
   $r_\tau(x)-1=m^2\sin((\tau-1)x)\sin((\tau+1)x)/(J(x)W(x)W(\tau x))$
   给左区 $r>1$、右区 $r<1$; $L_0$ 下界 $1<\tau^2r$, $W(x)/W(\tau x)<\tau^2r$
   于 $(0,x_{mid})$ (用 $\sin(\tau x)>\sin x$); 中间区 $(x_{mid},\pi/2]$
   严格递减 (对数导数 $\tau\Psi(\tau x)-\Psi(x)<0$, $\Psi=(\log J)'$);
   **危险区引理**: $x_{mid}<x<\pi/2<y\le\pi-x$ 时 $r_\tau(y)<r_\tau(x)$
   (用 $J(\pi-u)=J(u)$ 与 $g$ 递减); **反射分离 B'**: 区域 II 等值对
   $x\ne y$ 必满足 $x+y>\pi$.
5. **排除与收尾**: 左区 $L_3$ (凸包 $\Sigma_2/\Sigma_1\in\text{conv}\{1,
   W(A)/W(\tau A),W(B)/W(\tau B)\}<\tau^2r_\tau(A)$ 矛盾, 不依赖左区单调性);
   跨区符号矛盾; 区域 II $P$-和通道
   $P_\tau(A)+P_\tau(B)=(2-\tau)\pi$ 与反射恒等式
   $\alpha(x)+\alpha(\pi-x)=\pi$ 矛盾. 故 $A=B$, $a+b=1$.

## 适用范围
- **适用**: 阱族 (INF 侧) 在一切 $R>1$ 的 good-root 对称性; 与
  [[gap-n1-reduction]] (O1-INF 归约) 配合, INF 极值问题的内部临界点全部落在
  对称阱 $[R,1,R]$ 上 (对一切 $R>1$).
- **边界情形**: $R\to1^+$ 退化到 $\rho\equiv1$ ($\tau\to2^-$); $R\to\infty$
  极限由定理 A 处理 (CANDIDATE).
- **不适用 / 注意**: $\tau<2$ 只对 sign-consistent good root 成立; 一般阱族
  配置 $\tau$ 可远超 2. 危险区引理与 B' 需要 $\tau<2$ 与 $y<\pi/\tau$.
  垒族对应工具 [[phase-ratio-rigidity]] 对一切 $R>1$ 成立 (机制不同:
  $q$ 与 $\sin^2$ 而非 $\cos^2$ 相乘, 无需 $\tau<2$ 通道).
- **注意**: good root 定义、符号一致性条件与 FH 残差公式的符号约定
  (f = lam2*y2^2/n2 - lam1*y1^2/n1; dD/da = -(R-1)f(a)) 必须与本条目一致,
  见 all-R 证明文档注 rem:fh.

## 小 R 特例机制 (保留备查, 1<R<=3/2)
小 R 段旧证明 (docs/SL_gap_n1_well_rigidity_R32.pdf, 11 页) 用
$r_\tau$ 于 $(0,\pi/\tau)$ 的全局严格递减: 对 $\widetilde\Psi(x)=x\cot x+
qx\sin x\cos x/\widetilde W(x)$ ($\widetilde W=1+q\cos^2x$) 证明
$\widetilde\Psi'<0$ 于 $(0,\pi)$ (因式分解
$\widetilde W^2\sin^2x\,\widetilde\Psi'=-(q+1)(2N_0+qN_1)/8$, $H=4N_0+N_1>0$
引理, tan(u/2) 有理化 $N(t)>0$). 该机制在 $R>3/2$ 失效 (数值阈值 $R=3/2$,
EVIDENCE), 被全 R 五步链取代; 保留为特例记录.

## 验证与备注
- 严格证明文档: `docs/SL_gap_n1_well_rigidity_allR_proof.pdf` (14 页, 零警告,
  2026-08-10; STRICT x20, EVIDENCE x7 标注); 总结文档
  `docs/SL_gap_n1_well_rigidity_allR_summary.pdf` (8 页, 零警告; 失败路线与
  交接错误更正, 经验教训, EVIDENCE 登记, 数学知识板块).
- 符号恒等式 (sympy 在切形式约束下精确): $C_k^2=W(A_k)/W(B_k)$;
  $r_\tau-1$ 因子分解; $\alpha'=m/W$; $D'$ 闭式; $\Phi=W(A)\Sigma_1/(2m^2)$
  与 $\Phi(\tau\cdot)=\frac{W(\tau A)}{2m^2}\tau\Sigma_2$.
- 数值 EVIDENCE (全部登记于 `misc/_well_explore_log.md` 第 16 节, 脚本
  `scripts/_gapb_s55/`): 171 配置模态恒等式 0 失败; P-和 1e-40; 范数闭式与
  C^2 1e-40; sign-consistent $\max\tau=1.99995184$ (R=1.01) vs 一般配置
  $\tau\approx4.70$ (R=10^4); $D(x)$ min 9.7e-13; 中间区 0 违反; 危险区
  124 万样本 0 违反; B' 全局最小 $x+y=3.1421822$ 余量 5.9e-4 (R=10^4,
  tau=1.4); $\alpha$-反射仅 1-ulp 边界; 细化 $v^*=0.3825982567998447\ldots$
  处 $|R_1|<1e-50$, $\Sigma_2/\Sigma_1=\tau^2r(A)=\tau^2r(B)$ 到 1e-51 (R=4).
- 交接错误更正 (总结文档第 3 节): BETA 全域断言、$r(y)>r(\pi-y)$、左区
  单调性、$\tau<2$ 依赖 sign-consistency、范数闭式非交换对称、sympy 需代入
  切形式约束、$v^*$ 8 位精度假残差、L0 逆式抄写错误.
- 剩余缺口 (开放): (a') 对称线上 $f$ 零点唯一性与 $D(v)$ 单峰对 $R>3/2$
  的 1D 严格证明; (c) 定理 A (INF R->inf 极限) 独立复核 CANDIDATE;
  (d) 全局 good-root 论证 (极值点存在性、边界情形). 本文不宣称 INF 侧
  $R>3/2$ 完全闭合.
- 相关工具: [[phase-ratio-rigidity]], [[gap-n1-reduction]],
  [[symline-n1-monotonicity]], [[gap-band-extremals]], [[residual-exactness]],
  [[transfer-matrix-secular]], [[sturm-oscillation]].
