import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-keylemmaaudit-2F83B1\reproducibility")
import audit_iv as AI
import mpmath as mp
mp.mp.dps = 120

ok = True
for t, tv in [('0.2', mp.mpf('0.2')), ('a239', mp.mpf(1)/239), ('0.1', mp.mpf('0.1')),
              ('0.49', mp.mpf('0.49')), ('0.7', mp.mpf('0.7')), ('1', mp.mpf(1)),
              ('2', mp.mpf(2)), ('6.4', mp.mpf('6.4'))]:
    r = AI.iv_atan(AI.Iv.pt(tv))
    exact = mp.atan(tv)
    if not (mp.mpf(str(r.lo)) <= exact <= mp.mpf(str(r.hi))):
        ok = False
        print('ATAN FAIL', t, 'encl', mp.nstr(mp.mpf(str(r.lo)),35), mp.nstr(mp.mpf(str(r.hi)),35), 'exact', mp.nstr(exact, 40))
print('atan containment ok:', ok)
true_pi = mp.pi
print('PI =', AI.PI)
print('PI contains true pi:', mp.mpf(str(AI.PI.lo)) <= true_pi <= mp.mpf(str(AI.PI.hi)))
print('PI.lo - pi =', mp.nstr(mp.mpf(str(AI.PI.lo)) - true_pi, 5))
print('PI.hi - pi =', mp.nstr(mp.mpf(str(AI.PI.hi)) - true_pi, 5))
a5 = AI._atan_series(AI.Iv.pt(mp.mpf('0.2')), 120)
a239 = AI._atan_series(AI.Iv.pt(mp.mpf(1)/239), 120)
pi2 = AI.iv_sub(AI.iv_mul_d(a5, 16), AI.iv_mul_d(a239, 4))
print('direct machin contains pi:', mp.mpf(str(pi2.lo)) <= true_pi <= mp.mpf(str(pi2.hi)))
print('atan(0.2) true =', mp.nstr(mp.atan(mp.mpf('0.2')), 55))
print('a5 =', a5)
for n in [60, 90, 120, 200, 300]:
    a5n = AI._atan_series(AI.Iv.pt(mp.mpf('0.2')), n)
    print('n=%d contains: %s' % (n, mp.mpf(str(a5n.lo)) <= mp.atan(mp.mpf('0.2')) <= mp.mpf(str(a5n.hi))))
