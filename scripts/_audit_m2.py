# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50
def M2_expr(q, w):
    A = mp.pi - mp.atan(w/q); v = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + v*(4*A*w - 5*q - 9*q*w*w)
for w in [0.5, 1.0, 2.0]:
    M2_1 = M2_expr(mp.mpf('1'), mp.mpf(w))
    h = 4*w*(mp.pi - mp.atan(w)) - 5 - 9*w*w
    print("w=", w, "M2(1,w)=", float(M2_1), "pi*h=", float(mp.pi*h), "diff=", float(M2_1 - mp.pi*h))
