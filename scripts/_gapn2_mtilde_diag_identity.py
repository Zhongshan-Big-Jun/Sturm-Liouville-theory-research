# -*- coding: utf-8 -*-
"""Verify (EVIDENCE) the closed-form decomposition of the diagonal of M~:

  M~_{jj}/s_j = 2 w_j Sigma'(x_j) + 4 w_j^2 (D^2 - lambda_n lambda_{n+1})
                / (lambda_n lambda_{n+1} D),
  Sigma'(x) = sum_{l != n, n+1} lambda_l u_l(x)^2 D
              / ((lambda_l - lambda_{n+1})(lambda_l - lambda_n)) > 0 (strictly).

Derivation: at a band-consistent point w_j = lambda_n u_n(x_j)^2
= lambda_{n+1} u_{n+1}(x_j)^2, and
  lambda_{n+1} G~_{n+1} - lambda_n G~_n = Sigma' - 2 w_j / D - w_j D/(lambda_n lambda_{n+1})
via the partial-fraction identity lambda/(lambda_l - lambda)
= lambda_l/(lambda_l - lambda) - 1:  the l = n pole term is -lambda_n u_n^2/D
= -w_j/D, the l = n+1 term is -lambda_{n+1} u_{n+1}^2/D = -w_j/D, and
u_{n+1}^2 - u_n^2 = -w_j D/(lambda_n lambda_{n+1}) (all exact).

Also probe Sylvester pivots of K (LU without pivoting) for a constant sign
pattern.  All output is EVIDENCE.
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
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 800
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
                    print(f"n={n} {mode} R={R}: no root"); continue
                prev = zs
                ed = eigen_data(rcR, zs)
                lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
                D = lam_np1 - lam_n
                edges = ed['edges']
                u_n = ed['u_n']
                wj = lam_n * u_n ** 2
                blocks = rcR.blocks_from_z(zs)
                ss = roots_of(blocks, N + 1)
                lam_all = ss ** 2
                m = 2 * n
                Gn_diag = np.zeros(m)
                Gnp1_diag = np.zeros(m)
                sig = np.zeros(m)
                for l in range(N + 1):
                    ul = eigfun(blocks, ss[l], edges)
                    if l != n - 1:
                        Gn_diag += ul ** 2 / (lam_all[l] - lam_n)
                    if l != n:
                        Gnp1_diag += ul ** 2 / (lam_all[l] - lam_np1)
                    if l != n - 1 and l != n:
                        sig += lam_all[l] * ul ** 2 * D / ((lam_all[l] - lam_np1) * (lam_all[l] - lam_n))
                # LHS: M~_{jj}/s_j (analytic formula)
                lhs = (2.0 * wj * wj * D / (lam_n * lam_np1)
                       - 2.0 * lam_n ** 2 * u_n ** 2 * Gn_diag
                       + 2.0 * lam_np1 ** 2 * ed['u_np1'] ** 2 * Gnp1_diag)
                # RHS: closed form (corrected: +4 w_j^2 (D^2 - lam_n lam_np1)/(lam_n lam_np1 D))
                rhs = 2.0 * wj * sig - 4.0 * wj ** 2 / D
                rel = np.max(np.abs(lhs - rhs)) / max(np.max(np.abs(lhs)), 1e-300)
                # sign of the closed form
                sgn_rhs = np.sign(rhs)
                # partial-fraction identity with the SAME truncation:
                # lam_np1 G~_np1 - lam_n G~_n = sig - 2 wj/D + wj D/(lam_n lam_np1)
                ident = lam_np1 * Gnp1_diag - lam_n * Gn_diag - (sig - 2.0 * wj / D - wj * D / (lam_n * lam_np1))
                idrel = np.max(np.abs(ident)) / max(np.max(np.abs(lam_np1 * Gnp1_diag)), 1e-300)
                # Sylvester pivots of K (LU without pivoting), K from FD Jacobian
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(m)])
                Jfd = jac_fd(rcR, zs)
                K = np.diag(1.0 / s) @ Jfd
                piv = []
                A = K.copy()
                ok = True
                for k in range(m):
                    if abs(A[k, k]) < 1e-300:
                        ok = False
                        break
                    piv.append(A[k, k])
                    A[k + 1:, k + 1:] -= np.outer(A[k + 1:, k], A[k, k + 1:]) / A[k, k]
                piv = np.array(piv)
                pivsgn = np.sign(piv) if ok else None
                print(f"n={n} {mode:3s} R={R:5.2f}  M~diag-id rel={rel:.2e}  "
                      f"pf-ident rel={idrel:.2e}  sgn(rhs)={sgn_rhs}  "
                      f"detK={np.linalg.det(K):+.3e}  pivots={pivsgn}", flush=True)


if __name__ == '__main__':
    main()
