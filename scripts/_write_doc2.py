# -*- coding: utf-8 -*-
import io
p = r'docs\SL_fixed_n_supremum.tex'
tex = r"""% 编译方式: xelatex SL_fixed_n_supremum.tex
\documentclass[UTF8]{ctexart}
\usepackage{amsmath, amssymb, amsthm}
\usepackage[margin=2.5cm]{geometry}
\usepackage[hyphens]{url}
\usepackage[hidelinks]{hyperref}
\usepackage{booktabs}
\emergencystretch 3em

\newtheorem{theorem}{定理}[section]
\newtheorem{lemma}[theorem]{引理}
\newtheorem{corollary}[theorem]{推论}
\newtheorem{remark}[theorem]{注}
\newtheorem{proposition}[theorem]{命题}
\newtheorem{conjecture}[theorem]{猜想}

\title{固定指标 $n$ 的相邻特征值比值上确界: 交替极值配置的平衡相位结构}
\author{研究证明文档 (项目: BVE research)}
\date{2026-08-05}

\begin{document}
\maketitle

\begin{abstract}
本文研究概述文档第 2 号开放问题: 固定 $n \geq 1$ 时, 对 $0 < a \leq
\rho \leq A$, 弦方程 $-y'' = \lambda\rho(x)y$ (Dirichlet) 的相邻比值
$\lambda_{n+1}(\rho)/\lambda_n(\rho)$ 的上确界 $\Lambda_n^{\sup}(R)$
($R = A/a$). 会话 5 证明了全序列上确界
$\sup_n \Lambda_n^{\sup}(R) = \nu(R)$, 并给出猜想: 交替 bang-bang 配置
$[1, R, 1, \dots, 1]$ ($2n+1$ 块, 宽度比 $\sqrt{R}$) 达到
$\Lambda_n^{\sup}(R) = c_n(R)$. 本文取得以下进展:
\begin{enumerate}
	\item \emph{反射对称定理 (严格, 定理 \ref{thm:sym})}: 交替配置的世俗方程
		$F_n(y) = 0$ ($y = \omega\sqrt{R}\,t$, $t$ 为块宽) 满足
		$F_n(\pi - y) = F_n(y)$ 对一切 $n$; 证明用单元转移矩阵的
		$J$-共轭 ($J = \operatorname{diag}(1,-1)$).
	\item \emph{平衡定理 (数值, 定理 \ref{thm:balance})}: 世俗方程的根
		$y_1 < \dots < y_{2n}$ 恰为 $2n$ 个 (位于 $(0,\pi)$), 且按
		$y_j + y_{2n+1-j} = \pi$ 配对; 特别地
		$y_n + y_{n+1} = \pi$, 故
		\begin{equation}
			\frac{\lambda_{n+1}}{\lambda_n} = \Bigl(\frac{\pi - y_n}{y_n}\Bigr)^2,
			\qquad y_n = \sqrt{R}\,t\,\sqrt{\lambda_n}.
		\end{equation}
	\item \emph{显式闭式}: $n=1$: $y_1 = \arccos\frac{\sqrt R}{\sqrt R + 1}$
		(复得会话 5 的 $\nu(R)$); $n=2$:
		$y_2 = \arccos\frac{\sqrt{1+4R}-1}{2(\sqrt R+1)}$, 数值验证至
		$10^{-14}$; $n = 3, 4$ 由 $F_n$ 的次数 $2n$ 多项式给出.
	\item \emph{极值性数值证据}: $n=2$, $R=4$ 时 5 块族优化精确收敛到
		猜想配置 (比值 $4.2846614708$); 7 块优化塌缩到 5 块配置;
		3--11 块随机搜索全部低于猜想值; 猜想点处比值梯度为零.
\end{enumerate}
未闭合: 全局极值性 (Keller 型归约到交替 bang-bang) 与
$2n$-根计数的一般证明, 如实登记.
\end{abstract}

\tableofcontents

\section{问题与猜想}

设 $0 < a \leq A$, $R = A/a$. 考虑
\begin{equation}
	-y'' = \lambda\,\rho(x)\,y, \qquad y(0) = y(1) = 0,
	\qquad a \leq \rho \leq A,
\end{equation}
特征值 $0 < \lambda_1(\rho) < \lambda_2(\rho) < \cdots$.
固定 $n \geq 1$, 记
\[
	\Lambda_n^{\sup}(R) := \sup_{\rho} \frac{\lambda_{n+1}(\rho)}{\lambda_n(\rho)}.
\]
会话 5 证明 $\sup_{n \geq 1}\Lambda_n^{\sup}(R) = \nu(R)$ (全序列上确界),
并数值发现猜想极值配置: 交替 bang-bang
\begin{equation}\label{eq:alt}
	\rho = [1, R, 1, R, \dots, 1] \quad (2n+1 \text{ 块}),
	\qquad w_1 = w_3 = \dots = \sqrt{R}\,t,\; w_2 = w_4 = \dots = t,
	\qquad t = \frac{1}{(n+1)\sqrt R + n}.
\end{equation}
本文把这些配置的比值结构完全刻画 (反射对称 + 平衡相位), 给出闭式与
$c_n(R)$, 并把 ``$c_n(R)$ 是全局上确界'' 归约为一个更小的缺口
(见第 5 节).

\section{交替配置的世俗方程与反射对称}

令 $s = \sqrt R$, $y = \omega\,s\,t$ ($\omega = \sqrt\lambda$).
对 (eq:alt) 的每个单元 $[1, R]$ (宽度 $st, t$), 两块的相位均为 $y$:
块 1 (密度 1, 长度 $st$): $\omega \cdot st = y$; 块 2 (密度 $R$, 长度
$t$): $\omega\sqrt R \cdot t = y$. 单元转移矩阵
\[
	T_{\mathrm{cell}}(y) =
	\begin{pmatrix}
		\cos^2 y - s^{-1}\sin^2 y & \dfrac{(1+s)\sin y\cos y}{\omega s}\\[2mm]
		-\omega(1+s)\sin y\cos y & \cos^2 y - s\sin^2 y
	\end{pmatrix},
\]
末块 $[1]$ (宽度 $st$, 相位 $y$): $T_{\mathrm{end}}(y)$. 世俗函数
\begin{equation}
	F_n(y) := \bigl(T_{\mathrm{end}}(y)\,T_{\mathrm{cell}}(y)^n\bigr)_{01},
	\qquad \text{Dirichlet 特征值} \iff F_n(y) = 0.
\end{equation}

\begin{theorem}[反射对称]\label{thm:sym}
	对一切 $n \geq 1$ 与 $s > 0$,
	$F_n(\pi - y) = F_n(y)$.
\end{theorem}

\begin{proof}
	直接验证 $J\,T_{\mathrm{cell}}(y)\,J = T_{\mathrm{cell}}(\pi-y)$ 与
	$J\,T_{\mathrm{end}}(y)\,J = -T_{\mathrm{end}}(\pi-y)$, 其中
	$J = \operatorname{diag}(1, -1)$ (利用 $\cos(\pi-y) = -\cos y$,
	$\sin(\pi-y) = \sin y$). 于是
	\begin{equation}
		M_n(\pi-y) = T_{\mathrm{end}}(\pi-y)T_{\mathrm{cell}}(\pi-y)^n
		= (-J\,T_{\mathrm{end}}(y)J)(J\,T_{\mathrm{cell}}(y)J)^n
		= -J\,M_n(y)\,J,
	\end{equation}
	故 $(M_n(\pi-y))_{01} = -J_{00}(M_n(y))_{01}J_{11} = (M_n(y))_{01}$.
	\qed
\end{proof}

\begin{remark}
	定理 \ref{thm:sym} 的证明不依赖 $n$, 是严格结论. 它说明 $F_n$ 的根
	关于 $\pi/2$ 反射对称: 若 $y$ 是根, 则 $\pi - y$ 也是根.
\end{remark}

\section{平衡定理与闭式}

\begin{theorem}[根计数与配对]\label{thm:balance}
	对交替配置 (eq:alt), $F_n$ 在 $(0, \pi)$ 中恰有 $2n$ 个根
	$y_1 < y_2 < \dots < y_{2n}$, 且 $y_j + y_{2n+1-j} = \pi$
	($j = 1, \dots, n$). 特别地 $y_n + y_{n+1} = \pi$, 于是
	\begin{equation}
		\frac{\lambda_{n+1}}{\lambda_n}
		= \Bigl(\frac{y_{n+1}}{y_n}\Bigr)^2
		= \Bigl(\frac{\pi - y_n}{y_n}\Bigr)^2
		=: c_n(R).
	\end{equation}
\end{theorem}

\begin{proof}[证明结构与层级]
	配对是定理 \ref{thm:sym} 的直接推论 ($F_n$ 的根关于 $\pi/2$ 对称).
	$2n$-根计数: $F_n(y) = \sin y\,Q_n(\cos y)$ 且 $Q_n$ 是次数 $2n$ 的
	多项式 (符号验证 $n \leq 4$); 数值验证 $Q_n$ 在 $(-1,1)$ 中恰有
	$2n$ 个根 ($n \leq 6$, $R \in \{2,4,7,10\}$, 配对残差 $\leq
	4.4\times10^{-16}$). $y_n < \pi/2 < y_{n+1}$ 由计数与排序自动成立.
	把 $2n$-根计数提升为严格证明是开放缺口之一 (见第 5 节); 一旦计数
	成立, (2) 是定理.
\end{proof}

\begin{theorem}[显式闭式]\label{thm:closed}
	$y_n$ ($n$ 配置的平衡相位) 的闭式:
	\begin{align}
		n = 1: &\quad \cos y_1 = \frac{s}{s+1},\qquad
			c_1(R) = \nu(R);\\
		n = 2: &\quad \cos y_2 = \frac{\sqrt{1+4s^2}-1}{2(s+1)},\qquad
			c_2(R) = \Bigl(\frac{\pi}{y_2} - 1\Bigr)^2;\\
		n = 3, 4: &\quad y_n = \arccos C_n,\; Q_n(C_n) = 0,\;
			Q_3, Q_4 \text{ 见 } \path{scripts/op02_poly_extract.py}.
	\end{align}
	数值: $y_2 = \arccos\frac{\sqrt{1+4R}-1}{2(\sqrt R+1)}$ 与直接特征值
	提取的差 $\leq 4.4\times10^{-14}$ ($R = 2, 4, 10, 100$).
\end{theorem}

\begin{proof}
	$n = 1$: $Q_1(C) = (s+1)^2C^2 - s^2$, 根 $C = s/(s+1)$
	(会话 5 的平衡相位 $\theta$). $n = 2$: 半弦 $[1,R,1]$ 的 Dirichlet
	世俗方程 (符号推导): $\sin(y/2)\,[(s+1)^2C^2 + (s+1)C - s^2] = 0$,
	根 $C = (-1 + \sqrt{1+4s^2})/(2(s+1))$. $n = 3, 4$: $F_n$ 的
	$Q_n$ 由符号计算给出, 数值求根与直接特征值一致 (表 1). \qed
\end{proof}

\begin{table}[ht]
\centering
\caption{$c_n(R)$: 交替配置比值 ((2) 式) 与直接特征值计算的对照}
\begin{tabular}{c|ccccc}
	$n$ & 1 & 2 & 3 & 4 & 5 \\\hline
	$R=4$, (2) 式 & 7.481533386 & 4.284661471 & 3.453882959 & 3.091176917 & 2.894425766\\
	$R=4$, 直接 & 7.481533386 & 4.284661471 & 3.453882960 & 3.091176917 & 2.894425766\\
	$R=10$, (2) 式 & 11.820372828 & 6.939060695 & 5.705227369 & 5.181332498 & 4.904313087
\end{tabular}
\end{table}

\section{极值性的数值证据}

对 $n=2$, $R=4$ (猜想值 $c_2(4) = 4.2846614708$):
\begin{enumerate}
	\item \textbf{5 块族优化}: Nelder-Mead 从 9 个随机起点出发全部收敛到
		宽度 $(0.25, 0.125, 0.25, 0.125, 0.25)$ (即 $w_1/w_R = 2 =
		\sqrt 4$), 比值 $4.28466147$ (脚本 \path{scripts/op02_n2_opt.py}).
	\item \textbf{7 块优化塌缩}: 7 块 Nelder-Mead 收敛到
		$(0.25, 0.125, 0.25, 0.124, 0, 0, 0.25)$ —— 中间两块的宽度趋于
		零, 回到 5 块配置; 即额外块不提升比值.
	\item \textbf{随机搜索}: 3/5/7/9/11 块各 300 个随机 Dirichlet 配置,
		最大 $\lambda_3/\lambda_2$ 分别为 $2.89/3.98/4.17/3.72/3.36$,
		均 $< c_2(4)$.
	\item \textbf{临界点}: 猜想配置处 $\lambda_3/\lambda_2$ 对跳点的
		中心差分梯度为 $O(h^2)$ (即零梯度, 有限差分噪声 $\sim
		10^{-4}$ 由特征值精度引起).
	\item \textbf{Keller 变分条件}: 会话 5 对 $n = 1..8$ 符号级验证
		($10^{-11}$).
\end{enumerate}

\section{开放缺口 (如实登记)}

\begin{description}
	\item[全局极值性] 猜想 $\Lambda_n^{\sup}(R) = c_n(R)$ 等价于两步:
		(a) 对固定 $n$, Keller 变分条件把极值配置归约到交替 bang-bang
		$[1,R,\dots,1]$ (会话 5 的工具); (b) 在交替族内, 比值
		$\lambda_{n+1}/\lambda_n$ 在宽度比 $w_1/w_R = \sqrt R$ 处取最大.
		本会话完成 (b) 的结构 (平衡相位 $y_n$), 未完成 (a) 与 (b) 的
		单调性证明.
	\item[$2n$-根计数] 定理 \ref{thm:balance} 依赖 ``$Q_n$ 在 $(-1,1)$
		恰有 $2n$ 个根'' 的数值验证; 严格证明 (如 Sturm 型论证) 未完成.
	\item[单调收敛] $\Lambda_n^{\sup}(R) \downarrow c_\infty(R)$ 的严格证明,
		以及 $c_\infty(R) = ((\pi-\varphi_1)/\varphi_1)^2$ 与 $n \to \infty$
		极限 $\lim_n y_n = \varphi_1$ 的验证, 未完成.
\end{description}

\section{涉及到的数学知识}

\begin{description}
	\item[转移矩阵与世俗方程] 分段常数密度的特征值问题化为 $2\times2$
		转移矩阵乘积的 $01$ 分量求根.
	\item[反射对称与 $J$-共轭] $\operatorname{diag}(1,-1)$ 共轭给出
		$T(\pi-y)$ 与 $T(y)$ 的关系; 与能带理论中 Bloch 相位对称同源.
	\item[特征值交错] 对称密度的特征值分裂为半弦 Dirichlet ($\nu_k$) 与
		mixed ($\mu_k$) 两类, $\mu_k < \nu_k < \mu_{k+1} < \nu_{k+1}$;
		用于 $y_n < \pi/2 < y_{n+1}$.
	\item[平衡相位方法] 会话 5 的自研工具: 使相邻特征值相位互补
		($y_n + y_{n+1} = \pi$) 的配置; 本会话将其推广到固定 $n$.
	\item[极值问题的变分条件] Keller 变分原理与 Mahar--Willner 两步结构;
		Feynman--Hellmann 导数.
\end{description}

\begin{thebibliography}{5}
\bibitem{ratio} 项目文档, \emph{相邻特征值比值: 全序列上确界与平衡相位方法}
	(会话 5), \path{docs/SL_ratio_proof.pdf}.
\bibitem{summary} 项目文档, \emph{SL 谱主题总结与前沿开放问题} (会话 8),
	\path{docs/SL_spectral_topics_summary.pdf}.
\bibitem{keller} J. B. Keller, \emph{The minimum ratio of two eigenvalues},
	SIAM J. Appl. Math. 31 (1976), 485--491. \url{https://doi.org/10.1137/0131042}
\bibitem{mw} T. J. Mahar, B. Willner, \emph{An extremal eigenvalue problem},
	Comm. Pure Appl. Math. 29 (1976), 517--529.
	\url{https://doi.org/10.1002/cpa.3160290505}
\bibitem{wm} B. Willner, T. J. Mahar, \emph{Extremal eigenvalue problems for
	Sturm--Liouville operators with two-point constraints}, SIAM J. Math. Anal.
	13 (1982), 557--570. \url{https://doi.org/10.1137/0513040}
\end{thebibliography}

\end{document}
"""
io.open(p, 'w', encoding='utf-8').write(tex)
print("written", len(tex), "chars")
