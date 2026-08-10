# -*- coding: utf-8 -*-
"""NJ2 term values at corner L and at R; look for sign structure."""
import json
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
def terms(x, th):
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    out = []
    for cf, m in zip(coeffs, monoms):
        val = cf * x**m[0] * th**m[1] * s**m[2] * b**m[3] * S**m[4] * C**m[5]
        out.append((cf, m, val))
    return out
for (name, x, th) in [('L', 2*mppi/3, mppi/3), ('R', mppi-mpf('0.65564932893873566325493245529469'), 2*(mppi-mpf('0.65564932893873566325493245529469'))/5)]:
    ts = terms(x, th)
    print(name, ': sum =', sum(t[2] for t in ts))
    pos = sum(t[2] for t in ts if t[2] > 0); neg = sum(t[2] for t in ts if t[2] < 0)
    print('  pos sum =', pos, ' neg sum =', neg)
    for cf, m, val in sorted(ts, key=lambda t: t[2]):
        print('   %+d A^%d t^%d s^%d b^%d S^%d C^%d = %+.3f' % (cf, m[0],m[1],m[2],m[3],m[4],m[5], val))
