# -*- coding: utf-8 -*-
"""Audit Part 4: dense sampling of the certified inequalities (plausibility of interval certificates)."""
import numpy as np
import mpmath as mp
mp.mp.dps = 40

def M2_expr(q, w):
    A = mp.pi - mp.atan(w/q); v = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + v*(4*A*w - 5*q - 9*q*w*w)

def dM2_dq(q, w):
    return mp.diff(lambda t: M2_expr(t, w), q, 1)

print("=== 4a: dM2/dq < 0 on [1,20]x[0,sqrt41] (dense) ===")
worst = mp.mpf('1e30')
qs = np.linspace(1.0, 20.0, 120)
ws = np.linspace(0.0, np.sqrt(41.0), 120)
cnt = 0
for qv in qs:
    for wv in ws:
        if wv > 0.0 and wv < np.sqrt(2*qv+1) + 1e-9:
            d = dM2_dq(mp.mpf(qv), mp.mpf(wv))
            worst = min(worst, d)
            cnt += 1
            if d >= 0:
                print("FAIL", qv, wv, d); raise SystemExit
print(f"min over {cnt} samples:", float(worst), "(certificate claims upper bound -0.1902...)")
assert worst < 0

print("=== 4b: K(v) > 0 on [2pi/7, 2pi/5) (dense), via IN = A*K ===")
def K_val(v):
    w = mp.tan(v)
    A = mp.mpf('2.5')*v
    q = w/mp.tan(mp.pi - mp.mpf('2.5')*v)
    IN = (q*q+w*w)*A*(2*A*q - 3*w + 2*v) - 3*w*q*(1+w*w)*v
    return IN/A
worst_k = mp.mpf('1e30')
vs = np.linspace(2*np.pi/7 + 1e-9, 2*np.pi/5 - 1e-6, 4000)
for vv in vs:
    K = K_val(mp.mpf(vv))
    worst_k = min(worst_k, K)
    if K <= 0:
        print("FAIL K", vv, K); raise SystemExit
# tail: v = (2/5)(pi - omega), omega in (0, 2.5e-3]
worst_t = mp.mpf('1e30')
for om in np.linspace(1e-9, 2.5e-3, 2000):
    v = mp.mpf('0.4')*(mp.pi - mp.mpf(om))
    K = K_val(v)
    worst_t = min(worst_t, K)
    if K <= 0:
        print("FAIL tail", om, K); raise SystemExit
print("min K on interval:", float(worst_k), " min K on tail:", float(worst_t), "(certificate claims 2.497...)")
assert worst_k > 0 and worst_t > 0

print("=== 4c: C4 claim G2(0.4;q) >= 0 for all q>1 (dense) ===")
def phi_q(q, x): return mp.cos(x)**2 + q*q*mp.sin(x)**2
def G_func(q, c, x):
    D = q + c*phi_q(q, x)
    return -phi_q(q, x)*(3 + 2*x*mp.cot(x))/D + 2*c*x*phi_q(q, x)*(q*q-1)*mp.sin(x)*mp.cos(x)/D**2
def alpha2_of_c(q, c):
    f = lambda x: mp.atan(-q*mp.tan(x)) - c*x
    lo, hi = mp.pi/2 + mp.mpf('1e-18'), mp.pi - mp.mpf('1e-18')
    for _ in range(100):
        mid = (lo+hi)/2
        if f(mid) > 0: lo = mid
        else: hi = mid
    return (lo+hi)/2
worst_g = mp.mpf('1e30')
for qv in np.linspace(1.0001, 100.0, 200):
    g2 = G_func(mp.mpf(qv), mp.mpf('0.4'), alpha2_of_c(mp.mpf(qv), mp.mpf('0.4')))
    worst_g = min(worst_g, g2)
    if g2 < 0:
        print("FAIL G2(0.4)", qv, g2); raise SystemExit
print("min G2(0.4;q):", float(worst_g))
assert worst_g > 0

print("=== 4d: CORNER G2(1/2;q) >= 0 for q>=2 (dense) ===")
worst_c = mp.mpf('1e30')
for qv in np.linspace(2.0, 100.0, 150):
    x = 2*mp.asin(1/mp.sqrt(2*(qv+1)))
    g2 = 2*qv*(qv+1)*(mp.pi - x - 3*mp.sin(x))/(2*qv+1)**mp.mpf('1.5')
    worst_c = min(worst_c, g2)
    if g2 < 0:
        print("FAIL CORNER", qv, g2); raise SystemExit
print("min CORNER G2(1/2;q):", float(worst_c))
assert worst_c > 0
print("ALL PART 4 CHECKS PASSED")
