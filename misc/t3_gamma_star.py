# -*- coding: utf-8 -*-
"""t3_gamma_star: locate gamma(2, 0.4) precisely."""
from mpmath import mp, mpf, tan, atan, pi as mppi
mp.dps = 40

def h(g): return mpf('0.4')*(mppi-g) - atan(2*tan(g))
print('h(0.655) =', h(mpf('0.655')))
print('h(2pi/7) =', h(mp.mpf(2)*mppi/7))
# bisection
lo, hi = mpf('0.65'), mppi/3
assert h(lo)*h(hi) < 0
for _ in range(100):
    mid = (lo+hi)/2
    if h(mid)*h(lo) < 0: hi = mid
    else: lo = mid
gstar = (lo+hi)/2
print('gamma(2, 0.4) =', gstar, '= %.6f' % gstar, ' 2pi/7 = %.6f' % (2*mppi/7))
print('gamma(1, 1/2) =', mppi/3)
# c_2 at (gamma, q) for q=1: c = gamma/(pi-gamma); check c(2pi/7)=2/5
print('c2(2pi/7, 1) =', (2*mppi/7)/(mppi - 2*mppi/7))
# The true region T2 in (gamma,q): gamma in [gstar, pi/3], q in [1,2], c in [0.4,0.5]
# check c_2(gamma, 2) at gamma=gstar: = 0.4
print('c2(gstar, 2) =', atan(2*tan(gstar))/(mppi-gstar))
# check the corner (2pi/7, 1): gamma in range? 2pi/7 = 0.8976 > gstar ~?
print('gstar vs 2pi/7: gstar = %.6f, 2pi/7 = %.6f' % (gstar, 2*mppi/7))
