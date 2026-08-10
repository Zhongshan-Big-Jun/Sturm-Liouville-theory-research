# -*- coding: utf-8 -*-
"""q1_analysis.py -- verify q=1 closed forms and the symbolic reductions.
F~'(1,c) = [P(2u) - P(u)]/(1+c)^2, P(t) = 3 t^2 sin^2 t + 2 t^3 sin t cos t.
P(u)-P(2u) = u^2 sin^2 u * [3 - 45x^2 + 34ux - 30ux^3]/(1+x^2), x = cot u.
Log form at q=1: H(1,c) = (W(u)-W(2u))/(1+c) = (2u/pi)(W(u)-W(2u)); need min = 4 pi/(3 sqrt3).
"""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-keylemma-E58FB1\reproducibility')
from keylemma_lib import Wfun
mp.mp.dps = 40

def P(t):
    return 3*t*t*mp.sin(t)**2 + 2*t**3*mp.sin(t)*mp.cos(t)

print('=== q=1 F~\' form: P(u) - P(2u) > 0 on u in (pi/3, pi/2) ===')
mn = mp.inf; mnx = None
for k in range(501):
    u = mp.pi/3 + (mp.pi/2 - mp.pi/3)*k/500
    d = P(u) - P(2*u)
    if d < mn: mn, mnx = d, u
print(f'  min(P(u)-P(2u)) = {mp.nstr(mn,10)} at u={mp.nstr(mnx,8)}')
# verify the x-reduction formula
for k in [0, 100, 300, 500]:
    u = mp.pi/3 + (mp.pi/2 - mp.pi/3)*k/500
    x = mp.cot(u)
    lhs = P(u) - P(2*u)
    rhs = u*u*mp.sin(u)**2*(3 - 45*x*x + 34*u*x - 30*u*x**3)/(1+x*x)
    print(f'  u={mp.nstr(u,6)}: lhs={mp.nstr(lhs,8)} rhs={mp.nstr(rhs,8)} diff={mp.nstr(lhs-rhs,8)}')

print()
print('=== bound check: 3 - 45x^2 + 8*pi*x > 0 for x in (0, 1/sqrt3) ===')
mn2 = mp.inf
for k in range(501):
    x = mp.mpf(1)/mp.sqrt(3)*k/500
    v = 3 - 45*x*x + 8*mp.pi*x
    if v < mn2: mn2 = v
print(f'  min over x in [0,1/sqrt3] = {mp.nstr(mn2,8)} (expected ~6.51)')

print()
print('=== q=1 log form: H(1,c) = (W(u)-W(2u))/(1+c); check monotonicity in c ===')
def H1(c):
    u = mp.pi/(2*(1+c))
    return (Wfun(u) - Wfun(2*u))/(1+c)
vals = [(c, H1(c)) for c in [mp.mpf('1e-6'), mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.4999')]]
for c, h in vals:
    print(f'  c={mp.nstr(c,6)}: H(1,c)={mp.nstr(h,9)}')
# derivative in c: numerical
h = mp.mpf('1e-5')
mn3 = mp.inf
for k in range(1, 500):
    c = mp.mpf('1e-5') + (mp.mpf('0.5')-mp.mpf('2e-5'))*k/500
    d = (H1(c+h) - H1(c-h))/(2*h)
    if d < mn3: mn3 = d
print(f'  min dH/dc over (0,1/2) = {mp.nstr(mn3,8)} (should be < 0 if H decreasing in c)')
print(f'  4*pi/(3*sqrt3) = {mp.nstr(4*mp.pi/(3*mp.sqrt(3)), 12)}')
