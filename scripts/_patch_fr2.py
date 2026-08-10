# -*- coding: utf-8 -*-
import io
p = r'F:\LaTeX\BVE research\docs\SL_fractional_left_definite.tex'
s = io.open(p, encoding='utf-8-sig').read()
old = r"""脚本 \path{scripts/op10_fractional_window.py} 另验证负阶界
$\|x^k\|_t \le c^{t/2}\|x^k\|_0$ ($t = -0.5, -0.25, -0.1$) 与
$\|x^k\|_s$ 的数值指数趋近 $s - 1/2$."""
new = r"""脚本 \path{scripts/op10_fractional_window.py} 另验证负阶界
$\|x^k\|_t \le c^{t/2}\|x^k\|_0$ 与 $\|x^k\|_s$ 的数值指数趋近 $s-1/2$."""
assert old in s
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8-sig', newline='\n').write(s)
print('ok')
