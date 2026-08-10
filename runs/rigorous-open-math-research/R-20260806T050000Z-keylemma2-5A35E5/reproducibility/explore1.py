# -*- coding: utf-8 -*-
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

# ---- 1. Q1 profile ----
print('=== Q1 profile: dG2/dq at fixed c ===')
h = mp.mpf('1e-5')
for q in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('5'), mp.mpf('20'), mp.mpf('100'), mp.mpf('1000')]:
    for c in [mp.mpf('0.05'), mp.mpf('0.2'), mp.mpf('0.35'), mp.mpf('0.49')]:
        dq = (L.G2(c, q+h) - L.G2(c, q-h))/(2*h)
        print('  q=%s c=%s: dG2/dq=%s' % (mp.nstr(q,4), mp.nstr(c,4), mp.nstr(dq,7)))

# ---- 2. G2(c;2) monotone? ----
print('=== B6: G2(c;2) ===')
prev = None
for ci in range(1, 41):
    c = mp.mpf('0.5')*ci/40
    v = L.G2(c, mp.mpf('2'))
    if prev is not None and v > prev:
        print('  NOT monotone at c=%s: %s -> %s' % (mp.nstr(c,6), mp.nstr(prev,8), mp.nstr(v,8)))
    prev = v
c0499 = mp.mpf('0.499')
print('  G2(0.499,2) =', mp.nstr(L.G2(c0499, mp.mpf('2')), 12))
c05 = mp.mpf('0.5')
print('  G2(1/2,2)   =', mp.nstr(L.G2(c05, mp.mpf('2')), 12))

# ---- 3. G2(1/2;q) ----
print('=== G2 at c=1/2 ===')
for q in [mp.mpf('1.01'), mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('3'), mp.mpf('10'), mp.mpf('100')]:
    print('  q=%s: G2(1/2)=%s' % (mp.nstr(q,4), mp.nstr(L.G2(c05, q), 10)))

# ---- 4. Region B boundary ----
print('=== Region B: q*(G2=0) ===')
def q_star(c):
    lo, hi = mp.mpf('1.0001'), mp.mpf('3')
    f = lambda q: L.G2(c, q)
    if f(lo) < 0 and f(hi) > 0:
        return L.bisect(f, lo, hi)
    return None
for c in [mp.mpf('0.41'), mp.mpf('0.44'), mp.mpf('0.47'), mp.mpf('0.49'), mp.mpf('0.499')]:
    qs = q_star(c)
    print('  c=%s: q*(G2=0) = %s' % (mp.nstr(c,5), mp.nstr(qs,8) if qs else 'none'))

# ---- 5. L4box/L5box tight ----
print('=== L4box/L5box tight locations ===')
best = (mp.inf, None)
for qi in range(1, 41):
    q = mp.mpf(1) + mp.mpf(1)*qi/40
    for ci in range(0, 51):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/50
        v = L.Hp(c, q)
        if v < best[0]: best = (v, (q, c, 'Hp'))
print('  Hp min:', mp.nstr(best[0], 8), 'at', best[1])
best2 = (-mp.inf, None)
for qi in range(1, 41):
    q = mp.mpf(1) + mp.mpf(1)*qi/40
    for ci in range(0, 51):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/50
        v = L.Hp(c, q)
        if v > best2[0]: best2 = (v, (q, c, 'Hp'))
print('  Hp max:', mp.nstr(best2[0], 8), 'at', best2[1])
best3 = (mp.inf, None)
for qi in range(1, 41):
    q = mp.mpf(1) + mp.mpf(1)*qi/40
    for ci in range(0, 51):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/50
        v = L.Fpp_t(c, q)
        if v < best3[0]: best3 = (v, (q, c, 'Fpp'))
print('  Fpp min:', mp.nstr(best3[0], 8), 'at', best3[1])
