# -*- coding: utf-8 -*-
"""Reduced-system hunt for (G2) endpoint-limit configs.

The endpoint-limit config (first block width w1 -> 0 along a band-consistent
family) must satisfy: (i) the reduced self-consistency system with 2n-1
switches (pattern h2..h_{2n+1}), and (ii) the endpoint condition q0 = c,
q0 = |u_{n+1}'(0)/u_n'(0)|, c = sqrt(lam_n/lam_{n+1}).

This script solves (i) from random seeds and measures q0 - c on the solution
set.  If q0 - c != 0 at every reduced root, no endpoint-limit config exists
and the (G2) endpoint obstruction is closed (modulo interior coalescence).

Usage: python _gapn2_reduced_endpoint_hunt.py [n] [mode] [R]
"""
import sys, json
import numpy as np
import multiprocessing as mp
from scipy.optimize import least_squares
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_slope_ratio import eigfun_slope0


class Reduced:
    def __init__(self, n, R, mode, end='first'):
        self.n = n
        self.R = R
        self.end = end
        self.mode = mode
        rc = Recon(n, R, mode)
        pat0 = rc.pat
        self.pat0 = pat0
        if end == 'first':
            self.pat = pat0[1:]          # 2n blocks, 2n-1 switches
        elif end == 'last':
            self.pat = pat0[:-1]         # 2n blocks, 2n-1 switches
        elif end == 'both':
            self.pat = pat0[1:-1]        # 2n-1 blocks, 2n-2 switches
        else:
            raise ValueError(end)
        self.nb = len(self.pat)

    def z_to_widths(self, z):
        z = np.asarray(z, dtype=float)
        ez = np.exp(z - np.max(z))
        sm = ez / np.sum(ez)
        return (1.0 - self.nb * 1e-7) * sm + 1e-7

    def widths_to_z(self, widths):
        w = np.asarray(widths, dtype=float)
        w = np.clip(w, 2e-7, 1.0 - 2e-7)
        w = w / np.sum(w)
        return np.log(w - 1e-7)

    def blocks_from_z(self, z):
        w = self.z_to_widths(z)
        return [(float(w[i]), self.pat[i]) for i in range(self.nb)]

    def residual(self, z):
        blocks = self.blocks_from_z(z)
        ss = roots_of(blocks, self.n + 1)
        lam_n, lam_np1 = ss[self.n - 1] ** 2, ss[self.n] ** 2
        edges = np.cumsum(self.z_to_widths(z))[:-1]
        u_n = eigfun(blocks, ss[self.n - 1], edges)
        u_np1 = eigfun(blocks, ss[self.n], edges)
        return (lam_n * u_n ** 2 - lam_np1 * u_np1 ** 2) / lam_np1

    def report(self, z):
        blocks = self.blocks_from_z(z)
        w = self.z_to_widths(z)
        ss = roots_of(blocks, self.n + 1)
        lam_n, lam_np1 = ss[self.n - 1] ** 2, ss[self.n] ** 2
        # band matching: f = lam_n u_n^2 - lam_{n+1} u_{n+1}^2 at block midpoints
        mids = np.cumsum(w) - 0.5 * w
        u_n = eigfun(blocks, ss[self.n - 1], mids)
        u_np1 = eigfun(blocks, ss[self.n], mids)
        f_m = lam_n * u_n ** 2 - lam_np1 * u_np1 ** 2
        expect = []
        for h in self.pat:
            if self.mode == 'sup':
                expect.append(1.0 if h == self.R else -1.0)
            else:
                expect.append(1.0 if h == 1.0 else -1.0)
        expect = np.array(expect)
        band_ok = bool(np.all(np.sign(f_m) == expect) and
                       np.min(np.abs(f_m) / lam_np1) > 1e-6)
        # zero count of f on a fine grid (should be nb-1 for band-matched roots)
        grid = np.linspace(1e-9, 1 - 1e-9, 8000)
        gn = eigfun(blocks, ss[self.n - 1], grid)
        gp = eigfun(blocks, ss[self.n], grid)
        fg = lam_n * gn ** 2 - lam_np1 * gp ** 2
        nz = int(np.sum(np.signbit(fg[1:]) != np.signbit(fg[:-1])))
        s0n, s0p = eigfun_slope0(blocks, ss[self.n - 1]), eigfun_slope0(blocks, ss[self.n])
        q0 = np.sqrt(lam_np1) * abs(s0p) / (np.sqrt(lam_n) * abs(s0n))
        c = np.sqrt(lam_n / lam_np1)
        # slope at x=1 via 3-point backward difference on the exact eigenfunction
        h = min(1e-6, w[-1] * 0.05)
        out = {}
        for k, s in ((self.n - 1, ss[self.n - 1]), (self.n, ss[self.n])):
            a = eigfun(blocks, s, np.array([1.0 - h]))[0]
            b = eigfun(blocks, s, np.array([1.0 - 2.0 * h]))[0]
            out[k] = (b - 4.0 * a) / (2.0 * h)
        q1 = np.sqrt(lam_np1) * abs(out[self.n]) / (np.sqrt(lam_n) * abs(out[self.n - 1]))
        edges = np.cumsum(w)[:-1]
        d = dict(D=float(lam_np1 - lam_n), q0mc=float(q0 - c), q0c=float(q0 / c),
                 q1mc=float(q1 - c), q1c=float(q1 / c),
                 widths=w.tolist(), edges=edges.tolist(),
                 band_ok=band_ok, nz=nz)
        # margin relevant for the endpoint condition of this end
        if self.end == 'first':
            d['mc'] = d['q0mc']
        elif self.end == 'last':
            d['mc'] = d['q1mc']
        else:
            d['mc'] = min(d['q0mc'], d['q1mc'])
        return d


