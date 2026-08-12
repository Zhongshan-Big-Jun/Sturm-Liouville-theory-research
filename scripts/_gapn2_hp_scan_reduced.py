# -*- coding: utf-8 -*-
"""Reduced-cost rerun of the INF high-precision Jacobian scan.

Handoff 2026-08-12: the full scan (N=2000 Richardson, 13-point R grid) timed
out.  This driver reruns the INF branch with N=600 Richardson (G~ at 600 and
1200, tail ~1/(pi^2 N), Richardson removes the 1/N term => ~1/N^2) and a
reduced 9-point R grid, preserving the descending continuation order.

For each (n, R) on the symmetric INF branch (pattern [R,1,...,R]) it reports:
  res     - max |F| residual of the band self-consistency system
  D       - lambda_{n+1} - lambda_n
  detJ    - det of the analytic Jacobian J = D_xF
  detK+/- - det of the symmetric/antisymmetric blocks of K = diag(1/s) J
  evK+/-  - spectra of the two blocks
  cross   - max |K+-, K-+| (block off-diagonals, should be ~0 by equivariance)
  detC/D  - dets of the cross blocks of J (det J = (-1)^n detC detD, STRICT
            identity from tools/band-selfconsistency-equivariance.md)

All numerical output is EVIDENCE (not a proof).

Usage: python _gapn2_hp_scan_reduced.py [ns] [mode] [N]
"""
import sys
import json
import time
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_hp_scan import analytic_jacobian_hp

# descending first for continuation, then a jump to large R
RGRID = [4.0, 3.0, 2.5, 2.0, 1.5, 1.2, 1.1, 1.05, 10.0]


def sym_anti_blocks_full(M, n):
    """Full (sym, anti) block decomposition of a 2n x 2n matrix M."""
    S = np.zeros((2 * n, 2 * n))
    for j in range(n):
        S[j, j] = 1.0; S[j, 2 * n - 1 - j] = 1.0
        S[n + j, j] = 1.0; S[n + j, 2 * n - 1 - j] = -1.0
    T = np.linalg.inv(S)
    M2 = S @ M @ T
    return M2[:n, :n], M2[n:, n:], M2[:n, n:], M2[n:, :n]


def scan_one(n, mode, N, Rgrid_use, tab, out):
    """Run one (n, mode) branch over Rgrid_use; merge rows into out[key]."""
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    prev = None
    print(f"===== n={n} mode={mode} N={N} (Richardson) =====", flush=True)
    rows = []
    for R in Rgrid_use:
        rcR = Recon(n, R, mode)
        z = z0 if prev is None else prev
        t0 = time.time()
        zs = symmetric_root(rcR, z)
        if zs is None:
            zs = symmetric_root(rcR, z0)
        if zs is None:
            print(f"R={R:6.3g}: root NOT found", flush=True)
            rows.append(dict(R=R, status='no_root'))
            continue
        prev = zs
        res = np.max(np.abs(rcR.residual(zs)))
        ed = eigen_data(rcR, zs)
        D = ed['lam_np1'] - ed['lam_n']
        pat = rcR.pat
        s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
        J = analytic_jacobian_hp(rcR, zs, N=N)
        K2 = np.diag(1.0 / s) @ J
        Kpp, Kmm, Kpm, Kmp = sym_anti_blocks_full(K2, n)
        Jpp, Jmm, Jpm, Jmp = sym_anti_blocks_full(J, n)
        evp = np.sort(np.linalg.eigvalsh(Kpp))
        evm = np.sort(np.linalg.eigvalsh(Kmm))
        detJ = np.linalg.det(J)
        row = dict(
            R=R, res=float(res), D=float(D),
            N=N,
            detJ=float(detJ),
            detKp=float(np.linalg.det(Kpp)),
            detKm=float(np.linalg.det(Kmm)),
            evKp=[float(v) for v in evp],
            evKm=[float(v) for v in evm],
            crossK=float(np.max(np.abs(Kpm)) + np.max(np.abs(Kmp))),
            detC=float(np.linalg.det(Jpm)),
            detD=float(np.linalg.det(Jmp)),
            dt=float(time.time() - t0),
        )
        # STRICT identity check: det J = (-1)^n detC detD
        row['detJ_minus_id'] = float(detJ - (-1.0) ** n * row['detC'] * row['detD'])
        rows.append(row)
        print(f"R={R:6.3g} res={res:.1e} D={D:12.6f} detJ={detJ:+.4e} "
              f"detK+={row['detKp']:+.4e} detK-={row['detKm']:+.4e} "
              f"evK+={np.round(evp,5)} evK-={np.round(evm,5)} "
              f"crossK={row['crossK']:.1e} id_err={row['detJ_minus_id']:.1e} "
              f"t={row['dt']:.0f}s", flush=True)
    out[key] = rows


def main():
    ns = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3, 4]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'inf'
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 600
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    out = {}
    Rgrid_use = [float(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else RGRID
    path = r'scripts/_gapn2_hp_scan_inf_reduced.json'
    try:
        prev = json.load(open(path, encoding='utf-8'))
        out = prev.get('data', {})
    except Exception:
        out = {}
    modes = ['sup', 'inf'] if mode == 'both' else [mode]
    for m in modes:
        for n in ns:
            scan_one(n, m, N, Rgrid_use, tab, out)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(dict(mode=mode, N=N, Rgrid=Rgrid_use, data=out), fh, indent=1)
    print(f"saved {path}", flush=True)


if __name__ == '__main__':
    main()
