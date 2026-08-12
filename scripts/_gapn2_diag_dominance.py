# -*- coding: utf-8 -*-
"""Probe (EVIDENCE): diagonal-sign structure of K = diag(1/s) J at band-consistent
points along the symmetric branch.

Checks:
  (1) f'(x_j)/s_j constant sign per mode: SUP positive, INF negative
      (STRICT derivation: f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j), W < 0,
       eps_j = s_j/(R-1) for SUP and eps_j = -s_j/(R-1) for INF).
  (2) diagonal elements of K: sign and relative size of the f'-term vs the
      Green-kernel terms M1+M2+M3.
  (3) Gershgorin disks of K: |K_ii| vs sum_{j != i} |K_ij| (row sum).
  (4) spectra of K+ (symmetric block) and K- (antisymmetric block).
  (5) smallest |ev K| vs diagonal-matrix approximation: det K vs prod(K_ii).

All output is EVIDENCE; nothing here is a proof.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data, analytic_jacobian


def sym_blocks(K):
    """Decompose K into symmetric (even) and antisymmetric (odd) blocks."""
    m = K.shape[0]
    n = m // 2
    S = np.zeros((m, m))
    for j in range(n):
        S[j, j] = 1.0
        S[j, m - 1 - j] = 1.0
        S[n + j, j] = 1.0
        S[n + j, m - 1 - j] = -1.0
    M2 = S @ K @ np.linalg.inv(S)
    return M2[:n, :n], M2[n:, n:]


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    ns = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3]
    Rs = [float(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.2, 2.0, 4.0, 10.0]
    modes = sys.argv[3].split(',') if len(sys.argv) > 3 else ['sup', 'inf']
    for n in ns:
        for mode in modes:
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
                    print(f"n={n} {mode} R={R}: no root"); continue
                prev = zs
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                ed = eigen_data(rcR, zs)
                lam = ed['lam_np1']
                eps = ed['eps']
                W = ed['W']
                fprime = ed['lam_n'] * ed['u_n'] ** 2 * 0 + \
                    2.0 * ed['lam_n'] * ed['u_n'] * ed['up_n'] - \
                    2.0 * ed['lam_np1'] * ed['u_np1'] * ed['up_np1']
                # (1) constant-sign check of f'/s
                r = fprime / s
                sgn_ok = (np.all(r > 0) and mode == 'sup') or (np.all(r < 0) and mode == 'inf')
                # analytic identity f' = -2 lam_{n+1} eps c W  (c = sqrt(lam_n/lam_np1))
                fid = -2.0 * lam * eps * ed['c'] * W
                id_err = np.max(np.abs(fprime - fid)) / np.max(np.abs(fprime))
                # (2) K via FD Jacobian (authoritative; analytic unreliable near degeneracy)
                Jfd = jac_fd(rcR, zs)
                K = np.diag(1.0 / s) @ Jfd
                Kdiag = np.diag(K)
                # f'-term inside K: f'(x_j)/(s_j lam_{n+1})
                Kf = fprime / (s * lam)
                # M-part diagonal: Kdiag - Kf
                Km = Kdiag - Kf
                # (3) Gershgorin row sums (off-diagonal)
                offrow = np.sum(np.abs(K - np.diag(Kdiag)), axis=1)
                gersh = np.all(np.abs(Kdiag) > offrow)
                # (4) blocks
                Kp, Km_ = sym_blocks(K)
                evp = np.sort(np.linalg.eigvalsh(Kp))
                evm = np.sort(np.linalg.eigvalsh(Km_))
                # (5) det comparisons
                detK = np.linalg.det(K)
                prod_diag = np.prod(Kdiag)
                res = np.max(np.abs(rcR.residual(zs)))
                print(f"n={n} {mode:3s} R={R:5.2f} res={res:.1e}")
                print(f"   (1) f'/s sign-const({mode})={sgn_ok}  f'/s range=[{r.min():+.4e},{r.max():+.4e}]  "
                      f"id_err={id_err:.1e}")
                print(f"   (2) Kdiag range=[{Kdiag.min():+.4e},{Kdiag.max():+.4e}]  "
                      f"Kf/Kdiag |ratio|=[{np.min(np.abs(Kf / Kdiag)):.4f},{np.max(np.abs(Kf / Kdiag)):.4f}]  "
                      f"Km/Kdiag |ratio|=[{np.min(np.abs(Km / Kdiag)):.4f},{np.max(np.abs(Km / Kdiag)):.4f}]")
                print(f"   (3) Gershgorin row-dominant={gersh}  margin/min|Kdiag|="
                      f"{(np.min(np.abs(Kdiag) - offrow)) / np.min(np.abs(Kdiag)):+.4f}")
                print(f"   (4) evK+={np.round(evp, 4)}  evK-={np.round(evm, 4)}")
                print(f"   (5) detK={detK:+.4e}  prod(Kdiag)={prod_diag:+.4e}  "
                      f"detK/prod={detK / prod_diag:+.4f}")


if __name__ == '__main__':
    main()
