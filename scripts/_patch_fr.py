# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_fractional_left_definite.tex'
s = io.open(p, encoding='utf-8-sig').read()
old = r"""	\item[左定理论] 正算子 $A \ge \gamma I$ 的分数幂定义 Hilbert 标度
		$\{D(A^{s/2})\}$; 内积 $(f,g)_s = (A^{s/2}f, A^{s/2}g)$ \cite{lw1,fg}."""
new = r"""	\item[左定理论] 正算子 $A \ge \gamma I$ 的分数幂给出 Hilbert 标度
		$H^s = D(A^{s/2})$, 内积 $(f,g)_s = (A^{s/2}f, A^{s/2}g)$ \cite{lw1,fg}."""
assert old in s
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('ok')
