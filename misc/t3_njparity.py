# -*- coding: utf-8 -*-
"""t3_njparity: parity decomposition of NJ itself."""
import sympy as sp, json, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
NJr = sp.expand(NJ)
for _ in range(10):
    NJr = sp.expand(NJr.subs(st**2, 1-ct**2))
w = sp.symbols('w', positive=True)
v, u = sp.symbols('v u', positive=True)
E2 = sp.expand(NJr.subs({ct**2: v**2, ct: v, st: u}))
E0 = sp.expand(E2.subs(u, 0))
E1 = sp.expand((E2 - E0)/u)
E0e = sp.expand(E0.subs(v, 0)); E0o = sp.expand((E0-E0e)/v)
E1e = sp.expand(E1.subs(v, 0)); E1o = sp.expand((E1-E1e)/v)
def to_w(expr):
    e = sp.expand(expr)
    return sp.expand(e.subs(v**2, w))
N0 = to_w(E0e); N1 = to_w(E0o); N2 = to_w(E1e); N3 = to_w(E1o)
print('N0 terms:', len(sp.Add.make_args(N0)))
print('N1 terms:', len(sp.Add.make_args(N1)))
print('N2 terms:', len(sp.Add.make_args(N2)))
print('N3 terms:', len(sp.Add.make_args(N3)))
# NJ = N0 + v*N1 + u*N2 + u*v*N3 = N0 + sqrt(w)*N1 + sqrt(1-w)*N2 + sqrt(w(1-w))*N3
recon = N0 + sp.sqrt(w)*N1 + sp.sqrt(1-w)*N2 + sp.sqrt(w*(1-w))*N3
print('recon == NJr?', sp.expand(sp.expand(recon - NJr)) == 0)
with open('misc/t3_NJ_parity.pkl','wb') as fh: pickle.dump({'N0':N0,'N1':N1,'N2':N2,'N3':N3}, fh)
print('N2 =', sp.factor(N2))
print('N1 =', sp.factor(N1))
