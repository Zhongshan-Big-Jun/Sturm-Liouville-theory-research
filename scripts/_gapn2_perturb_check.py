# -*- coding: utf-8 -*-
"""Test first-order perturbation formulas for delta lambda_k / delta u_k at a switch.

Compares FD (perturb switch x_i by h in the width parameterization) with:
  dlam_i = -lam_k * s_i * u_k(x_i)^2                       (FH)
  du_k(x_j) = -u_k(x_j) * (1/2) * s_i * u_k(x_i)^2
              +- lam_k * s_i * u_k(x_i) * G~_k(x_j, x_i)   (resolvent part sign TBD)
and reports which sign of the resolvent part matches.
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
    blocks = rc.blocks_from_z(zs)
    w = rc.z_to_widths(zs)
    edges = np.cumsum(w)[:-1]
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    print(f"n={n} R={R} mode={mode}; lam_n={lam_n:.6f} lam_np1={lam_np1:.6f}")
    print(f"edges = {np.round(edges, 5)}; s = {s}")

    h = 1e-6
    for k_idx, (tag, lamk) in enumerate((("n", lam_n), ("n+1", lam_np1))):
        uk = eigfun(blocks, ss[k_idx], edges)
        # G~_k at edges
        Gk = gtilde_spectral(rc, zs, lamk, k_idx, edges, N=2000)
        # FD: move switch i by h: widths w_i -= h, w_{i+1} += h
        for i in range(2 * n):
            wplus = w.copy(); wminus = w.copy()
            wplus[i] -= h; wplus[i + 1] += h
            wminus[i] += h; wminus[i + 1] -= h
            zplus = rc.widths_to_z(wplus); zminus = rc.widths_to_z(wminus)
            bplus = rc.blocks_from_z(zplus); bminus = rc.blocks_from_z(zminus)
            ssp = roots_of(bplus, n + 1); ssm = roots_of(bminus, n + 1)
            lam_fd = ((ssp[k_idx] ** 2 - ssm[k_idx] ** 2) / (2 * h))
            edges_plus = np.cumsum(wplus)[:-1]
            u_fd = np.zeros(2 * n)
            for j in range(2 * n):
                # value at the (moving) switch x_j: evaluate on the perturbed config
                u_fd[j] = (eigfun(bplus, ssp[k_idx], [edges_plus[j]])[0]
                           - eigfun(bminus, ssm[k_idx], [edges[j]])[0]) / (2 * h)
            dlam_th = -lamk * s[i] * uk[i] ** 2
            du_norm = -uk * (0.5) * s[i] * uk[i] ** 2
            du_res = lamk * s[i] * uk[i] * Gk[:, i]
            du_th_plus = du_norm + du_res
            du_th_minus = du_norm - du_res
            err_plus = np.max(np.abs(u_fd - du_th_plus))
            err_minus = np.max(np.abs(u_fd - du_th_minus))
            err_lam = abs(lam_fd - dlam_th) / max(abs(lam_fd), 1e-30)
            print(f"k={tag} i={i}: lam err={err_lam:.2e} | u: plus={err_plus:.3e} minus={err_minus:.3e}"
                  f"  (max|du_fd|={np.max(np.abs(u_fd)):.3e})")


if __name__ == '__main__':
    main()
