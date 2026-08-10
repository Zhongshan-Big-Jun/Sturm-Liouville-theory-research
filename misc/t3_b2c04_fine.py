# -*- coding: utf-8 -*-
"""t3_b2c04_fine: fine study of B2(A,0.4) near the corner."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 30

def B2(A, c):
    t = c*A; g = mppi - A
    sg = sin(g); cg = cos(g); w = cos(t)**2
    G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
          + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
          + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
          - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
    G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
          + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
    F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
    H2 = cg*G1 - A*w*F
    return -sg*t*G0 + A*sqrt(w*(1-w))*H2

gstar = mpf('0.65564932893873566325493245529469')
gcorner = mpf(2)*mppi/7
# B2c04(g) = B2(pi-g, 0.4), g in [gstar, gcorner]
def B2c04(g): return B2(mppi-g, mpf('0.4'))
print('gcorner =', gcorner)
for gg in [mpf('0.88'), mpf('0.89'), mpf('0.895'), mpf('0.897'), mpf('0.8975'), mpf('0.89759'), gcorner]:
    print('g=%.6f B2c04=%.9f' % (gg, B2c04(gg)))
# one-sided derivatives near corner (c=0.4 side only)
def d04(g, h=mpf('1e-8')):
    return (B2c04(g+h)-B2c04(g-h))/(2*h)
for gg in [mpf('0.88'), mpf('0.89'), mpf('0.895'), mpf('0.897'), mpf('0.8975'), mpf('0.89758')]:
    print('g=%.6f dB2c04/dg=%.4f' % (gg, d04(gg)))
