# t3_box_mono2.py: monotonicity of H2, Gx, P1, H1 on full box [gstar, pi/3] x [1,2] in (g,q)
import math, random
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
    return H1, H2, Gx, P1
h = mpf('2e-6')
random.seed(21)
res = {k:[mpf('1e30'),mpf('-1e30')] for k in ['H2dg','H2dq','Gxdg','Gxdq','P1dg','P1dq','H1dg','H1dq']}
for _ in range(1200):
    g = glo + mpf(random.random())*(ghi-glo)
    q = mpf(1) + mpf(random.random())
    H1,H2,Gx,P1 = comps(g,q)
    H1a,H2a,Gxa,P1a = comps(g+h,q)
    H1b,H2b,Gxb,P1b = comps(g,q+h)
    vals = {'H2dg':(H2a-H2)/h,'H2dq':(H2b-H2)/h,'Gxdg':(Gxa-Gx)/h,'Gxdq':(Gxb-Gx)/h,
            'P1dg':(P1a-P1)/h,'P1dq':(P1b-P1)/h,'H1dg':(H1a-H1)/h,'H1dq':(H1b-H1)/h}
    for k,v in vals.items():
        if v < res[k][0]: res[k][0]=v
        if v > res[k][1]: res[k][1]=v
for k in ['H2dg','H2dq','Gxdg','Gxdq','P1dg','P1dq','H1dg','H1dq']:
    print('%s: [%.3f, %.3f]' % (k, res[k][0], res[k][1]))
