# -*- coding: utf-8 -*-
"""Corrected: null space via proper Gauss-Jordan (keep row fixed when skipping zero column)."""
from fractions import Fraction as F

def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def bc1(p):
    d = deriv(p); v = (ev(p, F(1)) - ev(p, F(-1)))/2
    return (ev(d, F(1)) - v, ev(d, F(-1)) - v)
def kc(p, c):
    n = len(p)-1; out = [F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return out

def nullspace_basis(M, ncols):
    M = [row[:] for row in M]; nrows = len(M)
    piv = 0; piv_cols = []
    r = 0
    while r < nrows and piv < ncols:
        pv = next((rr for rr in range(r, nrows) if M[rr][piv] != 0), None)
        if pv is None:
            piv += 1
            continue
        M[r], M[pv] = M[pv], M[r]
        fac = M[r][piv]; M[r] = [x/fac for x in M[r]]
        for rr in range(nrows):
            if rr != r and M[rr][piv] != 0:
                f = M[rr][piv]; M[rr] = [x - f*y for x, y in zip(M[rr], M[r])]
        piv_cols.append(piv); piv += 1; r += 1
    free = [i for i in range(ncols) if i not in piv_cols]
    basis = []
    for fcol in free:
        sol = [F(0)]*ncols; sol[fcol] = F(1)
        for rr, pc in enumerate(piv_cols):
            sol[pc] = -sum(M[rr][i]*sol[i] for i in range(ncols) if i != pc)
        basis.append(sol)
    return basis

for k in (1, 2, 3):
    c = F(3); m = 2*k
    print(f"== P^(H^{m}): dim of degree-<=d space, and minimal new degree per dimension jump (c={c}) ==")
    prev = -1
    jumps = []
    for d in range(0, 16):
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
        dim = len(nullspace_basis(conds, d+1))
        if dim > prev: jumps.append((d, dim - prev))
        prev = dim
    print("  dims by degree cap:", [len(nullspace_basis([ [F(0)]*(dd+1) for _ in () ] and
        [ row for row in [] ] , dd+1)) for dd in range(0)] or "(see jumps)")
    print("  dimension jumps (degree, +dim):", jumps)
