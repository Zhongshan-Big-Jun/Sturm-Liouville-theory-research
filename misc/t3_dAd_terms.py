# -*- coding: utf-8 -*-
"""t3_dAd_terms: term-by-term structure of dNJ2/dA at sample points."""
import sympy as sp, json, math

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
c = sp.symbols('c', positive=True)

with open('misc/t3_NJ2.json') as fh: r = json.load(fh)
monoms = r['monoms']; coeffs = [int(cf) for cf in r['coeffs']]
NJ2 = sum(coeffs[i]*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(monoms))
dA_expr = sp.expand(sp.diff(NJ2, A) + c*sp.diff(NJ2, t) - cg*sp.diff(NJ2, sg) + sg*sp.diff(NJ2, cg)
                    + c*ct*sp.diff(NJ2, st) - c*st*sp.diff(NJ2, ct))
dA_expr = sp.expand(dA_expr.subs(t, c*A))
terms = sp.Add.make_args(dA_expr)
print('number of terms:', len(terms))

def ev_term(term, Av, cv):
    tv = cv*Av; gv = math.pi-Av
    sv = {A: Av, c: cv, sg: math.sin(gv), cg: math.cos(gv), st: math.sin(tv), ct: math.cos(tv)}
    return float(term.subs(sv).evalf(20))

for (Av, cv, name) in [(2*math.pi/3, 0.5, 'corner (2pi/3,0.5)'),
                       (5*math.pi/7, 0.4, 'corner (5pi/7,0.4)'),
                       (math.pi-0.655, 0.5, 'far (pi-0.655,0.5)'),
                       (2.35, 0.45, 'mid (2.35,0.45)')]:
    vals = [(t, ev_term(t, Av, cv)) for t in terms]
    pos = [v for _, v in vals if v > 0]
    neg = [v for _, v in vals if v < 0]
    print('%s: total=%.2f  pos_sum=%.2f (n=%d)  neg_sum=%.2f (n=%d)' % (name, sum(v for _,v in vals), sum(pos), len(pos), sum(neg), len(neg)))
    top = sorted(vals, key=lambda x: -abs(x[1]))[:5]
    print('   top terms:', [(str(k)[:60], round(v,1)) for k, v in top])
