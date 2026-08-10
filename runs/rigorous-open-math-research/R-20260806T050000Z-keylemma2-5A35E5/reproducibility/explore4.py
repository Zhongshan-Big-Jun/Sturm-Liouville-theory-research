# -*- coding: utf-8 -*-
"""explore4.py -- dG1dc, dG2dc signs over the full domain."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

def dG1dc(c, q):
    h = mp.mpf('1e-6')
    return (L.G1(c+h, q) - L.G1(c-h, q))/(2*h)
def dG2dc(c, q):
    h = mp.mpf('1e-6')
    return (L.G2(c+h, q) - L.G2(c-h, q))/(2*h)

qs = [mp.mpf('1.01'), mp.mpf('1.05'), mp.mpf('1.1'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('3'),
      mp.mpf('5'), mp.mpf('10'), mp.mpf('30'), mp.mpf('100'), mp.mpf('1000')]
cs = [mp.mpf('0.01'), mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.45'), mp.mpf('0.49')]
print('dG1/dc:')
for q in qs:
    row = '%6s ' % mp.nstr(q,5)
    for c in cs:
        row += '%9s' % mp.nstr(dG1dc(c,q),5)
    print(row)
print()
print('dG2/dc:')
for q in qs:
    row = '%6s ' % mp.nstr(q,5)
    for c in cs:
        row += '%9s' % mp.nstr(dG2dc(c,q),5)
    print(row)
print()
# minima/maxima
mn1 = mp.inf; mx1 = -mp.inf; mn2 = mp.inf; mx2 = -mp.inf; at = {}
for q in qs:
    for c in cs:
        v1 = dG1dc(c,q); v2 = dG2dc(c,q)
        if v1 < mn1: mn1, at['mn1'] = v1, (q,c)
        if v1 > mx1: mx1, at['mx1'] = v1, (q,c)
        if v2 < mn2: mn2, at['mn2'] = v2, (q,c)
        if v2 > mx2: mx2, at['mx2'] = v2, (q,c)
print('dG1dc: min', mp.nstr(mn1,6), 'at', at['mn1'], ' max', mp.nstr(mx1,6), 'at', at['mx1'])
print('dG2dc: min', mp.nstr(mn2,6), 'at', at['mn2'], ' max', mp.nstr(mx2,6), 'at', at['mx2'])
