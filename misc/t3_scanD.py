# t3_scanD.py: scan region D (A,c): A in [2pi/3, pi-g*], c in [0.4,0.5], A(1+c)>=pi
# check monotonicity directions of u, Gx, H1=G^2+Gc, and J2
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar
def comps(A, c):
    t = c*A
    # u = A sin2A / (c sin2A - sin 2cA)
    s2, c2 = sin(2*A), cos(2*A)
    st, ct = sin(2*t), cos(2*t)
    D = c*s2 - st
    u = A*s2/D
    # q and Phi/D etc for G: use q = -tan t / tan A
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    # Gc = dG/dc at fixed (q, A)
    du = -A*Phi*Phi/(den*den)
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
    Gc = du*V + u*dH
    # Gx = dG/dx at fixed (q,c), x=A
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return u, G, Gc, Gx, q, V

rng = {k:[mpf('1e30'),mpf('-1e30')] for k in ['u','G','Gc','Gx','H1','H2','J2','q']}
for i in range(300):
    A = Amin + mpf(i)*(Amax-Amin)/300
    for j in range(300):
        c = mpf('0.4') + mpf(j)*(mpf('0.5')-mpf('0.4'))/300
        if A*(1+c) < mppi: continue
        u,G,Gc,Gx,q,V = comps(A,c)
        H1 = G*G+Gc; H2 = u*Gx; J2 = H1-H2
        for k,v in [('u',u),('G',G),('Gc',Gc),('Gx',Gx),('H1',H1),('H2',H2),('J2',J2),('q',q)]:
            if v < rng[k][0]: rng[k][0]=v
            if v > rng[k][1]: rng[k][1]=v
for k in ['u','G','Gc','Gx','H1','H2','J2','q']:
    print('%s: [%.6f, %.6f]' % (k, rng[k][0], rng[k][1]))
# directional checks at sample points: d/du in A (fixed c) and in c (fixed A)
import random
random.seed(1)
h = mpf('1e-5')
for _ in range(12):
    A = Amin + mpf(random.random())*(Amax-Amin)
    c = mpf('0.4') + mpf(random.random())*(mpf('0.5')-mpf('0.4'))
    if A*(1+c) < mppi: A = (mppi/c - A)*mpf('0.9999')  # push into region
    u0,G0,Gc0,Gx0,_,_ = comps(A,c)
    uA,_,_,GxA,_,_ = comps(A+h,c)
    uC,_,_,GxC,_,_ = comps(A,c+h)
    print('A=%.3f c=%.3f: du/dA=%.4f du/dc=%.4f | dGx/dA=%.4f dGx/dc=%.4f' % (
        float(A),float(c), float((uA-u0)/h), float((uC-u0)/h), float((GxA-Gx0)/h), float((GxC-Gx0)/h)))
