# -*- coding: utf-8 -*-
"""Insert the 2026-08-12 audit section into SL_gap_nge2_symmetry_local_proof.tex."""
import io

path = r'F:\LaTeX\BVE research\docs\SL_gap_nge2_symmetry_local_proof.tex'
with io.open(path, 'r', encoding='utf-8') as f:
    c = f.read()

anchor = r'\begin{remark}[涉及到的数学知识]'
assert anchor in c, 'anchor not found'
assert r'\section{带自洽点处' not in c, 'section already present'

section = r'''
\section{带自洽点处 Jacobian/Hessian 的闭式结构 (STRICT 增补, 2026-08-12)}\label{sec:aug}

本节目的是把 (G1$'$) 归约为一个可检验的矩阵符号条件, 并给出
$\tilde M$ 对角部分的闭式分解. 记号: $s_i:=\rho(x_i+)-\rho(x_i-)$
(交替 $\pm(R-1)$), $w_j:=\lambda_nu_n(x_j)^2=\lambda_{n+1}u_{n+1}(x_j)^2$
(带自洽点), $\tilde G_k(x,y):=\sum_{l\ne k}u_l(x)u_l(y)/(\lambda_l-\lambda_k)$
(正则化谱和).

\begin{proposition}[第一阶变分恒等式]\label{prop:firstorder}
设 $x$ 为带自洽点. 则
\begin{equation*}
	\frac{d\lambda_k}{dx_i}=+\lambda_k s_i u_k(x_i)^2,\qquad
	\frac{dD}{dx_i}=-s_i f(x_i),
\end{equation*}
且 Jacobian 有分解
\begin{equation*}
	J=D_xF=\frac{\tilde D+\tilde M}{\lambda_{n+1}},\qquad
	\tilde D=\operatorname{diag}(f'(x_j)),
\end{equation*}
\begin{equation}\label{eq:Mtilde}
	\tilde M_{ji}=s_i\Bigl\{
	\frac{2w_iw_jD}{\lambda_n\lambda_{n+1}}
	-2\lambda_n^2u_n(x_i)u_n(x_j)\tilde G_n(x_i,x_j)
	+2\lambda_{n+1}^2u_{n+1}(x_i)u_{n+1}(x_j)\tilde G_{n+1}(x_i,x_j)\Bigr\}.
\end{equation}
\end{proposition}
\begin{proof}
$\delta\rho=-s_i\,\delta(x-x_i)\,dx_i$ (开关右移使 $[x_i,x_i+dx_i)$ 由
$\mathrm{pat}[i+1]$ 变为 $\mathrm{pat}[i]$). 对加权弦
$A=-(1/\rho)d^2/dx^2$ 有 $\delta A=(\delta\rho/\rho^2)d^2/dx^2$, 一阶扰动论
给出 $d\lambda_k/dx_i=+\lambda_ks_iu_k(x_i)^2$ 与
$du_k(x)/dx_i=+\frac12s_iu_k(x_i)^2u_k(x)-\lambda_ks_iu_k(x_i)\tilde G_k(x,x_i)$.
组合两模式并在带自洽点使用 $w_j=\lambda_nu_n^2=\lambda_{n+1}u_{n+1}^2$
即得 \eqref{eq:Mtilde} (逐项核对见 \EVIDENCE 第~\ref{sec:aug-ev} 节).
\end{proof}

\begin{proposition}[(G1$'$) 的矩阵归约]\label{prop:K}
令 $K:=\operatorname{diag}(1/s)J$. 则 $K$ 对称
(因 $|s_i|\equiv R-1$), 且
\begin{equation}\label{eq:detK}
	\det J=(R-1)^{2n}(-1)^n\det K,\qquad
	\operatorname{Hess}(D_n)=-\lambda_{n+1}(R-1)^2K,
\end{equation}
故 (G1$'$) 等价于: 每个带自洽点处 $\det K>0$, 亦等价于
$\operatorname{Hess}(D_n)$ 处处定号 (SUP: 负定, INF: 正定).
\end{proposition}
\begin{proof}
$\prod_is_i=(R-1)^{2n}(-1)^n$ (两种图案均成立); 由
$\operatorname{Hess}(D_n)=-\lambda_{n+1}\operatorname{diag}(s)J$ (命题~\ref{prop:firstorder}
的微分) 与 $\operatorname{diag}(s)^2=(R-1)^2I$ 即得.
\end{proof}

\begin{proposition}[部分分式恒等式与 $\tilde M$ 对角闭式]\label{prop:pf}
设 $x$ 为带自洽点, $D=\lambda_{n+1}-\lambda_n$. 则
\begin{equation}\label{eq:pf}
	\lambda_{n+1}\tilde G_{n+1}(x_j,x_j)-\lambda_n\tilde G_n(x_j,x_j)
	=\Sigma'(x_j)-\frac{2w_j}{D}-\frac{w_jD}{\lambda_n\lambda_{n+1}},
\end{equation}
\begin{equation*}
	\Sigma'(x_j):=\sum_{l\ne n,n+1}
	\frac{\lambda_l u_l(x_j)^2D}{(\lambda_l-\lambda_{n+1})(\lambda_l-\lambda_n)}>0
	\quad(\text{严格, 逐项为正}),
\end{equation*}
从而
\begin{equation}\label{eq:mdiag}
	\frac{\tilde M_{jj}}{s_j}=2w_j\Sigma'(x_j)-\frac{4w_j^2}{D},
	\qquad
	K_{jj}=\frac{\sigma\cdot 2c|W(x_j)|}{R-1}
	+\frac{2w_j\Sigma'(x_j)}{\lambda_{n+1}}
	-\frac{4w_j^2}{D\lambda_{n+1}},
\end{equation}
其中 $\sigma=+1$ (SUP), $\sigma=-1$ (INF), $c=\sqrt{\lambda_n/\lambda_{n+1}}$.
\end{proposition}
\begin{proof}
由 $\lambda/(\lambda_l-\lambda)=\lambda_l/(\lambda_l-\lambda)-1$ 展开
$\lambda_{n+1}\tilde G_{n+1}-\lambda_n\tilde G_n$: 对 $l\ne n,n+1$ 得
$\Sigma'$ 的项; $l=n$ 项贡献 $-\lambda_nu_n(x_j)^2/D=-w_j/D$,
$l=n+1$ 项贡献 $-\lambda_{n+1}u_{n+1}(x_j)^2/D=-w_j/D$; 余项
$u_{n+1}(x_j)^2-u_n(x_j)^2=-w_jD/(\lambda_n\lambda_{n+1})$. 代入
$\tilde M_{jj}/s_j=2w_j\bigl(\frac{w_jD}{\lambda_n\lambda_{n+1}}
+\lambda_{n+1}\tilde G_{n+1}-\lambda_n\tilde G_n\bigr)$
即得 \eqref{eq:mdiag}; 第一项用恒等式
$f'(x_j)=-2\lambda_{n+1}\varepsilon_jcW(x_j)$ 与
$\varepsilon_j=u_{n+1}(x_j)/u_n(x_j)/c=\pm1$:
$\varepsilon_j=s_j/(R-1)$ (SUP) 而 $\varepsilon_j=-s_j/(R-1)$ (INF),
且 $W<0$ (定理~\ref{thm:structure}(a)), 故
$f'(x_j)/s_j=\sigma\cdot 2c|W(x_j)|/(R-1)$.
\end{proof}

\begin{proposition}[Wronskian 的 $D$ 界]\label{prop:Wbound}
对任意配置 (不限于带自洽点), $|W(x)|\le D$ 对一切 $x\in[0,1]$ 成立.
\end{proposition}
\begin{proof}
$W(0)=0$ 且 $W'=-D\rho u_nu_{n+1}$, 故
$W(x)=-D\int_0^x\rho u_nu_{n+1}\,dt$; Cauchy--Schwarz 与归一化
$\int_0^1\rho u_k^2\,dt=1$ 给出 $|W(x)|\le D$.
\end{proof}

\section{2026-08-12 审计增补: 符号审计与余量表 (EVIDENCE)}\label{sec:aug-ev}

以下全部为数值证据, 不构成证明; 其支撑的严格部分见
第~\ref{sec:aug} 节.

\begin{itemize}
	\item 符号审计 (FD, 步长 $10^{-4}$..$10^{-6}$):
	$d\lambda_k/dx_i=+\lambda_ks_iu_k(x_i)^2$ (12 位),
	$dD/dx_i=-s_if(x_i)$ (更正会话 51 记录的 $-(R-1)f(a)$ 符号;
	零集 $f=0$ 不变, 符号型论证须按新约定复核),
	$\operatorname{Hess}(D_n)=-\lambda_{n+1}\operatorname{diag}(s)J$
	(逐元素误差 4.6e-3, 量级 $10^3$);
	$K=\operatorname{diag}(1/s)J$ 对称 (crossK~1e-13);
	$\tilde M$ 公式与 jac\_fd 相对误差 ~1e-6 (中等 $R$).
	\item 恒等式 \eqref{eq:pf} 与 \eqref{eq:mdiag}: 一次预计算谱和
	($N=800$) 验证, 相对误差 $10^{-13}$..$10^{-15}$
	($n=2,3$, $R\in\{1.2,2,4,10\}$, 两图案). 曾试错两个错误闭式
	(漏极点消去项; $u_{n+1}^2-u_n^2$ 符号), 均被同一脚本拒绝.
	\item (G1$'$) 数值余量表 (对称分支, FD 权威):
	SUP $n=2..4$, $R\in[1.05,100]$: $\operatorname{sgn}\det J=(+1)^n$ 恒成立,
	$K$ 的特征值全正 (Hess 负定), 最小 $|\mathrm{ev}K|$ 在 $R=100$ 处为
	$0.0156/0.0185/0.0214$ ($n=2/3/4$);
	INF $n=2$ ($R\le100$), $n=3$ ($R\le75$), $n=4$ ($R\le40$):
	$\operatorname{sgn}\det J=(-1)^n$ 恒成立, ev$K$ 全负 (Hess 正定),
	最小 $|\mathrm{ev}K|$ 指数衰减至 ~$10^{-5}$ (无一致下界, 未发现符号翻转);
	近简并区解析谱和 Jacobian 不可靠 ($n=3,R=75$ 处伪 detJ 符号翻转已更正为
	FD 值 $-1.0125\times10^{-5}$, 步长收敛稳定).
	\item 死路登记: Gershgorin 对角占优 ($|K_{jj}|>\sum_{i\ne j}|K_{ji}|$)
	仅小 $R$ 成立 ($n=3$ INF $R=10$ 余量 $-38.1$); H-矩阵缩放
	(Perron--Frobenius: $\rho(\operatorname{diag}(|K_{jj}|)^{-1}|K_{\mathrm{off}}|)<1$)
	在 $n=2$ INF $R=4$ (1.31), $n=3$ SUP $R=4$ (1.05), $n=3$ INF $R=2$ (1.36)
	失败. 两候选路线均被否证, 严格证明需控制 Green 离对角部分.
	\item Sylvester 主元 (新证据): 沿对称分支 $K$ 的无换主元符号恒定
	(SUP 全正, INF 全负; $n=2,3$, $R\in\{1.2,2,4,10\}$), 与 $\det K>0$ 一致;
	由惯性律, 主元符号恒定等价于 (G1$'$). 符号模式
	($n=2$ SUP $R=4$): 对角 $+$, 非对角 $-$, 中央 $2\times2$ 块
	$\begin{psmallmatrix}++\\++\end{psmallmatrix}$;
	$K_+$ 与 $K_-$ 均 $\begin{psmallmatrix}+&-\\-&+\end{psmallmatrix}$ 型.
\end{itemize}

'''
idx = c.index(anchor)
c = c[:idx] + section + c[idx:]
with io.open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(c)
print('inserted OK, new length', len(c))
