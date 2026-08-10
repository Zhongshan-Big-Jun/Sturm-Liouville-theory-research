# -*- coding: utf-8 -*-
"""Fixed comps (correct Hx), re-verify all core facts."""
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
    # correct: w = s*(-b), w' = b^2 - s^2 ; H = 2c(q^2-1) w/den
    Hx = 2*c*(q*q-1)*((b*b - s*s)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, s=s, b=b, S=S, C=C, Phi=Phi, c=c, u=u, A0=A0, H=H, V=V, G=G, Gx=Gx, Gc=Gc)

# c=1/2 closed form recheck
M_str = "(b**7*s**2*x - 2*b**6*x + 2*b**5*s**4*x + b**5*s**3 - b**5*s**2*x + 3*b**5*s - 2*b**5*x - 2*b**4*s**4*x - 3*b**4*s**3 - 2*b**4*s**2*x + 5*b**4*s + 2*b**4*x + b**3*s**6*x + b**3*s**5 + 2*b**3*s**4*x - 3*b**3*s**3 - 3*b**3*s + 4*b**3*x - 2*b**2*s**6*x - 3*b**2*s**5 + 2*b**2*s**4*x - 3*b**2*s**3 - 2*b**2*s**2*x - 5*b**2*s + 3*b*s**6*x + 2*b*s**5 - 3*b*s**3 - 2*b*s**2*x - 2*b*x - 2*s**6*x + 3*s**3)"
for xv in [mpf('2.15'), mpf('2.15316'), mpf('2.16'), mpf('2.25'), mpf('2.3')]:
    x = xv; s = sin(xv); b = -cos(xv)
    M31 = eval(M_str)
    cf = -2*M31/(s**4*(1+b)**3)
    nc = comps(xv, xv/2)['Gx']
    print('c=1/2 x=%.6f: closed=%.8f comps=%.8f diff=%.1e' % (xv, cf, nc, abs(cf-nc)))

# Gx min on T2 (fixed)
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')
gmin = (mpf('1e30'), None); dmin = (mpf('1e30'), None); dth_min = mpf('1e30'); dth_max = mpf('-1e30')
N = 80
cnt = 0
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        cnt += 1
        rr = comps(x, th)
        if rr['Gx'] < gmin[0]: gmin = (rr['Gx'], (float(x), float(th), float(rr['q']), float(rr['c'])))
        d = (comps(x+h, th)['Gx'] - comps(x-h, th)['Gx'])/(2*h)
        if d < dmin[0]: dmin = (d, (float(x), float(th)))
        dth = (comps(x, th+h)['Gx'] - comps(x, th-h)['Gx'])/(2*h)
        if dth < dth_min: dth_min = dth
        if dth > dth_max: dth_max = dth
print('samples:', cnt)
print('Gx min:', gmin)
print('dGx/dx|th min:', dmin)
print('dGx/dth range: [%.4f, %.4f]' % (dth_min, dth_max))

# H1 = G^2+Gc max, H2 = u*Gx min, J2 max on T2
h1max = (mpf('-1e30'), None); h2min = (mpf('1e30'), None); jmax = (mpf('-1e30'), None)
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        rr = comps(x, th)
        H1 = rr['G']**2 + rr['Gc']; H2 = rr['u']*rr['Gx']
        J = H1 - H2
        if H1 > h1max[0]: h1max = (H1, (float(x), float(th), float(rr['q'])))
        if H2 < h2min[0]: h2min = (H2, (float(x), float(th), float(rr['q'])))
        if J > jmax[0]: jmax = (J, (float(x), float(th), float(rr['q'])))
print('H1 max:', h1max)
print('H2 min:', h2min)
print('J2 max:', jmax)
