# -*- coding: utf-8 -*-
"""Diagnostics for the analytic Jacobian mismatch.

Prints, at a band-consistent symmetric root:
  1. Jfd vs (D~ + M1 + M2 + M3)/lam_{n+1} term by term (max abs per matrix),
  2. G~_k from regularized resolvent vs explicit spectral sum (first N modes),
  3. the full matrices (Jfd, analytic, difference) for small n.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import jac_fd, symmetric_root
from _gapn2_jacobian_analytic import analytic_jacobian, term_breakdown, regularized_green, green_kernel

np.set_printoptions(precision=6, suppress=True, linewidth=160)


def spectral_green_tilde(rc, z, lam, k, edges, N=300):
    """Explicit sum_{l != k, l <= N} u_l(x_i) u_l(x_j)/(lambda_l - lam)."""
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, N + 1)
    G = np.zeros((len(edges), len(edges)))
    for l in range(N + 1):
        if l == k:
            continue
        ul = eigfun(blocks, ss[l], edges)
        G += np.outer(ul, ul) / (ss[l] ** 2 - lam)
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
    print(f"n={n} R={R} mode={mode} res={np.max(np.abs(rc.residual(zs))):.2e}")

    Jfd = jac_fd(rc, zs)
    J, fprime, fprime_id, wj, wj2 = analytic_jacobian(rc, zs)
    tb = term_breakdown(rc, zs)
    lam_n, lam_np1 = None, None
    blocks = rc.blocks_from_z(zs)
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2

    print("\n--- term magnitudes (max abs) ---")
    print(f"|Jfd| = {np.max(np.abs(Jfd)):.6e}")
    print(f"|D~/l| = {np.max(np.abs(np.diag(fprime) / lam_np1)):.6e}")
    print(f"|M1/l| = {np.max(np.abs(tb['M1'] / lam_np1)):.6e}")
    print(f"|M2/l| = {np.max(np.abs(tb['M2'] / lam_np1)):.6e}")
    print(f"|M3/l| = {np.max(np.abs(tb['M3'] / lam_np1)):.6e}")
    A = (np.diag(tb['fprime']) + tb['M1'] + tb['M2'] + tb['M3']) / lam_np1
    print(f"|Jfd - A| = {np.max(np.abs(Jfd - A)):.6e}")

    print("\n--- difference matrix Jfd - A ---")
    print(Jfd - A)

    print("\n--- Jfd ---")
    print(Jfd)

    print("\n--- regularized Green check: G~_n(analytic residue) vs spectral sum ---")
    edges = np.cumsum(rc.z_to_widths(zs))[:-1]
    u_n = eigfun(blocks, ss[n - 1], edges)
    Gtilde_reg = regularized_green(blocks, lam_n, edges, u_k=u_n)
    Gtilde_sum = spectral_green_tilde(rc, zs, lam_n, n - 1, edges, N=300)
    print(f"max |Gtilde_reg - Gtilde_sum| = {np.max(np.abs(Gtilde_reg - Gtilde_sum)):.6e}")
    print(f"max |Gtilde_reg| = {np.max(np.abs(Gtilde_reg)):.6e}, "
          f"max |Gtilde_sum| = {np.max(np.abs(Gtilde_sum)):.6e}")

    u_np1 = eigfun(blocks, ss[n], edges)
    Gtilde_reg2 = regularized_green(blocks, lam_np1, edges, u_k=u_np1)
    Gtilde_sum2 = spectral_green_tilde(rc, zs, lam_np1, n, edges, N=300)
    print(f"G~_{n+1}: max |reg - sum| = {np.max(np.abs(Gtilde_reg2 - Gtilde_sum2)):.6e}")

    print("\n--- M2 via regularized vs spectral (to isolate Green source) ---")
    svec = tb['s']
    M2s = np.zeros_like(tb['M2'])
    M2r = np.zeros_like(tb['M2'])
    m = 2 * n
    for j in range(m):
        for i in range(m):
            M2s[j, i] = svec[i] * 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gtilde_sum[j, i]
            M2r[j, i] = svec[i] * 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gtilde_reg[j, i]
    print(f"max |M2_reg - M2_sum| = {np.max(np.abs(M2r - M2s)):.6e}")


if __name__ == '__main__':
    main()
