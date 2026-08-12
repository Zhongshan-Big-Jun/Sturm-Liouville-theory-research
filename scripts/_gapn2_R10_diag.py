# -*- coding: utf-8 -*-
"""Diagnose the R=10 residual: N-dependence, difference matrix, term sizes."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import jac_fd, symmetric_root
from _gapn2_jacobian_spectral import analytic_jacobian_spectral

np.set_printoptions(precision=5, suppress=True, linewidth=180)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'inf'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)
    print(f"n={n} R={R} mode={mode}; res={np.max(np.abs(rc.residual(zs))):.2e}")
    Jfd = jac_fd(rc, zs)
    print("Jfd:")
    print(Jfd)
    for N in (500, 1000, 2000, 4000):
        J = analytic_jacobian_spectral(rc, zs, N=N)
        err = np.max(np.abs(J - Jfd))
        rel = err / np.max(np.abs(Jfd))
        print(f"N={N}: err={err:.3e} rel={rel:.3e}")
        if N == 2000:
            print("J - Jfd:")
            print(J - Jfd)


if __name__ == '__main__':
    main()
