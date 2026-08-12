# -*- coding: utf-8 -*-
"""Clean FD test of the OFF-DIAGONAL Jacobian entry dF_j/dx_i (j != i), raw blocks.

Compares with the perturbation formula (derived and partially verified):
  dF_j/dx_i = s_i { -2 w_i w_j D/(lam_n lam_np1)
                    + 2 lam_n^2 u_n(x_j) u_n(x_i) G~_n(x_j,x_i)
                    - 2 lam_np1^2 u_np1(x_j) u_np1(x_i) G~_np1(x_j,x_i) } / lam_np1
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import gtilde_spectral


def f_of(blocks, pts, n):
    """f(x) = lam_n u_n^2 - lam_np1 u_np1^2 at pts, plus (lam_n, lam_np1)."""
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    un = eigfun(blocks, ss[n - 1], pts)
    unp = eigfun(blocks, ss[n], pts)
    return lam_n * un ** 2 - lam_np1 * unp ** 2, lam_n, lam_np1


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

    blocks0 = [(w[i], pat[i]) for i in range(nb)]
    f0, lam_n, lam_np1 = f_of(blocks0, edges, n)
    D = lam_np1 - lam_n
    ss0 = roots_of(blocks0, n + 1)
    un = eigfun(blocks0, ss0[n - 1], edges)
    unp = eigfun(blocks0, ss0[n], edges)
    wj = lam_n * un ** 2
    Gn = gtilde_spectral(rc, zs, lam_n, n - 1, edges, N=2000)
    Gnp1 = gtilde_spectral(rc, zs, lam_np1, n, edges, N=2000)

    print(f"n={n} R={R} mode={mode}; lam_n={lam_n:.6f} lam_np1={lam_np1:.6f}")
    print("f0/lam_np1 (residual) =", np.round(f0 / lam_np1, 10))
    for i in range(2 * n):
        wp = w.copy(); wm = w.copy()
        wp[i] -= h; wp[i + 1] += h
        wm[i] += h; wm[i + 1] -= h
        bp = [(wp[j], pat[j]) for j in range(nb)]
        bm = [(wm[j], pat[j]) for j in range(nb)]
        ep = np.cumsum(wp)[:-1]
        em = np.cumsum(wm)[:-1]
        fp, _, _ = f_of(bp, ep, n)
        fm, _, _ = f_of(bm, em, n)
        # FD of F_j = f(x_j)/lam_{n+1} at the (moving) switch positions
        lams_p = roots_of(bp, n + 1) ** 2
        lams_m = roots_of(bm, n + 1) ** 2
        Fp = fp / lams_p[n]
        Fm = fm / lams_m[n]
        dF = (Fp - Fm) / (2 * h)
        for j in range(2 * n):
            if j == i:
                continue
            th = (s[i] * (-2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1)
                          + 2.0 * lam_n ** 2 * un[j] * un[i] * Gn[j, i]
                          - 2.0 * lam_np1 ** 2 * unp[j] * unp[i] * Gnp1[j, i])) / lam_np1
            print(f"i={i} j={j}: fd={dF[j]:+.8e} th={th:+.8e} |fd-th|={abs(dF[j]-th):.2e}")


if __name__ == '__main__':
    main()
