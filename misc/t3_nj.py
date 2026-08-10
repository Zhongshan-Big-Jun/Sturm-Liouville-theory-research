# -*- coding: utf-8 -*-
"""t3_nj: reduce J2_2d numerator; check divisibility; summarize structure."""
import sympy as sp, pickle

with open('misc/t3_symbols5.pkl','rb') as fh:
    d = pickle.load(fh)
G, Gc, Gx, u, P = d['G'], d['Gc'], d['Gx'], d['u'], d['P']
den_extra, NumJ = d['den_extra'], d['NumJ']

# check divisibility of NumJ by den_extra
q, rem = sp.div(sp.expand(NumJ), sp.expand(den_extra), domain='ZZ')
print('NumJ divisible by den_extra:', rem == 0)
if rem == 0:
    NJ = sp.expand(q)
    print('NJ terms:', len(sp.Add.make_args(NJ)))
    atoms = [sp.Symbol('A'), sp.Symbol('t'), sp.Symbol('sg'), sp.Symbol('cg'), sp.Symbol('st'), sp.Symbol('ct')]
    poly = sp.Poly(NJ, *atoms)
    print('NJ deg:', poly.total_degree(), ' monomials:', len(poly.monoms()))
    coeffs = poly.coeffs()
    pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
    print('pos:', len(pos), 'sum_pos:', sum(pos), ' max_pos:', max(pos))
    print('neg:', len(neg), 'sum_neg:', sum(neg), ' min_neg:', min(neg))
    # check the factor 4A^2 claim: J2_2d = 4A^2 NJ / P^4
    # already: NumJ over P^4*den_extra; reduced NJ over P^4 -> check J2_2d*P^4/(4A^2) == NJ
    diff = sp.expand(NJ - sp.expand(J2check)) if False else None
    import json
    res = {'nterms': len(poly.monoms()), 'deg': poly.total_degree(),
           'monoms': [list(m) for m in poly.monoms()], 'coeffs': [str(c) for c in coeffs]}
    with open('misc/t3_NJ.json','w') as fh: json.dump(res, fh)
    print('saved misc/t3_NJ.json')
