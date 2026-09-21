# -*- coding: utf-8 -*-
"""Second variation of D_n = lambda_{n+1} - lambda_n under density perturbations.

Derivation (STRICT, operator form; verified here numerically):
  A(rho) = -(1/rho) d^2/dx^2 on L^2(rho dx), Dirichlet.  Along rho_e = rho + e dr:
    d(lambda_k)/de   = -lambda_k * <dr, u_k^2>            (unweighted pairing)
    d^2(lambda_k)/de^2 = 2 lambda_k <dr, u_k^2>^2
        - 2 lambda_k^2 * sum_{l != k} <dr, u_k u_l>^2 / (lambda_l - lambda_k)
  where <dr, phi> = integral dr phi dx and u_k is normalized by
  integral rho u_k^2 = 1.

Hence at a critical point (band-consistent root) of the bang-bang family:
  Q(dr) := (1/2) d^2(D_n)/de^2
      =  lambda_{n+1} <dr, u_{n+1}^2>^2 - lambda_n <dr, u_n^2>^2
       + lambda_n^2   sum_{l != n}   <dr, u_n   u_l>^2 / (lambda_l - lambda_n)
       - lambda_{n+1}^2 sum_{l != n+1} <dr, u_{n+1} u_l>^2 / (lambda_l - lambda_{n+1})
  with tangent condition <dr, f> = 0, f = lambda_n u_n^2 - lambda_{n+1} u_{n+1}^2.

Probes (all EVIDENCE unless a STRICT derivation is later attached):
  P1: formula vs finite differences (piecewise-constant dr on the block grid;
      FD is exact second derivative up to O(h^2) of an analytic path).
  P2: sign of Q on the tangent space {<dr, f> = 0} for random piecewise-constant
      dr and for smooth (trigonometric) dr: is Q < 0 (SUP) / > 0 (INF)?
  P3: restriction of Q to bang-bang directions dr = -sum_i s_i d(x-x_i) dx_i
      vs the known Hessian form  Q = (1/2) (dx)^T Hess (dx), Hess = -diag(s)
      * lambda_{n+1} * J; cross-check against K = diag(1/s) J and its sector
      decomposition K_o/K_e (odd/even mirror sectors).

Session results (2026-08-13, R-206):
  P1 PASS: formula (with BOTH sums over l != k, unweighted pairings) matches
      FD to ~1e-3 relative at N=60 spectral truncation (single-eigenvalue
      check: 4e-3 / 5e-2; minimal constant-string example: 1.7e-5).
  P2: SUP negative definite on the tangent space (n=2,3 R=4; n=2 R=10),
      all random directions negative (EVIDENCE).  INF n=2 R=4 INDEFINITE
      (mixed signs) - the naive tangent-space route is SUP-only at best.
  P3 NEGATIVE: the bump-regularized bang-bang dr does NOT reproduce the
      width-Hessian (sign mismatch at all tested points).  Reason: the
      width path rho(x; w + e dw) has second-order density variation
      d^2 rho = sum_i s_i dw_i^2 delta'(x - x_i) (boundary-layer terms of
      leading order); the naive formula captures only the delta-mass part.
      The handoff's proposed second-order coefficient identity FAILS.

Usage: python _gapn2_second_variation_probe.py [n] [R] [mode]
"""
import sys
import json
import functools
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data

N_MODES = 60
N_GRID = 4001
GRID = np.linspace(0.0, 1.0, N_GRID)
DX = 1.0 / (N_GRID - 1)


@functools.lru_cache(maxsize=4)
def cached_spectrum(blocks):
    blocks = tuple((float(L), float(c)) for L, c in blocks)
    ss = roots_of(blocks, N_MODES + 1)
    lam = ss ** 2
    U = np.zeros((N_MODES + 1, N_GRID))
    for l in range(N_MODES + 1):
        U[l] = eigfun(blocks, ss[l], GRID)
    return ss, lam, U

