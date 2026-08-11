# -*- coding: utf-8 -*-
# 2026-08-12 探索: 非负集 (0,c*] 上 W0(gamma) 符号与 G1<G2 的证明候选
import math
from scipy.optimize import brentq
import numpy as np

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def alpha2(qt, c):
    return brentq(lambda a: qt*math.tan(a) + math.tan(c*a), math.pi/2 + 1e-13, math.pi - 1e-13)
def Phi(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2
def Mf(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi(qt, x))
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
def Fe(qt, c):
    return Mf(qt, c, alpha1(qt, c)) - Mf(qt, c, alpha2(qt, c))

# W0 的零点 gamma0* in (0, pi/2)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)
print("W0 零点 gamma0* =", gstar, "=", gstar*180/math.pi, "deg")

qlist = [0.9, 0.8, 0.8165, 0.7071, 0.6, 0.5, 0.4, 0.3162, 0.25, 0.1826, 0.1, 0.05, 0.0316, 0.01, 0.0032, 0.001]
print("qt      c*        gamma(c*)  W0(gamma*)  alpha1(c*)  W0<=0?   min(G2-G1) on (0,c*]   gamma0(qt)")
for qt in qlist:
    cstar = brentq(lambda c: Fe(qt, c), 1e-10, 0.5 - 1e-10)
    g = math.pi - alpha2(qt, cstar)
    a1 = alpha1(qt, cstar)
    w = W0(g)
    g0q = math.acos(qt/(1+qt))
    # min G2-G1 on (0, c*]
    cs = np.linspace(1e-8, cstar, 400)
    m = 1e99
    for c in cs:
        x1 = alpha1(qt, c); x2 = alpha2(qt, c)
        Ph1 = Phi(qt, x1); Ph2 = Phi(qt, x2)
        D1 = qt + c*Ph1; D2 = qt + c*Ph2
        g1 = -Ph1*(3 + 2*x1*math.cos(x1)/math.sin(x1))/D1 + 2*c*x1*Ph1*(qt*qt-1)*math.sin(x1)*math.cos(x1)/D1**2
        gg = math.pi - x2
        W0v = W0(gg)
        g2 = -Ph2*W0v/D2 + 2*c*(math.pi-gg)*Ph2*(1-qt*qt)*math.sin(gg)*math.cos(gg)/D2**2
        m = min(m, g2 - g1)
    print(f"{qt:8.4f} {cstar:9.5f} {g:9.5f} {w:+10.5f} {a1:9.5f} {str(w<=0):5s} {m:+12.5f} {g0q:9.5f}")