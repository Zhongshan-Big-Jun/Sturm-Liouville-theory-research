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
N = 160
print('dNJ/dq < 0 region mapping (g -> q-intervals where negative):')
for i in range(0, 161, 16):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    negs = []
    inneg = False; start = None
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        s = (NJ(g,q+h)-NJ(g,q-h))/(2*h) < 0
        if s and not inneg: start, inneg = j, True
        if not s and inneg: negs.append((float(1+mp.mpf(start)/N), float(1+mp.mpf(j-1)/N))); inneg = False
    if inneg: negs.append((float(1+mp.mpf(start)/N), 2.0))
    print('  g=%.4f: %s' % (g, negs))
