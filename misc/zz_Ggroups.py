# -*- coding: utf-8 -*-
"""Check key group-inequality expressions on the box."""
import mpmath as mp
mp.mp.dps = 30
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
N = 150
R = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['G1','G2','G3a','G3b','G4','G5']}
for i in range(N+1):
    g = glo + mp.mpf(i)*(ghi-glo)/N
    A = mp.pi - g
    for j in range(N+1):
        q = 1 + mp.mpf(j)/N
        t = mp.atan(q*mp.tan(g))
        sg, cg = mp.sin(g), mp.cos(g)
        st, ct = mp.sin(t), mp.cos(t)
        Phi = cg*cg + q*q*sg*sg
        B1 = A*cg - 2*sg
        B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
        B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
        B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
        B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
        G1 = Phi*B5 - A*B4
        G2 = 4*A*A*ct**4 - A*B7*ct*ct + 6*cg*cg*sg*sg
        G3a = -2*A**3*B1*ct*ct + A*A*cg*B2          # bracket for T1+T2 (partial)
        G3b = -2*A**3*(A*cg-2*sg)*ct**4 + A*A*cg*B2*ct*ct   # T1+T2 combined /(st^2)
        G4 = A*A*sg*t*B4*ct**3 + (-A*cg*cg*sg*t*B5*st*ct)   # = T4+T5 recheck
        G5 = B5 - A*B4
        vals = {'G1': G1, 'G2': G2, 'G3a': G3a, 'G3b': G3b, 'G4': G4, 'G5': G5}
        for k, v in vals.items():
            if v < R[k][0]: R[k][0] = v
            if v > R[k][1]: R[k][1] = v
for k in R:
    print('%s: [%.6f, %.6f]' % (k, R[k][0], R[k][1]))
