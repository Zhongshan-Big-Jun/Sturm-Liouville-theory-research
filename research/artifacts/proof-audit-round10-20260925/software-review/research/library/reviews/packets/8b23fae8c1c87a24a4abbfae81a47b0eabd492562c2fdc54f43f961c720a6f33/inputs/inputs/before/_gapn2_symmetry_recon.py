# -*- coding: utf-8 -*-
"""Reconnaissance: are all self-consistent stationary points of D_n = lambda_{n+1}-lambda_n
(within the (2n+1)-block bang-bang family, 1<=rho<=R, Dirichlet) reflection-symmetric?

Method: solve the band self-consistency system f(x_j) = 0, j=1..2n, where
f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2, from many random seeds AND from
anti-symmetric perturbations of the known symmetric solution.  For every root we
report: D, asymmetry max_j |x_j + x_{2n+1-j} - 1|, band-matching.

Usage:  python _gapn2_symmetry_recon.py [n] [R] [seeds] [mode] [workers]
mode in {both, sup, inf}
"""
import sys, json, time
import numpy as np
from scipy.optimize import least_squares

# ----------------------------------------------------------------------------
# spectral engine (transfer matrix, Dirichlet)
# ----------------------------------------------------------------------------
def roots_of(blocks, k, npts=20000, refine=60):
    """First k positive roots s of M01(s) = 0 (sqrt of eigenvalues)."""
    smax = np.pi * np.sqrt(max(c for _, c in blocks)) * (k + 2) + 20.0
    s = np.linspace(1e-9, smax, npts)
    # adaptive grid: fixed 20000 points misses low clusters (near-degenerate pairs)
    # when smax grows with k (spacing ~ smax/npts >= root gap).  Use spacing
    # <= 0.02 so clusters like the INF R=10 pair (gap 0.42 at s~3.3) are resolved.
    npts = max(npts, int(np.ceil(smax / 0.02)))
    s = np.linspace(1e-9, smax, npts)
    M00 = np.ones(npts); M01 = np.zeros(npts); M10 = np.zeros(npts); M11 = np.ones(npts)
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
    d = M01
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = s[i], s[i + 1]
        for _ in range(refine):
            mid = 0.5 * (lo + hi)
            if D_scalar(blocks, lo) * D_scalar(blocks, mid) <= 0:
                hi = mid
            else:
                lo = mid
        out.append(0.5 * (lo + hi))
    return np.array(out)


def D_scalar(blocks, s):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
    return M01


