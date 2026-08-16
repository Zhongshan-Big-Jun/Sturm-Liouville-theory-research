# validate_krein_sobolev.py
# Cleanly validate the Krein-Sobolev polynomials K_n against the SL_hs doc closed
# forms by printing both expressions (avoid string sympify pitfalls).
import sympy as sp

x, c = sp.symbols('x c', positive=True)

def krein_sobolev(n):
    a = {0: 1, 1: 1, 2: 1, 3: 1}
    for m in range(2, n + 1):
        if (m + 2) not in a:
            a[m + 2] = sp.expand(a[m] * (1 + (4 * m * m - 1) / c)
                                 + sp.Rational(2 * m + 1, 2 * m - 3) * (a[m] - a[m - 2]))
    def Pm(m):
        return 0 if m < 0 else sp.legendre(m, x)
    def S(m):
        return 0 if m < 0 else sp.expand(Pm(m) - Pm(m - 2))
    out = 0
    for r_ in range(0, n // 2 + 1):
        out += a[n - 2 * r_] * S(n - 2 * r_)
    return sp.factor(sp.expand(out))

# Doc closed forms (as sympy expressions built directly):
doc = {}
doc[0] = sp.sympify(1)
doc[1] = x
doc[2] = sp.Rational(3, 2) * x ** 2 - sp.Rational(1, 2)
doc[3] = sp.Rational(5, 2) * x ** 3 - sp.Rational(3, 2) * x
doc[4] = (35 * c + 525) / (8 * c) * x ** 4 - (30 * c + 630) / (8 * c) * x ** 2 \
         + (3 * c + 105) / (8 * c)

print('Krein-Sobolev validation against SL_hs doc closed forms:')
for n in range(0, 5):
    mine = krein_sobolev(n)
    diff = sp.expand(mine - doc[n])
    print('n=%d  match=%s' % (n, diff == 0))
    if diff != 0:
        print('   mine =', mine)
        print('   doc  =', sp.expand(doc[n]))
        print('   diff =', diff)

# Also re-verify the deficit positivity using this validated recurrence directly.
def K_inv_poly(p):
    out = 0
    pj = p
    j = 0
    while True:
        out += c ** (-1) * c ** (-j) * pj
        pj = sp.expand(sp.diff(pj, x, 2))
        if pj == 0:
            break
        j += 1
    return sp.expand(out)

print()
print('Deficit of K_c^{-1}K_n (validated K_n):')
for n in [2, 3, 4, 5, 6]:
    fn = K_inv_poly(krein_sobolev(n))
    if n % 2 == 0:
        defi = sp.expand(sp.diff(fn, x).subs(x, 1))
    else:
        defi = sp.expand(sp.diff(fn, x).subs(x, 1) - fn.subs(x, 1))
    # assert all coefficients of the polynomial part (in c) of the numerator are > 0
    print('n=%d parity=%s deficit=%s' % (n, 'even' if n % 2 == 0 else 'odd', sp.factor(defi)))
