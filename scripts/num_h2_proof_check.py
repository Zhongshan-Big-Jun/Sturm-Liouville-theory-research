# -*- coding: utf-8 -*-
"""Independent exact-rational verification of the H^2 analytic-completeness proof.
Checks: (A) inner-product identity (f,g)_{2,c} == (Kc f, Kc g)_L2
(B) moment-jump recurrence + growth lemma bound  u_j >= (4/c)^{j-1} j!
(C) L^2 projection residuals of x^2, x^3 onto span{Kc p_n} -> 0
(D) Gram nonsingularity of {Kc p_n} on [-1,1]
Uses fractions.Fraction only (no float) for (A)(B)(D) and moderate-N parts of (C)."""
from fractions import Fraction as F
from math import factorial

def l2_inner(p, q):
    """Exact L^2(-1,1) inner product of coefficient lists (ascending powers)."""
    n = max(len(p), len(q))
    P = list(p) + [F(0)] * (n - len(p))
    Q = list(q) + [F(0)] * (n - len(q))
    s = F(0)
    for j in range(n):
        for k in range(n):
            if (j + k) % 2 == 0:
                s += P[j] * Q[k] * F(2, j + k + 1)
    return s

def kc_apply(p, c):
    """K_c = -d^2/dx^2 + c on coefficient list; output length len(p) (no dropping!)."""
    n = len(p) - 1
    out = [F(0)] * (n + 1)
    for j in range(n + 1):
        out[j] += c * p[j]
        if j + 2 <= n:
            out[j] -= F((j + 1) * (j + 2)) * p[j + 2]
    return out

def bc_residual(p):
    """q'(1) - (q(1)-q(-1))/2 and q'(-1) - (q(1)-q(-1))/2 as exact Fractions."""
    der = [F(k) * p[k] for k in range(1, len(p))]
    def ev(q, x):
        return sum(a * (x ** k) for k, a in enumerate(q))
    d1 = ev(der, F(1)); dm1 = ev(der, F(-1))
    val = (ev(p, F(1)) - ev(p, F(-1))) / 2
    return (d1 - val, dm1 - val)

def p_basis(deg_max, c):
    """Return dict degree -> coefficient list for basis polynomials p_n in H^2."""
    out = {}
    for k in range(deg_max + 1):
        if k in (2, 3):
            continue
        cc = [F(0)] * (k + 1)
        cc[k] = F(1)
        n = k // 2
        if n != 1 and k >= 4:
            cc[k - 2] = -F(n, n - 1)
        r1, r2 = bc_residual(cc)
        assert r1 == 0 and r2 == 0, (k, r1, r2)
        out[k] = cc
    return out

def h2_inner(p, q, c):
    """(f,g)_{2,c} by the displayed formula (complex-conj-free real case)."""
    n = max(len(p), len(q))
    P = list(p) + [F(0)] * (n - len(p))
    Q = list(q) + [F(0)] * (n - len(q))
    def ev(r, x): return sum(a * (x ** k) for k, a in enumerate(r))
    def d2(r):
        return [F((k + 1) * (k + 2)) * r[k + 2] for k in range(len(r) - 2)]
    term = -c * (ev(P, F(1)) - ev(P, F(-1))) * (ev(Q, F(1)) - ev(Q, F(-1)))
    term += l2_inner(d2(P), d2(Q)) + 2 * c * l2_inner([F(k) * P[k] for k in range(1, len(P))],
                                                      [F(k) * Q[k] for k in range(1, len(Q))])
    term += c * c * l2_inner(P, Q)
    return term

