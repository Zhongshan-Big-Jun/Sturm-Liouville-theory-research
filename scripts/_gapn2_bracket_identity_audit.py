# -*- coding: utf-8 -*-
"""Audit: new bracket identities for the sector decomposition of K (EVIDENCE).

Newly derived identities (this session), valid at a SYMMETRIC band-consistent
point (the mirror sector decomposition and the parity relation
u_l(1-x) = (-1)^{l-1} u_l(x) require the density to be reflection symmetric,
i.e. symmetric widths; palindromic HEIGHTS alone do NOT give eigenfunction
parity -- see the 2026-08-13b addendum for the numerical refutation):

  bracket_e_same(x_i,x_j) :=  Sigma'(x_i,x_j) - p_n Sigma_+(x_i,xbar_j)
       = -2 lam_n R_n^||(x_i,x_j) + 2 lam_{n+1} R_{n+1}^||(x_i,x_j)      (i~j)
  bracket_e_cross(x_i,x_j) := -Sigma_+(x_i,x_j) + p_n Sigma'(x_i,xbar_j)
       = -2 lam_n R_n^||(x_i,x_j) - 2 lam_{n+1} R_{n+1}^||(x_i,x_j)      (i!~j)
  bracket_o_same(x_i,x_j) :=  Sigma'(x_i,x_j) + p_n Sigma_+(x_i,xbar_j)
       = +2 lam_{n+1} R_{n+1}^bot(x_i,x_j) - 2 lam_n R_n^bot(x_i,x_j)
         + (2 u_i u_j / D) (lam_{n+1} + lam_n^2/lam_{n+1})               (i~j)
  bracket_o_cross(x_i,x_j) := -Sigma_+(x_i,x_j) - p_n Sigma'(x_i,xbar_j)
       = -2 lam_{n+1} R_{n+1}^bot(x_i,x_j) - 2 lam_n R_n^bot(x_i,x_j)
         + (2 u_i u_j / D) (-lam_{n+1} - lam_n^2/lam_{n+1})              (i!~j)

with R_k^|| = same-parity reduced resolvent (l==k mod 2, l!=k),
     R_k^bot = opposite-parity reduced resolvent,
     u_i = u_n(x_i), p_n = (-1)^{n-1}, xbar_j = 1 - x_j,
     D = lam_{n+1} - lam_n.

Consequence (verified separately): in K_o = diag(d) + E_o + H_o the rank-1
part E_o cancels the u_i u_j/D correction of the bracket exactly, so
  K_o = diag(d_h) + H_o' with
  (H_o')_ij = (4 lam_n/lam_{n+1}) u_i u_j [lam_{n+1} eps_i eps_j R_{n+1}^bot
              - lam_n R_n^bot].

Also verifies: x_n < 1/2 < x_{n+1} at every band-consistent point (STRICT
structural claim: center zero of the odd mode lies in cell n), and the
half-problem interpretation R_k^||/R_k^bot = -(1/2) * full/residual Green
kernels of the Neumann/Dirichlet half-problems at lam_k.
"""
import sys
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data


