# -*- coding: utf-8 -*-
"""Verify psi(b) < 0 on [1/2,2/3] and its structure; Gx>=21/5 on c=1/2 curve."""
from mpmath import mp, mpf, cos, sin, pi as mppi, sqrt
mp.dps = 50
def P(b): return 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
def Q(b): return 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
def psi(b):
    s = sqrt(1-b*b)
    return 2*(2*mppi/3)*P(b) + 2*s*Q(b) + mpf(21)/5*(1-b*b)**2*(1+b)**3

pts = [mpf('0.5'), mpf('0.52'), mpf('0.55'), mpf('0.58'), mpf('0.6'), mpf('0.62'), mpf('0.65'), mpf(2)/3]
for b in pts:
    print('b=%.4f: P=%.6f Q=%.6f psi=%.6f' % (b, P(b), Q(b), psi(b)))
# find max of psi and its location
import numpy as np
bb = np.linspace(0.5, 2/3, 20001)
vals = [float(psi(mpf(str(v)))) for v in bb]
i = int(np.argmax(vals))
print('max psi = %.8f at b=%.6f' % (vals[i], bb[i]))
# derivative of psi
def dpsi(b):
    h = mpf('1e-7')
    return (psi(b+h)-psi(b-h))/(2*h)
for b in [mpf('0.5'), mpf('0.55'), mpf('0.6'), mpf('0.65'), mpf(2)/3]:
    print('dpsi(%.3f) = %.5f' % (b, dpsi(b)))
