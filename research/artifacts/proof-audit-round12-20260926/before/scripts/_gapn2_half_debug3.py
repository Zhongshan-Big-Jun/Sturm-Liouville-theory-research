# -*- coding: utf-8 -*-
"""R-207: verify L_x B = delta - rho(x) u(x) u(y) for the NO-rho(y)-factor
particular solution B = (u(x)v(y) - v(x)u(y)) 1_{x>y} - u(x)u(y) I1(x)
+ v(x)u(y) I2(x), and the resulting projection-free form Gt = B - u(x)P(y)
with P(y) = <rho u, B(.,y)> = v(y)(1-I2(y)) - u(y)(A1-A2+I1(L)-I1(y)).

All numerics EVIDENCE.
Usage: python _gapn2_half_debug3.py
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum, _norm2,
	_propagate, second_solution, _int_rho_u_v, _int_rho_u2, _spectral_green)


def bracket(hblocks, mu, x, y, u0, vf):
	I1x = _int_rho_u_v(hblocks, mu, x, u0)
	I2x = _int_rho_u2(hblocks, mu, x, u0)
	heaviside = 1.0 if x > y else 0.0
	return (u0 * _propagate(hblocks, mu, x)[0] * vf(y)
		- vf(x) * u0 * _propagate(hblocks, mu, y)[0]) * heaviside \
		- u0 * _propagate(hblocks, mu, x)[0] * u0 * _propagate(hblocks, mu, y)[0] * I1x \
		+ vf(x) * u0 * _propagate(hblocks, mu, y)[0] * I2x


def A1A2(hblocks, mu, u0, vf, Nq=200000):
	L = sum(b[0] for b in hblocks)
	cums = [sum(b[0] for b in hblocks[:i + 1]) for i in range(len(hblocks))]
	g = np.linspace(0.0, L, Nq)
	rho_g = np.array([hblocks[min(int(np.searchsorted(cums, t)), len(hblocks) - 1)][1] for t in g])
	u_g = np.array([u0 * _propagate(hblocks, mu, t)[0] for t in g])
	v_g = np.array([vf(t) for t in g])
	I1_g = np.array([_int_rho_u_v(hblocks, mu, t, u0) for t in g])
	I2_g = np.array([_int_rho_u2(hblocks, mu, t, u0) for t in g])
	A1 = np.trapz(rho_g * u_g ** 2 * I1_g, g)
	A2 = np.trapz(rho_g * u_g * v_g * I2_g, g)
	return A1, A2


def main():
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode='inf')
	e0 = np.array(tab['n2_INF']['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	rc = Recon(2, 4.0, 'inf')
	zs = symmetric_root(rc, rc0.widths_to_z(w0))
	ed = eigen_data(rc, zs)
	w = np.diff(np.concatenate([[0.0], ed['edges'], [1.0]]))
	hb = half_blocks(rc, w)
	L = sum(b[0] for b in hb)
	muD = half_spectrum(hb, 'D', N=80)
	muN = half_spectrum(hb, 'N', N=80)
	x1 = w[0]
	x2 = w[0] + w[1]
	eps = 1e-8
	for (name, mu, pole, bc) in [('D', muD[0], 0, 'D'), ('N', muN[1], 1, 'N')]:
		u0 = 1.0 / np.sqrt(_norm2(hb, mu, (0.0, 1.0)))
		vf = second_solution(hb, mu)
		A1, A2 = A1A2(hb, mu, u0, vf)
		I1L = _int_rho_u_v(hb, mu, L, u0)
		print('--- %s mu=%.12f A1=%.9f A2=%.9f ---' % (name, mu, A1, A2))
		# FD check of L_x B = delta - rho u u^T on a fine grid away from y
		g = np.linspace(0.0, L, 6000)
		h = g[1] - g[0]
		cums = [sum(b[0] for b in hb[:i + 1]) for i in range(len(hb))]
		rho_g = np.array([hb[min(int(np.searchsorted(cums, t)), len(hb) - 1)][1] for t in g])
		u_g = np.array([u0 * _propagate(hb, mu, t)[0] for t in g])
		yb = [0.15, 0.30, 0.45]
		for y in yb:
			Bg = np.array([bracket(hb, mu, t, y, u0, vf) for t in g])
			Lap = np.gradient(np.gradient(Bg, h), h)
			resid = -Lap - mu * rho_g * Bg + rho_g * u_g * u_g[int(round(y / h))]
			# residual should be ~0 away from x=y and x=block jumps of the
			# grid point evaluation (B is continuous, derivative jumps only at x=y)
			mask = np.abs(g - y) > 3 * h
			print('  L_xB residual at y=%.2f: max=%.3e (away from diagonal)'
				% (y, np.max(np.abs(resid[mask]))))
		# corrected closed form Gt = B - u(x)P(y), symmetric, no rho factor
		def Gt_cf(x, y):
			I1y = _int_rho_u_v(hb, mu, y, u0)
			I2y = _int_rho_u2(hb, mu, y, u0)
			P = vf(y) * (1.0 - I2y) - u0 * _propagate(hb, mu, y)[0] * (A1 - A2 + I1L - I1y)
			return bracket(hb, mu, x, y, u0, vf) - u0 * _propagate(hb, mu, x)[0] * P
		pts = [(x1, x1), (x1, x2), (x2, x2)]
		errs = []
		for (a, b) in pts:
			cf = Gt_cf(a, b)
			sp = _spectral_green(hb, mu, pole, bc, a, b, N=80)
			errs.append(abs(cf - sp))
			print('  Gt(%8.5f,%8.5f): cf=%.8f sp=%.8f err=%.3e' % (a, b, cf, sp, cf - sp))
		print('  symmetry check Gt(x2,x1) vs Gt(x1,x2): err = %.3e'
			% abs(Gt_cf(x2, x1) - Gt_cf(x1, x2)))
		print('  continuity across y=x2: err = %.3e'
			% abs(Gt_cf(x1, x2 + eps) - Gt_cf(x1, x2)))
		print('  max |cf - sp| over 3 pts = %.3e' % max(errs))


if __name__ == '__main__':
	main()
