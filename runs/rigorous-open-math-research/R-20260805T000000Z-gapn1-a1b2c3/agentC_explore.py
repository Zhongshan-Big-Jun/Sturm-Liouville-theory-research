# -*- coding: utf-8 -*-
"""Agent C: vectorized 2-block D(t) exploration."""
import numpy as np
from scipy.optimize import brentq

def M01_matrix(ts, c1, c2, s):
    # shape (len(ts), len(s)): M01(s; t) for blocks (t,c1),(1-t,c2)
    T = ts[:, None]
    S = s[None, :]
    w1 = S*np.sqrt(c1); w2 = S*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    A = np.cos(w1*T); B = np.sin(w1*T)/q1; C = -q1*np.sin(w1*T); Dm = np.cos(w1*T)
    E = np.cos(w2*(1-T)); F = np.sin(w2*(1-T))/q2; G = -q2*np.sin(w2*(1-T)); H = np.cos(w2*(1-T))
    # M2 @ M1, take [0,1] entry = E*B + F*Dm
    return E*B + F*Dm

def lams_grid(ts, c1, c2, k=2, n_s=40000, smax=None):
    if smax is None:
        smax = np.pi*np.sqrt(max(c1, c2))*(k+2)+10
    s = np.linspace(1e-8, smax, n_s)
    M = M01_matrix(ts, c1, c2, s)          # (n_t, n_s)
    sg = np.signbit(M)                     # negative flag
    ch = sg[:, 1:] != sg[:, :-1]           # (n_t, n_s-1) sign changes
    roots = np.zeros((len(ts), k))
    ok = np.zeros(len(ts), dtype=bool)
    for i in range(len(ts)):
        idx = np.nonzero(ch[i])[0][:k]
        if len(idx) < k:
            continue
        for j in range(k):
            lo, hi = s[idx[j]], s[idx[j]+1]
            roots[i, j] = brentq(lambda x: M01_2block(ts[i], c1, c2, x), lo, hi)
        ok[i] = True
    return roots, ok

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    B = np.sin(w1*t)/q1; Dm = np.cos(w1*t)
    E = np.cos(w2*(1-t)); F = np.sin(w2*(1-t))/q2
    return E*B + F*Dm

if __name__ == '__main__':
    PI2 = np.pi**2
    for R in [1.5, 2.0, 4.0, 10.0]:
        print(f"==== R={R} ====  3pi^2/R={3*PI2/R:.10f}  3pi^2={3*PI2:.10f}")
        ts = np.linspace(1e-4, 1-1e-4, 2000)
        for hl in [False, True]:
            c1, c2 = (R, 1.0) if hl else (1.0, R)
            roots, ok = lams_grid(ts, c1, c2)
            assert ok.all()
            Ds = roots[:, 1]**2 - roots[:, 0]**2
            imax = np.argmax(Ds); imin = np.argmin(Ds)
            lo_bad = (Ds <= 3*PI2/R).sum(); hi_bad = (Ds >= 3*PI2).sum()
            print(f"  {'heavy_left ' if hl else 'heavy_right'}: max D={Ds[imax]:.10f} t={ts[imax]:.6f} | min D={Ds[imin]:.10f} t={ts[imin]:.6f} | viol_low={lo_bad} viol_high={hi_bad}")
