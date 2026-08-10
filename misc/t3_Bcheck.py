# -*- coding: utf-8 -*-
"""t3_Bcheck.py: sign of reduced NJ2 factor B on T2."""
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30
gstar = mpf('0.65564932893873566325493245529469')
# B from reduction: variables A=x, t=th, sg=sin(g), cg=cos(g), st=sin(th), ct=cos(th), g=pi-A
def Bval(x, th):
    g = mppi - x
    sg, cg = sin(g), cos(g)
    st, ct = sin(th), cos(th)
    A, t = x, th
    B = (-A**3*cg**2*ct*sg*st*t + A**3*ct**3*sg*st*t + 2*A**2*cg**3*ct**2*t**2 + 12*A**2*cg**3*ct*st*t
         - A**2*cg**3*sg**2*t**2 - 4*A**2*cg*ct**4*t**2 + 4*A**2*cg*ct**3*st*t + A**2*cg*ct**2*sg**2*t**2
         - 6*A**2*cg*ct**2*st**2 + A**2*cg*ct**2*t**2 + 8*A*cg**2*ct**2*sg*t**2 - 12*A*cg**2*ct*sg*st*t
         + 6*cg**5*t**2 - 6*cg**3*sg**2*t**2 - 6*cg**3*t**2)
    return B

xmin, xmax = 2*mppi/3, mppi-gstar
lo, hi, arglo = mpf(1e30), mpf(-1e30), None
N=400
cnt=0
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    for j in range(N+1):
        th = mpf('0.4')*x + mpf(j)*(mpf('0.1')*x)/N
        if th < mppi - x: continue
        q = -tan(th)/tan(x)
        if q < 1 or q > 2: continue
        v = Bval(x, th)
        cnt += 1
        if v < lo: lo = v; arglo=(float(x),float(th))
        if v > hi: hi = v
print('B on T2: [%.6f, %.6f] at (x,th)=(%.4f,%.4f), n=%d' % (lo, hi, arglo[0], arglo[1], cnt))
# also verify NJ2 = -32 A^2 cg B on T2
import json
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
def NJ2val(x, th):
    g = mppi - x
    sg, cg = sin(g), cos(g)
    st, ct = sin(th), cos(th)
    tot = mpf(0)
    for cf, m in zip(r['coeffs'], r['monoms']):
        tot += int(cf)*x**m[0]*th**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5]
    return tot
for (x,th) in [(2*mppi/3, mppi/3), (2.4, 1.0), (2.2, 0.98), (2.4859, 0.9944)]:
    v1 = NJ2val(mpf(str(x)), mpf(str(th)))
    v2 = -32*x**2*cos(mppi-x)*Bval(mpf(str(x)), mpf(str(th)))
    print('x=%.4f th=%.4f: NJ2=%.6f vs -32A^2cgB=%.6f diff=%.1e' % (x,th,v1,v2,abs(v1-v2)))
