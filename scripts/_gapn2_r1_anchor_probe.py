# -*- coding: utf-8 -*-
"""R-207 route (i): finite rescaled R->1+ limit of (R-1)K at the constant string.

Claims (EVIDENCE via continuation; the STRICT anchor math lives in the run
notes addendum):
  A1: symmetric band-consistent roots continue down to R = 1+ (seeded from
      R=1.05) and converge to the constant string: D -> 5*pi^2, lam_2 ->
      4*pi^2, lam_3 -> 9*pi^2, switches x_j -> zeros of f0 = lam_2 u2^2 -
      lam_3 u3^2 (u_k = sqrt(2) sin(k pi x)).
  A2: (R-1) Kp_odd and (R-1) Ko converge to the diagonal limit
      diag(sigma 2 c0 |W0(x_j)|), j < n, sigma = +1 SUP / -1 INF, c0 = 2/3,
      W0 = u3' u2 - u3 u2' at the constant string, x_j = zeros of f0.
  A3: the O(1) parts (off-diagonal and Green blocks) stay bounded as R -> 1+.

All numbers below are EVIDENCE; the STRICT proof of the anchor is in the
run notes (W0 does not vanish at the zeros of f0; smooth branch near R=1).

Usage: python _gapn2_r1_anchor_probe.py [mode] [Rmax Rmin npts]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum,
	green_regular, green_regularized)


def f0_zeros(npts=20000):
	"""Zeros of f0(x) = 8 pi^2 (sin(2pi x)^2 - (9/4) sin(3pi x)^2) on (0,1)."""
	xs = np.linspace(0.0, 1.0, npts)
	f = np.sin(2.0 * np.pi * xs) ** 2 - 2.25 * np.sin(3.0 * np.pi * xs) ** 2
	zs = []
	for i in range(len(xs) - 1):
		if f[i] * f[i + 1] < 0.0:
			a, b = xs[i], xs[i + 1]
			for _ in range(80):
				m = 0.5 * (a + b)
				fm = np.sin(2.0 * np.pi * m) ** 2 - 2.25 * np.sin(3.0 * np.pi * m) ** 2
				if f[i] * fm <= 0.0:
					b = m
				else:
					a = m
			zs.append(0.5 * (a + b))
	return np.array(zs)


def w0_at(x):
	"""Wronskian W0(x) = u3'(x) u2(x) - u3(x) u2'(x) at the constant string."""
	u2 = np.sqrt(2.0) * np.sin(2.0 * np.pi * x)
	u3 = np.sqrt(2.0) * np.sin(3.0 * np.pi * x)
	du2 = np.sqrt(2.0) * 2.0 * np.pi * np.cos(2.0 * np.pi * x)
	du3 = np.sqrt(2.0) * 3.0 * np.pi * np.cos(3.0 * np.pi * x)
	return du3 * u2 - u3 * du2


def closed_sectors(rc, zs):
	"""Closed-form Kp_odd and Ko at the symmetric root (n=2)."""
	ed = eigen_data(rc, zs)
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	edges = ed['edges']
	w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
	hb = half_blocks(rc, w)
	muD = half_spectrum(hb, 'D', N=4)
	muN = half_spectrum(hb, 'N', N=4)
	x1, x2 = edges[0], edges[1]
	xs = [x1, x2]
	GD = np.zeros((2, 2))
	GN = np.zeros((2, 2))
	GtD = np.zeros((2, 2))
	GtN = np.zeros((2, 2))
	for (i, j) in [(0, 0), (0, 1), (1, 1)]:
		a, b = xs[i], xs[j]
		GD[i, j] = green_regular(hb, muN[1], a, b, 'D')
		GN[i, j] = green_regular(hb, muD[0], a, b, 'N')
		GtD[i, j] = green_regularized(hb, muD[0], a, b, 'D')
		GtN[i, j] = green_regularized(hb, muN[1], a, b, 'N')
	for M in (GD, GN, GtD, GtN):
		M[1, 0] = M[0, 1]
	c = ed['c']
	Wv = ed['W']
	sig = 1.0 if rc.mode == 'sup' else -1.0
	d = sig * 2.0 * c * np.abs(Wv) / (rc.R - 1.0)
	u = ed['u_n']
	c2 = lam_n / lam_np1
	e = np.array([1.0, -1.0])
	Kp_odd = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ (
		GD * np.outer(e, e) - c2 * GN) @ np.diag(u[:2])
	v = u ** 2
	r = 2.0 * lam_n * (lam_np1 - lam_n) / lam_np1 ** 2
	ev = np.array([1.0, -1.0])
	Ko = np.diag(d[:2]) + 2.0 * r * np.outer(ev * v[:2], ev * v[:2]) \
		+ 2.0 * lam_n * np.diag(u[:2]) @ (GtN - c2 * (GtD * np.outer(e, e))) \
		@ np.diag(u[:2])
	return Kp_odd, Ko, dict(lam_n=lam_n, lam_np1=lam_np1, d=d, u=u, W=Wv, c=c)


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'both'
	parts = sys.argv[2].split(',') if len(sys.argv) > 2 else ['1.05', '1.00001', '20']
	Rmax, Rmin, npts = float(parts[0]), float(parts[1]), int(parts[2])
	Rs = np.geomspace(Rmax, Rmin, npts)
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	# constant-string analytic limit
	xz = f0_zeros()
	print('f0 zeros on (0,1):', np.round(xz, 10))
	print('W0 at zeros:', np.round(w0_at(xz), 10))
	c0 = 2.0 / 3.0
	for m in (['sup', 'inf'] if mode == 'both' else [mode]):
		sig = 1.0 if m == 'sup' else -1.0
		lim_diag = sig * 2.0 * c0 * np.abs(w0_at(xz))
		print('=== mode=%s  limit diag (R-1)K -> ' % m, np.round(lim_diag, 8))
		rc0 = Recon(2, R=4.0, mode=m)
		key = 'n2_%s' % m.upper()
		e0 = np.array(tab[key]['edges'])
		w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
		zprev = rc0.widths_to_z(w0)
		for R in Rs:
			rcR = Recon(2, R, m)
			zs = symmetric_root(rcR, zprev)
			if zs is None:
				print('  R=%.6f: root not found' % R)
				break
			zprev = zs
			Kp_odd, Ko, info = closed_sectors(rcR, zs)
			ed = eigen_data(rcR, zs)
			D = ed['lam_np1'] - ed['lam_n']
			rKp = (R - 1.0) * Kp_odd
			rKo = (R - 1.0) * Ko
			lim2 = lim_diag[:2]
			err_p = np.max(np.abs(rKp - np.diag(lim2)))
			err_o = np.max(np.abs(rKo - np.diag(lim2)))
			print('  R=%.6f D=%.8f lam2=%.8f lam3=%.8f x1=%.8f x2=%.8f'
				% (R, D, ed['lam_n'], ed['lam_np1'], ed['edges'][0], ed['edges'][1]))
			print('    |(R-1)Kp_odd - lim| = %.3e   |(R-1)Ko - lim| = %.3e'
				% (err_p, err_o))
			print('    (R-1)Kp_odd =', np.round(rKp, 8))
			print('    (R-1)Ko     =', np.round(rKo, 8))


if __name__ == '__main__':
	main()
