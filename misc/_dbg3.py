# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'misc')
from decimal import Decimal
from rigid_dec import I, I_sin, I_cos, _sc_series, _sin_cos_u, _fl, _ce
import mpmath as mp
mp.mp.dps = 100
a = Decimal('0.30935401521945877'); b = Decimal('0.3365654764842564')
X = I(a, b)
R = I_sin(X)
tv = mp.sin(mp.mpf('0.30935401521945877'))
print('R.lo   =', R.lo)
print('true   =', mp.nstr(tv, 80))
print('R.lo - true =', mp.mpf(str(R.lo)) - tv)
print('R.hi   =', R.hi)
# inspect sc/cc
c = (a+b)/2
w = max(c-a, b-c)
from rigid_dec import _ce as ce
w = ce(w)
sc, cc = _sc_series(c)
print('sc:', sc)
print('cc:', cc)
print('true sin(c):', mp.nstr(mp.sin(mp.mpf(str(c))), 80))
print('true cos(c):', mp.nstr(mp.cos(mp.mpf(str(c))), 80))
su, cu = _sin_cos_u(w)
print('sw (sin(w) enc):', su)
print('cw (cos(w) enc):', cu)
print('true sin(w):', mp.nstr(mp.sin(mp.mpf(str(w))), 80))
print('true cos(w):', mp.nstr(mp.cos(mp.mpf(str(w))), 80))
# the lower bound: sc.lo*cu.lo - cc.hi*su.hi
lb = sc.lo*cu.lo - cc.hi*su.hi
print('manual lb = sc.lo*cu.lo - cc.hi*su.hi =', lb)
print('R.lo == manual lb?', R.lo == lb)
# true value of sin(a) = sin(c-w)
tv2 = mp.sin(mp.mpf(str(c)) - mp.mpf(str(w)))
print('sin(c-w) =', mp.nstr(tv2, 80))
