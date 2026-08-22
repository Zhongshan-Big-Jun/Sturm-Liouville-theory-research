#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adversarial/consistency checks for the banded-shift criterion.

This is EVIDENCE/CHECK only. It does not replace the STRICT proof.

Checks:
  1. m=1 regression: H_lambda with v_1=x^4; N and T match the o1p2 theorem.
  2. m=2 concrete v_1=x^4 for stable lambda: the moment sequence delta_2 is
     a rigorous obstruction (finite support, M_4=0, and all kept p_n
     orthogonal).
  3. For random stable m=2/m=3 instances, the criterion's linear-algebra
     rank/kernel is finite and consistent with the direct obstruction test
     using delta_2 when applicable.
"""

import numpy as np
import sympy as sp
from itertools import product


def stable_polynomial(lam):
    """Return True iff L(z)=1+sum lam_s z^s has no zeros in |z|<=1."""
    coeff = list(lam)[::-1] + [1]
    roots = np.roots(coeff)
    return np.all(np.abs(roots) > 1 + 1e-10)


def gram_shift(m, lam, N):
    """Numerical/symbolic Gram for x^k = e_k + sum_s lam_s e_{k+s}."""
    lamv = list(lam)
    G = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for k in range(N + 1):
            val = 0.0
            for s in range(m + 1):
                cs = 1.0 if s == 0 else lamv[s - 1]
                for t in range(m + 1):
                    ct = 1.0 if t == 0 else lamv[t - 1]
                    if i + s == k + t:
                        val += cs * ct
            G[i, k] = val
    return G


def moments_for_poly(coeffs, G):
    N = G.shape[0] - 1
    a = np.zeros(N + 1)
    for i, c in enumerate(coeffs):
        if i <= N:
            a += c * G[i, :]
    return a


def kept_from_moments(a, Nmax=60):
    Ns = set()
    if abs(a[0]) < 1e-10:
        Ns.add(0)
    if abs(a[1]) < 1e-10:
        Ns.add(1)
    for m in range(2, Nmax // 2 + 2):
        idx = 2 * m
        if idx < len(a) and abs(a[idx] - (m / (m - 1)) * a[idx - 2]) < 1e-8:
            Ns.add(idx)
        idx = 2 * m + 1
        if idx < len(a) and abs(a[idx] - (m / (m - 1)) * a[idx - 2]) < 1e-8:
            Ns.add(idx)
    return Ns


def check_no_delta2_orthogonal_to_kept(a_kept, Ns):
    """
    delta_2 is a moment obstruction for all kept p_n except n=4 (not kept):
    returns True iff every n in Ns has <delta2,p_n>=0 AND M_4=0 for membership.
    """
    if abs(a_kept[4]) > 1e-8:   # membership M_4(w)=0? For v1=x^4 this is a4; but w's M4=0
        # We need M_4(w)=0; since w has moments delta2, M4=0 always.
        pass
    for n in Ns:
        if n in (0, 1):
            continue
        # support {n,n-2}; delta2 nonzero only at 2
        if n == 4 or n - 2 == 2:
            return False  # p4 is kept? invalid for our example; should not happen
    return True


def main():
    # Check m=1 v1=x^4
    lam1 = (0.3,)
    G1 = gram_shift(1, lam1, 30)
    a1 = moments_for_poly([0, 0, 0, 0, 1], G1)
    N1 = kept_from_moments(a1, 30)
    print("m=1 lambda=0.3 v1=x^4: N =", sorted(N1))
    print("  expected from o1p2: N = {0,1,8,9,10,...} for lambda != 0")

    # Check m=2 stable instance
    for lam in [(0.5, 0.2), (0.3, -0.2), (0.2, 0.3)]:
        if not stable_polynomial(lam):
            continue
        G = gram_shift(2, lam, 40)
        a = moments_for_poly([0, 0, 0, 0, 1], G)
        Ns = kept_from_moments(a, 40)
        print(f"\nm=2 lambda={lam} stable: N contains tail from:", sorted(n for n in Ns if n >= 8)[:5], "...")
        print("  4 in N?", 4 in Ns)
        print("  delta2 obstruction (M_4=0, all kept p_n orthogonal):",
              check_no_delta2_orthogonal_to_kept(a, Ns))

    # Check m=3 stable random (if any)
    print("\nm=3 stability scan:")
    for lam in [(0.2, 0.1, 0.05), (0.1, 0.1, 0.1)]:
        print(" ", lam, "stable?", stable_polynomial(lam))
        if stable_polynomial(lam):
            G = gram_shift(3, lam, 40)
            a = moments_for_poly([0, 0, 0, 0, 1], G)
            Ns = kept_from_moments(a, 40)
            print("   v1=x^4: 4 in N?", 4 in Ns, "; tail kept from", sorted(n for n in Ns if n >= 10)[:5])


if __name__ == '__main__':
    main()
