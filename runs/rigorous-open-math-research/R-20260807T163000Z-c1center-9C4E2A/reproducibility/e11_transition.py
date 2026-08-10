# -*- coding: utf-8 -*-
"""e11_transition.py: fine scan of the transition region and broad E1/U evidence.
For each R: profile on [a0, beta]; record h(a0), h(beta), delta=g1(b0)-b0, delta*sqrt(R),
min/max of hp, hp zeros (bisection-refined), h zeros, Phi monotonicity violations
on [a0,fp] and [fp,beta], g1p positivity.
Output: e11_transition.json in the run reproducibility dir.
"""
import sys, json, time
sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility")
import c1trace_lib as cl
import numpy as np

def refine_zero(fun, lo, hi, iters=80):
    flo = fun(lo)
    for _ in range(iters):
        md = 0.5*(lo+hi)
        if np.signbit(fun(md)) == np.signbit(flo):
            lo = md
        else:
            hi = md
    return 0.5*(lo+hi)

def analyze(R, nstep=400):
    cache = {}
    prof = cl.profile(R, nstep=nstep, cache=cache)
    if prof is None:
        return {"R": R, "failed": True}
    rows = prof["rows"]
    aa = np.array([r[0] for r in rows]); bb = np.array([r[1] for r in rows])
    g1p = np.array([r[2] for r in rows]); uu = np.array([r[3] for r in rows])
    Phi = np.array([r[4] for r in rows]); h = np.array([r[5] for r in rows])
    hp = np.array([r[6] for r in rows])
    fp = prof["fp"]; beta = prof["beta"]
    # hp zeros by bisection on each sign-change interval
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
    # Phi monotonicity violations
    maskL = aa < fp - 1e-9; maskR = aa > fp + 1e-9
    violL = int(np.sum(np.diff(Phi[maskL]) < -1e-9)) if maskL.sum() > 2 else 0
    violR = int(np.sum(np.diff(Phi[maskR]) > 1e-9)) if maskR.sum() > 2 else 0
    # g1p violations
    violg = int(np.sum(g1p < -1e-9))
    # delta = g1(b0) - b0 (when beta == b0); else use h at beta
    d = None; ds = None
    if abs(beta - cl.B0) < 1e-9:
        d = float(h[-1]); ds = d*np.sqrt(R)
    # h at a0
    h_a0 = float(h[0]); h_a0s = h_a0*np.sqrt(R)
    k = int(np.argmin(np.abs(aa - fp)))
    rec = dict(R=R, fp=fp, beta=beta, npts=len(rows),
               h_a0=h_a0, h_a0_sr=h_a0s,
               h_beta=float(h[-1]),
               delta=d, delta_sr=ds,
               min_hp=float(np.nanmin(hp)), max_hp=float(np.nanmax(hp)),
               hpz=len(hp_zero), hp_zero=hp_zero,
               hz=len(h_zero), h_zero=h_zero,
               h_fp=float(h[k]),
               Phi_fp=float(Phi[k]),
               viol_Phi_L=violL, viol_Phi_R=violR, viol_g1p=violg,
               g1p_min=float(g1p.min()))
    return rec

Rs = []
for r in np.arange(950, 1301, 5): Rs.append(float(r))
for r in [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 6.0, 10.0, 30.0, 100.0,
          200.0, 500.0, 700.0, 900.0, 1300.0, 1350.0, 1500.0, 2000.0, 3000.0,
          1e4, 3e4, 1e5, 3e5]: Rs.append(float(r))
Rs = sorted(set(round(x, 6) for x in Rs))
out = {}
t0 = time.time()
for R in Rs:
    try:
        rec = analyze(R)
        out[str(R)] = rec
        flag = ""
        if rec.get("failed"):
            print(f"R={R}: FAILED")
        else:
            print(f"R={R}: beta={rec['beta']:.6f} h_a0={rec['h_a0']:+.3e} h_beta={rec['h_beta']:+.3e} "
                  f"min_hp={rec['min_hp']:+.3e} hpz={rec['hpz']} hz={rec['hz']} "
                  f"violL={rec['viol_Phi_L']} violR={rec['viol_Phi_R']} delta_sr={rec['delta_sr']}")
    except Exception as e:
        print(f"R={R}: EXC {type(e).__name__}: {e}")
        out[str(R)] = {"R": R, "failed": True, "exc": str(e)}
    print(f"  elapsed {time.time()-t0:.0f}s")
json.dump(out, open(r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260807T163000Z-c1center-9C4E2A\reproducibility\e11_transition.json", "w"), indent=1)
print("saved. total", round(time.time()-t0,1), "s")