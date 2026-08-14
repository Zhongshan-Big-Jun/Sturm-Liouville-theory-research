# -*- coding: utf-8 -*-
"""Debug E6_4 computation."""
import pickle
import sympy as sp

u = sp.symbols('u', positive=True)
K, A, B, Cv = sp.symbols('K A B C')
P0 = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
K0, K1 = sp.symbols('K0 K1')
A0, A1 = sp.symbols('A0 A1')
B0, B1 = sp.symbols('B0 B1')
C0, C1 = sp.symbols('C0 C1')

print('raw E6 orders present:', sorted(m for (n, m) in P0 if n == 'E6'))
print('raw E6_3 =', P0[('E6', 3)])

Kd = K0 + K1*u
Ad = A0 + A1*u
Bd = B0 + B1*u
Cd = C0 + C1*u

# compute K-cleared E6 coefficient of u^4
tot = 0
for (nm, m), coef in P0.items():
    if nm != 'E6' or m > 4:
        continue
    cc = sp.expand(coef * K)
    e = sp.expand(sp.expand(cc.subs({K: Kd, A: Ad, B: Bd, Cv: Cd})) * u**m)
    c = e.coeff(u, 4)
    print('contribution from (%s,%d): raw coef=%s' % (nm, m, P0[(nm, m)]))
    print('   cleared*subs*u^%d = %s ' % (m, e))
    print('   u^%d coeff = %s' % (4, c))
    if c != 0:
        tot += c
print('E6_4 (cleared) =', sp.expand(tot))
print('solver claims E6_4 = -(2*A0*K0*K1 + A1*K0^2 - 2*K1) =',
      sp.expand(-(2*A0*K0*K1 + A1*K0**2 - 2*K1)))
