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
h = mp.mpf('1e-6')
N = 80
# count sign patterns of (dNJ/dg, dNJ/dq)
import collections
cnt = collections.Counter()
cells = []
for i in range(N):
    g0 = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N):
        q0 = 1 + mp.mpf(j)/N
        g = g0 + (ghi-glo)/N/2; q = q0 + 1/N/2
        dg = (NJ(g+h,q)-NJ(g-h,q))/(2*h)
        dq = (NJ(g,q+h)-NJ(g,q-h))/(2*h)
        sgn = ('+' if dg>0 else '-') + ('+' if dq>0 else '-')
        cnt[sgn] += 1
print(cnt)
# locate W max
import numpy as np
best = (mp.mpf('1e30'), None)
for i in range(400+1):
    g = glo + mp.mpf(i)*(ghi-glo)/400
    for j in range(400+1):
        q = 1 + mp.mpf(j)/400
        v = NJ(g,q)
        if v > best[0]: best = (v, (float(g), float(q)))
print('NJ2 max %.6f at (g,q)=(%.4f,%.4f)' % (best[0], best[1][0], best[1][1]))
# NJ2 on the four edges
print('edges:')
for name, f in [('g=0.655', lambda q: NJ(mp.mpf('0.655'), q)), ('g=1.0472', lambda q: NJ(mp.pi/3, q)), ('q=1', lambda g: NJ(g, 1)), ('q=2', lambda g: NJ(g, 2))]:
    mn = mp.mpf('1e30'); mx = mp.mpf('-1e30')
    for i in range(200+1):
        if name.startswith('g'):
            v = f(1 + mp.mpf(i)/200)
        else:
            v = f(glo + mp.mpf(i)*(ghi-glo)/200)
        mn = min(mn, v); mx = max(mx, v)
    print('  %s: NJ2 in [%.4f, %.4f]' % (name, mn, mx))
