# -*- coding: utf-8 -*-
"""Check J P = P J (equivariance at the symmetric point) for Jfd and the analytic J."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import jac_fd, symmetric_root
from _gapn2_jacobian_spectral import analytic_jacobian_spectral

np.set_printoptions(precision=6, suppress=True, linewidth=180)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'sup'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)

    m = 2 * n
    P = np.zeros((m, m))
    for j in range(m):
        P[j, m - 1 - j] = 1.0

    Jfd = jac_fd(rc, zs)
    J = analytic_jacobian_spectral(rc, zs, N=1500)

    for name, Jx in (("Jfd", Jfd), ("Janalytic", J)):
        comm = np.max(np.abs(Jx @ P - P @ Jx))
        print(f"{name}: max|JP - PJ| = {comm:.3e}")
        if name == "Jfd":
            print("Jfd:")
            print(Jfd)
        else:
            print("Janalytic:")
            print(Jx)


if __name__ == '__main__':
    main()
