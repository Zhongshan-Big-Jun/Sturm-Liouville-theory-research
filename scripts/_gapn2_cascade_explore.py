# -*- coding: utf-8 -*-
"""Temporary exploration: load P, substitute full integer-power series for
K,A,B,C, and inspect the level-by-level structure of E1_j, E2_j, E5_{j+2},
E6_{j+3}.  All symbolic (STRICT bookkeeping).  No output file written.
"""
import pickle
import sympy as sp

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')

P = pickle.load(open(r'scripts/_gapn2_largeR_P.pkl', 'rb'))

# choose max series degree
ND = 9

Ks = [sp.symbols('K%d' % j) for j in range(ND + 1)]
As = [sp.symbols('A%d' % j) for j in range(ND + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(ND + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(ND + 1)]

Ks_expr = sum(Ks[j] * u**j for j in range(ND + 1))
As_expr = sum(As[j] * u**j for j in range(ND + 1))
Bs_expr = sum(Bs[j] * u**j for j in range(ND + 1))
Cs_expr = sum(Cs[j] * u**j for j in range(ND + 1))

subs = {K: Ks_expr, A: As_expr, B: Bs_expr, C: Cs_expr}

# For each equation, substitute and expand in u to degree ND.
Sys = {}
for (name, m), coef in P.items():
    e = sp.expand(coef.subs(subs))
    for n in range(ND + 1):
        cn = e.coeff(u, n)
        if cn != 0:
            Sys[(name, m, n)] = cn

# Now the true equation coefficient of u^n in equation 'name' is
# sum over m of Sys[(name, m, n)].
def eq(name, n):
    return sum(Sys.get((name, m, n), 0) for m in range(20))

print('=== level-by-level ===')
for j in range(0, 6):
    print('--- LEVEL j = %d ---' % j)
    for (name, n) in [('E1', j), ('E2', j), ('E5', j + 2), ('E6', j + 3)]:
        e = sp.simplify(eq(name, n))
        print('%s_%d :' % (name, n), e)
