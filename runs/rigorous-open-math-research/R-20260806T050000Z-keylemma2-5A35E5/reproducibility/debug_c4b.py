# -*- coding: utf-8 -*-
"""debug_c4b.py -- probe iv_sin/iv_cos on [0.0026, 0.8976]."""
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal
import riarith as R

w = R.Iv(Decimal('0.00261101961531014230603492508074567370424590084991892411169'),
         Decimal('0.89759790102565521103256004308296112411174298830434258428100'))
print('sin(w) =', R.iv_sin(w))
print('cos(w) =', R.iv_cos(w))
print('_sin_taylor(w) =', R._sin_taylor(w))
print('_cos_taylor(w) =', R._cos_taylor(w))
print('reduce:', R.sin_cos_reduce(w))
# what does the code do for kk=0 (k=0 -> _sin_taylor/_cos_taylor)?
s = R.iv_sin(w); c = R.iv_cos(w)
print('tan via s/c =', R.iv_div(s, c))
