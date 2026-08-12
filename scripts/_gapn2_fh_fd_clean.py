# -*- coding: utf-8 -*-
"""Clean FD test of delta lambda / delta x_i WITHOUT the z parameterization."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root


def lam_of_blocks(blocks, k):
    ss = roots_of(blocks, k + 1)
    return ss[k] ** 2


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
    pat = rc.pat
    nb = len(w)
    edges = np.cumsum(w)[:-1]
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])

    h = 1e-6
    for k_idx, tag in ((n - 1, "n"), (n, "n+1")):
        blocks0 = [(w[i], pat[i]) for i in range(nb)]
        ss0 = roots_of(blocks0, n + 1)
        lam0 = ss0[k_idx] ** 2
        uk = eigfun(blocks0, ss0[k_idx], edges)
        for i in range(2 * n):
            wp = w.copy(); wm = w.copy()
            wp[i] -= h; wp[i + 1] += h
            wm[i] += h; wm[i + 1] -= h
            bp = [(wp[j], pat[j]) for j in range(nb)]
            bm = [(wm[j], pat[j]) for j in range(nb)]
            lp = lam_of_blocks(bp, k_idx)
            lm = lam_of_blocks(bm, k_idx)
            fd = (lp - lm) / (2 * h)
            th = -lam0 * s[i] * uk[i] ** 2
            print(f"k={tag} i={i}: fd={fd:+.10e} th={th:+.10e} ratio={fd/th:.8f} "
                  f"u^2={uk[i]**2:.8f} s={s[i]}")
        # also print uk values
        print(f"uk({tag}) = {np.round(uk, 6)}")


if __name__ == '__main__':
    main()
