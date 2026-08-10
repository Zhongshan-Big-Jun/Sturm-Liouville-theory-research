# -*- coding: utf-8 -*-
"""Agent C: fast 2-block D(t) via chunked vectorized bracketing + brentq."""
import numpy as np
from scipy.optimize import brentq

def M01_2block(t, c1, c2, s):
    w1 = s*np.sqrt(c1); w2 = s*np.sqrt(c2)
    q1 = np.sqrt(c1); q2 = np.sqrt(c2)
    B = np.sin(w1*t)/q1; Dm = np.cos(w1*t)
    E = np.cos(w2*(1-t)); F = np.sin(w2*(1-t))/q2
    return E*B + F*Dm

def lams_grid_fast(ts, c1, c2, k=2, n_s=200000, chunk=500):
    smax = np.pi*np.sqrt(max(c1, c2))*(k+2)+10
    s = np.linspace(1e-9, smax, n_s)
    roots = np.zeros((len(ts), k))
    ok = np.zeros(len(ts), dtype=bool)
    for a in range(0, len(ts), chunk):
        tch = ts[a:a+chunk]
        T = tch[:, None]; S = s[None, :]
        w1 = S*np.sqrt(c1); w2 = S*np.sqrt(c2)
        B = np.sin(w1*T)/np.sqrt(c1)
        Dm = np.cos(w1*T)
        E = np.cos(w2*(1-T)); F = np.sin(w2*(1-T))/np.sqrt(c2)
        M = E*B + F*Dm
        sg = np.signbit(M)
        ch = sg[:, 1:] != sg[:, :-1]
        for i in range(len(tch)):
            idx = np.nonzero(ch[i])[0][:k]
            if len(idx) < k:
                continue
            for j in range(k):
                lo, hi = s[idx[j]], s[idx[j]+1]
                roots[a+i, j] = brentq(lambda x: M01_2block(tch[i], c1, c2, x), lo, hi)
            ok[a+i] = True
    return roots, ok

def D_all(ts, R, hl):
    c1, c2 = (R, 1.0) if hl else (1.0, R)
    roots, ok = lams_grid_fast(ts, c1, c2)
    assert ok.all()
    return roots[:, 1]**2 - roots[:, 0]**2

if __name__ == '__main__':
    print("=== monotonicity: sign changes of D(t+dt)-D(t) ===", flush=True)
    for R in [1.5, 2.0, 4.0, 10.0, 100.0]:
        for hl in [False, True]:
            for n in [3000, 20000]:
                ts = np.linspace(1e-6, 1-1e-6, n)
                Ds = D_all(ts, R, hl)
                dD = np.diff(Ds)
                sc = (np.signbit(dD[1:]) != np.signbit(dD[:-1])).sum()
                # also check global max/min vs endpoints
                print(f"  R={R:7.1f} {'HL' if hl else 'HR'} n={n}: sign changes of dD = {sc}", flush=True)

    print("=== large-R asymptotics: theta_j(c), eta(c)*(1+c)^2 vs 3pi^2 ===", flush=True)
    def theta_j(c, j):
        lo = np.pi/2 + (j-1)*np.pi + 1e-9
        hi = j*np.pi - 1e-9
        return brentq(lambda th: np.tan(th) + c*th, lo, hi)
    worst = (1e9, None)
    for c in np.logspace(-4, 2, 200):
        th1 = theta_j(c, 1); th2 = theta_j(c, 2)
        val = (th2**2 - th1**2)*(1+c)**2
        if val < worst[0]: worst = (val, c)
    print(f"  min of eta*(1+c)^2 over c in [1e-4,100]: {worst[0]:.12f} at c={worst[1]:.6f}  (3pi^2={3*np.pi**2:.12f})")
    for c in [1e-3, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 20.0]:
        t = c/(1+c)
        th1 = theta_j(c, 1); th2 = theta_j(c, 2)
        val = (th2**2 - th1**2)*(1+c)**2
        print(f"  c={c:8.4f}: eta*(1+c)^2={val:.10f} diff vs 3pi^2={val-3*np.pi**2:+.3e}")
