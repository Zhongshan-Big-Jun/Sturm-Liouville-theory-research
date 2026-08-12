# -*- coding: utf-8 -*-
"""Systematic anti-symmetric plane search for n=2: initialize the full
band self-consistency system on a grid of anti-symmetric perturbations
(d1, d2, -d2, -d1) of the known symmetric solution and solve from each.
Purpose: hunt for non-symmetric interior band-consistent stationary points.
"""
import sys, json, time
import numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
import multiprocessing as mp

LOG = r'scripts/_gapn2_antigrid_log.txt'


def log(msg):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')
    print(msg, flush=True)


def one(job):
    n, R, mode, z0, label = job
    rc = Recon(n, R, mode)
    r = rc.solve(z0, max_nfev=200)
    if np.max(np.abs(r.fun)) >= 1e-8:
        return None
    rep = rc.full_report(r.x)
    rep['seed'] = label
    return rep


def run(mode, n, R, grid_n):
    rc = Recon(n, R, mode)
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    e0 = np.array(tab[f'n{n}_{mode.upper()}']['edges'])
    jobs = []
    grid = np.linspace(-0.18, 0.18, grid_n)
    for d1 in grid:
        for d2 in grid:
            e = e0 + np.array([d1, d2, -d2, -d1])
            if e[0] < 0.005 or e[3] > 0.995 or e[1] >= e[2] - 0.005:
                continue
            w = np.diff(np.concatenate([[0.0], e, [1.0]]))
            jobs.append((n, R, mode, rc.widths_to_z(w), f'({d1:.3f},{d2:.3f})'))
    t0 = time.time()
    with mp.Pool(processes=8) as pool:
        results = []
        for i, r in enumerate(pool.imap_unordered(one, jobs, chunksize=2)):
            results.append(r)
            if (i + 1) % 50 == 0:
                log(f'  [{mode}] {i + 1}/{len(jobs)} done ({time.time() - t0:.0f}s)')
    sols = [s for s in results if s is not None]
    kept = []
    for s in sols:
        e = np.array(s['edges'])
        if not any(np.max(np.abs(e - np.array(k['edges']))) < 1e-6 for k in kept):
            kept.append(s)
    log(f'=== n={n} R={R} mode={mode}: {len(jobs)} anti-grid starts -> '
        f'{len(sols)} roots, {len(kept)} distinct')
    for s in sorted(kept, key=lambda z: z['D']):
        log(f"  D={s['D']:.8f} asym={s['asym']:.2e} band={s['band_ok']} "
            f"band_min={s['band_min']:.1e} seed={s['seed']}")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'both'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    R = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    grid_n = int(sys.argv[4]) if len(sys.argv) > 4 else 17
    open(LOG, 'w', encoding='utf-8').write(f'anti-grid search start n={n} R={R}\n')
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        run(m, n, R, grid_n)
    log('ALL DONE')
