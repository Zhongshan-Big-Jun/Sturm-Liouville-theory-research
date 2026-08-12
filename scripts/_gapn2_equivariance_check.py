# -*- coding: utf-8 -*-
"""Test the equivariance identity F(sigma x) = sigma F(x) numerically."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root


def sigma_x(x, n):
    """reflection of switch positions: (sigma x)_j = 1 - x_{2n+1-j}."""
    m = 2 * n
    out = x.copy()
    for j in range(m):
        out[j] = 1.0 - x[m - 1 - j]
    return out


def widths_from_edges(edges, nb):
    w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
    return w


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
    w = rc.z_to_widths(zs)
    edges = np.cumsum(w)[:-1]
    print(f"n={n} R={R} mode={mode}; symmetric edges={np.round(edges,6)}")

    # exact identity at the symmetric point and near it
    rng = np.random.default_rng(7)
    for eps in (0.0, 1e-3, 1e-1):
        worst = 0.0
        for t in range(5):
            delta = eps * rng.standard_normal(2 * n)
            x = edges + delta
            sx = sigma_x(x, n)
            w_sx = widths_from_edges(sx, 2 * n + 1)
            w_x = widths_from_edges(x, 2 * n + 1)
            Fx = rc.residual(rc.widths_to_z(w_x))
            Fsx = rc.residual(rc.widths_to_z(w_sx))
            lhs = Fsx
            rhs = Fx[::-1]
            worst = max(worst, np.max(np.abs(lhs - rhs)))
        print(f"eps={eps}: max|F(sigma x) - sigma F(x)| = {worst:.3e}")


if __name__ == '__main__':
    main()
