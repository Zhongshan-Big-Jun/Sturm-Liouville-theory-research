# -*- coding: utf-8 -*-
"""Verify (EVIDENCE) the closed-form OFF-DIAGONAL decomposition of M~ at
band-consistent points, plus mirror-sector structure probes.

Termwise-exact identities (hold for ANY truncation set L excluding the modes
l = n-1, n in 0-based indexing; verified to machine precision):

(C1) eps_i == eps_j  (same half):
  T_ji = 2 lam_n u_n(x_i) u_n(x_j) Sigma'(x_i,x_j) - 4 w_i w_j / D
(C2) eps_i == -eps_j (cross half):
  T_ji = 4 w_i w_j (lam_{n+1}^2 - lam_n lam_{n+1} + lam_n^2)/(lam_n lam_{n+1} D)
         - 2 lam_n u_n(x_i) u_n(x_j) Sigma_+(x_i,x_j)

where T_ji = M~_ji / s_i is the sign-independent factor of M~,
  Sigma'(x_i,x_j)  = sum_{l in L} a_l u_l(x_i) u_l(x_j),
                     a_l = lam_l D / ((lam_l - lam_{n+1})(lam_l - lam_n)),
  Sigma_+(x_i,x_j) = sum_{l in L} b_l u_l(x_i) u_l(x_j),
                     b_l = lam_n/(lam_l - lam_n) + lam_{n+1}/(lam_l - lam_{n+1}).

Derivation: per-mode partial fractions
  lam_{n+1}/(lam_l-lam_{n+1}) - lam_n/(lam_l-lam_n) = lam_l D/prod,
plus the band-consistent relations u_{n+1}(x_j) = eps_j c u_n(x_j),
w_j = lam_n u_n(x_j)^2, and the pole terms from l = n, n+1 which collapse
via u_{n+1}^2 - u_n^2 = w D/(lam_n lam_{n+1}) (same half) or the cross
identity u_{n+1}(x_i)u_{n+1}(x_j) = -lam_n p / lam_{n+1} (opposite half).

Also verified: resolvent identity (truncation-free via orthogonality)
  G~_{n+1}(x,y) - G~_n(x,y) = D * (G~_{n+1} o G~_n)(x,y),
  (A o B)(x,y) = int_0^1 A(x,t) B(t,y) rho(t) dt.

Structure probes at band points: K = D_f + E + H with
  D_f = diag(sigma * 2 c |W_j| / (R-1)), sigma = +1 SUP / -1 INF,
  E    = rank-2 pole part (closed form),
  H    = (2 lam_n/lam_{n+1}) diag(u_n) K~ diag(u_n),  K~_ij = Sigma' or
         -Sigma_+ according to the eps-pair,
and the mirror-sector (even/odd) spectra of K, E, H.  All output EVIDENCE.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    ns = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3]
    Rs = [float(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.2, 2.0, 4.0, 10.0]
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    for n in ns:
        for mode in ('sup', 'inf'):
            rc0 = Recon(n, R=4.0, mode=mode)
            key = f"n{n}_{mode.upper()}"
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc0.widths_to_z(w0)
            prev = None
            for R in Rs:
                rcR = Recon(n, R, mode)
                z = z0 if prev is None else prev
                zs = symmetric_root(rcR, z)
                if zs is None:
                    print(f"n={n} {mode} R={R}: no symmetric root"); continue
                prev = zs
                ed = eigen_data(rcR, zs)
                lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
                D = lam_np1 - lam_n
                edges = ed['edges']
                u_n, u_np1 = ed['u_n'], ed['u_np1']
                c, eps, W = ed['c'], ed['eps'], ed['W']
                m = 2 * n
                wj = lam_n * u_n ** 2
                blocks = rcR.blocks_from_z(zs)
                ss = roots_of(blocks, N + 1)
                lam_all = ss ** 2
                lam_n_idx, lam_np1_idx = n - 1, n
                U = np.zeros((N + 1, m))
                for l in range(N + 1):
                    U[l] = eigfun(blocks, ss[l], edges)
                # weighted Green matrices (truncated)
                wgt_n = np.zeros(N + 1)
                wgt_np1 = np.zeros(N + 1)
                wgt_s1 = np.zeros(N + 1)
                wgt_s2 = np.zeros(N + 1)
                for l in range(N + 1):
                    if l != lam_n_idx:
                        wgt_n[l] = 1.0 / (lam_all[l] - lam_n)
                    if l != lam_np1_idx:
                        wgt_np1[l] = 1.0 / (lam_all[l] - lam_np1)
                    if l != lam_n_idx and l != lam_np1_idx:
                        wgt_s1[l] = lam_all[l] * D / ((lam_all[l] - lam_np1) * (lam_all[l] - lam_n))
                        wgt_s2[l] = lam_n / (lam_all[l] - lam_n) + lam_np1 / (lam_all[l] - lam_np1)
                Gn = U.T @ np.diag(wgt_n) @ U
                Gnp1 = U.T @ np.diag(wgt_np1) @ U
                S1 = U.T @ np.diag(wgt_s1) @ U
                S2 = U.T @ np.diag(wgt_s2) @ U
                # analytic LHS (uniform formula), symmetric in (i, j)
                p = np.outer(u_n, u_n)
                T_lhs = (2.0 * np.outer(wj, wj) * D / (lam_n * lam_np1)
                         - 2.0 * lam_n ** 2 * p * Gn
                         + 2.0 * lam_np1 ** 2 * np.outer(u_np1, u_np1) * Gnp1)
                # closed form
                eij = np.outer(eps, eps)
                same = (eij > 0)
                T_cf = np.where(
                    same,
                    2.0 * lam_n * p * S1 - 4.0 * np.outer(wj, wj) / D,
                    4.0 * np.outer(wj, wj) * (lam_np1 ** 2 - lam_n * lam_np1 + lam_n ** 2)
                    / (lam_n * lam_np1 * D) - 2.0 * lam_n * p * S2)
                rel = np.max(np.abs(T_lhs - T_cf)) / max(np.max(np.abs(T_lhs)), 1e-300)
                # diagonal closed form (I2) with the SAME truncation
                diag_id = np.max(np.abs(T_lhs.diagonal() - (2.0 * wj * S1.diagonal() - 4.0 * wj ** 2 / D))) \
                    / max(np.max(np.abs(T_lhs.diagonal())), 1e-300)
                # resolvent identity on a per-block grid
                ng = 16
                xs = [0.0]
                for L, _ in blocks:
                    xs.append(xs[-1] + L)
                grid = []
                for bi in range(len(blocks)):
                    a, b = xs[bi], xs[bi + 1]
                    grid.extend(np.linspace(a, b, ng + 1)[:-1])
                grid.append(1.0)
                grid = np.array(grid)
                rho_g = np.array([blocks[max(i for i in range(len(blocks)) if xs[i] <= p)][1]
                                  for p in grid])
                ngrid = len(grid)
                V = np.zeros((N + 1, ngrid))
                for l in range(N + 1):
                    V[l] = eigfun(blocks, ss[l], grid)
                Gn_g = V.T @ np.diag(wgt_n) @ V
                Gnp1_g = V.T @ np.diag(wgt_np1) @ V
                # trapezoidal weights on the composite grid
                h = np.diff(grid)
                wq = np.zeros(ngrid)
                for i in range(ngrid - 1):
                    wq[i] += h[i] / 2.0
                    wq[i + 1] += h[i] / 2.0
                prod = Gnp1_g @ np.diag(rho_g * wq) @ Gn_g
                res_id = np.max(np.abs(Gnp1_g - Gn_g - D * prod)) \
                    / max(np.max(np.abs(Gnp1_g)), 1e-300)
                # structure: K = D_f + E + H
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(m)])
                sigma = 1.0 if mode == 'sup' else -1.0
                Df = np.diag(sigma * 2.0 * c * np.abs(W) / (R - 1.0))
                E = np.where(same,
                             -4.0 * np.outer(wj, wj) / (D * lam_np1),
                             4.0 * np.outer(wj, wj) * (lam_np1 ** 2 - lam_n * lam_np1 + lam_n ** 2)
                             / (lam_n * lam_np1 * D * lam_np1))
                Ktilde = np.where(same, S1, -S2)
                H = (2.0 * lam_n / lam_np1) * np.diag(u_n) @ Ktilde @ np.diag(u_n)
                K_cf = Df + E + H
                Jfd = jac_fd(rcR, zs)
                K_fd = np.diag(1.0 / s) @ Jfd
                Krel = np.max(np.abs(K_cf - K_fd)) / max(np.max(np.abs(K_fd)), 1e-300)
                # mirror sectors
                P = np.eye(m)[::-1]
                Be = np.zeros((m, n)); Bo = np.zeros((m, n))
                for j in range(n):
                    Be[j, j] = Be[m - 1 - j, j] = 1.0 / np.sqrt(2.0)
                    Bo[j, j] = 1.0 / np.sqrt(2.0); Bo[m - 1 - j, j] = -1.0 / np.sqrt(2.0)
                Ke = Be.T @ K_fd @ Be
                Ko = Bo.T @ K_fd @ Bo
                He = Be.T @ H @ Be
                Ho = Bo.T @ H @ Bo
                Ee = Be.T @ E @ Be
                Eo = Bo.T @ E @ Bo
                evK = np.linalg.eigvalsh(K_fd)
                evKe = np.linalg.eigvalsh(Ke)
                evKo = np.linalg.eigvalsh(Ko)
                evHe = np.linalg.eigvalsh(He)
                evHo = np.linalg.eigvalsh(Ho)
                evEe = np.linalg.eigvalsh(Ee)
                evEo = np.linalg.eigvalsh(Eo)
                detK = np.linalg.det(K_fd)
                detSec = np.linalg.det(Ke) * np.linalg.det(Ko)
                print(f"n={n} {mode:3s} R={R:5.2f}  C1C2 rel={rel:.2e}  I2 rel={diag_id:.2e}  "
                      f"resolv rel={res_id:.2e}  K-cf rel={Krel:.2e}", flush=True)
                print(f"    evK={np.round(evK,4)}  evKe={np.round(evKe,4)}  evKo={np.round(evKo,4)}")
                print(f"    evH(e/o)={np.round(evHe,4)}/{np.round(evHo,4)}  "
                      f"evE(e/o)={np.round(evEe,4)}/{np.round(evEo,4)}  "
                      f"detK={detK:+.3e} det(e*o)={detSec:+.3e}", flush=True)


if __name__ == '__main__':
    main()
