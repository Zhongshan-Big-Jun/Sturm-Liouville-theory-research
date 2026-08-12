# -*- coding: utf-8 -*-
"""Quick audit: block-energy identity K(0) = -2D, q0 > 1, q1 < -1.

Checks the STRICT predictions on (a) the full symmetric branch and
(b) reduced-system roots found from random seeds.
"""
import sys, json
import numpy as np
sys.path.insert(0, r"scripts")
from _gapn2_symmetry_recon import Recon, roots_of
from _gapn2_slope_ratio import eigfun_slope0
from _gapn2_reduced_endpoint_hunt import Reduced
from scipy.optimize import least_squares


def report(blocks, n):
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    s0n, s0p = eigfun_slope0(blocks, ss[n - 1]), eigfun_slope0(blocks, ss[n])
    q0 = s0p / s0n
    rb = [(L, h) for (L, h) in reversed(blocks)]
    s1n, s1p = eigfun_slope0(rb, ss[n - 1]), eigfun_slope0(rb, ss[n])
    q1 = ((-1.0) ** n * s1p) / ((-1.0) ** (n - 1) * s1n)
    return lam_n, lam_np1, q0, q1


def main():
    print("== full branch n=2 R=4 ==")
    for mode in ("sup", "inf"):
        rc = Recon(2, 4.0, mode)
        tab = json.load(open(r"scripts/op03_gap_table.json", encoding="utf-8"))
        e0 = np.array(tab["n2_" + mode.upper()]["edges"])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        res = rc.solve(rc.widths_to_z(w0))
        rep = rc.full_report(res.x)
        blocks = [(float(w), rc.pat[i]) for i, w in enumerate(rep["widths"])]
        lam_n, lam_np1, q0, q1 = report(blocks, 2)
        D = lam_np1 - lam_n
        s0n = eigfun_slope0(blocks, np.sqrt(lam_n))
        s0p = eigfun_slope0(blocks, np.sqrt(lam_np1))
        K0 = s0n ** 2 - s0p ** 2
        print(f"{mode}: band={rep['band_ok']} D={D:.6f} q0={q0:.6f} "
              f"q1={q1:.6f} K0+2D={K0 + 2 * D:.3e}")

    print("== reduced roots n=2 R=4 (random seeds) ==")
    for mode in ("sup", "inf"):
        rd = Reduced(2, 4.0, mode, "both")
        rng = np.random.default_rng(1000 * 2 + 40 + (0 if mode == "sup" else 1) + 4)
        found = 0
        for t in range(6):
            w0 = rng.dirichlet(np.ones(rd.nb))
            z0 = rd.widths_to_z(w0)
            res = least_squares(rd.residual, z0, xtol=1e-12, ftol=1e-12,
                                gtol=1e-12, max_nfev=150)
            if np.max(np.abs(res.fun)) < 1e-7:
                rep = rd.report(res.x)
                blocks = [(float(w), rd.pat[i]) for i, w in enumerate(rep["widths"])]
                lam_n, lam_np1, q0, q1 = report(blocks, 2)
                s0n = eigfun_slope0(blocks, np.sqrt(lam_n))
                s0p = eigfun_slope0(blocks, np.sqrt(lam_np1))
                K0 = s0n ** 2 - s0p ** 2
                D = lam_np1 - lam_n
                print(f"{mode} seed{t}: D={D:.6f} q0={q0:.6f} q1={q1:.6f} "
                      f"K0+2D={K0 + 2 * D:.3e} band={rep['band_ok']}")
                found += 1
        if not found:
            print(f"{mode}: no reduced roots found")


if __name__ == "__main__":
    main()
