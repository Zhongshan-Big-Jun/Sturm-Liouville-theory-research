# -*- coding: utf-8 -*-
import math
import numpy as np

def phase_D(mu, c):
    def th(x):
        k = math.floor((x + math.pi/2)/math.pi)
        xr = x - k*math.pi
        v = math.atan(mu*math.tan(xr)) if abs(math.cos(xr)) > 1e-15 else math.pi/2
        return v + k*math.pi
    xmax = 2*math.pi/(c + 1.0/mu) + 0.5
    step = min(1e-4, 0.1*math.pi/(c + mu))
    xs = []
    for kk in (1, 2):
        f = lambda x: th(x) + c*x - kk*math.pi
        prev = f(0.0); lo = None
        n = int(xmax/step)+2
        for i in range(1, n):
            x = i*step
            if x > xmax: break
            v = f(x)
            if prev*v < 0:
                lo = (i-1)*step; break
            prev = v
        assert lo is not None, (mu, c, kk, "no bracket")
        a, b = lo, lo+step
        for _ in range(120):
            m = 0.5*(a+b)
            if f(a)*f(m) <= 0: b = m
            else: a = m
        xs.append(0.5*(a+b))
    return (mu+c)**2*(xs[1]**2-xs[0]**2)/mu**2

pi2 = math.pi**2
worst_lo = 1e9; worst_hi = 1e9
bad = 0
for R in [1.05, 1.1, 1.5, 2, 3, 4, 10, 100, 1e4]:
    mu = math.sqrt(R)
    for t in np.linspace(0.001, 0.999, 120):
        c = mu*(1-t)/t
        D = phase_D(mu, c)
        lo = 3*pi2/R; hi = 3*pi2
        if not (D > lo and D < hi):
            bad += 1
            print("VIOLATION", R, t, D, lo, hi)
            break
        worst_lo = min(worst_lo, (D-lo)/lo); worst_hi = min(worst_hi, (hi-D)/hi)
print("two-block bound scan done; violations:", bad)
print("min relative margin lo %.2e  hi %.2e" % (worst_lo, worst_hi))
print("f_sym(1/2) = %.6f vs %.6f" % (pi2*2, 2*pi2))
print("4pi/(3 sqrt3) = %.10f" % (4*math.pi/(3*math.sqrt(3))))