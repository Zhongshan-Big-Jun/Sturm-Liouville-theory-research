# -*- coding: utf-8 -*-
"""Explore H^m polynomial subspaces and completeness for m = 3, 4, 5.
Exact rational for polynomial inner products; high-precision Gauss-Legendre for trig tests."""
from fractions import Fraction as F
import numpy as np

def l2(p, q):
    n = max(len(p), len(q)); P = list(p) + [F(0)]*(n-len(p)); Q = list(q) + [F(0)]*(n-len(q))
    s = F(0)
    for j in range(n):
        for k in range(n):
            if (j+k) % 2 == 0: s += P[j]*Q[k]*F(2, j+k+1)
    return s

def ev(p, x):
    if isinstance(x, F): return sum(a*x**k for k, a in enumerate(p))
    return sum(float(a)*x**k for k, a in enumerate(p))

def deriv(p):
    return [F(k)*p[k] for k in range(1, len(p))]

def bc1_residual(p):
    d1 = ev(deriv(p), F(1)); dm1 = ev(deriv(p), F(-1))
    val = (ev(p, F(1)) - ev(p, F(-1)))/2
    return (d1 - val, dm1 - val)

def kc(p, c):
    n = len(p)-1; out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return out

def h2_inner(p, q, c):
    return l2(kc(p, c), kc(q, c))

def h1_inner(p, q, c):
    """(f,g)_{1,c} = -Delta f Delta g /2 + int (f'g' + c f g)"""
    term = -F(1,2)*(ev(p,F(1))-ev(p,F(-1)))*(ev(q,F(1))-ev(q,F(-1)))
    return term + l2(deriv(p), deriv(q)) + c*l2(p, q)

def h3_inner(p, q, c):
    """(f,g)_3 = (Kc f, Kc g)_1 for polynomials (p in P^(3))"""
    return h1_inner(kc(p, c), kc(q, c), c)

def h4_inner(p, q, c):
    return l2(kc(kc(p, c), c), kc(kc(q, c), c))

# ---------- Part A: polynomial subspaces of H^m ----------
c = F(3)
# P^(2): q in H^2.  P^(4): q, Kc q in H^2.  P^(6): q, Kc q, Kc^2 q in H^2.
for m, cond in [("H2", lambda q, c: abs(bc1_residual(q)[0])==0 and abs(bc1_residual(q)[1])==0),
                ("H4", lambda q, c: all(abs(r)==0 for r in bc1_residual(q)+bc1_residual(kc(q,c)))),
                ("H6", lambda q, c: all(abs(r)==0 for r in bc1_residual(q)+bc1_residual(kc(q,c))+bc1_residual(kc(kc(q,c),c))))]:
    print(f"== {m} polynomial subspace: degrees and basis (c={c}) ==")
    for d in range(0, 13):
        if d in (2,3) and m in ("H2","H4","H6"):
            # check if any degree-d poly in the space
            pass
        # solve: monic poly of degree d satisfying cond, via null space
        # unknowns: coefficients a_0..a_{d-1} (leading 1)
        n_cond = 2 if m == "H2" else (4 if m == "H4" else 6)
        A = []; b = []
        # build linear map: for each condition, express as linear functional on coeffs
        # conditions are bc1 residuals of q, Kc q, Kc^2 q: each is 2 linear equations
        def residual_vector(p, c):
            return [bc1_residual(p)[0], bc1_residual(p)[1],
                    bc1_residual(kc(p,c))[0], bc1_residual(kc(p,c))[1],
                    bc1_residual(kc(kc(p,c),c))[0], bc1_residual(kc(kc(p,c),c))[1]]
        n_eq = 2 if m=="H2" else (4 if m=="H4" else 6)
        eqs = []
        for j in range(n_eq):
            # residual_j(p) as linear form in a_0..a_{d-1}
            row = [F(0)]*d
            for k in range(d):
                p = [F(0)]*(d+1); p[k] = F(1)
                row[k] = residual_vector(p, c)[j]
            bj = -residual_vector([F(0)]*d + [F(1)], c)[j]
            eqs.append((row, bj))
        # solve linear system (Gaussian elimination) -> parametrize solutions
        # build augmented matrix
        M = [row + [bj] for row, bj in eqs]
        # find rank and whether consistent; also dimension of solution space
        from fractions import Fraction
        def rref(mat):
            M = [row[:] for row in mat]; nrows = len(M); ncols = len(M[0]); piv = 0
            for r in range(nrows):
                if piv >= ncols: break
                pv = next((rr for rr in range(r, nrows) if M[rr][piv] != 0), None)
                if pv is None: piv += 1; continue
                M[r], M[pv] = M[pv], M[r]
                fac = M[r][piv]; M[r] = [x/fac for x in M[r]]
                for rr in range(nrows):
                    if rr != r and M[rr][piv] != 0:
                        f = M[rr][piv]; M[rr] = [x - f*y for x, y in zip(M[rr], M[r])]
                piv += 1
            return M
        R = rref(M)
        consistent = all(all(x == 0 for x in row[:-1]) or row[-1] != 0 or True for row in R)
        # check consistency: any row all-zero coeffs but nonzero rhs
        inconsistent = any(all(x==0 for x in row[:-1]) and row[-1]!=0 for row in R)
        if inconsistent:
            print(f"  degree {d}: NO polynomial in {m}")
            continue
        n_free = d - sum(1 for row in R if any(x != 0 for x in row[:-1]))
        if n_free <= 0:
            print(f"  degree {d}: NO polynomial in {m} (n_free={n_free})")
            continue
        # build a basis: for each free variable, set to 1 others 0
        piv_cols = []
        for row in R:
            pc = next((i for i, x in enumerate(row[:-1]) if x != 0), None)
            if pc is not None: piv_cols.append(pc)
        free_cols = [i for i in range(d) if i not in piv_cols]
        basis = []
        for fcol in free_cols:
            sol = [F(0)]*d
            sol[fcol] = F(1)
            for row in R:
                pc = next((i for i, x in enumerate(row[:-1]) if x != 0), None)
                if pc is None: continue
                sol[pc] = row[-1] - sum(row[i]*sol[i] for i in range(d) if i != pc)
            basis.append([F(1)] + sol)  # monic with leading 1
        if basis:
            print(f"  degree {d}: dim = {len(basis)}")
            for bi in basis[:2]:
                s = " + ".join(f"({a})x^{k}" for k, a in enumerate(bi) if a != 0)
                print(f"     {s}")
