# -*- coding: utf-8 -*-
"""t3_mono_xt.py: monotonicity of H2, Gx, H1, P1 in (x,th) coords on T2."""
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40
gstar = mpf('0.65564932893873566325493245529469')
xmin, xmax = 2*mppi/3, mppi - gstar

def comps(x, th):
    s, b = sin(x), -cos(x)
    S, C = sin(th), cos(th)
    q = S*b/(C*s)
    D = b*s*th + C*S*x
    u = b*s*x*x/D
    A0 = mpf(3)/x - 2*b/s
    H = 2*th*(C*C*s*s - S*S*b*b)/D
    V = H - A0
    G = u*V
    # Gc via sympy form (closed): use formula Gc = b s x^2 (C^2+S^2)*Nc/D^3
    # easier: recompute via components as before
    Phi = b*b/(C*C)
    du = -x*Phi*Phi/(D*D)
    dH = -2*(S*S*b*b/(C*C*s*s)-1)*s*b*q/(D*D)*1  # placeholder
    # use direct derivative formulas (as in t3_J2_components)
    Phix = -2*s*b*(q*q-1)
    ux = (Phi + x*Phix)/D - x*Phi*x*0  # careful: D depends on x through Phi only (q,p const in partial x)
    # partial_x at fixed (q,p): Phi = q^2 s^2 + b^2, dPhi/dx = 2q^2 s(-b) + 2b s = 2bs(1-q^2)
    Phix = 2*s*b*(1-q*q)
    Dx = (th/x)*Phix
    ux = (Phi + x*Phix)/D - x*Phi*Dx/(D*D)
    A0x = -3/(x*x) - 2/(s*s)
    Hx = -2*(th/x)*(q*q-1)*((s*s-b*b)*D - s*b*Dx)/(D*D)
    Gx = ux*V + u*(Hx - A0x)
    H1 = G*G + u*V*0 + (-x*Phi*Phi/(D*D))*V + u*(-2*(q*q-1)*s*b*q/(D*D))
    # Gc = dG/dp at fixed (x,q): p=th/x
    Gc = (-x*Phi*Phi/(D*D))*V + u*(-2*(q*q-1)*s*b*q/(D*D))
    H1 = G*G + Gc
    P1 = x*Phi*Phi*(x*V*V - V)/(D*D)
    return q, u, V, G, Gc, Gx, H1, u*Gx, P1

h = mpf('1e-6')
random.seed(3)
stats = {k: [1e30, -1e30] for k in ['dH2dx','dH2dth','dGxdx','dGxdth','dH1dx','dH1dth','dP1dx','dP1dth','du_dx','du_dth']}
cnt = 0
for _ in range(800):
    x = xmin + mpf(random.random())*(xmax-xmin)
    th_min = max(mpf('0.4')*x, mppi - x)
    th_q2 = atan(-2*tan(x))
    th_max = min(mpf('0.5')*x, th_q2)
    if th_max <= th_min: continue
    th = th_min + mpf(random.random())*(th_max-th_min)
    q0,u0,V0,G0,Gc0,Gx0,H10,H20,P10 = comps(x,th)
    if q0 < 1 or q0 > 2: continue
    cnt += 1
    q1,u1,V1,G1,Gc1,Gx1,H11,H21,P11 = comps(x+h,th)
    q2,u2,V2,G2,Gc2,Gx2,H12,H22,P12 = comps(x,th+h)
    vals = {'dH2dx':(H21-H20)/h,'dH2dth':(H22-H20)/h,'dGxdx':(Gx1-Gx0)/h,'dGxdth':(Gx2-Gx0)/h,
            'dH1dx':(H11-H10)/h,'dH1dth':(H12-H10)/h,'dP1dx':(P11-P10)/h,'dP1dth':(P12-P10)/h,
            'du_dx':(u1-u0)/h,'du_dth':(u2-u0)/h}
    for k,v in vals.items():
        if v < stats[k][0]: stats[k][0]=v
        if v > stats[k][1]: stats[k][1]=v
print('samples:', cnt)
for k in stats: print('%s: [%.4f, %.4f]' % (k, stats[k][0], stats[k][1]))
