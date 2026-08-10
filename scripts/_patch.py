# -*- coding: utf-8 -*-
import io
p = r"F:\LaTeX\BVE research\scripts\audit_o3a_pdf_part1.py"
s = io.open(p, encoding="utf-8").read()
old = """for w in [0.05, 0.5, 1.0, 2.0, 3.0, 5.0]:
    h = 4*w*(mp.pi - mp.atan(w)) - 5 - 9*w*w
    M2_1 = M2_expr(mp.mpf('1'), mp.mpf(w))"""
new = """for wv in [0.05, 0.5, 1.0, 2.0, 3.0, 5.0]:
    w = mp.mpf(wv)
    h = 4*w*(mp.pi - mp.atan(w)) - 5 - 9*w*w
    M2_1 = M2_expr(mp.mpf('1'), w)"""
assert old in s
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")
