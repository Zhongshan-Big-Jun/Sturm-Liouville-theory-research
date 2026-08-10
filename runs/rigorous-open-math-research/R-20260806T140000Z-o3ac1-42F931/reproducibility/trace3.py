# -*- coding: utf-8 -*-
"""trace3.py: b-parametrized main-sheet tracing with bracketed root solves."""
import sys, numpy as np
from scipy.optimize import brentq
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T140000Z-o3ac1-42F931\reproducibility")
from c1_lib import residual, v_at

a0 = np.arccos(0.25) / np.pi
b0 = np.arccos(-0.25) / np.pi

def a1_of_b(b, R, window=0.35):
    """main-sheet root of R1(a, b) = 0 near a0."""
    lo, hi = max(a0 - window, 1e-9), min(a0 + window, b - 1e-9)
    f = lambda a: residual(a, b, R, at='a')
    if f(lo) * f(hi) > 0:
        return None
    return brentq(f, lo, hi, xtol=1e-14)

def a2_of_b(b, R, window=0.35):
    """main-sheet root of R2(a, b) = 0 (a < b), near the Gamma_2 sheet."""
    lo, hi = 1e-9, b - 1e-9
    f = lambda a: residual(a, b, R, at='b')
    # find all sign changes, pick the one consistent with continuation
    Na = 600
    aa = np.linspace(lo, hi, Na)
    ff = np.array([f(x) for x in aa])
    ch = np.signbit(ff[1:]) != np.signbit(ff[:-1])
    roots = []
    for i in np.nonzero(ch)[0]:
        l, h = aa[i], aa[i + 1]
        r = brentq(f, l, h, xtol=1e-14)
        roots.append(r)
    return roots

if __name__ == "__main__":
    for R in [1.05, 1.2, 4.0, 100.0, 1000.0, 1e4]:
        print(f"===== R = {R} =====")
        # Gamma_1: b from a0+eps to 1
        g1 = []
        for b in np.linspace(a0 + 1e-3, 1.0 - 1e-4, 300):
            a = a1_of_b(b, R)
            if a is None:
                continue
            try:
                vv = v_at(a, b, R, a + 1e-10)
            except Exception:
                break
            if vv <= 0:
                break
            g1.append((a, b))
        print(f"  Gamma_1: {len(g1)} pts; a in [{g1[0][0]:.6f},{g1[-1][0]:.6f}]; b in [{g1[0][1]:.6f},{g1[-1][1]:.6f}]")
        # Gamma_2: b from b0-eps down to where it stops
        g2 = []
        for b in np.linspace(b0 - 1e-3, 0.05, 300):
            roots = a2_of_b(b, R)
            if not roots:
                break
            # main sheet: nearest to previous a, or for the first, largest a
            cand = [r for r in roots if r < b - 1e-9]
            if not cand:
                break
            if g2:
                a = min(cand, key=lambda r: abs(r - g2[-1][0]))
            else:
                a = max(cand)
            try:
                vv = v_at(a, b, R, b - 1e-10)
            except Exception:
                break
            if vv >= 0:
                break
            g2.append((a, b))
        print(f"  Gamma_2: {len(g2)} pts; a in [{g2[-1][0]:.6f},{g2[0][0]:.6f}]; b in [{g2[-1][1]:.6f},{g2[0][1]:.6f}]")
        # h at common-range endpoints
        a_min = max(g1[0][0], g2[-1][0])
        a_max = min(g1[-1][0], g2[0][0])
        def interp_ab(pts, aa):
            xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
            return np.interp(aa, xs, ys)
        if a_min < a_max:
            b1L, b2L = interp_ab(g1, a_min), interp_ab(g2, a_min)
            b1R, b2R = interp_ab(g1, a_max), interp_ab(g2, a_max)
            print(f"  common [{a_min:.6f},{a_max:.6f}]: h(L)={b1L-b2L:+.6f} h(R)={b1R-b2R:+.6f}")
        print()
