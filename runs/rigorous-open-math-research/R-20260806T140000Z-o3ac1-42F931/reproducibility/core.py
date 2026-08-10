# -*- coding: utf-8 -*-
"""core.py (v2): robust traces with v-sign + continuity checks."""
import numpy as np
from scipy.optimize import brentq
import c1_lib as L

def eig(a, b, R):
    return L.cfg(a, b, R)

def R1(a, b, R):
    return L.residual(a, b, R, at='a')

def R2(a, b, R):
    return L.residual(a, b, R, at='b')

def v_at(a, b, R, x):
    return L.v_at(a, b, R, x)

def fp(R, lo=0.40, hi=0.5):
    return L.a_fp(R, lo, hi)

def trace_g1(R, nb=600, bmax=1 - 1e-6, d0=1e-4):
    """fp-sheet of Gamma_1: b-continuation from (a0, a0); requires v(a) > 0."""
    a0 = np.arccos(0.25) / np.pi
    pts = []
    b = a0 + d0
    # initial: solve R1(a, b) = 0 near a0
    lo, hi = max(a0 - 0.02, 1e-9), min(a0 + 0.02, b - 1e-9)
    f = lambda x: R1(x, b, R)
    if f(lo) * f(hi) > 0:
        return pts
    a = brentq(f, lo, hi, xtol=1e-14)
    if v_at(a, b, R, a + 1e-9) <= 0:
        return pts
    pts.append((a, b))
    for i in range(nb - 1):
        bn = b + (bmax - b) / (nb - i - 1)
        if bn - b < 1e-10:
            break
        found = None
        for w in [0.04, 0.12, 0.3, 0.6]:
            lo = max(a - w, 1e-9); hi = min(a + w, bn - 1e-9)
            f = lambda x: R1(x, bn, R)
            # scan the bracket for a root with v(a) > 0 and continuity
            xs = np.linspace(lo, hi, 9)
            ys = np.array([f(x) for x in xs])
            ch = np.signbit(ys[1:]) != np.signbit(ys[:-1])
            for j in np.nonzero(ch)[0]:
                cand = brentq(f, xs[j], xs[j + 1], xtol=1e-14)
                if abs(cand - a) > w * 1.5:
                    continue
                try:
                    vv = v_at(cand, bn, R, cand + 1e-9)
                except Exception:
                    continue
                if vv > 0:
                    found = cand
                    break
            if found is not None:
                break
        if found is None:
            break
        pts.append((found, bn))
        a, b = found, bn
    return pts

def trace_g2(R, na=600, amin=1e-3, d0=1e-4):
    """fp-sheet of Gamma_2: a-continuation from (b0, b0); requires v(b) < 0."""
    b0 = np.arccos(-0.25) / np.pi
    pts = []
    a = b0 - d0
    # initial: solve R2(a, b) = 0 for b near b0
    lo, hi = a + 1e-9, min(b0 + 0.02, 1 - 1e-9)
    f = lambda y: R2(a, y, R)
    if f(lo) * f(hi) > 0:
        return pts
    b = brentq(f, lo, hi, xtol=1e-14)
    if v_at(a, b, R, b - 1e-9) >= 0:
        return pts
    pts.append((a, b))
    for i in range(na - 1):
        an = a - (a - amin) / (na - i - 1)
        if a - an < 1e-10:
            break
        found = None
        for w in [0.04, 0.12, 0.3, 0.6]:
            lo = max(b - w, an + 1e-9); hi = min(b + w, 1 - 1e-9)
            f = lambda y: R2(an, y, R)
            xs = np.linspace(lo, hi, 9)
            ys = np.array([f(x) for x in xs])
            ch = np.signbit(ys[1:]) != np.signbit(ys[:-1])
            for j in np.nonzero(ch)[0]:
                cand = brentq(f, xs[j], xs[j + 1], xtol=1e-14)
                if abs(cand - b) > w * 1.5:
                    continue
                try:
                    vv = v_at(an, cand, R, cand - 1e-9)
                except Exception:
                    continue
                if vv < 0:
                    found = cand
                    break
            if found is not None:
                break
        if found is None:
            break
        pts.append((an, found))
        a, b = an, found
    return pts

class Branches:
    def __init__(self, R, g1=None, g2=None):
        self.R = R
        self.g1 = g1 if g1 is not None else trace_g1(R)
        self.g2 = g2 if g2 is not None else trace_g2(R)
        self.a1 = np.array([p[0] for p in self.g1]); self.b1 = np.array([p[1] for p in self.g1])
        self.a2 = np.array([p[0] for p in self.g2]); self.b2 = np.array([p[1] for p in self.g2])
        o1 = np.argsort(self.a1); o2 = np.argsort(self.a2)
        self.a1, self.b1 = self.a1[o1], self.b1[o1]
        self.a2, self.b2 = self.a2[o2], self.b2[o2]
        self.a_max1 = self.a1[-1]
        self.b_min2 = self.a2[0]
        a0 = np.arccos(0.25) / np.pi; b0 = np.arccos(-0.25) / np.pi
        self.beta = min(self.a_max1, b0)
        self.a0 = a0; self.b0 = b0

    def g1_of(self, a):
        return np.interp(a, self.a1, self.b1)

    def g2_of(self, a):
        return np.interp(a, self.a2, self.b2)

    def h(self, a):
        return self.g1_of(a) - self.g2_of(a)

    def hp(self, a, h=1e-5):
        return (self.g1_of(a + h) - self.g1_of(a - h) - self.g2_of(a + h) + self.g2_of(a - h)) / (2 * h)

if __name__ == "__main__":
    import time
    for R in [1.02, 4.0, 100.0, 1000.0, 1500.0, 1e4]:
        t0 = time.time()
        B = Branches(R)
        print(f"R={R}: I=[{B.a0:.5f},{B.beta:.5f}] a_max1={B.a_max1:.5f} b_min2={B.b_min2:.5f} "
              f"h(a0)={B.h(B.a0):+.5f} h(beta)={B.h(B.beta):+.5f} g2(a0)={B.g2_of(B.a0):.5f}  ({time.time()-t0:.1f}s)")
