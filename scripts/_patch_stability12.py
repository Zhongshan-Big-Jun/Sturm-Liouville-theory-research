# -*- coding: utf-8 -*-
import io
p = r'docs\SL_stability_moment_jump.tex'
s = io.open(p, encoding='utf-8').read()

newsec = r"""
\subsection{精确二分: 对数总和门槛与门槛线分类}

本小节把门槛分类推进到完备: 定义\emph{对数总和}
\begin{equation}
	S(m) := \sum_{k=2}^{m} \log(1+\varepsilon_k)
	\;\; \Bigl(= \log \prod_{k=2}^m (1+\varepsilon_k)\Bigr).
\end{equation}
因为 $\log(1+\varepsilon) \geq (\log 2)\min(\varepsilon,1)$, 条件
$S(m) = \omega(\log m)$ 弱于定理 \ref{thm:stability} 中的
$\sum\min(\varepsilon_k,1) = \omega(\log m)$; 它才是真正控制
$u_m$ 增长的量 ($\log u_m \geq S(m)$).

\begin{theorem}[$S$-门槛: 充分性]\label{thm:Sthr}
	若 $S(m) = \omega(\log m)$, 则 $u_m/m^\beta \to \infty$ 对一切
	$\beta \geq 0$, 且 $\{q_n\}$ 在任何满足 (H1)(H2) 与多项式范数界
	$\|x^k\|_H \leq C_H k^\beta$ 的空间 $H$ 中完备.
\end{theorem}

\begin{proof}
	定理 \ref{thm:growth} 给出 $\log u_m \geq S(m) = \omega(\log m)$,
	故 $u_m$ 超多项式; 余下与定理 \ref{thm:stability} 的证明完全相同
	(矩 $M_{2m} = M_2 u_m$ 与多项式上界 $|M_{2m}| \leq \|w\|\,C_H(2m)^\beta$
	矛盾). \qed
\end{proof}

\begin{theorem}[对角空间的精确判据]\label{thm:exact}
	在对角空间 $H_\beta$ (内积 $(x^j,x^k) = \delta_{jk}(k+1)^{2\beta}$) 中,
	设 $u'_m$ 为奇次递推 ($c_0 u'_m = A'_m u'_{m-1} - B'_m u'_{m-2}$,
	$u'_0=0$, $u'_1=1$) 的解. 则 $\{q_n\}$ 在 $H_\beta$ 中完备当且仅当
	\begin{equation}
		\sum_{m \geq 1} \frac{u_m^2}{(2m+1)^{2\beta}} = \infty
		\quad\text{且}\quad
		\sum_{m \geq 1} \frac{(u'_m)^2}{(2m+2)^{2\beta}} = \infty.
	\end{equation}
\end{theorem}

\begin{proof}
	设 $w \perp \operatorname{span}\{q_n\}$, 记 $M_k = (w, x^k)_H$.
	由 $q_0, q_1$ 得 $M_0 = M_1 = 0$; 由 (3) 得
	$c_0 M_{2m} = A_m M_{2m-2} - B_m M_{2m-4}$, 故 $M_{2m} = M_2 u_m$
	($M_4 = A_2 M_2/c_0$ 起归纳). 反之, 给定标量 $M_2$, 向量
	$w = M_2 \sum_{m \geq 1} u_m (2m+1)^{-2\beta} x^{2m}$ 满足
	$(w, x^{2m}) = M_2 u_m$ 且 $\|w\|^2 = M_2^2 \sum_m u_m^2 (2m+1)^{-2\beta}$
	($H_\beta$ 的对角性). 故存在非零 $w \perp \operatorname{span}\{q_n\}$
	当且仅当偶次级数与奇次级数 (同理) 之一收敛. \qed
\end{proof}

\begin{corollary}[二分]\label{cor:di}
	设 $S(m) = O(\log m)$ (等价地存在 $D$ 使 $u_m \leq C m^D$),
	则 $\{q_n\}$ 在 $H_\beta$ 中对 $\beta > D + 1/2$ 不完备.
	特别地, 定理 \ref{thm:Sthr} 的充分条件是\emph{精确门槛}:
	$S = \omega(\log m)$ 对一切 $\beta$ 完备, 而 $S = O(\log m)$
	在某个对角空间中不完备. 在模型族中判据 (7) 可显式求和.
\end{corollary}

\begin{theorem}[门槛线: $\varepsilon_k = C/(k\log k)$]\label{thm:line}
	设 $\varepsilon_k = \varepsilon'_k = C/(k\log k)$ ($C > 0$, $k \geq 2$).
	则 $S(m) \sim C\log\log m$, $u_m \asymp (\log m)^C$ 仅为多项式增长
	($u_m/m^\delta \to 0$ 对一切 $\delta > 0$), 且 $\{q_n\}$ 在 $H_\beta$
	中完备当且仅当 $\beta \leq 1/2$. 门槛线 $\varepsilon_k \sim 1/(k\log k)$
	由此得到\emph{完全分类}.
\end{theorem}

\begin{proof}
	$\log u_m = \sum_{k=2}^m \log(1 + C/(k\log k)) \sim C \sum_{k=2}^m
	\frac{1}{k\log k} \sim C\log\log m$ (积分判别), 故
	$u_m \asymp (\log m)^C$. 判据 (7) 化为 $\sum_m (\log m)^{2C}(2m)^{-2\beta}$,
	由积分判别收敛当且仅当 $2\beta > 1$. \qed
\end{proof}

\begin{theorem}[模型族的显式门槛]\label{thm:model}
	设 $\varepsilon_k = \varepsilon'_k = C/k$. 则 $u_m = m^C/\Gamma(2+C)(1+o(1))$
	(定理 \ref{thm:sharp} 的闭式, 常数为 $\Gamma(2+C)$), 且
	$\{q_n\}$ 在 $H_\beta$ 中完备当且仅当 $\beta \leq C + 1/2$
	($\beta = C+1/2$ 处级数按 $\sum_m m^{-1}$ 发散, 对数型). 特别地,
	临界幂次 $\beta = C+1/2$ 处\emph{恰好}完备.
\end{theorem}

\begin{proof}
	判据 (7) 与 $\sum_m m^{2C} m^{-2\beta}$ 的积分判别:
	收敛当且仅当 $2C - 2\beta < -1$, 即 $\beta > C+1/2$; 在
	$\beta = C+1/2$ 处为 $\sum_m m^{-1} = \infty$. \qed
\end{proof}

\begin{proposition}[增益例: 稀疏大跳]\label{prop:sparse}
	取 $\varepsilon_k = e^{k}$ 当 $k = 2^{2^j}$ ($j \geq 1$), 其余
	$\varepsilon_k = 0$. 则 $\sum_{k \leq m} \min(\varepsilon_k,1)
	= \#\{j: 2^{2^j} \leq m\} = o(\log m)$ (旧条件不适用), 但
	最大跳满足 $k_j \geq \sqrt m$, 故
	$S(m) \geq \log(1+e^{k_j}) \geq \sqrt m = \omega(\log m)$. 于是
	$\{q_n\}$ 完备 (定理 \ref{thm:Sthr}); 这是用 $S$ 取代
	$(\log 2)\sum\min(\varepsilon,1)$ 的实际增益: 稀疏的指数大跳
	即可令 $u_m$ 超多项式.
\end{proposition}

\begin{proof}
	跳点 $k_j = 2^{2^j}$ 满足: 对 $2^{2^J} \leq m < 2^{2^{J+1}}$,
	$k_J \geq m^{1/2}$ ($2^{2^{J+1}} = k_J^2 > m$), 且
	$\log(1+e^{k_J}) \geq k_J$. \qed
\end{proof}

\begin{remark}[判据 (7) 的边界与奇偶]
	判据 (7) 是两个级数同时发散 (偶矩与奇矩各给一个自由度
	$M_2, M_3$); 只发散其一仍可构造偶/奇反例. 门槛线上
	$\varepsilon_k \sim 1/(k\log k)$ 的对数幂因子 $(\log m)^C$
	不影响收敛临界 $\beta = 1/2$, 故门槛线分类与 $C$ 无关.
	一般 $H$ (非对角) 的必要方向需范数\emph{下界}
	$\|x^k\| \geq c k^\gamma$, 未纳入本节.
\end{remark}

"""

anchor = r"\subsection{Krein 族的稳健性}"
assert anchor in s, "anchor not found"
s = s.replace(anchor, newsec + anchor, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print("inserted new subsection, new length:", len(s))
