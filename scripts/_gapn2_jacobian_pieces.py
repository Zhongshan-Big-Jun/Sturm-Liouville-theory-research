# -*- coding: utf-8 -*-
"""Term-by-term comparison of the analytic Jacobian pieces vs FD (spectral G~)."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import jac_fd, symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_spectral import gtilde_spectral

np.set_printoptions(precision=6, suppress=True, linewidth=180)


def pieces(rc, z, N=2000):
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
    Gn = gtilde_spectral(rc, z, lam_n, n - 1, edges, N=N)
    Gnp1 = gtilde_spectral(rc, z, lam_np1, n, edges, N=N)
    M1 = np.zeros((2 * n, 2 * n)); M2 = np.zeros((2 * n, 2 * n)); M3 = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            M1[j, i] = s[i] * (-2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1))
            M2[j, i] = s[i] * (2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j])
            M3[j, i] = s[i] * (-2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
    return dict(fprime=fprime, M1=M1, M2=M2, M3=M3, s=s, wj=wj, D=D, lam_n=lam_n, lam_np1=lam_np1)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'sup'
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = f"n{n}_{mode.upper()}"
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)
    Jfd = jac_fd(rc, zs)
    p = pieces(rc, zs, N)
    lam_np1 = p['lam_np1']
    Dp = np.diag(p['fprime']) / lam_np1
    print(f"n={n} R={R} mode={mode}; res={np.max(np.abs(rc.residual(zs))):.2e}; "
          f"lam_n={p['lam_n']:.4f} lam_np1={lam_np1:.4f}")

    print("\n--- Jfd (FD) ---")
    print(Jfd)
    for name, Mx in (("D~", Dp), ("M1", p['M1'] / lam_np1), ("M2", p['M2'] / lam_np1),
                     ("M3", p['M3'] / lam_np1), ("sum", (Dp + (p['M1'] + p['M2'] + p['M3']) / lam_np1))):
        print(f"--- {name} ---")
        print(Mx)
    A = (Dp + (p['M1'] + p['M2'] + p['M3']) / lam_np1)
    print("--- Jfd - A ---")
    print(Jfd - A)


if __name__ == '__main__':
    main()
