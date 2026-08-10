# -*- coding: utf-8 -*-
"""explore5.py -- dG1/dx (even curve), dG2/dgamma (odd curve) on box angle ranges."""
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
    c = L.odd_beta(mp.pi - g, q)/(mp.pi - g)   # = atan(q tan g)/(pi-g)
    return L.Gfun(mp.pi - g, c, q)
def dGOdg(g, q):
    h = mp.mpf('1e-7')
    return (GO(g+h, q) - GO(g-h, q))/(2*h)

print('dG1/dx along even curve (x near box range):')
for q in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('2')]:
    a0 = L.alpha0_of_q(q)
    row = 'q=%s alpha0=%s: ' % (mp.nstr(q,4), mp.nstr(a0,5))
    for x in [a0, mp.mpf('0.9'), mp.mpf('1.0'), mp.mpf('1.1'), mp.mpf('1.2')]:
        if x < mp.pi/2 and x > a0:
            row += ' x=%s: %s' % (mp.nstr(x,4), mp.nstr(dGEdx(x,q),6))
    print(row)
print()
print('dG2/dgamma along odd curve (gamma in box range):')
for q in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('2')]:
    a0 = L.alpha0_of_q(q)
    row = 'q=%s alpha0=%s: ' % (mp.nstr(q,4), mp.nstr(a0,5))
    for g in [mp.mpf('0.65'), mp.mpf('0.7'), mp.mpf('0.8'), mp.mpf('0.9'), a0]:
        if g < a0:
            row += ' g=%s: %s' % (mp.nstr(g,4), mp.nstr(dGOdg(g,q),6))
    print(row)
print()
# verify dG2dc = dGOdg * dgamma/dc identity
print('verify dG2dc = dGOdg*(dgamma/dc):')
for q in [mp.mpf('1.5'), mp.mpf('2')]:
    for c in [mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.49')]:
        g = L.gamma_of(q, c)
        dgdc = (mp.pi - g)*L.Phi(g, q)/(q + c*L.Phi(g, q))
        lhs = (L.G2(c+mp.mpf('1e-7'), q) - L.G2(c-mp.mpf('1e-7'), q))/(mp.mpf('2e-7'))
        rhs = dGOdg(g, q)*dgdc
        print('  q=%s c=%s: lhs=%s rhs=%s rel=%s' % (mp.nstr(q,4), mp.nstr(c,4), mp.nstr(lhs,7), mp.nstr(rhs,7), mp.nstr(abs(lhs-rhs)/abs(lhs),3)))
