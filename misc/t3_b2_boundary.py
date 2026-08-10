# -*- coding: utf-8 -*-
"""t3_b2_boundary: B2 on q=1 line and c=0.4 slice details."""
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
    G1a = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg - 12*A*cg**2*sg**2 - 12*A*sg**2 + 12*cg*sg**3)
    G1b = (6*A*cg**2*sg**2 + 2*A*sg**4 + 16*cg*sg**3)
    Fa = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg - 20*cg*sg**2)
    Fb = 16*cg*sg**2
    H2a = cg*G1a - A*w*Fa
    H2b = cg*G1b - A*w*Fb
    T0 = sg*t*G0
    T2a = A*sqrt(w*(1-w))*H2a
    T2b = A*t**2*sqrt(w*(1-w))*H2b
    B2 = -T0 + T2a + T2b
    return dict(t=t,g=g,sg=sg,cg=cg,w=w,G0=G0,H2a=H2a,H2b=H2b,T0=T0,T2a=T2a,T2b=T2b,B2=B2)

# (2c): q=1 line: A = pi/(1+c), t = gamma = pi c/(1+c), c in [0.4, 0.5]
print('=== B2 on q=1 line (c in [0.4,0.5]):')
lo, hi, arglo = mpf(1e30), mpf(-1e30), None
for i in range(2001):
    cv = mpf('0.4') + mpf(i)*mpf('0.1')/2000
    Av = mppi/(1+cv)
    v = comps(Av, cv)['B2']
    if v < lo: lo = v; arglo = (cv, i)
    if v > hi: hi = v
print('B2 on q1 line: min %.6f at c=%.6f ; max %.6f' % (lo, arglo[0], hi))
# derivative of B2 along q1 line w.r.t. c
def B2q1(c): return comps(mppi/(1+c), c)['B2']
loD, hiD = mpf(1e30), mpf(-1e30)
for i in range(1001):
    cv = mpf('0.4') + mpf(i)*mpf('0.1')/1000
    h = mpf('1e-6')
    v = (B2q1(cv+h)-B2q1(cv-h))/(2*h)
    loD = min(loD, v); hiD = max(hiD, v)
print('dB2/dc along q1 line: [%.4f, %.4f]' % (loD, hiD))

# (2b): B2(A, 0.4) on [5pi/7, pi-0.655]
print('=== B2(A,0.4) on [5pi/7, pi-0.655]:')
A0 = mpf(5)*mppi/7
Amax = mppi - mpf('0.655')
lo, hi, arglo = mpf(1e30), mpf(-1e30), None
for i in range(2001):
    Av = A0 + mpf(i)*(Amax-A0)/2000
    v = comps(Av, mpf('0.4'))['B2']
    if v < lo: lo = v; arglo = (Av, i)
    if v > hi: hi = v
print('min %.6f at A=%.6f ; max %.6f' % (lo, arglo[0], hi))
def B204(A): return comps(A, mpf('0.4'))['B2']
loD, hiD = mpf(1e30), mpf(-1e30)
for i in range(1001):
    Av = A0 + mpf(i)*(Amax-A0)/1000
    h = mpf('1e-6')
    v = (B204(Av+h)-B204(Av-h))/(2*h)
    loD = min(loD, v); hiD = max(hiD, v)
print('dB2/dA on c=0.4 slice: [%.4f, %.4f]' % (loD, hiD))
# pieces at min points
print('pieces at (5pi/7, 0.4):')
d = comps(mpf(5)*mppi/7, mpf('0.4'))
for k in ['G0','H2a','H2b','T0','T2a','T2b','B2']:
    print('  %s = %.6f' % (k, d[k]))
print('pieces at (2pi/3, 0.5):')
d = comps(mpf(2)*mppi/3, mpf('0.5'))
for k in ['G0','H2a','H2b','T0','T2a','T2b','B2']:
    print('  %s = %.6f' % (k, d[k]))
