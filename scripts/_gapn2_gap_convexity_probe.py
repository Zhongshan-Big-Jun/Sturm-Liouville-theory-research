# -*- coding: utf-8 -*-
"""R-207 route (ii) probe 2: is the half-gap g(x1,x2) = mu_2^N - mu_1^D
globally convex (INF) / concave (SUP) on the switch triangle for n=2?

The sector matrices are K = (1/(2(R-1)^2)) grad^2 g, so global convexity of g
would close (I1)+(I2) without R-monotonicity.  This script only samples the
Hessian eigenvalues on a grid (EVIDENCE).

Usage: python _gapn2_gap_convexity_probe.py [mode] [R] [grid]
"""
import sys
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_half_problem_probe import half_blocks, half_spectrum


def half_gap(R, x1, x2, mode):
	"""g = mu_2^N - mu_1^D for the left-half 3-block string of the n=2 pattern."""
	pat = [1.0, R, 1.0] if mode == 'sup' else [R, 1.0, R]
	hb = [(x1, pat[0]), (x2 - x1, pat[1]), (0.5 - x2, pat[2])]
	muD = half_spectrum(hb, 'D', N=2)
	muN = half_spectrum(hb, 'N', N=3)
	return muN[1] - muD[0]


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	R = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
	grid = int(sys.argv[3]) if len(sys.argv) > 3 else 8
	# triangle 0 < x1 < x2 < 1/2; sample interior points only
	pts = []
	for i in range(1, grid + 1):
		for j in range(1, grid + 1):
			if i < j:
				x1 = 0.5 * i / (grid + 1)
				x2 = 0.5 * j / (grid + 1)
				pts.append((x1, x2))
	h = 1e-5
	worst_lo = np.inf
	worst_hi = np.inf
	viol = 0
	for (x1, x2) in pts:
		# Hessian of g via central differences
		g0 = half_gap(R, x1, x2, mode)
		gx1p = half_gap(R, x1 + h, x2, mode)
		gx1m = half_gap(R, x1 - h, x2, mode)
		gx2p = half_gap(R, x1, x2 + h, mode)
		gx2m = half_gap(R, x1, x2 - h, mode)
		gxypp = half_gap(R, x1 + h, x2 + h, mode)
		gxypm = half_gap(R, x1 + h, x2 - h, mode)
		gxymp = half_gap(R, x1 - h, x2 + h, mode)
		gxymm = half_gap(R, x1 - h, x2 - h, mode)
		H11 = (gx1p - 2.0 * g0 + gx1m) / h ** 2
		H22 = (gx2p - 2.0 * g0 + gx2m) / h ** 2
		H12 = (gxypp - gxypm - gxymp + gxymm) / (4.0 * h ** 2)
		H = np.array([[H11, H12], [H12, H22]])
		ev = np.linalg.eigvalsh(H)
		if mode == 'inf':
			ok = ev[0] > 0.0
		else:
			ok = ev[1] < 0.0
		worst_lo = min(worst_lo, ev[0])
		worst_hi = min(worst_hi, -ev[1]) if mode == 'sup' else worst_hi
		if not ok:
			viol += 1
			print('  VIOLATION at x1=%.4f x2=%.4f eig=%s' % (x1, x2, ev))
	print('mode=%s R=%g grid=%d points=%d' % (mode, R, grid, len(pts)))
	if mode == 'inf':
		print('min eigenvalue of Hess(g): %.6e  (PD if > 0)' % worst_lo)
	else:
		print('max eigenvalue of Hess(g): %.6e  (ND if < 0)' % worst_hi)
	print('violations:', viol)


if __name__ == '__main__':
	main()
