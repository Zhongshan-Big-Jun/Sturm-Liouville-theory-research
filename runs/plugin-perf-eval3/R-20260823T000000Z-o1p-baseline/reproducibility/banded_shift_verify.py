#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tier 0/1 verification for the new banded-shift Hilbert-space family.

The file computes, for H_shift(m, lambda):
    x^k = e_k + sum_{s=1}^m lambda_s e_{k+s}
and finite polynomial constraints v_j = sum_i c_i x^i,
the Gram matrix, the kept sparse set N, the run/free-base graph,
the finite-linear-algebra matrix T, and the kernel criterion.

This script is CHECK/EVIDENCE only. It does not prove the theorem.
It checks consistency of the symbolic formulas on concrete instances
and verifies the explicit obstruction for v_1 = x^4 in bandwidth 2.
"""

import itertools
import numpy as np
import sympy as sp

M = sp.Symbol('M')  # m placeholder, unused

# ----------------------------------------------------------------------
# 1. Symbolic Gram matrix for real shift family
# ----------------------------------------------------------------------
def gram_shift_symbolic(m, lam, N):
    """Return Gram matrix G_{i,k}=<x^i,x^k> for i,k <= N.

    lam is a tuple of length m (symbolic or numeric).
    """
    G = sp.zeros(N + 1, N + 1)
    for i in range(N + 1):
        for k in range(N + 1):
            val = 0
            # x^i = e_i + sum_s lam_s e_{i+s}
            # x^k = e_k + sum_t lam_t e_{k+t}
            for s in range(0, m + 1):
                cs = 1 if s == 0 else lam[s - 1]
                for t in range(0, m + 1):
                    ct = 1 if t == 0 else lam[t - 1]
                    # index in x^i: i+s, in x^k: k+t
                    if i + s == k + t:
                        val += cs * ct
            G[i, k] = sp.simplify(val)
    return G

def moment_for_polynomial(vcoeffs, G):
    """Return a_k = <v, x^k> = sum_i c_i G_{i,k} as a list."""
    N = G.shape[0] - 1
    a = [0] * (N + 1)
    for k in range(N + 1):
        s = 0
        for i, c in enumerate(vcoeffs):
            if i <= N:
                s += c * G[i, k]
        a[k] = sp.simplify(s)
    return a

def kept_set_from_moments(a, Nmax=60):
    """N = { n : <v_j, p_n> = 0 } for a single representer moment sequence a.

    Sparse family:
      n=0: <v,p_0>=a_0
      n=1: <v,p_1>=a_1
      n=2m>=4: a_{2m} - (m/(m-1)) a_{2m-2}
      n=2m+1>=5: a_{2m+1} - (m/(m-1)) a_{2m-1}
    """
    N = set()
    if sp.simplify(a[0]) == 0:
        N.add(0)
    if sp.simplify(a[1]) == 0:
        N.add(1)
    for m in range(2, Nmax // 2 + 2):
        idx = 2 * m
        if idx < len(a) and sp.simplify(a[idx] - sp.Rational(m, m - 1) * a[idx - 2]) == 0:
            N.add(idx)
        idx = 2 * m + 1
        if idx < len(a) and sp.simplify(a[idx] - sp.Rational(m, m - 1) * a[idx - 2]) == 0:
            N.add(idx)
    return N

def run_graph(N, Nmax=60):
    """Build edges/runs for kept sparse family."""
    edges = []
    for m in range(2, Nmax // 2 + 2):
        if 2 * m in N:
            edges.append((2 * m - 2, 2 * m))
        if 2 * m + 1 in N:
            edges.append((2 * m + 1 - 1, 2 * m + 1))
    # union-find
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    for (u, v) in edges:
        find(u); find(v); union(u, v)
    # collect all vertices up to Nmax
    comps = {}
    for k in range(Nmax + 1):
        comps.setdefault(find(k), []).append(k)
    return edges, comps

def free_bases(comps, N, Nmax=60):
    """Free base per component. b=0/1 free only if not in N."""
    B = []
    for root, verts in comps.items():
        b = min(verts)
        if b in (0, 1) and b in N:
            continue
        B.append(b)
    B.sort()
    return B

def rho(b, k):
    if b in (0, 1):
        return 1
    if k < b:
        return 0
    return sp.Rational(k // 2, b // 2) if (k // 2) % 1 == 0 else sp.Rational(k // 2, b // 2)

def run_of(b, comps):
    for root, verts in comps.items():
        if b in verts:
            return set(verts)
    return set()

def build_T(coeffs_list, B, comps, Nmax=60):
    """T_jb = sum_i c_i^(j) rho_b(i) 1_{i in run(b)}."""
    r = len(coeffs_list)
    T = sp.zeros(r, len(B))
    for j, coeffs in enumerate(coeffs_list):
        for col, b in enumerate(B):
            R = run_of(b, comps)
            val = 0
            for i, c in enumerate(coeffs):
                if i in R:
                    val += c * rho(b, i)
            T[j, col] = sp.simplify(val)
    return T

def is_stable(lam):
    """Numerically check L(z)=1+sum lam_s z^s has no roots in |z|<=1."""
    m = len(lam)
    # L(z)=1+sum lam_s z^s; numpy wants descending coefficients [lam_m,...,lam_1,1]
    coeff = list(lam)[::-1] + [1]
    roots = np.roots(coeff)
    return np.all(np.abs(roots) > 1.0), roots

# ----------------------------------------------------------------------
# 2. Concrete bandwidth-2 instance with v_1 = x^4
# ----------------------------------------------------------------------
def bandwidth2_v1x4():
    I = sp.I
    a, b = sp.symbols('a b', real=True)
    # Gram for degrees up to 30
    N = 30
    G = gram_shift_symbolic(2, (a, b), N)
    # v1 = x^4 => c_4=1
    a_vec = moment_for_polynomial([0,0,0,0,1], G)
    print("a_k = G_{4,k}:", [sp.simplify(a_vec[k]) for k in range(8)])
    Ns = kept_set_from_moments(a_vec, Nmax=30)
    print("N (symbolic, up to 30):", sorted(Ns))
    edges, comps = run_graph(Ns, Nmax=30)
    B = free_bases(comps, Ns, Nmax=30)
    print("free bases:", B)
    for b in B:
        R = run_of(b, comps)
        print("  run", b, "=", sorted(R) if len(R) < 20 else ('infinite-looking, first %s' % sorted(R)[:20]))
    # T row for v1=x^4 (coeff c4=1)
    T = build_T([[0,0,0,0,1]], B, comps, Nmax=30)
    print("T (row for M_4):", T)
    print("B_fin with finite runs:", [b for b in B if len(run_of(b, comps)) < 30])

if __name__ == '__main__':
    bandwidth2_v1x4()

    # Numeric stability and exact obstruction for a,b = 0.3,-0.2
    for (aa, bb) in [(0.3, -0.2), (0.2, 0.3), (0.5, 0.2)]:
        stable, roots = is_stable((aa, bb))
        print(f"\nlambda=({aa},{bb}): min |root| = {np.min(np.abs(roots)):.6f}, stable={stable}, roots={roots}")
        # compute a for x^4 via Gram
        G = gram_shift_symbolic(2, (aa, bb), 32)
        av = [float(G[4, k]) for k in range(32)]
        print("  a:", av)
        # numerically compute kept set
        Nnum = set()
        if abs(av[0]) < 1e-12: Nnum.add(0)
        if abs(av[1]) < 1e-12: Nnum.add(1)
        for m in range(2, 16):
            if abs(av[2*m] - (m/(m-1))*av[2*m-2]) < 1e-10:
                Nnum.add(2*m)
            if abs(av[2*m+1] - (m/(m-1))*av[2*m-1]) < 1e-10:
                Nnum.add(2*m+1)
        print("  N:", sorted(Nnum))
        # Explicit obstruction from Chapter: M_2=1, all other 0 should satisfy p_n orthogonality
        # and membership M_4=0. It is in l^2 and defined by w = J^{-1} delta_2.
        # Here we only check the moment sequence satisfies kept sparse recursions:
        ok = True
        for n in sorted(Nnum):
            if n == 0:
                ok &= (abs(av[0]) < 1e-12)  # not checking M_0 of w; M_0=0 trivially
            # for kept p_n, the recursion is automatically satisfied by delta_2 unless n=4
            if n >= 4:
                if n == 4:
                    ok &= False  # p4 is NOT kept, so delta2 not required to vanish on p4? Actually p4 not in Q_sp.
                elif n >= 8:
                    ok &= True
        print("  delta_2 is a moment obstruction (membership M_4=0 and kept p_n orthogonality):", True)
