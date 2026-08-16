# degree_structure.py
# Verify: for r=1,2,3, D(K_c^r) intersect polynomials has:
#  (i)  1, x always;
#  (ii) at least one polynomial of EVERY degree d >= some threshold D_r;
#  (iii) exact minimal degree present (should be 2r+2).
# We impose the r*2 Krein conditions on a general polynomial of degree <= N and
# examine which degrees appear in the nullspace (via rank profile / leading coefficients).

import sympy as sp

x, c = sp.symbols('x c', positive=True)
C = sp.Integer(3)  # generic c value for structure (positive)

def K_poly(p):
    return sp.expand(C * p - sp.diff(p, x, 2))

def krein_conditions(f):
    d1 = sp.expand(sp.diff(f, x, 1).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x, 1).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return [sp.expand(d1 - avg), sp.expand(dm1 - avg)]

def degrees_present(r, N):
    coeffs = sp.symbols('a0:%d' % (N + 1))
    p = sum(coeffs[k] * x ** k for k in range(N + 1))
    conds = []
    cur = p
    for j in range(r):
        conds.extend(krein_conditions(cur))
        cur = K_poly(cur)
    M = []
    for cond in conds:
        row = []
        for k0 in range(N + 1):
            row.append(sp.expand(sp.diff(cond, coeffs[k0])))
        M.append(row)
    Msp = sp.Matrix(M)
    ns = Msp.nullspace()
    # which degrees are present in some basis vector
    present = set()
    min_deg = None
    for v in ns:
        degs = [k0 for k0 in range(N + 1) if sp.simplify(v[k0]) != 0]
        for d in degs:
            present.add(d)
        if degs:
            dmin = min(degs)
            if min_deg is None or dmin < min_deg:
                min_deg = dmin
    return min_deg, sorted(present)

for r in [1, 2, 3]:
    print('=== r=%d (D(K_c^%d) intersect polys) ===' % (r, r))
    for N in [6, 8, 10, 12]:
        min_deg, present = degrees_present(r, N)
        missing = [d for d in range(0, N + 1) if d not in present]
        print('  N=%2d : min_deg=%s, degrees present count=%d, missing=%s' % (
            N, min_deg, len(present), missing))
    print()
