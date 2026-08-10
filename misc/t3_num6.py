# -*- coding: utf-8 -*-
"""t3_num6: numerators via together(v*denom) WITHOUT pre-expanding v."""
import sympy as sp
import pickle, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
P = 2*(A*st*ct + t*sg*cg)
p = A*st*ct + t*sg*cg
q2m1 = (cg**2-ct**2)/(sg**2*ct**2)
Phi  = cg**2/ct**2
Phi_x= -2*q2m1*sg*cg
W    = 3 - 2*A*cg/sg
W_x  = -2*cg/sg - 2*A/sg**2
sc_  = -sg*cg
cos2x= cg**2 - sg**2
c    = t/A
K    = cg/(2*A*sg*ct**2)
D, D2, D3 = P*K, (P*K)**2, (P*K)**3
G  = (4*A**2*cg**2 - 6*A*sg*cg)/P - 8*A**2*t*sg*cg*(cg**2-ct**2)/P**2
Gc = (12*A**2*sg**2*cg**2 - 8*A**3*sg*cg*(2*cg**2-ct**2))/P**2 + 32*A**3*t*sg**2*cg**2*(cg**2-ct**2)/P**3
u  = 2*A**2*sg*cg/P
t1 = -(Phi_x*W + Phi*W_x)/D
t2 = Phi*W*c*Phi_x/D2
t3 = 2*c*(Phi*q2m1*sc_ + A*Phi_x*q2m1*sc_ + A*Phi*q2m1*cos2x)/D2
t4 = -4*c**2*A*Phi*Phi_x*q2m1*sc_/D3
den_extra = cg**3*sg**3*ct**6
GxP3c = sum(sp.expand(tt*P**3*den_extra) for tt in [t1,t2,t3,t4])
Gx = GxP3c/(P**3*den_extra)

def d_dt(f): return sp.diff(f, t) + ct*sp.diff(f, st) - st*sp.diff(f, ct)
def d_dg(f): return -sp.diff(f, A) + cg*sp.diff(f, sg) - sg*sp.diff(f, cg)
dG_dt = d_dt(G); dG_dg = d_dg(G); dGc_dt = d_dt(Gc); dGc_dg = d_dg(Gc); dGx_dt = d_dt(Gx); dGx_dg = d_dg(Gx)

specs = {
 'dG_dq':  (dG_dt,                                        p**3),
 'dG_dg':  (dG_dg + dG_dt*st*ct/(sg*cg),                  sg*p**3),
 'dGc_dq': (dGc_dt,                                       p**4),
 'dGc_dg': (dGc_dg + dGc_dt*st*ct/(sg*cg),                p**4),
 'dGx_dq': (dGx_dt,                                       ct*sg*p**4),
 'dGx_dg': (dGx_dg + dGx_dt*st*ct/(sg*cg),                cg*sg**2*p**4),
}
atoms = [A,t,sg,cg,st,ct]
res = {}
for k,(v, denom) in specs.items():
    nn = sp.expand(sp.together(v*denom))
    poly = sp.Poly(nn, *atoms)
    coeffs = poly.coeffs(); monoms = poly.monoms()
    pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
    res[k] = {'nterms': len(monoms), 'deg': poly.total_degree(),
              'pos': len(pos), 'neg': len(neg), 'maxpos': int(max(pos)) if pos else 0, 'minneg': int(min(neg)) if neg else 0,
              'monoms': [list(m) for m in monoms], 'coeffs': [str(c) for c in coeffs]}
    print('%-8s: n=%d deg=%d pos=%d neg=%d maxpos=%d minneg=%d' % (k, len(monoms), poly.total_degree(), len(pos), len(neg), max(pos) if pos else 0, min(neg) if neg else 0))

with open('misc/t3_num6.json','w',encoding='utf-8') as fh: json.dump(res, fh, ensure_ascii=False)
with open('misc/t3_num6.pkl','wb') as fh: pickle.dump({'res': res, 'comp': {k: v[0] for k,v in specs.items()}, 'denom': {k: v[1] for k,v in specs.items()}}, fh)
print('saved misc/t3_num6.json/.pkl')
