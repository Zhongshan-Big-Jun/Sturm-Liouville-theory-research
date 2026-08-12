# -*- coding: utf-8 -*-
"""Probe (EVIDENCE): is K = diag(1/s) J an H-matrix along the symmetric branch?

An H-matrix (with all |K_ii| > 0) admits a positive diagonal scaling making it
strictly diagonally dominant, which by Perron-Frobenius is equivalent to
rho(B) < 1, B = D_K^{-1} |K_off|, D_K = diag(|K_ii|).  If K is an H-matrix and
all diagonal entries have one sign, then det K has that sign (det(I-B) > 0),
which would close (G1') once H-matrix-ness is proved analytically.

Also prints the sign pattern of K and of its symmetric/antisymmetric blocks.
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd


def sym_blocks(K):
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
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                Jfd = jac_fd(rcR, zs)
                K = np.diag(1.0 / s) @ Jfd
                dk = np.abs(np.diag(K))
                B = np.abs(K - np.diag(np.diag(K))) / dk[:, None]
                rho = np.max(np.abs(np.linalg.eigvals(B)))
                # H-matrix scaling d: solve (I - B) d = 1 (if invertible)
                try:
                    d = np.linalg.solve(np.eye(2 * n) - B, np.ones(2 * n))
                    d_ok = np.all(d > 0)
                except np.linalg.LinAlgError:
                    d = None; d_ok = False
                Kp, Km_ = sym_blocks(K)
                print(f"n={n} {mode:3s} R={R:5.2f}  rho(B)={rho:.4f}  H-matrix={rho < 1}  "
                      f"scaling d>0: {d_ok}" + (f"  d range=[{d.min():.3e},{d.max():.3e}]" if d_ok else ""))
                if R in (4.0, 10.0):
                    print(f"     sgn K =\n{np.sign(K)}")
                    print(f"     sgn K+ =\n{np.sign(Kp)}")
                    print(f"     sgn K- =\n{np.sign(Km_)}")


if __name__ == '__main__':
    main()
