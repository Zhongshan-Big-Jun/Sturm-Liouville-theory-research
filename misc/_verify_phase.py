# -*- coding: utf-8 -*-
import sys, math
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import numpy as np
from gap_lib import lams_fast

R = 10000.0
t = 0.02
blocks = [(t, 1.0), (1-t, R)]
s = lams_fast(blocks, 2, npts=20000)
print("TM roots s:", s, " lambda:", s**2, " D:", s[1]**2 - s[0]**2)

# phase-coordinate formula: mu=sqrt(R), c = mu*(1-t)/t; roots x1<x2 of theta(x)+c x = k pi
mu = math.sqrt(R)
c = mu*(1-t)/t
def theta(x):
    return math.atan(mu*math.tan(x)) + math.pi*round(x/math.pi - 0.5) if False else None
# continuous branch: theta(x+pi)=theta(x)+pi
def th(x):
    k = math.floor((x + math.pi/2)/math.pi)
    xr = x - k*math.pi
    v = math.atan(mu*math.tan(xr)) if math.cos(xr) != 0 else math.pi/2
    return v + k*math.pi
# find first two roots of th(x) + c*x = k*pi
xs = []
for k in (1, 2):
    f = lambda x: th(x) + c*x - k*math.pi
    # scan
    lo = None
    prev = None
    for i in range(20000):
        x = (i+1)*1e-4
        v = f(x)
        if prev is not None and prev*v < 0:
            lo = (i)*1e-4
            break
        prev = v
    # bisect
    a, b = lo, lo+1e-4
    for _ in range(100):
        m = 0.5*(a+b)
        if f(a)*f(m) <= 0: b = m
        else: a = m
    xs.append(0.5*(a+b))
print("phase roots x:", xs)
W = (mu+c)**2*(xs[1]**2-xs[0]**2)
print("W =", W, " 3pi^2 =", 3*math.pi**2, " 3pi^2 mu^2 =", 3*math.pi**2*mu**2)
lam_ph = [(x*(mu+c)/mu)**2 for x in xs]
print("phase lambda:", lam_ph, " D:", lam_ph[1]-lam_ph[0])