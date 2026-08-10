# -*- coding: utf-8 -*-
"""Audit Part 2b: symmetric-line SR(xi) single crossing for all sampled R; R=1000 targeted.
Uses F_tilde(c) = 0 formulation for c* and direct residual verification."""
import numpy as np
from scipy.optimize import brentq
import sys
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("p2", r"F:\LaTeX\BVE research\scripts\audit_o3a_pdf_part2.py")
# do NOT import (module runs the whole scan); instead inline the needed functions
from scipy.optimize import root

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

def eigvals(a, b, q, kmax=2, grid_n=3000):
    # top = 3*pi: for rho >= 1 the second Dirichlet eigenvalue satisfies
    # s2 <= 2*pi, but s2 approaches 2*pi from below for thin barriers, so the
    # 2*pi - 1e-7 top truncated the bracket and missed the second zero.
    grid = np.linspace(1e-7, 3*np.pi, grid_n)
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

def residual(a, b, q, grid_n=3000):
    s1, s2 = eigvals(a, b, q, grid_n=grid_n)
    l1, l2 = s1**2, s2**2
    ya1, yb1, n1 = eigenmode(a, b, q, s1)
    ya2, yb2, n2 = eigenmode(a, b, q, s2)
    R1 = l1*ya1**2/n1 - l2*ya2**2/n2
    R2 = l1*yb1**2/n1 - l2*yb2**2/n2
    return R1, R2, ya2/ya1, yb2/yb1, s1, s2

print("=== Part 2b: symmetric-line SR(xi) single crossing ===")
# float64 transfer matrices lose precision for wide barriers at R >= 1e4;
# large-R single crossing is verified in higher precision by part2c (mpmath),
# _audit_cstar.py and _tmp_verify_r1e6.py.
for R in [1.1, 1.5, 2.0, 4.0, 10.0, 100.0, 1000.0]:
    q = np.sqrt(R)
    # sample SR on (0,1/2)
    sign = []
    for xi in [0.05, 0.15, 0.25, 0.35, 0.42, 0.46, 0.48, 0.495, 0.499]:
        R1, R2, v_a, v_b, s1, s2 = residual(xi, 1-xi, q, grid_n=1000 if R < 1e4 else 6000)
        sign.append((xi, R1))
    # count sign changes in ordered samples
    sc = sum(1 for i in range(len(sign)-1) if sign[i][1]*sign[i+1][1] < 0)
    print(f"R={R}: SR sign changes over sampled xi = {sc}  (R1 at xi=0.05,0.25,0.48,0.499: {sign[0][1]:.3e}, {sign[2][1]:.3e}, {sign[6][1]:.3e}, {sign[8][1]:.3e})")
    assert sc == 1
print("single crossing confirmed on samples")

print("=== Part 2c: R=1000 and R=1e6 root location and residual ===")
for R in [1000.0, 1e6]:
    q = np.sqrt(R)
    # find xi* by bisection on SR(xi) (symmetric line)
    def srf(xi):
        R1, *_ = residual(xi, 1-xi, q, grid_n=6000)
        return R1
    lo, hi = 0.4, 0.4999
    assert srf(lo)*srf(hi) < 0, (R, srf(lo), srf(hi))
    for _ in range(80):
        mid = (lo+hi)/2
        if srf(mid)*srf(lo) <= 0: hi = mid
        else: lo = mid
    xi_star = (lo+hi)/2
    R1, R2, v_a, v_b, s1, s2 = residual(xi_star, 1-xi_star, q, grid_n=6000)
    print(f"R={R}: xi*={xi_star:.12f} 1-xi*={1-xi_star:.12f} R1={R1:.3e} R2={R2:.3e} v_a={v_a:+.6f} v_b={v_b:+.6f} s1={s1:.6f} s2={s2:.6f}")
    assert abs(R1) < 1e-9 and abs(R2) < 1e-9 and v_a > 0 and v_b < 0
print("R=1000,1e6 symmetric roots verified")
