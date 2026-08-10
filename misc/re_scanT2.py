# -*- coding: utf-8 -*-
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
    G = u*V
    Gx = ux*V + u*(Hx - A0x)
    Gc = (-x*Phi*Phi/(den*den))*V + u*(-2*(q*q-1)*s*(-b)*q/(den*den))
    return dict(q=q, c=c, u=u, G=G, Gx=Gx, Gc=Gc, J=G*G+Gc-u*Gx)

gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi-gstar
N = 200
R = {k: [mpf('1e30'), mpf('-1e30'), None, None] for k in ['G','Gc','Gx','u','uGx','H1','J']}
cnt = 0
for i in range(N+1):
    x = xmin + mpf(i)*(xmax-xmin)/N
    th_lo = max(2*x/5, mppi-x); th_hi = min(x/2, atan(-2*tan(x)))
    if th_lo >= th_hi: continue
    for j in range(-1, N+2):
        if j < 0: th = th_lo
        elif j > N: th = th_hi
        else: th = th_lo + mpf(j)*(th_hi-th_lo)/N
        if th < th_lo or th > th_hi: continue
        cnt += 1
        r = comps(x, th)
        vals = {'G': r['G'], 'Gc': r['Gc'], 'Gx': r['Gx'], 'u': r['u'],
                'uGx': r['u']*r['Gx'], 'H1': r['G']**2 + r['Gc'], 'J': r['J']}
        for k in vals:
            if vals[k] < R[k][0]: R[k][0], R[k][2] = vals[k], (float(x), float(th), float(r['q']), float(r['c']))
            if vals[k] > R[k][1]: R[k][1], R[k][3] = vals[k], (float(x), float(th), float(r['q']), float(r['c']))
print('samples:', cnt)
for k in ['G','Gc','Gx','u','uGx','H1','J']:
    print('%s: min=%.6f at %s ; max=%.6f at %s' % (k, R[k][0], R[k][2], R[k][1], R[k][3]))
