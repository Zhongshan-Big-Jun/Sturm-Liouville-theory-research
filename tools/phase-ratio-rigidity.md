---
title: 相位比刚性 (phase-ratio rigidity)
tags: [mathtool, self-developed, o3a]
source: 自研 (O3a 完整证明, 2026-08-09; 来源 Blueprint 项目 runs/R-20260808T143337Z-o3a-c1, 用户提供 O3a_complete_proof_zh.pdf)
status: CANDIDATE_COMPLETE_PROOF (解析证明 + 两类证书支持的严格证明; 2026-08-09 升级: $\partial_qM_2<0$ 于 $D$ 已完全解析化, C4 区间段 $K>0$ 亦已纯初等解析化, 证书仅剩两个紧盒导数符号; 证书内核不在本仓库, 非 kernel-checked)
created: 2026-08-09
---

# 相位比刚性 (phase-ratio rigidity)

## 解析
对 Dirichlet 加权弦 $-y''=\lambda\rho y$ ($1\le\rho\le R$, 势垒族
$\rho=R$ on $(a,b)$, $1$ 其余), 设 $(a,b)$ 是 sign-consistent good root
($R_1=R_2=0$, $v(a)>0>v(b)$). 机制分四步:

1. **传输能量守恒**: 高密度区间的传输矩阵
   $P_m(\theta)=\begin{pmatrix}\cos\theta & \sin\theta/m\\ -m\sin\theta & \cos\theta\end{pmatrix}$
   保持二次型 $Q_m(X,Y)=m^2X^2+Y^2$, 给出精确振幅比
   $y_s(b)^2/y_s(a)^2=J_m(s(1-b))/J_m(sa)$, $J_m(x)=\sin^2x/(\cos^2x+m^2\sin^2x)$.
2. **残差消元**: $R_1=R_2=0$ 使 $\lambda_k,n_k$ 因子在同一模态内精确消去,
   得到相位比等值 $r_\tau(\alpha)=r_\tau(\beta)$,
   $r_\tau(x)=J_m(\tau x)/J_m(x)$ ($\tau=s_2/s_1$, $\alpha=s_1a$, $\beta=s_1(1-b)$).
3. **严格单调性**: 令 $\Psi(x)=x\cot x/(1+q_0\sin^2x)$, $q_0=m^2-1$,
   则 $W(x)^2\sin^2x\,\Psi'(x)=\sin x\cos x-x+q_0\sin^2x[\sin x\cos x-x(1+2\cos^2x)]<0$
   于 $(0,\pi)$ (两项均为负: $G(x)=x-\sin x\cos x$ 严格增), 故
   $d\log r_\tau/dx=(2/x)[\Psi(\tau x)-\Psi(x)]<0$ 于 $(0,\pi/\tau)$.
   等值推出 $\alpha=\beta$, 即 $a+b=1$ (对称刚性).
