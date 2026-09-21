# -*- coding: utf-8 -*-
"""O-3 scan: det A, det B, det J, det K, K-eigenvalues, Hessian spectra along the
symmetric branches, n = 2..5, R grid, SUP/INF, using the analytic Jacobian.

Structural checks:
  (S1) s_j * eps_j = +(R-1) for all switches j and both modes (needed for the
       symmetrization below).
  (S2) K := lam_np1 * diag(s)^{-1} * J is SYMMETRIC.
  (S3) K has positive diagonal.
  (G1') det J != 0 with sign (-1)^n  <=>  det K > 0 (K symmetric).
  (O5) det B != 0 (anti block in x-coords and in K-coords).
"""
import sys
import json
import time
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import jac_fd, sym_antisym_decomp, symmetric_root
from _gapn2_jacobian_spectral import analytic_jacobian_spectral, gtilde_spectral
from _gapn2_jacobian_analytic import eigen_data


def main():
    ns = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [2, 3, 4, 5]
    Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else \
        [1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0]
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
            # continuation: descend from R=4 to 1.05, then jump and ascend to 100
            prev = None
            first = True
            print(f"\n===== n={n} mode={m} =====")
            for R in Rs:
                rcR = Recon(n, R, m)
                z = z0 if first else prev
                zs = symmetric_root(rcR, z)
                if zs is None:
                    # retry from table seed
                    zs = symmetric_root(rcR, z0)
                if zs is None:
                    print(f"R={R:8.4g}: root NOT found")
                    continue
                prev = zs
                first = False
                ed = eigen_data(rcR, zs)
                lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
                u_n, u_np1 = ed['u_n'], ed['u_np1']
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                eps = np.sign(u_np1 / u_n)
                se = s * eps
                t0 = time.time()
                J = analytic_jacobian_spectral(rcR, zs, N=N)
                K = lam_np1 * np.diag(1.0 / s) @ J
                Ksym_err = np.max(np.abs(K - K.T))
                A, B = sym_antisym_decomp(J, n)
                detJ = np.linalg.det(J)
                detA = np.linalg.det(A)
                detB = np.linalg.det(B)
                detK = np.linalg.det(K)
                evK = np.linalg.eigvalsh(K)
                evH = np.linalg.eigvalsh(-np.diag(s) * lam_np1 * J)  # Hessian
                diagK = np.diag(K)
                sign_ok = (np.sign(detJ) == ((-1) ** n)) if abs(detJ) > 0 else False
                print(f"R={R:8.4g} D={ed['lam_np1']-ed['lam_n']:12.6f} "
                      f"se={se[0]:+.1f} Ksym={Ksym_err:.1e} "
                      f"detJ={detJ:+.3e}(sgn(-1)^n={sign_ok}) detK={detK:+.3e} "
                      f"detA={detA:+.3e} detB={detB:+.3e} "
                      f"minK={evK.min():+.3e} maxK={evK.max():+.3e} "
                      f"minHess={evH.min():+.3e} maxHess={evH.max():+.3e} "
                      f"minDiagK={diagK.min():+.3e} t={time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
