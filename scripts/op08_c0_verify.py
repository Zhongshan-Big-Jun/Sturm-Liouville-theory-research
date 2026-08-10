# -*- coding: utf-8 -*-
"""#8 verify: c->0 degenerate limit of Krein Laplacian left-definite spaces.
(A) W = span{1,x} is the radical: (1,f)_{1,0} = (x,f)_{1,0} = 0 for all f
(B) Gram determinants of {S_n : n>=2} (i.e. span{x^k: k>=2}) nonzero at c=0
(C) K_n^{(c)} norms: n=0,1 -> 0 as c->0;  n>=2 -> finite limit
(D) completeness in quotient: span{[x^k]: k>=2} dense in H^1/W (standard)
"""
import numpy as np, math

def q0(f, g):
    """(f,g)_{1,0} = int f'g' - (f(1)-f(-1))(g(1)-g(-1))/2 for polynomials (coeff ascending)."""
    def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
    def der(p): return [k*a for k, a in enumerate(p)][1:]
    n = max(len(f), len(g))
    F = list(f)+[0.0]*(n-len(f)); G = list(g)+[0.0]*(n-len(g))
    # int F' G'
    dF, dG = der(F), der(G)
    s = 0.0
    for j, a in enumerate(dF):
        for k, b in enumerate(dG):
            if (j+k) % 2 == 0:
                s += a*b*2.0/(j+k+1)
    s -= (ev(F,1)-ev(F,-1))*(ev(G,1)-ev(G,-1))/2.0
    return s

print("=== (A) W is radical ===")
for name, f in [("1",[1.0]), ("x",[0.0,1.0])]:
    for name2, g in [("x^2",[0,0,1]), ("x^3",[0,0,0,1]), ("x^7-2x^3",[0,0,0,-2,0,0,0,1])]:
        v = q0(f, g)
        print(f"  ({name}, {name2})_0 = {v:.3e}")

print("\n=== (B) Gram determinant of {x^2,...,x^N} at c=0 ===")
for N in (4, 6, 8):
    G = np.array([[q0([0.0]*k+[1.0], [0.0]*j+[1.0]) for j in range(2, N+1)] for k in range(2, N+1)])
    print(f"  N={N}: det = {np.linalg.det(G):.6e}, min eig = {np.linalg.eigvalsh(G).min():.6e}")

print("\n=== (C) Gram-Schmidt norms of K_n^{(c)} vs c ===")
# Gram matrix of S_n = P_n - P_{n-2} under (.,.)_{1,c}; K_n = orthonormalized S_n (normalized K_n(1)=1 is different scale; here use orthonormal norms)
# We compute the leading principal Gram matrix of {S_0..S_3} and its eigenvalues at c -> 0.
def legendre_coeffs(n):
    # P_n normalized P_n(1)=1, ascending coeffs (exact rational via recurrence)
    from fractions import Fraction as F
    P = [[F(1)], [F(0), F(1)]]
    for m in range(2, n+1):
        # P_m = ((2m-1)/m) x P_{m-1} - ((m-1)/m) P_{m-2}
        c = [F(0)]*(m+1)
        for k, a in enumerate(P[m-1]):
            c[k+1] += F(2*m-1, m)*a
        for k, a in enumerate(P[m-2]):
            c[k] -= F(m-1, m)*a
        P.append(c)
    return [float(a) for a in P[n]]

def qc(f, g, c):
    return q0(f, g) + c*sum(a*b*2.0/(j+k+1) for j, a in enumerate(f) for k, b in enumerate(g) if (j+k)%2==0)

for n in (0, 1, 2, 3):
    S = [list(np.zeros(n+1)) for _ in range(n+1)]
    for m in range(n+1):
        P_m = legendre_coeffs(m); P_m2 = legendre_coeffs(m-2) if m >= 2 else [0.0]*(m+1)
        S[m] = [P_m[k] - (P_m2[k] if k < len(P_m2) else 0.0) for k in range(m+1)]
    print(f"  S_{n}:", [round(float(x),4) for x in S[n]])
    for c in (1.0, 0.1, 0.01, 0.001, 0.0):
        Gm = np.array([[qc(S[i], S[j], c) for j in range(n+1)] for i in range(n+1)])
        print(f"    c={c}: Gram({n+1}x{n+1}) det = {np.linalg.det(Gm):.6e}")
