# -*- coding: utf-8 -*-
"""explore3.py -- J1, J2 signs over the domain; check Hp>0 claim at (30, 0.33)."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

print('=== prior claim: Hp(30, 0.33) and components ===')
for (q, c) in [(mp.mpf('30'), mp.mpf('0.33')), (mp.mpf('1.01'), mp.mpf('0.001'))]:
    a1 = L.alpha1(c,q); a2 = L.alpha2(c,q)
    J1 = L.Jfun(a1,c,q); J2 = L.Jfun(a2,c,q)
    Hp = L.Hp(c,q)
    Fpp = L.Fpp_t(c,q)
    print('  q=%s c=%s: J1=%s J2=%s Hp=%s Fpp=%s' % (mp.nstr(q,4), mp.nstr(c,4), mp.nstr(J1,7), mp.nstr(J2,7), mp.nstr(Hp,7), mp.nstr(Fpp,7)))

print()
print('=== scan signs of J1, J2, Hp, Fpp over (1,1000] x (0.001,0.49] ===')
counts = {'J1neg':0, 'J2pos':0, 'Hppos':0, 'Fppneg':0}
examples = {}
for qi in [1,2,3,5,8,12,17,25,40,60,100,200,400,1000]:
    q = mp.mpf(1) + mp.mpf(qi)/20
    for ci in range(1, 50):
        c = mp.mpf('0.001') + mp.mpf('0.489')*ci/49
        a1 = L.alpha1(c,q); a2 = L.alpha2(c,q)
        J1 = L.Jfun(a1,c,q); J2 = L.Jfun(a2,c,q)
        Hp = J2 - J1
        Fpp = L.Mtilde(a1,c,q)*J1 - L.Mtilde(a2,c,q)*J2
        if J1 < 0:
            counts['J1neg'] += 1
            examples.setdefault('J1neg', (q,c,J1))
        if J2 > 0:
            counts['J2pos'] += 1
            examples.setdefault('J2pos', (q,c,J2))
        if Hp > 0:
            counts['Hppos'] += 1
            examples.setdefault('Hppos', (q,c,Hp))
        if Fpp < 0:
            counts['Fppneg'] += 1
            examples.setdefault('Fppneg', (q,c,Fpp))
print('  counts:', counts)
for k, v in examples.items():
    print('  example %s: q=%s c=%s val=%s' % (k, mp.nstr(v[0],5), mp.nstr(v[1],5), mp.nstr(v[2],6)))
