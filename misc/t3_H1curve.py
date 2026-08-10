# t3_H1curve.py: H1 along c=0.4 boundary and near corner; also V=0 curve location
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 40

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
    return u, G, Gc, q, V, A0, H

print('H1 along c=0.4:')
for A in [mpf(x)/1000 for x in range(2150, 2500, 25)]:
    if A*(1.4) < mppi: continue
    u,G,Gc,q,V,A0,H = comps(A, mpf('0.4'))
    print('  A=%.3f: G=%.4f Gc=%.4f H1=%.4f q=%.4f V=%.4f A0=%.4f H=%.4f' % (float(A),G,Gc,G*G+Gc,q,V,A0,H))
print('V=0 search along c=0.4, 0.45, 0.5:')
for c in [mpf('0.4'), mpf('0.45'), mpf('0.5')]:
    lo, hi = mpf('2.15'), mpf('2.49')
    for _ in range(80):
        mid = (lo+hi)/2
        u,G,Gc,q,V,_,_ = comps(mid, c)
        if V < 0: lo = mid
        else: hi = mid
    u,G,Gc,q,V,_,_ = comps(hi, c)
    print('  c=%.2f: V=0 at A=%.5f (q=%.4f, G=%.4f, Gc=%.4f, H1=%.4f)' % (float(c), float(hi), q, G, Gc, G*G+Gc))
