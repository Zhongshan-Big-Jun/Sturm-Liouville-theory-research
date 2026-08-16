#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Counterexample verification (EXACT rational arithmetic via sympy).

Instance (H^2[-1,1], (.,.)_2), V = { f in H^2 : f(1)-f(-1) = 0 } = ker(Delta).
Candidate Q_sp = { p_n : p_n in V }.

Claims verified EXACTLY:
  C1. p_n in H^2 for all n in {0,1,4,5,...} (Krein BC satisfied).
  C2. Every even p_n (n in {0,4,6,8,...}) lies in V  (Delta p_n = 0).
  C3. Every odd p_n (n in {1,5,7,9,...}) has Delta p_n != 0, hence NOT in V.
      -> Q_sp = {p_0} union {p_{2n}: n>=2} (even sparse family only).
  C4. q := p_5 - 2*p_7 is an ODD polynomial with Delta q = 0, so q in V, q != 0.
  C5. H^2 inner product is parity-orthogonal: (even, odd)_2 = 0
      (verified for the kept even Q_sp against q).
  C6. Hence q in V cap Q_sp^orth, q != 0 => closure(span Q_sp) != V
      (density FAILS) by DensBC Theorem A.

This is EVIDENCE (exact arithmetic) corroborating the STRICT proof in
candidate_proof.md; the proof itself is the argument, not this script.
"""
import sympy as sp

c = sp.symbols('c', positive=True)
x = sp.symbols('x')

def p_sparse(n):
    if n == 0:
        return sp.Integer(1)
    if n == 1:
        return x
    if n % 2 == 0:
        m = n // 2
        return x**n - sp.Rational(m, m - 1) * x**(n - 2)
    else:
        m = (n - 1) // 2
        return x**n - sp.Rational(m, m - 1) * x**(n - 2)

def krein_bc(p):
    dp = sp.diff(p, x)
    lhs1 = dp.subs(x, 1)
    lhs_1 = dp.subs(x, -1)
    rhs = sp.Rational(1, 2) * (p.subs(x, 1) - p.subs(x, -1))
    return sp.simplify(lhs1 - rhs) == 0 and sp.simplify(lhs_1 - rhs) == 0

def Delta(p):
    return sp.simplify(p.subs(x, 1) - p.subs(x, -1))

def h2_inner(f, g, cc):
    d2f = sp.diff(f, x, 2)
    d2g = sp.diff(g, x, 2)
    d1f = sp.diff(f, x)
    d1g = sp.diff(g, x)
    Df = Delta(f)
    Dg = Delta(g)
    return sp.simplify(sp.integrate(d2f * d2g, (x, -1, 1))
                       + 2 * cc * sp.integrate(d1f * d1g, (x, -1, 1))
                       + cc**2 * sp.integrate(f * g, (x, -1, 1))
                       - cc * Df * Dg)

print("=" * 70)
print("C1: p_n in H^2 (Krein BC)  for n in {0,1,4,5,6,7,8,9}")
print("=" * 70)
for n in [0, 1, 4, 5, 6, 7, 8, 9]:
    print("  p_%d in H^2? %s" % (n, krein_bc(p_sparse(n))))

print()
print("=" * 70)
print("C2/C3: parity + membership in V = ker(Delta)")
print("=" * 70)
for n in [0, 1, 4, 5, 6, 7]:
    pn = p_sparse(n)
    print("  p_%d: Delta=%s (0 => p_n in V); parity=%s"
          % (n, Delta(pn), "even" if n % 2 == 0 else "odd"))

print()
print("=" * 70)
print("C4: q = p_5 - 2 p_7 is odd, in V (Delta q = 0), nonzero")
print("=" * 70)
q = p_sparse(5) - 2 * p_sparse(7)
print("  q(x) =", sp.simplify(q))
print("  Delta q =", Delta(q), " (0 => q in V)")
print("  q(x) - (-1)^1 q(-x)? (odd check) =", sp.simplify(q.subs(x, -x) + q))
print("  q == 0 ?", sp.simplify(q) == 0)
print("  q in H^2 (BC)?", krein_bc(q))

print()
print("=" * 70)
print("C5/C6: q orthogonal to every kept even p_n (parity-orthogonality)")
print("=" * 70)
print("  H^2 (p_even, q) for even p_n in Q_sp:")
for n in [0, 4, 6, 8]:
    val = h2_inner(p_sparse(n), q, c)
    print("    (p_%d, q)_2 = %s" % (n, val))
# also directly verify even p_n all have Delta 0 hence in V
print("  kept set check: for n in {0,4,6,8}: Delta(p_n) =",
      [Delta(p_sparse(n)) for n in [0, 4, 6, 8]])
print("  => Q_sp = even sparse family; q in V cap Q_sp^orth, q != 0.")
print("  => closure(span Q_sp) != V  (density FAILS)  [DensBC Theorem A]")
print()
print("DONE")
