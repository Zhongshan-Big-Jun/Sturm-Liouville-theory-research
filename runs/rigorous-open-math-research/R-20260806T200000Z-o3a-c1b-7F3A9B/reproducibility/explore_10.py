# -*- coding: utf-8 -*-
"""explore_10.py: robust main-sheet branch trace from the corner (a0,a0)."""
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

def bisect(a, R, lo, hi, iters=55):
    flo = R1r(a, lo, R)
    fhi = R1r(a, hi, R)
    if not (flo < 0 < fhi or flo > 0 > fhi): return None
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(R1r(a, md, R)) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def corner_slope(R, h=1e-6):
    r1b = R1r(A0, A0+h, R)/h
    r1a = R1r(A0-h, A0, R)/(-h)
    return -r1a/r1b

def trace_branch(R, max_steps=8000, report_every=500):
    fp = a_fp(R)
    slope = corner_slope(R)
    a = A0 + 1e-6
    b = A0 + slope*1e-6
    # verify and correct the first point
    b0 = bisect(a, R, A0, A0 + slope*2e-6 + 1e-4)
    if b0 is None:
        b0 = bisect(a, R, a+1e-8, min(1.0-1e-8, a+0.05))
    if b0 is None:
        return None, None, None
    b = b0
    out_a, out_g = [a], [b]
    da = 1e-5
    failures = 0
    while len(out_a) < max_steps:
        a_next = a + da
        # predictor
        slope_loc = (out_g[-1] - out_g[-2])/(out_a[-1]-out_a[-2]) if len(out_g) >= 2 else slope
        b_pred = b + slope_loc*da
        # corrector: bracket around predictor
        w = max(4*da, 0.02)
        b_next = bisect(a_next, R, max(a_next+1e-9, b_pred - w), min(1.0-1e-9, b_pred + w))
        if b_next is None:
            # try wider
            w2 = max(20*da, 0.1)
            b_next = bisect(a_next, R, max(a_next+1e-9, b_pred - w2), min(1.0-1e-9, b_pred + w2))
        if b_next is None:
            failures += 1
            if failures > 3:
                break
            da *= 0.5
            if da < 1e-8:
                break
            continue
        failures = 0
        # main-sheet check
        s1,s2 = F.roots2_fast(a_next,b_next,R)
        va = (np.sin(s2*a_next)/s2)/(np.sin(s1*a_next)/s1)
        if va <= 0:
            break
        out_a.append(a_next); out_g.append(b_next)
        # adapt step
        dg = abs(b_next - b)
        if dg > 0.03 and da > 1e-5:
            da = max(1e-5, da*0.5)
        elif dg < 0.004 and da < 0.002:
            da = min(0.002, da*1.5)
        b = b_next
        a = a_next
        if len(out_a) % report_every == 0:
            pass
    return np.array(out_a), np.array(out_g), fp

if __name__ == "__main__":
    out = {}
    for R in [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]:
        t0 = time.time()
        aa, gg, fp = trace_branch(R)
        if aa is None or len(aa) < 10:
            print(f"R={R}: trace failed", flush=True)
            continue
        a_max1 = aa[-1]; g_max = gg[-1]
        beta = min(a_max1, B0)
        u_a0 = None
        if np.min(gg) <= B0 <= np.max(gg):
            u_a0 = np.interp(B0, gg, aa)
        h_a0 = u_a0 - B0 if u_a0 is not None else None
        g_beta = np.interp(beta, aa, gg) if (np.min(aa) <= beta <= np.max(aa)) else None
        u_beta = np.interp(1.0-beta, gg, aa) if (np.min(gg) <= 1.0-beta <= np.max(gg)) else None
        h_beta = (g_beta - (1.0-u_beta)) if (g_beta is not None and u_beta is not None) else None
        # save full table
        out[f"R={R}"] = {"fp": fp, "a_max1": a_max1, "g1(a_max1)": g_max, "beta": beta,
                          "h(a0)": h_a0, "h(beta)": h_beta,
                          "agrid": aa.tolist(), "g1": gg.tolist()}
        print(f"R={R:7g} fp={fp:.6f} a_max1={a_max1:.6f} g1(a_max1)={g_max:.6f} beta={beta:.6f} "
              f"h(a0)={h_a0 if h_a0 is None else f'{h_a0:+.4e}'} "
              f"h(beta)={h_beta if h_beta is None else f'{h_beta:+.4e}'} "
              f"n={len(aa)} ({time.time()-t0:.0f}s)", flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_branch_full.json"), "w") as fh:
        json.dump(out, fh)
    print("saved data_branch_full.json")
