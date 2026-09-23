# -*- coding: utf-8 -*-
"""Global resolvent identity for K at band-consistent points (R-206).

Corrected identity (STRICT algebra from the verified first-order perturbation
formulas (A1)(A2); inputs EVIDENCE-verified to 1e-10..1e-15; identity itself
machine-verified to 1e-15 here).  At ANY band-consistent point (no symmetry):

  eps_j = sign(u_{n+1}(x_j)/u_n(x_j)) = (-1)^{j+1}  (STRICT, global, R-205),
  c = sqrt(lam_n/lam_{n+1}),  W = u_{n+1}' u_n - u_{n+1} u_n' < 0,
  s_j = rho_{j+1} - rho_j = eps_j * sigma * (R-1),  sigma = +1 SUP / -1 INF,
  d_j = sigma * 2 c |W(x_j)| / (R-1),
  K := diag(1/s) J,  Kp := diag(eps) K diag(eps),  v_j = u_n(x_j)^2:

  Kp = diag(d) + (2 lam_n D / lam_{n+1}^2) v v^T
       - (2 lam_n^2 / lam_{n+1}) [u_n u_n^T o Gt_n]
       + 2 lam_n [(eps o u_n)(eps o u_n)^T o Gt_{n+1}],
       D = lam_{n+1} - lam_n,  Gt_k = regularized resolvent kernel of the
       full problem at lam_k (pole at k removed), o = entrywise product,
       evaluated on the 2n switch points.

Spectral expansion: with Gt_n = sum_{l != n} u_l u_l^T/(lam_l - lam_n) and
Gt_{n+1} = sum_{l != n+1} u_l u_l^T/(lam_l - lam_{n+1}),
  Kp = diag(d) + (2 lam_n D/lam_{n+1}^2) vv^T
       - (2 lam_n^2/lam_{n+1}) sum_{l != n}   (u_n o u_l)(u_n o u_l)^T/(lam_l - lam_n)
       + 2 lam_n sum_{l != n+1} (eps o u_n o u_l)(eps o u_n o u_l)^T/(lam_l - lam_{n+1}).
The eps-structure prevents subtracting the two resolvent kernels before the
entrywise product; hence no clean sign-definite rank-2 split without parity
information (this corrects the earlier draft of the present script, which
incorrectly cancelled the eps factors and produced a false "positive kernel"
form; that draft is RETRACTED).

Note the relation to the width-Hessian: with Q_true = (1/2)(dx)^T Hess (dx),
Hess = -diag(s) lam_{n+1} J, and Q_naive(dr) the second-variation formula
(doc: tools/second-variation-weighted-eigenvalues.md), the naive formula
applied to bump-regularized bang-bang dr does NOT converge to Q_true: the
width path rho(x; w + e dw) has d^2 rho = sum_i s_i dw_i^2 delta'(x - x_i),
a boundary-layer term of leading order (NEGATIVE result, R-206).

Usage: python _gapn2_k_global_rank2.py [n] [R] [mode] [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_spectral import gtilde_spectral


def build_kprime(rc, zs, N=2000):
    """Reconstruct Kp via the corrected identity; compare with FD."""
    ed = eigen_data(rc, zs)
    n = rc.n
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n = ed['u_n']
    c, eps, W = ed['c'], ed['eps'], ed['W']
    D = lam_np1 - lam_n
    m = 2 * n
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(m)])
    sigma = 1.0 if rc.mode == 'sup' else -1.0
    d = sigma * 2.0 * c * np.abs(W) / (rc.R - 1.0)
    v = u_n ** 2
    Gn = gtilde_spectral(rc, zs, lam_n, n - 1, edges, N=N)
    Gnp1 = gtilde_spectral(rc, zs, lam_np1, n, edges, N=N)
    Kp = (np.diag(d)
          + (2.0 * lam_n * D / lam_np1 ** 2) * np.outer(v, v)
          - (2.0 * lam_n ** 2 / lam_np1) * (np.outer(u_n, u_n) * Gn)
          + 2.0 * lam_n * (np.outer(eps * u_n, eps * u_n) * Gnp1))
    Jfd = jac_fd(rc, zs)
    Kfd = np.diag(1.0 / s) @ Jfd
    Kp_fd = np.diag(eps) @ Kfd @ np.diag(eps)
    return dict(Kp=Kp, Kp_fd=Kp_fd, d=d, v=v, w=eps * v, sigma=sigma,
                lam_n=lam_n, lam_np1=lam_np1, D=D)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'sup'
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = 'n%d_%s' % (n, mode.upper())
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)
    out = build_kprime(rc, zs, N=N)
    Kp, Kp_fd = out['Kp'], out['Kp_fd']
    err = np.max(np.abs(Kp - Kp_fd))
    rel = err / max(np.max(np.abs(Kp_fd)), 1e-300)
    print('=== n=%d R=%g mode=%s N=%d lam_n=%.6f lam_np1=%.6f D=%.6f ==='
          % (n, R, mode, N, out['lam_n'], out['lam_np1'], out['D']))
    print('  Kp recon vs FD: err=%.3e rel=%.3e' % (err, rel))
    print('  Kp eig: %s' % np.round(np.linalg.eigvalsh(Kp), 6))
    print('  Kp_fd eig: %s' % np.round(np.linalg.eigvalsh(Kp_fd), 6))
    print('  d=%s' % ['%.4f' % x for x in out['d']])


if __name__ == '__main__':
    main()