def one(job):
    n, R, mode, end, z0 = job
    rd = Reduced(n, R, mode, end)
    res = least_squares(rd.residual, z0, xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=150)
    if np.max(np.abs(res.fun)) < 1e-7:
        return rd.report(res.x)
    return None


def hunt(n, R, mode, end='first', seeds=8):
    rd = Reduced(n, R, mode, end)
    rng = np.random.default_rng(1000 * n + 10 * int(R) + (0 if mode == 'sup' else 1)
                                + (0 if end == 'first' else (2 if end == 'last' else 4)))
    jobs = []
    for t in range(seeds):
        w0 = rng.dirichlet(np.ones(rd.nb))
        jobs.append((n, R, mode, end, rd.widths_to_z(w0)))
    with mp.Pool(processes=8) as pool:
        results = pool.map(one, jobs, chunksize=1)
    sols = [r for r in results if r is not None]
    kept = []
    for r in sols:
        dup = any(np.max(np.abs(np.array(r['edges']) - np.array(k['edges']))) < 1e-4 for k in kept)
        if not dup:
            kept.append(r)
    return kept


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
    R = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
    end = sys.argv[4] if len(sys.argv) > 4 else 'first'
    seeds = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    modes = ['sup', 'inf'] if mode == 'both' else [mode]
    Rs = [2.0, 4.0, 10.0, 30.0] if R <= 0 else [R]
    for m in modes:
        for Rv in Rs:
            sols = hunt(n, Rv, m, end, seeds)
            if sols:
                qs = [s['mc'] for s in sols]
                bm = [s for s in sols if s['band_ok']]
                print(f"n={n} {m} R={Rv:5.1f} end={end}: {len(sols)} roots  "
                      f"mc in [{min(qs):+.3e}, {max(qs):+.3e}]; band-matched: {len(bm)}",
                      flush=True)
                if bm:
                    bqs = [s['mc'] for s in bm]
                    print(f"    band-matched mc in [{min(bqs):+.3e}, {max(bqs):+.3e}]",
                          flush=True)
                    for s in sorted(bm, key=lambda z: z['mc'])[:4]:
                        print(f"    D={s['D']:.6f} mc={s['mc']:+.3e} q0/c={s['q0c']:.5f} "
                              f"q1/c={s['q1c']:.5f} nz={s['nz']} minw={min(s['widths']):.5f}",
                              flush=True)
                else:
                    for s in sorted(sols, key=lambda z: z['mc'])[:2]:
                        print(f"    (unmatched) D={s['D']:.6f} mc={s['mc']:+.3e} "
                              f"q0/c={s['q0c']:.5f} nz={s['nz']} minw={min(s['widths']):.5f}",
                              flush=True)
            else:
                print(f"n={n} {m} R={Rv:5.1f} end={end}: none", flush=True)


if __name__ == "__main__":
    main()
