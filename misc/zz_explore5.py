import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
best = (mp.mpf('-1e30'), None); bq = None
for i in range(500+1):
    g = glo + mp.mpf(i)*(ghi-glo)/500
    for j in range(500+1):
        q = 1 + mp.mpf(j)/500
        v = NJ(g,q)
        if v > best[0]: best = (v, (float(g), float(q)))
print('NJ2 max %.6f at (g,q)=(%.5f,%.5f)' % (best[0], best[1][0], best[1][1]))
# also W max (W=NJ2/(32A^2 cg))
def Wv(g,q):
    A_ = mp.pi-g
    return NJ(g,q)/(32*A_**2*mp.cos(g))
bestW = (mp.mpf('-1e30'), None)
for i in range(300+1):
    g = glo + mp.mpf(i)*(ghi-glo)/300
    for j in range(300+1):
        q = 1 + mp.mpf(j)/300
        v = Wv(g,q)
        if v > bestW[0]: bestW = (v, (float(g), float(q)))
print('W max %.6f at (g,q)=(%.5f,%.5f)' % (bestW[0], bestW[1][0], bestW[1][1]))
# NJ2 along top edge g=1.0472
mn = mp.mpf('1e30'); mx = mp.mpf('-1e30'); argmx = None
for j in range(400+1):
    q = 1 + mp.mpf(j)/400
    v = NJ(ghi, q)
    if v > mx: mx, argmx = v, float(q)
    mn = min(mn, v)
print('top edge g=1.0472: NJ2 in [%.4f, %.4f], max at q=%.4f' % (mn, mx, argmx))
