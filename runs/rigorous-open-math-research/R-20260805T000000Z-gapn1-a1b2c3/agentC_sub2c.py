# -*- coding: utf-8 -*-
"""Agent C: subclaim 2 via half-problem. Robust scalar/array."""
import numpy as np
from scipy.optimize import brentq

def sec_DN_arr(u_arr, c1, c2, s_arr):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    U = np.atleast_1d(u_arr)[:, None]; S = np.atleast_1d(s_arr)[None, :]
    a = S*q1*U; b = S*q2*(0.5-U)
    out = np.cos(a)*np.cos(b)/q2 - np.sin(a)*np.sin(b)/q1
    return out[0,0] if (np.ndim(u_arr)==0 and np.ndim(s_arr)==0) else out

def sec_DD_arr(u_arr, c1, c2, s_arr):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    U = np.atleast_1d(u_arr)[:, None]; S = np.atleast_1d(s_arr)[None, :]
    a = S*q1*U; b = S*q2*(0.5-U)
    out = np.sin(a)*np.cos(b)/q1 + np.cos(a)*np.sin(b)/q2
    return out[0,0] if (np.ndim(u_arr)==0 and np.ndim(s_arr)==0) else out

def roots_half(u_arr, c1, c2):
    u_arr = np.atleast_1d(u_arr)
    n = len(u_arr)
    s0 = np.zeros(n); s1 = np.zeros(n)
    for lo, hi, fname, out in [(1e-9, np.pi+2, 'DN', s0), (1e-9, 2*np.pi+2, 'DD', s1)]:
        sg = np.linspace(lo, hi, 30000)
        f = sec_DN_arr(u_arr, c1, c2, sg) if fname=='DN' else sec_DD_arr(u_arr, c1, c2, sg)
        sg2 = np.signbit(f)
        ch = sg2[:,1:] != sg2[:,:-1]
        for i in range(n):
            idx = np.nonzero(ch[i])[0]
            if len(idx) == 0: continue
            j = idx[0]
            fn = (lambda x, ii=i: sec_DN_arr(u_arr[ii], c1, c2, x)) if fname=='DN' else (lambda x, ii=i: sec_DD_arr(u_arr[ii], c1, c2, x))
            out[i] = brentq(fn, sg[j], sg[j+1])
    return s0, s1

def half_norm(u, c1, c2, s):
    q1, q2 = np.sqrt(c1), np.sqrt(c2)
    nrm = 0.0
    w1 = q1*s; L1 = u
    B1 = 1.0/w1
    Iss = 0.5*(L1 - np.sin(2*w1*L1)/(2*w1))
    nrm += c1*B1*B1*Iss
    a = q1*s*u
    yt = np.sin(a)/(q1*s); ypt = np.cos(a)
    w2 = q2*s; L2 = 0.5-u
    A2, B2 = yt, ypt/w2
    Icc = 0.5*(L2 + np.sin(2*w2*L2)/(2*w2)); Iss = 0.5*(L2 - np.sin(2*w2*L2)/(2*w2)); Ics = np.sin(w2*L2)**2/(2*w2)
    nrm += c2*(A2*A2*Icc + B2*B2*Iss + 2*A2*B2*Ics)
    return nrm

def f_u(u, c1, c2):
    s0, s1 = roots_half(np.array([u]), c1, c2)
    s0, s1 = s0[0], s1[0]
    N0 = half_norm(u, c1, c2, s0); N1 = half_norm(u, c1, c2, s1)
    q1 = np.sqrt(c1)
    y0 = np.sin(q1*s0*u)/(q1*s0)
    y1 = np.sin(q1*s1*u)/(q1*s1)
    f = s0**2*y0**2/(2*N0) - s1**2*y1**2/(2*N1)
    return f, s0, s1

def ustar(R, sup, npts=300):
    c1, c2 = (1.0, R) if sup else (R, 1.0)
    uu = np.linspace(1e-5, 0.5-1e-5, npts)
    ff = np.array([f_u(u, c1, c2)[0] for u in uu])
    sg = np.signbit(ff)
    idx = np.nonzero(sg[1:] != sg[:-1])[0]
    zeros = [brentq(lambda u: f_u(u, c1, c2)[0], uu[i], uu[i+1]) for i in idx]
    return zeros, ff[0], ff[-1]

PI2 = np.pi**2
if __name__ == "__main__":
    print("R, SUP: zeros, u*, D, D-3pi^2 | INF: zeros, u*, D, 3pi^2/R-D")
    for R in [1.02, 1.05, 1.2, 1.5, 2.0, 4.0, 10.0, 100.0, 1e4, 1e6]:
        zs, f0, f1 = ustar(R, True)
        zt, g0, g1 = ustar(R, False)
        if len(zs)==0 or len(zt)==0:
            print(f"R={R}: SUP zeros={len(zs)} (f:{f0:.2e},{f1:.2e}) INF zeros={len(zt)} (f:{g0:.2e},{g1:.2e})")
            continue
        us = zs[0]; _, s0, s1 = f_u(us, 1.0, R)
        Dsup = s1**2 - s0**2
        ui = zt[0]; _, t0, t1 = f_u(ui, R, 1.0)
        Dinf = t1**2 - t0**2
        print(f"R={R:9.1f}: SUP z={len(zs)} u*={us:.7f} D={Dsup:.8f} D-3pi^2={Dsup-3*PI2:+.6e} | INF z={len(zt)} u*={ui:.7f} D={Dinf:.8f} D*R={Dinf*R:.8f} 3pi^2/R-D={3*PI2/R-Dinf:+.6e}")