def eigfun(blocks, s, pts):
    """Normalized eigenfunction values at pts (L^2(rho) normalization)."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    starts = []
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    starts.append((0.0, M00, M01, M10, M11))
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
        starts.append((xs[len(starts)], M00, M01, M10, M11))
    norm = 0.0
    for bi, (L, c) in enumerate(blocks):
        _, M00, M01, M10, M11 = starts[bi]
        w = s * np.sqrt(c)
        A = M01; B = M11 / w
        Icos = 0.5 * (L + np.sin(2 * w * L) / (2 * w))
        Isin = 0.5 * (L - np.sin(2 * w * L) / (2 * w))
        Icross = np.sin(w * L) ** 2 / (2 * w)
        norm += c * (A * A * Icos + B * B * Isin + 2 * A * B * Icross)
    out = np.zeros(len(pts))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs) - 1) if xs[i] <= p)
        _, M00, M01, M10, M11 = starts[bi]
        L, c = blocks[bi]
        w = s * np.sqrt(c); d = p - xs[bi]
        out[j] = M01 * np.cos(w * d) + (M11 / w) * np.sin(w * d)
    return out / np.sqrt(norm)


class Recon:
    def __init__(self, n, R, mode):
        self.n = n
        self.R = R
        self.mode = mode  # 'sup' or 'inf'
        self.start_val = 1.0 if mode == 'sup' else R
        self.alt_val = R if mode == 'sup' else 1.0
        self.nb = 2 * n + 1
        self.pat = [self.start_val if i % 2 == 0 else self.alt_val for i in range(self.nb)]

    def z_to_widths(self, z):
        """softmax parameterization: strictly feasible widths, sum = 1."""
        z = np.asarray(z, dtype=float)
        ez = np.exp(z - np.max(z))
        sm = ez / np.sum(ez)
        return (1.0 - self.nb * 1e-7) * sm + 1e-7

    def widths_to_z(self, widths):
        """inverse softmax (up to shift): z_i = log(width_i - 1e-7)."""
        w = np.asarray(widths, dtype=float)
        w = np.clip(w, 2e-7, 1.0 - 2e-7)
        w = w / np.sum(w)
        return np.log(w - 1e-7)

    def blocks_from_z(self, z):
        w = self.z_to_widths(z)
        return [(float(w[i]), self.pat[i]) for i in range(self.nb)]

    def f_at(self, z, pts):
        """f = lam_n u_n^2 - lam_{n+1} u_{n+1}^2 at pts (normalized)."""
        blocks = self.blocks_from_z(z)
        ss = roots_of(blocks, self.n + 1)
        lam_n = ss[self.n - 1] ** 2
        lam_np1 = ss[self.n] ** 2
        u_n = eigfun(blocks, ss[self.n - 1], pts)
        u_np1 = eigfun(blocks, ss[self.n], pts)
        return lam_n * u_n ** 2 - lam_np1 * u_np1 ** 2, lam_n, lam_np1

    def residual(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]  # 2n interior switch points
        f, lam_n, lam_np1 = self.f_at(z, edges)
        return f / lam_np1

    def full_report(self, z):
        z = np.asarray(z, dtype=float)
        w = self.z_to_widths(z)
        edges = np.cumsum(w)[:-1]
        mids = np.cumsum(w) - 0.5 * w  # block midpoints
        f_e, lam_n, lam_np1 = self.f_at(z, edges)
        f_m, _, _ = self.f_at(z, mids)
        D = lam_np1 - lam_n
        n = self.n
        asym = max(abs(edges[j] + edges[2 * n - 1 - j] - 1.0) for j in range(2 * n))
        # band matching (delta D = int delta-rho f dx, numerically verified):
        #   SUP: f>0 on rho=R blocks, f<0 on rho=1 blocks;
        #   INF: f>0 on rho=1 blocks, f<0 on rho=R blocks
        expect = []
        for i in range(self.nb):
            if self.mode == 'sup':
                expect.append(1.0 if self.pat[i] == self.R else -1.0)
            else:
                expect.append(1.0 if self.pat[i] == 1.0 else -1.0)
        expect = np.array(expect)
        band_min = float(np.min(np.abs(f_m) / lam_np1))
        band_ok = bool(np.all(np.sign(f_m) == expect) and band_min > 1e-6)
        return dict(edges=edges.tolist(), widths=w.tolist(), D=float(D),
                    lam_n=float(lam_n), lam_np1=float(lam_np1),
                    asym=float(asym), band_ok=band_ok,
                    band_min=band_min,
                    res_max=float(np.max(np.abs(f_e) / lam_np1)))

    def solve(self, z0, max_nfev=250):
        res = least_squares(self.residual, np.asarray(z0, dtype=float),
                            xtol=1e-12, ftol=1e-12, gtol=1e-12, max_nfev=max_nfev)
        return res


def cluster_solutions(sols, tol=1e-6):
    kept = []
    for s in sols:
        e = np.array(s['edges'])
        dup = False
        for k in kept:
            if np.max(np.abs(e - np.array(k['edges']))) < tol:
                dup = True
                break
        if not dup:
            kept.append(s)
    return kept


def one_solve(job):
    """job = (n, R, mode, z0, label). Returns report dict or None."""
    n, R, mode, z0, label = job
    rc = Recon(n, R, mode)
    r = rc.solve(z0)
    if np.max(np.abs(r.fun)) >= 1e-7:
        return None
    rep = rc.full_report(r.x)
    rep['seed'] = label
    rep['cost'] = float(np.max(np.abs(r.fun)))
    return rep


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    seeds = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    mode = sys.argv[4] if len(sys.argv) > 4 else 'both'
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    import multiprocessing as mp
    t0 = time.time()
    rng = np.random.default_rng(20260812)

    known = {}
    try:
        tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
        for m in ('sup', 'inf'):
            key = f"n{n}_{m.upper()}"
            if key in tab:
                known[m] = np.array(tab[key]['edges'])
    except Exception:
        pass

    pool = mp.Pool(processes=workers)
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        rc0 = Recon(n, R, m)
        print(f"=== n={n} R={R} mode={m} pattern={rc0.pat} seeds={seeds} ===", flush=True)
        # --- random seeds: uniform over width simplex ---
        jobs = []
        for t in range(seeds):
            w0 = rng.dirichlet(np.ones(rc0.nb))
            jobs.append((n, R, m, rc0.widths_to_z(w0), f"rand{t}"))
        results = pool.map(one_solve, jobs, chunksize=1)
        sols = [s for s in results if s is not None]
        # --- perturbation center: table solution, else most symmetric root ---
        center = None
        if m in known and len(known[m]) == 2 * n:
            center = known[m]
        else:
            cand = [s for s in sols if s['band_min'] > 1e-7]
            if cand:
                cand.sort(key=lambda s: s['asym'])
                center = np.array(cand[0]['edges'])
        # --- anti-symmetric perturbations of the symmetric solution ---
        pert_jobs = []
        if center is not None:
            e0 = center
            for eps in (1e-5, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1, 2e-1):
                for t in range(16):
                    a = rng.standard_normal(2 * n)
                    a[2 * n - 1 - np.arange(2 * n)] = -a
                    a /= np.linalg.norm(a)
                    e = e0 + eps * a
                    w = np.diff(np.concatenate([[0.0], e, [1.0]]))
                    pert_jobs.append((n, R, m, rc0.widths_to_z(w), f"asym{eps}-{t}"))
            for eps in (1e-4, 1e-2, 5e-2):
                for t in range(8):
                    a = rng.standard_normal(n)
                    a = np.concatenate([a, -a[::-1]])
                    a /= np.linalg.norm(a)
                    e = e0 + eps * a
                    w = np.diff(np.concatenate([[0.0], e, [1.0]]))
                    pert_jobs.append((n, R, m, rc0.widths_to_z(w), f"sym{eps}-{t}"))
            results2 = pool.map(one_solve, pert_jobs, chunksize=1)
            sols = sols + [s for s in results2 if s is not None]
        # --- dedupe and report ---
        unique = cluster_solutions(sols)
        print(f"  total roots found: {len(sols)}, distinct: {len(unique)}", flush=True)
        for i, s in enumerate(sorted(unique, key=lambda z: z['D'])):
            print(f"  [{i}] D={s['D']:.10f} asym={s['asym']:.3e} band={s['band_ok']} "
                  f"band_min={s['band_min']:.2e} res={s['res_max']:.2e} "
                  f"edges={[round(e, 6) for e in s['edges']]}", flush=True)
        n_band = sum(1 for s in unique if s['band_ok'])
        n_band_sym = sum(1 for s in unique if s['band_ok'] and s['asym'] < 1e-7)
        print(f"  distinct roots with correct band matching: {n_band}; "
              f"of those symmetric: {n_band_sym}", flush=True)
        with open(f"scripts/_gapn2_symmetry_recon_n{n}_{m}.json", "w", encoding="utf-8") as fh:
            json.dump(unique, fh, indent=1)
    pool.close()
    pool.join()
    print(f"total wall time {time.time() - t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
