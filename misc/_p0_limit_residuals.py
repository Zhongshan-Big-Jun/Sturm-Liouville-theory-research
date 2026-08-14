# -*- coding: utf-8 -*-
"""Manager-side independent check (audit-prep, round 4): evaluate the exact
P coefficients at the handoff fit limits to see the leading-order residuals.
EVIDENCE only; does not constitute proof."""
import pickle
import sympy as sp

P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
K, A, B, C = sp.symbols('K A B C')
lim = {K: sp.Rational(34553, 10000), A: sp.Rational(5788, 10000),
       B: sp.Rational(2898, 10000), C: sp.Rational(14741, 10000)}
print('a0*K0 =', float(sp.N(lim[A]*lim[K], 20)))
for name in ['E1', 'E2', 'E5', 'E6']:
    keys = sorted([m for (nm, m) in P if nm == name])
    for m in keys:
        v = sp.N(P[(name, m)].subs(lim), 15)
        print('%s_%d = %s' % (name, m, v))
