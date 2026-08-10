# -*- coding: utf-8 -*-
"""Re-scan M1'-M3' derivative signs with CORRECT Gc, in (gamma,q) coords on T2."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 50

def comps_gq(g, q):
    A = mppi - g
    t = atan(q*tan(g)); c = t/A
    x = A; th = t
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    Phi = b*b/(C*C)
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
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*b*q/(den*den))
    return dict(G=G, Gc=Gc, Gx=Gx, u=u)

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
h = mpf('1e-7')
def qlo(g): return max(mpf(1), tan(mpf('0.4')*(mppi-g))/tan(g))
def qhi(g): return min(mpf(2), tan(mpf('0.5')*(mppi-g))/tan(g))

fields = ['G','Gc','Gx']
drd = {f: {'dg': [mpf('1e30'), mpf('-1e30')], 'dq': [mpf('1e30'), mpf('-1e30')]} for f in fields}
N = 150
for i in range(N+1):
    g = glo + mpf(i)*(ghi-glo)/N
    ql, qh = qlo(g), qhi(g)
    if qh <= ql: continue
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q <= ql or q >= qh: continue
        r0 = comps_gq(g, q)
        rg = comps_gq(g+h, q); rq = comps_gq(g, q+h)
        for f in fields:
            dg = (rg[f]-r0[f])/h; dq = (rq[f]-r0[f])/h
            drd[f]['dg'][0] = min(drd[f]['dg'][0], dg); drd[f]['dg'][1] = max(drd[f]['dg'][1], dg)
            drd[f]['dq'][0] = min(drd[f]['dq'][0], dq); drd[f]['dq'][1] = max(drd[f]['dq'][1], dq)
for f in fields:
    print('%s: d/dg in [%.4f, %.4f], d/dq in [%.4f, %.4f]' % (f, drd[f]['dg'][0], drd[f]['dg'][1], drd[f]['dq'][0], drd[f]['dq'][1]))
