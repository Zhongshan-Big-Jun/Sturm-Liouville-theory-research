"""Verbatim function bodies from the pinned repository, not a whole-file copy.
Source: scripts/_gapn2_half_problem_probe.py, commit be7c0912849a50a46869773eab4b3a2ec655ce88.
The source file's Git blob is 502c1846dd45cabaf7caa72debaaed110189778c.
Only the numpy import and this provenance header were added.
"""
import numpy as np


def _secular_all(mu, hblocks, bc):
	"""Vectorized: BC value of the transfer-matrix solution u(0)=0, u'(0)=1."""
	A = np.zeros_like(mu)
	B = np.ones_like(mu)
	for (l, rho) in hblocks:
		k = np.sqrt(np.maximum(mu, 0.0) * rho)
		c = np.cos(k * l)
		s = np.sin(k * l)
		A2 = A * c + B * s / k
		B2 = -A * k * s + B * c
		A, B = A2, B2
	return A if bc == 'D' else B


def half_spectrum(hblocks, bc, N=60, mumax=None):
	"""Eigenvalues of -u'' = mu rho u on [0,L], u(0)=0, u'(L)=0 (N) or u(L)=0 (D).

	Coarse vectorized scan + bisection on sign-change brackets; grid spacing is
	chosen finer than the expected spacing between consecutive eigenvalues.
	"""
	L = sum(b[0] for b in hblocks)
	rho_min = min(b[1] for b in hblocks)
	if mumax is None:
		mumax = max(4.0 * np.pi ** 2 * (N + 2) ** 2 / L ** 2, 100.0)
	npts = max(4000, int(np.ceil(400.0 * np.sqrt(mumax))))
	mus = np.linspace(1e-8, mumax, npts)
	vals = _secular_all(mus, hblocks, bc)
	brackets = []
	for i in range(len(mus) - 1):
		if vals[i] == 0.0:
			brackets.append((mus[i], mus[i]))
		elif vals[i] * vals[i + 1] < 0:
			brackets.append((mus[i], mus[i + 1]))
	roots = []
	for (a, b) in brackets:
		if a == b:
			roots.append(a)
			continue
		fa = _secular_all(np.array([a]), hblocks, bc)[0]
		for _ in range(80):
			m = 0.5 * (a + b)
			fm = _secular_all(np.array([m]), hblocks, bc)[0]
			if fa * fm <= 0:
				b = m
			else:
				a = m
				fa = fm
		roots.append(0.5 * (a + b))
	roots = sorted(roots)
	out = np.array(roots[:N])
	# refine the first bracket pair only (roots are simple, spacing grows)
	return out


def _propagate(hblocks, mu, x):
	"""u (A), u' (B) of the solution with u(0)=0, u'(0)=1 at scalar x."""
	k_list = [(np.sqrt(max(mu, 0.0) * rho), l, rho) for (l, rho) in hblocks]
	A, B = 0.0, 1.0
	x0 = 0.0
	for (k, l, rho) in k_list:
		if x <= x0 + l + 1e-14:
			dx = x - x0
			c = np.cos(k * dx)
			s = np.sin(k * dx)
			return A * c + B * s / k, -A * k * s + B * c
		c = np.cos(k * l)
		s = np.sin(k * l)
		A2 = A * c + B * s / k
		B2 = -A * k * s + B * c
		A, B = A2, B2
		x0 += l
	dx = x - x0
	c = np.cos(k_list[-1][0] * dx)
	s = np.sin(k_list[-1][0] * dx)
	return A * c + B * s / k, -A * k * s + B * c


def _norm2(hblocks, mu, coefs, N=20000):
	"""Exact per-block L2(rho) integral of (A,B)-coefficient function u, u(0)=0,u'(0)=1.

	On a block of length l and wavenumber k with u = A C + (B/k) S:
	  int rho u^2 = rho[ A^2 (l/2 + sin(2kl)/(4k))
	                   + 2 A B/k * sin^2(kl)/(2k)
	                   + (B/k)^2 (l/2 - sin(2kl)/(4k)) ].
	"""
	A, B = coefs
	x0 = 0.0
	tot = 0.0
	for (l, rho) in hblocks:
		k = np.sqrt(max(mu, 0.0) * rho)
		c = np.cos(k * l)
		s = np.sin(k * l)
		A2n = A * c + B * s / k
		B2n = -A * k * s + B * c
		tot += rho * (A ** 2 * (l / 2 + np.sin(2 * k * l) / (4 * k))
			+ 2 * A * B / k * (s ** 2 / (2 * k))
			+ (B / k) ** 2 * (l / 2 - np.sin(2 * k * l) / (4 * k)))
		A, B = A2n, B2n
		x0 += l
	return tot


def _spectral_green(hblocks, mu, pole_idx, bc, x, y, N=80):
	"""Spectral sum of the half-problem regularized Green at (x,y)."""

	mus = half_spectrum(hblocks, bc, N=N)
	L = sum(b[0] for b in hblocks)
	# normalized eigenfunctions
	norms = np.array([np.sqrt(_norm2(hblocks, m, (0.0, 1.0))) for m in mus])
	out = 0.0
	for l in range(len(mus)):
		if l == pole_idx:
			continue
		ul = _propagate(hblocks, mus[l], x)[0] / norms[l]
		ul2 = _propagate(hblocks, mus[l], y)[0] / norms[l]
		out += ul * ul2 / (mus[l] - mu)
	return out
