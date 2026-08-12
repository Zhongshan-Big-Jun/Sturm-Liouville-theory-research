# -*- coding: utf-8 -*-
"""Debug: roots_of stability, gtilde_spectral divide-by-zero, FH lambda FD."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_spectral import gtilde_spectral

np.set_printoptions(precision=8, suppress=True, linewidth=180)


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
    blocks = rc.blocks_from_z(zs)
    w = rc.z_to_widths(zs)
    edges = np.cumsum(w)[:-1]
    ss = roots_of(blocks, n + 1)
    lam_n, lam_np1 = ss[n - 1] ** 2, ss[n] ** 2
    print(f"lam_n={lam_n:.10f} lam_np1={lam_np1:.10f}")

    # --- 1. check ss monotonicity and distinctness (n+1 roots) ---
    print("ss (first 5):", np.round(ss[:5], 8))
    print("diffs:", np.round(np.diff(ss), 8))

    # --- 2. gtilde_spectral: find min |ss[l]^2 - lam| for l != k ---
    for k_idx, lamk in ((0, lam_n), (1, lam_np1)):
        ssN = roots_of(blocks, 2000 + 1)
        print(f"len(ssN)={len(ssN)}")
        d = np.abs(ssN ** 2 - lamk)
        d[k_idx] = np.inf
        j = np.argmin(d)
        print(f"k={k_idx}: min |ss[l]^2-lam| at l={j}: {d[j]:.3e}, ss[{j}]^2={ssN[j]**2:.10f}")

    # --- 3. FH lambda FD directly with raw width perturbation ---
    h = 1e-6
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    for k_idx, (tag, lamk) in enumerate((("n", lam_n), ("n+1", lam_np1))):
        uk = eigfun(blocks, ss[k_idx], edges)
        for i in range(2 * n):
            wplus = w.copy(); wminus = w.copy()
            wplus[i] -= h; wplus[i + 1] += h
            wminus[i] += h; wminus[i + 1] -= h
            bplus = rc.blocks_from_z(rc.widths_to_z(wplus))
            bminus = rc.blocks_from_z(rc.widths_to_z(wminus))
            ssp = roots_of(bplus, n + 1); ssm = roots_of(bminus, n + 1)
            lam_fd = (ssp[k_idx] ** 2 - ssm[k_idx] ** 2) / (2 * h)
            dlam_th = -lamk * s[i] * uk[i] ** 2
            print(f"k={tag} i={i}: fd={lam_fd:+.8e} th={dlam_th:+.8e} ratio={lam_fd/dlam_th:.6f}")


if __name__ == '__main__':
    main()
