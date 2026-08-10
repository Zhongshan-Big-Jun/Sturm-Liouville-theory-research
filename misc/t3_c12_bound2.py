# -*- coding: utf-8 -*-
"""t3_c12_bound2.py"""
from mpmath import mp, mpf, cos, sin, sqrt, acos, pi as mppi
mp.dps = 40
def P(b): return 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
def Q(b): return 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
def RHS(b): return -mpf('21')/10 * (1-b**2)**2 * (1+b)**3
worst = (mpf(1e30), None); loGx = mpf(1e30)
bad = 0
for i in range(4001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    x = mppi - acos(b)
    s = sqrt(1-b*b)
    LHS = x*P(b) + s*Q(b)
    crude = (2*mppi/3)*P(b) + (sqrt(mpf(5))/3)*Q(b)
    gap = crude - RHS(b)
    if gap > worst[0]: worst = (gap, float(b))
    if LHS > crude: bad += 1
    Gx = -2*(x*P(b)+s*Q(b))/(s**4*(1+b)**3)
    loGx = min(loGx, Gx)
print('LHS<=crude violations:', bad)
print('max of crude - RHS: %.6f at b=%.4f' % (worst[0], worst[1]))
print('min Gx on c=1/2 (b in [1/2,2/3]): %.6f' % loGx)
# also crude - RHS as explicit function of b for polynomial analysis
# F(b) = (2pi/3)P + (sqrt5/3)Q - RHS = (2pi/3)P + (sqrt5/3)Q + (21/10)(1-b^2)^2(1+b)^3
# print its values at endpoints and check monotonic structure
for b in [mpf('0.5'), mpf('0.55'), mpf('0.6'), mpf('0.65'), mpf('2')/3]:
    F = (2*mppi/3)*P(b) + (sqrt(mpf(5))/3)*Q(b) + mpf('21')/10*(1-b*b)**2*(1+b)**3
    print('b=%.4f: F=%.6f' % (b, F))
