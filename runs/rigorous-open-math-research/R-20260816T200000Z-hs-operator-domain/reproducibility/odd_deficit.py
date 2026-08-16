# odd_deficit.py
# For odd Legendre P_n (n >= 3), study the Krein deficit of f_n = K_c^{-1}P_n:
#   deficit(c) := f_n'(1) - f_n(1)   (odd Krein BC: f'(1)=f(1))
# We want the sign and exact expression to build a rigorous proof that f_n notin D(K_c).

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

print('=== Odd n: f_n=K_c^{-1}P_n, deficit f\'(1)-f(1) ===')
for n in [3, 5, 7, 9, 11]:
    fn = K_inv_poly(sp.legendre(n, x))
    f1 = sp.expand(fn.subs(x, 1))
    fp1 = sp.expand(sp.diff(fn, x).subs(x, 1))
    defi = sp.expand(fp1 - f1)
    # numerator polynomial in c, factored
    num = sp.factor(sp.together(defi).as_numer_denom()[0])
    den = sp.together(defi).as_numer_denom()[1]
    print('n=%d deficit = %s' % (n, sp.factor(defi)))

print()
print('=== signs: evaluate deficit at c=1,3,10 ===')
for n in [3, 5, 7, 9]:
    fn = K_inv_poly(sp.legendre(n, x))
    defi = sp.expand(sp.diff(fn, x).subs(x, 1) - fn.subs(x, 1))
    print('n=%d: deficit(c=1)=%s, c=3)=%s, c=10)=%s' % (n,
        sp.nsimplify(defi.subs(c, 1)), sp.nsimplify(defi.subs(c, 3)), sp.nsimplify(defi.subs(c, 10))))
