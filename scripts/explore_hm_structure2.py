# -*- coding: utf-8 -*-
"""Corrected exploration of P^(m) = H^m ∩ C[x] for m = 2,4,6 (even) via null space."""
from fractions import Fraction as F

def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def bc1(p):  # returns (q'(1)-Delta q/2, q'(-1)-Delta q/2)
    d = deriv(p); v = (ev(p, F(1)) - ev(p, F(-1)))/2
    return (ev(d, F(1)) - v, ev(d, F(-1)) - v)
def kc(p, c):
    n = len(p)-1; out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return out

def nullspace_basis(M, ncols):
    """M: list of rows (Fractions), each length ncols. Returns basis of null space."""
    M = [row[:] for row in M]; nrows = len(M)
    piv = 0; piv_cols = []
    for r in range(nrows):
        if piv >= ncols: break
        pv = next((rr for rr in range(r, nrows) if M[rr][piv] != 0), None)
        if pv is None: piv += 1; continue
        M[r], M[pv] = M[pv], M[r]
        fac = M[r][piv]; M[r] = [x/fac for x in M[r]]
        for rr in range(nrows):
            if rr != r and M[rr][piv] != 0:
                f = M[rr][piv]; M[rr] = [x - f*y for x, y in zip(M[rr], M[r])]
        piv_cols.append(piv); piv += 1
    free = [i for i in range(ncols) if i not in piv_cols]
    basis = []
    for fcol in free:
        sol = [F(0)]*ncols; sol[fcol] = F(1)
        for r, pc in enumerate(piv_cols):
            sol[pc] = -sum(M[r][i]*sol[i] for i in range(ncols) if i != pc)
        basis.append(sol)
    return basis

for k in (1, 2, 3):
    c = F(3); m = 2*k
    print(f"== P^(H^{m}): degrees present, dim of degree-<=d space (c={c}) ==")
    prev = None
    for d in range(0, 16):
        conds = []
        for j in range(k):
            # bc1 of Kc^j q: express as linear form in coeffs a_0..a_d
            for e in range(2):
                row = [F(0)]*(d+1)
                for t in range(d+1):
                    p = [F(0)]*(d+1); p[t] = F(1)
                    row[t] = bc1(kc(p, c)**0 if False else kc(p, c))[e]  # placeholder
                conds.append(row)
        # build properly
        conds = []
        for j in range(k):
            for e in range(2):
                row = [F(0)]*(d+1)
                for t in range(d+1):
                    p = [F(0)]*(d+1); p[t] = F(1)
                    kcj = p
                    for _ in range(j): kcj = kc(kcj, c)
                    row[t] = bc1(kcj)[e]
                conds.append(row)
        basis = nullspace_basis(conds, d+1)
        dim = len(basis)
        # minimal degree in basis
        mind = None
        for b in basis:
            dd = max(i for i, a in enumerate(b) if a != 0)
            mind = dd if mind is None else min(mind, dd)
        if dim != prev or d in (0,1,2,3,4,5,6,7):
            print(f"  d<= {d}: dim = {dim}")
        prev = dim
    print()
