# -*- coding: utf-8 -*-
# 2026-08-12 缺口 (a'): 对称线全 R 探索 (EVIDENCE only)
# 检查: G1<0, G1<G2, F~e 唯一零点, 端点符号, 对 q̃ in (0,1), c in (0,1/2)
import math, numpy as np
from scipy.optimize import brentq

def alpha1(qt, c):
    # tan(a) tan(c a) = 1/qt, a in (0, pi/2)
    f = lambda a: math.tan(a)*math.tan(c*a) - 1.0/qt
    return brentq(f, 1e-12, math.pi/2 - 1e-12)

def alpha2(qt, c):
    # qt tan(a) + tan(c a) = 0, a in (pi/2, pi) for c < 1/2
    f = lambda a: qt*math.tan(a) + math.tan(c*a)
    return brentq(f, math.pi/2 + 1e-12, math.pi - 1e-12)

def Phi(qt, x):
    return math.cos(x)**2 + qt*qt*math.sin(x)**2

def Mf(qt, c, x):
    return x*x*math.sin(x)**2/(qt + c*Phi(qt, x))

def G(qt, c, x):
    Ph = Phi(qt, x)
    D = qt + c*Ph
    t1 = -Ph*(3 + 2*x*math.cos(x)/math.sin(x))/D
    t2 = 2*c*x*Ph*(qt*qt-1)*math.sin(x)*math.cos(x)/D**2
    return t1 + t2

def Fe(qt, c):
    a1 = alpha1(qt, c); a2 = alpha2(qt, c)
    return Mf(qt, c, a1) - Mf(qt, c, a2)

Rlist = [1.01, 1.2, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 30.0, 100.0, 1000.0]
cgrid = np.linspace(1e-6, 0.5-1e-6, 2000)
print("R, qtilde, F~e(0+)_sign, F~e(1/2)_sign, zero_count, c*, G1_max, G1<G2 everywhere?, min(G2-G1)")
for R in Rlist:
    qt = 1.0/math.sqrt(R)
    vals = [Fe(qt, c) for c in cgrid]
    signs = [1 if v > 0 else (-1 if v < 0 else 0) for v in vals]
    zc = 0
    for i in range(1, len(signs)):
        if signs[i] != signs[i-1]:
            zc += 1
    # zero via brentq on sign change
    cstar = None
    for i in range(1, len(cgrid)):
        if vals[i-1]*vals[i] < 0:
            cstar = brentq(lambda c: Fe(qt, c), cgrid[i-1], cgrid[i])
            break
    g1max = -1e99; ming2g1 = 1e99; bad = []
    for c in cgrid:
        a1 = alpha1(qt, c); a2 = alpha2(qt, c)
        g1 = G(qt, c, a1); g2 = G(qt, c, a2)
        g1max = max(g1max, g1)
        ming2g1 = min(ming2g1, g2 - g1)
        if not (g1 < 0 and g1 < g2):
            bad.append(c)
    print(f"{R:8.2f} {qt:8.4f} {signs[0]:+d} {signs[-1]:+d} zc={zc} c*={cstar if cstar else 'none':>8.4f} G1max={g1max:+.6f} min(G2-G1)={ming2g1:+.6f} bad_c={len(bad)}")