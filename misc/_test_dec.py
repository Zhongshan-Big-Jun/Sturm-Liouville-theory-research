# -*- coding: utf-8 -*-
"""Re-test rigid_dec: containment with Decimal (not float) comparisons + der_sign speed."""
import sys, time, random
sys.path.insert(0, 'misc')
from decimal import Decimal, localcontext, ROUND_CEILING
from rigid_dec import I, PI, I_sin, I_cos, I_atan2, D1, d1_sin, d1_cos, d1_atan, der_sign, range_pos
import mpmath as mp
mp.mp.dps = 80
random.seed(3)
bad = 0; total = 0
for _ in range(400):
    a = random.random()*1.3
    b = a + random.random()*0.05
    X = I(Decimal(str(a)), Decimal(str(b)))
    for name, R, tf in [('sin', I_sin(X), mp.sin), ('cos', I_cos(X), mp.cos), ('atan', I_atan2(X), mp.atan)]:
        for pt in (a, (a+b)/2, b, a+0.37*(b-a)):
            tv = tf(mp.mpf(str(pt)))
            total += 1
            if not (mp.mpf(str(R.lo)) <= tv <= mp.mpf(str(R.hi))):
                bad += 1
                print('VIOLATION', name, a, b, pt, 'R=', R)
print('containment: total %d, violations %d' % (total, bad))

def comps2(g):
    A = PI - g
    sg = d1_sin(g); cg = d1_cos(g)
    D2v = I(1) + 3*sg.v*sg.v
    B2 = 4*A*A*cg.v*cg.v - A*A - 12*A*cg.v*sg.v + 6*sg.v*sg.v
    M  = 2*A*A*cg.v*cg.v - A*A - 8*A*cg.v*sg.v + 6*sg.v*sg.v
    TA_B2 = 4*(-B2)*A*A*sg.v*sg.v*cg.v**4/(D2v*D2v)
    return TA_B2
t0 = time.time()
ok, n = der_sign(lambda g: comps2(g), Decimal('0.72'), Decimal('0.724'), True)
print('der_sign TA_B2 inc [0.72,0.724]:', ok, 'boxes:', n, 'time %.2fs' % (time.time()-t0))
t0 = time.time()
ok, n = der_sign(lambda g: comps2(g), Decimal('0.655'), Decimal('1.0472'), False)
print('der_sign TA_B2 dec full (expect False, peak):', ok, 'time %.2fs' % (time.time()-t0))
