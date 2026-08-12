# -*- coding: utf-8 -*-
"""Probe: Jacobian structure of the band self-consistency system along the
R-continuation curve for n=2 (SUP/INF).  At the symmetric root, the 4x4
Jacobian (in coordinates x1..x4) commutes with reflection; we decompose it
into the symmetric block A (2x2, on (x1+x4, x2+x3) directions) and the
anti-symmetric block B (2x2, on (x1-x4, x2-x3) directions) and report dets.

Also verifies the R=1 explicit zero set of f (closed form) and det J = prod f'(x_j).
"""
import sys, json
import numpy as np
sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of

def jac_fd(rc, z, h=1e-6):
    """FD Jacobian of the residual in edge coordinates x (2n x 2n)."""
    m = 2 * rc.n
    w = rc.z_to_widths(z)
    u = w[:m]  # free widths; last width = 1 - sum(u)
    Ju = np.zeros((m, m))
    for k in range(m):
        up = u.copy(); um = u.copy()
        up[k] += h; um[k] -= h
        wp = np.concatenate([up, [1.0 - np.sum(up)]]); wm = np.concatenate([um, [1.0 - np.sum(um)]])
        Ju[:, k] = (rc.residual(rc.widths_to_z(wp)) - rc.residual(rc.widths_to_z(wm))) / (2 * h)
    # edges = L u with L = lower-triangular ones (m x m); Jx = Ju @ inv(L)
    L = np.tril(np.ones((m, m)))
    return Ju @ np.linalg.inv(L)

def sym_antisym_decomp(J, n):
    """J is 2n x 2n in x-space.  Return (A, B) in (sym, anti) coordinates."""
    # sym coords: s_j = x_j + x_{2n+1-j} - 1 ; anti: a_j = x_j - x_{2n+1-j}
    S = np.zeros((2 * n, 2 * n))
    for j in range(n):
        S[j, j] = 1.0; S[j, 2 * n - 1 - j] = 1.0
        S[n + j, j] = 1.0; S[n + j, 2 * n - 1 - j] = -1.0
    T = np.linalg.inv(S)
    M = S @ J @ T
    return M[:n, :n], M[n:, n:]

def symmetric_root(rc, z_seed, max_nfev=300):
    """solve the symmetric 2-param system: enforce x3=1-x2, x4=1-x1 by symmetry of widths."""
    from scipy.optimize import least_squares
    n = rc.n
    def res_sym(z):
        # project z onto symmetric widths: w_i = w_{nb-1-i}
        w = rc.z_to_widths(z)
        ws = 0.5 * (w + w[::-1])
        zs = rc.widths_to_z(ws)
        return rc.residual(zs)
    r = least_squares(res_sym, z_seed, xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=max_nfev)
    if np.max(np.abs(r.fun)) > 1e-8:
        return None
    w = rc.z_to_widths(r.x)
    ws = 0.5 * (w + w[::-1])
    z = rc.widths_to_z(ws)
    return z

def main():
    Rs = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [1.05, 1.2, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 20.0, 50.0]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        rc = Recon(n, R=4.0, mode=m)
        # seed from table (R=4) or from a R=10 recon file
        key = f"n{n}_{m.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc.widths_to_z(w0)
        print(f"=== n={n} mode={m} ===")
        prev = None
        for R in Rs:
            rcR = Recon(n, R, m)
            if prev is None:
                z = z0
            else:
                z = prev
            zs = symmetric_root(rcR, z)
            if zs is None:
                print(f"  R={R}: symmetric root NOT found from seed")
                continue
            rep = rcR.full_report(zs)
            Jx = jac_fd(rcR, zs)
            A, B = sym_antisym_decomp(Jx, n)
            detA = np.linalg.det(A); detB = np.linalg.det(B); detJ = np.linalg.det(Jx)
            print(f"  R={R}: D={rep['D']:.6f} edges={[round(e,6) for e in rep['edges']]} "
                  f"res={rep['res_max']:.1e} band={rep['band_ok']}")
            print(f"       det A={detA:+.4e} det B={detB:+.4e} det J={detJ:+.4e}")
            prev = zs

if __name__ == '__main__':
    main()
