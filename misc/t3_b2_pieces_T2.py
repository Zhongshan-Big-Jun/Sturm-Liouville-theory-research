# -*- coding: utf-8 -*-
"""t3_b2_pieces_T2: ranges of B2 pieces over T2."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
mp.dps = 30

def pieces(A, c):
    t = c*A; g = mppi - A
    sg = sin(g); cg = cos(g); w = cos(t)**2
    G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
          + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
          + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
          - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
    G1a = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg - 12*A*cg**2*sg**2 - 12*A*sg**2 + 12*cg*sg**3)
    G1b = (6*A*cg**2*sg**2 + 2*A*sg**4 + 16*cg*sg**3)
    Fa = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg - 20*cg*sg**2)
    Fb = 16*cg*sg**2
    H2a = cg*G1a - A*w*Fa
    H2b = cg*G1b - A*w*Fb
    T0 = sg*t*G0
    T2a = A*sqrt(w*(1-w))*H2a
    T2b = A*t**2*sqrt(w*(1-w))*H2b
    return dict(T0=T0, T2a=T2a, T2b=T2b, mT0pT2a=-T0+T2a, B2=-T0+T2a+T2b, H2a=H2a, H2b=H2b, G0=G0)

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

rng = {k: [mpf(1e30), mpf(-1e30)] for k in ['T0','T2a','T2b','mT0pT2a','B2','H2a','H2b','G0']}
arg = {}
for i in range(300):
    g = glo + mpf(i)*(ghi-glo)/300
    ql, qh = qlo(g), qhi(g)
    for j in range(300):
        q = ql + mpf(j)*(qh-ql)/300
        if q < 1 or q > 2: continue
        A = mppi-g
        c = atan(q*tan(g))/A
        d = pieces(A, c)
        for k in rng:
            v = d[k]
            if v < rng[k][0]: rng[k][0]=v; arg[k]=('min',g,q)
            if v > rng[k][1]: rng[k][1]=v; arg[k]=('max',g,q)
for k in rng:
    print('%s: in [%.4f, %.4f]  %s' % (k, rng[k][0], rng[k][1], arg[k]))
# at the min point of B2
g0, q0 = mpf(2)*mppi/7, mpf(1)
A = mppi-g0; c = atan(q0*tan(g0))/A
d = pieces(A, c)
print('pieces at corner (2pi/7, 1):')
for k in d: print('  %s = %.6f' % (k, d[k]))
