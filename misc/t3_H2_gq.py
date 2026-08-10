# t3_H2_gq.py: H2, u, Gx monotonicity in (gamma,q) on T2
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
glo, ghi = gstar, mppi/3
def qlo(g): return tan(mpf('0.4')*(mppi-g))/tan(g)
def qhi(g): return tan(mpf('0.5')*(mppi-g))/tan(g)
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
    return u, G, Gc, Gx

h = mpf('1e-6')
random.seed(9)
rows=[]
for _ in range(500):
    g = glo + mpf(random.random())*(ghi-glo)
    ql = max(qlo(g), mpf(1)); qh = min(qhi(g), mpf(2))
    if qh <= ql: continue
    q = ql + mpf(random.random())*(qh-ql)
    u0,G0,Gc0,Gx0 = comps(g,q)
    u1,G1,Gc1,Gx1 = comps(g+h,q)
    u2,G2,Gc2,Gx2 = comps(g,q+h)
    rows.append((float(g),float(q),float((u1*Gx1-u0*Gx0)/h),float((u2*Gx2-u0*Gx0)/h),
                 float((Gx1-Gx0)/h), float((Gx2-Gx0)/h), float((u1-u0)/h), float((u2-u0)/h)))
dH2dg = [r[2] for r in rows]; dH2dq=[r[3] for r in rows]
dGxdg=[r[4] for r in rows]; dGxdq=[r[5] for r in rows]
dudg=[r[6] for r in rows]; dudq=[r[7] for r in rows]
print('dH2/dg: [%.3f, %.3f]  dH2/dq: [%.3f, %.3f]' % (min(dH2dg),max(dH2dg),min(dH2dq),max(dH2dq)))
print('dGx/dg: [%.3f, %.3f]  dGx/dq: [%.3f, %.3f]' % (min(dGxdg),max(dGxdg),min(dGxdq),max(dGxdq)))
print('du/dg : [%.3f, %.3f]  du/dq : [%.3f, %.3f]' % (min(dudg),max(dudg),min(dudq),max(dudq)))
