# -*- coding: utf-8 -*-
"""R-209 probe: robust large-R continuation for the INF/SUP n=2 branch.

The stock roots_of grid (spacing 0.02 in s) misses the near-degenerate
pair lambda_2 ~ lambda_3 once D/(2 sqrt(lam)) < 0.02; this probe patches
roots_of so the pair is refined near the previous step's values (bracket
closest to the seed + bisection), then recomputes eigen data and sector
matrices from the refined pair.

All EVIDENCE; used to fix the degenerate-perturbation setup (route iii).

Usage: python _gapn2_largeR_probe2.py [mode] [Rstart] [Rend] [step]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
import _gapn2_symmetry_recon as SRC
from _gapn2_symmetry_recon import Recon, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import uv_at
from _gapn2_half_problem_probe import green_regular, green_regularized

SEED2 = None
SEED3 = None
_ORIG_ROOTS_OF = SRC.roots_of


def _m01(blocks, s):
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for (L, c) in blocks:
		w = s * np.sqrt(c)
		wL = w * L
		cw, sw = np.cos(wL), np.sin(wL) / w
		sw2 = -w * np.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, \
			sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return M01


def refine_near(blocks, seed, fallback):
	"""Bisect the sign change of M01 closest to seed; fallback if none."""
	win = max(0.02, 0.2 * max(seed, 0.5))
	lo, hi = max(seed - win, 1e-9), seed + win
	g = np.linspace(lo, hi, 20001)
	vals = np.array([_m01(blocks, s) for s in g])
	best = None
	best_d = np.inf
	for i in range(len(g) - 1):
		if vals[i] * vals[i + 1] < 0.0:
			mid = 0.5 * (g[i] + g[i + 1])
			dd = abs(mid - seed)
			if dd < best_d:
				best_d = dd
				best = (g[i], g[i + 1], vals[i])
	if best is None:
		return fallback
	a, b, fa = best
	for _ in range(200):
		m = 0.5 * (a + b)
		fm = _m01(blocks, m)
		if fa * fm <= 0.0:
			b = m
		else:
			a = m
			fa = fm
	return 0.5 * (a + b)


def roots_of_patched(blocks, k, npts=20000, refine=60):
	orig = _ORIG_ROOTS_OF(blocks, k, npts, refine)
	if SEED2 is not None and k >= 3 and len(orig) >= 3:
		orig[1] = refine_near(blocks, SEED2, orig[1])
		orig[2] = refine_near(blocks, SEED3, orig[2])
	return orig


SRC.roots_of = roots_of_patched


def main():
	global SEED2, SEED3
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	Rstart = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
	Rend = float(sys.argv[3]) if len(sys.argv) > 3 else 10000.0
	step = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	e0 = np.array(tab['n2_%s' % mode.upper()]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	zprev = rc0.widths_to_z(w0)
	R = Rstart
	while R <= Rend * 1.001:
		rc = Recon(2, R, mode)
		zs = symmetric_root(rc, zprev)
		if zs is None:
			print('R=%.4g: continuation FAILED' % R)
			break
		zprev = zs
		blocks = rc.blocks_from_z(zs)
		edges = np.cumsum(rc.z_to_widths(zs))[:-1]
		ss = SRC.roots_of(blocks, 3)
		SEED2, SEED3 = float(ss[1]), float(ss[2])
		s2, s3 = SEED2, SEED3
		lam2, lam3 = s2 ** 2, s3 ** 2
		un = eigfun(blocks, s2, edges)
		unp = eigfun(blocks, s3, edges)
		dn = uv_at(blocks, s2, edges, left=True)
		dnp = uv_at(blocks, s3, edges, left=True)
		Cn = un[0] / dn[0][0]
		Cnp = unp[0] / dnp[0][0]
		upn, upnp = Cn * dn[:, 1], Cnp * dnp[:, 1]
		c = np.sqrt(lam2 / lam3)
		eps = np.sign(unp / un)
		W = upnp * un - unp * upn
		sig = 1.0 if mode == 'sup' else -1.0
		d = sig * 2.0 * c * np.abs(W) / (R - 1.0)
		w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
		pat = rc.pat
		hb = [(w[0], pat[0]), (w[1], pat[1]), (w[2] / 2.0, pat[2])]
		muD1, muN2 = lam2, lam3
		x1, x2 = edges[0], edges[1]
		xs = [x1, x2]
		GD = np.zeros((2, 2)); GN = np.zeros((2, 2))
		GtD = np.zeros((2, 2)); GtN = np.zeros((2, 2))
		for (i, j) in [(0, 0), (0, 1), (1, 1)]:
			GD[i, j] = green_regular(hb, muN2, xs[i], xs[j], 'D')
			GN[i, j] = green_regular(hb, muD1, xs[i], xs[j], 'N')
			GtD[i, j] = green_regularized(hb, muD1, xs[i], xs[j], 'D')
			GtN[i, j] = green_regularized(hb, muN2, xs[i], xs[j], 'N')
		for M in (GD, GN, GtD, GtN):
			M[1, 0] = M[0, 1]
		c2 = lam2 / lam3
		e = np.array([1.0, -1.0])
		u = un
		Kp_odd = np.diag(d[:2]) + 2.0 * lam2 * np.diag(u[:2]) @ (
			GD * np.outer(e, e) - c2 * GN) @ np.diag(u[:2])
		v = u ** 2
		r = 2.0 * lam2 * (lam3 - lam2) / lam3 ** 2
		Ko = np.diag(d[:2]) + 2.0 * r * np.outer(e * v[:2], e * v[:2]) \
			+ 2.0 * lam2 * np.diag(u[:2]) @ (GtN - c2 * (GtD * np.outer(e, e))) \
			@ np.diag(u[:2])
		ep = np.linalg.eigvalsh(Kp_odd)
		eo = np.linalg.eigvalsh(Ko)
		D = lam3 - lam2
		print('R=%9.3g x1=%.9f x2=%.9f lam2=%.6f D*R=%.6f c=%.6f'
			% (R, x1, x2, lam2, D * R, c))
		print('    W(R-1)=%s  GDdiag=%s GNdiag=%s GtDdiag=%s GtNdiag=%s'
			% (np.round(W * (R - 1), 5), np.round(np.diag(GD), 5),
				np.round(np.diag(GN), 5), np.round(np.diag(GtD), 5),
				np.round(np.diag(GtN), 5)))
		print('    eigKp=%s eigKo=%s detKp=%.3e detKo=%.3e'
			% (np.round(ep, 6), np.round(eo, 6),
				np.linalg.det(Kp_odd), np.linalg.det(Ko)))
		R *= step


if __name__ == '__main__':
	main()
