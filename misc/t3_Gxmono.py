# t3_Gxmono.py: dGx/dA on full rectangle; Gx(2pi/3,c); Gx(2pi/3,c) min
import math, random
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30

gstar = mpf('0.65564932893873566325493245529469')
Amin = 2*mppi/3
Amax = mppi - gstar
def comps(A, c):
    t = c*A
    q = -tan(t)/tan(A)
    sx, cx = sin(A), cos(A)
    Phi = q*q*sx*sx + cx*cx
    D = q + c*Phi
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/D
    V = H - A0
    u = A*Phi/D
    Phix = 2*(q*q-1)*sx*cx
    ux = (Phi + A*Phix)/D - A*Phi*c*Phix/(D*D)
    A0x = -3/(A*A) - 2/sx**2
    Hx = (2*c*(q*q-1)*(cx*cx - sx*sx)*D - 2*c*(q*q-1)*sx*cx*c*Phix)/(D*D)
    Gx = ux*V + u*(Hx - A0x)
    return u, Gx

h = mpf('2e-6')
random.seed(5)
lo = 1e30; arg = None
for _ in range(1000):
    A = Amin + mpf(random.random())*(Amax-Amin)
    c = mpf('0.4') + mpf(random.random())*mpf('0.1')
    u0,Gx0 = comps(A,c)
    u1,Gx1 = comps(A+h,c)
    d = (Gx1-Gx0)/h
    if d < lo: lo=d; arg=(float(A),float(c))
print('dGx/dA min over full rectangle: %.4f at (A,c)=(%.4f,%.3f)' % (lo,arg[0],arg[1]))
print('Gx(2pi/3, c):')
for c in [mpf(x)/100 for x in range(40,51)]:
    u,Gx = comps(Amin,c)
    print('  c=%.2f: Gx=%.6f' % (float(c),Gx))
