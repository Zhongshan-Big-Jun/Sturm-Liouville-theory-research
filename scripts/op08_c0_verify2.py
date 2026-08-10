# -*- coding: utf-8 -*-
"""#8 c->0 degenerate limit of Krein Laplacian: full audit.
(A) radical W = span{1,x} of (.,.)_{1,0}
(B) Gram matrix of {S_2..S_N} (S_n = P_n - P_{n-2}) in (.,.)_{1,0}: positive definite
(C) ||K_n||^2_{1,c} = 2c*a_n*a_{n+2}/(2n+1): n=0,1 -> 0; n=2,3 -> 6,10; n>=4 -> infinity
(D) unit-normalized system converges: u4 = K4/||K4|| -> S4/||S4|| (direction), and
    {Q_n} = GS-orthonormalization of {S_n: n>=2} in (.,.)_{1,0} is complete in H^1/W ~ L2_0.
"""
import numpy as np
from fractions import Fraction as Fr

def ip0(f, g):
    """(f,g)_{1,0} for polynomials as lists of exact Fractions (ascending)."""
    def der(p): return [Fr(k)*a for k, a in enumerate(p)][1:]
    def ev(p, x):
        if x == 1: return sum(p)
        return sum(a*Fr((-1)**k) for k, a in enumerate(p))
    n = max(len(f), len(g))
    F = f + [Fr(0)]*(n-len(f)); G = g + [Fr(0)]*(n-len(g))
    dF, dG = der(F), der(G)
    s = Fr(0)
    for j, a in enumerate(dF):
        for k, b in enumerate(dG):
            if (j+k) % 2 == 0:
                s += a*b*Fr(2, j+k+1)
    s -= (ev(F,1)-ev(F,-1))*(ev(G,1)-ev(G,-1))/Fr(2)
    return s

def ipc(f, g, c):
    """(f,g)_{1,c} = (f,g)_{1,0} + c*(f,g)_L2"""
    n = max(len(f), len(g))
    F = f + [Fr(0)]*(n-len(f)); G = g + [Fr(0)]*(n-len(g))
    s = Fr(0)
    for j, a in enumerate(F):
        for k, b in enumerate(G):
            if (j+k) % 2 == 0:
                s += a*b*Fr(2, j+k+1)
    return ip0(f, g) + c*s

def legendre(n):
    P = [[Fr(1)], [Fr(0), Fr(1)]]
    for m in range(2, n+1):
        c = [Fr(0)]*(m+1)
        for k, a in enumerate(P[m-1]):
            c[k+1] += Fr(2*m-1, m)*a
        for k, a in enumerate(P[m-2]):
            c[k] -= Fr(m-1, m)*a
        P.append(c)
    return P[n]

def S(n):
    P = legendre(n); Pm2 = legendre(n-2) if n >= 2 else [Fr(0)]*(n+1)
    return [P[k] - (Pm2[k] if k < len(Pm2) else Fr(0)) for k in range(n+1)]

print("=== (A) radical ===")
for name, f in [("1",[Fr(1)]), ("x",[Fr(0),Fr(1)])]:
    for name2, g in [("x^2",[Fr(0),Fr(0),Fr(1)]), ("S_4",S(4)), ("S_7",S(7))]:
        v = ip0(f, g)
        print(f"  ({name},{name2})_{1,0} = {v}")
print("  (f,f)_{1,0} = int f'^2 - (int f')^2/2 >= 0 by C-S; equality iff f in W")

print("\n=== (B) Gram of {S_2..S_N} in (.,.)_{1,0} ===")
for N in (4, 6, 8, 10, 12):
    G = np.array([[float(ip0(S(k), S(j))) for j in range(2, N+1)] for k in range(2, N+1)])
    det = np.linalg.det(G)
    mineig = np.linalg.eigvalsh(G).min()
    print(f"  N={N}: det={det:.6e} min_eig={mineig:.6e} (positive definite: {mineig>0})")

