# t3_H1cA.py: H1 as function of c at fixed A over D
import math
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
    den = q + c*Phi
    u = A*Phi/den
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/den
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(den*den)
    dH = 2*(q*q-1)*sx*cx/den - 2*c*(q*q-1)*sx*cx*Phi/(den*den)
    Gc = du*V + u*dH
    return G, Gc
for Av in [2.1, 2.2, 2.3, 2.4, 2.45, 2.486]:
    print('A=%.3f:' % Av)
    for c in [mpf(x)/100 for x in range(40,51)]:
        if mpf(str(Av))*(1+c) < mppi: continue
        G, Gc = comps(mpf(str(Av)), c)
        print('   c=%.2f G=%.4f Gc=%.4f H1=%.4f' % (float(c), G, Gc, G*G+Gc))
