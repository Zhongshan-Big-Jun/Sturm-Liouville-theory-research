# -*- coding: utf-8 -*-
"""R-209 M3: multistart solve of the full 8-equation truncated balance
(5 symbolic + 3 high-precision Richardson constraints).  Reports whether
the u^2-corrected power ansatz can close the balance at all.  EVIDENCE.
"""
import sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, r'scripts')
from _gapn2_largeR_balance import make_residual, make_symbolic  # noqa: E402


def main():
	residual, extra = make_residual()
	sym = make_symbolic()
	orders = [('E1', 0, 0), ('E1', 2, 0), ('E1', 2, 1),
		('E2', 2, 0), ('E2', 2, 1)]
	best = None
	for trial in range(120):
		g = [2.5 + 1.5*np.random.rand(), 0.5 + 0.2*np.random.rand(),
			0.1 + 0.4*np.random.rand(), 1.0 + 1.0*np.random.rand(),
			-4 + 8*np.random.rand(), -1 + 2*np.random.rand(),
			-1 + 2*np.random.rand(), -8 + 16*np.random.rand()]
		sol = least_squares(residual, g, xtol=1e-11, ftol=1e-11,
			gtol=1e-11, max_nfev=800, diff_step=1e-5)
		r = np.max(np.abs(sol.fun))
		if best is None or r < best[0]:
			best = (r, sol.x)
			print('trial %3d: residual %.3e X=%s' % (trial, r,
				np.array2string(sol.x, precision=4)), flush=True)
	r, X = best
	print('=== best ===')
	print('residual: %.3e' % r)
	print('X =', np.array2string(X, precision=10))
	print('extra:', np.array2string(extra(X), precision=3))
	symvals = [float(sym[o](*X)) for o in orders]
	print('symbolic part residuals:', ['%.2e' % v for v in symvals])


if __name__ == '__main__':
	main()
