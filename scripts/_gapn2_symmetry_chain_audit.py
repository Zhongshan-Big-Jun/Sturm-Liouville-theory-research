# -*- coding: utf-8 -*-
"""Audit of the symmetry chain for band-consistent points (EVIDENCE support
for the STRICT symmetry theorem; the theorem itself is analytic).

Chain being audited at every scan root (n=2..4, SUP/INF, R ladder):
  (P1) u_k(1-x) = (-1)^{k-1} u_k(x)  (parity, palindromic pattern)
  (P2) W(x) < 0 on (0,1), W = u_n u_{n+1}' - u_{n+1} u_n'
       (equivalently B(x) = int_0^x rho u_n u_{n+1} > 0)
  (P3) r(1-x) = -r(x), r = u_{n+1}/(c u_n)
  (P4) eps_j = (-1)^{j+1}, and x_j = 1 - x_{2n+1-j} for all j (symmetry),
       and x_n < 1/2 < x_{n+1}, and q1 = -q0.
"""
import sys
import numpy as np
import json

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_jacobian_analytic import uv_at


def shoot_pair(blocks, s, t):
    """(u, u') of the solution with u(0)=0, u'(0)=1 at scalar t."""
    v = uv_at(blocks, s, np.array([t]), left=True)
    return v[0, 0], v[0, 1]


def rho_at(blocks, t):
    """Density value at t (right-continuous convention at block edges)."""
    acc = 0.0
    for L, c in blocks:
        if t < acc + L:
            return c
        acc += L
    return blocks[-1][1]


def audit(rc, zs, N=200, grid=401):
    ed = eigen_data(rc, zs)
    n = rc.n
    x = ed['edges']
    lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
    c = ed['c']
    blocks = rc.blocks_from_z(zs)
    ss = roots_of(blocks, N + 1)
    # sample r on a fine grid via direct transfer-matrix shooting
    g = np.linspace(1e-6, 1 - 1e-6, grid)
    un = np.array([shoot_pair(blocks, np.sqrt(lam_n), t)[0] for t in g])
    unp = np.array([shoot_pair(blocks, np.sqrt(lam_np1), t)[0] for t in g])
    r = unp / (c * un)
    # P1 parity of u_n, u_{n+1}
    pn = (-1) ** (n - 1)
    err_p1 = max(np.max(np.abs(un - pn * un[::-1]) / (1 + np.abs(un).max())),
                 np.max(np.abs(unp - (-pn) * unp[::-1]) / (1 + np.abs(unp).max())))
    # P3 antisymmetry of r (where finite)
    rrev = -r[::-1]
    mask = np.abs(un) > 1e-8
    maskrev = np.abs(un[::-1]) > 1e-8
    m = mask & maskrev
    err_p3 = np.max(np.abs(r[m] - rrev[m]) / (1 + np.abs(r[m]).max()))
    # P2: W < 0 strictly in (0,1): W = -D int_0^x rho u_n u_{n+1}
    # compute W by ODE integration of W' = (lam_n - lam_{n+1}) rho u_n u_{n+1}
    D = lam_np1 - lam_n
    W = np.zeros_like(g)
    acc = 0.0
    for i in range(1, grid):
        t0, t1 = g[i - 1], g[i]
        mid = 0.5 * (t0 + t1)
        um = shoot_pair(blocks, np.sqrt(lam_n), mid)[0]
        upm = shoot_pair(blocks, np.sqrt(lam_np1), mid)[0]
        acc += (t1 - t0) * rho_at(blocks, mid) * um * upm
        W[i] = -D * acc
    inner = g[(g > 0.02) & (g < 0.98)]
    Wi = W[(g > 0.02) & (g < 0.98)]
    Wmax = Wi.max()
    Wmin = Wi.min()
    # P4: eps alternation + symmetry + center + q0/q1
    unx = np.array([shoot_pair(blocks, np.sqrt(lam_n), t)[0] for t in x])
    unpx = np.array([shoot_pair(blocks, np.sqrt(lam_np1), t)[0] for t in x])
    eps = unpx / (c * unx)
    eps_expect = np.array([(-1) ** (j + 1) for j in range(1, 2 * n + 1)])
    err_eps = np.max(np.abs(eps - eps_expect))
    sym_err = max(np.abs(x[j] - (1 - x[2 * n - 1 - j])) for j in range(2 * n))
    center_ok = x[n - 1] < 0.5 < x[n]
    # q0, q1 from r endpoints
    q0 = r[0]
    q1 = r[-1]
    return dict(err_p1=err_p1, err_p3=err_p3, Wmax=Wmax, Wmin=Wmin,
                err_eps=err_eps, sym_err=sym_err, center_ok=center_ok,
                q0=q0, q1=q1)


def main():
    tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
    worst = dict(err_p1=0.0, err_p3=0.0, Wmax=-1.0, Wmin=1.0,
                 err_eps=0.0, sym_err=0.0, q0q1=0.0)
    for n in (2, 3, 4):
        for mode in ('sup', 'inf'):
            rc = Recon(n, R=4.0, mode=mode)
            key = 'n%d_%s' % (n, mode.upper())
            e0 = np.array(tab[key]['edges'])
            w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
            z0 = rc.widths_to_z(w0)
            prev = z0
            Rs = [4.0, 1.2, 10.0, 30.0] if n <= 3 else [4.0, 1.2, 10.0]
            for R in Rs:
                rc = Recon(n, R, mode)
                zs = symmetric_root(rc, prev)
                if zs is None:
                    print('n=%d %s R=%g: NO ROOT' % (n, mode, R))
                    continue
                prev = zs
                a = audit(rc, zs)
                print('n=%d %s R=%5.1f: err_p1=%.1e err_p3=%.1e W in [%.3e, %.3e] '
                      'err_eps=%.1e sym_err=%.1e center=%s q0=%.6f q1=%.6f'
                      % (n, mode, R, a['err_p1'], a['err_p3'], a['Wmin'], a['Wmax'],
                         a['err_eps'], a['sym_err'], a['center_ok'], a['q0'], a['q1']))
                worst['err_p1'] = max(worst['err_p1'], a['err_p1'])
                worst['err_p3'] = max(worst['err_p3'], a['err_p3'])
                worst['Wmax'] = max(worst['Wmax'], a['Wmax'])
                worst['Wmin'] = min(worst['Wmin'], a['Wmin'])
                worst['err_eps'] = max(worst['err_eps'], a['err_eps'])
                worst['sym_err'] = max(worst['sym_err'], a['sym_err'])
                worst['q0q1'] = max(worst['q0q1'], abs(a['q0'] + a['q1']))
    print('WORST: err_p1=%.1e err_p3=%.1e Wmax=%.3e Wmin=%.3e err_eps=%.1e '
          'sym_err=%.1e |q0+q1|=%.1e' % (worst['err_p1'], worst['err_p3'],
                                         worst['Wmax'], worst['Wmin'],
                                         worst['err_eps'], worst['sym_err'],
                                         worst['q0q1']))


if __name__ == '__main__':
    main()
