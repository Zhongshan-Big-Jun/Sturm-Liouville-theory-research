# -*- coding: utf-8 -*-
"""Check spectral-sum convergence and root quality at R=10 INF."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import gtilde_spectral


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'inf'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)
    blocks = rc.blocks_from_z(zs)
    edges = np.cumsum(rc.z_to_widths(zs))[:-1]
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    print(f"n={n} R={R} mode={mode}; lam_n={lam_n:.4f} lam_np1={lam_np1:.4f}; edges={np.round(edges,4)}")
    print("blocks (L,rho):", [(round(L, 4), c) for L, c in blocks])

    # 1. roots quality: monotone, distinct, asymptotic spacing
    for N in (500, 1000, 2000):
        ssN = roots_of(blocks, N + 1)
        dd = np.diff(ssN)
        bad = np.sum(dd <= 1e-10)
        print(f"N={N}: len={len(ssN)} nonmonotone/dup={bad} "
              f"spacing[min,max] at tail=[{dd[-10:].min():.4f},{dd[-10:].max():.4f}] "
              f"first3={np.round(ssN[:3],4)}")

    # 2. eigenfunction normalization check for sampled modes
    for l in (0, 1, 2, 50, 500, 1500, 1999):
        ssN = roots_of(blocks, N + 1) if False else roots_of(blocks, 2000 + 1)
        u = eigfun(blocks, ssN[l], np.linspace(0.001, 0.999, 500))
        # approximate integral int rho u^2 via block midpoints
        w = rc.z_to_widths(zs)
        xs = np.cumsum(w)
        nrm = 0.0
        for b in range(len(w)):
            pts = np.linspace(max(0.0001, xs[b] - w[b] + 1e-9), min(0.9999, xs[b] - 1e-9), 80)
            uv = eigfun(blocks, ssN[l], pts)
            nrm += np.trapz(uv ** 2 * blocks[b][1], pts)
        print(f"l={l}: s={ssN[l]:.6f} approx_int(rho u^2)={nrm:.6f}")

    # 3. Gtilde convergence
    for k_idx, lamk, tag in ((n - 1, lam_n, "n"), (n, lam_np1, "n+1")):
        G1 = gtilde_spectral(rc, zs, lamk, k_idx, edges, N=500)
        G2 = gtilde_spectral(rc, zs, lamk, k_idx, edges, N=1000)
        G3 = gtilde_spectral(rc, zs, lamk, k_idx, edges, N=2000)
        print(f"G~_{tag}: |G500-G1000|={np.max(np.abs(G1-G2)):.3e} "
              f"|G1000-G2000|={np.max(np.abs(G2-G3)):.3e} "
              f"max|G500|={np.max(np.abs(G1)):.3e} max|G2000|={np.max(np.abs(G3)):.3e}")


if __name__ == '__main__':
    main()
