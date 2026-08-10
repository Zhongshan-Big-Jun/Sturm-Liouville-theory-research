# -*- coding: utf-8 -*-
"""Audit of O3a_complete_proof_zh.pdf (2026-08-09), Part 1: analytic identities and inequalities.
Verifies: (7), r_tau monotonicity, G1<0, IN=G2*POS, c(w)=1/2 boundary, M2<0, M2(1,w)=pi*h(w),
CORNER formula, Fe'(q,1/2) formula, Fe endpoint limits, KEY LEMMA Fe'<0, Fe''>0 on Q, B(q) and large-w bounds."""
import mpmath as mp
mp.mp.dps = 90

def phi_q(q, x):
    return mp.cos(x)**2 + q*q*mp.sin(x)**2

def Mf(q, c, x):
    return x*x*mp.sin(x)**2/(q + c*phi_q(q, x))

def G_func(q, c, x):
    D = q + c*phi_q(q, x)
    return -phi_q(q, x)*(3 + 2*x*mp.cot(x))/D + 2*c*x*phi_q(q, x)*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2

def _bracket_bisect(f, lo, hi, tol=mp.mpf('1e-80')):
    for _ in range(120):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return mp.findroot(f, (lo+hi)/2, tol=tol)

def alpha1_of_c(q, c):
    return _bracket_bisect(lambda x: mp.atan(1/(q*mp.tan(x))) - c*x,
                           mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20'))

def alpha2_of_c(q, c):
    if c < 1:
        return _bracket_bisect(lambda x: mp.atan(-q*mp.tan(x)) - c*x,
                               mp.pi/2 + mp.mpf('1e-20'), mp.pi - mp.mpf('1e-20'))
    else:
        return _bracket_bisect(lambda x: mp.pi - mp.atan(q*mp.tan(x)) - c*x,
                               mp.mpf('1e-20'), mp.pi/2 - mp.mpf('1e-20'))

def Fe(q, c):
    return Mf(q, c, alpha1_of_c(q, c)) - Mf(q, c, alpha2_of_c(q, c))

def dFe(q, c):
    return mp.diff(lambda t: Fe(q, t), c, 1)

def IN_expr(q, w):
    A = mp.pi - mp.atan(w/q); v = mp.atan(w)
    return (q*q+w*w)*A*(2*A*q - 3*w + 2*v) - 3*w*q*(1+w*w)*v

def M2_expr(q, w):
    A = mp.pi - mp.atan(w/q); v = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + v*(4*A*w - 5*q - 9*q*w*w)

print("=== 1c: G1 < 0; IN = G2*POS sign identity ===")
worst_g2 = 0
for q in [1.01, 1.2, 1.5, 1.9, 2.0, 3.0, 10.0, 100.0]:
    for c in [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.49]:
        a1 = alpha1_of_c(q, c); a2 = alpha2_of_c(q, c)
        g1 = G_func(q, c, a1); g2 = G_func(q, c, a2)
        assert g1 < 0
        gamma = mp.pi - a2
        w = q*mp.tan(gamma)
        IN = IN_expr(q, w)
        POS = (q + c*phi_q(q, a2))**2 * a2 * (q*q + w*w) * w / (phi_q(q, a2) * q)
        rel = abs(IN - g2*POS)/max(mp.mpf('1'), abs(g2*POS))
        worst_g2 = max(worst_g2, rel)
        assert mp.sign(IN) == mp.sign(g2)
print("G1<0 OK; worst |IN - G2*POS|/scale:", worst_g2)

print("=== 1d: c(w=sqrt(2q+1)) = 1/2 ===")
for q in [1.0001, 1.01, 1.5, 2.0, 5.0, 20.0, 100.0, 1e6]:
    w05 = mp.sqrt(2*q+1)
    c_at = mp.atan(w05)/(mp.pi - mp.atan(w05/q))
    assert abs(c_at - mp.mpf('0.5')) < mp.mpf('1e-45')
print("c(w=sqrt(2q+1)) = 1/2 OK")

print("=== 1e: M2 < 0 on D sampled; analytic == numeric dIN/dw ===")
worst = 0
for q in [1.0001, 1.01, 1.3, 2.0, 5.0, 20.0, 100.0, 500.0, 1e4]:
    wmax = mp.sqrt(2*q+1)
    for frac in [0.05, 0.5, 0.9, 0.99]:
        w = frac*wmax
        num = mp.diff(lambda t: IN_expr(q, t), w, 1)
        worst = max(worst, abs(M2_expr(q,w) - num))
        assert M2_expr(q,w) < 0, (q, w, M2_expr(q,w))
print("M2<0 sampled OK; worst |analytic-numeric|:", worst)

print("=== 1f: q=1 baseline M2(1,w) = pi*h(w) < 0 ===")
for wv in [0.05, 0.5, 1.0, 2.0, 3.0, 5.0]:
    w = mp.mpf(wv)
    h = 4*w*(mp.pi - mp.atan(w)) - 5 - 9*w*w
    M2_1 = M2_expr(mp.mpf('1'), w)
    assert abs(h - M2_1/mp.pi) < mp.mpf('1e-45')
    assert h < 0
print("M2(1,w)=pi*h(w)<0 OK")

print("=== 1g: CORNER G2(1/2;q) formula ===")
for q in [2.0, 3.0, 5.0, 10.0, 100.0, 1e6]:
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    g2 = G_func(q, mp.mpf('0.5'), alpha2_of_c(q, mp.mpf('0.5')))
    formula = 2*q*(q+1)*(mp.pi - x - 3*mp.sin(x))/(2*q+1)**mp.mpf('1.5')
    assert abs(g2-formula) < mp.mpf('1e-40'), (q, g2, formula)
    assert g2 > 0
print("CORNER formula OK")

print("=== 1h: Fe'(q,1/2) formula ===")
for q in [1.0, 1.5, 2.0, 10.0, 100.0]:
    x = 2*mp.asin(1/mp.sqrt(2*(q+1)))
    Fp_num = dFe(q, mp.mpf('0.5'))
    P = 3*x*x + 6*x*mp.sin(x) - 3*mp.pi*x - 3*mp.pi*mp.sin(x) + mp.pi*mp.pi
    formula = 2*mp.pi*(mp.cos(x)-1)**3/mp.sin(x)**3 * P
    assert abs(Fp_num-formula) < mp.mpf('1e-30')
    assert Fp_num < 0
print("Fe'(q,1/2) formula OK, < 0")

print("=== 1i: Fe(c)->pi^2/(4q) as c->0; Fe<0 for c>=1/2 ===")
for q in [1.2, 2.0, 5.0, 100.0]:
    c_small = mp.mpf('1e-14')
    assert abs(Fe(q, c_small) - mp.pi**2/(4*q)) < mp.mpf('1e-6')
    for c in [0.5, 0.6, 1.0, 2.0, 5.0, 100.0]:
        assert Fe(q, mp.mpf(c)) < 0, (q, c)
print("endpoint behavior OK")

print("=== 1j: KEY LEMMA Fe'(c)<0 on 0<c<1/2 ===")
for q in [1.0001, 1.01, 1.1, 1.3, 1.5, 1.7, 1.9, 2.0, 2.5, 3.0, 5.0, 10.0, 100.0, 1e6]:
    for c in [1e-6, 0.001, 0.05, 0.1, 0.2, 0.3, 0.4, 0.45, 0.49, 0.499, 0.4999]:
        assert dFe(q, mp.mpf(c)) < 0, (q, c, dFe(q, mp.mpf(c)))
print("Fe'<0 sampled OK")

print("=== 1k: Fe''>0 on Q=[1,2]x[0.4,0.5] ===")
minval = mp.mpf('1e30')
for q in [1.0, 1.1, 1.3, 1.5, 1.7, 1.9, 2.0]:
    for c in [0.4, 0.42, 0.45, 0.48, 0.5]:
        Fpp = mp.diff(lambda t: Fe(q, t), c, 2)
        minval = min(minval, Fpp)
        assert Fpp > 0
print("Fe''>0 on Q OK; min sampled:", float(minval))

print("=== 1l: B(q) tail bound for M2: B(q)<0 and M2<=B(q) for q>=20 ===")
pi = mp.pi
for q in [20, 21, 30, 50, 100, 1000, 1e6]:
    q = mp.mpf(q)
    B = (4*pi**2+14)*mp.sqrt(2*q+1) + 8*pi*mp.sqrt(2*q+1)/q + 1 + 2*pi*(2*q+1)/q**2 - 10*pi*q
    wmax = mp.sqrt(2*q+1)
    wgrid = [0.05*wmax, 0.3*wmax, 0.7*wmax, 0.95*wmax, 0.99*wmax]
    m2max = max(M2_expr(q, w) for w in wgrid)
    assert B < 0 and m2max < B, (q, B, m2max)
print("B(q) bound OK (sampled)")

print("=== 1m: large-w estimate: M2/q^2 <= 4pi^2*0.33 - 7(pi-0.33) + 2pi(1+0.33^2)/42 ===")
bound = 4*pi**2*mp.mpf('0.33') - 7*(pi - mp.mpf('0.33')) + 2*pi*(1+mp.mpf('0.33')**2)/42
assert bound < 0
for q in [20.1, 21, 25, 30, 50, 100, 1000]:
    wmax = mp.sqrt(2*q+1)
    for w in [mp.sqrt(41)+0.01, 0.8*wmax, wmax-1e-6]:
        if w <= mp.sqrt(41) or w >= wmax: continue
        assert M2_expr(q, w)/q**2 < bound, (q, w, M2_expr(q,w)/q**2)
print("large-w estimate OK (sampled); bound =", float(bound))

print("ALL PART 1 CHECKS PASSED")
