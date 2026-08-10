# -*- coding: utf-8 -*-
"""t3_dnj2dA_split: decompose dNJ2/dA = 32 A^3 * KA, reduce KA."""
import sympy as sp, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(c) for c in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
c = sp.symbols('c', positive=True)
dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
# reduce st^2
dAr = sp.expand(dA_expr)
for _ in range(10):
    dAr = sp.expand(dAr.subs(st**2, 1-ct**2))
# substitute ct -> sqrt(w), st -> sqrt(1-w), normalize w^(k/2)
w = sp.symbols('w', positive=True)
E = sp.expand(dAr.subs({ct: sp.sqrt(w), st: sp.sqrt(1-w)}))
for _ in range(15):
    rep = {}
    for p in E.atoms(sp.Pow):
        if p.base == w and sp.Rational(p.exp.denominator) == 2 and int(p.exp.numerator) % 2 == 1:
            k = int(p.exp.numerator)
            rep[p] = w**((k-1)//2)*sp.sqrt(w)
    if not rep: break
    E = sp.expand(E.subs(rep))
E = sp.expand(E)
P0 = sp.Integer(0); Pw = sp.Integer(0); P1 = sp.Integer(0); Pw1 = sp.Integer(0)
sw_ = sp.sqrt(w); s1w = sp.sqrt(1-w); sw1 = sp.sqrt(w*(1-w))
for term in sp.Add.make_args(E):
    hw = term.has(sw_); h1 = term.has(s1w)
    if hw and h1: Pw1 += sp.expand(term/sw1)
    elif hw: Pw += sp.expand(term/sw_)
    elif h1: P1 += sp.expand(term/s1w)
    else: P0 += term
P0 = sp.expand(P0); Pw = sp.expand(Pw); P1 = sp.expand(P1); Pw1 = sp.expand(Pw1)
print('P0:', len(sp.Add.make_args(P0)), ' Pw:', len(sp.Add.make_args(Pw)), ' P1:', len(sp.Add.make_args(P1)), ' Pw1:', len(sp.Add.make_args(Pw1)))
print('Pw has sqrt?', Pw.has(sp.sqrt), ' P1 has sqrt?', P1.has(sp.sqrt), ' Pw1 has sqrt?', Pw1.has(sp.sqrt))
recon = P0 + sw_*Pw + s1w*P1 + sw1*Pw1
print('recon == E?', sp.expand(sp.expand(recon - E)) == 0)
print('Pw =', sp.factor(Pw))
print('P1 =', sp.factor(P1))
print('Pw1 =', sp.factor(Pw1))
print('P0 =', sp.factor(P0))
