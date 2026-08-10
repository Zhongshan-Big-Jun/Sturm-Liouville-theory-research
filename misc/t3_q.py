# -*- coding: utf-8 -*-
"""t3_q: Q(u) = P05/u^4; examine structure and check numeric range."""
import sympy as sp, json, math
with open('misc/t3_P05.json') as fh: r = json.load(fh)
u, su, cu = sp.symbols('u su cu', positive=True)
P05 = sum(int(c)*u**m[0]*su**m[1]*cu**m[2] for m,c in zip(r['monoms'], r['coeffs']))
Q = sp.expand(P05/u**4)
pq = sp.Poly(Q, u, su, cu)
print('Q terms:', len(pq.monoms()), 'deg:', pq.total_degree())
for m,c in sorted(zip(pq.monoms(), pq.coeffs()), key=lambda x: -int(x[1])):
    print('  %9d * u^%d su^%d cu^%d' % (int(c),m[0],m[1],m[2]))