print("\n=== (C) ||K_n||^2_{1,c} = 2c*a_n*a_{n+2}/(2n+1) ===")
def a_seq(N, c):
    # recurrence: a_{n+2} = a_n(1+(4n^2-1)/c) + (2n+1)/(2n-3)*(a_n - a_{n-2}), a_0=a_1=a_2=a_3=1
    a = [Fr(1)]*max(4, N+3)
    for n in range(2, N+1):
        a[n+2] = a[n]*(Fr(1) + Fr(4*n*n-1)/c) + Fr(2*n+1, 2*n-3)*(a[n]-a[n-2])
    return a
for c in (Fr(1), Fr(1,10), Fr(1,100), Fr(1,1000)):
    a = a_seq(8, c)
    row = []
    for n in range(0, 7):
        norm2 = Fr(2)*c*a[n]*a[n+2]/Fr(2*n+1)
        row.append(str(norm2))
    print("  c=", float(c), " norms^2 (n=0..6):", " | ".join(row))
print("  limits: n=0:2c->0, n=1:2c/3->0, n=2:->6, n=3:->10, n=4:->inf (3150/c^2)")

print("\n=== (D) K_2=P_2, K_3=P_3; unit-normalized system converges ===")
def K_poly(n, c):
    a = a_seq(n, c)
    # K_n = sum_{r=0}^{[n/2]} a_{n-2r} S_{n-2r}
    out = [Fr(0)]*(n+1)
    for r in range(n//2 + 1):
        s = S(n-2*r)
        for k, v in enumerate(s):
            out[k] += a[n-2*r]*v
    return out

# (D1) K2, K3 c-independent
for c in (Fr(1), Fr(1,100)):
    K2, K3 = K_poly(2, c), K_poly(3, c)
    P2, P3 = legendre(2), legendre(3)
    print(f"  c={float(c)}: K2==P2: {K2==P2}, K3==P3: {K3==P3}")
    print(f"    ||K2||^2_1,c = {ipc(K2,K2,c)}  ||K3||^2_1,c = {ipc(K3,K3,c)}")

# (D2) unit-normalized u4 -> direction of S4
c = Fr(1,1000)
K4 = K_poly(4, c)
n4 = ipc(K4, K4, c)
# projection onto S4 direction in (.,.)_{1,0}
s4n = ip0(S(4), S(4))
coef = ip0(K4, S(4))/s4n
res = [v - coef*u for v, u in zip(K4, S(4)+[Fr(0)]*(len(K4)-len(S(4))))]
print(f"  c=1/1000: ||K4||^2_1,c = {n4} ; <K4,S4>_1,0/(S4,S4)_1,0 = {coef} ; residual norm^2 = {ip0(res,res)}")
print(f"  => u4 = K4/||K4|| -> +/- S4/||S4|| (residual -> 0)")

# (D3) completeness of {Q_n : n>=2} (GS of {S_n} in (.,.)_{1,0}) in H^1/W ~ L2_0:
# verify [Pi_N] = span{[S_2..S_N]} exactly by dimension and by solving a random target
rng = np.random.default_rng(1)
for N in (5, 8, 11):
    # random polynomial of degree N: solve for combination of S_2..S_N (top-down)
    target = [Fr(rng.integers(-5, 6)) for _ in range(N+1)]
    # top-down elimination: subtract multiples of S_N, S_{N-1}, ..., S_2; remainder should be degree<=1
    rem = list(target)
    for n in range(N, 1, -1):
        s = S(n) + [Fr(0)]*(len(rem)-len(S(n)))
        lead = s[n]
        co = rem[n]/lead
        rem = [rem[k] - co*s[k] for k in range(len(rem))]
    ok = all(rem[k] == 0 for k in range(2, len(rem)))
    print(f"  N={N}: [target] = comb of {[f'S_{j}' for j in range(2,N+1)]} + affine: {ok} (affine part deg<=1: {len([v for v in rem if v!=0])<=2})")
