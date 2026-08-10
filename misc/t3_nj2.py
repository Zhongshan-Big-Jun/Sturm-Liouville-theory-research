# -*- coding: utf-8 -*-
"""t3_nj2: reduce J2 numerator with matching symbols; summarize structure."""
import sympy as sp, pickle, json

A, t = sp.symbols('A t', positive=True)
sg, cg, st, ct = sp.symbols('sg cg st ct', positive=True)
with open('misc/t3_symbols5.pkl','rb') as fh:
    d = pickle.load(fh)
den_extra, NumJ = d['den_extra'], d['NumJ']
q, rem = sp.div(sp.expand(NumJ), sp.expand(den_extra), domain='ZZ')
print('divisible:', rem == 0)
NJ = sp.expand(q)
atoms = [A,t,sg,cg,st,ct]
poly = sp.Poly(NJ, *atoms)
coeffs = poly.coeffs(); monoms = poly.monoms()
print('NJ terms:', len(monoms), ' deg:', poly.total_degree())
pos = [c for c in coeffs if c > 0]; neg = [c for c in coeffs if c < 0]
print('pos:', len(pos), 'sum_pos:', sum(pos), ' max_pos:', max(pos))
print('neg:', len(neg), 'sum_neg:', sum(neg), ' min_neg:', min(neg))
res = {'nterms': len(monoms), 'deg': poly.total_degree(),
       'monoms': [list(m) for m in monoms], 'coeffs': [str(c) for c in coeffs]}
with open('misc/t3_NJ.json','w') as fh: json.dump(res, fh)
print('saved misc/t3_NJ.json')
# show the biggest positive and negative terms
tm = sorted(zip(monoms, coeffs), key=lambda x: -int(x[1]))
print('--- top 10 positive ---')
for m,c in tm[:10]: print('  %6d A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c,m[0],m[1],m[2],m[3],m[4],m[5]))
print('--- top 10 negative ---')
for m,c in tm[-10:]: print('  %6d A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c,m[0],m[1],m[2],m[3],m[4],m[5]))
