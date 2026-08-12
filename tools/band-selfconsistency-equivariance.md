---
canonical_key: band-selfconsistency-equivariance (n>=2 gap-extremal reflection symmetry)
title: 带状自洽等变性: F(R,x̄)=PF(R,x) 与反对合 Jacobi 结构 J=-PJP
tags: [mathtool, self-developed, equivariance, jacobian, gap-extremals, nge2, reflection-symmetry]
source: 自研 (会话 58 续作 4b, 2026-08-12; 文档 docs/SL_gap_nge2_symmetry_local_proof.pdf 与 docs/SL_gap_nge2_symmetry_recon.pdf)
status: 等变恒等式与反对合结构为 STRICT; 以 (G1')(G2) 为充分条件的全局唯一性/对称性为已证框架定理, 两条件本身为开放 (数值 EVIDENCE 支持)
created: 2026-08-12
updated: 2026-08-12
---

# 带状自洽等变性 (反射等变 + 反对合 Jacobi 结构)

## 解析

对 Dirichlet 弦 $-y''=\lambda\rho y$, 块密度 $\rho=\sum_{i=1}^{2n+1}R^{\sigma_i}\mathbf1_{[w_{i-1},w_i]}$
($\sigma_i\in\{0,1\}$ 记 $\{1,R\}$ 两种块, $w_0=0<w_1<\cdots<w_{2n}=1$),
开关位置向量 $x=(x_1,\dots,x_{2n})$ ($x_i$ 为第 $i$ 个开关), 带自洽系统为
$F_\sigma(R,x)=0$, 其分量是 FH 跳点条件 $f(x_i)=0$ 的归一化残差.

**等变恒等式 (STRICT)**: 设图案回文 $\sigma_i=\sigma_{2n+2-i}$, 边缘反射
$\bar x_i=1-x_{2n+1-i}$, $P$ 为反转置换矩阵, 则对一切 $(R,x)$
\begin{equation*}
  F_\sigma(R,\bar x)=P\,F_\sigma(R,x).
\end{equation*}

**反对合 Jacobi 结构 (STRICT)**: 反射的微分是 $-P$, 故在对称点 $x^*=\bar x^*$ 处
\begin{equation*}
  J=-PJP,\qquad J:=D_xF_\sigma(R,x^*),
\end{equation*}
即在对称/反对称坐标下 $J=\begin{pmatrix}0&A\\B&0\end{pmatrix}$ 为交叉块形式,
$\det J=(-1)^n\det A\det B$. 推论: 对称方向与反对称方向的变分完全解耦;
对称点非退化当且仅当两块 $A,B$ 均可逆.

**拓扑度同伦框架 (STRICT 定理, 条件开放)**: 设
(G1$'$) 对 $R\in(1,R_0]$, 解簇上 $\det D_xF_\sigma(R,x)\ne0$ 且
$\operatorname{sgn}\det D_xF_\sigma(R,x)=(-1)^n$;
(G2) 块宽在紧 $R$ 区间上一致正 (无退化配置).
则: (i) 度 $\deg(F_\sigma(R,\cdot),W,0)$ 同伦不变; (ii) $R=1$ 处唯一解
$x^*$ 非退化且符号 $(-1)^n$, 度 $=(-1)^n$;
(iii) 对 $R\in(1,R_0]$, $(-1)^n=\#\{\text{解}\}\cdot(-1)^n$, 故恰有一解;
(iv) 等变 + 唯一性给出 $x^*(R)$ 对称; (v) 结合有限块约化与带自洽
(弱星紧性 + bang-bang + 恰 $2n$ 有效开关), 全局极值子 $=$ 唯一解, 故极值子
唯一且对称.

**R=1 一般 $n$ 分析 (STRICT, 新工具内容)**: $R=1$ 时带自洽退化为
$f_1(x)=2\pi^2\big(n^2\sin^2(n\pi x)-(n+1)^2\sin^2((n+1)\pi x)\big)=0$.
直接 Wronskian 公式 $W=-2(n+1)\pi\sin(\pi x)<0$ 与商函数胞腔单调性给出:
$f_1$ 恰 $2n$ 个简单零点 $x_1^*<\cdots<x_{2n}^*$, 反射对称
($x_{2n+1-j}^*=1-x_j^*$), 每胞腔 $(w_{i-1},w_i)$ 恰 2 个,
区间符号 $(-,+,-,\dots,-)$ ($f_1(0+)=f_1(1-)=0$, 端点附近为负),
$\operatorname{sgn}f_1'(x_j^*)=(-1)^{j+1}$,
$\operatorname{sgn}\det D_xF(1,x^*)=(-1)^n$. 这是 (G1$'$) 与局部唯一性
(隐函数) 在 $R=1$ 处的初等基座. $n=2$ 闭式:
$t=(11\pm2\sqrt{10})/36$, 零点 $\approx(0.25597364,0.38264716,0.61735284,0.74402636)$,
$\det J\approx1.43180\times10^5$ (数值复算 $\prod f_1'(x_j^*)/(9\pi^2)^4=143179.8687$).

## 适用范围

- **适用**: $n\ge2$ 相邻谱隙 $D_n=\lambda_{n+1}-\lambda_n$ 极值子的反射对称性
  与唯一性论证; 一般具有回文图案与边缘反射等变性的参数化边值问题;
  把 "对称点 Jacobian 交叉块化" 用作降维工具 ($\det$ 化为两块乘积);
  把 "R=1 唯一非退化解 + 拓扑度" 用作全局分支唯一性的充分性框架.
- **边界情形**: $R=1$ (等变平凡化, 退化为显式 $f_1$, 全部初等);
  $R\to\infty$ 极限 (SUP 中心质量钉扎 $D\to4\pi^2$, INF $D\to0$;
  与 (G2) 不矛盾, G2 只约束有限 $R$); 非回文图案无等变性, 本工具不适用.
- **不适用 / 注意**: (G1$'$) 与 (G2) 目前是开放条件, 未证时框架只给
  充分性, 不得宣称全局唯一性/对称性已证; 等变性要求图案回文
  ($\sigma_i=\sigma_{2n+2-i}$), 一般图案需另法; 对称化不等式路线
  (对密度取平均 $\bar\rho$) 已被否证为单调工具: SUP 118/200、
  INF 116/200 个随机例出现 $D(\bar\rho)<D(\rho)$, 无单调性
  (EVIDENCE, 见 recon 文档).

## 验证与备注

- 来源: 自研 (会话 58 续作 4b, 2026-08-12); 主文档
  docs/SL_gap_nge2_symmetry_local_proof.pdf (9 页, 零警告; §2 结构定理,
  §3 R=1 一般 $n$, §4 R$\to$1 局部定理含唯一性边界排除引理 4.2/4.3,
  §5 拓扑度框架); 侦察文档 docs/SL_gap_nge2_symmetry_recon.pdf (5 页,
  零警告; 失败路线登记 6 条, 含旧对称化数字不可复现的更正).
- 数值交叉检验 (EVIDENCE, 不构成证明): scripts/_gapn2_symmetry_recon.py,
  scripts/_gapn2_jacobian_probe.py, scripts/_gapn2_antigrid_search.py;
  R=1 零点结构 n=2..8 全过; 等变恒等式 $D(\bar x)\equiv D(x)$ 数值 1e-16;
  n=2 沿 R 分支 $\det J>0$ (SUP $1.38\times10^5\to330$,
  INF $1.22\times10^5\to0.123$, $R\in[1.05,100]$); 侦察约 2000 次求解
  未发现内部非对称解或边界聚点; n=2, R=4 反对称平面网格无解;
  n=2..5, R$\in\{2,4,10\}$, 两图案, 每图案恰一带自洽驻点, 对称到 1e-11.
- 诚实登记: §5 (G1$'$)/(G2) 为开放条件, 全局闭合是充分性框架非证明;
  §3 谱符号 ($u_k'(0)>0$ 等) 为 1 维经典结果, 自证依赖已标注;
  旧交接记载的对称化反例数字 (33/200, 57/200) 无法复现, 以本会话
  复算数据 (118/116) 为准.
- 相关工具: [[gap-band-extremals]] (带自洽驻点判据), [[switch-saturation-k-invariant]]
  (恰 $2n$ 开关), [[feynman-hellmann]] (跳点公式), [[keller-variational]] (变分归约),
  [[well-family-rigidity]] (n=1 对称刚性, 本工具是 n>=2 对应物).
