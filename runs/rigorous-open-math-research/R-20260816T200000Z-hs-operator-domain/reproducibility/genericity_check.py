# genericity_check.py
# Confirm the degree structure of D(K_c^r) intersect polynomials is independent of c
# (generic): for c in {1,3,10}, find the minimal degree and that every degree
# >= 2r+2 present (up to N=10).  Also print explicit low-degree examples.

import sympy as sp

x = sp.symbols('x', real=True)

def K_poly(p, c):
    return sp.expand(c * p - sp.diff(p, x, 2))

def krein_conditions(f):
    d1 = sp.expand(sp.diff(f, x, 1).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x, 1).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return [sp.expand(d1 - avg), sp.expand(dm1 - avg)]

def min_and_present_degrees(r, N, cval):
    c = sp.Integer(cval)
    coeffs = sp.symbols('a0:%d' % (N + 1))
    p = sum(coeffs[k] * x ** k for k in range(N + 1))
    conds = []
    cur = p
    for j in range(r):
        conds.extend(krein_conditions(cur))
        cur = K_poly(cur, c)
    M = []
    for cond in conds:
        row = []
        for k0 in range(N + 1):
            row.append(sp.expand(sp.diff(cond, coeffs[k0])))
        M.append(row)
    Msp = sp.Matrix(M)
    ns = Msp.nullspace()
    # true exact-top-degree of each basis vector
    tops = set()
    min_deg = None
    for v in ns:
        degs = [k0 for k0 in range(N, -1, -1) if sp.simplify(v[k0]) != 0]
        if not degs:
            continue
        top = degs[0]
        tops.add(top)
        if min_deg is None or top < min_deg:
            min_deg = top
    return min_deg, sorted(tops)

for cval in [1, 3, 10]:
    print('=== c = %d ===' % cval)
    for r in [1, 2, 3]:
        min_deg, tops = min_and_present_degrees(r, 10, cval)
        # expected degrees >= 2r+2 all present? check against set
        expected_all = all(d in tops or d in [0, 1] for d in range(0, 11)
                           if d >= 2 * r + 2 or d in [0, 1])
        print('  r=%d: min_deg=%s, exact-top-degrees=%s, 2r+2=%d' % (r, min_deg, tops, 2 * r + 2))
    print()
