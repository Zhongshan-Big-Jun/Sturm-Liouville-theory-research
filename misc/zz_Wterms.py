# -*- coding: utf-8 -*-
"""Ranges of W terms T1..T8 on the box."""
import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 120
R = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['T1','T2','T3','T4','T5','T6','T7','T8']}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi - g
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g))
        sg, cg = mp.sin(g), mp.cos(g)
        st, ct = mp.sin(t), mp.cos(t)
        B1 = A*cg - 2*sg
        B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
        B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
        B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
        B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
        T = {}
        T['T1'] = -2*A**3*(A*cg-2*sg)*st*st*ct**4
        T['T2'] = A*A*cg*B2*st*st*ct*ct
        T['T3'] = -2*A**3*sg*t*st*ct**5
        T['T4'] = A*A*sg*t*B4*st*ct**3
        T['T5'] = -A*cg*cg*sg*t*B5*st*ct
        T['T6'] = 4*A*A*cg*sg*sg*t*t*ct**4
        T['T7'] = -A*cg*sg*sg*t*t*B7*ct*ct
        T['T8'] = 6*cg**3*sg**4*t*t
        for k, v in T.items():
            if v < R[k][0]: R[k][0] = v
            if v > R[k][1]: R[k][1] = v
totneg = mp.mpf(0); totpos = mp.mpf(0)
for k in R:
    print('%s: [%.4f, %.4f]' % (k, R[k][0], R[k][1]))
