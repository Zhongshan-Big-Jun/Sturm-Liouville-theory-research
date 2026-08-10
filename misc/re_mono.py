# -*- coding: utf-8 -*-
"""Check dJ2/dx|th < 0, dGx/dx|th > 0 on T2 (fine grid); J2/Gx along left boundary curves."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt, acos
mp.dps = 40

def comps(x, th):
    q = -tan(th)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
    c = th/x
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    Phix = 2*s*b*(1-q*q)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    J = G*G + Gc - u*Gx
    return dict(q=q, u=u, G=G, Gx=Gx, Gc=Gc, J=J)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')

# fine scan of dJ/dx|th and dGx/dx|th
N = 120
dJ_min = mpf('1e30'); dGx_min = mpf('1e30'); dJ_max = mpf('-1e30')
locJ = None; locG = None
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        dJ = (comps(x+h, th)['J'] - comps(x-h, th)['J'])/(2*h)
        dG = (comps(x+h, th)['Gx'] - comps(x-h, th)['Gx'])/(2*h)
        if dJ < dJ_min: dJ_min, locJ = dJ, (float(x), float(th))
        if dJ > dJ_max: dJ_max = dJ
        if dG < dGx_min: dGx_min, locG = dG, (float(x), float(th))
print('dJ/dx|th range [%.3f, %.3f], min at %s' % (dJ_min, dJ_max, locJ))
print('dGx/dx|th min %.3f at %s' % (dGx_min, locG))

# J2 along q=1 curve (left boundary part 1)
print()
print('q=1 curve (x in [2pi/3, 5pi/7]):')
for xv in [2*mppi/3, mpf('2.12'), mpf('2.16'), mpf('2.20'), mpf('2.24')]:
    r = comps(xv, mppi-xv)
    print('  x=%.4f: J=%.6f G=%.5f Gc=%.5f Gx=%.5f u=%.5f' % (xv, r['J'], r['G'], r['Gc'], r['Gx'], r['u']))
# c=2/5 curve (left boundary part 2): x in [5pi/7, xmax]
print('c=2/5 curve (x in [5pi/7, xmax]):')
for xv in [5*mppi/7, mpf('2.30'), mpf('2.36'), mpf('2.42'), mppi-gstar]:
    r = comps(xv, 2*xv/5)
    print('  x=%.4f: J=%.6f G=%.5f Gc=%.5f Gx=%.5f u=%.5f q=%.4f' % (xv, r['J'], r['G'], r['Gc'], r['Gx'], r['u'], r['q']))
