# -*- coding: utf-8 -*-
"""t3_verify_all: full pipeline verification for NJ2, dNJ2/dt, B2, P05."""
import sympy as sp, json, math, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)

with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

# --- dNJ2/dt (total derivative along st=sin t, ct=cos t) ---
dNJ2dt = sp.expand(sp.diff(NJ2, t) + ct*sp.diff(NJ2, st) - st*sp.diff(NJ2, ct))
dNJ2r = sp.expand(dNJ2dt)
for _ in range(10):
    dNJ2r = sp.expand(dNJ2r.subs(st**2, 1-ct**2))
w = sp.symbols('w', positive=True)
E = sp.expand(dNJ2r.subs({ct: sp.sqrt(w), st: sp.sqrt(1-w)}))
E = sp.expand(E)

P0 = sp.Integer(0); Pw = sp.Integer(0); P1 = sp.Integer(0); Pw1 = sp.Integer(0)
sw_ = sp.sqrt(w); s1w = sp.sqrt(1-w); sw1 = sp.sqrt(w*(1-w))
for term in sp.Add.make_args(E):
    has_w = term.has(sw_); has_1 = term.has(s1w)
    if has_w and has_1:
        Pw1 += sp.expand(term/sw1)
    elif has_w:
        Pw += sp.expand(term/sw_)
    elif has_1:
        P1 += sp.expand(term/s1w)
    else:
        P0 += term
P0 = sp.expand(P0); Pw = sp.expand(Pw); P1 = sp.expand(P1); Pw1 = sp.expand(Pw1)
print('dNJ2dt split: P0 terms:', len(sp.Add.make_args(P0)), ' Pw:', len(sp.Add.make_args(Pw)),
      ' P1:', len(sp.Add.make_args(P1)), ' Pw1:', len(sp.Add.make_args(Pw1)))
recon = P0 + sw_*Pw + s1w*P1 + sw1*Pw1
print('recon == E?', sp.expand(sp.expand(recon - E)) == 0)

# Save for inspection
with open('misc/t3_dNJ2dt_clean.pkl','wb') as fh:
    pickle.dump({'P0':P0,'Pw':Pw,'P1':P1,'Pw1':Pw1}, fh)
print('P0 =', sp.factor(P0))
print('Pw =', sp.factor(Pw))
print('P1 =', sp.factor(P1))
print('Pw1 =', sp.factor(Pw1))