def pairings(drf):
    """Cw[k,l] = <dr, rho u_k u_l>, Cu[k,l] = <dr, u_k u_l>, dr_sq[k] = <dr, u_k^2>."""
    ss, lam, U = cached_spectrum(blocks)
    drg = drf(GRID)
    rho_g = rho_of_x(GRID)
    W = U * drg
    Cu = (W @ U.T) * DX
    Cw = ((U * rho_g * drg) @ U.T) * DX
    dr_sq = (W * U).sum(axis=1) * DX
    return lam, Cu, Cw, dr_sq


def q_formula(lam, Cu, Cw, n, dr_sq):
    a_n, a_np1 = dr_sq[n - 1], dr_sq[n]
    lam_n, lam_np1 = lam[n - 1], lam[n]
    total = lam_np1 * a_np1 ** 2 - lam_n * a_n ** 2
    for l in range(N_MODES + 1):
        if l != n - 1:
            total += lam_n ** 2 * Cu[n - 1, l] ** 2 / (lam[l] - lam_n)
        if l != n:
            total -= lam_np1 ** 2 * Cu[n, l] ** 2 / (lam[l] - lam_np1)
    return total


def rho_of_x(x):
    """Piecewise-constant rho on the grid."""
    i = np.clip(np.searchsorted(xs, x, side='right') - 1, 0, nb - 1)
    return np.array([PAT[ii] for ii in i], dtype=float)


