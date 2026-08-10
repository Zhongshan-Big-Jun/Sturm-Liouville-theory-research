# -*- coding: utf-8 -*-
"""t3_c12_bound3.py"""
from mpmath import mp, mpf, sqrt, acos, pi as mppi
mp.dps = 40
def P(b): return 2*b**6 + b**5 - 4*b**4 + 4*b**2 - b - 2
def Q(b): return 7*b**5 + 11*b**4 - 6*b**3 - 14*b**2 - b + 3
worst = (mpf('-1e30'), None); loGx = mpf(1e30); worst2=(mpf('1e30'),None)
for i in range(4001):
    b = mpf('0.5') + mpf(i)*mpf('1')/6000
    if b > mpf('2')/3: break
    x = mppi - acos(b); s = sqrt(1-b*b)
    F = (2*mppi/3)*P(b) + (sqrt(mpf(5))/3)*Q(b) + mpf('21')/10*(1-b*b)**2*(1+b)**3
    if F > worst[0]: worst = (F, float(b))
    Gx = -2*(x*P(b)+s*Q(b))/(s**4*(1+b)**3)
    loGx = min(loGx, Gx)
    # also gap for direct Gx - 21/5
    gap = Gx - mpf('21')/5
    if gap < worst2[0]: worst2 = (gap, float(b))
print('max F(b)=crude-RHS: %.8f at b=%.4f' % (worst[0], worst[1]))
print('min Gx on c=1/2: %.8f ; min gap Gx-21/5: %.8f at b=%.4f' % (loGx, worst2[0], worst2[1]))
# F at endpoints and check derivative sign pattern
for b in [mpf('0.5'), mpf('0.55'), mpf('0.6'), mpf('0.65'), mpf('2')/3]:
    F = (2*mppi/3)*P(b) + (sqrt(mpf(5))/3)*Q(b) + mpf('21')/10*(1-b*b)**2*(1+b)**3
    print('b=%.4f: F=%.6f' % (b, F))
