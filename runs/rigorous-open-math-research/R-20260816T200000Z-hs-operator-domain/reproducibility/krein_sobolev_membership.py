# krein_sobolev_membership.py
# For ODD s = 2r+1, the SL_hs system is Q_n^{(2r+1)} = K_c^{-r} K_n (Krein-Sobolev).
# Membership in H^{2r+1} = D(K_c^{r+1/2}) requires K_c^{-m} K_n in D(K_c) for m=1..r
# and K_n in H^1.  We check K_c^{-1}K_n in D(K_c) for small n exactly.

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

def in_DKc(f):
    d1 = sp.expand(sp.diff(f, x, 1).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x, 1).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return (d1 - avg == 0) and (dm1 - avg == 0)

def krein_sobolev(n, cval):
    # K_n from the closed forms in SL_hs doc:
    # K_n = sum_{r=0}^{floor(n/2)} a_{n-2r} S_{n-2r}, S_m = P_m - P_{m-2}
    # with a_0=a_1=a_2=a_3=1 and the given recurrences.  We compute symbolic in symbols.
    # Define a_m for m up to n symbolically using the doc recurrence (9):
    # a_{m+2} = a_m (1 + (4m^2-1)/c) + ((2m+1)/(2m-3)) (a_m - a_{m-2}), m>=2
    a = {0: 1, 1: 1, 2: 1, 3: 1}
    for m in range(2, n + 1):
        if (m + 2) not in a:
            a[m + 2] = sp.expand(a[m] * (1 + (4 * m * m - 1) / c) + sp.Rational(2 * m + 1, 2 * m - 3) * (a[m] - a[m - 2]))
    def P(m):
        return sp.legendre(m, x)
    def S(m):
        if m < 0:
            return 0
        if m == 0:
            return sp.legendre(0, x)
        return sp.expand(P(m) - P(m - 2))
    out = 0
    for r_ in range(0, n // 2 + 1):
        out += a[n - 2 * r_] * S(n - 2 * r_)
    return sp.expand(out)

print('=== Odd case: is K_c^{-1}K_n in D(K_c)?  (K_n = Krein-Sobolev) ===')
for n in range(0, 9):
    Kn = krein_sobolev(n, c)
    f = K_inv_poly(Kn)
    print('n=%d Kc^-1 K_n in D(Kc) = %s' % (n, in_DKc(f)))

print()
print('=== Also verify K_n itself is in H^1 = D(K_c^{1/2}) trivially (all polys),')
print('    and Kc^{-1}K_n in D(Kc) is the binding condition. ===')

print()
print('=== For the even case cross-check: Q_n^{(2r)}=Kc^{-r}P_n in D(Kc^r) ===')
for r in [1, 2]:
    for n in [0, 1, 2, 4]:
        q = K_inv_poly(sp.legendre(n, x))
        for _ in range(r - 1):
            q = K_inv_poly(q)
        # check all K^j q in D(Kc)
        ok = True
        cur = q
        for j in range(r):
            if not in_DKc(cur):
                ok = False
                break
            cur = sp.expand(c * cur - sp.diff(cur, x, 2))
        print('r=%d n=%d Q_n in D(Kc^r)=%s' % (r, n, ok))