4. **对称线单变量化 + KEY LEMMA**: $S_R(\xi)=2(c+q)\widetilde F_e(c)/\xi^2$,
   $\widetilde F_e'(c)<0$ 于 $0<c<1/2$. 关键子命题 $M_2=\partial_w\mathrm{IN}<0$
   于 $D$ 已完全解析化 (2026-08-09, 引理 5.2--5.4): (i) $q=1$ 基线
   $M_2(1,w)=\pi h(w)<0$; (ii) $\partial_q^2M_2<0$ 的两段初等界
   (盒 $[1,20]\times[0,\sqrt3]$ 上 $N_2\le-(10\pi/3)q^4+3\sqrt3 q<0$;
   $D\cap\{w\ge\sqrt3\}$ 上 $N_2=-AB_0+qw^3(1-w^2-4wt)-4qw^2t<0$);
   (iii) $\partial_qM_2(1,w)=g(w)<0$ 于 $[0,\sqrt3]$ (凹性 $g''<0$ + 切线界
   $g(4/5)+g'(4/5)(\sqrt3-4/5)\le-1054523/114800<0$);
   (iv) 边界曲线 $w=\sqrt{2q+1}$ 上 $\theta$-参数化闭式: $M_2<0$ 由
   $2-(\pi/2-\theta)\sin2\theta\ge2-\pi/2$, $\partial_qM_2=N(z)/(2z^2(z^2+1)^2)$
   且 $N$ 对 $\beta=\arctan z$ 凸性的端点极大 + 精确有理上界
   $R(z)\le-262235520291/59137044050<0$, $T(z)\le-7282185739373/266116698225<0$;
   (v) 尾部 $q\ge20$ 由 $B(q)<0$ 解析处理.
   **C4 的解析证明** (2026-08-09): 在 $c=0.4$ 曲线上 $v=\arctan w$,
   $K=q^2L$ 且 $q\ge1$; $L(v)=(1+T^2)(w(5v/T-3)+2v)-\frac65T(1+w^2)$,
   $T=\tan(\pi-\frac52v)$. 商数法则给出 $L'=N/(10T^2)$, 分子
   $N=125wv+50T(v(1+w^2)+w)+20T^2+c_3T^3+(20-125wv)T^4+c_5T^5$,
   $c_3=50w^2v-24w^3+176w-50v$, $c_5=150w-100v$. 两区域估计: 区域 I
   $v\in[2\pi/7,3\pi/10]$ 上 $N\ge88146367488708279/400000000000000>0$;
   区域 II $v\in[3\pi/10,2\pi/5)$ 上 $T\le1$,
   $N=125wv(1-T^4)+20T^4+50T(v(1+w^2)+w)+20T^2+c_3T^3+c_5T^5$ 为非负项之和
   ($c_3\ge0$ 按 $w\le27/10$ 与 $w\ge27/10$ 两段核验, $c_5>0$). 故 $L$ 严格
   递增, $K=q^2L\ge L\ge L(2\pi/7)>0$. 常数全部精确核验: Machin 级数给
   $\pi\in(3.1415,3.1416)$; $\tan(3\pi/10)^2=1+2\sqrt5/5$,
   $\tan(2\pi/5)^2=5+2\sqrt5$ 配合 $\sqrt5\in(2.2360,2.2361)$;
   $\tan(2\pi/7)$ 是 $P(t)=t^6-21t^4+35t^2-7$ 在 $(1,2)$ 的唯一零点,
   $P(1253/1000)>0>P(1254/1000)$. 该证明完全取代原 200 叶盒 C4 证书与
   尾段处理. 剩余两处紧盒证书: 128 叶盒证 $(G_2-G_1)'<0$ (上界 $-4.8416$),
   128 叶盒证 $\widetilde F_e''>0$ (下界 $+8.3794$); 端点 $c\ge1/2$ 区域
   解析为负, $c\to0^+$ 时 $\widetilde F_e\to\pi^2/(4q)>0$, 故对称线上
   single crossing.

## 适用范围
- 适用: 单垒/单阱两块族上残差系统的唯一性; 无需残差分支单图性、额外 sheet
  排除或 Jacobian 非退化假设; 与 [[transfer-matrix-secular]], [[keller-variational]],
  [[reflection-branch-reduction]] 配合.
- 边界情形: $R\to1^+$ (形式极限 $m=1$ 时 $\Psi'<0$ 仍成立), $R\to\infty$
  (仅需相位严格小于 $\pi$, 无安全距离), $a\to0^+$, $b\to1^-$, $a\to b$
  (传输恒等式不除以 $\sin\theta$).
- 不适用: 多阱/多块族 (振幅比结构不同); $n\ge2$ 相邻间距 (需重新建立
  $f$ 结构与相位框架); 有质量/范数约束的类 (MDE, 见 [[mde-extremal]]).
- 注意: 证书叶盒仅覆盖两个紧盒 (原 C4 曲线证书已被解析证明取代), 半无限
  尾部与 C4 曲线均由解析估计处理; 证书重放器不是形式化证明助手内核 (PDF
  说明 8.1 如实标注). 数值扫描仅作交叉检验, 不作为结论依据.

## 验证与备注
- 审计脚本 (2026-08-09, 全部通过): scripts/audit_o3a_pdf_part1.py (恒等式 (7),
  $G_1<0$, $IN=G_2\cdot POS$, CORNER 公式, KEY LEMMA 采样, $B(q)$ 尾部),
  part2/2c (根计数 $R\in\{1.1,\dots,10^6\}$), part3 (核心恒等式 59 位, 引理 4.1),
  part4 (证书不等式稠密采样); 大 $R$ 定位 scripts/_audit_cstar.py.
- 解析化验证 (2026-08-09): scripts/verify_o3a_M2_analytic.py (全部有理界与闭式
  逐条复核, 含 $R,T$ 上界、$g$ 链、$N_2$ 界、$B(q)$ 尾界、$h$ 分析).
- C4 解析化验证 (2026-08-09): scripts/verify_o3a_c4_analytic.py (PART A 精确
  有理数复算全部常数与两区域下界, 15 项全 PASS; PART B 数值交叉检验
  $N,L,K>0$ 于 40001 点网格, 仅作 E3 证据).
- 主定理: 对每个 $R>1$, 参数三角形内恰有一个 sign-consistent good root,
  且必为对称根 $a+b=1$; 即 O3a/C1 (docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf).
- 文献检索 (2026-08-09): 未检索到与该机制 (相位比刚性 + good-root 唯一性)
  直接重合的已发表结果; Keller 1976 / Mahar-Willner 1976 处理 $\lambda_2/\lambda_1$
  比值与极值函数对称双跳, 机制不同.
