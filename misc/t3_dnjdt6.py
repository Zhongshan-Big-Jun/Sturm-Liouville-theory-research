# -*- coding: utf-8 -*-
"""t3_dnjdt6: robust split of dNJdt = P1(w) + sqrt(w(1-w))*P2(w)."""
import sympy as sp, pickle

with open('misc/t3_dNJdt_split.pkl','rb') as fh: d = pickle.load(fh)
E = sp.expand(d['E'])   # polynomial in A,t,sg,cg, w, sqrt(w), sqrt(1-w)
A, t, sg, cg = sp.symbols('A t sg cg', positive=True)
w = sp.symbols('w', positive=True)

def classify(term):
    """return (wpow, has_s1w, coeff) such that term = w^wpow * sqrt(1-w)^has_s1w * coeff, coeff w-free."""
    p = sp.Integer(0); s1w = False
    for atom in term.atoms(sp.Pow):
        if atom.base == w:
            e = atom.exp
            if sp.Rational(e.denominator) == 2:
                p += (e.numerator - 1)//2   # w^(k/2) = w^((k-1)/2)*sqrt(w)
                # factor sqrt(w) handled via sqrt(w(1-w))? No: keep as sqrt(w) part
        if atom == sp.sqrt(1-w) or (atom.is_Pow and atom.base == 1-w):
            s1w = True
    return p, s1w

# Instead: substitute w -> v^2, sqrt(w) -> v, sqrt(1-w) -> u; then split u^0/u^1; then back
v, u = sp.symbols('v u', positive=True)
E2 = sp.expand(E.subs({w: v**2, sp.sqrt(w): v, sp.sqrt(1-w): u}))
print('E2 terms:', len(sp.Add.make_args(E2)))
# split by u power
E0 = sp.expand(E2.subs(u, 0))
E1 = sp.expand((E2 - E0)/u)
print('E0 has u?', E0.has(u), ' E1 has u?', E1.has(u))
# now E0, E1 are polynomials in v (maybe odd powers). Split v even/odd
E0e = sp.expand(E0.subs(v, 0)); E0o = sp.expand((E0-E0e)/v)
E1e = sp.expand(E1.subs(v, 0)); E1o = sp.expand((E1-E1e)/v)
# back to w: v^2 -> w
def to_w(expr):
    e = sp.expand(expr)
    e = sp.expand(e.subs(v**2, w))
    return e
P1a = to_w(E0e); P1b = to_w(E0o); P2a = to_w(E1e); P2b = to_w(E1o)
print('P1a terms:', len(sp.Add.make_args(P1a)))
print('P1b terms:', len(sp.Add.make_args(P1b)))
print('P2a terms:', len(sp.Add.make_args(P2a)))
print('P2b terms:', len(sp.Add.make_args(P2b)))
# check all are w-pure
for name, P in [('P1a',P1a),('P1b',P1b),('P2a',P2a),('P2b',P2b)]:
    print(name, 'has v?', P.has(v), ' has u?', P.has(u))
# dNJ/dt = P1a(w) + v*P1b(w) + u*P2a(w) + u*v*P2b(w) = P1a + sqrt(w)*P1b + sqrt(1-w)*P2a + sqrt(w(1-w))*P2b
# reconstruct and verify vs E
recon = P1a + sp.sqrt(w)*P1b + sp.sqrt(1-w)*P2a + sp.sqrt(w(1-w))*P2b
print('recon == E?', sp.simplify(sp.expand(recon - E)) == 0)
import pickle as pk
with open('misc/t3_dNJdt_parity.pkl','wb') as fh: pk.dump({'P1a':P1a,'P1b':P1b,'P2a':P2a,'P2b':P2b}, fh)
print('P1b =', sp.factor(P1b))
print('P2a =', sp.factor(P2a))
print('P2b =', sp.factor(P2b))
print('P1a =', sp.factor(P1a))
