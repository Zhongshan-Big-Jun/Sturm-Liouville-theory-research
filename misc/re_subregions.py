# -*- coding: utf-8 -*-
"""Component ranges on subregions of T2 (x<=x0, x>=x0) for the p1+p2+p3 decomposition."""
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi, sqrt
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
    Gx = ux*V + u*(Hx - A0x)
    return dict(q=q, c=c, u=u, ux=ux, V=V, Hx=Hx, p1=ux*V, p2=u*Hx, p3=-u*A0x, Gx=Gx)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 150
for x0 in [mpf('2.25'), mpf('2.3'), mpf('2.35')]:
    print('=== subregion x %s %s ===' % ('>=' if x0 else '', float(x0)))
    for side in ['lo','hi']:
        R = {k: [mpf('1e30'), mpf('-1e30')] for k in ['p1','p2','p3','Gx','ux','V','Hx','u']}
        for i in range(N+1):
            x = xmin + mpf(i)*(xmax-xmin)/N
            if side=='lo' and x < x0: continue
            if side=='hi' and x > x0: continue
            th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
            if th_lo >= th_hi: continue
            for j in range(-1, N+2):
                th = th_lo + mpf(j)*(th_hi-th_lo)/N if (0 <= j <= N) else (th_lo if j<0 else th_hi)
                if th < th_lo or th > th_hi: continue
                r = comps(x, th)
                for k in R:
                    if r[k] < R[k][0]: R[k][0] = r[k]
                    if r[k] > R[k][1]: R[k][1] = r[k]
        tag = 'x>=' + str(float(x0)) if side=='lo' else 'x<=' + str(float(x0))
        print('  %s: p1[%.3f,%.3f] p2[%.3f,%.3f] p3[%.3f,%.3f] Gx[%.4f,%.4f]' % (tag, R['p1'][0], R['p1'][1], R['p2'][0], R['p2'][1], R['p3'][0], R['p3'][1], R['Gx'][0], R['Gx'][1]))
        print('      ux[%.3f,%.3f] V[%.3f,%.3f] Hx[%.3f,%.3f] u[%.3f,%.3f]' % (R['ux'][0], R['ux'][1], R['V'][0], R['V'][1], R['Hx'][0], R['Hx'][1], R['u'][0], R['u'][1]))
