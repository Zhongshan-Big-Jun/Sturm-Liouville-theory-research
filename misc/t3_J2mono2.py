# -*- coding: utf-8 -*-
"""t3_J2mono2.py: monotonicity of J2_2d itself on T2 in (g,q), (x,c), (x,th)."""
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')

def comps_gq(g, q):
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
    A0x = -3/(A*A) - 2/(sx*sx)
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return G*G + Gc - u*Gx

def comps_xc(x, c):
    t = c*x
    q = -tan(t)/tan(x)
    s, b = sin(x), -cos(x)
    S, C = sin(t), cos(t)
    Phi = b*b/(C*C)
    den = q + c*Phi
    u = x*Phi/den
    A0 = mpf(3)/x - 2*b/s
    H = 2*c*(q*q-1)*s*(-b)/den
    V = H - A0
    G = u*V
    du = -x*Phi*Phi/(den*den)
    dH = 2*q*(q*q-1)*s*(-b)/(den*den)
    Gc = du*V + u*dH
    Phix = -2*s*b*(q*q-1)
    denx = c*Phix
    ux = (Phi + x*Phix)/den - x*Phi*denx/(den*den)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = (2*c*(q*q-1)*((-b)**2 - s*s)*den - 2*c*(q*q-1)*s*(-b)*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return G*G + Gc - u*Gx, q

def inT2x(x, c):
    t = c*x
    q = -tan(t)/tan(x)
    return q >= 1 and q <= 2 and c >= mpf('0.4') and c <= mpf('0.5')

h = mpf('1e-6')
random.seed(11)
stats = {}
xmin, xmax = 2*mppi/3, mppi-gstar
rows=[]
for _ in range(600):
    x = xmin + mpf(random.random())*(xmax-xmin)
    c = mpf('0.4') + mpf(random.random())*mpf('0.1')
    if not inT2x(x, c): continue
    J0,q0 = comps_xc(x,c)
    J1,_ = comps_xc(x+h,c); J2,q2 = comps_xc(x,c+h)
    rows.append((float(x),float(c),float((J1-J0)/h),float((J2-J0)/h)))
for k, idx in [('dJ/dx',2),('dJ/dc',3)]:
    v = [r[idx] for r in rows]
    print('%s: [%.3f, %.3f]' % (k, min(v), max(v)))
# also dJ/dq at fixed gamma
def inT2g(g,q):
    return q >= 1 and q <= 2 and (g >= gstar) and (g <= mppi/3) and \
        q >= tan(mpf('0.4')*(mppi-g))/tan(g) and q <= tan(mpf('0.5')*(mppi-g))/tan(g)
rows2=[]
for _ in range(600):
    g = gstar + mpf(random.random())*(mppi/3-gstar)
    ql = max(tan(mpf('0.4')*(mppi-g))/tan(g), mpf(1))
    qh = min(tan(mpf('0.5')*(mppi-g))/tan(g), mpf(2))
    if qh <= ql: continue
    q = ql + mpf(random.random())*(qh-ql)
    J0 = comps_gq(g,q); J1 = comps_gq(g+h,q); J2 = comps_gq(g,q+h)
    rows2.append((float(g),float(q),float((J1-J0)/h),float((J2-J0)/h)))
for k, idx in [('dJ/dg',2),('dJ/dq',3)]:
    v = [r[idx] for r in rows2]
    print('%s: [%.3f, %.3f]' % (k, min(v), max(v)))
