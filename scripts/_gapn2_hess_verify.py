# -*- coding: utf-8 -*-
"""Focused sign/structure checks (EVIDENCE):

(1) dD/dx_j = s_j * f(x_j) at band-consistent points (FD gradient in edge coords).
(2) Hess(D) vs lambda * diag(s) * J  (both orders: J and J^T) at h=1e-3.
(3) analytic J vs FD residual Jacobian jac_fd at N=400 (Richardson).
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_hp_scan import analytic_jacobian_hp


def D_edges(rc, e):
    """D = lambda_{n+1} - lambda_n as a function of the 2n edges."""
    w = np.diff(np.concatenate([[0.0], e, [1.0]]))
    blocks = rc.blocks_from_z(rc.widths_to_z(w))
    ss = roots_of(blocks, rc.n + 1)
    return ss[rc.n] ** 2 - ss[rc.n - 1] ** 2


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for mode in ('inf', 'sup'):
        rc = Recon(2, R=4.0, mode=mode)
        e0 = np.array(tab[f'n2_{mode.upper()}']['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        zs = symmetric_root(rc, rc.widths_to_z(w0))
        e = np.cumsum(rc.z_to_widths(zs))[:-1]
        ed = eigen_data(rc, zs)
        lam = ed['lam_np1']
        s = np.array([rc.pat[i + 1] - rc.pat[i] for i in range(4)])
        f = lam * ed['u_n'] ** 2 * 0 + (lam * ed['u_n'] ** 2 - lam * ed['u_np1'] ** 2)
        F = f / lam  # residual components at switches
        # (1) FD gradient of D w.r.t. edges
        h = 1e-6
        g = np.array([(D_edges(rc, e + h * np.eye(4)[j]) - D_edges(rc, e - h * np.eye(4)[j])) / (2 * h)
                      for j in range(4)])
        print(f"[{mode}] (1) dD/dx_j = {np.round(g, 6)} vs s_j f(x_j) = {np.round(s * f, 6)} "
              f"err={np.max(np.abs(g - s * f)):.2e}")
        # (2) FD Hessian (h=1e-3) vs lambda * diag(s) * J and J^T versions
        H = np.zeros((4, 4))
        hh = 1e-3
        for a in range(4):
            for b in range(4):
                vpp = e.copy(); vpp[a] += hh; vpp[b] += hh
                vpm = e.copy(); vpm[a] += hh; vpm[b] -= hh
                vmp = e.copy(); vmp[a] -= hh; vmp[b] += hh
                vmm = e.copy(); vmm[a] -= hh; vmm[b] -= hh
                H[a, b] = (D_edges(rc, vpp) - D_edges(rc, vpm) - D_edges(rc, vmp)
                           + D_edges(rc, vmm)) / (4 * hh * hh)
        J = analytic_jacobian_hp(rc, zs, N=400)
        H1 = lam * np.diag(s) @ J
        H2 = lam * J.T @ np.diag(s)
        print(f"[{mode}] (2) FD Hess = {np.round(H, 3)}")
        print(f"[{mode}]     H - lam diag(s) J      err={np.max(np.abs(H - H1)):.3e}")
        print(f"[{mode}]     H - lam J^T diag(s)    err={np.max(np.abs(H - H2)):.3e}")
        print(f"[{mode}]     eig(FD Hess) = {np.round(np.linalg.eigvalsh(H), 3)}")
        # (3) analytic J vs jac_fd
        Jfd = jac_fd(rc, zs)
        print(f"[{mode}] (3) |J - J_fd| = {np.max(np.abs(J - Jfd)):.2e} "
              f"rel = {np.max(np.abs(J - Jfd)) / np.max(np.abs(Jfd)):.2e}")


if __name__ == '__main__':
    main()
