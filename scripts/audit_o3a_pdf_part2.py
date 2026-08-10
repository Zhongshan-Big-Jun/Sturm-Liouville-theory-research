# -*- coding: utf-8 -*-
"""Audit Part 2 (v3, vectorized): direct verification of Theorem 1.2 for sampled R."""
import numpy as np
from scipy.optimize import root, brentq

def y1_grid(a, b, q, sgrid):
    # vectorized propagation of (y,y') for array of s
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

def eigvals(a, b, q, kmax=2, grid_n=200):
    grid = np.linspace(1e-6, 2*np.pi - 1e-6, grid_n)
    ys = y1_grid(a, b, q, grid)
    idx = np.where(np.diff(np.sign(ys)) != 0)[0]
    assert len(idx) >= kmax, (a, b, q, len(idx))
    res = []
    for i in range(kmax):
        s = brentq(lambda t: float(y1_grid(a, b, q, np.array([t]))[0]), grid[idx[i]], grid[idx[i]+1], xtol=1e-13, rtol=1e-13)
        res.append(s)
    return res

def eigenmode(a, b, q, s):
    om1 = s
    yA, dyA = np.sin(om1*a)/om1, np.cos(om1*a)
    om2 = s*q
    ya, dya = yA, dyA
    c, sn = np.cos(om2*(b-a)), np.sin(om2*(b-a))
    yb, dyb = ya*c + dya*sn/om2, -ya*om2*sn + dya*c
    om3 = s
    c, sn = np.cos(om3*(1-b)), np.sin(om3*(1-b))
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

def residual(a, b, q):
    s1, s2 = eigvals(a, b, q)
    l1, l2 = s1**2, s2**2
    ya1, yb1, n1 = eigenmode(a, b, q, s1)
    ya2, yb2, n2 = eigenmode(a, b, q, s2)
    R1 = l1*ya1**2/n1 - l2*ya2**2/n2
    R2 = l1*yb1**2/n1 - l2*yb2**2/n2
    return R1, R2, ya2/ya1, yb2/yb1, s1, s2, n1, n2

def residuals_pair(x, q):
    a, b = x
    R1, R2, *_ = residual(a, b, q)
    return np.array([R1, R2])

q = np.sqrt(10.0)
for a in [0.45, 0.46, 0.47, 0.48]:
    b = 1-a
    R1, R2, v_a, v_b, s1, s2, n1, n2 = residual(a, b, q)
    print(f"a={a:.4f} R1={R1:.6e} R2={R2:.6e} v_a={v_a:+.4f} v_b={v_b:+.4f} s1={s1:.6f} s2={s2:.6f}")

print("=== Part 2a (v3): interior sign-consistent good-root count ===")
rng = np.random.default_rng(42)
for R in [1.1, 1.5, 2.0, 4.0, 10.0, 100.0, 1000.0]:
    q = np.sqrt(R)
    sols = []
    starts = []
    for a in np.linspace(0.03, 0.47, 10):
        for b in np.linspace(a+0.03, 0.97, 10):
            starts.append((a, b))
    for _ in range(150):
        a = rng.uniform(0.01, 0.49); b = rng.uniform(a+0.01, 0.99)
        starts.append((a, b))
    seen = set()
    for st in starts:
        try:
            r = root(residuals_pair, np.array(st), args=(q,), method='hybr', options={'xtol': 1e-11})
            if not r.success: continue
            a, b = r.x
            if not (0.002 < a < b < 0.998): continue
            res = np.linalg.norm(r.fun)
            if res > 1e-6: continue
            R1, R2, v_a, v_b, s1, s2, n1, n2 = residual(a, b, q)
            if v_a > 0 and v_b < 0:
                key = (round(a, 7), round(b, 7))
                if key not in seen:
                    seen.add(key)
                    sols.append((a, b, res, v_a, v_b))
        except Exception:
            pass
    print(f"R={R}: interior sign-consistent roots = {len(sols)}")
    for a, b, res, v_a, v_b in sols:
        print(f"   a={a:.12f} b={b:.12f} a+b-1={a+b-1:.2e} res={res:.2e} v_a={v_a:+.4f} v_b={v_b:+.4f}")
