# -*- coding: utf-8 -*-
"""Test the spectral Green kernel conventions at a band-consistent point.

Checks:
  1. G_mu (resolvent via phi/psi/W) vs explicit spectral sum at a NON-resonant mu.
  2. Residue identity: lim_{mu -> lambda_k^-} (lambda_k - mu) G_mu(x_i,x_j)
     == u_k(x_i) u_k(x_j)  (u_k = eigfun, rho-normalized).
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import green_kernel


def spectral_green(rc, z, mu, edges, N=300):
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, N + 1)
    G = np.zeros((len(edges), len(edges)))
    for l in range(N + 1):
        ul = eigfun(blocks, ss[l], edges)
        G += np.outer(ul, ul) / (ss[l] ** 2 - mu)
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
    ss = roots_of(blocks, n + 2)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    print(f"n={n} R={R} mode={mode}; lam_n={lam_n:.6f} lam_np1={lam_np1:.6f}")

    # 1. non-resonant mu: midpoint between lam_n and lam_np1
    mu = 0.5 * (lam_n + lam_np1)
    Gf = green_kernel(blocks, mu, edges)
    Gs = spectral_green(rc, zs, mu, edges, N=400)
    print(f"\n[1] mu = {mu:.6f} (between lam_n and lam_np1)")
    print(f"    max |G_resolvent - G_spectral| = {np.max(np.abs(Gf - Gs)):.6e}")
    print(f"    max |G_resolvent| = {np.max(np.abs(Gf)):.6e}")

    # 2. residue at lam_n
    for tag, k, lamk in (("n", n - 1, lam_n), ("n+1", n, lam_np1)):
        uk = eigfun(blocks, ss[k], edges)
        for delta in (1e-4, 1e-6, 1e-8, 1e-10):
            mu = lamk * (1.0 - delta)
            Gf2 = green_kernel(blocks, mu, edges)
            Rres = Gf2 * (lamk - mu)
            err = np.max(np.abs(Rres - np.outer(uk, uk)))
            print(f"[2] k={tag} delta={delta:.0e}: max |(lam-mu)G - u_k u_k| = {err:.6e}")
        # Gtilde consistency at delta = 1e-8
        mu = lamk * (1.0 - 1e-8)
        Gf2 = green_kernel(blocks, mu, edges)
        Gt_reg = Gf2 - np.outer(uk, uk) / (lamk - mu)
        Gt_sum = spectral_green(rc, zs, lamk, edges, N=400)
        Gt_sum -= np.outer(uk, uk) / 0.0  # remove pole contribution: spectral at mu=lamk
        # recompute properly: sum over l != k
        Gt_sum2 = np.zeros_like(Gt_reg)
        sss = roots_of(blocks, 400 + 1)
        for l in range(400 + 1):
            if l == k:
                continue
            ul = eigfun(blocks, sss[l], edges)
            Gt_sum2 += np.outer(ul, ul) / (sss[l] ** 2 - lamk)
        print(f"    max |Gtilde_reg - Gtilde_spectral| = {np.max(np.abs(Gt_reg - Gt_sum2)):.6e}")


if __name__ == '__main__':
    main()
