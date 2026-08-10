# -*- coding: utf-8 -*-
"""trace.py: continuation tracer for the main sheets of Gamma_1, Gamma_2.

Gamma_1 main sheet: passes through (a0, a0); Gamma_2 main sheet: passes
through (b0, b0).  Continuation in the a-variable with a local Newton solve
of R1(a,b)=0 (resp. R2(a,b)=0) seeded from the previous step, plus a check
that the root is on the main sheet (v-sign: v(a) > 0 for Gamma_1, v(b) < 0
for Gamma_2; and b near the previous step).
"""
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import residual, roots2, y_at

def v(a, b, R, x):
    s1, s2 = roots2(a, b, R)
    return y_at(s2, a, b, R, x) / y_at(s1, a, b, R, x)

def trace_g1(R, amin, amax, n=400, tol=1e-12):
    """Trace Gamma_1 main sheet from a=amin (near a0)."""
    a0 = np.arccos(0.25) / np.pi
    bprev = a0
    pts = []
    for a in np.linspace(amin, amax, n):
        # Newton on R1(a, b) = 0 starting from bprev
        b = bprev
        for it in range(60):
            r = residual(a, b, R, at='a')
            # secant derivative
            h = 1e-7
            rp = residual(a, b + h, R, at='a')
            dr = (rp - r) / h
            if abs(dr) < 1e-14:
                break
            step = r / dr
            b = b - step
            if b <= a or b >= 1:
                break
            if abs(step) < tol:
                break
        if not (a < b < 1):
            break
        try:
            va = v(a, b, R, a + 1e-12)
        except Exception:
            break
        if not (va > 0):
            break
        # consistency: b should be near bprev (main sheet)
        if abs(b - bprev) > 0.05:
            break
        pts.append((a, b, residual(a, b, R, at='a')))
        bprev = b
    return pts

def trace_g2(R, amin, amax, n=400, tol=1e-12):
    """Trace Gamma_2 main sheet from a=amax (near b0)."""
    b0 = np.arccos(-0.25) / np.pi
    bprev = b0
    pts = []
    for a in np.linspace(amax, amin, n):
        b = bprev
        for it in range(60):
            r = residual(a, b, R, at='b')
            h = 1e-7
            rp = residual(a, b + h, R, at='b')
            dr = (rp - r) / h
            if abs(dr) < 1e-14:
                break
            step = r / dr
            b = b - step
            if b <= a or b >= 1:
                break
            if abs(step) < tol:
                break
        if not (a < b < 1):
            break
        try:
            vb = v(a, b, R, b - 1e-12)
        except Exception:
            break
        if not (vb < 0):
            break
        if abs(b - bprev) > 0.05:
            break
        pts.append((a, b, residual(a, b, R, at='b')))
        bprev = b
    return pts

if __name__ == "__main__":
    a0 = np.arccos(0.25) / np.pi
    b0 = np.arccos(-0.25) / np.pi
    for R in [1.05, 4.0, 100.0, 1000.0, 1500.0, 1e4]:
        print(f"===== R = {R} =====")
        g1 = trace_g1(R, a0 + 2e-3, 0.95, n=200)
        g2 = trace_g2(R, b0 - 2e-3, 0.42, n=200)
        print(f"  Gamma_1: {len(g1)} pts, a in [{g1[0][0]:.6f}, {g1[-1][0]:.6f}], b in [{min(p[1] for p in g1):.6f}, {max(p[1] for p in g1):.6f}]")
        print(f"  Gamma_2: {len(g2)} pts, a in [{g2[-1][0]:.6f}, {g2[0][0]:.6f}], b in [{min(p[1] for p in g2):.6f}, {max(p[1] for p in g2):.6f}]")
        # at a0 + eps
        a = a0 + 1e-3
        b1 = min((p[1] for p in g1 if abs(p[0]-a) < 0.01), default=None)
        b2 = min((p[1] for p in g2 if abs(p[0]-a) < 0.01), default=None)
        print(f"  at a={a:.4f}: g1 ~ {b1:.6f}, g2 ~ {b2:.6f}, h ~ {(b1-b2) if b1 and b2 else None:.6f}")
