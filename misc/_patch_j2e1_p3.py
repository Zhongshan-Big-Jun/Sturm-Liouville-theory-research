# -*- coding: utf-8 -*-
# Part 3: R12 appendix insertion + R13 artifacts update
PATH = 'docs/SL_gap_n1_O3a_phase_rigidity_proof.tex'
s = open(PATH, encoding='utf-8').read()
frag = open('misc/e1_cert_tables.tex', encoding='utf-8').read()

appendix = r"""
\section{有理包络证书总表}\label{app:cert}

本节实现第 \ref{ss:j2e1} 子节注 \ref{rem:env} 所声明的全部证书。先给出两个
基础引理。

\begin{lemma}[交错级数包络]\label{lem:envseries}
对 $0<x<3/2$,
\begin{equation}
	\sin x=\sum_{k=0}^{\infty}\frac{(-1)^k x^{2k+1}}{(2k+1)!},\qquad
	\cos x=\sum_{k=0}^{\infty}\frac{(-1)^k x^{2k}}{(2k)!}.
\end{equation}
相邻项绝对值之比 $x^2/((2k+2)(2k+3))\le2.25/6<1$ 递减, 故部分和交替夹逼: 对
$m\ge0$,
\begin{equation}
	S_{2m+1}\ge\sin x\ge S_{2m},\qquad
	C_{2m}\ge\cos x\ge C_{2m+1},\qquad
	\text{余项绝对值}\le\frac{x^{2m+3}}{(2m+3)!}.
\end{equation}
对 $0<x\le1$, $\arctan x=\sum_{k=0}^{\infty}(-1)^k x^{2k+1}/(2k+1)$ 同理 (部分和
交替夹逼, 余项 $\le x^{2m+3}/(2m+3)$)。$\pi$ 由 Machin 公式
$\pi=16\arctan(1/5)-4\arctan(1/239)$ 的两个反正切项包络组合得到有理界。本文对
$\sin,\cos$ 取 12 项, 对 $\arctan$ 取 22 项, 在 $x\le3/2$ 时余项 $<10^{-12}$;
因此表 \ref{tab:envprims} 中每个原语包络的宽度 $\le10^{-12}$。
\end{lemma}

\begin{lemma}[泰勒模型判据]\label{lem:envtaylor}
设 $f$ 在 $[a,b]$ 上二阶连续可导, $c:=(a+b)/2$, $w:=(b-a)/2$。若 $f'(c)\in J$
(有理区间 $J=[j_-,j_+]$) 且 $\sup_{[a,b]}|f''|\le M$, 则对 $\gamma\in[a,b]$,
\begin{equation}
	f'(\gamma)\in[j_- - Mw,\; j_+ + Mw].
\end{equation}
特别地, $j_- - Mw>0$ 蕴含 $f'>0$ 于 $[a,b]$, $j_+ + Mw<0$ 蕴含 $f'<0$ 于
$[a,b]$。同理, 若 $f(c)\in J_0$ 且 $\sup_{[a,b]}|f'|\le M_0$, 则
\begin{equation}
	f(\gamma)\in J_0+[-M_0w,M_0w]\quad(\gamma\in[a,b]).
\end{equation}
\end{lemma}

\begin{proof}
$f'(\gamma)=f'(c)+f''(\xi)(\gamma-c)$ 且 $|\gamma-c|\le w$; 值版本用一阶 Taylor
余项 $f(\gamma)=f(c)+f'(\xi)(\gamma-c)$。
\end{proof}

注 \ref{rem:env}(b) 给出原语在小区间上的值域: $\sin\gamma$ 增, $\cos\gamma$ 减,
$A=\pi-\gamma$ 减, $D=\sqrt{1+3\sin^2\gamma}$ 增, $\tau=\arctan(2\tan\gamma)$ 增
($\tau'=2/D^2>0$); 故小区间端点处的点值包络直接给出小区间上的原语包络。导数
表达式由链式法则得到 ($\mathrm{d}A/\mathrm{d}\gamma=-1$,
$\mathrm{d}\sin\gamma/\mathrm{d}\gamma=\cos\gamma$,
$\mathrm{d}\cos\gamma/\mathrm{d}\gamma=-\sin\gamma$,
$\mathrm{d}D/\mathrm{d}\gamma=3\sin\gamma\cos\gamma/D$,
$\mathrm{d}\tau/\mathrm{d}\gamma=2/D^2$), 因此 $f'$ 与 $f''$ 在小区间上的包络
由同一原语包络经注 \ref{rem:env}(c) 的精确有理区间算术计算。以下四张表即由此
逐项生成; 每个区间都是一条有限精确有理数不等式链。生成脚本
misc/e1\_certgen.py 与认证台账 misc/e1\_cert\_ledger.json (内容哈希 L10--L12,
第 \ref{sec:certs} 节) 可复现全部数据, 但表中数据本身才是结论。

""" + frag + """

"""

old = '\\appendix\n\n\\section{符号速查}'
new = '\\appendix\n\n' + appendix + '\\section{符号速查}'
assert old in s, 'appendix anchor missing'
s = s.replace(old, new, 1)
print('ok: R12 appendix')

# ---- R13 artifacts ----
old = """定理 \\ref{thm:j2e1} 的 E1 验证产物:
\\begin{itemize}
\t\\item 严格区间引擎: \\texttt{misc/rigid\\_dec.py} (十进制定向舍入, 内容哈希 L7);
\t\\item E1 认证脚本与台账: \\texttt{misc/zz\\_verify\\_e1\\_dec.py},
\t\\texttt{misc/e1\\_facts\\_ledger.json} (内容哈希 L8, L9);
\t\\item 代数分解精确验证: \\texttt{misc/\\_verify\\_identity.py},
\t\\texttt{misc/zz\\_rebuild\\_check1.py}, 分子数据文件 \\texttt{misc/t3\\_NJ2.json};
\t\\item 引擎包含性自检: \\texttt{misc/\\_test\\_dec.py} (4800 次随机检查, 零违反)。
\\end{itemize}"""
new = """定理 \\ref{thm:j2e1} 的 E1 验证产物:
\\begin{itemize}
\t\\item 有理包络证书链: \\texttt{misc/e1\\_certgen.py} (生成器),
\t\\texttt{misc/e1\\_cert\\_ledger.json} (认证台账), \\texttt{misc/e1\\_cert\\_tables.py}
\t(证书表生成器); 内容哈希 L10--L12, 证书总表见附录 \\ref{app:cert};
\t\\item 精确有理区间内核: \\texttt{misc/rigid1d.py} (交错级数包络 + Machin $\\pi$;
\t2026-08-09 修复 \\texttt{I.sqrt} 的 $+1$ 单位错误);
\t\\item 代数分解精确验证: \\texttt{misc/\\_verify\\_identity.py},
\t\\texttt{misc/zz\\_rebuild\\_check1.py}, 分子数据文件 \\texttt{misc/t3\\_NJ2.json};
\t\\item 旧十进制区间验证器三件套 (\\texttt{misc/rigid\\_dec.py},
\t\\texttt{misc/zz\\_verify\\_e1\\_dec.py}, \\texttt{misc/e1\\_facts\\_ledger.json})
\t已退役, 仅作历史复现 (内容哈希 L7--L9)。
\\end{itemize}"""
assert old in s, 'artifacts anchor missing'
s = s.replace(old, new, 1)
print('ok: R13 artifacts')

open(PATH, 'w', encoding='utf-8').write(s)
print('part 3 written')
