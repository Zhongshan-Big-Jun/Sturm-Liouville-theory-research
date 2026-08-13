# -*- coding: utf-8 -*-
"""R-207: exact per-block closed forms for A1 = int rho u^2 I1 and
A2 = int rho u v I2 (I1 = int rho u v, I2 = int rho u^2), plus the corrected
regularized Green Gt = B - u(x)P(y) with NO rho(y) factor, checked against
Richardson-extrapolated spectral sums.

Primitive derivation (STRICT, elementary): on a block with wavenumber k,
C = cos(k xi), S = sin(k xi), c2 = cos(2k xi), s2 = sin(2k xi),
iCC = xi/2 + s2/(4k), iSS = xi/2 - s2/(4k), iCS = (1-c2)/(4k).  The nine
products (C^2,CS,S^2) x (iCC,iCS,iSS) integrate in closed form (see
_prims_9).  With u = aC+bS, v = cC+dS, prim_uv = ac iCC+(ad+bc)iCS+bd iSS,
prim_u2 = a^2 iCC+2ab iCS+b^2 iSS, the block contributions are
  A1 += rho [I1_0 int u^2 + rho * P3((a,b),(a,b),(ac,ad+bc,bd))],
  A2 += rho [I2_0 int u v + rho * P3((a,b),(c,d),(a^2,2ab,b^2))],
where P3 folds the nine primitives with the quadratic-form coefficients.

All numerics EVIDENCE.
Usage: python _gapn2_half_debug4.py
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum, _norm2,
	_propagate, second_solution, _int_rho_u_v, _int_rho_u2)


def _prims_9(l, k):
	"""Integrals over [0,l] of C^2/S^2/CS times iCC/iCS/iSS.

	Returns dict keyed by ('C2','iCC') etc.
	"""
	s2 = np.sin(2.0 * k * l)
	c2 = np.cos(2.0 * k * l)
	s4 = np.sin(4.0 * k * l)
	c4 = np.cos(4.0 * k * l)
	l2 = l * l
	o = {}
	o['C2,iCC'] = l2 / 8.0 + l * s2 / (8.0 * k) + (1.0 - c4) / (64.0 * k * k)
	o['C2,iSS'] = l2 / 8.0 + l * s2 / (8.0 * k) + (c2 - 1.0) / (8.0 * k * k) \
		- (1.0 - c4) / (64.0 * k * k)
	o['C2,iCS'] = l / (16.0 * k) - s4 / (64.0 * k * k)
	o['CS,iCC'] = -l * c2 / (8.0 * k) + s2 / (16.0 * k * k) + l / (16.0 * k) \
		- s4 / (64.0 * k * k)
	o['CS,iSS'] = -l * c2 / (8.0 * k) + s2 / (16.0 * k * k) - l / (16.0 * k) \
		+ s4 / (64.0 * k * k)
	o['CS,iCS'] = -(c2 - 1.0) / (16.0 * k * k) + (c4 - 1.0) / (64.0 * k * k)
	o['S2,iCC'] = l2 / 8.0 - l * s2 / (8.0 * k) - (c2 - 1.0) / (8.0 * k * k) \
		- (1.0 - c4) / (64.0 * k * k)
	o['S2,iSS'] = l2 / 8.0 - l * s2 / (8.0 * k) + (1.0 - c4) / (64.0 * k * k)
	o['S2,iCS'] = 3.0 * l / (16.0 * k) - s2 / (8.0 * k * k) + s4 / (64.0 * k * k)
	return o


def _fold3(pr, p1, p2, r):
	"""int (p1.C+p2.S)(q1.C+q2.S)(r1 iCC + r2 iCS + r3 iSS) over [0,l]."""
	(a, b) = p1
	(c, d) = p2
	(r1, r2, r3) = r
	cc = a * c
	cs = a * d + b * c
	ss = b * d
	out = 0.0
	for (cfs, base) in [(cc, 'C2'), (cs, 'CS'), (ss, 'S2')]:
		out += cfs * (r1 * pr['%s,iCC' % base]
			+ r2 * pr['%s,iCS' % base] + r3 * pr['%s,iSS' % base])
	return out


def _a1a2_exact(hblocks, mu, u0):
	"""Exact A1, A2 via per-block closed primitives (float64 roundoff only)."""
	uA, uB = 0.0, 1.0
	vA, vB = -1.0 / u0, 0.0
	I1 = 0.0
	I2 = 0.0
	A1 = 0.0
	A2 = 0.0
	for (l, rho) in hblocks:
		k = np.sqrt(max(mu, 0.0) * rho)
		# normalized u: a = u(x0), b = u'(x0)/k ; v: c = v(x0), d = v'(x0)/k
		a = u0 * uA
		b = u0 * uB / k
		c = vA
		d = vB / k
		pr = _prims_9(l, k)
		iCC = l / 2.0 + np.sin(2.0 * k * l) / (4.0 * k)
		iCS = np.sin(k * l) ** 2 / (2.0 * k)
		iSS = l / 2.0 - np.sin(2.0 * k * l) / (4.0 * k)
		int_u2 = a * a * iCC + 2.0 * a * b * iCS + b * b * iSS
		int_uv = a * c * iCC + (a * d + b * c) * iCS + b * d * iSS
		A1 += rho * (I1 * int_u2 + rho * _fold3(pr, (a, b), (a, b), (a * c, a * d + b * c, b * d)))
		A2 += rho * (I2 * int_uv + rho * _fold3(pr, (a, b), (c, d), (a * a, 2.0 * a * b, b * b)))
		# advance block-start coefficients and running integrals
		c1 = np.cos(k * l)
		s1 = np.sin(k * l)
		uA2 = uA * c1 + uB * s1 / k
		uB2 = -uA * k * s1 + uB * c1
		vA2 = vA * c1 + vB * s1 / k
		vB2 = -vA * k * s1 + vB * c1
		uA, uB = uA2, uB2
		vA, vB = vA2, vB2
		I1 += rho * int_uv
		I2 += rho * int_u2
	return A1, A2


def _a1a2_trapz(hblocks, mu, u0, vf, Nq):
	L = sum(b[0] for b in hblocks)
	cums = [sum(b[0] for b in hblocks[:i + 1]) for i in range(len(hblocks))]
	g = np.linspace(0.0, L, Nq)
	rho_g = np.array([hblocks[min(int(np.searchsorted(cums, t)), len(hblocks) - 1)][1] for t in g])
	u_g = np.array([u0 * _propagate(hblocks, mu, t)[0] for t in g])
	v_g = np.array([vf(t) for t in g])
	I1_g = np.array([_int_rho_u_v(hblocks, mu, t, u0) for t in g])
	I2_g = np.array([_int_rho_u2(hblocks, mu, t, u0) for t in g])
	return np.trapz(rho_g * u_g ** 2 * I1_g, g), np.trapz(rho_g * u_g * v_g * I2_g, g)


def bracket(hblocks, mu, x, y, u0, vf):
	I1x = _int_rho_u_v(hblocks, mu, x, u0)
	I2x = _int_rho_u2(hblocks, mu, x, u0)
	heaviside = 1.0 if x > y else 0.0
	return (u0 * _propagate(hblocks, mu, x)[0] * vf(y)
		- vf(x) * u0 * _propagate(hblocks, mu, y)[0]) * heaviside \
		- u0 * _propagate(hblocks, mu, x)[0] * u0 * _propagate(hblocks, mu, y)[0] * I1x \
		+ vf(x) * u0 * _propagate(hblocks, mu, y)[0] * I2x


def _richardson(seq):
	"""seq = [S_N, S_2N]; return 2*S_2N - S_N (tail ~ 1/N -> O(1/N^2))."""
	return 2.0 * seq[1] - seq[0]


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
	muD = half_spectrum(hb, 'D', N=340)
	muN = half_spectrum(hb, 'N', N=340)
	x1 = w[0]
	x2 = w[0] + w[1]
	for (name, mu, pole, bc) in [('D', muD[0], 0, 'D'), ('N', muN[1], 1, 'N')]:
		u0 = 1.0 / np.sqrt(_norm2(hb, mu, (0.0, 1.0)))
		vf = second_solution(hb, mu)
		A1e, A2e = _a1a2_exact(hb, mu, u0)
		A1t, A2t = _a1a2_trapz(hb, mu, u0, vf, 200000)
		print('--- %s mu=%.12f ---' % (name, mu))
		print('  A1 exact=%.12f trapz=%.12f diff=%.3e' % (A1e, A1t, A1e - A1t))
		print('  A2 exact=%.12f trapz=%.12f diff=%.3e' % (A2e, A2t, A2e - A2t))
		I1L = _int_rho_u_v(hb, mu, L, u0)

		def Gt_cf(x, y):
			I1y = _int_rho_u_v(hb, mu, y, u0)
			I2y = _int_rho_u2(hb, mu, y, u0)
			P = vf(y) * (1.0 - I2y) - u0 * _propagate(hb, mu, y)[0] * (A1e - A2e + I1L - I1y)
			return bracket(hb, mu, x, y, u0, vf) - u0 * _propagate(hb, mu, x)[0] * P
		# spectral reference with Richardson in N
		pts = [(x1, x1), (x1, x2), (x2, x2)]
		best = {}
		for Nref in [80, 160, 320]:
			norm_ref = np.array([np.sqrt(_norm2(hb, m, (0.0, 1.0))) for m in muD]) if bc == 'D' \
				else np.array([np.sqrt(_norm2(hb, m, (0.0, 1.0))) for m in muN])
			mus = muD if bc == 'D' else muN
			vals = {}
			for (a, b) in pts:
				out = 0.0
				for l in range(Nref):
					if l == pole:
						continue
					ua = _propagate(hb, mus[l], a)[0] / norm_ref[l]
					ub = _propagate(hb, mus[l], b)[0] / norm_ref[l]
					out += ua * ub / (mus[l] - mu)
				vals[(a, b)] = out
			best[Nref] = vals
		for (a, b) in pts:
			cf = Gt_cf(a, b)
			sp80 = best[80][(a, b)]
			sp160 = best[160][(a, b)]
			rich = _richardson([sp80, sp160])
			print('  Gt(%8.5f,%8.5f): cf=%.12f sp80=%.12f rich=%.12f'
				% (a, b, cf, sp80, rich))
			print('     cf-sp80 = %.3e, cf-rich = %.3e' % (cf - sp80, cf - rich))
		print('  symmetry: %.3e' % abs(Gt_cf(x2, x1) - Gt_cf(x1, x2)))


if __name__ == '__main__':
	main()
