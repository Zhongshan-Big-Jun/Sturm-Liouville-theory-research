# -*- coding: utf-8 -*-
"""Print G~_k matrices: regularized resolvent at several delta vs spectral sum."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import green_kernel

np.set_printoptions(precision=5, suppress=True, linewidth=180)


def gtilde_spectral(blocks, lamk, k, edges, N=400):
    ss = roots_of(blocks, N + 1)
    G = np.zeros((len(edges), len(edges)))
    for l in range(N + 1):
        if l == k:
            continue
        ul = eigfun(blocks, ss[l], edges)
        G += np.outer(ul, ul) / (ss[l] ** 2 - lamk)
    return G


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'sup'
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

    for tag, k, lamk in (("n", n - 1, lam_n), ("n+1", n, lam_np1)):
        uk = eigfun(blocks, ss[k], edges)
        Gs = gtilde_spectral(blocks, lamk, k, edges, N=500)
        print(f"\n===== G~_{tag} =====")
        print("spectral sum matrix:")
        print(Gs)
        for delta in (1e-4, 1e-6, 1e-8, 1e-10):
            mu = lamk * (1.0 - delta)
            G = green_kernel(blocks, mu, edges)
            Gr = G - np.outer(uk, uk) / (lamk - mu)
            print(f"delta={delta:.0e}: max|reg-sum|={np.max(np.abs(Gr - Gs)):.3e}")
            if delta in (1e-6, 1e-10):
                print("  reg matrix:")
                print(Gr)


if __name__ == '__main__':
    main()
