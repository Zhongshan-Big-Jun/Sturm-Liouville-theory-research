# -*- coding: utf-8 -*-
"""t3_J2_components: extrema of G^2+Gc and u*Gx over T2."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, tan, atan, pi as mppi
mp.dps = 30

# G, Gc, Gx, u in (A, t, gamma) coordinates; A=pi-g, t=cA
# From doc: u = x*Phi/(q+c*Phi), Phi = q^2 sin^2 x + cos^2 x, x = A
# G = u*(H - A0), A0 = 3/x + 2 cot x, H = 2c(q^2-1) sin x cos x/(q + c Phi)
# Gc = partial_c G, Gx = partial_x G
def comps(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sg = sin(g); cg = cos(g)
    # x = A = pi-g: sin x = sg, cos x = -cg
    sx, cx = sg, -cg
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = 3/A + 2*cx/sx   # cot x = cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    G = u*(H - A0)
    # Gc: d/dc G at fixed (x,q): u = x Phi/(q+c Phi), H = 2c(q^2-1)sx cx/(q+c Phi)
    # dG/dc = du/dc*(H-A0) + u*dH/dc
    du = -A*Phi*Phi/(den*den)
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
    Gc = du*(H-A0) + u*dH
    # Gx: d/dx G at fixed (q,c): x = A. u_x, H_x, A0_x
    # Phi_x = d/dx (q^2 sin^2 x + cos^2 x) = 2(q^2-1) sx cx
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) + 2*(-1/sx**2)   # d/dx cot x = -csc^2 x = -1/sin^2 x
    Hx = (2*c*(q*q-1)*(cx**2 - sx**2)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*(H-A0) + u*(Hx - A0x)
    return G, Gc, Gx, u

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)

bestH1 = (mpf(-1e30), None); bestH2 = (mpf(1e30), None)
bestG = (None, None); bestGc = (None, None); bestGx = (None, None); bestu = (None, None)
ranges = {'G':[mpf(1e30),mpf(-1e30)], 'Gc':[mpf(1e30),mpf(-1e30)], 'Gx':[mpf(1e30),mpf(-1e30)], 'u':[mpf(1e30),mpf(-1e30)]}
for i in range(200):
    g = glo + mpf(i)*(ghi-glo)/200
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(200):
        q = ql + mpf(j)*(qh-ql)/200
        if q < 1 or q > 2: continue
        G, Gc, Gx, u = comps(g,q)
        H1 = G*G + Gc; H2 = u*Gx
        if H1 > bestH1[0]: bestH1 = (H1, (g,q))
        if H2 < bestH2[0]: bestH2 = (H2, (g,q))
        for k, v in [('G',G),('Gc',Gc),('Gx',Gx),('u',u)]:
            if v < ranges[k][0]: ranges[k][0]=v
            if v > ranges[k][1]: ranges[k][1]=v
print('G^2+Gc max: %.6f at (g,q)=(%.4f,%.3f)' % (bestH1[0], bestH1[1][0], bestH1[1][1]))
print('u*Gx min:   %.6f at (g,q)=(%.4f,%.3f)' % (bestH2[0], bestH2[1][0], bestH2[1][1]))
for k in ranges: print('%s: [%.4f, %.4f]' % (k, ranges[k][0], ranges[k][1]))
