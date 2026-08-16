#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural facts verification for the left-definite specialization.

Facts checked (EXACT rational arithmetic via sympy, symbol c > 0):
  F1.  For s = 1 (H^1 Krein inner product): every monomial x^k is in H^1 and the
       moment matrix G1[k,i] = <x^i, x^k>_1 is NON-diagonal (e.g. <x^1,x^3>_1 =
       2c/5 != 0).
  F2.  For s = 2 (H^2 = D(K_c)): the sparse polynomials p_n (n != 2,3) satisfy
       the Krein boundary condition, hence p_n in H^2.
  F3.  For s = 2: x^2 and x^3 (and all x^k, k>=2) are NOT in H^2.
  F4.  For s = 2: <w,p_4>_2 = M_4 - 2 M_2 is NOT a valid moment decomposition
       (M_2 undefined).
  F5.  (AUDIT-CORRECTED) In H^2 only monomials 1,x are present and (1,x)_2 = 0,
       so the H^2 "monomial block" is vacuous; the moment matrix that is genuinely
       NON-diagonal (blocking DensBC O1 finiteness) is the H^1 one (F1).
  S1d. (DECISIVE) For s >= 4 the sparse p_n (n >= 4) are NOT in H^s under the
       operator-domain reading H^s = D(K_c^{s/2}): p_4 notin H^4 because
       K_c p_4 fails the Krein BC.  Hence H^s ∩ C[x] = span{1,x} for s >= 4, and
       the sparse family does NOT recover H^s (L1'').

This is EVIDENCE (exact arithmetic), not a proof; the STRICT statements and their
proofs live in candidate_proof.md.  Numerical/exact checks never close a proof
obligation by themselves.
"""
import sys
import sympy as sp

c = sp.symbols('c', positive=True)
x = sp.symbols('x')

# ---------------------------------------------------------------- H^1
def h1_inner(f, g, cc):
    """Krein H^1 inner product (f,g)_1 = int f'g' + c*int f g - (1/2) Delta(f) Delta(g)."""
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
G1 = sp.zeros(6)
for k in range(6):
    for i in range(6):
        G1[k, i] = sp.simplify(h1_inner(x**i, x**k, c))
print("G1 (rows k=0..5, cols i=0..5):")
for k in range(6):
    print("  k=%d: %s" % (k, str([sp.simplify(G1[k, i]) for i in range(6)])))
diag_ok = all(sp.simplify(G1[k, i]) == 0 for k in range(6) for i in range(6) if k != i)
print("  G1 diagonal? (should be False):", diag_ok)
nz = sum(1 for k in range(6) for i in range(6) if k != i and sp.simplify(G1[k, i]) != 0)
print("  # nonzero off-diagonal H^1 entries (0..5):", nz, " ; <x^1,x^3>_1 =",
      sp.simplify(G1[1, 3]), " != 0")

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
print("  monomials in H^2 (BC)? x^2:", krein_bc_satisfied(x**2),
      " x^3:", krein_bc_satisfied(x**3))
print("  monomials x^4..x^10 in H^2 (BC)?")
for k in range(4, 11):
    print("    x^%d: %s" % (k, krein_bc_satisfied(x**k)))

print()
print("=" * 70)
print("F4: <w, p_4>_2 decomposition — is M_4 - 2 M_2 valid? (M_2 undefined)")
print("=" * 70)
print("  p_4 = x^4 - 2 x^2 ; x^2 not in H^2 => M_2(w)=<w,x^2>_2 is NOT a")
print("  well-defined inner product.  The functional <w, ·>_2 on p_4 is defined")
print("  (p_4 in H^2) but cannot be split as M_4 - 2 M_2 via monomial moments.")

print()
print("=" * 70)
print("F5 (AUDIT-CORRECTED): H^2 monomial block is vacuous; H^1 is non-diagonal")
print("=" * 70)
G2 = sp.zeros(2)
for a, k in enumerate([0, 1]):
    for b, i in enumerate([0, 1]):
        G2[a, b] = sp.simplify(h2_polys(x**i, x**k, c))
print("  H^2 monomial moment block over {1, x}:")
for a, k in enumerate([0, 1]):
    print("    k=%d: %s" % (k, str([sp.simplify(G2[a, b]) for b in range(2)])))
print("  (1,x)_2 =", sp.simplify(G2[0, 1]), " (0 => diagonal/vacuous; x^k for k>=2 absent)")
print("  => The non-diagonal matrix that blocks DensBC O1 finiteness lives in H^1 (F1).")

print()
print("=" * 70)
print("S1d (DECISIVE): for s >= 4 the sparse p_n (n>=4) are NOT in H^s")
print("=" * 70)
def Kc(q):
    return sp.expand(-sp.diff(q, x, 2) + c * q)
Kp4 = Kc(p_sparse(4))
dKp4 = sp.diff(Kp4, x)
bc_rhs = sp.Rational(1, 2) * (Kp4.subs(x, 1) - Kp4.subs(x, -1))
print("  p_4 =", p_sparse(4))
print("  K_c p_4 =", Kp4)
print("  (K_c p_4)'(+1) =", sp.simplify(dKp4.subs(x, 1)),
      " ; (K_c p_4)'(-1) =", sp.simplify(dKp4.subs(x, -1)),
      " ; half endpoint diff =", sp.simplify(bc_rhs))
print("  K_c p_4 satisfies Krein BC?", krein_bc_satisfied(Kp4))
print("  => K_c p_4 notin H^2 => p_4 notin H^4 = D(K_c^2).  (S1d: p_n notin H^s, s>=4, n>=4)")
print("  p_0=1 and p_1=x in every H^s: 1:", krein_bc_satisfied(sp.Integer(1)),
      " ; x:", krein_bc_satisfied(x))
print("  => H^s ∩ C[x] = span{1,x} for s >= 4; the sparse family is NOT a subset of H^s.")
print("  => (L1'') for V = H^s (s>=4): Q_sp = {1,x}, closure(span Q_sp) = span{1,x} != H^s.")

print()
print("DONE")
