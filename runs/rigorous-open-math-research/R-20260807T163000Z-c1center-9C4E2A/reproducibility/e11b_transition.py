# -*- coding: utf-8 -*-
"""e11b_transition.py: chunked fine scan. Args: start stop step nstep outfile"""
import sys, json, time, os
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility")
import c1trace_lib as cl
import numpy as np

start, stop, step = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
nstep = int(sys.argv[4])
outfile = sys.argv[5]

def refine_zero(fun, lo, hi, iters=80):
    flo = fun(lo)
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(fun(md)) == np.signbit(flo):
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def analyze(R, nstep):
    cache = {}
    prof = cl.profile(R, nstep=nstep, cache=cache)
    if prof is None:
        return {"R": R, "failed": True}
    rows = prof["rows"]
    aa = np.array([r[0] for r in rows]); bb = np.array([r[1] for r in rows])
    g1p = np.array([r[2] for r in rows]); Phi = np.array([r[4] for r in rows])
    h = np.array([r[5] for r in rows]); hp = np.array([r[6] for r in rows])
    fp = prof["fp"]; beta = prof["beta"]
    hp_zero = []
    for i in range(1, len(hp)):
        if hp[i-1]*hp[i] < 0:
            z = refine_zero(lambda x: np.interp(x, aa, hp), aa[i-1], aa[i])
            hp_zero.append(float(z))
    h_zero = []
    for i in range(1, len(h)):
        if h[i-1]*h[i] < 0:
            z = refine_zero(lambda x: np.interp(x, aa, h), aa[i-1], aa[i])
            h_zero.append(float(z))
    maskL = aa < fp - 1e-9; maskR = aa > fp + 1e-9
    violL = int(np.sum(np.diff(Phi[maskL]) < -1e-9)) if maskL.sum() > 2 else 0
    violR = int(np.sum(np.diff(Phi[maskR]) > 1e-9)) if maskR.sum() > 2 else 0
    violg = int(np.sum(g1p < -1e-9))
    d = None; ds = None
    if abs(beta - cl.B0) < 1e-9:
        d = float(h[-1]); ds = d*np.sqrt(R)
    k = int(np.argmin(np.abs(aa - fp)))
    return dict(R=R, fp=fp, beta=beta, npts=len(rows),
                h_a0=float(h[0]), h_a0_sr=float(h[0])*np.sqrt(R),
                h_beta=float(h[-1]), delta=d, delta_sr=ds,
                min_hp=float(np.nanmin(hp)), max_hp=float(np.nanmax(hp)),
                hpz=len(hp_zero), hp_zero=hp_zero, hz=len(h_zero),
                h_fp=float(h[k]), Phi_fp=float(Phi[k]),
                viol_Phi_L=violL, viol_Phi_R=violR, viol_g1p=violg,
                g1p_min=float(g1p.min()))

Rs = list(np.arange(start, stop + 1e-9, step))
out = {}
t0 = time.time()
for R in Rs:
    try:
        rec = analyze(float(R), nstep)
        out[str(R)] = rec
        if rec.get("failed"):
            print(f"R={R}: FAILED", flush=True)
        else:
            print(f"R={R}: min_hp={rec['min_hp']:+.3e} hpz={rec['hpz']} hz={rec['hz']} "
                  f"h_a0={rec['h_a0']:+.3e} h_beta={rec['h_beta']:+.3e} violL={rec['viol_Phi_L']} violR={rec['viol_Phi_R']}", flush=True)
    except Exception as e:
        print(f"R={R}: EXC {type(e).__name__}: {e}", flush=True)
        out[str(R)] = {"R": R, "failed": True, "exc": str(e)}
    print(f"  t={time.time()-t0:.0f}s", flush=True)
with open(outfile, "w") as f:
    json.dump(out, f, indent=1)
print("saved", outfile, "elapsed", round(time.time()-t0,1))