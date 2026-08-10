# -*- coding: utf-8 -*-
"""t3_b2_box: B2 min over the box [g*,pi/3] x [1,2] and related regions."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
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
glo, ghi = gstar, mppi/3
def B2_gq(g, q):
    A = mppi-g
    t = atan(q*tan(g))
    c = t/A
    return B2(A, c)

best = (mpf(1e30), None)
for i in range(200):
    g = glo + mpf(i)*(ghi-glo)/200
    for j in range(200):
        q = mpf(1) + mpf(j)/200
        v = B2_gq(g, q)
        if v < best[0]: best = (v, (g, q))
print('B2 min over box [g*,pi/3]x[1,2]: %.6f at (g,q)=(%.6f, %.4f)' % (best[0], best[1][0], best[1][1]))
# corners of box
for (g,q) in [(gstar,1.0),(gstar,2.0),(mppi/3,1.0),(mppi/3,2.0)]:
    print('corner (g=%.4f, q=%.1f): B2=%.6f' % (g, q, B2_gq(g,q)))
# region between T2 and q=2 line: gamma in [g*,pi/3], q in [q_lo(g), 2]
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
best2 = (mpf(1e30), None)
for i in range(200):
    g = glo + mpf(i)*(ghi-glo)/200
    ql = qlo(g)
    if ql > 2: continue
    for j in range(200):
        q = ql + mpf(j)*(2-ql)/200
        v = B2_gq(g, q)
        if v < best2[0]: best2 = (v, (g, q))
print('B2 min over {q in [q_lo(g), 2]}: %.6f at (g,q)=(%.6f, %.4f)' % (best2[0], best2[1][0], best2[1][1]))
