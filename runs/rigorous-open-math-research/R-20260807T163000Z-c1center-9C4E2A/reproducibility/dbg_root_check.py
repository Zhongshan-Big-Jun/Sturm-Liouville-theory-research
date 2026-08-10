# -*- coding: utf-8 -*-
import mpmath as mp
mp.mp.dps = 60
a0f = float(mp.acos(mp.mpf(1)/4)/mp.pi)
am, bm = mp.mpf(a0f), mp.mpf(0.5)

def sec_R(s, R0v):
    q = mp.sqrt(R0v); al = s*am; be = s*(1-bm); th = s*q*(bm-am)
    return (mp.cos(be)*mp.cos(th)*mp.sin(al) - q*mp.sin(be)*mp.sin(th)*mp.sin(al)
            + (mp.cos(be)*mp.sin(th)/q)*mp.cos(al) + mp.sin(be)*mp.cos(th)*mp.cos(al))

for R0v in (mp.mpf(1.01), 1 + mp.mpf(0.01), mp.mpf("1.01")):
    print("R =", mp.nstr(R0v, 30))
    for s in (mp.mpf("3.139121071538"), mp.mpf("3.140332703874"), mp.pi):
        print("   sec(%.12f) = %.6e" % (s, sec_R(s, R0v)))
# scan for roots near pi
for R0v in (mp.mpf("1.01"),):
    pts = [mp.mpf(3.13) + mp.mpf(k)*mp.mpf("0.002") for k in range(10)]
    vals = [sec_R(p, R0v) for p in pts]
    print("scan R=1.01:")
    for p, v in zip(pts, vals):
        print("   s=%.6f  sec=%.4e" % (p, v))
