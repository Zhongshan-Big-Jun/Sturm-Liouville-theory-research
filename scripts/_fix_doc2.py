# -*- coding: utf-8 -*-
import io
p = r'docs\SL_fixed_n_supremum.tex'
s = io.open(p, encoding='utf-8').read()
old = r"""		n = 3, 4: &\quad y_n = \arccos C_n,\; Q_n(C_n) = 0,\;
			Q_3, Q_4 \text{ 见 } \path{scripts/op02_poly_extract.py}.
"""
new = r"""		n = 3, 4: &\quad y_n = \arccos C_n \text{ 且 } Q_n(C_n) = 0,
			\text{ 其中 } Q_3, Q_4 \text{ 为 } F_n \text{ 的显式多项式}.
"""
assert old in s
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print("fixed math-mode path")
