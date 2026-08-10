# -*- coding: utf-8 -*-
"""t3_db2dt_T2: dB2/dt min over T2 + symbolic decomposition attempt."""
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
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)
def B2_gq(g, q):
    A = mppi-g
    t = atan(q*tan(g))
    return B2(A, t/A)

# dB2/dt at (A,c): dB2/dc * (1/A) since t = cA => dB2/dt = (1/A) dB2/dc
def dB2dt_gq(g, q, h=mpf('1e-6')):
    A = mppi-g
    t0 = atan(q*tan(g)); c0 = t0/A
    return (B2(A, c0+h) - B2(A, c0-h))/(2*h)
    # note: this is dB2/dc; dB2/dt = dB2/dc / A... wait t=cA, dB2/dt = (dB2/dc)/A? No: B2 as function of c: dB2/dc = A * dB2/dt. So dB2/dt = (dB2/dc)/A.
# fix: return dB2/dt
def dB2dt_gq2(g, q, h=mpf('1e-6')):
    A = mppi-g
    t0 = atan(q*tan(g)); c0 = t0/A
    return (B2(A, c0+h) - B2(A, c0-h))/(2*h)/A

lo, hi, arglo = mpf(1e30), mpf(-1e30), None
for i in range(200):
    g = glo + mpf(i)*(ghi-glo)/200
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(200):
        q = ql + mpf(j)*(qh-ql)/200
        if q < 1 or q > 2: continue
        v = dB2dt_gq2(g, q)
        if v < lo: lo = v; arglo = (g, q)
        if v > hi: hi = v
print('dB2/dt over T2: [%.3f, %.3f], min at (g,q)=(%.4f, %.4f)' % (lo, hi, arglo[0], arglo[1]))
# check at corner (2pi/7, 1)
gv = mpf(2)*mppi/7
print('dB2/dt at corner:', dB2dt_gq2(gv, mpf(1)))
