# -*- coding: utf-8 -*-
"""map_dG2dq.py -- map dG2/dq over (q,c), find danger zones."""
import sys, mpmath as mp
sys.path.insert(0, r'F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T050000Z-keylemma2-5A35E5\reproducibility')
import kl2_lib as L
mp.mp.dps = 30

def dG2dq(c, q):
    h = mp.mpf('1e-6')*q
    return (L.G2(c, q+h) - L.G2(c, q-h))/(2*h)

qs = [mp.mpf('1.01'), mp.mpf('1.05'), mp.mpf('1.1'), mp.mpf('1.2'), mp.mpf('1.5'), mp.mpf('2'), mp.mpf('3'), mp.mpf('5'),
      mp.mpf('10'), mp.mpf('30'), mp.mpf('100'), mp.mpf('300'), mp.mpf('1000'), mp.mpf('3000'), mp.mpf('10000'), mp.mpf('100000')]
cs = [mp.mpf('0.01'), mp.mpf('0.03'), mp.mpf('0.05'), mp.mpf('0.1'), mp.mpf('0.2'), mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.49')]
print('dG2/dq table (rows q, cols c):')
hdr = 'q      ' + ''.join('%9s' % mp.nstr(c,3) for c in cs)
print(hdr)
for q in qs:
    row = '%6s ' % mp.nstr(q,5)
    for c in cs:
        v = dG2dq(c, q)
        row += '%9s' % mp.nstr(v,4)
    print(row)
print()
# minimum over the table
mn = mp.inf; at = None
for q in qs:
    for c in cs:
        v = dG2dq(c, q)
        if v < mn: mn, at = v, (q, c)
print('min over table:', mp.nstr(mn, 8), 'at', mp.nstr(at[0],5), mp.nstr(at[1],5))
