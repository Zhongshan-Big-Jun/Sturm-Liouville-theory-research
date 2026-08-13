# -*- coding: utf-8 -*-
"""Refutation probe: eigenfunction parity is NOT global for palindromic heights.

The parity u_k(1-x) = (-1)^{k-1} u_k(x) needs rho(1-x) = rho(x), i.e.
SYMMETRIC widths, not just palindromic heights.  This probe evaluates the
parity and f-evenness errors on random asymmetric widths.

Result (EVIDENCE, see 2026-08-13b addendum): errors are O(1) on asymmetric
widths and O(1e-16) on the symmetric branch.
"""
import sys
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun


def probe(seed=20260813, trials=8):
    rng = np.random.default_rng(seed)
    worst_p1 = 0.0
    worst_feven = 0.0
    for trial in range(trials):
        n = 2 + (trial % 3)
        R = [2.0, 4.0, 7.0][trial % 3]
        for mode in ('sup', 'inf'):
            rc = Recon(n, R, mode)
            w = rng.dirichlet(np.ones(rc.nb))
            blocks = [(float(wi), rc.pat[i]) for i, wi in enumerate(w)]
            pat = rc.pat
            pal = all(pat[i] == pat[rc.nb - 1 - i] for i in range(rc.nb))
            ss = roots_of(blocks, n + 2)
            grid = np.linspace(0, 1, 501)
            for k in range(1, n + 2):
                u = eigfun(blocks, ss[k - 1], grid)
                pref = (-1.0) ** (k - 1)
                rel = np.max(np.abs(u[::-1] - pref * u)) / (1.0 + np.max(np.abs(u)))
                worst_p1 = max(worst_p1, rel)
            un = eigfun(blocks, ss[n - 1], grid)
            unp = eigfun(blocks, ss[n], grid)
            f = ss[n - 1] ** 2 * un ** 2 - ss[n] ** 2 * unp ** 2
            rel_f = np.max(np.abs(f - f[::-1])) / (1.0 + np.max(np.abs(f)))
            worst_feven = max(worst_feven, rel_f)
    return pal, worst_p1, worst_feven


if __name__ == '__main__':
    pal, p1, fe = probe()
    print('palindromic heights hold:', pal)
    print('WORST parity error (random asymmetric widths): %.3e' % p1)
    print('WORST f-evenness error (random asymmetric widths): %.3e' % fe)
