# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'misc')
from decimal import Decimal
from rigid_dec import I, I_sin, I_cos, _sc_series, _sin_cos_u, PI
import mpmath as mp
mp.mp.dps = 80
x = I(Decimal('0.30935401521945877'), Decimal('0.3365654764842564'))
R = I_sin(x)
print('sin interval:', R)
tv = mp.sin(mp.mpf('0.30935401521945877'))
print('true sin(a):', tv)
print('contains?', mp.mpf(str(R.lo)) <= tv <= mp.mpf(str(R.hi)))
# inspect pieces
c = (x.lo + x.hi)/2
print('c =', c)
sc, cc = _sc_series(c)
print('sc =', sc)
print('cc =', cc)
print('true sin(c) =', mp.sin(mp.mpf(str(c))))
print('true cos(c) =', mp.cos(mp.mpf(str(c))))
w = max(c - x.lo, x.hi - c)
from rigid_dec import _ce
w = _ce(w)
su, cu = _sin_cos_u(w)
print('su =', su)
print('cu =', cu)
print('true sin(w) =', mp.sin(mp.mpf(str(w))))
print('true cos(w) =', mp.cos(mp.mpf(str(w))))
