# -*- coding: utf-8 -*-
"""Rerun SUP big-R pivot check with R-ladder continuation (seed from each
previous R; the direct jump R=4 -> R>=30 fails and produced a spurious root
with alternating pivots at n=4, R=100)."""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd


def pivots(K):
    m = K.shape[0]
    piv = []
    A = K.copy()
    for k in range(m):
        if abs(A[k, k]) < 1e-300:
            return None
        piv.append(A[k, k])
        A[k + 1:, k + 1:] -= np.outer(A[k + 1:, k], A[k, k + 1:]) / A[k, k]
    return np.array(piv)


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    ladder = [4.0, 6.0, 10.0, 20.0, 30.0, 40.0, 50.0, 75.0, 100.0]
    plan = [
        (2, 'sup', [30.0, 50.0, 75.0, 100.0]),
        (3, 'sup', [30.0, 50.0, 75.0, 100.0]),
        (4, 'sup', [30.0, 50.0, 75.0, 100.0]),
        (4, 'inf', [40.0]),
    ]
    for n, mode, Rs in plan:
        rc0 = Recon(n, R=4.0, mode=mode)
        key = f"n{n}_{mode.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc0.widths_to_z(w0)
        prev = z0
        prevR = 4.0
        for R in ladder:
            if R < min(Rs):
                rcR = Recon(n, R, mode)
                zs = symmetric_root(rcR, prev)
                if zs is None:
                    print(f"ladder break at R={R}"); break
                prev = zs
            elif R in Rs:
                rcR = Recon(n, R, mode)
                zs = symmetric_root(rcR, prev)
                if zs is None:
                    print(f"n={n} {mode} R={R}: no root (ladder reached)"); prev = None; break
                prev = zs
                pat = rcR.pat
                s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
                Jfd = jac_fd(rcR, zs)
                K = np.diag(1.0 / s) @ Jfd
                piv = pivots(K)
                ev = np.linalg.eigvalsh(K)
                res = np.max(np.abs(rcR.residual(zs)))
                ps = 'ZERO PIVOT' if piv is None else ' '.join(f"{p:+.3e}" for p in piv)
                print(f"n={n} {mode:3s} R={R:5.0f} res={res:.1e} detK={np.linalg.det(K):+.3e} "
                      f"evK=[{ev.min():+.3e},{ev.max():+.3e}] pivots: {ps}", flush=True)


if __name__ == '__main__':
    main()
