# -*- coding: utf-8 -*-
import mpmath as mp
from mpmath import iv
iv.dps = 40
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cert_lib import F_iv, Fs_iv, Fa_iv, Fb_iv
from fast_lib import cfg, sec

def P(x): return iv.mpf((mp.mpf(float(x)), mp.mpf(float(x))))
a0 = float(mp.acos(mp.mpf(1)/4)/mp.pi)
b = 0.7; R = 1.0005
s1f, s2f, _, _ = cfg(a0, b, R)
s = s1f
# compare Fb_iv with finite difference of F_iv
fb_iv = Fb_iv(P(s), P(a0), P(b), P(R))
h = 1e-6
fd = (float(F_iv(P(s), P(a0), P(b+h), P(R)).a) - float(F_iv(P(s), P(a0), P(b-h), P(R)).a))/(2*h)
fd_s = (float(F_iv(P(s+h), P(a0), P(b), P(R)).a) - float(F_iv(P(s-h), P(a0), P(b), P(R)).a))/(2*h)
fa_iv = Fa_iv(P(s), P(a0), P(b), P(R))
fd_a = (float(F_iv(P(s), P(a0+h), P(b), P(R)).a) - float(F_iv(P(s), P(a0-h), P(b), P(R)).a))/(2*h)
print("Fb_iv =", fb_iv, " FD_b =", fd)
print("Fa_iv =", fa_iv, " FD_a =", fd_a)
print("Fs_iv =", Fs_iv(P(s), P(a0), P(b), P(R)), " FD_s =", fd_s)
print("F at point:", F_iv(P(s), P(a0), P(b), P(R)))
