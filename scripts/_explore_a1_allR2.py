# -*- coding: utf-8 -*-
# 2026-08-12 缺口 (a') 精确检查: G1<G2 在 {F~e>=0} 上的成立性 + 失败点位置
import math, numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    return brentq(lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt, 1e-13, math.pi/2 - 1e-13)
def alpha2(qt, c):
    return brentq(lambda a: qt*math.tan(a) + math.tan(c*a), math.pi/2 + 1e-13, math.pi - 1e-13)
def Phi(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2
def Mf(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi(qt, x))
def G(qt, c, x):
    Ph = Phi(qt, x); D = qt + c*Ph
    return -Ph*(3 + 2*x*math.cos(x)/math.sin(x))/D + 2*c*x*Ph*(qt*qt-1)*math.sin(x)*math.cos(x)/D**2
def Fe(qt, c):
    return Mf(qt, c, alpha1(qt, c)) - Mf(qt, c, alpha2(qt, c))

Rlist = [1.5, 4.0, 30.0, 100.0, 1000.0, 1e4, 1e5, 1e6]
print("R        qtilde  c*        Fe>=0 区间内 min(G2-G1)  全域 min(G2-G1)  失败点位置(c) 失败点处 Fe 符号")
for R in Rlist:
    qt = 1.0/math.sqrt(R)
    # find c* (unique zero)
    lo, hi = 1e-9, 0.5 - 1e-9
    cstar = brentq(lambda c: Fe(qt, c), lo, hi)
    # coarse scan for failure region
    cs = np.linspace(1e-9, 0.5-1e-9, 4000)
    bads = []
    for c in cs:
        a1 = alpha1(qt, c); a2 = alpha2(qt, c)
        if not (G(qt, c, a1) < G(qt, c, a2)):
            bads.append(c)
    # fine scan on (0, c*]
    cs2 = np.linspace(1e-9, cstar, 3000)
    ming2g1_pos = 1e99
    for c in cs2:
        a1 = alpha1(qt, c); a2 = alpha2(qt, c)
        ming2g1_pos = min(ming2g1_pos, G(qt, c, a2) - G(qt, c, a1))
    # min over whole domain (coarse)
    ming2g1_all = 1e99
    for c in cs:
        a1 = alpha1(qt, c); a2 = alpha2(qt, c)
        ming2g1_all = min(ming2g1_all, G(qt, c, a2) - G(qt, c, a1))
    if bads:
        b0 = bads[0]; b1 = bads[-1]
        f0 = Fe(qt, b0); f1 = Fe(qt, b1)
        print(f"{R:8.0f} {qt:8.4f} {cstar:9.5f} {ming2g1_pos:+10.6f} {ming2g1_all:+10.6f} first={b0:.5f} last={b1:.5f} n={len(bads)} Fe(b0)={f0:+.3e} Fe(b1)={f1:+.3e}")
    else:
        print(f"{R:8.0f} {qt:8.4f} {cstar:9.5f} {ming2g1_pos:+10.6f} {ming2g1_all:+10.6f} none")