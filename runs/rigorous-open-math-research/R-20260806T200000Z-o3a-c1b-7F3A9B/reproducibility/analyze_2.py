# -*- coding: utf-8 -*-
"""analyze_2.py: h and h' profiles on I; E1 via g1(b0)-b0; R1(b0,·) shape."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast_lib as F

A0 = np.arccos(0.25)/np.pi
B0 = 1.0 - A0

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_branch_full.json")) as fh:
    data = json.load(fh)

def g1_interp(rec, a):
    aa = np.array(rec["agrid"]); gg = np.array(rec["g1"])
    if a < aa[0] or a > aa[-1]: return None
    return np.interp(a, aa, gg)

def g1inv(rec, target):
    aa = np.array(rec["agrid"]); gg = np.array(rec["g1"])
    if target < gg[0] or target > gg[-1]: return None
    return np.interp(target, gg, aa)

for Rstr, rec in data.items():
    R = float(Rstr[2:])
    fp = rec["fp"]; a_max1 = rec["a_max1"]; beta = rec["beta"]
    # g1(b0) directly
    g1b0 = None
    if B0 <= a_max1:
        g1b0 = g1_interp(rec, B0)
    # h(a0), h(b0)
    u_a0 = g1inv(rec, B0)
    h_a0 = u_a0 - B0 if u_a0 is not None else None
    h_b0 = g1b0 - B0 if g1b0 is not None else None
    # h profile on [a0, min(beta, ...)]
    amax_p = min(beta, 0.55)
    grid = np.linspace(rec["agrid"][0], amax_p, 60)
    hprof = []
    for a in grid:
        g1 = g1_interp(rec, a)
        u = g1inv(rec, 1.0-a)
        if g1 is None or u is None: continue
        hprof.append((a, g1 - (1.0-u)))
    hprof = np.array(hprof)
    # h' via g1' formula: h'(a) = g1'(a) - 1/g1'(u(a)); use finite diff of g1 table
    hp = np.diff(hprof[:,1])/np.diff(hprof[:,0])
    neg = np.count_nonzero(hp < 0)
    print(f"R={R:7g} beta={beta:.5f} h(a0)={h_a0 if h_a0 is None else f'{h_a0:+.4e}'} "
          f"g1(b0)-b0={h_b0 if h_b0 is None else f'{h_b0:+.4e}'} "
          f"h(beta,trunc)={hprof[-1,1]:+.4e} h'<0:{neg}/{len(hp)} min(h')={hp.min():.3e}")

# R1(b0, b) shape for selected R
print()
print("R1(b0, b) profile:")
for R in [2.0, 3.0, 4.0, 10.0, 100.0, 1000.0, 1e4]:
    vals = []
    for b in np.linspace(B0+1e-5, 0.999, 40):
        vals.append((b, F.R1R2(B0, b, R)[0]))
    vals = np.array(vals)
    # roots
    roots = []
    for i in range(len(vals)-1):
        if vals[i,1]*vals[i+1,1] < 0:
            roots.append(0.5*(vals[i,0]+vals[i+1,0]))
    print(f"  R={R:7g}: R1(b0,b0+)={vals[0,1]:+.3e} R1(b0,1-)= {vals[-1,1]:+.3e} roots at b ~ {[round(float(r),5) for r in roots]}")
