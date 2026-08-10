# -*- coding: utf-8 -*-
"""Map dJ2/dq|g > 0 region precisely; check J values there."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
def Delta(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return A_*mp.sin(t_)*mp.cos(t_) + t_*mp.sin(g)*mp.cos(g)
def Jv(g, q): return NJ(g, q)/(16*Delta(g,q)**4)
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-7')
N = 120
pos = []
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        dq = (NJ(g, q+h)-NJ(g, q-h))/(2*h)
        if dq > 0: pos.append((float(g), float(q), float(dq), float(Jv(g, q))))
print('dNJ/dq>0 samples: %d/%d' % (len(pos), (N+1)**2))
if pos:
    print('region: g in [%.4f, %.4f], q in [%.4f, %.4f]' % (min(p[0] for p in pos), max(p[0] for p in pos), min(p[1] for p in pos), max(p[1] for p in pos)))
    print('J values in region: [%.4f, %.4f]' % (min(p[3] for p in pos), max(p[3] for p in pos)))
    # J on q=1 line for same gamma range
    gs = sorted(set(p[0] for p in pos))
    print('J(g,1) for g at region edges: J(%.4f,1)=%.4f, J(%.4f,1)=%.4f' % (gs[0], Jv(gs[0],1), gs[-1], Jv(gs[-1],1)))
