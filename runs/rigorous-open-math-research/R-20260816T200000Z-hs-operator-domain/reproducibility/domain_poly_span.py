# domain_poly_span.py
# Exact description of D(K_c^r) intersect polynomials (degree <= N),
# for the Krein Laplacian.  We find the linear span (as exact rational functions
# of c) of all polynomials of degree <= N that lie in D(K_c^r).
#
# D(K_c^r) = { f : K_c^j f in D(K_c), j = 0..r-1 }
# Krein BC for f: f'(1) = f'(-1) = (f(1)-f(-1))/2.
#
# We parametrize a general polynomial p of degree <= N, impose all r*2 linear
# Krein conditions (each smooth), and read off the solution space structure.

import sympy as sp

x, c = sp.symbols('x c', positive=True)

def K_poly(p):
    return sp.expand(c * p - sp.diff(p, x, 2))

def krein_conditions(f):
    # returns [condition1, condition2]  (both must be 0)
    d1 = sp.expand(sp.diff(f, x, 1).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x, 1).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return [sp.expand(d1 - avg), sp.expand(dm1 - avg)]

def poly_span_in_DKr(r, N, cval=None):
    # general polynomial p of degree <= N with symbolic coefficients a_0..a_N
    coeffs = sp.symbols('a0:%d' % (N + 1))
    p = sum(coeffs[k] * x ** k for k in range(N + 1))
    # impose conditions: for j in 0..r-1, K_c^j p in D(K_c)
    conds = []
    cur = p
    for j in range(r):
        conds.extend(krein_conditions(cur))
        cur = K_poly(cur)
    # Each cond is a linear expression in coeffs with coefficients rational in c.
    # Build matrix M and solve M * a = 0 over Rational(c) if cval given else symbolic.
    if cval is not None:
        M = []
        for cond in conds:
            row = []
            for k0 in range(N + 1):
                row.append(sp.expand(sp.diff(cond, coeffs[k0])))
            M.append(row)
        # verify cond == sum row*coeffs
        for cond, row in zip(conds, M):
            check = sum(row[k0] * coeffs[k0] for k0 in range(N + 1))
            assert sp.expand(check - cond) == 0, 'linear check failed'
        Msp = sp.Matrix(M)
        ns = Msp.nullspace()
        # ns: list of vectors in coeff coordinates
        basis = []
        for v in ns:
            poly = sum(sp.expand(v[k0]) * x ** k0 for k0 in range(N + 1))
            basis.append(sp.expand(poly))
        return basis, Msp
    else:
        return None

print('=== For a SPECIFIC c value: polynomial solutions in D(K_c^r), degree <= N ===')
# use c = 3 (generic)
for r in [1, 2, 3]:
    for N in [6, 8]:
        basis, M = poly_span_in_DKr(r, N, cval=3)
        print('r=%d N=%d : nullspace dim=%d' % (r, N, len(basis)))
        for b in basis:
            print('   ', sp.factor(b))
    print()

print('=== Same with symbolic c (degree <= 8) — show coefficients are rational fns of c ===')
for r in [1, 2, 3]:
    basis, M = poly_span_in_DKr(r, 8, cval=sp.Rational(1) * 3)  # c=3 as rational
    print('r=%d N=8 nullspace dim=%d' % (r, len(basis)))
    for b in basis:
        print('   ', sp.factor(b))
    print()