print("== (A) identity (f,g)_{2,c} == (Kc f, Kc g)_L2, exact, degrees <= 9 ==")
for c in (F(1), F(3), F(5)):
    basis = p_basis(9, c)
    degs = sorted(basis)
    ok = True
    for i, d in enumerate(degs):
        for e in degs[i:]:
            lhs = h2_inner(basis[d], basis[e], c)
            rhs = l2_inner(kc_apply(basis[d], c), kc_apply(basis[e], c))
            if lhs != rhs:
                ok = False
                print("  MISMATCH c=%s d=%d e=%d" % (c, d, e))
    print("  c=%s: %d pairs, all equal = %s" % (c, len(degs) * (len(degs) + 1) // 2, ok))

print()
print("== (B) moment recurrence + growth bound u_j >= (4/c)^{j-1} j! ==")
def moments_seq(c, J):
    A = lambda j: F(2 * j * (2 * j - 1)) + c * F(j) / (j - 1)
    B = lambda j: F(2 * j * (2 * j - 3))
    u = [F(0), F(1)]
    for j in range(2, J + 1):
        u.append((A(j) * u[j - 1] - B(j) * u[j - 2]) / c)
    return u

for c in (F(1), F(3), F(5)):
    u = moments_seq(c, 24)
    ok = True
    for j in range(1, 25):
        lb = F(4, c) ** (j - 1) * F(factorial(j))
        if not (u[j] > 0 and u[j] >= u[j - 1] and u[j] >= lb):
            ok = False
            print("  FAIL c=%s j=%d u_j=%s lb=%s" % (c, j, u[j], lb))
    print("  c=%s: u_12 ~ %s ; bound holds for j<=24 = %s" % (c, u[12], ok))
    print("         u_24 has %d digits" % len(str(u[24])))

print()
print("== (C) L^2 projection residuals of x^2, x^3 onto span{Kc p_n}, deg<=N ==")
import numpy as np
def float_l2(p, q):
    n = max(len(p), len(q))
    P = np.zeros(n + 1); Q = np.zeros(n + 1)
    P[:len(p)] = p; Q[:len(q)] = q
    s = 0.0
    for j in range(n + 1):
        for k in range(n + 1):
            if (j + k) % 2 == 0:
                s += P[j] * Q[k] * 2.0 / (j + k + 1)
    return s
c = 3.0
Nmax = 40
degs = [k for k in range(Nmax + 1) if k not in (2, 3)]
kcb = {}
for k in degs:
    n = k // 2
    cc = np.zeros(k + 1); cc[k] = 1.0
    if n != 1 and k >= 4:
        cc[k - 2] = -n / (n - 1)
    kcb[k] = kc_apply([float(x) for x in cc], c)
for target in (2, 3):
    f = np.zeros(target + 1); f[target] = 1.0
    kf = kc_apply(list(f), c)
    f2 = float_l2(kf, kf)
    print("  target x^%d:" % target)
    for N in (6, 10, 16, 24, 32, 40):
        idx = [k for k in degs if k <= N]
        G = np.array([[float_l2(kcb[i], kcb[j]) for j in idx] for i in idx])
        rhs = np.array([float_l2(kf, kcb[j]) for j in idx])
        x = np.linalg.solve(G, rhs)
        resid = max(f2 - x @ G @ x, 0.0)
        print("    N=%2d residual = %.3e" % (N, resid))

print()
print("== (D) Gram matrix of {Kc p_n} nonsingular (exact), deg<=11, c=3 ==")
c = F(3)
basis = p_basis(11, c)
degs = sorted(basis)
G = [[l2_inner(kc_apply(basis[d], c), kc_apply(basis[e], c)) for e in degs] for d in degs]
# exact Gaussian elimination determinant check
import copy
M = [row[:] for row in G]
det = F(1); n = len(M)
for i in range(n):
    pvt = next((r for r in range(i, n) if M[r][i] != 0), None)
    if pvt is None:
        det = F(0); break
    if pvt != i:
        M[i], M[pvt] = M[pvt], M[i]; det = -det
    det *= M[i][i]
    inv = 1 / M[i][i]
    for r in range(i + 1, n):
        fac = M[r][i] * inv
        if fac != 0:
            for ccol in range(i, n):
                M[r][ccol] -= fac * M[i][ccol]
print("  exact det of 10x10 Gram (deg 0,1,4..11) = %s  (nonzero = %s)" % (det, det != 0))
