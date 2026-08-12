# -*- coding: utf-8 -*-
"""Boundary slope comparison lemma - tests for (G2) endpoint exclusion.

Part A: at band-consistent points (alternating bang-bang family, exactly 2n
switches, SUP/INF branches) check the endpoint expansion
    f(x) = (lam_n u_n'(0)^2 - lam_{n+1} u_{n+1}'(0)^2) x^2 + O(x^4),
i.e. whether the framework slope ratio q0 = u'_{n+1}(0)/u'_n(0) > 1 holds with
positive margin (block-energy identity K == -2D), equivalently a < 0.
Validated against f(x) at small x (finite difference of the exact
transfer-matrix eigenfunctions).

Part B: random bang-bang widths (heights in {1, R}, 2n+1 blocks): violation
rate of the same inequality, classified by pattern type (alternating vs not,
first block 1 vs R) and by minimal block width (near-degenerate configs).

Usage: python _gapn2_slope_ratio.py [part] [n] [Rmax]
"""
import sys, json
import numpy as np
from scipy.optimize import least_squares
from _gapn2_symmetry_recon import Recon, roots_of, D_scalar, eigfun

# ----------------------------------------------------------------------------
# exact slope at 0 (Dirichlet u(0)=0, unnormalized slope = 1 at x=0)
# ----------------------------------------------------------------------------
def eigfun_slope0(blocks, s):
    """Normalized u'(0) for the eigenfunction with sqrt(s) = s eigenvalue."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    starts = [(0.0, M00, M01, M10, M11)]
    for L, c in blocks:
        w = s * np.sqrt(c); wL = w * L
        cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
        M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
                             sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
        starts.append((xs[len(starts)], M00, M01, M10, M11))
    norm = 0.0
    for bi, (L, c) in enumerate(blocks):
        w = s * np.sqrt(c)
        _, _, M01b, _, M11b = starts[bi]
        A = M01b; B = M11b / w
        Icos = 0.5 * (L + np.sin(2 * w * L) / (2 * w))
        Isin = 0.5 * (L - np.sin(2 * w * L) / (2 * w))
        Icross = np.sin(w * L) ** 2 / (2 * w)
        norm += c * (A * A * Icos + B * B * Isin + 2 * A * B * Icross)
    return 1.0 / np.sqrt(norm)


def slope_ratio_report(blocks, n):
    """Returns dict: lam_n, lam_np1, r = q0 = u'_{n+1}(0)/u'_n(0) (framework
    convention, no sqrt(lam) weights),
    a = lam_n u_n'(0)^2 - lam_{n+1} u_{n+1}'(0)^2 (should be < 0 for band match),
    and validation of the quadratic expansion f(x) ~= a x^2 near 0."""
    ss = roots_of(blocks, n + 1)
    sn, sp = ss[n - 1], ss[n]
    lam_n, lam_np1 = sn * sn, sp * sp
    un0, up0 = eigfun_slope0(blocks, sn), eigfun_slope0(blocks, sp)
    r = up0 / un0
    a = lam_n * un0 ** 2 - lam_np1 * up0 ** 2
    # validation: f(x) at x = 1e-4, 1e-3 vs a x^2
    fv = []
    for x in (1e-4, 1e-3):
        uv = eigfun(blocks, sn, np.array([x]))[0]
        up = eigfun(blocks, sp, np.array([x]))[0]
        fx = lam_n * uv ** 2 - lam_np1 * up ** 2
        fv.append(fx / (a * x * x))
    return dict(lam_n=float(lam_n), lam_np1=float(lam_np1),
                r=float(r), a=float(a), a_scaled=float(a / lam_np1),
                f_ratio=fv)


def branch_solution(n, R, mode, seed=None):
    """Solve the band self-consistency system on the alternating branch."""
    rc = Recon(n, R, mode)
    if seed is None:
        tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
        key = f"n{n}_{mode.upper()}"
        if key in tab:
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            seed = rc.widths_to_z(w0)
        else:
            seed = rc.widths_to_z(np.full(rc.nb, 1.0 / rc.nb))
    res = rc.solve(seed)
    if np.max(np.abs(res.fun)) >= 1e-7:
        return None, rc
    rep = rc.full_report(res.x)
    return rep, rc


def part_a(n, rmax):
    print(f"=== Part A: band-consistent alternating branches, n={n}, R<= {rmax} ===")
    for mode in ('sup', 'inf'):
        rc0 = Recon(n, 4.0, mode)
        rep, _ = branch_solution(n, 4.0, mode)
        if rep is None:
            print(f"  n={n} {mode}: no R=4 root"); continue
        widths = np.array(rep['widths'])
        rows = [(4.0, rep, widths)]
        # ladder upward
        prev_w = widths
        for R in np.concatenate([np.linspace(4.5, rmax, 40)]):
            rc = Recon(n, float(R), mode)
            w = np.clip(prev_w, 1e-6, 1 - 1e-6); w = w / w.sum()
            z0 = rc.widths_to_z(w)
            r2, rc2 = branch_solution(n, float(R), mode, seed=z0)
            if r2 is None:
                print(f"  n={n} {mode} R={R:.2f}: no root (branch lost)"); break
            rows.append((float(R), r2, np.array(r2['widths'])))
            prev_w = np.array(r2['widths'])
        # ladder downward
        prev_w = widths
        for R in np.linspace(3.5, 1.05, 30):
            rc = Recon(n, float(R), mode)
            w = np.clip(prev_w, 1e-6, 1 - 1e-6); w = w / w.sum()
            r2, rc2 = branch_solution(n, float(R), mode, seed=rc.widths_to_z(w))
            if r2 is None:
                print(f"  n={n} {mode} R={R:.2f}: no root"); break
            rows.append((float(R), r2, np.array(r2['widths'])))
            prev_w = np.array(r2['widths'])
        # report
        bad = []
        for R, rep, _w in rows:
            rcc = Recon(n, float(R), mode)
            blocks = [(float(w), rcc.pat[i]) for i, w in enumerate(_w)]
            sr = slope_ratio_report(blocks, n)
            row = dict(R=R, mode=mode, D=rep['D'], band_ok=rep['band_ok'],
                       r=sr['r'], a=sr['a'], a_scaled=sr['a_scaled'],
                       f_ratio=sr['f_ratio'])
            print(f"  {mode} R={R:8.3f} D={rep['D']:12.6f} band={rep['band_ok']} "
                  f"r={sr['r']:.6f} a_scaled={sr['a_scaled']:.3e} "
                  f"f/(a x^2)={[round(v, 4) for v in sr['f_ratio']]}")
            if not (sr['r'] > 1.0 and sr['a'] < 0.0):
                bad.append((R, row))
        print(f"  {mode}: violations (r<=1 or a>=0): {len(bad)}")
        for R, row in bad:
            print(f"    R={R:.3f} r={row['r']:.6f} a={row['a']:.3e}")
    return rows


def part_b(n, R, ntrials, seed=20260812):
    print(f"=== Part B: random bang-bang n={n} R={R} trials={ntrials} ===")
    rng = np.random.default_rng(seed)
    counts = {}
    viol = {}
    for t in range(ntrials):
        h = rng.choice([1.0, R], size=2 * n + 1)
        # random widths
        w = rng.dirichlet(np.ones(2 * n + 1) * 2.0)
        # merge adjacent equal blocks
        merged_h, merged_w = [], []
        for hi, wi in zip(h, w):
            if merged_h and merged_h[-1] == hi:
                merged_w[-1] += wi
            else:
                merged_h.append(hi); merged_w.append(wi)
        blocks = [(float(wi), float(hi)) for wi, hi in zip(merged_w, merged_h)]
        nsw = len(merged_h) - 1
        alt = (nsw == 2 * n)  # alternating with exactly 2n switches
        first = merged_h[0]
        cls = ('alt' if alt else 'nonalt') + ('_R' if first == R else '_1')
        minw = min(merged_w)
        sr = slope_ratio_report(blocks, n)
        ok = sr['r'] > 1.0 and sr['a'] < 0.0
        counts[cls] = counts.get(cls, 0) + 1
        if not ok:
            viol[cls] = viol.get(cls, 0) + 1
            if minw < 0.02:
                viol['near_degen'] = viol.get('near_degen', 0) + 1
    print("  class        trials   violations")
    for cls in sorted(counts):
        print(f"  {cls:14s} {counts[cls]:6d} {viol.get(cls, 0):6d}")
    print(f"  near_degen (min width < 0.02 among violators): {viol.get('near_degen', 0)}")


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else 'a'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    rmax = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
    if part == 'a':
        part_a(n, rmax)
    else:
        R = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
        nt = int(sys.argv[4]) if len(sys.argv) > 4 else 300
        part_b(n, R, nt)
