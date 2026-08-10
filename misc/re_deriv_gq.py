# -*- coding: utf-8 -*-
"""Directional derivatives of G,Gc,Gx at fixed q and fixed c over T2 (E3 check)."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
mp.dps = 40

def from_gq(g, q):
    x = mppi - g
    th = atan(q*tan(g))
    return x, th

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
    return dict(G=G, Gx=Gx, Gc=Gc)

def at_gq(g, q):
    x, th = from_gq(g, q)
    return comps(x, th)

h = mpf('1e-5')
# sample T2 in (g,q): g in [gstar, pi/3], q in [1,2], c in (0.4,0.5)
gstar = mpf('0.65564932893873566325493245529469')
N = 40
print('dG/dg|q range, dG/dq|g range, dGc/dg|q, dGc/dq|g, dGx/dg|q, dGx/dq|g:')
mins = dict(dGg=(1e30,None),dGq=(1e30,None),dGcg=(1e30,None),dGcq=(1e30,None),dGxg=(1e30,None),dGxq=(1e30,None))
maxs = dict(dGg=(-1e30,None),dGq=(-1e30,None),dGcg=(-1e30,None),dGcq=(-1e30,None),dGxg=(-1e30,None),dGxq=(-1e30,None))
cnt = 0
for i in range(N+1):
    g = gstar + mpf(i)*(mppi/3 - gstar)/N
    for j in range(N+1):
        q = mpf(1) + mpf(j)/N
        x, th = from_gq(g, q)
        c = th/x
        if not (mpf('0.4') < c < mpf('0.5')): continue
        cnt += 1
        r0 = at_gq(g, q)
        rp = at_gq(g+h, q); rm = at_gq(g-h, q)
        rqp = at_gq(g, q+h); rqm = at_gq(g, q-h)
        d = dict(dGg=(rp['G']-rm['G'])/(2*h), dGq=(rqp['G']-rqm['G'])/(2*h),
                 dGcg=(rp['Gc']-rm['Gc'])/(2*h), dGcq=(rqp['Gc']-rqm['Gc'])/(2*h),
                 dGxg=(rp['Gx']-rm['Gx'])/(2*h), dGxq=(rqp['Gx']-rqm['Gx'])/(2*h))
        for k in d:
            if d[k] < mins[k][0]: mins[k] = (d[k], (float(g), float(q)))
            if d[k] > maxs[k][0]: maxs[k] = (d[k], (float(g), float(q)))
print('samples:', cnt)
for k in ['dGg','dGq','dGcg','dGcq','dGxg','dGxq']:
    print('  %s in [%.4f, %.4f]' % (k, mins[k][0], maxs[k][0]))
    print('     min at %s, max at %s' % (mins[k][1], maxs[k][1]))
