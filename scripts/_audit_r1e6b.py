# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import brentq
import mpmath as mp
mp.mp.dps = 60

def y1_grid(a, b, q, sgrid):
    s = sgrid
    y = np.zeros_like(s); dy = np.ones_like(s)
    om = s; t = a
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s*q; t = b-a
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    om = s; t = 1-b
    c, sn = np.cos(om*t), np.sin(om*t)
    y, dy = y*c + dy*sn/om, -y*om*sn + dy*c
    return y

def residual_fast(a, b, q, N=100000):
    top = 2*np.pi + 1e-3
    grid = np.linspace(1e-9, top, N)
    ys = y1_grid(a, b, q, grid)
    idx = np.where(np.diff(np.sign(ys)) != 0)[0]
    assert len(idx) >= 2, (a, b, q, len(idx))
    ss = []
    for i in range(2):
        s = brentq(lambda t: float(y1_grid(a, b, q, np.array([t]))[0]), grid[idx[i]], grid[idx[i]+1], xtol=1e-14, rtol=1e-14)
        ss.append(s)
    s1, s2 = ss
    l1, l2 = s1**2, s2**2
    def mode(s):
        om1 = s
        yA, dyA = np.sin(om1*a)/om1, np.cos(om1*a)
        om2 = s*q
        ya, dya = yA, dyA
        c, sn = np.cos(om2*(b-a)), np.sin(om2*(b-a))
        yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
        om3 = s
        n = (a/2 - np.sin(2*s*a)/(4*s))/s**2
        amp2 = ya**2 + (dya/om2)**2
        cross = ya*dya/om2
        L = b-a
        n += q**2 * ( amp2*L/2 + (ya**2 - (dya/om2)**2)*np.sin(2*om2*L)/(4*om2) + cross*(1-np.cos(2*om2*L))/(2*om2) )
        amp2b = yb**2 + (dyb/om3)**2
        crossb = yb*dyb/om3
        L = 1-b
        n += amp2b*L/2 + (yb**2 - (dyb/om3)**2)*np.sin(2*om3*L)/(4*om3) + crossb*(1-np.cos(2*om3*L))/(2*om3)
        return ya, yb, n
    ya1, yb1, n1 = mode(s1)
    ya2, yb2, n2 = mode(s2)
    R1 = l1*ya1**2/n1 - l2*ya2**2/n2
    R2 = l1*yb1**2/n1 - l2*yb2**2/n2
    return R1, R2, ya2/ya1, yb2/yb1, s1, s2

print("=== R=1000 (q=31.62): root between 0.495 and 0.498 ===")
for R in [1000.0]:
    q = np.sqrt(R)
    for xi in [0.4960, 0.4962, 0.4964, 0.4966]:
        R1, R2, v_a, v_b, s1, s2 = residual_fast(xi, 1-xi, q)
        print(f"  xi={xi}: R1={R1:.4e} v_a={v_a:+.6f} v_b={v_b:+.6f}")

print("=== R=1e6 (q=1000): root near xi*=q/(2(c*+q)) with c*=0.23982 -> 0.4998801 ===")
R = 1e6; q = np.sqrt(R)
for xi in [0.49980, 0.49985, 0.49988, 0.49990, 0.49995]:
    R1, R2, v_a, v_b, s1, s2 = residual_fast(xi, 1-xi, q)
    print(f"  xi={xi}: R1={R1:.4e} v_a={v_a:+.8f} v_b={v_b:+.8f}")
