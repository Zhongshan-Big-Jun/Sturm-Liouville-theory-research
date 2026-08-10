# -*- coding: utf-8 -*-
"""t3_show: show dG_dq numerator monomials/coeffs; try small-factor."""
import sympy as sp, json, pickle

with open('misc/t3_num6.pkl','rb') as fh: data = pickle.load(fh)
res = data['res']
atoms = [sp.Symbol('A'), sp.Symbol('t'), sp.Symbol('sg'), sp.Symbol('cg'), sp.Symbol('st'), sp.Symbol('ct')]
for k in ['dG_dq','dG_dg','dGc_dq','dGc_dg','dGx_dg']:
    r = res[k]
    print('='*20, k, ' n=%d deg=%d' % (r['nterms'], r['deg']))
    terms = list(zip(r['monoms'], r['coeffs']))
    terms_sorted = sorted(terms, key=lambda x: -int(x[1]))
    for m, c in terms_sorted[:14]:
        print('   %6s * A^%d t^%d sg^%d cg^%d st^%d ct^%d' % (c, m[0],m[1],m[2],m[3],m[4],m[5]))
    if len(terms) > 14: print('   ...')
