# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_inf_ratio_proof.tex'
s = io.open(p, encoding='utf-8-sig').read()
old = r"""	对 $y$ 满足 (1) 且 $y(0) = 0$, 定义
	\[
		\tan \theta(x) = \frac{y'(x)}{\sqrt{\lambda}\, y(x)},
		\qquad \theta(0) = \frac{\pi}{2}.
	\]
	用引理 \ref{lem:prufer} 的 Prufer 相角: 定义
"""
new = r"""	用引理 \ref{lem:prufer} 的 Prufer 相角 (对 $y(0)=0$ 的解 $y$): 定义
"""
assert old in s
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('ok')
