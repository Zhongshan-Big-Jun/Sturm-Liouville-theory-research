# -*- coding: utf-8 -*-
"""Fine subregion scans: rectangle-based Gx lower bounds for various splits."""
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
    return dict(q=q, c=c, u=u, ux=ux, V=V, Hx=Hx, p3=-u*A0x, Gx=Gx)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 200

def scan(xlo, xhi):
    R = {k: [mpf('1e30'), mpf('-1e30')] for k in ['u','ux','V','Hx','p3','Gx']}
    for i in range(N+1):
        x = xmin + mpf(i)*(xmax-xmin)/N
        if x < xlo or x > xhi: continue
        th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
        if th_lo >= th_hi: continue
        for j in range(-1, N+2):
            th = th_lo + mpf(j)*(th_hi-th_lo)/N if (0 <= j <= N) else (th_lo if j<0 else th_hi)
            if th < th_lo or th > th_hi: continue
            r = comps(x, th)
            for k in R:
                if r[k] < R[k][0]: R[k][0] = r[k]
                if r[k] > R[k][1]: R[k][1] = r[k]
    return R

for (xlo, xhi) in [(xmin, mpf('2.1')), (xmin, mpf('2.15')), (xmin, mpf('2.2')), (mpf('2.1'), mpf('2.25')), (mpf('2.15'), mpf('2.25')), (mpf('2.2'), mpf('2.3')), (mpf('2.25'), xmax), (mpf('2.3'), xmax)]:
    R = scan(xlo, xhi)
    # rectangle lower bound: p1 >= min(ux_min*V_max, ux_max*V_min), p2 >= min over u*Hx corners
    p1lb = min(R['ux'][0]*R['V'][1], R['ux'][1]*R['V'][0], R['ux'][0]*R['V'][0], R['ux'][1]*R['V'][1])
    p2lb = min(R['u'][0]*R['Hx'][1], R['u'][1]*R['Hx'][0], R['u'][0]*R['Hx'][0], R['u'][1]*R['Hx'][1])
    Gx_lb = R['p3'][0] + p1lb + p2lb
    print('x in [%.3f, %.3f]: u[%.3f,%.3f] ux[%.3f,%.3f] V[%.3f,%.3f] Hx[%.3f,%.3f] p3[%.3f,%.3f]' % (float(xlo), float(xhi), R['u'][0], R['u'][1], R['ux'][0], R['ux'][1], R['V'][0], R['V'][1], R['Hx'][0], R['Hx'][1], R['p3'][0], R['p3'][1]))
    print('    p1>%.3f p2>%.3f Gx>%.4f (true min %.4f)' % (p1lb, p2lb, Gx_lb, R['Gx'][0]))
