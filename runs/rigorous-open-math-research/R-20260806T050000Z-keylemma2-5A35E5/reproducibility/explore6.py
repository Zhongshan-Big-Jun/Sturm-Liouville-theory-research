# -*- coding: utf-8 -*-
"""explore6.py -- extend dG1/dx, dG2/dgamma negativity to full c-range for q in (1,2]."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

def GE(x, q):
    c = L.even_beta(x, q)/x
    return L.Gfun(x, c, q)
def dGEdx(x, q):
    h = mp.mpf('1e-7')
    return (GE(x+h, q) - GE(x-h, q))/(2*h)
def GO(g, q):
    c = L.odd_beta(mp.pi - g, q)/(mp.pi - g)
    return L.Gfun(mp.pi - g, c, q)
def dGOdg(g, q):
    h = mp.mpf('1e-7')
    return (GO(g+h, q) - GO(g-h, q))/(2*h)

print('=== dG2/dgamma over gamma in (0, alpha0(q)), q in (1,2] ===')
mn = mp.inf; at = None
for qi in range(1, 21):
    q = mp.mpf(1) + mp.mpf(1)*qi/20
    a0 = L.alpha0_of_q(q)
    for gi in range(1, 40):
        g = mp.mpf('0.001') + (a0 - mp.mpf('0.001'))*gi/40
        v = dGOdg(g, q)
        if v > 0:
            print('  POSITIVE at q=%s g=%s val=%s' % (mp.nstr(q,5), mp.nstr(g,5), mp.nstr(v,7)))
        if v < mn: mn, at = v, (q, g)
print('  min =', mp.nstr(mn,6), 'at', mp.nstr(at[0],5), mp.nstr(at[1],5))

print('=== dG1/dx over x in (alpha0(q), pi/2), q in (1,2] ===')
mn = mp.inf; mx = -mp.inf; at1 = at2 = None
for qi in range(1, 21):
    q = mp.mpf(1) + mp.mpf(1)*qi/20
    a0 = L.alpha0_of_q(q)
    for xi in range(1, 40):
        x = a0 + (mp.pi/2 - a0)*xi/40 - mp.mpf('1e-7')
        if x <= a0: continue
        v = dGEdx(x, q)
        if v > mx: mx, at2 = v, (q, x)
        if v < mn: mn, at1 = v, (q, x)
print('  min =', mp.nstr(mn,6), 'at', mp.nstr(at1[0],5), mp.nstr(at1[1],5))
print('  max =', mp.nstr(mx,6), 'at', mp.nstr(at2[0],5), mp.nstr(at2[1],5))

print()
print('=== how far in q does dG2/dgamma < 0 persist (full gamma range)? ===')
for q in [mp.mpf('2.5'), mp.mpf('3'), mp.mpf('5'), mp.mpf('10')]:
    a0 = L.alpha0_of_q(q)
    pos = False
    for gi in range(1, 60):
        g = mp.mpf('0.001') + (a0 - mp.mpf('0.001'))*gi/60
        if dGOdg(g, q) > 0:
            pos = True
            print('  q=%s: dG2/dgamma>0 at g=%s' % (mp.nstr(q,4), mp.nstr(g,5)))
            break
    if not pos:
        print('  q=%s: dG2/dgamma < 0 on full gamma range' % mp.nstr(q,4))
