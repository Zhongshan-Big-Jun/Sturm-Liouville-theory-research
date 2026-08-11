# -*- coding: utf-8 -*-
# 2026-08-12: 策略 S2 检查 - 在 (c0(qt), 1/2) 上 F~e' 的符号; G1, G2, M1, M2 分量
import math
import numpy as np
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
def W0(g):
    return 3 - 2*(math.pi - g)*math.cos(g)/math.sin(g)
gstar = brentq(W0, 1e-9, math.pi/2 - 1e-9)
c0q = lambda qt: math.atan(qt*math.tan(gstar))/(math.pi - gstar)

print("qt       c0(qt)   F~e'(c) 符号于 (c0, 1/2)    G2 符号区间    min F~e'(数值)   F~e(c0) 符号")
for qt in [0.9, 0.7, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02, 0.01, 0.005, 0.002, 0.001]:
    c0 = c0q(qt)
    cs = np.linspace(c0 + 1e-8, 0.5 - 1e-8, 1200)
    minFp = 1e99; pos = neg = 0; g2neg = g2pos = 0; Fe0 = None
    for c in cs:
        a1 = alpha1(qt, c); a2 = alpha2(qt, c)
        M1 = Mf(qt, c, a1); M2 = Mf(qt, c, a2)
        g1 = G(qt, c, a1); g2 = G(qt, c, a2)
        Fp = M1*g1 - M2*g2
        minFp = min(minFp, Fp)
        if Fp >= 0: pos += 1
        else: neg += 1
        if g2 >= 0: g2pos += 1
        else: g2neg += 1
    Fe0 = Mf(qt, c0, alpha1(qt, c0)) - Mf(qt, c0, alpha2(qt, c0))
    print(f"{qt:6.3f} {c0:9.5f}  pos={pos:5d} neg={neg:5d} ({'ALL>0' if neg==0 else 'has<=0'})  G2>=0:{g2pos}/{g2neg}  minFp={minFp:+.6f}  Fe(c0)={'NEG' if Fe0<0 else 'POS'}")