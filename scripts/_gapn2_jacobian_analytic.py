# -*- coding: utf-8 -*-
"""Verify the analytic Jacobian structure of the band self-consistency system.

Claims (all to be verified numerically, EVIDENCE):
  (A1) At a band-consistent point x (F_j = f(x_j)/lambda_{n+1} = 0):
       J = D_xF = (D~ + M~)/lambda_{n+1},  D~ = diag(f'(x_j)),
       M~_{ji} = s_i * { -2 w_i w_j D/(lambda_n lambda_{n+1})
                         + 2 lambda_n^2 u_n(x_i) u_n(x_j) G~_n(x_i,x_j)
                         - 2 lambda_{n+1}^2 u_{n+1}(x_i) u_{n+1}(x_j) G~_{n+1}(x_i,x_j) },
       w_j = lambda_n u_n(x_j)^2 = lambda_{n+1} u_{n+1}(x_j)^2,
       s_i = rho_{i+1} - rho_i = +-(R-1) (alternating),
       G~_k(x,y) = regularized resolvent kernel at lambda_k (pole removed),
       derived from first-order perturbation theory of the weighted string.
  Derivation (signs corrected 2026-08-12): with delta rho = s_i delta(x-x_i) delta x_i,
  delta A = -(delta rho/rho) A  =>  delta lambda_k = -lambda_k s_i u_k(x_i)^2 delta x_i,
  delta u_k(x) = -u_k(x)(s_i u_k(x_i)^2/2) delta x_i
                 + lambda_k s_i u_k(x_i) G~_k(x,x_i) delta x_i,
  G~_k(x,y) = sum_{l != k} u_l(x) u_l(y)/(lambda_l - lambda_k) (resolvent kernel wrt rho dy,
  pole removed).  Combining the two modes with w_i = lambda_n u_n(x_i)^2 and
  u_{n+1}(x_j)^2 - u_n(x_j)^2 = -w_j D/(lambda_n lambda_{n+1}) gives
  M~_{ji} = s_i * { -2 w_i w_j D/(lambda_n lambda_{n+1})
                         + 2 lambda_n^2 u_n(x_i) u_n(x_j) G~_n(x_i,x_j)
                         - 2 lambda_{n+1}^2 u_{n+1}(x_i) u_{n+1}(x_j) G~_{n+1}(x_i,x_j) }.
  (A2) f'(x_j) = -2 lambda_{n+1} eps_j c W(x_j),  eps_j = u_{n+1}(x_j)/u_n(x_j)/c,
       c = sqrt(lambda_n/lambda_{n+1}), W = u_{n+1}' u_n - u_{n+1} u_n' < 0.
  (A3) Hess(D_n) restricted to the family = diag(s_i) * lambda_{n+1} * J at any
       critical point; hence (G1') <=> det Hess > 0 at every critical point.

Usage: python _gapn2_jacobian_analytic.py [n] [Rs] [mode]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import jac_fd, sym_antisym_decomp, symmetric_root


def prop_matrix(blocks, s):
    """Transfer matrix (u, u') -> (u, u') across all blocks for -u'' = s^2 rho u."""
    M = np.eye(2)
    for L, c in blocks:
        w = s * np.sqrt(c)
        wL = w * L
        cw, sw = np.cos(wL), np.sin(wL)
        P = np.array([[cw, sw / w], [-w * sw, cw]])
        M = P @ M
    return M


def uv_at(blocks, s, pts, left=True):
    """(u, u') at pts for the solution with u(0)=0, u'(0)=1 (left=True) or
    the solution with u(1)=0, u'(1)=-1 propagated backward (left=False)."""
    xs = [0.0]
    for L, _ in blocks:
        xs.append(xs[-1] + L)
    out = np.zeros((len(pts), 2))
    # propagate segment starts
    starts = []
    M = np.eye(2)
    starts.append((0.0, M.copy()))
    for L, c in blocks:
        w = s * np.sqrt(c)
        wL = w * L
        cw, sw = np.cos(wL), np.sin(wL)
        P = np.array([[cw, sw / w], [-w * sw, cw]])
        M = P @ M
        starts.append((xs[len(starts)], M.copy()))
    for j, p in enumerate(pts):
        bi = max(i for i in range(len(xs) - 1) if xs[i] < p)
        base_x, M0 = starts[bi]
        L, c = blocks[bi]
        w = s * np.sqrt(c)
        d = p - base_x
        cw, sw = np.cos(w * d), np.sin(w * d)
        if left:
            v0 = np.array([0.0, 1.0])
        else:
            # backward: u(1)=0, u'(1)=-1 ; propagate through blocks after bi
            v1 = np.array([0.0, -1.0])
            Mback = np.eye(2)
            for Lb, cb in blocks[bi + 1:]:
                wb = s * np.sqrt(cb)
                wLb = wb * Lb
                cbw, sbw = np.cos(wLb), np.sin(wLb)
                Pb = np.array([[cbw, sbw / wb], [-wb * sbw, cbw]])
                Mback = Pb @ Mback
            # state at block start x_bi solves Mback @ v_start = v1 (propagate to x=1)
            v_start = np.linalg.solve(Mback, v1)
        if left:
            # forward from 0: state at block start then within-block propagation
            v_at_start = M0 @ v0
            P = np.array([[cw, sw / w], [-w * sw, cw]])
            out[j] = P @ v_at_start
        else:
            # backward from 1: v_start = state at block RIGHT end xs[bi+1];
            # propagate back to p within block bi: P(-(xs[bi+1]-p))
            db = xs[bi + 1] - p
            cbw, sbw = np.cos(w * db), np.sin(w * db)
            Pb = np.array([[cbw, -sbw / w], [w * sbw, cbw]])  # P(-db)
            out[j] = Pb @ v_start
    return out


def green_kernel(blocks, mu, pts):
    """G_mu(x_i, x_j) via phi/psi/W formula; returns (npts x npts) matrix."""
    s = np.sqrt(mu)
    npts = len(pts)
    phi = uv_at(blocks, s, pts, left=True)          # (npts,2): phi, phi'
    psi = uv_at(blocks, s, pts, left=False)         # (npts,2): psi, psi'
    # Wronskian W = phi psi' - phi' psi (constant; evaluate at pts, take median)
    W = phi[:, 0] * psi[:, 1] - phi[:, 1] * psi[:, 0]
    Wv = np.median(W)
    # spectral Green kernel: G_mu(x,y) = -phi(x)psi(y)/W for x<=y
    # (normalization phi(0)=0, phi'(0)=1; psi(1)=0, psi'(1)=-1)
    G = np.zeros((npts, npts))
    for i in range(npts):
        for j in range(npts):
            if i <= j:
                G[i, j] = -phi[i, 0] * psi[j, 0] / Wv
            else:
                G[i, j] = -phi[j, 0] * psi[i, 0] / Wv
    return G


def regularized_green(blocks, lam, pts, u_k=None, delta=1e-9):
    """G~_k(x,y) = lim_{mu->lam_k} [G_mu(x,y) - u_k(x)u_k(y)/(lam_k-mu)].

    The spectral residue u_k(x)u_k(y) is mu-independent (u_k = normalized
    eigenfunction at lambda_k), so the direct subtraction converges with error
    O(delta); delta relative to lam, e.g. 1e-9 gives ~1e-12 accuracy on the
    smooth part (G_mu ~ 1/delta -> cancellation error ~ 1e-16/delta*lam ~ 1e-6
    relative to the pole, i.e. ~1e-12 absolute for values O(0.01))."""
    mu = lam * (1.0 - delta)
    G = green_kernel(blocks, mu, pts)
    if u_k is None:
        # caller must pass the normalized eigenfunction values at pts
        raise ValueError('u_k (normalized eigenfunction values at pts) required')
    return G - np.outer(u_k, u_k) / (lam - mu)


def eigen_data(rc, z):
    """lambda_n, lambda_{n+1}, u_n, u_{n+1}, u'_n, u'_{n+1} at switch points,
    eps_j, c, W(x_j)."""
    blocks = rc.blocks_from_z(z)
    ss = roots_of(blocks, rc.n + 1)
    lam_n, lam_np1 = ss[rc.n - 1] ** 2, ss[rc.n] ** 2
    w = rc.z_to_widths(z)
    edges = np.cumsum(w)[:-1]
    n = rc.n
    sn, snp1 = ss[rc.n - 1], ss[rc.n]
    # normalized eigenfunction values + derivatives at edges
    un = eigfun(blocks, sn, edges)
    unp = eigfun(blocks, snp1, edges)
    # derivatives: use uv_at with scaling.  eigfun normalizes by sqrt(int rho u^2).
    def derivs(s, edges_):
        # unnormalized solution (u0,u0') with u(0)=0,u'(0)=1
        vals = uv_at(blocks, s, edges_, left=True)
        # normalization: u = C * u0 ; C from eigfun value at first point
        u0 = vals[:, 0]
        # norm factor: eigfun already normalized; u0 unnormalized -> C = un/ u0
        C = np.mean(eigfun(blocks, s, edges_) / u0)
        return C * vals[:, 0], C * vals[:, 1]
    d_n, d_np = derivs(sn, edges), derivs(snp1, edges)
    u_n, up_n = d_n
    u_np1, up_np1 = d_np
    c = np.sqrt(lam_n / lam_np1)
    eps = np.sign(u_np1 / u_n)  # +1 left switches (odd j), -1 right (even j)
    W = up_np1 * u_n - u_np1 * up_n
    return dict(lam_n=lam_n, lam_np1=lam_np1, edges=edges, u_n=u_n, u_np1=u_np1,
                up_n=up_n, up_np1=up_np1, c=c, eps=eps, W=W)


def analytic_jacobian(rc, z):
    """J_analytic = (D~ + M~)/lambda_{n+1} at a band-consistent point."""
    ed = eigen_data(rc, z)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n, u_np1 = ed['u_n'], ed['u_np1']
    up_n, up_np1 = ed['up_n'], ed['up_np1']
    c, eps, W = ed['c'], ed['eps'], ed['W']
    n = rc.n
    # s_i = rho_{i+1} - rho_i
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    D = lam_np1 - lam_n
    wj = lam_n * u_n ** 2
    # check consistency lambda_{n+1} u_{n+1}^2 = wj
    wj2 = lam_np1 * u_np1 ** 2
    # diagonal D~
    fprime = 2.0 * lam_n * u_n * up_n - 2.0 * lam_np1 * u_np1 * up_np1
    # analytic identity f' = -2 lambda_{n+1} eps c W
    fprime_id = -2.0 * lam_np1 * eps * c * W
    # regularized resolvent kernels
    blocks = rc.blocks_from_z(z)
    Gn = regularized_green(blocks, lam_n, edges, u_k=u_n)
    Gnp1 = regularized_green(blocks, lam_np1, edges, u_k=u_np1)
    # sign-corrected formula (see docstring derivation): all three terms flipped
    # relative to the original draft
    M = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            term = (-2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1)
                    + 2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j]
                    - 2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
            M[j, i] = s[i] * term
    np.fill_diagonal(M, M.diagonal())  # keep diagonal from the uniform formula
    J = (np.diag(fprime) + M) / lam_np1
    return J, fprime, fprime_id, wj, wj2


