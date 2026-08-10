# -*- coding: utf-8 -*-
"""Patch 2: _atan_pt doubling step returns a small interval; route it back
through the endpoint evaluator (atan increasing => endpoint enclosure is sound)."""
import pathlib
p = pathlib.Path(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility\riarith.py")
src = p.read_text(encoding="utf-8")
old = '''    if x > Decimal('0.5'):
        # atan(x) = 2 atan(x/(1+sqrt(1+x^2))); argument <= ~0.4142
        one = Iv.pt(1)
        s = iv_sqrt(iv_add(one, iv_sqr(x_iv)))
        t = iv_div(x_iv, iv_add(one, s))
        inner = _atan_pt(t)
        return Iv(2*inner.lo, 2*inner.hi)
    return atan_taylor_series(x_iv, 80)
'''
new = '''    if x > Decimal('0.5'):
        # atan(x) = 2 atan(x/(1+sqrt(1+x^2))); argument <= ~0.4142.
        # The interval-arithmetic step returns a tiny interval t; atan is
        # increasing, so enclose atan(t) by the two endpoint evaluations.
        one = Iv.pt(1)
        s = iv_sqrt(iv_add(one, iv_sqr(x_iv)))
        t = iv_div(x_iv, iv_add(one, s))
        inner = iv_atan(t)
        return Iv(2*inner.lo, 2*inner.hi)
    return atan_taylor_series(x_iv, 80)
'''
assert old in src
src = src.replace(old, new)
p.write_text(src, encoding="utf-8")
print("patched (2)")
