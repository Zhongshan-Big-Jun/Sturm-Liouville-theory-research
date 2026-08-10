# -*- coding: utf-8 -*-
"""Patch riarith.iv_atan: sound interval atan for intervals that may straddle 1
or contain 0.  Strategy: atan is strictly increasing on [0,inf), so
atan([lo,hi]) = [atan(lo), atan(hi)]; evaluate the two ENDPOINTS rigorously via
a point routine (series on [0,0.5], doubling reduction on (0.5,1], and
atan(x) = pi/2 - atan(1/x) on (1,inf)), then form the outward-rounded hull.
This replaces the previous version, which recursed indefinitely on intervals
straddling 1 and divided by zero at lo = 0.
"""
import re, pathlib
p = pathlib.Path(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\riarith.py")
src = p.read_text(encoding="utf-8")
new = '''def _atan_pt(x_iv):
    """rigorous atan of a POINT interval (x >= 0)."""
    if x_iv.lo != x_iv.hi:
        raise ValueError("_atan_pt requires a point interval")
    x = x_iv.lo
    if x < 0:
        raise ValueError("atan for x >= 0 only")
    if x > 1:
        inv = iv_inv(x_iv)
        return Iv(HALF_PI.lo - _atan_pt(inv).hi, HALF_PI.hi - _atan_pt(inv).lo)
    if x > Decimal('0.5'):
        # atan(x) = 2 atan(x/(1+sqrt(1+x^2))); argument <= ~0.4142
        one = Iv.pt(1)
        s = iv_sqrt(iv_add(one, iv_sqr(x_iv)))
        t = iv_div(x_iv, iv_add(one, s))
        inner = _atan_pt(t)
        return Iv(2*inner.lo, 2*inner.hi)
    return atan_taylor_series(x_iv, 80)

def iv_atan(x_iv):
    if x_iv.lo < 0:
        raise ValueError("atan for x >= 0 only")
    lo_r = _atan_pt(Iv.pt(x_iv.lo))
    hi_r = _atan_pt(Iv.pt(x_iv.hi))
    return Iv(lo_r.lo, hi_r.hi)
'''
start = src.index("def iv_atan(x_iv):")
end = src.index("def I(x):")
patched = src[:start] + new + src[end:]
p.write_text(patched, encoding="utf-8")
print("patched riarith.iv_atan")
