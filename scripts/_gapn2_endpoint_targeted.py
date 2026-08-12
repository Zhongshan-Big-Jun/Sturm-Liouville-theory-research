# -*- coding: utf-8 -*-
"""Targeted endpoint-collapse search for (G2).

If the alternating band-consistent branch could collapse its first block
(w1 -> 0 at some R), the limit would be a band-matched root of the reduced
(2n-block) system satisfying q0 = c.  The natural seed is the branch itself:
drop block 1, renormalize the remaining widths to sum 1, and solve the reduced
system from that seed (plus small perturbations).  Report band matching and
q0 - c at each root found.

Usage: python _gapn2_endpoint_targeted.py [n]
"""
import sys
import json
import numpy as np
from scipy.optimize import least_squares
from _gapn2_reduced_endpoint_hunt import Reduced
from _gapn2_symmetry_recon import Recon


def branch_widths(n, R, mode):
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    rc = Recon(n, R, mode)
    res = rc.solve(rc.widths_to_z(w0), max_nfev=800)
    if np.max(np.abs(res.fun)) >= 1e-7:
        return None, rc
    rep = rc.full_report(res.x)
    if not rep['band_ok']:
        return None, rc
    return np.array(rep['widths']), rc


def targeted(n, R, mode):
    wf, rc = branch_widths(n, R, mode)
    if wf is None:
        print(f"n={n} {mode} R={R:5.1f}: branch seed unavailable", flush=True)
        return
    wred = wf[1:]
    wred = wred / wred.sum()
    rd = Reduced(n, R, mode, 'first')
    seeds = [wred]
    rng = np.random.default_rng(10 * n + int(R))
    for eps in (0.03,):
        for _ in range(2):
            p = wred * (1.0 + eps * rng.standard_normal(len(wred)))
            p = np.clip(p, 1e-4, None)
            seeds.append(p / p.sum())
    roots = []
    for s in seeds:
        z0 = rd.widths_to_z(s)
        res = least_squares(rd.residual, z0, xtol=1e-12, ftol=1e-12, gtol=1e-12,
                            max_nfev=120)
        if np.max(np.abs(res.fun)) < 1e-7:
            rep = rd.report(res.x)
            dup = any(np.max(np.abs(np.array(rep['edges']) -
                                   np.array(r['edges']))) < 1e-4 for r in roots)
            if not dup:
                roots.append(rep)
    if not roots:
        print(f"n={n} {mode} R={R:5.1f}: no reduced root from branch seed", flush=True)
        return
    bm = [r for r in roots if r['band_ok']]
    print(f"n={n} {mode} R={R:5.1f}: {len(roots)} roots, band-matched {len(bm)}",
          flush=True)
    for r in sorted(roots, key=lambda z: z['mc']):
        tag = "BM" if r['band_ok'] else "  "
        print(f"  [{tag}] D={r['D']:10.5f} q0-c={r['q0mc']:+.4e} q0/c={r['q0c']:.5f} "
              f"q1/c={r['q1c']:.5f} nz={r['nz']} minw={min(r['widths']):.5f}",
              flush=True)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    if len(sys.argv) > 2:
        Rs = [float(x) for x in sys.argv[2].split(',')]
    else:
        Rs = [1.5, 2.0, 4.0, 10.0, 30.0]
    for mode in ('sup', 'inf'):
        for R in Rs:
            targeted(n, R, mode)


if __name__ == "__main__":
    main()
