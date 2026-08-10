# -*- coding: utf-8 -*-
"""t3_b2b_shape: detailed shape of boundary B2b(gamma)."""
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

# boundary: gamma in [0.655, pi/3]
# seg1: gamma in [0.655, 2pi/7], c=0.4: A=pi-gamma, t=0.4A
# seg2: gamma in [2pi/7, pi/3], q=1: A=pi-gamma, t=gamma, c=gamma/(pi-gamma)
gcorner = mpf(2)*mppi/7
def B2b(g):
    if g <= gcorner:
        A = mppi - g
        return B2(A, mpf('0.4'))
    else:
        A = mppi - g
        c = g/A
        return B2(A, c)

# scan values
glo, ghi = mpf('0.655'), mppi/3
lo, hi, arglo = mpf(1e30), mpf(-1e30), None
for i in range(4001):
    g = glo + mpf(i)*(ghi-glo)/4000
    v = B2b(g)
    if v < lo: lo = v; arglo = (g, i)
    if v > hi: hi = v
print('B2b on [0.655, pi/3]: min %.6f at g=%.6f ; max %.6f' % (lo, arglo[0], hi))

# derivative
def dB2b(g, h=mpf('1e-6')):
    return (B2b(g+h)-B2b(g-h))/(2*h)
loD, hiD, argloD = mpf(1e30), mpf(-1e30), None
for i in range(2001):
    g = glo + mpf(i)*(ghi-glo)/2000
    v = dB2b(g)
    if v < loD: loD = v; argloD = (g, i)
    if v > hiD: hiD = v
print('dB2b/dg in [%.4f, %.4f]; min at g=%.6f' % (loD, hiD, argloD[0]))
# second derivative
def d2B2b(g, h=mpf('1e-4')):
    return (B2b(g+h)-2*B2b(g)+B2b(g-h))/(h*h)
lo2, hi2 = mpf(1e30), mpf(-1e30)
for i in range(1001):
    g = glo + mpf(i)*(ghi-glo)/1000
    v = d2B2b(g)
    lo2 = min(lo2, v); hi2 = max(hi2, v)
print('d2B2b in [%.4f, %.4f]' % (lo2, hi2))
# sample the shape on seg1
print('B2b samples on seg1 (g, B2b, dB2b):')
for i in range(0, 11):
    g = mpf('0.655') + mpf(i)*(gcorner-mpf('0.655'))/10
    print('  g=%.5f B2b=%.6f dB2b=%.4f' % (g, B2b(g), dB2b(g)))
print('B2b samples on seg2:')
for i in range(0, 11):
    g = gcorner + mpf(i)*(mppi/3-gcorner)/10
    print('  g=%.5f B2b=%.6f dB2b=%.4f' % (g, B2b(g), dB2b(g)))
