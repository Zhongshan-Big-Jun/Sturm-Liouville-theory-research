# -*- coding: utf-8 -*-
"""explore_8.py: full main-sheet branch for each R; a_max1, g1(a_max1), h endpoints."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

def R1r(a,b,R): return F.R1R2(a,b,R)[0]

def a_fp(R, lo=0.40, hi=0.5):
    r0 = R1r(lo,1.0-lo,R)
    for _ in range(60):
        m = 0.5*(lo+hi)
        if np.signbit(R1r(m,1.0-m,R)) == np.signbit(r0): lo = m
        else: hi = m
    return 0.5*(lo+hi)

def bisect(a, R, lo, hi, iters=20):
    flo = R1r(a, lo, R)
    if flo*R1r(a, hi, R) > 0: return None
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(R1r(a, md, R)) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def g1_at(a, R):
    """main-sheet g1(a) via bracketing search; returns b or None."""
    bs = np.linspace(a+1e-5, 1.0-1e-5, 150)
    vals = np.array([R1r(a,b,R) for b in bs])
    ch = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    for j in np.nonzero(ch)[0]:
        b = bisect(a, R, bs[j], bs[j+1], iters=45)
        if b is None: continue
        s1,s2 = F.roots2_fast(a,b,R)
        if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) > 0:
            return b
    return None

def trace_branch(R, a_start=None, da=1e-4, max_steps=4000):
    """Follow g1 from a_start by continuation; returns (a_list, g1_list) until failure."""
    if a_start is None: a_start = A0
    a = a_start
    b_prev = None
    out_a, out_g = [], []
    for step in range(max_steps):
        if b_prev is None:
            b = g1_at(a, R)
        else:
            b = bisect(a, R, max(a+1e-6, b_prev-0.05), min(1.0-1e-6, b_prev+0.05))
            if b is None:
                b = bisect(a, R, max(a+1e-6, b_prev-0.3), min(1.0-1e-6, b_prev+0.3))
        if b is None:
            break
        # main-sheet check
        s1,s2 = F.roots2_fast(a,b,R)
        if (np.sin(s2*a)/s2)/(np.sin(s1*a)/s1) <= 0:
            break
        out_a.append(a); out_g.append(b); b_prev = b
        a += da
    return np.array(out_a), np.array(out_g)

if __name__ == "__main__":
    out = {}
    for R in [1.02, 1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 100.0, 1000.0, 1e4]:
        t0 = time.time()
        fp = a_fp(R)
        aa, gg = trace_branch(R, da=2e-4 if R < 3 else 5e-4, max_steps=4000)
        # a_max1 = last a; g1(a_max1)
        if len(aa) == 0:
            print(f"R={R}: branch trace failed", flush=True); continue
        a_max1 = aa[-1]; g_max = gg[-1]
        beta = min(a_max1, B0)
        # g1^{-1}(b0)
        u_a0 = None
        if np.min(gg) <= B0 <= np.max(gg):
            u_a0 = np.interp(B0, gg, aa)
        h_a0 = u_a0 - B0 if u_a0 is not None else None
        # h(beta)
        if beta >= a_max1 - 1e-9:
            h_beta = 1.0 - (1.0 - np.interp(1.0-beta, gg[::-1], aa[::-1]) if (1.0-beta) <= np.max(gg) else None)
            # h(beta) = g1(beta) - g2(beta), g2(beta) = 1 - g1^{-1}(1-beta)
            u_beta = np.interp(1.0-beta, gg, aa) if (np.min(gg) <= 1.0-beta <= np.max(gg)) else None
            h_beta = (np.interp(beta, aa, gg) - (1.0 - u_beta)) if u_beta is not None else None
        else:
            u_beta = np.interp(1.0-beta, gg, aa) if (np.min(gg) <= 1.0-beta <= np.max(gg)) else None
            h_beta = (g_max - (1.0 - u_beta)) if u_beta is not None else None
        rec = {"fp": fp, "a_max1": a_max1, "g1(a_max1)": g_max, "beta": beta,
               "h(a0)": h_a0, "h(beta)": h_beta}
        out[f"R={R}"] = rec
        print(f"R={R:9g} fp={fp:.6f} a_max1={a_max1:.6f} g1(a_max1)={g_max:.6f} "
              f"beta={beta:.6f} h(a0)={h_a0 if h_a0 is None else f'{h_a0:+.3e}'} "
              f"h(beta)={h_beta if h_beta is None else f'{h_beta:+.3e}'} ({time.time()-t0:.0f}s)", flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_endpoints.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("saved")