def bracket_audit(rc, zs, N=121, tol=1e-10):
    ed = eigen_data(rc, zs)
    n = rc.n
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    D = lam_np1 - lam_n
    u_n = ed['u_n']
    eps = ed['eps']
    x = ed['edges']
    xbar = 1.0 - x
    ni, nj = n - 1, n
    blocks = rc.blocks_from_z(zs)
    ss = roots_of(blocks, N + 1)
    lam_all = ss ** 2
    m = 2 * n
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
    pn = 1.0 if n % 2 == 1 else -1.0

    # reduced resolvent kernels on the full switch grid
    def rk(k):
        out = np.zeros((m, m))
        for l in range(N + 1):
            if l != k:
                out += np.outer(U[l], U[l]) / (lam_all[l] - lam_all[k])
        return out
    Rn = rk(ni)
    Rnp1 = rk(nj)
    par = np.array([(-1) ** l for l in range(N + 1)])
    Rn_par = np.zeros((m, m))
    Rn_cross = np.zeros((m, m))
    Rnp1_par = np.zeros((m, m))
    Rnp1_cross = np.zeros((m, m))
    for l in range(N + 1):
        if l == ni or l == nj:
            continue
        if par[l] == par[ni]:
            Rn_par += np.outer(U[l], U[l]) / (lam_all[l] - lam_n)
            Rnp1_cross += np.outer(U[l], U[l]) / (lam_all[l] - lam_np1)
        else:
            Rn_cross += np.outer(U[l], U[l]) / (lam_all[l] - lam_n)
            Rnp1_par += np.outer(U[l], U[l]) / (lam_all[l] - lam_np1)
    # include the cross pole terms
    Rn_cross += np.outer(U[nj], U[nj]) / (lam_np1 - lam_n)
    Rnp1_cross += np.outer(U[ni], U[ni]) / (lam_n - lam_np1)
    uu = np.outer(u_n, u_n)

    def rel(a, b):
        return np.linalg.norm(a - b) / max(np.linalg.norm(b), 1e-300)

    worst = 0.0
    pmask = np.fromfunction(lambda i, j: (i + j) % 2 == 0, (m, m))
    # bracket_e same parity
    lhs = S1 - pn * S2b
    rhs = -2 * lam_n * Rn_par + 2 * lam_np1 * Rnp1_par
    err = rel(np.where(pmask, lhs, 0), np.where(pmask, rhs, 0))
    worst = max(worst, err)
    print('  bracket_e_same  rel err: %.3e' % err)
    # bracket_e cross parity
    lhs = -S2 + pn * S1b
    rhs = -2 * lam_n * Rn_par - 2 * lam_np1 * Rnp1_par
    err = rel(np.where(~pmask, lhs, 0), np.where(~pmask, rhs, 0))
    worst = max(worst, err)
    print('  bracket_e_cross rel err: %.3e' % err)
    # bracket_o same parity
    corr_same = (2.0 / D) * uu * (lam_np1 + lam_n ** 2 / lam_np1)
    lhs = S1 + pn * S2b
    rhs = 2 * lam_np1 * Rnp1_cross - 2 * lam_n * Rn_cross + corr_same
    err = rel(np.where(pmask, lhs, 0), np.where(pmask, rhs, 0))
    worst = max(worst, err)
    print('  bracket_o_same  rel err: %.3e' % err)
    # bracket_o cross parity
    corr_cross = (2.0 / D) * uu * (-lam_np1 - lam_n ** 2 / lam_np1)
    lhs = -S2 - pn * S1b
    rhs = -2 * lam_np1 * Rnp1_cross - 2 * lam_n * Rn_cross + corr_cross
    err = rel(np.where(~pmask, lhs, 0), np.where(~pmask, rhs, 0))
    worst = max(worst, err)
    print('  bracket_o_cross rel err: %.3e' % err)

    # cancellation: E_o + correction of H_o
    fac = 2.0 * lam_n / lam_np1
    pmask_h = np.fromfunction(lambda i, j: (i + j) % 2 == 0, (n, n))
    c_o = -4.0 * (lam_n ** 2 + lam_np1 ** 2) / (lam_n * lam_np1 * D * lam_np1)
    wh = (lam_n * u_n ** 2)[:n]
    eh = eps[:n]
    Eo = c_o * np.outer(eh * wh, eh * wh)
    # correction part of H_o: corr_ij = fac u_i u_j * (2 eps_i eps_j / D)(lam_{n+1}+lam_n^2/lam_{n+1}) u_i u_j
    corr = fac * (2.0 / D) * (lam_np1 + lam_n ** 2 / lam_np1) * np.outer(eh, eh) * (uu[:n, :n] ** 2)
    resid = Eo + corr
    err = np.linalg.norm(resid) / max(np.linalg.norm(Eo), 1e-300)
    worst = max(worst, err)
    print('  Eo+cancellation residual (rel to Eo): %.3e' % err)

    # half-problem interpretations (parity of mode n decides Neumann vs Dirichlet)
    # GN = 2 * sum_{even modes l} u_l u_l/(lam_n - lam_l)  (Neumann half, pole-free)
    # GD = 2 * sum_{odd  modes l} u_l u_l/(lam_np1 - lam_l) (Dirichlet half)
    # R_n^bot  = sum_{l opposite parity to mode n} u_l u_l/(lam_l - lam_n)
    #          = -(1/2) GN (n even) or -(1/2) GD_at_lam_n (n odd).
    GN = np.zeros((m, m))
    GD = np.zeros((m, m))
    for l in range(N + 1):
        if l % 2 == 1:
            # zero-based index l => mode l+1; odd index = even mode = Dirichlet-half
            if abs(lam_all[l] - lam_np1) > 1e-9:
                GD += np.outer(U[l], U[l]) / (lam_np1 - lam_all[l])
        else:
            if abs(lam_all[l] - lam_n) > 1e-9:
                GN += np.outer(U[l], U[l]) / (lam_n - lam_all[l])
    GN *= 2.0
    GD *= 2.0
    # mode n parity: even (n odd) -> opposite is odd -> Dirichlet half at lam_n
    if n % 2 == 0:
        err = rel(Rn_cross, -0.5 * GN)
        print('  R_n^bot = -(1/2) G^N_{lam_n}  rel err: %.3e' % err)
    else:
        GDn = np.zeros((m, m))
        for l in range(N + 1):
            if l % 2 == 1 and abs(lam_all[l] - lam_n) > 1e-9:
                GDn += np.outer(U[l], U[l]) / (lam_n - lam_all[l])
        GDn *= 2.0
        err = rel(Rn_cross, -0.5 * GDn)
        print('  R_n^bot = -(1/2) G^D_{lam_n}  rel err: %.3e' % err)
    if n % 2 == 0:
        err = rel(Rnp1_cross, -0.5 * GD)
        print('  R_{n+1}^bot = -(1/2) G^D_{lam_{n+1}}  rel err: %.3e' % err)
    else:
        GNp = np.zeros((m, m))
        for l in range(N + 1):
            if l % 2 == 0 and abs(lam_all[l] - lam_np1) > 1e-9:
                GNp += np.outer(U[l], U[l]) / (lam_np1 - lam_all[l])
        GNp *= 2.0
        err = rel(Rnp1_cross, -0.5 * GNp)
        print('  R_{n+1}^bot = -(1/2) G^N_{lam_{n+1}}  rel err: %.3e' % err)

    # structural claim: x_n < 1/2 < x_{n+1}
    ok_center = x[n - 1] < 0.5 < x[n]
    print('  x_%d=%.10f < 1/2 < x_%d=%.10f : %s' % (n, x[n - 1], n + 1, x[n], ok_center))
    return worst, GN, GD, Rn_par, Rnp1_par


def main():
    tab = {}
    import json
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for n in (2, 3):
        for mode in ('sup', 'inf'):
            rc = Recon(n, R=4.0, mode=mode)
            key = 'n%d_%s' % (n, mode.upper())
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc.widths_to_z(w0)
            zs = symmetric_root(rc, z0)
            print('n=%d %s:' % (n, mode))
            w, GN, GD, Rn_par, Rnp1_par = bracket_audit(rc, zs)
            # sign patterns of the half-problem Green kernels on the grid
            for name, G in (('G^N_lam_n', GN), ('G^D_lam_{n+1}', GD)):
                sgn = np.sign(G[:n, :n])
                print('  sign(%s) on left-half grid:' % name)
                for row in sgn:
                    print('   ', ' '.join('%2.0f' % v for v in row))


if __name__ == '__main__':
    main()
