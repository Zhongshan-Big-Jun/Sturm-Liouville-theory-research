# densbc_v6_exact_recursion.py
# EVIDENCE (not a proof).  Exact-rational verification of the recursion
# structure that underpins Theorem E (corrected diagonal classification).
#
# Verify with exact integer/fraction arithmetic (fractions.Fraction) that the
# maximal-run free-parameter decomposition satisfies the moment recursion of
# EVERY kept sparse p_n exactly:
#   p_n kept  <=> support {n, n-2} disjoint from R (n in {0,1,4,5,...}).
#   M_{2m} = (m/(m-1)) M_{2m-2} when both 2m, 2m-2 unconstrained.
# We assign, on each maximal run [lo,hi] of unconstrained same-parity degrees,
#   M_{2k} = (k/lo) * 1  (even) and M_{2k'+1} = ((k'+1)/lo) * 1 (odd),
# M = 0 off-runs and at constrained degrees.  Then every kept p_n must be
# orthogonal (exact rational zero).

from fractions import Fraction as F

def pn_exact(n):
    if n == 0: return {0: F(1)}
    if n == 1: return {1: F(1)}
    if n % 2 == 0:
        mp = n // 2
        return {n: F(1), n-2: -F(mp, mp-1)}
    else:
        mp = (n+1)//2
        return {n: F(1), n-2: -F(mp, mp-1)}

def runs(R, parity, top):
    # parity True -> even degrees {2,4,6,...}; parity False -> odd {3,5,7,...}
    # (degree 1 is NOT a recursion site: p_1=x always forces M_1=0 if 1 not in R)
    lo0 = 2 if parity else 3
    ds = sorted(d for d in range(lo0, top, 2) if d not in R)
    out = []
    i = 0
    while i < len(ds):
        j = i
        while j+1 < len(ds) and ds[j+1] == ds[j]+2:
            j += 1
        out.append((ds[i], ds[j]))
        i = j+1
    return out

def moment(R, top):
    even_runs = runs(R, True, top)
    odd_runs  = runs(R, False, top)
    def M(k):
        if k == 0 or k == 1:
            return F(0)   # M_0 and M_1 pinned to 0 (p_0=1, p_1=x if kept)
        if k % 2 == 0:
            for (lo, hi) in even_runs:
                if lo <= k <= hi:
                    m0 = lo // 2
                    return F(k // 2) / m0
            return F(0)
        else:
            for (lo, hi) in odd_runs:
                if lo <= k <= hi:
                    m0 = (lo + 1) // 2
                    return F((k + 1) // 2) / m0
            return F(0)
    return M

def verify(R, top=80):
    M = moment(R, top)
    pad = 0
    first = []
    for n in range(0, top):
        if n in (2, 3):
            continue
        co = pn_exact(n)
        if any(d in R for d in co):
            continue
        val = sum(M(d) * c for d, c in co.items())
        if val != 0:
            pad += 1
            if len(first) < 5:
                first.append((n, val))
    fin = []
    for (lo, hi) in runs(R, True, 400):
        if hi < 399: fin.append(('even', lo, hi))
    for (lo, hi) in runs(R, False, 400):
        if hi < 399: fin.append(('odd', lo, hi))
    return pad, first, fin

if __name__ == "__main__":
    cases = [(2,3),(2,),(4,),(2,4),(2,3,4),(2,6),(4,8),(3,9),(2,3,11),(1,2),(0,2,3)]
    print("Exact-rational check of the run/free-parameter decomposition.")
    print("pad = number of kept p_n with NONZERO (w,p_n).  Expected 0 for all.")
    print()
    for R in cases:
        pad, first, fin = verify(R)
        fs = ", ".join(f"{p}[{l}-{h}]" for (p, l, h) in fin[:4]) or "none"
        print(f"R={str(list(R)):16s}: pad={pad}  first_nonz={first[:2]}  finite_runs={fs}")
    print()
    print("Interpretation: pad==0 everywhere => the maximal-run decomposition gives")
    print("an EXACT orthogonal w for every R, hence the finite-run/infinite-run test")
    print("is the complete obstruction criterion (density follows iff beta<=3/2 and")
    print("no finite run).")
