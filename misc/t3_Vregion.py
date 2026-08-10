# t3_Vregion.py: find V<0 region on T2, V range, |H|, A0 there; check margins for plan targets
import math
from mpmath import mp, mpf, cos, sin, tan, atan, pi as mppi
mp.dps = 30
gstar = mpf('0.65564932893873566325493245529469')
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
    return A, c, u, V, H, A0, G, Phi/den
loV = (mpf('1e30'), None); loG = (mpf('1e30'), None)
N=400
Vneg = []
for i in range(N+1):
    g = gstar + mpf(i)*(mppi/3-gstar)/N
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q < 1 or q > 2: continue
        A, c, u, V, H, A0, G, pD = comps(g,q)
        if V < loV[0]: loV = (V, (float(g),float(q),float(A),float(c)))
        if G < loG[0]: loG = (G, (float(g),float(q),float(A),float(c)))
        if V < 0: Vneg.append((float(g),float(q),float(A),float(c),float(V),float(H),float(A0)))
print('V min on T2: %.6f at (g,q,A,c)=(%s)' % (loV[0], loV[1]))
print('G min on T2: %.6f at (g,q,A,c)=(%s)' % (loG[0], loG[1]))
print('V<0 count:', len(Vneg), 'of', (N+1)**2)
if Vneg:
    print('V<0 range: V in [%.5f, 0), A in [%.4f, %.4f], |H| in [%.4f, %.4f], A0 in [%.4f, %.4f]' % (
        min(v[4] for v in Vneg), min(v[2] for v in Vneg), max(v[2] for v in Vneg),
        min(abs(v[5]) for v in Vneg), max(abs(v[5]) for v in Vneg),
        min(v[6] for v in Vneg), max(v[6] for v in Vneg)))
# check: is V >= -0.28 in V<0 region? is |V| <= 0.28?
print('min V in V<0 region:', min(v[4] for v in Vneg))
# margins check for the targets on T2
res = {'u':[mpf('1e30'),mpf('-1e30')], 'Gx':[mpf('1e30'),mpf('-1e30')], 'G':[mpf('1e30'),mpf('-1e30')], 'pD':[mpf('1e30'),mpf('-1e30')], 'V':[mpf('1e30'),mpf('-1e30')]}
for i in range(N+1):
    g = gstar + mpf(i)*(mppi/3-gstar)/N
    ql, qh = qlo(g), qhi(g)
    if qh < 1: continue
    ql = max(ql, mpf(1))
    for j in range(N+1):
        q = ql + mpf(j)*(qh-ql)/N
        if q < 1 or q > 2: continue
        A,c,u,V,H,A0,G,pD = comps(g,q)
        for k,v in [('u',u),('G',G),('pD',pD),('V',V)]:
            if v < res[k][0]: res[k][0]=v
            if v > res[k][1]: res[k][1]=v
for k in ['u','G','pD','V']:
    print('%s on T2: [%.5f, %.5f]' % (k, res[k][0], res[k][1]))
