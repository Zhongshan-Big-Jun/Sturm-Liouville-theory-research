# -*- coding: utf-8 -*-
"""t3_dAd_split: split dNJ2/dA|c into w-parts."""
import sympy as sp, json, pickle

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
c = sp.symbols('c', positive=True)

with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))

dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
for _ in range(12):
    dA_expr = sp.expand(dA_expr.subs(st**2, 1-ct**2))
w = sp.symbols('w', positive=True)
E = sp.expand(dA_expr.subs({ct: sp.sqrt(w), st: sp.sqrt(1-w)}))
E = sp.expand(E)
print('E terms:', len(sp.Add.make_args(E)))
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
print('P0:', len(sp.Add.make_args(P0)), ' Pw:', len(sp.Add.make_args(Pw)),
      ' P1:', len(sp.Add.make_args(P1)), ' Pw1:', len(sp.Add.make_args(Pw1)))
recon = P0 + sw_*Pw + s1w*P1 + sw1*Pw1
print('recon == E?', sp.expand(sp.expand(recon - E)) == 0)
for name, P in [('P0',P0),('Pw',Pw),('P1',P1),('Pw1',Pw1)]:
    print(name, 'has sqrt?', P.has(sp.sqrt), ' terms:', len(sp.Add.make_args(P)))
with open('misc/t3_dAd_clean.pkl','wb') as fh:
    pickle.dump({'P0':P0,'Pw':Pw,'P1':P1,'Pw1':Pw1}, fh)
for name in ['P0','Pw','P1','Pw1']:
    P = {'P0':P0,'Pw':Pw,'P1':P1,'Pw1':Pw1}[name]
    print()
    print(name, '=', sp.factor(P))
