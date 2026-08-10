# -*- coding: utf-8 -*-
"""Test: does rounding rho to the 3-block pattern determined by its own f increase D?
SUP-rounding: rho_t = R on {f>0}, 1 elsewhere. INF-rounding: reverse.
Also test single-interval structure and endpoint degeneracy for random smooth rho."""
import numpy as np
from scipy.linalg import eigh
from gap_lib import fd_check

R = 4.0

def gap_of(rho_fn, N=1201):
    lam, u, xs = fd_check(rho_fn, N)
    return lam[1]-lam[0], lam, u, xs

def f_of(rho_fn, N=1201):
    D, lam, u, xs = gap_of(rho_fn, N)[:4] if False else (None,)*4
    lam, u, xs = fd_check(rho_fn, N)[:3]
    lam1, lam2 = lam[0], lam[1]
    u1, u2 = u[0], u[1]
    return lam1*u1**2 - lam2*u2**2, lam1, lam2, u1, u2, xs

def pos_interval(f, xs, tol=1e-12):
    pos = f > tol
    nz = np.nonzero(pos)[0]
    if len(nz)==0: return (np.nan, np.nan, 0)
    # count components
    comps = 1 + np.sum(np.diff(nz) > 1)
    return (xs[nz[0]], xs[nz[-1]], comps)

rng = np.random.default_rng(7)
results = []
for trial in range(24):
    # random smooth-ish rho in [1,R]
    xx = np.linspace(0,1,400)
    base = 1.0 + (R-1.0)*(0.5 + 0.4*np.sin(np.pi*xx*(1+0.3*trial)) + 0.2*rng.random(len(xx))-0.1)
    base = np.clip(base, 1.0, R)
    rho = lambda x: np.interp(x, xx, base)
    f, lam1, lam2, u1, u2, xs = f_of(rho)
    a, b, comps = pos_interval(f, xs)
    D = lam2 - lam1
    # SUP rounding
    rho_sup = lambda x: np.where((x>a)&(x<b), R, 1.0) if comps==1 else None
    # INF rounding
    rho_inf = lambda x: np.where((x>a)&(x<b), 1.0, R) if comps==1 else None
    if comps != 1:
        results.append((trial, D, comps, np.nan, np.nan, np.nan))
        continue
    Ds = gap_of(rho_sup)[0]
    Di = gap_of(rho_inf)[0]
    results.append((trial, D, comps, Ds, Di, a, b))
print("trial  D(rho)  comps  D(SUP-round)  D(INF-round)  a  b  SUP>=D  INF<=D")
ok_sup = 0; ok_inf = 0; tot = 0
for r in results:
    trial, D, comps, Ds, Di = r[0], r[1], r[2], r[3], r[4]
    if comps==1:
        a,b = r[5], r[6]
        print(f"{trial:4d}  {D:9.4f}   {comps}    {Ds:9.4f}      {Di:9.4f}   {a:.3f} {b:.3f}  {Ds>=D-1e-8} {Di<=D+1e-8}")
        tot += 1
        ok_sup += Ds >= D - 1e-8
        ok_inf += Di <= D + 1e-8
    else:
        print(f"{trial:4d}  {D:9.4f}   {comps}    ---            ---")
print(f"single-interval: {tot}/{len(results)}; SUP-round improves: {ok_sup}/{tot}; INF-round improves: {ok_inf}/{tot}")
