# -*- coding: utf-8 -*-
import io
p = r'docs\SL_fixed_n_supremum.tex'
s = io.open(p, encoding='utf-8').read()
old1 = r"""\begin{equation}\label{eq:alt}
	\rho = [1, R, 1, R, \dots, 1] \quad (2n+1 \text{ 块}),
	\qquad w_1 = w_3 = \dots = \sqrt{R}\,t,\; w_2 = w_4 = \dots = t,
	\qquad t = \frac{1}{(n+1)\sqrt R + n}.
\end{equation}"""
new1 = r"""\begin{equation}\label{eq:alt}
	\rho = [1, R, 1, R, \dots, 1] \quad (2n+1 \text{ 块}), \qquad
	\frac{w_1}{w_2} = \sqrt R,
	\qquad t = \frac{1}{(n+1)\sqrt R + n},
\end{equation}
其中值为 $1$ 的块宽 $w_1 = w_3 = \cdots = \sqrt R\,t$, 值为 $R$ 的块宽
$w_2 = w_4 = \cdots = t$."""
assert old1 in s
s = s.replace(old1, new1, 1)

old2 = r"""\item \textbf{随机搜索}: 3/5/7/9/11 块各 300 个随机 Dirichlet 配置,
		最大 $\lambda_3/\lambda_2$ 分别为 $2.89/3.98/4.17/3.72/3.36$,
		均 $< c_2(4)$."""
new2 = r"""\item \textbf{随机搜索}: 3, 5, 7, 9, 11 块各 300 个随机 Dirichlet
		配置, 最大 $\lambda_3/\lambda_2$ 分别为 $2.89$, $3.98$, $4.17$,
		$3.72$, $3.36$, 均低于 $c_2(4)$."""
assert old2 in s
s = s.replace(old2, new2, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print("fixed overfull lines")
