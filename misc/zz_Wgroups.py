# -*- coding: utf-8 -*-
"""Check grouped terms on the box: P1=T4+T5, P2=T6+T7+T8, P3=T1+T2+T3, and sub-groups."""
import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 150
R = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['P1','P2','P3','T45','T1_2','W']}
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
        T1 = -2*A**3*(A*cg-2*sg)*st*st*ct**4
        T2 = A*A*cg*B2*st*st*ct*ct
        T3 = -2*A**3*sg*t*st*ct**5
        T4 = A*A*sg*t*B4*st*ct**3
        T5 = -A*cg*cg*sg*t*B5*st*ct
        T6 = 4*A*A*cg*sg*sg*t*t*ct**4
        T7 = -A*cg*sg*sg*t*t*B7*ct*ct
        T8 = 6*cg**3*sg**4*t*t
        vals = {'P1': T4+T5, 'P2': T6+T7+T8, 'P3': T1+T2+T3, 'T45': T4+T5+T2+T7, 'T1_2': T1+T2, 'W': T1+T2+T3+T4+T5+T6+T7+T8}
        for k, v in vals.items():
            if v < R[k][0]: R[k][0] = v
            if v > R[k][1]: R[k][1] = v
for k in R:
    print('%s: [%.5f, %.5f]' % (k, R[k][0], R[k][1]))
