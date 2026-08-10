# -*- coding: utf-8 -*-
"""t3_GGc: correlation structure of G and Gc over T2."""
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
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
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

# where is Gc > 0? and G there?
best = {}
for i in range(300):
    g = glo + mpf(i)*(ghi-glo)/300
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(300):
        q = ql + mpf(j)*(qh-ql)/300
        if q < 1 or q > 2: continue
        G, Gc, Gx, u = comps(g,q)
        key = 'Gmax'; 
        if key not in best or G > best[key][0]: best[key] = (G, (g,q,Gc))
        key = 'GcMax'
        if key not in best or Gc > best[key][0]: best[key] = (Gc, (g,q,G))
        key = 'H1max'
        H1 = G*G+Gc
        if key not in best or H1 > best[key][0]: best[key] = (H1, (g,q,G,Gc))
        if Gc > 0:
            key = 'GcPos'
            if key not in best or G > best[key][0]: best[key] = (G, (g,q,Gc))
for k in best:
    print(k, ':', best[k])
# G, Gc at key points
for (g,q) in [(gstar,2.0),(2*math.pi/7,1.0),(math.pi/3,1.0),(0.9,1.5),(1.0,1.2)]:
    G,Gc,Gx,u = comps(mpf(str(g)), mpf(str(q)))
    print('(g=%.4f, q=%.2f): G=%.5f Gc=%.5f G^2+Gc=%.5f u=%.5f Gx=%.5f' % (g,q,G,Gc,G*G+Gc,u,Gx))
