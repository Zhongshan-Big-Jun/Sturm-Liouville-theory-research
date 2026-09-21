# -*- coding: utf-8 -*-
"""High-precision det K+ / det K- along branches with Richardson-accelerated G~.

G~(N) = G~_true + c/N: two-point extrapolation G~_ext = 2 G~(2N) - G~(N).
Tighter root tolerance (res < 1e-13) and adaptive R stepping.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import gtilde_spectral
from _gapn2_jacobian_analytic import eigen_data


def gtilde_richardson(rc, z, lam, k, edges, N=2000):
    G1 = gtilde_spectral(rc, z, lam, k, edges, N=N)
    G2 = gtilde_spectral(rc, z, lam, k, edges, N=2 * N)
    return 2.0 * G2 - G1


def analytic_jacobian_hp(rc, z, N=2000):
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
    Gn = gtilde_richardson(rc, z, lam_n, n - 1, edges, N=N)
    Gnp1 = gtilde_richardson(rc, z, lam_np1, n, edges, N=N)
    M = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            term = (2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1)
                    - 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j]
                    + 2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
            M[j, i] = s[i] * term
    return (np.diag(fprime) + M) / lam_np1


def sym_anti_blocks(M, n):
    S = np.zeros((2 * n, 2 * n))
    for j in range(n):
        S[j, j] = 1.0; S[j, 2 * n - 1 - j] = 1.0
        S[n + j, j] = 1.0; S[n + j, 2 * n - 1 - j] = -1.0
    T = np.linalg.inv(S)
    M2 = S @ M @ T
    return M2[:n, :n], M2[n:, n:]


def main():
    ns = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [3]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'inf'
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    # order: descend 4 -> 1.1 first (good continuation), then 1.05 from 1.1
    Rgrid = [4.0, 3.0, 2.5, 2.0, 1.5, 1.3, 1.2, 1.1, 1.05, 5.0, 6.0, 8.0, 10.0]
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for n in ns:
        rc0 = Recon(n, R=4.0, mode=mode)
        key = f"n{n}_{mode.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc0.widths_to_z(w0)
        prev = None
        print(f"===== n={n} mode={mode} N={N} (Richardson) =====")
        for R in Rgrid:
            rcR = Recon(n, R, mode)
            z = z0 if prev is None else prev
            zs = symmetric_root(rcR, z)
            if zs is None:
                zs = symmetric_root(rcR, z0)
            if zs is None:
                print(f"R={R:6.3g}: root NOT found")
                continue
            prev = zs
            res = np.max(np.abs(rcR.residual(zs)))
            J = analytic_jacobian_hp(rcR, zs, N=N)
            s = np.array([rcR.pat[i + 1] - rcR.pat[i] for i in range(2 * n)])
            K2 = np.diag(1.0 / s) @ J
            Kpp, Kmm = sym_anti_blocks(K2, n)
            dKp = np.linalg.det(Kpp)
            dKm = np.linalg.det(Kmm)
            dJ = np.linalg.det(J)
            evp = np.sort(np.linalg.eigvalsh(Kpp))
            evm = np.sort(np.linalg.eigvalsh(Kmm))
            print(f"R={R:6.3g} res={res:.1e} detJ={dJ:+.3e} detK+={dKp:+.3e} "
                  f"detK-={dKm:+.3e} evK+={np.round(evp,6)} evK-={np.round(evm,6)}")


if __name__ == '__main__':
    main()
