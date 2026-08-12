# -*- coding: utf-8 -*-
"""G~_k via explicit spectral sum: sum_{l != k, l <= N} u_l(x) u_l(y)/(lambda_l - lam_k).

More robust than the resolvent subtraction (W(lam) -> 0 near the pole causes
catastrophic cancellation for delta < 1e-6).  Tail error ~ sum_{l>N} O(1)/lambda_l
~ 1/(pi^2 N) times mean u_l u_l, i.e. ~ 1e-5 at N = 2000 (verified by N doubling).

Jacobian formula (verified 2026-08-12 against clean raw-block FD, EVIDENCE):
  J_ji = dF_j/dx_i = (diag(f') + M~)/lam_np1,
  M~_{ji} = s_i { +2 w_i w_j D/(lam_n lam_np1)
                  - 2 lam_n^2 u_n(x_i) u_n(x_j) G~_n(x_i,x_j)
                  + 2 lam_np1^2 u_np1(x_i) u_np1(x_j) G~_np1(x_i,x_j) },
  derived from first-order perturbation theory with the geometric convention
  delta rho = -s_i delta(x-x_i) delta x_i when switch i moves RIGHT by delta x_i
  (region [x_i, x_i+dx] changes pat[i+1] -> pat[i]; the sign of delta rho is the
  OPPOSITE of the naive convention - this was the original source of confusion).
  Checked: delta lam_k/dx_i = +lam_k s_i u_k(x_i)^2, delta u_k/dx_i at fixed points
  = +u_k(1/2) s_i u_k(x_i)^2 - lam_k s_i u_k(x_i) G~_k, both to 1e-10; off-diagonal
  Jacobian entries to ~1e-6 (FD truncation).
"""
import sys
import json
import time
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import jac_fd, symmetric_root
from _gapn2_jacobian_analytic import eigen_data


def gtilde_spectral(rc, z, lam, k, edges, N=2000):
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, N + 1)
    G = np.zeros((len(edges), len(edges)))
    for l in range(N + 1):
        if l == k:
            continue
        ul = eigfun(blocks, ss[l], edges)
        G += np.outer(ul, ul) / (ss[l] ** 2 - lam)
    return G


def analytic_jacobian_spectral(rc, z, N=2000):
    """Analytic Jacobian with spectral-sum regularized Green kernels."""
    ed = eigen_data(rc, z)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n, u_np1 = ed['u_n'], ed['u_np1']
    up_n, up_np1 = ed['up_n'], ed['up_np1']
    n = rc.n
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    D = lam_np1 - lam_n
    wj = lam_n * u_n ** 2
    fprime = 2.0 * lam_n * u_n * up_n - 2.0 * lam_np1 * u_np1 * up_np1
    Gn = gtilde_spectral(rc, z, lam_n, n - 1, edges, N=N)
    Gnp1 = gtilde_spectral(rc, z, lam_np1, n, edges, N=N)
    M = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            term = (2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1)
                    - 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j]
                    + 2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
            M[j, i] = s[i] * term
    J = (np.diag(fprime) + M) / lam_np1
    return J


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.05, 2.0, 4.0, 10.0]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        rc0 = Recon(n, R=4.0, mode=m)
        key = f"n{n}_{m.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc0.widths_to_z(w0)
        prev = None
        print(f"=== n={n} mode={m} N={N} ===")
        for R in Rs:
            rcR = Recon(n, R, m)
            z = z0 if prev is None else prev
            zs = symmetric_root(rcR, z)
            if zs is None:
                print(f"R={R}: no symmetric root found"); continue
            prev = zs
            Jfd = jac_fd(rcR, zs)
            t0 = time.time()
            J = analytic_jacobian_spectral(rcR, zs, N=N)
            err = np.max(np.abs(J - Jfd))
            rel = err / np.max(np.abs(Jfd))
            res = np.max(np.abs(rcR.residual(zs)))
            print(f"R={R:8.4g} |Jfd|max={np.max(np.abs(Jfd)):10.3e} "
                  f"err={err:10.3e} rel={rel:10.3e} res={res:10.3e} t={time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
