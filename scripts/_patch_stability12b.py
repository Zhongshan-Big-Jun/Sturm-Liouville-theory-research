# -*- coding: utf-8 -*-
import io
p = r'docs\SL_stability_moment_jump.tex'
s = io.open(p, encoding='utf-8').read()

# abstract: add item 5
old = r"""	\item \emph{Krein 族的稳健性 (定理 \ref{thm:margin})}: Krein 族
		$\varepsilon_m \sim (4/c)m$, 余量极大; 常数 $c$ 的扰动
		($c \to c+\delta$, $\delta > -c$) 与基系数有界扰动均保持完备性.
\end{enumerate}"""
new = r"""	\item \emph{Krein 族的稳健性 (定理 \ref{thm:margin})}: Krein 族
		$\varepsilon_m \sim (4/c)m$, 余量极大; 常数 $c$ 的扰动
		($c \to c+\delta$, $\delta > -c$) 与基系数有界扰动均保持完备性.
	\item \emph{精确二分与门槛线分类 (定理 \ref{thm:Sthr}--\ref{thm:model})}:
		门槛量是 $S(m) = \sum \log(1+\varepsilon_k)$: $S = \omega(\log m)$
		充分; 对角空间 $H_\beta$ 中完备性判据是精确的
		(级数 (7) 发散); 门槛线 $\varepsilon_k \sim 1/(k\log k)$ 被完全分类
		(完备 $\iff \beta \leq 1/2$); 稀疏指数大跳显示 $S$ 优于
		$\sum\min(\varepsilon,1)$.
\end{enumerate}"""
assert old in s, "abstract item not found"
s = s.replace(old, new, 1)

# open problems section: S1 resolved, S2 addressed
old2 = r"""	\item[开放问题] (S1) 门槛线上系数族 ($\sum \min(\varepsilon_k,1) \sim \log m$)
		的完整分类; (S2) 一般 $H$ 中``可表示性''门槛 (对角空间给出
		$u_m$ 与 $m^{\beta-1/2}$ 的比较, 一般 $H$ 无闭式);
		(S3) 变系数算子 $K = -D^2 + c(x)$ 的跳变结构破坏后, 是否有高阶
		矩跳跃替代机制."""
new2 = r"""	\item[已解决 (本版)] (S1) 门槛线分类已闭合: 精确判据 (7) 给出
		对角空间中 $u_m$ 增长与 $\beta$ 的精确比较 (定理 \ref{thm:exact}),
		门槛线 $\varepsilon_k \sim 1/(k\log k)$ 完全分类
		(定理 \ref{thm:line}); (S2) 的一般方向在对角空间完全解决,
		一般 $H$ 的必要方向需要范数下界.
	\item[开放问题] (S2) 一般 $H$ 中``可表示性''门槛的必要方向
		(需 $\|x^k\| \geq c k^\gamma$ 型下界, 无闭式);
		(S3) 变系数算子 $K = -D^2 + c(x)$ 的跳变结构破坏后, 是否有高阶
		矩跳跃替代机制."""
assert old2 in s, "open problems section not found"
s = s.replace(old2, new2, 1)

# numerical verification section: add the new checks
old3 = r"""	\item \textbf{临界窗口}: $\varepsilon_k = 1/\log k$ 时
		$\log u_m - 8\log m$ 在 $m = 200, 800, 1999$ 处为
		$1.5, 81.2, 229.7$ (超多项式, 条件 $\omega(\log m)$ 恰好成立).
\end{enumerate}"""
new3 = r"""	\item \textbf{临界窗口}: $\varepsilon_k = 1/\log k$ 时
		$\log u_m - 8\log m$ 在 $m = 200, 800, 1999$ 处为
		$1.5, 81.2, 229.7$ (超多项式, 条件 $\omega(\log m)$ 恰好成立).
	\item \textbf{精确二分 (本版)}: (i) $\varepsilon_k = k^{-1/2}$:
		$\log u_{4000}/\log 4000 = 14.53$ (超多项式, $S \sim 2\sqrt m$);
		(ii) $\varepsilon_k = 1/(k\log k)$: $u_{200000} = 15.88 \approx \log m$,
		部分和 (7) 在 $\beta = 0.5$ 缓慢发散 ($\sim (\log m)^3$),
		在 $\beta = 0.6$ 收敛 ($N=10^5$ 时 75.06) —— 临界 $\beta = 1/2$
		精确; (iii) 稀疏指数大跳 $\varepsilon_{2^{2^j}} = e^{2^{2^j}}$:
		$\sum\min = 5 = o(\log 4000)$ 但 $\log u_{4000} = 1364$ (超多项式);
		(iv) $\varepsilon_k = 2/k$: $u_m/m^2 \to 1/6 = 1/\Gamma(4)$, 部分和 (7)
		在 $\beta = 2.4$ 发散 ($\sim m^{0.2}$), 在 $\beta = 2.6$ 收敛,
		临界 $\beta = 2.5$ 处对数发散 —— 与 $C+1/2 = 2.5$ 一致.
		脚本 \path{scripts/op12_dichotomy_verify.py},
		\path{scripts/op12_threshold_verify.py}, \path{scripts/op12_sparse_check.py}.
\end{enumerate}"""
assert old3 in s, "num verify section not found"
s = s.replace(old3, new3, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print("patched abstract + open problems + verification")
