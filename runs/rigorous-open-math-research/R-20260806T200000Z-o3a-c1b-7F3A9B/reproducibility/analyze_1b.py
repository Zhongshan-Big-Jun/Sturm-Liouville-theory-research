# -*- coding: utf-8 -*-
"""analyze_1b.py: fixed formatting."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

def load():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_g1.json")) as fh:
        return json.load(fh)

def g1_interp(rec, a):
    ag = np.array(rec["agrid"]); g1 = np.array([np.nan if x is None else x for x in rec["g1"]])
    mask = ~np.isnan(g1)
    if a < ag[mask][0] or a > ag[mask][-1]: return None
    return np.interp(a, ag[mask], g1[mask])

def g1inv(rec, target):
    ag = np.array(rec["agrid"]); g1 = np.array([np.nan if x is None else x for x in rec["g1"]])
    mask = ~np.isnan(g1)
    if target < g1[mask][0] or target > g1[mask][-1]: return None
    return np.interp(target, g1[mask], ag[mask])

data = load()
for Rstr in [f"R={r}" for r in [1.05, 1.2, 2.0, 4.0, 10.0, 100.0, 1000.0, 1e4, 1e5, 1e6]]:
    rec = data[Rstr]; R = float(Rstr[2:]); fp = rec["fp"]
    ag = np.array(rec["agrid"])
    hvals = []
    for a in ag:
        g1 = g1_interp(rec, a)
        u = g1inv(rec, 1.0 - a)
        if g1 is None or u is None: continue
        hvals.append((a, g1 - (1.0 - u)))
    hvals = np.array(hvals)
    g1b0 = g1_interp(rec, B0)
    u_a0 = g1inv(rec, B0)
    h_a0 = (u_a0 - B0) if u_a0 is not None else None
    h_b0 = (g1b0 - B0) if g1b0 is not None else None
    g1fp = g1_interp(rec, fp); ufp = g1inv(rec, 1.0-fp)
    hfp = (g1fp - (1.0-ufp)) if (g1fp is not None and ufp is not None) else None
    crossings = []
    for i in range(len(hvals)-1):
        if hvals[i,1]*hvals[i+1,1] < 0:
            crossings.append(0.5*(hvals[i,0]+hvals[i+1,0]))
    hs = "None" if hfp is None else f"{hfp:+.2e}"
    print(f"R={R:9g} fp={fp:.6f} | h(a0)={h_a0 if h_a0 is None else f'{h_a0:+.3e}'} "
          f"h(b0)={h_b0 if h_b0 is None else f'{h_b0:+.3e}'} h(fp)={hs} "
          f"| crossings: {[round(c,4) for c in crossings]}")
    hp = np.diff(hvals[:,1])/np.diff(hvals[:,0])
    neg = np.count_nonzero(hp < 0)
    print(f"    h' < 0 at {neg}/{len(hp)} intervals; min h'={hp.min():.3e}")
