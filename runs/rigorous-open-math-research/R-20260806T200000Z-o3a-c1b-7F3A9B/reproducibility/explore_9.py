# -*- coding: utf-8 -*-
"""explore_9.py: main-sheet branch trace from a0+eps with adaptive stepping."""
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

def bisect(a, R, lo, hi, iters=50):
    flo = R1r(a, lo, R)
    if flo*R1r(a, hi, R) > 0: return None
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(R1r(a, md, R)) == np.signbit(flo): lo = md
        else: hi = md
    return 0.5*(lo+hi)

def find_root_near(a, R, b_hint):
    """Find R1=0 root near b_hint (closest sign change to b_hint)."""
    lo = max(a+1e-6, b_hint-0.02); hi = min(1.0-1e-6, b_hint+0.02)
    b = bisect(a, R, lo, hi)
    if b is not None: return b
    # widen
    for w in (0.05, 0.15, 0.4):
        b = bisect(a, R, max(a+1e-6, b_hint-w), min(1.0-1e-6, b_hint+w))
        if b is not None: return b
    return None

def trace_branch(R, a0_eps=2e-4, da0=5e-5, da=5e-4, max_steps=3000):
    fp = a_fp(R)
    a = A0 + a0_eps
    # initial root: scan b from a to a+0.05
    b = None
    for hi_off in (0.02, 0.05, 0.1):
        b = bisect(a, R, a+1e-6, min(1.0-1e-6, a+hi_off))
        if b is not None: break
    if b is None:
        return None, None
    out_a, out_g = [a], [b]
    step = da0
    while a < 0.5 - 1e-6 and len(out_a) < max_steps:
        a_next = a + step
        b_next = find_root_near(a_next, R, b)
        if b_next is None:
            # step too large; halve
            step *= 0.5
            if step < 1e-7: break
            continue
        # main-sheet sanity: v(a)>0
        s1,s2 = F.roots2_fast(a_next,b_next,R)
        va = (np.sin(s2*a_next)/s2)/(np.sin(s1*a_next)/s1)
        if va <= 0:
            step *= 0.5
            if step < 1e-7: break
            continue
        out_a.append(a_next); out_g.append(b_next)
        # adapt step: if |dg| large, reduce
        if abs(b_next - b) > 0.02 and step > da0:
            step = max(da0, step*0.5)
        elif abs(b_next - b) < 0.003 and step < da:
            step = min(da, step*2.0)
        b = b_next
        a = a_next
    return np.array(out_a), np.array(out_g)

if __name__ == "__main__":
    out = {}
    for R in [1.02, 1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 10.0, 100.0, 1000.0, 1e4]:
        t0 = time.time()
        fp = a_fp(R)
        aa, gg = trace_branch(R)
        if aa is None or len(aa) < 3:
            print(f"R={R}: trace failed", flush=True); continue
        a_max1 = aa[-1]; g_max = gg[-1]
        beta = min(a_max1, B0)
        # does the trace reach the fp?
        reached_fp = np.any(np.abs(aa - fp) < 1e-3)
        # h(a0) via g1^{-1}(b0)
        u_a0 = None
        if np.min(gg) <= B0 <= np.max(gg):
            u_a0 = np.interp(B0, gg, aa)
        h_a0 = u_a0 - B0 if u_a0 is not None else None
        # h(beta)
        g_beta = np.interp(beta, aa, gg)
        u_beta = np.interp(1.0-beta, gg, aa) if (np.min(gg) <= 1.0-beta <= np.max(gg)) else None
        h_beta = (g_beta - (1.0-u_beta)) if u_beta is not None else None
        rec = {"fp": fp, "a_max1": a_max1, "g1(a_max1)": g_max, "beta": beta,
               "h(a0)": h_a0, "h(beta)": h_beta, "reached_fp": bool(reached_fp),
               "g1(fp)": float(np.interp(fp, aa, gg)) if (np.min(aa)<=fp<=np.max(aa)) else None}
        out[f"R={R}"] = rec
        print(f"R={R:9g} fp={fp:.6f} a_max1={a_max1:.6f} g1(a_max1)={g_max:.6f} beta={beta:.6f} "
              f"reached_fp={reached_fp} h(a0)={h_a0 if h_a0 is None else f'{h_a0:+.3e}'} "
              f"h(beta)={h_beta if h_beta is None else f'{h_beta:+.3e}'} ({time.time()-t0:.0f}s)", flush=True)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_endpoints.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("saved data_endpoints.json")
