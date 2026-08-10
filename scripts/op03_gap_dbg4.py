# -*- coding: utf-8 -*-
"""Correct independent check: y(x) = M01*cos(wd) + M11*sin(wd)/w."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise
from op03_gap_n1 import eigfuns_at

R = 4.0
u = 0.4515
blocks = [(u,1.0),(1-2*u,R),(u,1.0)]
s = lams_precise(blocks, 3)
lam = s**2

def y_correct(x, ss):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in blocks:
        x1 = x0 + L
        if x <= x1:
            w = ss*np.sqrt(c); d = x - x0
            return M01*np.cos(w*d) + M11*np.sin(w*d)/w
        w = ss*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
    raise ValueError

def exact_norm(ss):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    norm = 0.0
    for L, c in blocks:
        w = ss*np.sqrt(c)
        A = M01; B = M11/w
        Icos = 0.5*(L + np.sin(2*w*L)/(2*w))
        Isin = 0.5*(L - np.sin(2*w*L)/(2*w))
        Icross = np.sin(w*L)**2/(2*w)
        norm += c*(A*A*Icos + B*B*Isin + 2*A*B*Icross)
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
    return norm

pts = np.array([u])
vp = eigfuns_precise(blocks, s[:2], pts)
vc = eigfuns_at(blocks, lam[:2], pts)
for k in range(2):
    yj = y_correct(u, s[k]); nrm = exact_norm(s[k])
    print(f"k={k}: y(u)={yj:.10f} norm={nrm:.10f} -> u(u)^2={yj**2/nrm:.10f}")
print("precise routine:", vp[0,0]**2, vp[1,0]**2)
print("coarse routine:", vc[0,0]**2, vc[1,0]**2)
# f at junction
f_prec = lam[0]*vp[0,0]**2 - lam[1]*vp[1,0]**2
f_corr = lam[0]*y_correct(u,s[0])**2/exact_norm(s[0]) - lam[1]*y_correct(u,s[1])**2/exact_norm(s[1])
f_coarse = lam[0]*vc[0,0]**2 - lam[1]*vc[1,0]**2
print(f"f(u): precise={f_prec:.6f} correct={f_corr:.6f} coarse={f_coarse:.6f}")
