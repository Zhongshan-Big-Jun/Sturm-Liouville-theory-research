# -*- coding: utf-8 -*-
# 2026-08-12: 量化 M1<M2 (gamma >= gamma0*) 的证明张力
# M1<M2 <=> q* A + c C < 0, A = a1^2 s1^2 - (pi-g)^2 s2^2 < 0 (gamma>=gamma0*)
# 检查张力比 c*C/(q*(-A)) 是否 < 1, 以及 A, C 的行为
import math
import numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def Phi(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2
def Mf(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi(qt, x))
def Fe(qt, c):
    a1 = alpha1(qt, c)
    return Mf(qt, c, a1) - Mf(qt, c, math.pi - 0.0)  # placeholder unused

def gamma_from_c(qt, c):
    # solve qt*tan(a2) + tan(c*a2) = 0 for a2 in (pi/2, pi)
    a2 = brentq(lambda a: qt*math.tan(a) + math.tan(c*a), math.pi/2 + 1e-13, math.pi - 1e-13)
    return math.pi - a2

# W0 零点
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)

qlist = [0.99, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01, 0.001]
print("qt      max_tension(c*C/(q*(-A)))  at gamma  (gamma>=gamma0*)   A<0 全域?")
for qt in qlist:
    g0q = math.acos(qt/(1+qt))
    # sample gamma in [gstar, g0q) and for each: c = arctan(qt*tan g)/(pi-g), alpha1 from c
    gs = np.linspace(gstar + 1e-6, g0q - 1e-6, 1500)
    mt = -1.0; mg = None
    for g in gs:
        c = math.atan(qt*math.tan(g))/(math.pi - g)
        if not (0 < c < 0.5): continue
        a1 = alpha1(qt, c)
        s1 = math.sin(a1); s2 = math.sin(g)
        Ph1 = Phi(qt, a1); Ph2 = Phi(qt, g)
        A = a1*a1*s1*s1 - (math.pi-g)**2*s2*s2
        C = a1*a1*s1*s1*Ph2 - (math.pi-g)**2*s2*s2*Ph1
        if A >= -1e-12:
            print("  !! A>=0 at", qt, g, A); break
        tens = c*C/(qt*(-A)) if C > 0 else -1.0
        if tens > mt:
            mt = tens; mg = g
    print(f"{qt:6.3f} {mt:+10.5f} {mg if mg else 0:9.5f}")