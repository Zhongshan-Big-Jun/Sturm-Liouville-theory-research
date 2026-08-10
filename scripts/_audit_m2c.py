# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 50
def M2_expr(q, w):
    A = mp.pi - mp.atan(w/q); v = mp.atan(w)
    return 4*A*A*w*q - 7*A*q*q - 9*A*w*w + 2*A*(q*q+w*w)/(1+w*w) + v*(4*A*w - 5*q - 9*q*w*w)
for wv in [0.05, 0.5, 1.0, 2.0, 3.0, 5.0]:
    w = mp.mpf(wv)
    h = 4*w*(mp.pi - mp.atan(w)) - 5 - 9*w*w
    M2_1 = M2_expr(mp.mpf('1'), w)
    assert abs(h - M2_1/mp.pi) < mp.mpf('1e-45')
    assert h < 0
print("M2(1,w)=pi*h(w)<0 OK")
