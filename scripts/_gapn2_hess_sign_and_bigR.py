# -*- coding: utf-8 -*-
"""Probe: (1) verify Hess(D_n) = +/- diag(s) * lambda_{n+1} * J at band-consistent
points against an FD Hessian (settles the sign convention of A3); (2) extended-R
margin scan R in {30, 100} for the K+-/K-- spectra (INF n=2..4, SUP n=2..3).

All output is EVIDENCE.
"""
import sys
import json
import time
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_hp_scan import analytic_jacobian_hp


def hess_fd(rc, z, h=1e-5):
    """FD Hessian of D = lambda_{n+1} - lambda_n in the free-width coordinates,
    then pushed to edge coordinates (same convention as jac_fd)."""
    m = 2 * rc.n
    w = rc.z_to_widths(z)
    u = w[:m]
    def D_of(uu):
        ww = np.concatenate([uu, [1.0 - np.sum(uu)]])
        zz = rc.widths_to_z(ww)
        blocks = rc.blocks_from_z(zz)
        from _gapn2_symmetry_recon import roots_of
        ss = roots_of(blocks, rc.n + 1)
        return ss[rc.n] ** 2 - ss[rc.n - 1] ** 2
    H = np.zeros((m, m))
    for a in range(m):
        for b in range(m):
            up, um = u.copy(), u.copy()
            up[a] += h; um[a] -= h
            vpp = up.copy(); vpm = up.copy(); vmp = um.copy(); vmm = um.copy()
            vpp[b] += h; vpm[b] -= h; vmp[b] += h; vmm[b] -= h
            H[a, b] = (D_of(vpp) - D_of(vpm) - D_of(vmp) + D_of(vmm)) / (4 * h * h)
    L = np.tril(np.ones((m, m)))
    return np.linalg.inv(L).T @ H @ np.linalg.inv(L)


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    # ---- (1) Hess sign check at n=2, R=4, both modes ----
    for mode in ('inf', 'sup'):
        rc = Recon(2, R=4.0, mode=mode)
        e0 = np.array(tab[f'n2_{mode.upper()}']['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        zs = symmetric_root(rc, rc.widths_to_z(w0))
        ed = eigen_data(rc, zs)
        lam = ed['lam_np1']
        J = analytic_jacobian_hp(rc, zs, N=400)
        s = np.array([rc.pat[i + 1] - rc.pat[i] for i in range(4)])
        Hfd = hess_fd(rc, zs)
        for sign, name in ((1.0, 'H = +diag(s) lam J'), (-1.0, 'H = -diag(s) lam J')):
            H = sign * np.diag(s) * lam * J
            print(f"[{mode}] {name}: err={np.max(np.abs(H - Hfd)):.2e}")
        evH = np.linalg.eigvalsh(Hfd)
        print(f"[{mode}] FD Hess eigenvalues: {np.round(evH, 4)}")
    # ---- (2) extended-R margins ----
    for mode, ns in (('inf', [2, 3, 4]), ('sup', [2, 3])):
        for n in ns:
            rc0 = Recon(n, R=4.0, mode=mode)
            key = f"n{n}_{mode.upper()}"
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc0.widths_to_z(w0)
            prev = None
            for R in (30.0, 100.0):
                rcR = Recon(n, R, mode)
                z = z0 if prev is None else prev
                t0 = time.time()
                zs = symmetric_root(rcR, z)
                if zs is None:
                    zs = symmetric_root(rcR, z0)
                if zs is None:
                    print(f"[{mode} n={n} R={R}]: no root"); continue
                prev = zs
                res = np.max(np.abs(rcR.residual(zs)))
                J = analytic_jacobian_hp(rcR, zs, N=400)
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                K = np.diag(1.0 / s) @ J
                # sym/anti blocks
                S = np.zeros((2 * n, 2 * n))
                for j in range(n):
                    S[j, j] = 1.0; S[j, 2 * n - 1 - j] = 1.0
                    S[n + j, j] = 1.0; S[n + j, 2 * n - 1 - j] = -1.0
                M2 = S @ K @ np.linalg.inv(S)
                evp = np.sort(np.linalg.eigvalsh(M2[:n, :n]))
                evm = np.sort(np.linalg.eigvalsh(M2[n:, n:]))
                margin = min(np.min(np.abs(evp)), np.min(np.abs(evm)))
                print(f"[{mode} n={n} R={R:5.0f}] res={res:.1e} detJ={np.linalg.det(J):+.3e} "
                      f"margin={margin:.3e} evK+={np.round(evp,4)} evK-={np.round(evm,4)} "
                      f"t={time.time()-t0:.0f}s", flush=True)


if __name__ == '__main__':
    main()
