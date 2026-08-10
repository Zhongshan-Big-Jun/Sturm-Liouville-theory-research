# t3_derivmap.py: locate near-zero points of dH2/dg, dGx/dg, dP1/dA etc on full box
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30
gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def comps(g, q):
    A = mppi-g; t = atan(q*tan(g)); c = t/A
    sx, cx = sin(g), -cos(g)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    u = A*Phi/den
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*sx*cx/(den*den)
    Gc = du*V + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    H1 = G*G+Gc; H2 = u*Gx
    P1 = u*(Phi/den)*(A*V*V - V)
    return dict(u=u,G=G,Gc=Gc,Gx=Gx,H1=H1,H2=H2,P1=P1,V=V)
h = mpf('2e-6')
targets = ['H2','Gx','P1','H1','u']
res = {}
for k in targets:
    res[k+'dg'] = [mpf('1e30'), None]
    res[k+'dq'] = [mpf('1e30'), None]
N = 250
for i in range(N+1):
    g = glo + mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = mpf(1) + mpf(j)/N
        d0 = comps(g,q)
        da = comps(g+h,q); db = comps(g,q+h)
        for k in targets:
            vg = (da[k]-d0[k])/h; vq = (db[k]-d0[k])/h
            if vg < res[k+'dg'][0]: res[k+'dg'] = [vg, (float(g),float(q))]
            if vq < res[k+'dq'][0]: res[k+'dq'] = [vq, (float(g),float(q))]
for k in targets:
    print('%s: d/dg min %.4f at (g,q)=(%.4f,%.3f); d/dq min %.4f at (g,q)=(%.4f,%.3f)' % (
        k, res[k+'dg'][0], res[k+'dg'][1][0], res[k+'dg'][1][1], res[k+'dq'][0], res[k+'dq'][1][0], res[k+'dq'][1][1]))
# also max of P1 and H1 over full box
mx = {}
for i in range(N+1):
    g = glo + mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = mpf(1) + mpf(j)/N
        d0 = comps(g,q)
        for k in ['P1','H1','u','V']:
            v = d0[k]
            if k not in mx or v > mx[k][0]: mx[k] = (v,(float(g),float(q)))
for k in ['P1','H1','u','V']:
    print('%s max on box: %.5f at (g,q)=(%.4f,%.3f)' % (k, mx[k][0], mx[k][1][0], mx[k][1][1]))
