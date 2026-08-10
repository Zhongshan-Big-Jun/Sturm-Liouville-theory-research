# -*- coding: utf-8 -*-
"""Check W'(c) < 0 on (0,1/3] for mu > 1. mpmath at 50 digits: the margin
W' ~ -C*(mu^2-1)*c^2 is below double-precision resolution near c=0.
mu=1 is degenerate (W=3*pi^2 constant, W'=0 identically) and is excluded."""
import mpmath as mp
mp.mp.dps = 50

def theta(x, mu):
    return mp.atan(mu*mp.tan(x)) + mp.pi*mp.floor((x+mp.pi/2)/mp.pi)

def thp(x, mu):
    t = mp.tan(x)
    return mu*(1+t*t)/(1+mu*mu*t*t)

def xk(mu, c, k):
    # F = theta + c*x strictly increasing on (0, k*pi), F(k*pi) > k*pi
    lo, hi = mp.mpf(0), mp.mpf(k)*mp.pi
    for _ in range(200):
        mid = (lo+hi)/2
        if theta(mid, mu) + c*mid > k*mp.pi:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2

def Wp(mu, c):
    x1, x2 = xk(mu, c, 1), xk(mu, c, 2)
    U = x2**2 - x1**2
    p1, p2 = thp(x1, mu), thp(x2, mu)
    Up = -2*x2**2/(p2+c) + 2*x1**2/(p1+c)
    return 2*(mu+c)*U + (mu+c)**2*Up

allok = True
for mu in [mp.mpf('1.001'), mp.mpf('1.05'), mp.mpf('1.1'), mp.mpf('1.2'),
           mp.mpf('1.5'), mp.mpf('2'), mp.mpf('3'), mp.mpf('5'),
           mp.mpf('10'), mp.mpf('100'), mp.mpf('10000')]:
    cs = [mp.mpf('1e-12')*mp.mpf('10')**(i/10) for i in range(0, 121)]
    cs += [mp.mpf(i)/1000 for i in range(1, 334)]  # 0.001 .. 0.333
    worst = None; worst_arg = None
    for c in cs:
        if c > mp.mpf(1)/3:
            break
        v = Wp(mu, c)
        if worst is None or v > worst:
            worst, worst_arg = v, c
    ok = (worst is not None) and (worst < 0)
    allok = allok and ok
    print(f"mu={mu}: max W' on (0,1/3] = {worst} at c={worst_arg}  (<0 ? {ok})")
print("ALL DECREASING (mu>1):", allok)
