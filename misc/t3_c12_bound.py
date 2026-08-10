# -*- coding: utf-8 -*-
"""t3_c12_bound.py: verify xP+sQ <= (2pi/3)P + (sqrt5/3)Q <= RHS on b in [1/2, 2/3]."""
import math
from mpmath import mp, mpf, cos, sin, sqrt, pi as mppi
mp.dps = 40
def P(b): return 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
def Q(b): return 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
def RHS(b): return -mpf('21')/10 * (1-b**2)**2 * (1+b)**3

# check P, Q negative on [1/2,2/3]
loP, loQ = mpf(1e30), mpf(1e30)
for i in range(1001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    loP = min(loP, P(b)); loQ = min(loQ, Q(b))
print('P range on [1/2,2/3]: max = %.6f (should be <0)' % max(P(mpf('0.5')), P(mpf('2')/3)))
print('Q range on [1/2,2/3]: max = %.6f (should be <0)' % max(Q(mpf('0.5')), Q(mpf('2')/3)))

# verify the chain
worst = (mpf(1e30), None)
for i in range(2001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    x = mppi - acos(b)  # arccos(-b) = pi - arccos(b)
    s = sqrt(1-b*b)
    LHS = x*P(b) + s*Q(b)
    crude = (2*mppi/3)*P(b) + (sqrt(mpf(5))/3)*Q(b)
    gap = crude - RHS(b)
    if gap > worst[0]: worst = (gap, float(b))
    if not (LHS <= crude): print('FAIL LHS<=crude at', b); break
print('max of crude - RHS on [1/2,2/3]: %.6f at b=%.4f (should be <0)' % (worst[0], worst[1]))
# also direct check Gx >= 21/5
loGx = mpf(1e30)
for i in range(2001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    x = mppi - acos(b); s = sqrt(1-b*b)
    Gx = -2*(x*P(b)+s*Q(b))/(s**4*(1+b)**3)
    loGx = min(loGx, Gx)
print('min Gx on c=1/2 curve over b in [1/2,2/3]: %.6f' % loGx)
