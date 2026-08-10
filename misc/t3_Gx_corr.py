# -*- coding: utf-8 -*-
"""t3_Gx_corr: correlation of Gx components."""
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
    V = H - A0
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return ux, V, u, Hx, A0x, Gx, Phi, den

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

# find min of Gx and components
best = {}
for i in range(400):
    g = glo + mpf(i)*(ghi-glo)/400
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(400):
        q = ql + mpf(j)*(qh-ql)/400
        if q < 1 or q > 2: continue
        ux, V, u, Hx, A0x, Gx, Phi, den = comps(g,q)
        for k, v in [('Gx',Gx),('uxV',ux*V),('uHx',u*Hx),('mAx',-u*A0x),('V',V),('ux',ux)]:
            if k not in best or v < best[k][0]: best[k] = (v, (g,q))
        # correlation: uxV+uHx and -uA0x
        key='negpart'; v=ux*V+u*Hx
        if key not in best or v < best[key][0]: best[key]=(v,(g,q))
        key='summ'; v=ux*V+u*Hx-u*A0x
        if key not in best or v < best[key][0]: best[key]=(v,(g,q))
for k in best:
    print('%s: min %.6f at (g,q)=(%.4f,%.4f)' % (k, best[k][0], best[k][1][0], best[k][1][1]))
# correlation check: at argmin of negpart, what is -uA0x?
g0,q0 = best['negpart'][1]
ux, V, u, Hx, A0x, Gx, Phi, den = comps(g0,q0)
print('at negpart min: uxV=%.5f uHx=%.5f -uA0x=%.5f Gx=%.5f' % (ux*V, u*Hx, -u*A0x, Gx))
