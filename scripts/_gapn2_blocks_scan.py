# -*- coding: utf-8 -*-
"""Check the sym/anti block structure of K (and J) along the symmetric branch.

K = -Hess/(R-1)^2 is symmetric and commutes with P; in (sym, anti) coordinates
K = [[K+, 0], [0, K-]].  If spec(K+) == spec(K-) exactly, then det K = (det K+)^2
and (G1') reduces to det K+ != 0 (sign automatic).  Also report det C, det D
(the cross blocks of J in sym/anti coordinates, with det J = (-1)^n det C det D).
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import analytic_jacobian_spectral
from _gapn2_jacobian_analytic import eigen_data


def sym_anti_blocks(M, n):
    """M in x-coords -> (M++, M--, M+-, M-+) blocks in (sym, anti) coords.
    sym_j = x_j + x_{2n-1-j} - 1, anti_j = x_j - x_{2n-1-j}."""
    S = np.zeros((2 * n, 2 * n))
    for j in range(n):
        S[j, j] = 1.0; S[j, 2 * n - 1 - j] = 1.0
        S[n + j, j] = 1.0; S[n + j, 2 * n - 1 - j] = -1.0
    T = np.linalg.inv(S)
    M2 = S @ M @ T
    return M2[:n, :n], M2[n:, n:], M2[:n, n:], M2[n:, :n]


def main():
    ns = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3, 4]
    Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.05, 2.0, 4.0, 10.0]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))

    for n in ns:
        for m in (['sup', 'inf'] if mode == 'both' else [mode]):
            rc0 = Recon(n, R=4.0, mode=m)
            key = f"n{n}_{m.upper()}"
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc0.widths_to_z(w0)
            prev = None
            print(f"\n===== n={n} mode={m} =====")
            for R in Rs:
                rcR = Recon(n, R, m)
                z = z0 if prev is None else prev
                zs = symmetric_root(rcR, z)
                if zs is None:
                    print(f"R={R}: not found"); continue
                prev = zs
                J = analytic_jacobian_spectral(rcR, zs, N=N)
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                K = -np.diag(1.0 / s) @ J  # = Hess/(lam (R-1)^2) up to scaling; use Hess-like
                # K = lam * diag(s)^{-1} J = -Hess/(R-1)^2 ; scale-free version:
                K2 = np.diag(1.0 / s) @ J
                Kpp, Kmm, Kpm, Kmp = sym_anti_blocks(K2, n)
                Jpp, Jmm, Jpm, Jmp = sym_anti_blocks(J, n)
                evp = np.sort(np.linalg.eigvalsh(Kpp))
                evm = np.sort(np.linalg.eigvalsh(Kmm))
                ev_all = np.linalg.eigvalsh(K2)
                print(f"R={R:6.3g}: crossK={np.max(np.abs(Kpm)):.1e} crossJ={np.max(np.abs(Jpp))+np.max(np.abs(Jmm)):.1e} "
                      f"evK+={np.round(evp,4)} evK-={np.round(evm,4)} "
                      f"detK={np.linalg.det(K2):+.3e} detKp={np.linalg.det(Kpp):+.3e} "
                      f"detKm={np.linalg.det(Kmm):+.3e} detC={np.linalg.det(Jpm):+.3e} "
                      f"detD={np.linalg.det(Jmp):+.3e} detJ={np.linalg.det(J):+.3e}")


if __name__ == '__main__':
    main()
