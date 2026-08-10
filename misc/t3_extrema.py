# -*- coding: utf-8 -*-
"""t3_extrema: precise extrema of G, Gc, Gx, u, G^2+Gc, uGx over T2."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
mp.dps = 30

def comps(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = 3/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    G = u*(H - A0)
    du = -A*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*sx*cx/(den*den)
    Gc = du*(H-A0) + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*(H-A0) + u*(Hx - A0x)
    return G, Gc, Gx, u

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

ext = {'G':(None,None), 'Gc':(None,None), 'Gx':(None,None), 'u':(None,None),
       'H1':(None,None), 'H2':(None,None)}
N = 400
for i in range(N+1):
    g = glo + mpf(i)*(ghi-glo)/N
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q < 1 or q > 2: continue
        G, Gc, Gx, u = comps(g,q)
        for k, v in [('G',G),('Gc',Gc),('Gx',Gx),('u',u),('H1',G*G+Gc),('H2',u*Gx)]:
            lo, hi = ext[k]
            if lo is None or v < lo[0]: ext[k] = ((v,(g,q)), hi)
            if hi is None or v > hi[0]: ext[k] = (lo, (v,(g,q)))
for k in ext:
    lo, hi = ext[k]
    print('%s: min %.6f at (g,q)=(%.4f,%.4f); max %.6f at (g,q)=(%.4f,%.4f)' % (
        k, lo[0], lo[1][0], lo[1][1], hi[0], hi[1][0], hi[1][1]))
# exact values at the corners
for (g,q) in [(gstar,mpf(2)), (mpf(2)*mppi/7,mpf(1)), (mppi/3,mpf(1))]:
    G,Gc,Gx,u = comps(g,q)
    print('corner (g=%.5f,q=%.1f): G=%.6f Gc=%.6f Gx=%.6f u=%.8f  H1=%.6f H2=%.6f' % (g,q,G,Gc,Gx,u,G*G+Gc,u*Gx))
