# -*- coding: utf-8 -*-
"""Patch 3: _atan_pt x>1 branch must enclose atan(1/x) for the tiny non-point
interval 1/x produced by directed rounding (use iv_atan, not _atan_pt)."""
import pathlib
p = pathlib.Path(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\riarith.py")
src = p.read_text(encoding="utf-8")
old = '''    if x > 1:
        inv = iv_inv(x_iv)
        return Iv(HALF_PI.lo - _atan_pt(inv).hi, HALF_PI.hi - _atan_pt(inv).lo)
'''
new = '''    if x > 1:
        inv = iv_inv(x_iv)   # tiny interval around 1/x in (0,1)
        return Iv(HALF_PI.lo - iv_atan(inv).hi, HALF_PI.hi - iv_atan(inv).lo)
'''
assert old in src
src = src.replace(old, new)
p.write_text(src, encoding="utf-8")
print("patched (3)")
