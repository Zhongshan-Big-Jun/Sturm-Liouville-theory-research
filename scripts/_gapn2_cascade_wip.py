# -*- coding: utf-8 -*-
"""R-209 M3 cascade solver (STRICT derivation).

Level-by-level solve of E1=E2=E5=E6=0 for the full integer-power branch
  K(u) = sum K_j u^j,  a(u) = sum A_j u^j,  b(u) = sum B_j u^j,
  c(u) = sum C_j u^j,
where u = R^(-1/6), and the ansatz is k2 = K u, k3 = K u + C u^5,
p1 = pi/2 + a u^2, p3 = pi/4 + b u^2, eps = u^3.

At level j we use equations E1_j, E2_j, E5_{j+2}, E6_{j+3} (coefficient of
u^j etc.), with the level-j unknowns (K_j, A_j, B_j, C_j).  Levels 0-2 are
the nonlinear seed; every higher level is linear in the 4 level unknowns
(proved inside by inspection of the linearized coefficient).

We substitute lower-level solved coefficients as exact values and expand only
up to the needed order, so each level is a SMALL polynomial system.

STRICT: every step exact sympy; no floats in the derivation.  The final
numbers printed with sp.nsimplify / evalf are the exact rationals.
"""
import pickle
import sympy as sp
from sympy import pi

ND = 9  # max series degree requested through u^4 minimum, use 9 for room

u = sp.symbols('u', positive=True)
K, A, B, C = sp.symbols('K A B C')


def loadP():
    with open(r'scripts/_gapn2_largeR_P.pkl', 'rb') as f:
        return pickle.load(f)


P = loadP()

# Solve coefficients as exact sympy expressions (values are Rationals times pi).
sol = {}  # symbol name -> exact value


def set_sol(name, val):
    sol[sp.symbols(name)] = val


def subs_solved(expr):
    return expr.subs(sol)


def series_subs(coef, Ks, As, Bs, Cs, deg):
    """Substitute the series into a P coefficient (polynomial in K,A,B,C),
    and collect coefficients of u up to degree <deg>.  Only symbolic
    current-level variables remain; lower solved ones already substituted
    into the Ks/As/Bs/Cs dicts.  Returns dict n -> expression."""
    out = {}
    for n, var in enumerate(Ks):
        if n >= deg:
            break
        out.setdefault(n, {})
    # build truncated series of K,A,B,C
    Kexpr = sum(Ks[n] * u**n for n in range(deg))
    Aexpr = sum(As[n] * u**n for n in range(deg))
    Bexpr = sum(Bs[n] * u**n for n in range(deg))
    Cexpr = sum(Cs[n] * u**n for n in range(deg))
    e = sp.expand(coef.subs({K: Kexpr, A: Aexpr, B: Bexpr, C: Cexpr}))
    res = {}
    for n in range(deg):
        c = e.coeff(u, n)
        if c != 0:
            res[n] = c
    return res


def eq_coeff(name, n, Ks, As, Bs, Cs, deg=None):
    if deg is None:
        deg = n + 1
    Kex = sum(Ks[j] * u**j for j in range(deg))
    Aex = sum(As[j] * u**j for j in range(deg))
    Bex = sum(Bs[j] * u**j for j in range(deg))
    Cex = sum(Cs[j] * u**j for j in range(deg))
    tot = 0
    for (nm, m), coef in P.items():
        if nm != name:
            continue
        cc = sp.expand((coef.subs({K: Kex, A: Aex, B: Bex, C: Cex})) * u**m)
        c = cc.coeff(u, n)
        if c != 0:
            tot += c
    return sp.expand(tot)


# ---- manage the series coefficient holders ----
Ks = [sp.symbols('K%d' % j) for j in range(ND + 1)]
As = [sp.symbols('A%d' % j) for j in range(ND + 1)]
Bs = [sp.symbols('B%d' % j) for j in range(ND + 1)]
Cs = [sp.symbols('C%d' % j) for j in range(ND + 1)]


# =========================================================================
# LEVEL 0-2 nonlinear seed.
# =========================================================================
# Level 0 equations: E1_0, E2_0, E5_2, E6_3.
E1_0 = eq_coeff('E1', 0, Ks, As, Bs, Cs, deg=1)
E2_0 = eq_coeff('E2', 0, Ks, As, Bs, Cs, deg=1)
print('E1_0 =', sp.simplify(E1_0))
print('E2_0 =', sp.simplify(E2_0))
print('E5_0 =', sp.simplify(eq_coeff('E5', 0, Ks, As, Bs, Cs, deg=1)))
print('E6_3 =', sp.simplify(eq_coeff('E6', 3, Ks, As, Bs, Cs, deg=2)))
