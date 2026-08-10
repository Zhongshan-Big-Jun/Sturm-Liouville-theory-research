# -*- coding: utf-8 -*-
"""Study F := Phi*(9x^2-4pi*th) - 4pi*x*q on T2: min, location, monotonicity."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 50

def Fval(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    return Phi*(9*x*x - 4*mppi*th) - 4*mppi*x*q

def uval(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    return x*Phi/(q + c*Phi)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 150
mn = (mpf('1e30'), None); mx = (mpf('-1e30'), None)
dFx_min = mpf('1e30'); dFx_max = mpf('-1e30'); dFth_min = mpf('1e30'); dFth_max = mpf('-1e30')
h = mpf('1e-6')
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    tlo = max(2*x/5, mppi-x); thi = min(x/2, atan(-2*tan(x)))
    if tlo >= thi: continue
    for j in range(N+1):
        t = tlo + mpf(j)*(thi-tlo)/N
        if t <= tlo or t >= thi: continue
        v = Fval(x, t)
        if v < mn[0]: mn = (v, (float(x), float(t)))
        if v > mx[0]: mx = (v, (float(x), float(t)))
        dFx = (Fval(x+h,t)-Fval(x-h,t))/(2*h)
        dFt = (Fval(x,t+h)-Fval(x,t-h))/(2*h)
        dFx_min = min(dFx_min, dFx); dFx_max = max(dFx_max, dFx)
        dFth_min = min(dFth_min, dFt); dFth_max = max(dFth_max, dFt)
print('F on T2: min %.6f at %s ; max %.6f' % (mn[0], mn[1], mx[0]))
print('dF/dx|th: [%.4f, %.4f] ; dF/dth|x: [%.4f, %.4f]' % (dFx_min, dFx_max, dFth_min, dFth_max))
# u - 4pi/9 on boundary curves
print()
for (nm, thf) in [('q=1', lambda x: mppi-x), ('c=1/2', lambda x: x/2), ('c=2/5', lambda x: 2*x/5)]:
    lo = (mpf('1e30'), None)
    for i in range(2000):
        x = xmin + mpf(i)*(xmax-xmin)/2000
        t = thf(x)
        if t < max(2*x/5, mppi-x) - mpf('1e-12') or t > min(x/2, atan(-2*tan(x))) + mpf('1e-12'): continue
        v = uval(x, t) - 4*mppi/9
        if v < lo[0]: lo = (v, float(x))
    print('%s: u-4pi/9 min %.8f at x=%.4f' % (nm, lo[0], lo[1]))
