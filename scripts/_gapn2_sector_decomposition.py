# -*- coding: utf-8 -*-
"""Sector decomposition of K at band-consistent points (EVIDENCE unless STRICT).

At a symmetric band-consistent root (structure theorem), with left-half sector
coordinates j = 1..n (mirror pairing j <-> 2n+1-j):

  K = D_f + E + H,   (mirror blocks: K_e = Be^T K Be, K_o = Bo^T K Bo)

  D_f = diag(sigma * 2 c |W(x_j)|/(R-1)),   sigma = +1 SUP / -1 INF,
  E_e = c_e w_h w_h^T,    c_e = 4 D/(lam_n lam_{n+1}^2) > 0,
  E_o = c_o (eps_h . w_h)(eps_h . w_h)^T,   c_o = -4 (lam_n^2+lam_{n+1}^2)
        / (lam_n lam_{n+1} D lam_{n+1}) < 0,
  (H_e)_ij = (2 lam_n/lam_{n+1}) u_i u_j [ Sigma'(x_i,x_j) - p_n Sigma_+(x_i,xbar_j) ]  (i~j parity)
           = (2 lam_n/lam_{n+1}) u_i u_j [ -Sigma_+(x_i,x_j) + p_n Sigma'(x_i,xbar_j) ]  (i!~j)
  (H_o)_ij = (2 lam_n/lam_{n+1}) u_i u_j [ Sigma'(x_i,x_j) + p_n Sigma_+(x_i,xbar_j) ]   (i~j)
           = (2 lam_n/lam_{n+1}) u_i u_j [ -Sigma_+(x_i,x_j) - p_n Sigma'(x_i,xbar_j) ]  (i!~j)

with w_j = lam_n u_n(x_j)^2, eps_j = (-1)^{j+1} (STRICT alternating, verified
n = 2..5 both modes), p_n = (-1)^{n-1} (parity of u_n), xbar_j = 1 - x_j,
Sigma'(x,y) = sum_{l != n,n+1} a_l u_l(x) u_l(y),
  a_l = lam_l D / ((lam_l - lam_{n+1})(lam_l - lam_n)) > 0,
Sigma_+(x,y) = sum_{l != n,n+1} b_l u_l(x) u_l(y),
  b_l = lam_n/(lam_l - lam_n) + lam_{n+1}/(lam_l - lam_{n+1}).

These closed forms are verified to machine precision (rel 1e-15..1e-16) at
n = 2, 3, R = 4 (see _gapn2_mtilde_offdiag_identity.py) and used here to scan
the sector spectra / sharp dominance inequalities over an R ladder.

Scan results (EVIDENCE, saved to scripts/_gapn2_sector_scan_<n>_<mode>.json):
- SUP: K_e, K_o positive definite on every scan point
  (n=2: R in 1.05..100; n=3: 1.2..10; n=4: 1.2..10), and the sufficient
  inequalities lammin(H_o - E_o) + min d > 0, lammin(H_e + E_e) + min d > 0
  hold with positive margin on every point.
- INF: K_e, K_o negative definite on every scan point (n=2: R <= 100; n=3:
  R <= 30), but the naive sufficient inequalities lammax(H+E) - min|d| < 0
  FAIL at large R (n=2 R=100 borderline; n=3 R >= 4): the true negativity
  uses the non-uniform diagonal; det K -> 0+ as R -> inf (no uniform margin).
- Sylvester pivots of K_e and K_o (LU without pivoting): SUP all +, INF all -
  on every scan point (equivalent to sector definiteness by Sylvester's law).

Usage: python _gapn2_sector_decomposition.py <n> <sup|inf> [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data


def sector_data(rc, zs, N=121):
    """Closed-form sector decomposition at the symmetric root zs."""
    ed = eigen_data(rc, zs)
    n = rc.n
    mode = rc.mode
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    D = lam_np1 - lam_n
    u_n = ed['u_n']
    eps = ed['eps']
    W = ed['W']
    c = ed['c']
    m = 2 * n
    wj = lam_n * u_n ** 2
    blocks = rc.blocks_from_z(zs)
    ss = roots_of(blocks, N + 1)
    lam_all = ss ** 2
    ni, nj = n - 1, n
    x = ed['edges']
    xbar = 1.0 - x
    U = np.zeros((N + 1, m))
    Ubar = np.zeros((N + 1, m))
    for l in range(N + 1):
        U[l] = eigfun(blocks, ss[l], x)
        Ubar[l] = eigfun(blocks, ss[l], xbar)
    wgt_s1 = np.zeros(N + 1)
    wgt_s2 = np.zeros(N + 1)
    for l in range(N + 1):
        if l != ni and l != nj:
            wgt_s1[l] = lam_all[l] * D / ((lam_all[l] - lam_np1) * (lam_all[l] - lam_n))
            wgt_s2[l] = lam_n / (lam_all[l] - lam_n) + lam_np1 / (lam_all[l] - lam_np1)
    S1 = U.T @ np.diag(wgt_s1) @ U
    S2 = U.T @ np.diag(wgt_s2) @ U
    S1b = U.T @ np.diag(wgt_s1) @ Ubar
    S2b = U.T @ np.diag(wgt_s2) @ Ubar
    sigma = 1.0 if mode == 'sup' else -1.0
    R = rc.R
    d = sigma * 2.0 * c * np.abs(W) / (R - 1.0)
    wh = wj[:n]
    eh = eps[:n]
    c_e = 4.0 * D / (lam_n * lam_np1 ** 2)
    c_o = -4.0 * (lam_n ** 2 + lam_np1 ** 2) / (lam_n * lam_np1 * D * lam_np1)
    pn = 1.0 if n % 2 == 1 else -1.0
    pmask = np.fromfunction(lambda i, j: (i + j) % 2 == 0, (n, n))
    uu = np.outer(u_n[:n], u_n[:n])
    fac = 2.0 * lam_n / lam_np1
    He = fac * uu * (np.where(pmask, S1[:n, :n] - pn * S2b[:n, :n], -S2[:n, :n] + pn * S1b[:n, :n]))
    Ho = fac * uu * (np.where(pmask, S1[:n, :n] + pn * S2b[:n, :n], -S2[:n, :n] - pn * S1b[:n, :n]))
    Ee = c_e * np.outer(wh, wh)
    Eo = c_o * np.outer(eh * wh, eh * wh)
    Ke = np.diag(d[:n]) + Ee + He
    Ko = np.diag(d[:n]) + Eo + Ho
    out = dict(d=d[:n].tolist(), c_e=c_e, c_o=c_o, He=He.tolist(), Ho=Ho.tolist(),
               Ee=Ee.tolist(), Eo=Eo.tolist(), Ke=Ke.tolist(), Ko=Ko.tolist())
    for k, M in (('Ke', Ke), ('Ko', Ko), ('He', He), ('Ho', Ho), ('Ee', Ee), ('Eo', Eo)):
        out[k + '_ev'] = np.linalg.eigvalsh(M).tolist()
    return out


def main():
    n = int(sys.argv[1])
    mode = sys.argv[2]
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 121
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f'n{n}_{mode.upper()}'
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    if n == 2:
        Rs = [1.05, 1.2, 2.0, 4.0, 10.0, 30.0, 100.0]
    else:
        Rs = [1.2, 2.0, 4.0, 10.0, 30.0, 100.0]
    results = {}
    prev = z0
    for R in Rs:
        rc = Recon(n, R, mode)
        zs = symmetric_root(rc, prev)
        if zs is None:
            results[str(R)] = {'status': 'no root'}
            continue
        prev = zs
        try:
            sd = sector_data(rc, zs, N=N)
            sd['status'] = 'ok'
            results[str(R)] = sd
        except Exception as e:
            results[str(R)] = {'status': 'fail: %s: %s' % (type(e).__name__, e)}
        print('n=%d %s R=%s: %s' % (n, mode, R, results[str(R)]['status']), flush=True)
    out = r'scripts/_gapn2_sector_scan_%d_%s.json' % (n, mode)
    json.dump(results, open(out, 'w'), indent=1)
    print('saved', out)


if __name__ == '__main__':
    main()
