# -*- coding: utf-8 -*-
"""Direct FD of the composed maps d(F.sigma) and d(sigma.F) at the symmetric point.

F(sigma x) vs sigma F(x): which sign?  Compare
  [F(x* - h*P*e_k) - F(x*)]/h      (derivative of F.sigma along e_k)
  [sigma F(x* + h e_k) - sigma F(x*)]/h   (derivative of sigma.F along e_k)
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root


def widths_from_edges(edges, nb):
    return np.diff(np.concatenate([[0.0], edges, [1.0]]))


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
    w = rc.z_to_widths(zs)
    edges = np.cumsum(w)[:-1]
    m = 2 * n
    P = np.zeros((m, m))
    for j in range(m):
        P[j, m - 1 - j] = 1.0
    h = 1e-6

    F0 = rc.residual(zs)
    for k in range(m):
        # d(F.sigma) along e_k: sigma(x* + h e_k) = x* - h P e_k = x* - h e_{m-1-k}
        jj = m - 1 - k
        wp = w.copy(); wm = w.copy()
        # move switch jj LEFT by h (block jj shrinks, block jj+1 grows)
        wp[jj] -= h; wp[jj + 1] += h
        Fp = rc.residual(rc.widths_to_z(wp))
        dFsig = (Fp - F0) / h
        # d(sigma.F) along e_k: sigma F(x* + h e_k): F at config with switch k moved RIGHT
        wq = w.copy()
        wq[k] += h; wq[k + 1] -= h
        Fq = rc.residual(rc.widths_to_z(wq))
        dSigF = -P @ (Fq - F0) / h
        print(f"k={k}: d(F.sigma) = {np.round(dFsig, 8)}")
        print(f"      d(sigma.F) = {np.round(dSigF, 8)}")
        print(f"      diff = {np.max(np.abs(dFsig - dSigF)):.2e}  sum = {np.max(np.abs(dFsig + dSigF)):.2e}")


if __name__ == '__main__':
    main()
