# -*- coding: utf-8 -*-
"""verify_kl2.py -- independent cross-checks (optimized, cached)."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 40

ok = True
def check(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {detail}")

# --- E1 log-derivative identity
print('--- E1 ---')
for q in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
    for c in [mp.mpf('0.05'), mp.mpf('0.4')]:
        h = mp.mpf('1e-6')
        ld = (mp.log(L.M1t(c+h,q)/L.M2t(c+h,q)) - mp.log(L.M1t(c-h,q)/L.M2t(c-h,q)))/(2*h)
        check(f'E1 q={q} c={c}', abs(ld - (L.G1(c,q)-L.G2(c,q))) < mp.mpf('1e-9'), f'|d|={float(abs(ld-(L.G1(c,q)-L.G2(c,q)))):.1e}')

# --- E2 Fp identity
print('--- E2 ---')
for q in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
    for c in [mp.mpf('0.05'), mp.mpf('0.4')]:
        h = mp.mpf('1e-6')
        dn = ( (L.M1t(c+h,q)-L.M2t(c+h,q)) - (L.M1t(c-h,q)-L.M2t(c-h,q)) )/(2*h)
        fp = L.Fp_t(c,q)
        check(f'E2 q={q} c={c}', abs(fp-dn) < mp.mpf('1e-9'), f'|d|={float(abs(fp-dn)):.1e}')

# --- dGdc vs FD
print('--- dGdc ---')
for q in [mp.mpf('1.1'), mp.mpf('2'), mp.mpf('10')]:
    for c in [mp.mpf('0.1'), mp.mpf('0.45')]:
        h = mp.mpf('1e-6')
        for k, ak in ((1, L.alpha1), (2, L.alpha2)):
            num = (L.Gfun(ak(c+h,q), c+h, q) - L.Gfun(ak(c-h,q), c-h, q))/(2*h)
            d = L.dGdc(ak(c,q), c, q)
            check(f'dGdc q={q} c={c} k={k}', abs(num-d) < mp.mpf('1e-8'), f'|d|={float(abs(num-d)):.1e}')

# --- E8 Fpp
print('--- E8 ---')
for q in [mp.mpf('1.3'), mp.mpf('1.9'), mp.mpf('2.0')]:
    for c in [mp.mpf('0.41'), mp.mpf('0.49')]:
        h = mp.mpf('1e-5')
        num = (L.Fp_t(c+h,q) - L.Fp_t(c-h,q))/(2*h)
        val = L.Fpp_t(c,q)
        check(f'E8 q={q} c={c}', abs(num-val) < mp.mpf('1e-6'), f'|d|={float(abs(num-val)):.1e}')

# --- Hp == J2 - J1
print('--- Hp == J2-J1 ---')
for q in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('2')]:
    for c in [mp.mpf('0.42'), mp.mpf('0.49')]:
        J1 = L.Jfun(L.alpha1(c,q), c, q); J2 = L.Jfun(L.alpha2(c,q), c, q)
        check(f'Hp q={q} c={c}', abs(L.Hp(c,q) - (J2-J1)) < mp.mpf('1e-30'), f'|d|={float(abs(L.Hp(c,q)-(J2-J1))):.1e}')

# --- margins (cached roots to speed up)
from functools import lru_cache
class C:
    def __init__(self):
        self.a1 = {}; self.a2 = {}
    def a1c(self, c, q):
        key = (float(c), float(q))
        if key not in self.a1: self.a1[key] = L.alpha1(c, q)
        return self.a1[key]
    def a2c(self, c, q):
        key = (float(c), float(q))
        if key not in self.a2: self.a2[key] = L.alpha2(c, q)
        return self.a2[key]
cache = C()

def G2c(c, q):
    a = cache.a2c(c, q)
    return L.Gfun(a, c, q)
def Hpc(c, q):
    a1 = cache.a1c(c, q); a2 = cache.a2c(c, q)
    return L.dGdc(a2, c, q) - L.dGdc(a1, c, q)
def Fppc(c, q):
    a1 = cache.a1c(c, q); a2 = cache.a2c(c, q)
    return L.Mtilde(a1,c,q)*L.Jfun(a1,c,q) - L.Mtilde(a2,c,q)*L.Jfun(a2,c,q)

print('--- R1 ---')
m = mp.inf; at = None
for qi in range(0, 21):
    q = mp.mpf(2) + mp.mpf(18)*qi/20
    for ci in range(1, 101):
        c = mp.mpf('0.001') + mp.mpf('0.499')*ci/100
        v = G2c(c, q)
        if v < m: m, at = v, (q, c)
print(f'  min G2 = {mp.nstr(m, 8)} at q={mp.nstr(at[0],5)}, c={mp.nstr(at[1],5)}')

print('--- R2 ---')
m = mp.inf; at = None
for qi in range(1, 21):
    q = mp.mpf(1) + mp.mpf(0.5)*qi/20
    for ci in range(1, 101):
        c = mp.mpf('0.001') + mp.mpf('0.399')*ci/100
        v = G2c(c, q)
        if v < m: m, at = v, (q, c)
print(f'  min G2 = {mp.nstr(m, 8)} at q={mp.nstr(at[0],5)}, c={mp.nstr(at[1],5)}')

print('--- L4box ---')
m = -mp.inf; at = None
for qi in range(1, 11):
    q = mp.mpf(1) + mp.mpf(1)*qi/10
    for ci in range(0, 101):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/100
        v = Hpc(c, q)
        if v > m: m, at = v, (q, c)
print(f'  max Hp = {mp.nstr(m, 8)} at q={mp.nstr(at[0],5)}, c={mp.nstr(at[1],5)}')

print('--- L5box ---')
m = mp.inf; at = None
for qi in range(1, 11):
    q = mp.mpf(1) + mp.mpf(1)*qi/10
    for ci in range(0, 101):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/100
        v = Fppc(c, q)
        if v < m: m, at = v, (q, c)
print(f'  min Fpp = {mp.nstr(m, 8)} at q={mp.nstr(at[0],5)}, c={mp.nstr(at[1],5)}')

print('--- Q1 (central FD, coarse) ---')
m = mp.inf; at = None
for qi in range(1, 31):
    q = mp.mpf(1) + mp.mpf(49)*qi/30
    for ci in range(1, 21):
        c = mp.mpf('0.005') + mp.mpf('0.49')*ci/20
        h = mp.mpf('1e-4')
        v = (G2c(c, q+h) - G2c(c, q-h))/(2*h)
        if v < m: m, at = v, (q, c)
print(f'  min dG2/dq = {mp.nstr(m, 6)} at q={mp.nstr(at[0],5)}, c={mp.nstr(at[1],5)}')

print()
print('ALL OK' if ok else 'SOME FAILED')
