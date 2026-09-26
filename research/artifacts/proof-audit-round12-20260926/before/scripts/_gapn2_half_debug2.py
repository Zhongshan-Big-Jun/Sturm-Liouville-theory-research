# -*- coding: utf-8 -*-
"""R-207 debug: isolate the closed-form regularized-Green failure mechanism.

Two competing hypotheses for the C2 mismatch (3-block INF R=4):
  H1: A1/A2 trapezoid quadrature is too coarse (handoff claim).
  H2: rho(y) convention at density jumps: the closed form is rho(y)*H(x,y)
      with continuous H, so its pointwise value at a switch point y=x_j
      depends on which block rho(y) is read from, while the spectral sum is
      a specific continuous representative.

All numerics EVIDENCE.
Usage: python _gapn2_half_debug2.py
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


def rho_left(hblocks, t):
	"""rho from the LEFT block at t (same convention as green_regularized)."""
	cums = [sum(b[0] for b in hblocks[:i + 1]) for i in range(len(hblocks))]
	return hblocks[min(int(np.searchsorted(cums, t)), len(hblocks) - 1)][1]


def rho_right(hblocks, t):
	cums = [sum(b[0] for b in hblocks[:i + 1]) for i in range(len(hblocks))]
	return hblocks[min(int(np.searchsorted(cums, t, side='right')), len(hblocks) - 1)][1]


def gprime_bracket(hblocks, mu, x, y, u0, vf):
	"""Bracket of G' without the rho(y) factor (continuous function H)."""
	I1x = _int_rho_u_v(hblocks, mu, x, u0)
	I2x = _int_rho_u2(hblocks, mu, x, u0)
	heaviside = 1.0 if x > y else 0.0
	return (u0 * _propagate(hblocks, mu, x)[0] * vf(y)
		- vf(x) * u0 * _propagate(hblocks, mu, y)[0]) * heaviside \
		- u0 * _propagate(hblocks, mu, x)[0] * u0 * _propagate(hblocks, mu, y)[0] * I1x \
		+ vf(x) * u0 * _propagate(hblocks, mu, y)[0] * I2x


def pbracket(hblocks, mu, y, u0, vf, A1, A2):
	"""Bracket of P without the rho(y) factor."""
	I1L = _int_rho_u_v(hblocks, mu, sum(b[0] for b in hblocks), u0)
	I1y = _int_rho_u_v(hblocks, mu, y, u0)
	I2y = _int_rho_u2(hblocks, mu, y, u0)
	return vf(y) * (1.0 - I2y) - u0 * _propagate(hblocks, mu, y)[0] * (A1 - A2 + I1L - I1y)


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
	print('blocks:', [(round(b[0], 9), b[1]) for b in hb])
	print('x1 =', repr(x1), 'x2 =', repr(x2), 'L =', L)
	eps = 1e-8
	for (name, mu, pole, bc) in [('D', muD[0], 0, 'D'), ('N', muN[1], 1, 'N')]:
		u0 = 1.0 / np.sqrt(_norm2(hb, mu, (0.0, 1.0)))
		vf = second_solution(hb, mu)
		print('--- %s mu=%.12f u0=%.9f ---' % (name, mu, u0))
		# A1/A2 at several quadrature orders
		for Nq in [4000, 40000, 400000]:
			g = np.linspace(0.0, L, Nq)
			u_g = np.array([u0 * _propagate(hb, mu, t)[0] for t in g])
			v_g = np.array([vf(t) for t in g])
			rho_g = np.array([rho_left(hb, t) for t in g])
			I1_g = np.array([_int_rho_u_v(hb, mu, t, u0) for t in g])
			I2_g = np.array([_int_rho_u2(hb, mu, t, u0) for t in g])
			A1 = np.trapz(rho_g * u_g ** 2 * I1_g, g)
			A2 = np.trapz(rho_g * u_g * v_g * I2_g, g)
			print('  Nq=%d: A1=%.12f A2=%.12f' % (Nq, A1, A2))
		# H(x, x_j) values at the two switch points (H2 diagnostic)
		g = np.linspace(0.0, L, 400000)
		u_g = np.array([u0 * _propagate(hb, mu, t)[0] for t in g])
		v_g = np.array([vf(t) for t in g])
		rho_g = np.array([rho_left(hb, t) for t in g])
		I1_g = np.array([_int_rho_u_v(hb, mu, t, u0) for t in g])
		I2_g = np.array([_int_rho_u2(hb, mu, t, u0) for t in g])
		A1 = np.trapz(rho_g * u_g ** 2 * I1_g, g)
		A2 = np.trapz(rho_g * u_g * v_g * I2_g, g)
		for yj in [x1, x2]:
			row = []
			for x in [x1, x2]:
				H = gprime_bracket(hb, mu, x, yj, u0, vf) \
					- u0 * _propagate(hb, mu, x)[0] * pbracket(hb, mu, yj, u0, vf, A1, A2)
				row.append(H)
			print('  H(x, y=%.6f) = %s' % (yj, ['%.4e' % r for r in row]))
		# spectral continuity across the jump at x2 (reference values)
		for yv in [x2 - eps, x2, x2 + eps]:
			sp11 = _spectral_green(hb, mu, pole, bc, x1, yv, N=80)
			sp22 = _spectral_green(hb, mu, pole, bc, x2, yv, N=80)
			print('  spectral y=%.9f: (x1,y)=%.8f (x2,y)=%.8f' % (yv, sp11, sp22))


if __name__ == '__main__':
	main()
