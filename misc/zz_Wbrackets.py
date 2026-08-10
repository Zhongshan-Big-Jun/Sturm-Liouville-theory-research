# -*- coding: utf-8 -*-
"""Ranges of the bracket factors B1..B8 and W terms on the box."""
import mpmath as mp
mp.mp.dps = 30
import numpy as np
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 120
B = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['B1','B2','B4','B5','B7','W']}
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
        Wv = ( -2*A**3*(A*cg-2*sg)*st*st*ct**4
               + A*A*cg*B2*st*st*ct*ct
               - 2*A**3*sg*t*st*ct**5
               + A*A*sg*t*B4*st*ct**3
               - A*cg*cg*sg*t*B5*st*ct
               + 4*A*A*cg*sg*sg*t*t*ct**4
               - A*cg*sg*sg*t*t*B7*ct*ct
               + 6*cg**3*sg**4*t*t )
        for k, v in [('B1',B1),('B2',B2),('B4',B4),('B5',B5),('B7',B7),('W',Wv)]:
            if v < B[k][0]: B[k][0] = v
            if v > B[k][1]: B[k][1] = v
for k in B:
    print('%s: [%.5f, %.5f]' % (k, B[k][0], B[k][1]))
