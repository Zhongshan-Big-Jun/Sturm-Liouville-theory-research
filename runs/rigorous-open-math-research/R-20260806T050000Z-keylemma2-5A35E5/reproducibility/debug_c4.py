# -*- coding: utf-8 -*-
"""debug_c4.py -- find the failing interval op in K_iv on the wide box."""
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility")
from decimal import Decimal
import riarith as R

v = R.Iv(Decimal('0.897597901025655210972033336078616704034170566267291310427109'),
         Decimal('1.25559265358979323846264338327950288419716939937510582097494'))
print('v =', v)
u = R.iv_tan(v); print('tan(v) =', u)
w = R.iv_sub(R.PI, R.iv_mul(R.Iv.pt(Decimal('2.5')), v)); print('w =', w)
tw = R.iv_tan(w); print('tan(w) =', tw)
