# -*- coding: utf-8 -*-
"""Explicit H^2-orthogonalization of the polynomial basis {p_n} for the shifted Krein
Laplacian K_c = -d^2/dx^2 + c (Krein BC f'(±1) = (f(1)-f(-1))/2).

Key equivalence: (p,q)_{2,c} = (K_c p, K_c q)_{L^2}, so orthogonalizing {p_n} in H^2
is the pull-back of L^2-orthogonalizing {K_c p_n}.  Parity separates, so the
H^2-orthogonal basis is parity-pure: even q_0,q_4,q_6,... and odd q_1,q_5,q_7,...
(degrees 2,3 absent: no polynomial of degree 2 or 3 lies in H^2).

Usage: python h2_gs_orthogonal.py
"""
from fractions import Fraction as F

def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def addsub(a, b, s):
    """a - s*b with zero padding to equal length."""
    n = max(len(a), len(b))
    A = list(a) + [F(0)]*(n-len(a)); B = list(b) + [F(0)]*(n-len(b))
    return trim([x - s*y for x, y in zip(A, B)])

def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def kc(p, c):
    n = len(p)-1; out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return trim(out)
def l2(p, q):
    n = max(len(p), len(q)); P = list(p)+[F(0)]*(n-len(p)); Q = list(q)+[F(0)]*(n-len(q))
    return sum(P[j]*Q[k]*F(2, j+k+1) for j in range(n) for k in range(n) if (j+k) % 2 == 0)

def p_basis(N, c):
    out = {}
    for k in range(N+1):
        if k in (2, 3):
            continue
        cc = [F(0)]*(k+1); cc[k] = F(1)
        n = k//2
        if n != 1 and k >= 4:
            cc[k-2] = -F(n, n-1)
        out[k] = cc
    return out

def orthogonalize(c, N):
    basis = p_basis(N, c)
    degs = sorted(basis)
    r = {d: kc(basis[d], c) for d in degs}
    e = {}
    for d in degs:
        v = r[d][:]
        for d2 in degs:
            if d2 >= d:
                break
            den = l2(e[d2], e[d2])
            if den != 0:
                lam = l2(v, e[d2])/den
                if lam != 0:
                    v = addsub(v, e[d2], lam)
        e[d] = trim(v)
    # pull back: K_c q = r  =>  leading c*q_d = r_d; c*q_j - (j+1)(j+2) q_{j+2} = r_j
    q = {}
    for d in degs:
        rn = e[d]
        qd = [F(0)]*(d+1)
        qd[d] = rn[d]/c
        for j in range(d-1, -1, -1):
            qd[j] = (rn[j] + F((j+1)*(j+2))*qd[j+2])/c if j+2 <= d else rn[j]/c
        q[d] = trim(qd)
    return q, e, basis

def verify(c, q, degs):
    bad = []
    for i, d1 in enumerate(degs):
        for d2 in degs[i:]:
            val = l2(kc(q[d1], c), kc(q[d2], c))
            if d1 != d2 and val != 0:
                bad.append((d1, d2))
            if d1 == d2 and val == 0:
                bad.append((d1, d2, "zero self-norm"))
    return bad

def poly_str(p):
    terms = []
    for k in range(len(p)-1, -1, -1):
        if p[k] != 0:
            if k == 0:
                terms.append(str(p[k]))
            elif k == 1:
                terms.append(f"{p[k]}x")
            else:
                terms.append(f"{p[k]}x^{k}")
    return " + ".join(terms)

def show(c, N=14):
    q, e, basis = orthogonalize(c, N)
    print(f"c = {c}: unnormalized H^2-orthogonal basis (deg in {sorted(q)}):")
    for d in sorted(q):
        print(f"  q_{d} = {poly_str(q[d])}")
    bad = verify(c, q, sorted(q))
    print("  exact orthogonality violations:", bad if bad else "none")
    return q

if __name__ == "__main__":
    q3 = show(F(3), 14)
    print()
    q1 = show(F(1), 10)
