# -*- coding: utf-8 -*-
"""test_riarith.py -- fixed comparisons."""
import sys
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import riarith as R
import mpmath as mp
from decimal import Decimal
mp.mp.dps = 60

def d_of_mp(x):
    return Decimal(str(x))

print('pi interval width:', float(R.PI.hi - R.PI.lo))
pi60 = d_of_mp(mp.pi)
print('pi enclosure ok:', R.PI.lo <= pi60 <= R.PI.hi, ' [%s, %s]' % (R.PI.lo, R.PI.hi))

def check(name, iv, true, tol=1e-38):
    lo, hi = iv.lo, iv.hi
    t = d_of_mp(true)
    ok = lo <= t <= hi and (hi - lo) < Decimal(tol)
    print('[%s] %s' % ('PASS' if ok else 'FAIL', name))

for x in ['0.1', '1.0', '1.5', '2.6', '3.0', '3.14']:
    xi = R.Iv.pt(Decimal(x))
    check('sin(%s)' % x, R.iv_sin(xi), mp.sin(mp.mpf(x)))
    check('cos(%s)' % x, R.iv_cos(xi), mp.cos(mp.mpf(x)))
for x in ['0.3', '1.0', '1.4']:
    xi = R.Iv.pt(Decimal(x))
    check('tan(%s)' % x, R.iv_tan(xi), mp.tan(mp.mpf(x)), 1e-36)
for x in ['0.3', '1.0', '2.0', '10.0', '100.0']:
    xi = R.Iv.pt(Decimal(x))
    check('atan(%s)' % x, R.iv_atan(xi), mp.atan(mp.mpf(x)))
iv = R.Iv(Decimal('1.0'), Decimal('1.1'))
res = R.iv_sin(iv)
print('sin([1,1.1]) =', res, 'width', float(res.wid()))
print('encloses sin(1.05):', res.lo <= d_of_mp(mp.sin(mp.mpf('1.05'))) <= res.hi)
# a couple of interval arithmetic identities vs mpmath
q = R.Iv(Decimal('1.5'), Decimal('2.0'))
a = R.Iv(Decimal('0.8'), Decimal('0.9'))
prod = R.iv_mul(q, a)
print('q*a encloses:', prod.lo <= d_of_mp(mp.mpf('1.5')*mp.mpf('0.8')) and d_of_mp(mp.mpf('2.0')*mp.mpf('0.9')) <= prod.hi)
