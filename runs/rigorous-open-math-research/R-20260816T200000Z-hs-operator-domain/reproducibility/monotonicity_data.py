# monotonicity_data.py
# Study the monotonicity of D_m (Krein deficit of K_c^{-1}P_m) to support a
# rigorous odd-case (Krein-Sobolev) proof.
# D_m := f_m'(1) - [f_m(1)-f_m(-1)]/2  (full Krein deficit), f_m = K_c^{-1}P_m.
# For parity m: even -> D_m = f_m'(1); odd -> D_m = f_m'(1) - f_m(1).

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

def Dm(m):
    P = sp.legendre(m, x)
    f = K_inv_poly(P)
    d1 = sp.expand(sp.diff(f, x).subs(x, 1))
    dm1 = sp.expand(sp.diff(f, x).subs(x, -1))
    avg = sp.expand((f.subs(x, 1) - f.subs(x, -1)) / 2)
    return sp.expand(d1 - avg)

print('=== D_m and differences delta_m = D_m - D_{m-1} ===')
prev = None
for m in range(0, 13):
    D = Dm(m)
    if prev is not None:
        delta = sp.expand(D - prev)
        print('m=%2d  D_m=%-40s  delta=%-50s' % (m, sp.factor(D), sp.factor(delta)))
    else:
        print('m=%2d  D_m=%s' % (m, sp.factor(D)))
    prev = D
