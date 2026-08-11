# -*- coding: utf-8 -*-
# 2026-08-12: 验证 R(qt,gamma) <= max(R(qt,gstar), R_bound(qt)) 
# R_bound = 边界 c=1/2 处 R = (1-qt^2) sin^2(gamma0(qt)) / (1+2qt)
import math
import numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)

def R_val(qt, g):
    c = math.atan(qt*math.tan(g))/(math.pi - g)
    a1 = alpha1(qt, c)
    s1 = math.sin(a1); s2 = math.sin(g)
    Del = (math.pi-g)**2*s2*s2 - a1*a1*s1*s1
    T = (1-qt*qt)*s1*s1*s2*s2*((math.pi-g)**2 - a1*a1)
    return c*T/((qt+c)*Del)

print("qt        Rstar(gamma0*)   R_bound(1/2-)   interior max R   <= max(endpoints)?")
worst_excess = 0.0
for qt in [0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005]:
    g0q = math.acos(qt/(1+qt))
    gs = np.linspace(gstar + 1e-8, g0q - 1e-8, 5000)
    mx = 0.0; mg = None
    for g in gs:
        r = R_val(qt, g)
        if r > mx: mx = r; mg = g
    Rstar = R_val(qt, gstar)
    Rbound = (1-qt*qt)*math.sin(g0q)**2/(1+2*qt)
    endmax = max(Rstar, Rbound)
    ok = mx <= endmax + 1e-9
    excess = mx - endmax
    worst_excess = max(worst_excess, excess)
    print(f"{qt:8.4f} {Rstar:10.6f} {Rbound:10.6f} {mx:12.6f} at {mg:.5f}  {ok}  excess={excess:+.2e}")
print("worst excess:", worst_excess)