# t3_H2mono2.py: dH2/dA on full rectangle; H2(2pi/3, c); and dH2/dc at A=2pi/3
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar
def comps(A, c):
    t = c*A
    s2, c2 = sin(2*A), cos(2*A)
    st, ct = sin(2*t), cos(2*t)
    D = c*s2 - st
    u = A*s2/D
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    den = q + c*Phi
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(den*den)
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
    Gc = du*V + u*dH
    Phix = 2*(q*q-1)*sx*cx
    denx = c*Phix
    ux = (Phi + A*Phix)/den - A*Phi*denx/(den*den)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*den - 2*c*(q*q-1)*sx*cx*denx)/(den*den)
    Gx = ux*V + u*(Hx - A0x)
    return u, G, Gc, Gx, q, V

h = mpf('2e-6')
random.seed(3)
loA = 1e30; argmin = None
for _ in range(800):
    A = Amin + mpf(random.random())*(Amax-Amin)
    c = mpf('0.4') + mpf(random.random())*mpf('0.1')
    u0,_,_,Gx0,_,_ = comps(A,c)
    u1,_,_,Gx1,_,_ = comps(A+h,c)
    dA = (u1*Gx1 - u0*Gx0)/h
    if dA < loA: loA = dA; argmin=(float(A),float(c))
print('dH2/dA min over full rectangle: %.4f at (A,c)=(%.4f,%.3f)' % (loA, argmin[0], argmin[1]))
print('H2(2pi/3, c) for c in [0.4,0.5]:')
for c in [mpf(x)/100 for x in range(40,51)]:
    u,G,Gc,Gx,q,V = comps(Amin, c)
    print('  c=%.2f: u=%.5f Gx=%.5f H2=%.5f q=%.4f' % (float(c), u, Gx, u*Gx, q))
