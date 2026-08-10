# -*- coding: utf-8 -*-
"""analyze_e15.py: structural analysis of G, Phi, h, hp from e15_authoritative.json."""
import json, numpy as np
p = r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility\e15_authoritative.json"
d = json.load(open(p, encoding="utf-8"))
for Rkey in ["R=1.02","R=4","R=20","R=100","R=500","R=888","R=1000","R=1500","R=10000","R=100000","R=1e+06"]:
    o = d[Rkey]
    rows = [r for r in o["rows"] if np.isfinite(r[5]) and r[4] is not None and np.isfinite(r[4])]
    if not rows: print(Rkey, "none"); continue
    a = np.array([r[0] for r in rows]); b = np.array([r[1] for r in rows])
    G = np.array([r[2] for r in rows]); u = np.array([r[3] for r in rows])
    Phi = np.array([r[4] for r in rows]); h = np.array([r[5] for r in rows]); hp = np.array([r[6] for r in rows])
    fp = o["fp"]
    # Phi-1 sign pattern
    s = np.sign(Phi-1)
    chg = np.nonzero(np.diff(s)!=0)[0]
    # h' sign pattern
    sh = np.sign(hp)
    chgh = np.nonzero(np.diff(sh)!=0)[0]
    # G monotonic pieces relative to fp
    iL = a <= fp; iR = a >= fp
    GL = G[iL]; GR = G[iR]; aL = a[iL]; aR = a[iR]
    dGL = np.diff(GL); dGR = np.diff(GR)
    print("=== %s  fp=%.6f" % (Rkey, fp))
    print("  Phi-1: nz_chg=%d at a=%s ; signs: %s" % (len(chg), np.array2string(a[chg], precision=4), "".join('+' if x>0 else '-' for x in np.sign(Phi[::max(1,len(Phi)//12)]))))
    print("  hp:   nz_chg=%d at a=%s" % (len(chgh), np.array2string(a[chgh], precision=4)))
    print("  G at fp=%.6f ; G left of fp: inc=%d dec=%d ; right: inc=%d dec=%d" % (
        G[np.argmin(np.abs(a-fp))], int((dGL>0).sum()), int((dGL<0).sum()), int((dGR>0).sum()), int((dGR<0).sum())))
    print("  h: min=%.5f max=%.5f h(a0)=%.5f h(beta)=%.5f ; a0-side G=%.5f beta-side G=%.5f" % (
        h.min(), h.max(), h[0], h[-1], G[0], G[-1]))
