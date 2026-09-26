# -*- coding: utf-8 -*-
"""Green inertia probe for the half problems and the K_o reduction (EVIDENCE).

On the symmetric branch, the odd-sector reduced resolvents
  R_n^bot  = sum_{l opposite parity to mode n} u_l u_l/(lambda_l - lambda_n),
  R_{n+1}^bot = sum_{l opposite parity to mode n+1} u_l u_l/(lambda_l - lambda_{n+1})
restricted to the n left-half switches have, by the classical Gantmacher-Krein
oscillation theorem, negative index equal to the number of opposite-parity
half eigenvalues strictly below the spectral parameter:
  n even: R_n^bot has n/2 negative, R_{n+1}^bot has n/2 negative;
  n odd : R_n^bot has (n-1)/2 negative, R_{n+1}^bot has (n+1)/2 negative.
This probe verifies the exact reconstruction
  K_o = diag(d) + (4 lambda_n/lambda_{n+1}) diag(u) M diag(u),
  M   = lambda_{n+1} diag(eps) R_{n+1}^bot diag(eps) - lambda_n R_n^bot,
and compares the inertia of M with that of K_o (whose definiteness is supplied
by the non-uniform diagonal d).
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data


def reduced_resolvent(blocks, mu, pts, par, N=200):
    """R = sum over the parity class `par` of u_l u_l/(lambda_l - mu)."""
    ss = roots_of(blocks, N + 1)
    lam_all = ss ** 2
    pts = np.array(pts)
    G = np.zeros((len(pts), len(pts)))
    for l in range(N + 1):
        u = eigfun(blocks, ss[l], pts)
        outer = np.outer(u, u)
        if (l % 2 == 0) == (par == 'even'):
            if abs(lam_all[l] - mu) > 1e-9:
                G += outer / (lam_all[l] - mu)
    return G


def inertia(M, tol=1e-7):
    ev = np.linalg.eigvalsh(M)
    return (int((ev > tol).sum()), int((ev < -tol).sum()),
            int((np.abs(ev) <= tol).sum()))


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for n, R, mode in [(2, 4.0, 'sup'), (2, 4.0, 'inf'),
                       (3, 4.0, 'sup'), (3, 4.0, 'inf')]:
        rc = Recon(n, R, mode)
        key = 'n%d_%s' % (n, mode.upper())
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc.widths_to_z(w0)
        zs = symmetric_root(rc, z0)
        blocks = rc.blocks_from_z(zs)
        ed = eigen_data(rc, zs)
        lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
        x = ed['edges'][:n]
        u = ed['u_n'][:n]
        eps = ed['eps'][:n]
        if n % 2 == 0:
            R_lo = reduced_resolvent(blocks, lam_n, x, 'even')
            R_hi = reduced_resolvent(blocks, lam_np1, x, 'odd')
        else:
            R_lo = reduced_resolvent(blocks, lam_n, x, 'odd')
            R_hi = reduced_resolvent(blocks, lam_np1, x, 'even')
        E = np.diag(eps)
        M = lam_np1 * (E @ R_hi @ E) - lam_n * R_lo
        sd = sector_data(rc, zs, N=200)
        Ko = np.array(sd['Ko'])
        d = np.array(sd['d'])
        fac = 4.0 * lam_n / lam_np1
        Ho = np.array(sd['Ho'])
        Eo = np.array(sd['Eo'])
        recon = fac * np.diag(u) @ M @ np.diag(u)
        rel = np.linalg.norm(recon - (Ho + Eo)) / max(np.linalg.norm(Ho + Eo), 1e-300)
        print('n=%d %s R=%g: lam_n=%.4f lam_np1=%.4f' % (n, mode, R, lam_n, lam_np1))
        print('  R_n^bot inertia %s, R_{n+1}^bot inertia %s' %
              (inertia(R_lo), inertia(R_hi)))
        print('  M inertia %s, Ko inertia %s' % (inertia(M), inertia(Ko)))
        print('  K_o = diag(d)+fac*diag(u)M diag(u) recon rel err: %.2e' % rel)
        print('  d = %s' % ['%.4f' % v for v in d])


if __name__ == '__main__':
    main()
