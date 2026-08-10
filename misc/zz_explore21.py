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
h = mp.mpf('1e-7')
N = 200
neg = []
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        dg = (NJ(g+h,q)-NJ(g-h,q))/(2*h)
        if dg < 0: neg.append((float(g), float(q), float(dg)))
print('dNJ/dg < 0 count: %d' % len(neg))
if neg:
    print('region: g in [%.4f, %.4f], q in [%.4f, %.4f]' % (min(p[0] for p in neg), max(p[0] for p in neg), min(p[1] for p in neg), max(p[1] for p in neg)))
    neg.sort(key=lambda p: -p[2])
    for p in neg[:10]: print('  g=%.5f q=%.5f dNJ/dg=%.5f' % p)
# along q=1: dNJ/dg?
for j in [0, 40, 80, 120, 160, 200]:
    q = 1 + mp.mpf(j)/200
    vals = []
    for i in range(0, 201, 40):
        g = glo + mp.mpf(i)*(ghi-glo)/200
        dg = (NJ(g+h,q)-NJ(g-h,q))/(2*h)
        vals.append((float(g), float(dg)))
    print('q=%.3f: dNJ/dg at g=0.655,0.733,0.812,0.890,0.969,1.047: %s' % (q, ['%.2f'%v[1] for v in vals]))
