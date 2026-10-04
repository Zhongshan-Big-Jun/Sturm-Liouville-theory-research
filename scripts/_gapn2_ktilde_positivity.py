# -*- coding: utf-8 -*-
"""Sweep (EVIDENCE) the sign structure of the closed-form decomposition of K at
band-consistent points:

  Kp = SKS = D_f + E + H, S=diag(eps),
  E = c_1 w w^T + c_2' (eps w)(eps w)^T  (rank 2, closed form),
  H = (2 lam_n/lam_{n+1}) diag(u_n) K~ diag(u_n),
  K~_ij = Sigma'(x_i,x_j)  (eps_i = eps_j),  -Sigma_+(x_i,x_j)  (eps_i != eps_j).

Patterns probed on n in {2,3,4}, SUP/INF, R in a ladder up to the reachable
range (continuation in R from the op03 table seed):
  (P1) K~_ij > 0 for all pairs (entrywise positivity of the Green sign matrix);
  (P2) spectra of G_n^mat = diag(u_n) G~_n diag(u_n) and
       G_{n+1}^mat = diag(eps u_n) G~_{n+1} diag(eps u_n);
  (P3) raw K mirror-sector spectra (even/odd); Kp sectors are returned separately;
  (P4) total rank-1 coefficients rho_+ (same-eps) and rho_- (cross-eps):
       rho_+ = -beta + 2 lam_n/(D lam_{n+1}^2) + 2/(lam_n D)  (numerically > 0),
       rho_- = -alpha - 2 lam_n/(D lam_{n+1}^2) - 2/(lam_n D)  (numerically < 0),
       so the pole part alone has the H-sign pattern (+ same-eps, - cross-eps).

All output is EVIDENCE unless a STRICT tag is printed.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _sl_spectral_identity import positive_count, spectrum_for, spectral_denominators


def run(n, mode, R, zs, N=150):
    rcR = Recon(n, R, mode)
    rcR.require_stationary(zs)
    if rcR.R <= 1:
        raise ValueError('stationary K requires R>1')
    ed = eigen_data(rcR, zs)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    D = lam_np1 - lam_n
    edges = ed['edges']
    u_n, u_np1 = ed['u_n'], ed['u_np1']
    c, eps, W = ed['c'], ed['eps'], ed['W']
    m = 2 * n
    wj = lam_n * u_n ** 2
    blocks = rcR.blocks_from_z(zs)
    Count = positive_count(N, 'spectral truncation N') + 1
    Table = spectrum_for(blocks, 'D', Count)
    lam_all, KeepN, DenN = spectral_denominators(Table, lam_n, Count, PoleMode=n)
    _, KeepP, DenP = spectral_denominators(Table, lam_np1, Count, PoleMode=n+1)
    ss = Table.frequency_prefix(Count)
    U = np.zeros((Count, m))
    for l in range(Count):
        U[l] = eigfun(blocks, ss[l], edges)
    wgt_n, wgt_np1, wgt_s1, wgt_s2 = [np.zeros(Count) for _ in range(4)]
    KeepBoth = KeepN & KeepP
    with np.errstate(over='raise', divide='raise', invalid='raise'):
        wgt_n[KeepN] = 1.0 / DenN
        wgt_np1[KeepP] = 1.0 / DenP
        wgt_s1[KeepBoth] = lam_all[KeepBoth]*D / ((lam_all[KeepBoth]-lam_np1)*(lam_all[KeepBoth]-lam_n))
        wgt_s2[KeepBoth] = lam_n/(lam_all[KeepBoth]-lam_n) + lam_np1/(lam_all[KeepBoth]-lam_np1)
    if not all(np.all(np.isfinite(Values)) for Values in (U, wgt_n, wgt_np1, wgt_s1, wgt_s2)):
        raise ArithmeticError('stationary spectral assembly is not finite')
    Gn = U.T @ np.diag(wgt_n) @ U
    Gnp1 = U.T @ np.diag(wgt_np1) @ U
    S1 = U.T @ np.diag(wgt_s1) @ U
    S2 = U.T @ np.diag(wgt_s2) @ U
    eij = np.outer(eps, eps)
    same = (eij > 0)
    Ktilde = np.where(same, S1, -S2)
    H = (2.0 * lam_n / lam_np1) * np.diag(u_n) @ Ktilde @ np.diag(u_n)
    sigma = 1.0 if mode == 'sup' else -1.0
    Df = np.diag(sigma * 2.0 * c * np.abs(W) / (R - 1.0))
    beta = 4.0 / (D * lam_np1)
    alpha = 4.0 * (lam_np1 ** 2 - lam_n * lam_np1 + lam_n ** 2) / (lam_n * lam_np1 * D * lam_np1)
    E = np.where(same, -beta * np.outer(wj, wj), alpha * np.outer(wj, wj))
    Kp = Df + E + H
    S = np.diag(eps)
    K = S @ Kp @ S
    rho_p = -beta + 2.0 * lam_n / (D * lam_np1 ** 2) + 2.0 / (lam_n * D)
    rho_m = -alpha - 2.0 * lam_n / (D * lam_np1 ** 2) - 2.0 / (lam_n * D)
    Gn_mat = np.diag(u_n) @ Gn @ np.diag(u_n)
    Gnp1_mat = np.diag(eps * u_n) @ Gnp1 @ np.diag(eps * u_n)
    Be = np.zeros((m, n)); Bo = np.zeros((m, n))
    for j in range(n):
        Be[j, j] = Be[m - 1 - j, j] = 1.0 / np.sqrt(2.0)
        Bo[j, j] = 1.0 / np.sqrt(2.0); Bo[m - 1 - j, j] = -1.0 / np.sqrt(2.0)
    Ke = Be.T @ K @ Be
    Ko = Bo.T @ K @ Bo
    KpEven = Be.T @ Kp @ Be
    KpOdd = Bo.T @ Kp @ Bo
    return dict(min_ktilde=Ktilde.min(), min_S1_same=S1[same].min(), max_S2_cross=S2[~same].max(),
                rho_p=rho_p, rho_m=rho_m,
                evKe=np.linalg.eigvalsh(Ke), evKo=np.linalg.eigvalsh(Ko),
                evKpEven=np.linalg.eigvalsh(KpEven), evKpOdd=np.linalg.eigvalsh(KpOdd),
                evGn=np.linalg.eigvalsh(Gn_mat), evGnp1=np.linalg.eigvalsh(Gnp1_mat),
                detK=np.linalg.det(K), min_diagK=np.diag(K).min())


def main():
    ns = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3, 4]
    Rs = [float(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else \
        [1.2, 2.0, 4.0, 10.0, 30.0, 75.0, 100.0]
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for n in ns:
        for mode in ('sup', 'inf'):
            rc0 = Recon(n, R=4.0, mode=mode)
            key = f"n{n}_{mode.upper()}"
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc0.widths_to_z(w0)
            prev = z0
            for R in Rs:
                global rcR
                rcR = Recon(n, R, mode)
                zs = symmetric_root(rcR, prev)
                if zs is None:
                    print(f"n={n} {mode} R={R}: no root (continuation stops)", flush=True)
                    break
                prev = zs
                try:
                    d = run(n, mode, R, zs)
                except Exception as ex:
                    print(f"n={n} {mode} R={R}: EXC {ex}", flush=True)
                    break
                print(f"n={n} {mode:3s} R={R:6.2f}  min(K~)={d['min_ktilde']:+.4e}  "
                      f"min S1[same]={d['min_S1_same']:+.4e}  max S2[cross]={d['max_S2_cross']:+.4e}  "
                      f"rho_+={d['rho_p']:+.3e}  rho_-={d['rho_m']:+.3e}", flush=True)
                print(f"     evKe={np.round(d['evKe'],4)}  evKo={np.round(d['evKo'],4)}  "
                      f"detK={d['detK']:+.3e}  min diagK={d['min_diagK']:+.4e}")
                print(f"     ev(Gn_mat)={np.round(d['evGn'],4)}  ev(Gnp1_mat)={np.round(d['evGnp1'],4)}")


if __name__ == '__main__':
    main()