def fd_second(blocks, dr_blocks, k, h=1e-4, refine=60):
    base = [b for b in blocks]

    def lam_at(e):
        blk = [(L, max(c + e * d, 1e-8)) for (L, c), d in zip(base, dr_blocks)]
        ss = roots_of(blk, k + 1, refine=refine)
        return ss[k] ** 2
    lp = lam_at(h)
    lm = lam_at(-h)
    l0 = lam_at(0.0)
    return (lp - 2.0 * l0 + lm) / h ** 2, l0, lp, lm


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    global PAT
    R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
    mode = sys.argv[3] if len(sys.argv) > 3 else 'sup'
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    rc0 = Recon(n, R=4.0, mode=mode)
    key = 'n%d_%s' % (n, mode.upper())
    e0 = np.array(tab[key]['edges'])
    w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
    z0 = rc0.widths_to_z(w0)
    rc = Recon(n, R, mode)
    zs = symmetric_root(rc, z0)
    global blocks
    PAT = rc.pat
    blocks = rc.blocks_from_z(zs)
    global xs, nb
    blocks = tuple((float(L), float(c)) for L, c in blocks)
    ed = eigen_data(rc, zs)
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    ss0 = roots_of(blocks, n + 1)
    un = eigfun(blocks, ss0[n - 1], GRID)
    unp = eigfun(blocks, ss0[n], GRID)
    f = lam_n * un ** 2 - lam_np1 * unp ** 2

    print('=== n=%d R=%g mode=%s lam_n=%.6f lam_np1=%.6f D=%.6f ==='
          % (n, R, mode, lam_n, lam_np1, lam_np1 - lam_n), flush=True)

    rng = np.random.default_rng(20260813)
    widths = rc.z_to_widths(zs)
    xs = np.concatenate([[0.0], np.cumsum(widths)])
    nb = 2 * n + 1
    idx = np.searchsorted(xs, GRID, side='right') - 1
    idx = np.clip(idx, 0, nb - 1)

    def block_dr_func(b):
        def drf(x):
            i = np.clip(np.searchsorted(xs, x, side='right') - 1, 0, nb - 1)
            return b[i]
        return drf

    favg = np.array([np.trapezoid(f[(GRID >= xs[i]) & (GRID < xs[i + 1])], dx=DX)
                     for i in range(nb)])
    fblock = favg / widths

    print('  P1: Q(formula) vs Q(FD) for random piecewise-constant dr:')
    for t in range(3):
        b = rng.standard_normal(nb)
        b -= b.dot(fblock) * fblock / fblock.dot(fblock)
        b *= 1e-2 / max(abs(b))
        lam2, Cu2, Cw2, dr_sq = pairings(block_dr_func(b))
        q_f = q_formula(lam2, Cu2, Cw2, n, dr_sq)
        lam_np1_fd, _, _, _ = fd_second(blocks, b, n, h=1e-4)
        lam_n_fd, _, _, _ = fd_second(blocks, b, n - 1, h=1e-4)
        q_fd = 0.5 * (lam_np1_fd - lam_n_fd)
        print('    t=%d: Q_formula=%.8e  Q_fd=%.8e  rel=%.2e  |tang|=%.2e'
              % (t, q_f, q_fd, abs(q_f - q_fd) / max(abs(q_fd), 1e-300),
                 abs(b.dot(fblock))), flush=True)

    print('  P2: sign of Q on tangent space (piecewise-constant dr, tangent to f):')
    signs = []
    for t in range(8):
        b = rng.standard_normal(nb)
        b -= b.dot(fblock) * fblock / fblock.dot(fblock)
        lam2, Cu2, Cw2, dr_sq = pairings(block_dr_func(b))
        q_f = q_formula(lam2, Cu2, Cw2, n, dr_sq)
        signs.append(q_f)
        print('    t=%d: Q=%.8e' % (t, q_f), flush=True)
    print('    sign summary: %s' % np.sign(signs))

    print('  P2b: sign of Q on tangent space (smooth trig dr, tangent to f):')
    gvec = np.array([np.trapezoid(np.sin((j + 1) * np.pi * GRID) * f, dx=DX)
                     for j in range(8)])

    def q_smooth(coef):
        def drf(x):
            out = np.zeros_like(x)
            for j, cj in enumerate(coef):
                out += cj * np.sin((j + 1) * np.pi * x)
            return out
        lam2, Cu2, Cw2, dr_sq = pairings(drf)
        return q_formula(lam2, Cu2, Cw2, n, dr_sq)

    for t in range(6):
        coef = rng.standard_normal(8)
        coef = coef - gvec * coef.dot(gvec) / gvec.dot(gvec)
        q = q_smooth(coef)
        def drf2(x):
            out = np.zeros_like(x)
            for j, cj in enumerate(coef):
                out += cj * np.sin((j + 1) * np.pi * x)
            return out
        tng = np.trapezoid(drf2(GRID) * f, dx=DX)
        print('    t=%d: Q=%.8e  tang=%.2e' % (t, q, tng), flush=True)

    print('  P3: bang-bang Q vs Hessian/K sector forms:')
    s = np.array([rc.pat[i + 1] - rc.pat[i] for i in range(2 * n)])
    Jfd = jac_fd(rc, zs)
    Hess = -np.diag(s) * lam_np1 * Jfd
    edges = ed['edges']
    w_bump = 5e-4

    def bump_drf(dxvec):
        def drf(x):
            out = np.zeros_like(x)
            for i in range(2 * n):
                m = (x > edges[i] - w_bump) & (x < edges[i] + w_bump)
                out[m] += -s[i] * dxvec[i] / (2.0 * w_bump)
            return out
        return drf

    for t in range(3):
        dxvec = rng.standard_normal(2 * n)
        q_h = 0.5 * dxvec.dot(Hess).dot(dxvec)
        lam2, Cu2, Cw2, dr_sq = pairings(bump_drf(dxvec))
        q_bb = q_formula(lam2, Cu2, Cw2, n, dr_sq)
        print('    t=%d: Q(Hess)=%.8e  Q(naive bump formula)=%.8e  rel=%.2e'
              % (t, q_h, q_bb, abs(q_h - q_bb) / max(abs(q_h), 1e-300)), flush=True)



if __name__ == '__main__':
    main()
