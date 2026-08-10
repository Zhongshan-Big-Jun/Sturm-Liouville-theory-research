# -*- coding: utf-8 -*-
"""t3_b2_fine: fine scan of B2 min over D and 1D slice behavior."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 30

def comps(A, c):
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

Amin, Amax = mpf(2)*mppi/3, mppi - mpf('0.655')
def inD(A, c): return A*(1+c) >= mppi and A >= Amin and A <= Amax and c >= mpf('0.4') and c <= mpf('0.5')

best = (mpf(1e30), None)
for i in range(300):
    A = Amin + mpf(i)*(Amax-Amin)/300
    for j in range(300):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/300
        if not inD(A, c): continue
        v = comps(A, c)
        if v < best[0]: best = (v, (A, c))
print('coarse min B2 over D:', best)
# refine around best
Ab, cb = best[1]
for _ in range(3):
    hA = mpf('0.0001'); hc = mpf('0.0001')
    b2 = (mpf(1e30), None)
    for i in range(21):
        A = Ab - hA + mpf(i)*(2*hA)/20
        for j in range(21):
            c = cb - hc + mpf(j)*(2*hc)/20
            if not inD(A, c): continue
            v = comps(A, c)
            if v < b2[0]: b2 = (v, (A, c))
    Ab, cb = b2[1]
print('refined min B2 over D:', b2)
A0 = mpf(5)*mppi/7
lo, hi, arglo = mpf(1e30), mpf(-1e30), None
for i in range(2001):
    A = A0 + mpf(i)*(Amax-A0)/2000
    v = comps(A, mpf('0.4'))
    if v < lo: lo = v; arglo = (A, i)
    if v > hi: hi = v
print('B2(A,0.4) on [5pi/7, pi-0.655]: min %.6f at A=%.6f ; max %.6f' % (lo, arglo[0], hi))
def dB2dt(A, c, h=mpf('1e-6')):
    return (comps(A, c+h) - comps(A, c-h))/(2*h)
loT, hiT, argT = mpf(1e30), mpf(-1e30), None
for i in range(150):
    A = Amin + mpf(i)*(Amax-Amin)/150
    for j in range(150):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/150
        v = dB2dt(A, c)
        if v < loT: loT = v; argT = ('min', A, c)
        if v > hiT: hiT = v
print('dB2/dt over full box: [%.3f, %.3f] at %s' % (loT, hiT, argT))
print('B2(5pi/7, 0.4) =', comps(mpf(5)*mppi/7, mpf('0.4')))
