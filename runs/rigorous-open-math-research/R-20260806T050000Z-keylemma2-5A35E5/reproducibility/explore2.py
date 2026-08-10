# -*- coding: utf-8 -*-
"""explore2.py -- structure of dG2/dc (for R2), and box components (for L4box/L5box)."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

def dG2dc(c, q):
    h = mp.mpf('1e-6')
    return (L.G2(c+h, q) - L.G2(c-h, q))/(2*h)

print('=== sign of dG2/dc over (1,3] x (0.001,0.49] ===')
mn = mp.inf; mx = -mp.inf; at1 = at2 = None
for qi in range(1, 31):
    q = mp.mpf(1) + mp.mpf(2)*qi/30
    for ci in range(1, 51):
        c = mp.mpf('0.001') + mp.mpf('0.489')*ci/50
        v = dG2dc(c, q)
        if v < mn: mn, at1 = v, (q, c)
        if v > mx: mx, at2 = v, (q, c)
print('  min dG2/dc =', mp.nstr(mn,6), 'at', mp.nstr(at1[0],5), mp.nstr(at1[1],5))
print('  max dG2/dc =', mp.nstr(mx,6), 'at', mp.nstr(at2[0],5), mp.nstr(at2[1],5))

print()
print('=== dG2/dc on c <= 0.4 (R2 region), q in (1,2] ===')
mn = mp.inf; mx = -mp.inf; at1 = at2 = None
for qi in range(1, 21):
    q = mp.mpf(1) + mp.mpf(1)*qi/20
    for ci in range(1, 41):
        c = mp.mpf('0.001') + mp.mpf('0.399')*ci/40
        v = dG2dc(c, q)
        if v < mn: mn, at1 = v, (q, c)
        if v > mx: mx, at2 = v, (q, c)
print('  min dG2/dc =', mp.nstr(mn,6), 'at', mp.nstr(at1[0],5), mp.nstr(at1[1],5))
print('  max dG2/dc =', mp.nstr(mx,6), 'at', mp.nstr(at2[0],5), mp.nstr(at2[1],5))

print()
print('=== box components: dG1/dc, dG2/dc, M1t, M2t, J1, J2 on (1,2]x[0.4,0.5] ===')
mn = mp.inf; mx = -mp.inf; at1 = at2 = None
best = {'dG1dc_min': (mp.inf,None), 'dG1dc_max': (-mp.inf,None), 'dG2dc_max': (-mp.inf,None),
        'J1_min': (mp.inf,None), 'J1_max': (-mp.inf,None), 'J2_min': (mp.inf,None), 'J2_max': (-mp.inf,None),
        'M1t_min': (mp.inf,None), 'M2t_min': (mp.inf,None), 'M2t_max': (-mp.inf,None)}
for qi in range(1, 21):
    q = mp.mpf(1) + mp.mpf(1)*qi/20
    for ci in range(0, 21):
        c = mp.mpf('0.4') + mp.mpf('0.1')*ci/20
        a1 = L.alpha1(c,q); a2 = L.alpha2(c,q)
        d1 = L.dGdc(a1,c,q); d2 = L.dGdc(a2,c,q)
        J1 = L.Jfun(a1,c,q); J2 = L.Jfun(a2,c,q)
        M1 = L.Mtilde(a1,c,q); M2 = L.Mtilde(a2,c,q)
        for k, v in [('dG1dc_min',d1), ('dG1dc_max',d1), ('dG2dc_max',d2), ('J1_min',J1), ('J1_max',J1), ('J2_min',J2), ('J2_max',J2), ('M1t_min',M1), ('M2t_min',M2), ('M2t_max',M2)]:
            if 'min' in k and v < best[k][0]: best[k] = (v, (q,c))
            if 'max' in k and v > best[k][0]: best[k] = (v, (q,c))
for k in ['dG1dc_min','dG1dc_max','dG2dc_max','J1_min','J1_max','J2_min','J2_max','M1t_min','M2t_min','M2t_max']:
    print('  %s = %s at %s' % (k, mp.nstr(best[k][0],8), best[k][1]))
