# -*- coding: utf-8 -*-
"""t3_b2_1d: detailed study of B2(A,0.4) and pieces at min."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 50

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
    return dict(A=A,c=c,t=t,g=g,sg=sg,cg=cg,w=w,G0=G0,G1=G1,F=F,H2=H2,
                T0=sg*t*G0, T2=A*sqrt(w*(1-w))*H2, B2=-sg*t*G0 + A*sqrt(w*(1-w))*H2)

# 1D: B2(A, 0.4)
Amin, Amax = mpf(2)*mppi/3, mppi - mpf('0.655')
def B2_04(A): return comps(A, mpf('0.4'))['B2']
def dB2_04(A, h=mpf('1e-6')): return (B2_04(A+h)-B2_04(A-h))/(2*h)
def d2B2_04(A, h=mpf('1e-4')): return (B2_04(A+h)-2*B2_04(A)+B2_04(A-h))/(h*h)

lo, hi = mpf(1e30), mpf(-1e30); arglo = None
for i in range(2001):
    A = Amin + mpf(i)*(Amax-Amin)/2000
    v = B2_04(A)
    if v < lo: lo = v; arglo = (A, i)
    if v > hi: hi = v
print('B2(A,0.4) on [2pi/3, pi-0.655]: min %.6f at A=%.6f ; max %.6f' % (lo, arglo[0], hi))
print('endpoints: B2(2pi/3,0.4)=%.6f  B2(pi-0.655,0.4)=%.6f' % (B2_04(Amin), B2_04(Amax)))
# derivative ranges
loD, hiD, lo2, hi2 = mpf(1e30), mpf(-1e30), mpf(1e30), mpf(-1e30)
for i in range(1001):
    A = Amin + mpf(i)*(Amax-Amin)/1000
    v = dB2_04(A); v2 = d2B2_04(A)
    loD = min(loD,v); hiD = max(hiD,v); lo2 = min(lo2,v2); hi2 = max(hi2,v2)
print('dB2_04 in [%.4f, %.4f]; d2B2_04 in [%.4f, %.4f]' % (loD, hiD, lo2, hi2))
# find zero of dB2_04
# bisection on increasing part
zA = None
for i in range(2000):
    A1 = Amin + mpf(i)*(Amax-Amin)/2000
    A2 = Amin + mpf(i+1)*(Amax-Amin)/2000
    d1, d2 = dB2_04(A1), dB2_04(A2)
    if d1*d2 < 0:
        zA = (A1+A2)/2
        break
print('zero of dB2_04 near A=%.6f' % zA if zA else 'no sign change found')
# pieces at the min
c0 = comps(arglo[0], mpf('0.4'))
for k in ['t','g','sg','cg','w','G0','G1','F','H2','T0','T2','B2']:
    print('%s = %.6f' % (k, c0[k]))
# pieces at corner 5pi/7
c1 = comps(mpf(5)*mppi/7, mpf('0.4'))
print('--- corner (5pi/7, 0.4):')
for k in ['t','g','sg','cg','w','G0','G1','F','H2','T0','T2','B2']:
    print('%s = %.6f' % (k, c1[k]))
