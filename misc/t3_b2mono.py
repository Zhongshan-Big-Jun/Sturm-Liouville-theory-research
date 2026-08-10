# -*- coding: utf-8 -*-
"""t3_b2mono: B2 monotonicity in A and t; min location."""
import numpy as np, math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 40
Amin, Amax = mpf(2)*mppi/3, mppi - mpf('0.655')

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
    return -sg*t*G0 + A*sqrt(w*(1-w))*(cg*G1 - A*w*F)

# find min over region
best = (mpf(1e30), None)
for i in range(300):
    A = Amin + mpf(i)*(Amax-Amin)/300
    for j in range(300):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/300
        if A*(1+c) < mppi: continue
        v = B2(A, c)
        if v < best[0]: best = (v, (A, c))
print('min B2 =', best)
# B2 at that point components
A, c = best[1]; t = c*A; g = mppi - A
sg = sin(g); cg = cos(g); w = cos(t)**2
print('at min: A=%.6f c=%.6f t=%.6f gamma=%.6f sg=%.5f cg=%.5f w=%.5f' % (A,c,t,g,sg,cg,w))
# monotonicity near min: dB2/dA, dB2/dt
def dB2dA(A, c, h=mpf('1e-5')):
    return (B2(A+h, c) - B2(A-h, c))/(2*h)
def dB2dt(A, c, h=mpf('1e-5')):
    return (B2(A, c+h) - B2(A, c-h))/(2*h)
print('dB2/dA at min:', dB2dA(A,c), ' dB2/dt at min:', dB2dt(A,c))
# scan derivative signs
loA, hiA = mpf(1e30), mpf(-1e30); loT, hiT = mpf(1e30), mpf(-1e30)
for i in range(100):
    A = Amin + mpf(i)*(Amax-Amin)/100
    for j in range(100):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/100
        if A*(1+c) < mppi: continue
        vA = dB2dA(A, c); vT = dB2dt(A, c)
        loA = min(loA, vA); hiA = max(hiA, vA)
        loT = min(loT, vT); hiT = max(hiT, vT)
print('dB2/dA in [%.3f, %.3f]; dB2/dt in [%.3f, %.3f]' % (loA, hiA, loT, hiT))
