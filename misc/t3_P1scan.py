# t3_P1scan.py: scan P1 = A*Phi^2*(A*V^2 - V)/D^2 over T2; verify H1 = P1 + N1
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
    D = q + c*Phi
    u = A*Phi/D
    A0 = mpf(3)/A + 2*cx/sx
    H = 2*c*(q*q-1)*sx*cx/D
    V = H - A0
    G = u*V
    du = -A*Phi*Phi/(D*D)
    dH = 2*(q*q-1)*sx*cx/D - 2*c*(q*q-1)*sx*cx*Phi/(D*D)
    Gc = du*V + u*dH
    H1 = G*G + Gc
    P1 = A*Phi*Phi*(A*V*V - V)/(D*D)
    N1 = A*Phi*q*H/(c*D*D)
    return H1, P1, N1, V, q
best = (mpf('-1e30'), None); worst=(mpf('1e30'),None)
N=400
for i in range(N+1):
    A = Amin + mpf(i)*(Amax-Amin)/N
    for j in range(N+1):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/N
        if A*(1+c) < mppi: continue
        H1, P1, N1, V, q = comps(A,c)
        if q > 2: continue  # restrict to T2
        if abs(H1 - (P1+N1)) > mpf('1e-12'):
            print('MISMATCH', float(A), float(c), float(H1), float(P1+N1)); raise SystemExit
        if P1 > best[0]: best = (P1, (float(A), float(c)))
        if P1 < worst[0]: worst = (P1, (float(A), float(c)))
print('P1 max on T2: %.8f at (A,c)=(%.5f,%.4f)' % (best[0], best[1][0], best[1][1]))
print('P1 min on T2: %.8f at (A,c)=(%.5f,%.4f)' % (worst[0], worst[1][0], worst[1][1]))
# check V range on T2
loV, hiV = mpf('1e30'), mpf('-1e30')
for i in range(N+1):
    A = Amin + mpf(i)*(Amax-Amin)/N
    for j in range(N+1):
        c = mpf('0.4') + mpf(j)*mpf('0.1')/N
        if A*(1+c) < mppi: continue
        H1, P1, N1, V, q = comps(A,c)
        if q > 2: continue
        if V < loV: loV=V
        if V > hiV: hiV=V
print('V range on T2: [%.5f, %.5f]' % (loV, hiV))
