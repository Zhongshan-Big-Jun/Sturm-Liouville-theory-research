# -*- coding: utf-8 -*-
"""debug_riarith.py"""
import sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import riarith as R
from decimal import Decimal
import mpmath as mp
mp.mp.dps = 40

print('sin(0.1):', R.iv_sin(R.Iv.pt(Decimal('0.1'))))
print('true:', mp.sin(mp.mpf('0.1')))
print('_sin_taylor(0.1):', R._sin_taylor(R.Iv.pt(Decimal('0.1'))))
print('_cos_taylor(0.1):', R._cos_taylor(R.Iv.pt(Decimal('0.1'))))
print('true cos(0.1):', mp.cos(mp.mpf('0.1')))
print()
print('reduction of 1.05:', R.sin_cos_reduce(R.Iv.pt(Decimal('1.05'))))
print('sin(1.05):', R.iv_sin(R.Iv.pt(Decimal('1.05'))))
print('true:', mp.sin(mp.mpf('1.05')))
print()
# check _sin_taylor for point intervals with negative r
print('_sin_taylor(-0.5208):', R._sin_taylor(R.Iv.pt(Decimal('-0.5208'))))
print('true sin(-0.5208):', mp.sin(mp.mpf('-0.5208')))
print('_cos_taylor(-0.5208):', R._cos_taylor(R.Iv.pt(Decimal('-0.5208'))))
print('true cos(-0.5208):', mp.cos(mp.mpf('-0.5208')))
