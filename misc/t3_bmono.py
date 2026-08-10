# -*- coding: utf-8 -*-
"""t3_bmono: check d B /dt and d B /dA signs on region (finite differences, high precision)."""
import numpy as np, math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 40
Amin, Amax = mpf(2)*mppi/3, mppi - mpf('0.655')

def comps(A, c):
    t = c*A; g = mppi - A
    sg = sin(g); cg = cos(g); w = cos(t)**2
    F1 = 8*A**3*cg**2 - 8*A**3*sg**2 + 16*A**3 + 16*A**2*cg**3*sg + 16*A**2*cg*sg**3 + 26*A**2*cg*sg - 15*A*sg**2 + 15*cg*sg**3
    F2 = (8*A**2*cg**4 - 8*A**2*cg**2*sg**2 - 56*A**2*cg**2*w + 58*A**2*cg**2 + 16*A**2*sg**2*w - 12*A**2*sg**2
          + 48*A**2*w**2 - 40*A**2*w + 66*A*cg**3*sg + 8*A*cg*sg**3 - 38*A*cg*sg*w + 15*A*cg*sg + cg**2*sg**2)
    F3 = (-72*A**3*cg**3*w + 36*A**3*cg**3 + 96*A**3*cg*w**2 - 32*A**3*cg*w - 16*A**3*cg
          + 8*A**2*cg**4*sg - 8*A**2*cg**2*sg**3 + 140*A**2*cg**2*sg*w - 68*A**2*cg**2*sg + 8*A**2*sg**3*w
          - 140*A**2*sg*w**2 + 104*A**2*sg*w - 48*A*cg**3*sg**2*t**2 + 42*A*cg**3*sg**2 - 16*A*cg*sg**4*t**2
          + 72*A*cg*sg**2*t**2*w - 40*A*cg*sg**2*w + 15*A*cg*sg**2 - 32*cg**2*sg**3*t**2 - 15*cg**2*sg**3)
    B = cg**2*sg*t*F1 - 2*A*sg*t*w*F2 - A*sqrt(w*(1-w))*F3
    return B

def dBdt(A, c, h=mpf('1e-6')):
    return (comps(A, c+h) - comps(A, c-h))/(2*h)
def dBdA(A, c, h=mpf('1e-6')):
    return (comps(A+h, c) - comps(A-h, c))/(2*h)

lo_t = (1e9, None); lo_A = (1e9, None); hi_t = (-1e9, None); hi_A = (-1e9, None)
for i in range(200):
    A = Amin + mpf(i)*(Amax-Amin)/200
    for j in range(200):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/200
        if A*(1+c) < mppi: continue
        dt = dBdt(A, c); dA = dBdA(A, c)
        if dt < lo_t[0]: lo_t = (float(dt), (float(A), float(c)))
        if dt > hi_t[0]: hi_t = (float(dt), (float(A), float(c)))
        if dA < lo_A[0]: lo_A = (float(dA), (float(A), float(c)))
        if dA > hi_A[0]: hi_A = (float(dA), (float(A), float(c)))
print('dB/dt in [%.3f, %.3f]  min at %s max at %s' % (lo_t[0], hi_t[0], lo_t[1], hi_t[1]))
print('dB/dA in [%.3f, %.3f]  min at %s max at %s' % (lo_A[0], hi_A[0], lo_A[1], hi_A[1]))
