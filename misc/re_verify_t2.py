# -*- coding: utf-8 -*-
"""Re-verify core facts: closed forms, E3 ranges on T2."""
import math, pickle, json
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
mp.dps = 40

# ---------- closed forms in (x, th) ----------
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
    Hx = 2*c*(q*q-1)*((s*s - b*b)*den - s*(-b)*denx)/(den*den)
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, s=s, b=b, S=S, C=C, Phi=Phi, c=c, u=u, A0=A0, H=H, V=V, G=G, Gx=Gx, Gc=Gc)

# check identity Phi = b^2/C^2, u = b*s*x^2/(b*s*th + C*S*x) etc.
x0 = mpf('2.2'); th0 = mpf('1.0')
r = comps(x0, th0)
Delta = r['b']*r['s']*th0 + r['C']*r['S']*x0
print('Phi check:', r['Phi'], r['b']**2/r['C']**2)
print('u check  :', r['u'], r['b']*r['s']*x0**2/Delta)
# H check: 2t(C^2 s^2 - S^2 b^2)/Delta
print('H check  :', r['H'], 2*th0*(r['C']**2*r['s']**2 - r['S']**2*r['b']**2)/Delta)

# ---------- T2 sampling: Gx min, dGx/dx|th ----------
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
h = mpf('1e-6')
def dGx_dx(x, th):
    return (comps(x+h, th)['Gx'] - comps(x-h, th)['Gx'])/(2*h)
def dGx_dth(x, th):
    return (comps(x, th+h)['Gx'] - comps(x, th-h)['Gx'])/(2*h)

gmin = (mpf('1e30'), None); dmin = (mpf('1e30'), None)
# sample the whole T2 box in (x,th): th in [2x/5, x/2] intersected with q in (1,2)
N = 60
worst_d = mpf('1e30')
cnt = 0
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    # theta range at this x
    th_lo = max(2*x/5, mppi-x)
    th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(N+1):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        cnt += 1
        rr = comps(x, th)
        Gx = rr['Gx']
        if Gx < gmin[0]: gmin = (Gx, (float(x), float(th), float(rr['q']), float(rr['c'])))
        d = dGx_dx(x, th)
        if d < worst_d: worst_d = d
print('samples:', cnt, ' Gx min:', gmin)
print('min dGx/dx|th over sample:', worst_d)
# dGx/dth sign changes?
dth_vals = [dGx_dth(x, th) for i in range(0,N+1,5) for j in range(0,N+1,5)
            for x in [xmin + mpf(i)*(xmax-xmin)/N] for th in []]
# do explicit scan for dGx/dth
dth_min = mpf('1e30'); dth_max = mpf('-1e30'); dth_at_min = None; dth_at_max = None
for i in range(0,N+1,3):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(0,N+1,3):
        th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th <= th_lo or th >= th_hi: continue
        d = dGx_dth(x, th)
        if d < dth_min: dth_min, dth_at_min = d, (float(x), float(th))
        if d > dth_max: dth_max, dth_at_max = d, (float(x), float(th))
print('dGx/dth range: [%.4f, %.4f] at %s / %s' % (dth_min, dth_max, dth_at_min, dth_at_max))
