# odd_proof_data.py
# Explore the Krein-Sobolev transport-deficit to find a provable positivity structure.
# K_n = sum_i a_{n-2i} S_{n-2i}, S_m = P_m - P_{m-2}; f_n := K_c^{-1}K_n.
# deficit L(K_n) = sum_i a_{n-2i} (D_{n-2i} - D_{n-2i-2}) where D_m := deficit of K_c^{-1}P_m.

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

def krein_sobolev_coeff(n):
    # returns dict {degree_index: a_coeff} with K_n = sum_i a_{n-2i} S_{n-2i}
    a = {0: 1, 1: 1, 2: 1, 3: 1}
    for m in range(2, n + 1):
        if (m + 2) not in a:
            a[m + 2] = sp.expand(a[m] * (1 + (4 * m * m - 1) / c)
                                 + sp.Rational(2 * m + 1, 2 * m - 3) * (a[m] - a[m - 2]))
    return a

def Dm(m):
    # deficit of K_c^{-1}P_m (Legendre)
    P = sp.legendre(m, x)
    f = K_inv_poly(P)
    if m % 2 == 0:
        return sp.expand(sp.diff(f, x).subs(x, 1))
    else:
        return sp.expand(sp.diff(f, x).subs(x, 1) - f.subs(x, 1))

print('=== D_m = Krein deficit of K_c^{-1}P_m (Legendre) for m=0..10 ===')
for m in range(0, 11):
    print('D_%d = %s' % (m, sp.factor(Dm(m))))

print()
print('=== Krein-Sobolev deficit via a-combination: sum_i a_{n-2i}(D_{n-2i}-D_{n-2i-2}) ===')
for n in range(2, 8):
    a = krein_sobolev_coeff(n)
    L = 0
    for i in range(0, n // 2 + 1):
        m = n - 2 * i
        L += a[m] * (Dm(m) - (Dm(m - 2) if m - 2 >= 0 else 0))
    print('L(K_%d) = %s' % (n, sp.factor(sp.expand(L))))

print()
print('=== the a coefficients a_m for m=0..8 (positive?) ===')
a = krein_sobolev_coeff(8)
for m in sorted(a):
    print('a_%d = %s' % (m, sp.factor(a[m])))
