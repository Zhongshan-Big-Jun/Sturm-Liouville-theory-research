# -*- coding: utf-8 -*-
"""R-207 probe: collapsed Kp identity + structure of S = eps*Gt_{n+1}*eps - (lam_n/lam_{n+1})*Gt_n.

New algebra (to verify, derived this session from the R-206 identity; a
first draft with S = eps*Gt_{n+1}*eps - Gt_n FAILED P1 at rel 0.49 and
was corrected to the (lam_n/lam_{n+1}) mask):
  Kp = diag(d) + c_r * v v^T + 2 lam_n * diag(u_n) S diag(u_n),
  S = eps Gt_{n+1} eps - (lam_n/lam_{n+1}) Gt_n   (Gt_k = regularized resolvent at lam_k),
  c_r = 2 lam_n^2 (lam_n - 3 lam_{n+1}) / (lam_{n+1}^2 D) < 0 ALWAYS,
  v_j = u_n(x_j)^2, u_n = vector (u_n(x_j)).
After congruence by diag(1/u_n):
  Kp~ = diag(d/u^2) + 2 lam_n S + c_r u_n u_n^T.

Additional structural decomposition:
  S = Delta_n + D eps T eps - (eps u_n)(eps u_n)^T / D - (eps u_{n+1})(eps u_{n+1})^T / D,
  Delta_n = eps Gt_n eps - (lam_n/lam_{n+1}) Gt_n
    (diagonal = (D/lam_{n+1}) Gt_n; flips cross-parity entries),
  T = sum_{l != n,n+1} u_l u_l^T / ((lam_l - lam_n)(lam_l - lam_{n+1}))  (PD).

Probes:
  P1: collapsed identity vs FD Kp (expect ~1e-15).
  P2: S decomposition check (Delta + D epsTeps - rank terms) vs S.
  P3: eigenvalues of S, Delta_n, T, eps T eps; and of
      diag(d/u^2) + 2 lam_n S + c_r u u^T (= Kp~) for SUP/INF.
  P4: mirror-basis block structure of Kp~ (even/odd mirror decomposition).
  P5: cross-parity block entries: closed form with Sigma_+ (R-202 (C2))
      vs the low/high mode split Sigma_+ = Sigma_low - Sigma_high.

All numerics EVIDENCE only.
Usage: python _gapn2_kp_collapsed_probe.py [n] [R] [mode] [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_spectral import gtilde_spectral

import warnings
warnings.filterwarnings('ignore')


def build(rc, zs, N=2000):
    ed = eigen_data(rc, zs)
    n = rc.n
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n = ed['u_n']
    u_np1 = ed['u_np1']
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
    S = np.diag(eps) @ Gnp1 @ np.diag(eps) - (lam_n / lam_np1) * Gn
    r = 2.0 * lam_n * D / lam_np1 ** 2
    c2 = lam_n / lam_np1
    Kp = (np.diag(d) + r * np.outer(v, v)
          + 2.0 * lam_n * (np.outer(u_n, u_n) * S))
    Jfd = jac_fd(rc, zs)
    Kfd = np.diag(1.0 / s) @ Jfd
    Kp_fd = np.diag(eps) @ Kfd @ np.diag(eps)
    # P2: S decomposition
    ss = roots_of(rc.blocks_from_z(zs), N + 1)
    T = np.zeros((m, m))
    for l in range(N + 1):
        if l in (n - 1, n):
            continue
        ul = eigfun(rc.blocks_from_z(zs), ss[l], edges)
        T += np.outer(ul, ul) / ((ss[l] ** 2 - lam_n) * (ss[l] ** 2 - lam_np1))
    Delta = np.diag(eps) @ Gn @ np.diag(eps) - (lam_n / lam_np1) * Gn
    epsTeps = np.diag(eps) @ T @ np.diag(eps)
    eun = eps * u_n
    eunp1 = eps * u_np1
    S2 = Delta + D * epsTeps - np.outer(eun, eun) / D - np.outer(eunp1, eunp1) / D
    Kp2 = (np.diag(d) + r * np.outer(v, v)
           - (2.0 * lam_n / D) * (np.diag(eps) @ np.outer(v, v) @ np.diag(eps))
           - (2.0 * lam_n * c2 / D) * np.outer(v, v)
           + 2.0 * lam_n * D * (np.outer(u_n, u_n) * epsTeps)
           + 2.0 * lam_n * (np.outer(u_n, u_n) * Delta))
    Kp_t = np.diag(1.0 / v) @ Kp @ np.diag(1.0 / v)
    out = dict(n=n, lam_n=lam_n, lam_np1=lam_np1, D=D, d=d, v=v,
               S=S, S2=S2, T=T, Delta=Delta, epsTeps=epsTeps, Kp=Kp, Kp2=Kp2,
               Kp_fd=Kp_fd, Kp_t=Kp_t, Gn=Gn, Gnp1=Gnp1, eps=eps, u_n=u_n,
               u_np1=u_np1, edges=edges, rc=rc, zs=zs, N=N, r=r, c2=c2)
    return out


def mirror_blocks(out):
    m = 2 * out['n']
    A = out['Kp_t']
    n = out['n']
    idx = list(range(m))
    pairs = [(j, m - 1 - j) for j in range(n)]
    keep = [j for j in range(n)] + [m - 1 - j for j in range(n)]
    P = np.zeros((m, m))
    k = 0
    for j in range(n):
        P[k, j] = 1.0
        k += 1
    for j in range(n):
        P[k, m - 1 - j] = 1.0
        k += 1
    B = P @ A @ P.T
    return B, P


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
    out = build(rc, zs, N=N)
    np.set_printoptions(precision=4, suppress=True, linewidth=200)
    print('=== n=%d R=%g mode=%s N=%d lam_n=%.6f lam_np1=%.6f D=%.6f c_r=%.6e ==='
          % (n, R, mode, N, out['lam_n'], out['lam_np1'], out['D'], out['r']))
    err = np.max(np.abs(out['Kp'] - out['Kp_fd']))
    print('P1 collapsed Kp vs FD: err=%.3e rel=%.3e'
          % (err, err / max(np.max(np.abs(out['Kp_fd'])), 1e-300)))
    err2 = np.max(np.abs(out['S'] - out['S2']))
    print('P2 S decomposition: err=%.3e' % err2)
    err2b = np.max(np.abs(out['Kp2'] - out['Kp_fd']))
    print('P2b expanded Kp2 vs FD: err=%.3e rel=%.3e'
          % (err2b, err2b / max(np.max(np.abs(out['Kp_fd'])), 1e-300)))
    print('P3 eig(S)      =', np.round(np.linalg.eigvalsh(out['S']), 4))
    print('   eig(Delta)  =', np.round(np.linalg.eigvalsh(out['Delta']), 4))
    print('   eig(T)      =', np.round(np.linalg.eigvalsh(out['T']), 4))
    print('   eig(epsTeps)=', np.round(np.linalg.eigvalsh(out['epsTeps']), 4))
    print('   eig(Kp_t)   =', np.round(np.linalg.eigvalsh(out['Kp_t']), 4))
    print('   eig(Kp_fd scaled) =',
          np.round(np.linalg.eigvalsh(np.diag(1.0 / out['v']) @ out['Kp_fd']
                                      @ np.diag(1.0 / out['v'])), 4))
    B, P = mirror_blocks(out)
    print('P4 mirror Kp_t (upper-left n x n = L-L, lower-right = R-R):')
    print(np.round(B, 4))
    print('   eig(mirror blocks):', np.round(np.linalg.eigvalsh(B), 4))
    # P5: cross-parity closed form with Sigma_+ low/high split
    m = 2 * n
    ss = roots_of(rc.blocks_from_z(zs), N + 1)
    edges = out['edges']
    eps = out['eps']
    u_n = out['u_n']
    lam_n, lam_np1 = out['lam_n'], out['lam_np1']
    D = out['D']
    SigLow = np.zeros((m, m))
    SigHigh = np.zeros((m, m))
    for l in range(N + 1):
        if l in (n - 1, n):
            continue
        ul = eigfun(rc.blocks_from_z(zs), ss[l], edges)
        lam_l = ss[l] ** 2
        if l < n - 1:
            b = lam_n / (lam_l - lam_n) + lam_np1 / (lam_l - lam_np1)
            SigLow += b * np.outer(ul, ul)
        else:
            b = lam_n / (lam_l - lam_n) + lam_np1 / (lam_l - lam_np1)
            SigHigh += b * np.outer(ul, ul)
    # cross-parity off-diagonal of Kp from the closed form:
    # Kp_ij = -(2 lam_n/lam_np1) u_i u_j Sigma_+(x_i,x_j)
    #         + 4 lam_n u_i^2 u_j^2 (lam_np1^2 - lam_n lam_np1 + lam_n^2)/(lam_np1^2 D)
    Kp_cross = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            if i == j or eps[i] == eps[j]:
                continue
            Kp_cross[i, j] = (-(2.0 * lam_n / lam_np1) * u_n[i] * u_n[j] * (SigLow[i, j] + SigHigh[i, j])
                + 4.0 * lam_n * u_n[i] ** 2 * u_n[j] ** 2 * (lam_np1 ** 2 - lam_n * lam_np1 + lam_n ** 2) / (lam_np1 ** 2 * D))
    err3 = np.max(np.abs(Kp_cross - (out['Kp'] - np.diag(np.diag(out['Kp']))) * (1 - np.eye(m))))
    cmask = np.zeros((m, m), bool)
    for i in range(m):
        for j in range(m):
            cmask[i, j] = (i != j and eps[i] != eps[j])
    Koff = out['Kp'] - np.diag(np.diag(out['Kp']))
    err3 = np.max(np.abs((Kp_cross - Koff) * cmask))
    print('P5 cross-parity closed form vs Kp off-diag (cross mask): err=%.3e' % err3)
    print('   SigLow eig (cross block):', np.round(np.linalg.eigvalsh(SigLow), 4))
    print('   SigHigh eig (cross block):', np.round(np.linalg.eigvalsh(SigHigh), 4))

    # P6: piecewise definiteness in the u-scaled frame
    u_n = out['u_n']; v = out['v']; eps = out['eps']; d = out['d']
    lam_n = out['lam_n']; lam_np1 = out['lam_np1']; D = out['D']
    Delta = out['Delta']; epsTeps = out['epsTeps']
    invu = 1.0 / u_n
    Dt = np.diag(invu) @ Delta @ np.diag(invu)
    Tt = np.diag(invu) @ epsTeps @ np.diag(invu)
    B1 = np.diag(d / (v * v)) + 2.0 * lam_n * Dt
    B2 = B1 + 2.0 * lam_n * D * Tt
    c2 = lam_n / lam_np1
    B3 = (B2 + (out['r'] - 2.0 * lam_n * c2 / D) * np.outer(np.ones(m), np.ones(m))
          - (2.0 * lam_n / D) * np.diag(eps) @ np.outer(np.ones(m), np.ones(m)) @ np.diag(eps))
    print('P6 eig(B1)=diag(d/v^2)+2lam_n*Dtilde:', np.round(np.linalg.eigvalsh(B1), 4))
    print('   eig(B2)=B1+2lam_n*D*Ttilde   :', np.round(np.linalg.eigvalsh(B2), 4))
    print('   eig(B3)=B2+rank terms       :', np.round(np.linalg.eigvalsh(B3), 4))
    print('   eig(Kp_t) reference          :', np.round(np.linalg.eigvalsh(out['Kp_t']), 4))
    print('   rank coeff r-2lam_n*c2/D = %.6e,  -2lam_n/D = %.6e'
          % (out['r'] - 2.0 * lam_n * c2 / D, -2.0 * lam_n / D))


if __name__ == '__main__':
    main()
