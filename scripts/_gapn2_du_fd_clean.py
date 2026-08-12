# -*- coding: utf-8 -*-
"""Clean FD test of delta u_k (fixed point) at switch i != j.

th_plus  = -u(x_j)(1/2) s_i u(x_i)^2 + lam s_i u(x_i) G~_k(x_j,x_i)
th_minus = -u(x_j)(1/2) s_i u(x_i)^2 - lam s_i u(x_i) G~_k(x_j,x_i)
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import gtilde_spectral


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
        Gk = gtilde_spectral(rc, zs, lam0, k_idx, edges, N=2000)
        for i in range(2 * n):
            wp = w.copy(); wm = w.copy()
            wp[i] -= h; wp[i + 1] += h
            wm[i] += h; wm[i + 1] -= h
            bp = [(wp[j], pat[j]) for j in range(nb)]
            bm = [(wm[j], pat[j]) for j in range(nb)]
            ssp = roots_of(bp, n + 1); ssm = roots_of(bm, n + 1)
            up = eigfun(bp, ssp[k_idx], edges)
            um = eigfun(bm, ssm[k_idx], edges)
            du_fd = (up - um) / (2 * h)
            # exclude j == i (moving point)
            for j in range(2 * n):
                if j == i:
                    continue
                du_th_plus = -uk[j] * 0.5 * s[i] * uk[i] ** 2 + lam0 * s[i] * uk[i] * Gk[j, i]
                du_th_minus = -uk[j] * 0.5 * s[i] * uk[i] ** 2 - lam0 * s[i] * uk[i] * Gk[j, i]
                fd = du_fd[j]
                print(f"k={tag} i={i} j={j}: fd={fd:+.8e} plus={du_th_plus:+.8e} "
                      f"minus={du_th_minus:+.8e}  |fd-plus|={abs(fd-du_th_plus):.2e} "
                      f"|fd-minus|={abs(fd-du_th_minus):.2e}")


if __name__ == '__main__':
    main()
