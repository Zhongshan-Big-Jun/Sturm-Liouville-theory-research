# -*- coding: utf-8 -*-
import io
p = r'docs\SL_third_order_recurrence_theory.tex'
s = io.open(p, encoding='utf-8').read()

newsec = r"""
\section{一般系数族的积分解分类与最小解的精细结构 (2026-08-05 补充)}

本补充把第 3 节的分类定理 \ref{thm:beta} 从两参数族
$E_j = \prod_{k=1}^j (1+\beta/(2k))$ 推广到一般有理比值族, 并给出
最小解的渐近展开、常数 $K(c)$ 的数值表, 以及盒式归纳齐次部分的封闭.
全部断言经精确有理数或高精度浮点验证 (脚本 \path{scripts/op13_*.py}).

\subsection{有理比值积分解的完整分类}

记 $e_j = E_j/E_{j-1}$. 若 $E$ 解 (2) 且 $e_j \to 1$ (根-1 支), 称
$E$ 为根-1 解. 显式解 $E^\pm$ (定理 \ref{thm:closed}) 生成二维解子空间.

\begin{theorem}[渐近分类]\label{thm:asym}
	设 $e_j \to 1$ 满足比值固定点恒等式 (引理 \ref{lem:fp}), 且
	$u := \lim_j j(e_j - 1)$ 存在. 则偶次 $u \in \{-\tfrac12, \tfrac12\}$,
	奇次 $u \in \{\tfrac12, \tfrac32\}$.
\end{theorem}

\begin{proof}
	对 $e_j = 1 + u/j + v/j^2 + w/j^3 + \cdots$ 作 $t$-尺度
	($j = 1/t$) 代入恒等式展开: 首非零约束为 $t^2$ 项
	(偶次 $-(2u-1)(2u+1)/4$, 奇次 $-(2u-3)(2u-1)/4$), 解得上述 $u$;
	符号推导见 \path{scripts/op13_asymptotic_classify.py}. \qed
\end{proof}

\begin{theorem}[刚性支]\label{thm:rigid}
	偶次 $u = -1/2$ 或奇次 $u = 1/2$ 时, 恒等式逐阶强制
	$v = w = \cdots = 0$: $t^{k+2}$ 项系数恰为 $(k+1)x_{k+1}$
	($x_{k+1}$ 为 $j^{-(k+1)}$ 的系数), 对 $k = 1, \dots, 5$ 符号验证
	(\path{scripts/op13_rigidity_check.py}). 因此若 $e_j$ 是有理函数,
	则 $e_j - e^-_j$ ($e^-_j = 1 - 1/(2j)$ 偶, $1 + 1/(2j)$ 奇)
	是有理函数且其 $\infty$ 处渐近展开全零, 故恒等为零:
	刚性支只有 $E^-$.
\end{theorem}

\begin{theorem}[自由支: 4-参数归约]\label{thm:free}
	在 4-参数有理族 $e_j = (j^2 + aj + b)/(j^2 + cc\,j + d)$
	(规范化 $a = u + cc$) 中, 固定点恒等式的解恰为:
	\begin{itemize}
		\item 偶次 $u = 1/2$: $d = 0$, 两支 —— $b = -(\tau+1)/2$,
			$cc = \tau$ (即 $E^{(\tau)}$, 比值 $(1-\frac{1}{2j})
			\frac{j+\tau+1}{j+\tau}$) 与 $b = (|2\tau+1|-1)/4$,
			$cc = \tau$ (表示 $E^+$ 的可约形式, 与 $\tau$ 无关);
		\item 奇次 $u = 3/2$: $d = 0$, $b = (\tau+1)/2$, $cc = \tau$
			(即 $E^{(\tau)}$, 比值 $(1+\frac{1}{2j})
			\frac{j+\tau+1}{j+\tau}$); $E^+$ 同理可约;
		\item 刚性支 ($u = -1/2$ 偶, $u = 1/2$ 奇): 仅 $E^-$
			($b = -cc/2$, $d = 0$, 比值与 $cc$ 无关).
	\end{itemize}
	符号求解 \path{scripts/op13_4param_reduced.py}; 精确逐项验证
	\path{scripts/op13_families_exact.py} 与
	\path{scripts/op13_classification_verify2.py} (偶/奇 $\times$
	$c \in \{1,3,10\}$ $\times$ $\tau \in \{0, 2, \tfrac52, -\tfrac12, -\tfrac32\}$
	全部通过). 注意: \path{op13_4param_reduced.py} 对奇次 $u = 1/2$ 返回的
	``负支''是 sympy 增根, 精确复算 (39/40 项失败) 排除;
	奇次 $u = 3/2$ 的符号求解返回空集是 sympy 局限, 直接代入精确验证通过.
\end{theorem}

\begin{theorem}[完整分类]\label{thm:full}
	偶次根-1 支的一切\emph{有理比值}积分解恰为
	$E^{(\tau)}_j = \frac{\tau+1+j}{\tau+1}\,E^-_j$
	($\tau \neq -1$), 即 $E^{(\tau)} = c_1 E^+ + c_2 E^-$ 且
	$c_1 = \frac{1}{2(\tau+1)}$, $c_2 = \frac{2\tau+1}{2(\tau+1)}$
	(偶次), $c_1 = \frac{3}{2(\tau+1)}$, $c_2 = \frac{2\tau-1}{2(\tau+1)}$
	(奇次); 加上刚性支 $E^-$. 比值显式
	$e^{(\tau)}_j = (1 - \tfrac{1}{2j})\frac{j+\tau+1}{j+\tau}$ (偶),
	$(1 + \tfrac{1}{2j})\frac{j+\tau+1}{j+\tau}$ (奇);
	偏差 $d^{(\tau)}_j := e^{(\tau)}_j - e^+_j = -\frac{\tau+1/2}{j(j+\tau)}$
	(偶), $\frac{1-2\tau}{2j(j+\tau)}$ (奇).
\end{theorem}

\begin{proof}[证明结构]
	三支柱: (i) 定理 \ref{thm:asym} 限定 $u$; (ii) 定理 \ref{thm:rigid}
	闭合刚性支; (iii) 自由支的 4-参数归约 (定理 \ref{thm:free})
	给出 $E^{(\tau)}$ 族. 高次有理函数 ($\deg > 2$) 的排除: 对自由支,
	任何 $e_j = 1 + \frac12/j + v/j^2 + \cdots$ 的有理解必须满足同一组
	无限阶约束; 4-参数族是次数 $\leq 2$ 的完全列举. 次数 $> 2$ 的
	穷尽排除未完成 (见第 6.4 节审计). \qed
\end{proof}

\subsection{最小解排除与第 6.4 节审计}

根-0 (最小) 支的比值 $\rho^*_j = z^*_j/z^*_{j-1} \to 0$ 不属于
$e_j \to 1$ 类, 不可能是有理比值: 对 $c = 1$, 高精度向后迭代计算
$\rho^*_j$ ($j \leq 300$, 120 位), 对次数 $d = 1, \dots, 4$ 拟合
$P(j)/Q(j)$ ($\deg Q - \deg P = 2$) 残差均为 $O(10^5)$
(真有理序列残差应为机器精度), 见 \path{scripts/op13_min_rational_test.py}.
更强结构: 根-0 支的渐近展开逐阶唯一 (下一小节), 无自由参数可与
有理函数匹配. 此排除是数值级 + 唯一性论证, 未上升为完整定理,
如实标注.

\subsection{最小解的渐近展开与常数 $K(c)$}\label{sec:K}

定理 \ref{thm:minimal} 的 $h^*_j \sim K(c/4)^j j^{-3}/(j!)^2$ 中,
比值 $\rho^*_j = h^*_j/h^*_{j-1}$ 的逐阶匹配展开 (符号, 严格到任意阶
的形式推导, \path{scripts/op13_matched_asymp3.py}):

\begin{equation}\label{eq:rhos}
	\rho^*_j = \frac{c}{4j^2}\Bigl(1 - \frac{3}{j} + \frac{C}{j^2}
	+ \frac{D}{j^3} + \frac{E}{j^4} + \frac{F}{j^5}
	+ \frac{G}{j^6} + O(j^{-7})\Bigr),
\end{equation}
偶次: $C = 6$, $D = -(c + \frac{21}{2})$, $E = \frac{33c}{4} + \frac{69}{4}$,
$F = -(\frac{c^2}{4} + \frac{163c}{4} + \frac{219}{8})$,
$G = \frac{85c^2}{16} + \frac{2529c}{16} + \frac{681}{16}$;
奇次: $C = 8$, $D = -(c + \frac{41}{2})$, $E = \frac{39c}{4} + \frac{207}{4}$,
$F = -(\frac{c^2}{4} + \frac{241c}{4} + \frac{1039}{8})$,
$G = \frac{95c^2}{16} + \frac{4843c}{16} + \frac{5203}{16}$.
注意 $B = -3$ 是首阶强制值 (与根-1 支无关), 各系数为 $c$ 的递增次多项式.

常数 $K(c)$ ($c > 0$) 由
$K(c) = \lim_j h^*_j (j!)^2 (4/c)^j j^3$ 数值提取 (\path{scripts/op13_K1_definitive.py},
\path{scripts/op13_K_grid.py}); 结果:

\begin{center}\begin{tabular}{l|rrrrrrrr}
	$c$ & 0.01 & 0.1 & 0.5 & 1 & 2 & 5 & 10 & 100 \\\hline
	$K(c)$ & 0.74925 & 0.74255 & 0.71367 & 0.67957 & 0.61737 & 0.46932
		& 0.30846 & 0.00252
\end{tabular}\end{center}

锚点: $K(0) = \tfrac34$ (拟合至 11 位, \path{op13_K_smallc.py}),
$K(1) = e/4 = 0.6795704571147613088400719$ (\emph{25 位数值确认},
$K(1) - e/4 = -7.1 \times 10^{-25}$, \path{op13_K1_definitive.py}).
小 $c$ 展开: $\ln K(c) = \ln\tfrac34 - \tfrac{c}{10}
+ 0.0014286\,c^2 - 0.0000422\,c^3 + O(c^4)$
(数值拟合, \path{op13_K_cubic.py}). 一般 $c$ 的闭式\emph{未识别};
生成函数满足五阶线性 ODE (\path{op13_gf_ode5.py}), 未进一步求解.
严格性: (eq:rhos) 为形式级数 (逐阶匹配), $K(1) = e/4$ 为强数值证据,
\emph{均非完整证明}.

\subsection{盒式归纳齐次部分的封闭}\label{sec:box}

会话 10 路线 A 的缺口: 比值偏差 $d_j = \rho_j - e^+_j$ 的归纳需要排除
退化配置 ``$d_{j-1} = 0$ 且 $d_{j-2} > 0$''. 由定理 \ref{thm:full},
一切齐次根-1 轨迹的偏差精确等于 $d^{(\tau)}_j$ (偶)
$= -\frac{\tau+1/2}{j(j+\tau)}$, 且对固定 $j$ 是 $\tau$ 的严格减函数
($\partial_\tau d^{(\tau)}_j = -\frac{j-1/2}{j(j+\tau)^2} < 0$),
$E^{(\infty)} = E^+$ 对应 $d \equiv 0$ ($\tau = -\tfrac12$ 偶,
$\tfrac12$ 奇). 故 $d_{j-1} = 0$ 唯一决定 $\tau$, 迫使
$d_{j-2} = 0$: 退化配置被\emph{精确排除}. 双侧盒
$d_j \in [\tfrac12 j^{-2},\; \alpha j^{-1}]$,
$\alpha = 2 + \tfrac{5c}{12}$ (偶), $4 + \tfrac{7c}{20}$ (奇),
对 3000 个随机盒内配置在 $j = 30..300$ 完全前向不变 (零违例,
\path{op13_box2side2.py}, $c \in \{1,3,10\}$).
\emph{残余缺口}: 非齐次源项 (最小解分量的 $T_j D$ 项) 的 $D$-控制
未在本补充中闭合; 齐次部分已封闭.

"""

anchor = r"\section{数值验证}"
assert anchor in s
s = s.replace(anchor, newsec + anchor, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print("inserted; new len:", len(s))
