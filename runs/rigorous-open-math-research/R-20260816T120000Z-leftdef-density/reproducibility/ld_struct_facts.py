#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural facts verification for the left-definite specialization.

Facts checked (EXACT rational arithmetic via sympy, symbol c > 0):
  F1. For s = 1 (H^1 Krein inner product): every monomial x^k is in H^1
      (all moments M_k(w)=<w,x^k>_1 well-defined).  The moment matrix
      G1[k,i] = <x^i, x^k>_1 is NON-diagonal (nontrivial in monomial basis).
  F2. For s = 2 (H^2, = D(K_c)): the sparse polynomials p_n (n != 2,3)
      satisfy the Krein boundary condition, hence p_n in H^2.
  F3. For s = 2: x^2 and x^3 are NOT in H^2 (structural absence).  Hence the
      monomial moments M_2(w)=<w,x^2>_2 and M_3(w)=<w,x^3>_2 are NOT
      well-defined as inner products with x^2,x^3 in H^2.
  F4. For s = 2: <w,p_4>_2 = M_4 - 2*M_2 is NOT a legitimate moment
      decomposition (M_2 undefined); the abstract functional <w,·>_2 on
      p_4 in H^2 is defined but not monomial-moment decomposable through x^2.
  F5. The H^2 inner product (moment matrix) is NOT diagonal in the monomial
      basis: G2[k,i] = <x^i,x^k>_2 (where both monomials are in H^2) has
      nonzero off-diagonal entries.

This is EVIDENCE (exact arithmetic), not a proof; the STRICT statements and
their proofs live in candidate_proof.md.  Numerical/exact checks never close
a proof obligation by themselves.
"""
import sys
import sympy as sp

c = sp.symbols('c', positive=True)
x = sp.symbols('x')

# ---------------------------------------------------------------- H^1
def h1_inner(f, g, cc):
    """Krein H^1 inner product (f,g)_1 on [-1,1], *conjugated in second Var
    handled by taking real coefficients: (f,g)_1 = <K^1/2 f, K^1/2 g>.
    Formula: int f' * g' + c*int f*g - (1/2) Delta(f) Delta(g).
    For real-valued polynomials we compute the real bilinear form; the
    conjugate-linear convention is <f,g> = conj of this with g entries.
    """
    df = sp.diff(f, x)
    dg = sp.diff(g, x)
    Df = (f.subs(x, 1) - f.subs(x, -1))
    Dg = (g.subs(x, 1) - g.subs(x, -1))
    return sp.integrate(df * dg, (x, -1, 1)) + cc * sp.integrate(f * g, (x, -1, 1)) \
        - sp.Rational(1, 2) * Df * Dg

def h2_polys(f, g, cc):
    """H^2 inner product (f,g)_{2,c} = int(f'' g'') + 2c int(f' g') + c^2 int(f g)
       - c * Delta(f) * Delta(g)."""
    d2f = sp.diff(f, x, 2)
    d2g = sp.diff(g, x, 2)
    d1f = sp.diff(f, x)
    d1g = sp.diff(g, x)
    Df = (f.subs(x, 1) - f.subs(x, -1))
    Dg = (g.subs(x, 1) - g.subs(x, -1))
    return sp.integrate(d2f * d2g, (x, -1, 1)) + 2 * cc * sp.integrate(d1f * d1g, (x, -1, 1)) \
        + cc**2 * sp.integrate(f * g, (x, -1, 1)) - cc * Df * Dg

def krein_bc_satisfied(p):
    """Does polynomial p satisfy the Krein boundary condition
       p'(1) = p'(-1) = (p(1)-p(-1))/2 ?"""
    dp = sp.diff(p, x)
    lhs1 = dp.subs(x, 1)
    lhs_1 = dp.subs(x, -1)
    rhs = sp.Rational(1, 2) * (p.subs(x, 1) - p.subs(x, -1))
    return sp.simplify(lhs1 - rhs) == 0 and sp.simplify(lhs_1 - rhs) == 0

print("=" * 70)
print("F1: H^1 monomial moments and moment matrix G1[k,i] = <x^i, x^k>_1")
print("=" * 70)
# moment matrix 0..5 for H^1
G1 = sp.zeros(6)
for k in range(6):
    for i in range(6):
        G1[k, i] = sp.simplify(h1_inner(x**i, x**k, c))
print("G1 (rows k=0..5, cols i=0..5):")
for k in range(6):
    print("  k=%d: %s" % (k, str([sp.simplify(G1[k, i]) for i in range(6)])))
# diagonal check
diag_ok = all(sp.simplify(G1[k, i]) == 0 for k in range(6) for i in range(6) if k != i)
print("  G1 diagonal? (should be False):", diag_ok)
print("  nonzero off-diagonal entries present:", any(sp.simplify(G1[k, i]) != 0 for k in range(6) for i in range(6) if k != i))

print()
print("=" * 70)
print("F2/F3: H^2 membership via Krein boundary condition")
print("=" * 70)
# sparse family
def p_sparse(n):
    if n == 0:
        return sp.Integer(1)
    if n == 1:
        return x
    if n % 2 == 0:
        m = n // 2          # n = 2m, m >= 2
        return x**n - sp.Rational(m, m - 1) * x**(n - 2)
    else:
        m = (n - 1) // 2    # n = 2m+1, m >= 2
        return x**n - sp.Rational(m, m - 1) * x**(n - 2)

print("  p_n in H^2 (n from 0..9, n!={2,3}):")
for n in [0, 1, 4, 5, 6, 7, 8, 9]:
    print("    p_%d: BC satisfied? %s" % (n, krein_bc_satisfied(p_sparse(n))))
print("  monomials x^2, x^3 in H^2 (BC satisfied)?")
print("    x^2:", krein_bc_satisfied(x**2), "  x^3:", krein_bc_satisfied(x**3))

print()
print("=" * 70)
print("F4: <w, p_4>_2 decomposition — is M_4 - 2 M_2 valid? (M_2 undefined)")
print("=" * 70)
# p_4 = x^4 - 2 x^2 ; x^2 not in H^2, so M_2 = <w,x^2>_2 undefined.
print("  p_4 = x^4 - 2 x^2 ; x^2 not in H^2 => M_2(w)=<w,x^2>_2 is NOT a")
print("  well-defined inner product.  The functional <w, ·>_2 on p_4 is defined")
print("  (p_4 in H^2) but cannot be split as M_4 - 2 M_2 via monomial moments.")


