# -*- coding: utf-8 -*-
"""profile_bracket.py -- time the pieces."""
import sys, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal, localcontext
import riarith as R

t0 = time.time()
with localcontext() as c:
    c.prec = 60
    for i in range(100):
        x = R.Iv.pt(Decimal('0.4') + Decimal(i)/10000)
        y = R.iv_atan(x)
print('100 iv_atan point evals:', time.time()-t0)

t0 = time.time()
with localcontext() as c:
    c.prec = 60
    for i in range(100):
        x = R.Iv.pt(Decimal('0.4') + Decimal(i)/10000)
        y = R.iv_tan(x)
print('100 iv_tan point evals:', time.time()-t0)

t0 = time.time()
import sound_bracket as SB
with localcontext() as c:
    c.prec = 60
    a = SB.bracket_x1(Decimal('0.5'), Decimal('1.05'), Decimal('1e-20'))
print('one bracket_x1:', time.time()-t0, a)
