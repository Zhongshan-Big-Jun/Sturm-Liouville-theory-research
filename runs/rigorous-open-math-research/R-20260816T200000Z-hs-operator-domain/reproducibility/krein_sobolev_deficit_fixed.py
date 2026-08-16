# krein_sobolev_deficit_fixed.py
# Fixed Krein-Sobolev (S_m = P_m - P_{m-2} with P_{-1}=P_{-2}=0 convention)
# and exact Krein deficit of f_n = K_c^{-1}K_n.

import sympy as sp

x, c = sp.symbols('x c', positive=True)

def K_inv_poly(p):
    out = 0
    pj = p
    j = 0
    while True:
        out += c**(-1) * c**(-j) * pj
        pj = sp.expand(sp.diff(pj, x, 2))
        if pj == 0:
            break
        j += 1
    return sp.expand(out)

def krein_sobolev(n):
    a = {0: 1, 1: 1, 2: 1, 3: 1}
    for m in range(2, n + 1):
        if (m + 2) not in a:
            a[m + 2] = sp.expand(a[m] * (1 + (4 * m * m - 1) / c)
                                 + sp.Rational(2 * m + 1, 2 * m - 3) * (a[m] - a[m - 2]))
    def Pm(m):
        if m < 0:
            return 0
        return sp.legendre(m, x)
    def S(m):
        if m < 0:
            return 0
        return sp.expand(Pm(m) - Pm(m - 2))
    out = 0
    for r_ in range(0, n // 2 + 1):
        out += a[n - 2 * r_] * S(n - 2 * r_)
    return sp.expand(out)

print('=== Validate K_n vs doc closed forms ===')
doc = {
    0: '1', 1: 'x',
    2: '3/2*x**2 - 1/2',
    3: '5/2*x**3 - 3/2*x',
    4: '(35*c+525)/(8*c)*x**4 - (30*c+630)/(8*c)*x**2 + (3*c+105)/(8*c)',
}
for n in range(0, 5):
    mine = krein_sobolev(n)
    ed = sp.sympify(doc[n])
    print('n=%d match_doc=%s' % (n, sp.expand(mine - ed) == 0))

print()
print('=== Is K_c^{-1}K_n in D(K_c)? ===')
for n in range(0, 9):
    Kn = krein_sobolev(n)
    fn = K_inv_poly(Kn)
    d1 = sp.expand(sp.diff(fn, x).subs(x, 1))
    dm1 = sp.expand(sp.diff(fn, x).subs(x, -1))
    avg = sp.expand((fn.subs(x, 1) - fn.subs(x, -1)) / 2)
    print('n=%d Kc^-1K_n in D(Kc)=%s' % (n, (d1 - avg == 0) and (dm1 - avg == 0)))

print()
print('=== Krein deficit of f_n = K_c^{-1}K_n ===')
for n in [2, 3, 4, 5, 6]:
    Kn = krein_sobolev(n)
    fn = K_inv_poly(Kn)
    if n % 2 == 0:
        defi = sp.expand(sp.diff(fn, x).subs(x, 1))
        print('n=%d (even) deficit f\'(1)= %s' % (n, sp.factor(defi)))
    else:
        defi = sp.expand(sp.diff(fn, x).subs(x, 1) - fn.subs(x, 1))
        print('n=%d (odd) deficit f\'(1)-f(1)= %s' % (n, sp.factor(defi)))
