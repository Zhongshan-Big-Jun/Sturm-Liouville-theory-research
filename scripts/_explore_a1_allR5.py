# -*- coding: utf-8 -*-
import math
import numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def Phi(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2
def Mf(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi(qt, x))
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)

def tension(qt, g):
    c = math.atan(qt*math.tan(g))/(math.pi - g)
    a1 = alpha1(qt, c)
    s1 = math.sin(a1); s2 = math.sin(g)
    Ph1 = Phi(qt, a1); Ph2 = Phi(qt, g)
    A = a1*a1*s1*s1 - (math.pi-g)**2*s2*s2
    C = a1*a1*s1*s1*Ph2 - (math.pi-g)**2*s2*s2*Ph1
    return c*C/(qt*(-A)) if C > 0 else -1.0

# 检查: T(qt,gamma) <= T(qt,gstar) + tol  对所有 gamma
print("== T(qt,gamma) <= T(qt,gstar)? ==")
worst = 0.0
for qt in [0.8, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
    g0q = math.acos(qt/(1+qt))
    gs = np.linspace(gstar + 1e-6, g0q - 1e-6, 2000)
    Tstar = tension(qt, gstar)
    mx = -1.0
    for g in gs:
        T = tension(qt, g)
        mx = max(mx, T)
    excess = mx - Tstar
    worst = max(worst, excess)
    print(f"qt={qt:7.4f} Tstar={Tstar:+.6f} maxT={mx:+.6f} excess={excess:+.2e}")
print("worst excess:", worst)

def Fe_real(qt, c):
    a2 = brentq(lambda a: qt*math.tan(a) + math.tan(c*a), math.pi/2 + 1e-13, math.pi - 1e-13)
    return Mf(qt, c, alpha1(qt, c)) - Mf(qt, c, a2)

print("== gamma(c*) <= gstar 直接验证 ==")
ok = True
for qt in [0.99, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.001]:
    cstar = brentq(lambda c: Fe_real(qt, c), 1e-10, 0.5 - 1e-10)
    a2s = brentq(lambda a: qt*math.tan(a) + math.tan(cstar*a), math.pi/2 + 1e-13, math.pi - 1e-13)
    gc = math.pi - a2s
    if not (gc < gstar): ok = False
    print(f"qt={qt:7.4f} c*={cstar:9.5f} gamma(c*)={gc:9.5f} < gstar={gstar:.5f}? {gc < gstar}")
print("ALL gamma(c*)<gstar:", ok)