def term_breakdown(rc, z):
    """Return D~, M1 (w term), M2 (lambda_n Green), M3 (lambda_{n+1} Green) for diagnostics."""
    ed = eigen_data(rc, z)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    edges = ed['edges']
    u_n, u_np1 = ed['u_n'], ed['u_np1']
    n = rc.n
    pat = rc.pat
    s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
    D = lam_np1 - lam_n
    wj = lam_n * u_n ** 2
    fprime = 2.0 * lam_n * u_n * ed['up_n'] - 2.0 * lam_np1 * u_np1 * ed['up_np1']
    blocks = rc.blocks_from_z(z)
    Gn = regularized_green(blocks, lam_n, edges, u_k=u_n)
    Gnp1 = regularized_green(blocks, lam_np1, edges, u_k=u_np1)
    M1 = np.zeros((2 * n, 2 * n)); M2 = np.zeros((2 * n, 2 * n)); M3 = np.zeros((2 * n, 2 * n))
    for j in range(2 * n):
        for i in range(2 * n):
            M1[j, i] = s[i] * (-2.0 * wj[i] * wj[j] * D / (lam_n * lam_np1))
            M2[j, i] = s[i] * (2.0 * lam_n ** 2 * u_n[i] * u_n[j] * Gn[i, j])
            M3[j, i] = s[i] * (-2.0 * lam_np1 ** 2 * u_np1[i] * u_np1[j] * Gnp1[i, j])
    return dict(fprime=fprime, M1=M1, M2=M2, M3=M3, s=s, wj=wj, D=D)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.05, 2.0, 4.0, 10.0]
    mode = sys.argv[3] if len(sys.argv) > 3 else 'both'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    for m in (['sup', 'inf'] if mode == 'both' else [mode]):
        rc0 = Recon(n, R=4.0, mode=m)
        key = f"n{n}_{m.upper()}"
        e0 = np.array(tab[key]['edges'])
        w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
        z0 = rc0.widths_to_z(w0)
        prev = None
        print(f"=== n={n} mode={m} ===")
        for R in Rs:
            rcR = Recon(n, R, m)
            z = z0 if prev is None else prev
            zs = symmetric_root(rcR, z)
            if zs is None:
                print(f"R={R}: no symmetric root found (residual too large)"); continue
            prev = zs
            Jfd = jac_fd(rcR, zs)
            J, fprime, fprime_id, wj, wj2 = analytic_jacobian(rcR, zs)
            err = np.max(np.abs(J - Jfd))
            rel = err / np.max(np.abs(Jfd))
            # residual check: f ~ 0 at switches
            res = np.max(np.abs(rcR.residual(zs)))
            # w consistency
            wrel = np.max(np.abs(wj - wj2) / np.max(np.abs(wj)))
            # f' identity
            fprime_rel = np.max(np.abs(fprime - fprime_id)) / np.max(np.abs(fprime))
            # Hessian spectrum: Hess = diag(s) * lambda_{n+1} * J
            pat = rcR.pat
            s = np.array([pat[i + 1] - pat[i] for i in range(2 * n)])
            lam_np1 = eigen_data(rcR, zs)['lam_np1']
            H = np.diag(s) * lam_np1 * Jfd
            ev = np.linalg.eigvalsh(H)
            print(f"R={R:8.4g} |Jfd|max={np.max(np.abs(Jfd)):10.3e} "
                  f"err={err:10.3e} rel={rel:10.3e} res={res:10.3e} "
                  f"wrel={wrel:10.3e} fprimrel={fprime_rel:10.3e}")
            print(f"         Hess eig (SUP=neg def?, INF=pos def?): {np.round(ev, 4)}")


if __name__ == '__main__':
    main()
