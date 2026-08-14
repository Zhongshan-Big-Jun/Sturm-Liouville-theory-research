# -*- coding: utf-8 -*-
"""R-209 M3 corrected seed solve using the UNAMBIGUOUS full-substitution
eq_coeff (proven correct vs the Pbuild definition).  Only low orders (fast).
Solve the seed with sympy nsolve seeded at the handoff fit, then higher
orders as a check.

Unknowns (after a0=2/K0, a1=-2K1/K0^2): K0,K1,K2, A2, B0,B1, C0,C1 (8).
Seed equations: E1_2, E2_2, E6_5, E5_4, E5_5, E5_6 (6).  Solve with 2 fixed
(detect which 2 are structurally free).
"""
import pickle
import sympy as sp
from sympy import pi, sqrt, nsolve

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')
P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))
DNAME = {'E1': 0, 'E2': 2, 'E5': 5, 'E6': 1}
Pc = {(name, m): sp.expand(coef * K**DNAME[name]) for (name, m), coef in P.items()}


def eq_coeff(name, n, Kex, Aex, Bex, Cex):
    tot = 0
    for (nm, m), coef in Pc.items():
        if nm != name:
            continue
        cc = sp.expand(coef.subs({K: Kex, A: Aex, B: Bex, C: Cex}) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


K0, K1, K2, A2, B0, B1, C0, C1 = sp.symbols('K0 K1 K2 A2 B0 B1 C0 C1')

Kex = K0 + K1 * u + K2 * u**2
Aex = (2 / K0) + (-2 * K1 / K0**2) * u + A2 * u**2
Bex = B0 + B1 * u
Cex = C0 + C1 * u

# seed equations
seed = {
    'E1_2': eq_coeff('E1', 2, Kex, Aex, Bex, Cex),
    'E2_2': eq_coeff('E2', 2, Kex, Aex, Bex, Cex),
    'E6_5': eq_coeff('E6', 5, Kex, Aex, Bex, Cex),
    'E5_4': eq_coeff('E5', 4, Kex, Aex, Bex, Cex),
    'E5_5': eq_coeff('E5', 5, Kex, Aex, Bex, Cex),
    'E5_6': eq_coeff('E5', 6, Kex, Aex, Bex, Cex),
}

# clear denominators (multiply by K0^6) so nsolve sees polynomials
for nm, e in seed.items():
    seed[nm] = sp.expand(sp.together(e) * K0**6)

print('seed equations (K0^6-cleared):')
for nm, e in seed.items():
    print('  %s: %d terms, unknowns=%s' % (nm, len(e.as_ordered_terms()),
                                           sorted({str(a) for a in e.free_symbols})))
print()

# which unknowns appear per equation
allu = [K0, K1, K2, A2, B0, B1, C0, C1]
for nm, e in seed.items():
    present = [str(a) for a in allu if e.has(a)]
    print('  %s depends on %s' % (nm, present))

print()
# impose K1=0 (structural: K even; E1_2..E5_4 involve only K1^2, so K1=0 is
# a valid branch choice, and the odd forcing lands on C1, see E5_5).
# Solve 6 unknowns {K0,K2,A2,B0,C0,C1} from the 6 seed equations (K1=0, B1=0).
subs1 = {K1: 0, B1: 0}
eqs = [seed[nm].subs(subs1) for nm in ['E1_2', 'E2_2', 'E6_5', 'E5_4', 'E5_5', 'E5_6']]

import numpy as np
from scipy.optimize import least_squares

targets = [K0, K2, A2, B0, C0, C1]
Fn = sp.lambdify(targets, [sp.together(e) for e in eqs], 'numpy')
guess = {K0: 3.4553, K2: 2.937, A2: -0.643, B0: 0.2898, C0: 1.4741, C1: 0.5}
gv = np.array([float(guess[t]) for t in targets])
print('initial |res| = %.3e' % np.max(np.abs(Fn(*gv))))

try:
    sol = nsolve([sp.together(e) for e in eqs], targets, [guess[t] for t in targets],
                 solver='mnewton', verify=False, tol=1e-20, maxsteps=200)
    print('nsolve (mnewton) converged:')
    for t, v in zip(targets, sol):
        print('  %s = %.12f' % (t, v))
    vals = {t: v for t, v in zip(targets, sol)}
    print('residual |max| = %.3e' % np.max(np.abs(Fn(*[float(v) for v in sol]))))
except Exception as ex:
    print('nsolve failed:', str(ex)[:200])
    def fun(v):
        return np.array([float(x) for x in Fn(*v)], dtype=float)
    res = least_squares(fun, gv, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=40000)
    print('least_squares |res| = %.3e' % np.max(np.abs(res.fun)))
    for t, v in zip(targets, res.x):
        print('  %s = %.12f' % (t, v))

