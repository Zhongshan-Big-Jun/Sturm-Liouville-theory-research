# -*- coding: utf-8 -*-
"""t3_b2_T2: B2 and dNJ2/dq over the TRUE region T2."""
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

# T2 in (gamma, q): gamma in [gstar, pi/3], q in [q_lo(gamma), q_hi(gamma)]
# q_lo: c=0.4: atan(q tan g) = 0.4(pi-g) => q = tan(0.4(pi-g))/tan g
# q_hi: c=0.5: q = tan(0.5(pi-g))/tan g = cot(g/2)/tan g
gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

best = (mpf(1e30), None)
worst = (mpf(-1e30), None)
for i in range(400):
    g = glo + mpf(i)*(ghi-glo)/400
    ql, qh = qlo(g), qhi(g)
    for j in range(400):
        q = ql + mpf(j)*(qh-ql)/400
        if q < 1 or q > 2: continue
        A = mppi-g
        c = atan(q*tan(g))/A
        v = B2(A, c)
        if v < best[0]: best = (v, (g, q, c))
        if v > worst[0]: worst = (v, (g, q, c))
print('B2 over T2: min %.6f at (g,q,c)=(%.6f, %.4f, %.4f); max %.6f' % (best[0], best[1][0], best[1][1], best[1][2], worst[0]))
# corners
for (g,q) in [(gstar, 2.0), (2*mppi/7, 1.0), (mppi/3, 1.0)]:
    A = mppi-g
    c = atan(q*tan(g))/A
    print('corner (g=%.6f, q=%.2f): c=%.6f B2=%.6f' % (g, q, c, B2(A,c)))
# also q=2 line from gstar to where q_hi = 2: c ranges 0.4 -> ?
# check B2 on the c=0.4 curve over gamma in [gstar, 2pi/7]
lo, hi = mpf(1e30), mpf(-1e30)
for i in range(1001):
    g = gstar + mpf(i)*(2*mppi/7-gstar)/1000
    q = qlo(g)
    A = mppi-g
    v = B2(A, mpf('0.4'))
    lo = min(lo, v); hi = max(hi, v)
print('B2 on c=0.4 curve (g in [gstar, 2pi/7]): [%.6f, %.6f]' % (lo, hi))
