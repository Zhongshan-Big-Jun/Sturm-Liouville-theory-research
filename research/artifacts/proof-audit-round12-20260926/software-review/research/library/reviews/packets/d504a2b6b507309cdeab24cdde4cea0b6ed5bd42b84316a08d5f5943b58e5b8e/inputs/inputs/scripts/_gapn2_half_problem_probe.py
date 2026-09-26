# -*- coding: utf-8 -*-
"""R-207: n=2 half-problem Green functions and separately named K/Kp sectors.

The symmetric band-consistent configuration for n=2 has 2n+1 = 5 blocks with
mirror = center of the middle block.  The left half [0, 1/2] carries n+1 = 3
blocks:
  SUP [1 w0][R w1][1 w2/2],   INF [R w0][1 w1][R w2/2].
Even full eigenfunctions restrict to the Neumann half problem (u'(1/2)=0),
odd to the Dirichlet half problem (u(1/2)=0).  For n=2 (n even):
  lam_2 = mu_1^D,   lam_3 = mu_2^N,
The cross-parity R-205 reduction represents the odd block of Kp=S K S,
equal to E Ke E, with E=diag(1,-1), NOT the odd block Ko of raw K.

STRICT closed-form derivation (corrected 2026-08-13, R-207):
- Variation of parameters for L_x = -d^2/dx^2 - mu rho(x) with h(x) =
  delta(x-y) - rho(x)u(x)u(y) gives the particular solution WITHOUT any
  rho(y) factor:
      B(x,y) = (u(x)v(y) - v(x)u(y)) 1_{x>y}
               - u(x)u(y) I1(x) + v(x)u(y) I2(x),
      I1(x) = int_0^x rho u v dt,  I2(x) = int_0^x rho u^2 dt,
  with u the normalized eigenfunction, v the second solution (W(u,v)=1),
  v(0) = -1/u'(0).  Then L_x B = delta(x-y) - rho(x)u(x)u(y) (STRICT).
- Projection onto {u}^perp with P(y) = <rho u, B(.,y)> (NO rho(y) factor):
      P(y) = v(y)(1 - I2(y)) - u(y)[A1 - A2 + I1(L) - I1(y)],
      A1 = int_0^L rho u^2 I1 dx,  A2 = int_0^L rho u v I2 dx.
  Gt_k = B - u(x)P(y) is then the reduced resolvent kernel of the half
  problem at its own eigenvalue mu_k (pole removed).  A1, A2 are computed
  EXACTLY by per-block closed primitives (_a1a2_exact, elementary trig
  antiderivatives; STRICT).
- Earlier draft with the extra rho(y) factors in B and P is RETRACTED: it
  is discontinuous at density jumps and wrong off the diagonal; the
  constant-density check could not detect the bug because rho(y)=1 there.

Checks:
  C1: interleaving mu_1^N < mu_1^D < mu_2^N < mu_2^D and lam_2 = mu_1^D,
      lam_3 = mu_2^N; self-test on the constant-density half string.
  C2: CLOSED-FORM regularized Green functions of the half problems at their
      own eigenvalue vs Richardson-extrapolated spectral sums:
        Gt_D(mu_1^D), Gt_N(mu_2^N),
      and the FULL (no-pole) Green functions at the cross eigenvalue:
        G_D(mu_2^N), G_N(mu_1^D) (exact closed forms).
  C3: odd sector of Kp at the symmetric root, two assemblies of the SAME
      object, plus convention checks:
      (i)  R-205 form: M = lam_3 eps (G_D(mu_2^N)/2) eps - lam_2 G_N(mu_1^D)/2,
           Kp_odd = diag(d) + (4 lam_2/lam_3) diag(u) M diag(u);
      (ii) collapsed-global form (R-206, STRICT identity): with the rank
           term r vv^T mirror-even (drops out of the odd sector) and the
           mirror projection of S = eps Gt_{n+1} eps - c^2 Gt_n equal to
           Be^T S Be = G_D(mu_2^N) o ee^T - c^2 G_N(mu_1^D),  e = (1,-1),
           c^2 = lam_2/lam_3:
           Kp_odd = diag(d) + 2 lam_2 diag(u)[G_D o ee^T - c^2 G_N]diag(u).
      These are compared against Po Kp_full Po^T and E Ke E. Raw Ko is
      separately reconstructed from same-parity reduced kernels and its
      surviving rank-one term, then compared against raw spectral/FD Ko.

Closed-form ingredients: fundamental solutions u (normalized eigenfunction),
v (W(u,v)=1), exact per-block I1/I2 primitives, exact A1/A2 (_a1a2_exact).
All numerics EVIDENCE.
Usage: python _gapn2_half_problem_probe.py [R] [mode] [N]
"""
import sys
import json
from dataclasses import dataclass
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
from _sl_prufer import indexed_roots, positive_blocks


def _positive_count(Value, Name):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, (int, np.integer)) or Value < 1:
		raise ValueError(Name + ' must be a positive integer')
	return int(Value)


@dataclass(frozen=True, init=False)
class HalfSpectrum:
	"""Immutable numerical mode table, bound to exact binary64 blocks and BC.

	Mode numbers are one-based. The error radii are floating diagnostics, not
	rigorous error bounds. Construct from the equation, never from scan hits.
	"""
	blocks: tuple
	boundary: str
	eigenvalues: tuple
	error_radii: tuple
	phase_records: tuple

	def __init__(self, Blocks, Boundary, Count):
		Values = positive_blocks(Blocks)
		Frequencies, Records = indexed_roots(Values, Count, RightBoundary=Boundary)
		with np.errstate(over='ignore', under='ignore', invalid='ignore'):
			Eigenvalues = Frequencies ** 2
			Brackets = np.array([Record['bracket'] for Record in Records]) ** 2
			Radii = np.maximum(Eigenvalues - Brackets[:, 0], Brackets[:, 1] - Eigenvalues)
			Radii += 8 * np.finfo(float).eps * Eigenvalues
		if (not np.all(np.isfinite(Eigenvalues)) or np.any(Eigenvalues <= 0)
			or np.any(np.diff(Eigenvalues) <= 0) or not np.all(np.isfinite(Radii))
			or np.any(np.diff(Eigenvalues) <= 4 * (Radii[:-1] + Radii[1:]))):
			raise ArithmeticError('half eigenvalues are not numerically resolvable')
		object.__setattr__(self, 'blocks', tuple(tuple(map(float, Block)) for Block in Values))
		object.__setattr__(self, 'boundary', Boundary)
		object.__setattr__(self, 'eigenvalues', tuple(map(float, Eigenvalues)))
		object.__setattr__(self, 'error_radii', tuple(map(float, Radii)))
		object.__setattr__(self, 'phase_records', tuple(tuple((Key, tuple(Value) if isinstance(Value, list) else Value)
			for Key, Value in sorted(Record.items())) for Record in Records))

	def prefix(self, Count):
		Count = _positive_count(Count, 'prefix count')
		if Count > len(self.eigenvalues):
			raise ValueError('requested prefix exceeds the indexed table')
		return np.array(self.eigenvalues[:Count])


def half_blocks(rc, w):
	"""Left-half blocks of the symmetric 2n+1-block configuration."""
	pat = rc.pat
	n = rc.n
	hs = []
	for i in range(n + 1):
		if i < n:
			hs.append((w[i], pat[i]))
		else:
			hs.append((w[n] / 2.0, pat[n]))
	return hs


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


def half_spectrum(hblocks, bc, N=60, mumax=None, *, return_table=False):
	"""Eigenvalues of -u'' = mu rho u on [0,L], u(0)=0, u'(L)=0 (N) or u(L)=0 (D).

	Use indexed lifted phase levels. The first N modes are independent of the
	requested total count. mumax, when given, is a ceiling that must contain
	all N modes; it never silently truncates the output. Not a certificate.
	"""
	Table = HalfSpectrum(hblocks, bc, N)
	if mumax is not None:
		if np.iscomplexobj(mumax) or not np.isscalar(mumax) or not np.isfinite(mumax) or mumax <= 0:
			raise ValueError('mumax must be finite and positive')
		if Table.eigenvalues[-1] > mumax:
			raise ValueError('mumax does not contain the requested indexed modes')
	return Table if return_table else Table.prefix(N)


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


def eigen_half(hblocks, mu, bc, Nnorm=20000):
	"""Normalized eigenfunction u of the half problem at mu: u(0)=0, u'(0)=u0>0."""
	u0 = 1.0 / np.sqrt(_norm2(hblocks, mu, (0.0, 1.0)))
	return lambda x: u0 * _propagate(hblocks, mu, x)[0]


def second_solution(hblocks, mu):
	"""v with W(u,v) = 1: v(0) = -1/u'(0), v'(0) = 0 (gauge-fixed)."""
	L = sum(b[0] for b in hblocks)
	u0 = 1.0 / np.sqrt(_norm2(hblocks, mu, (0.0, 1.0)))
	v0 = -1.0 / u0
	A, B = v0, 0.0
	x0 = 0.0
	coefs = [(A, B)]
	for (l, rho) in hblocks:
		k = np.sqrt(max(mu, 0.0) * rho)
		c = np.cos(k * l)
		s = np.sin(k * l)
		A2 = A * c + B * s / k
		B2 = -A * k * s + B * c
		A, B = A2, B2
		x0 += l
		coefs.append((A, B))

	def v(x):
		blk = 0
		xb = 0.0
		for i, (l, rho) in enumerate(hblocks):
			if x <= xb + l + 1e-14:
				dx = x - xb
				k = np.sqrt(max(mu, 0.0) * rho)
				c = np.cos(k * dx)
				s = np.sin(k * dx)
				a, b = coefs[i]
				return a * c + b * s / k
			xb += l
		return 0.0
	return v


def _int_rho_u2(hblocks, mu, x, uA_u0=1.0):
	"""Exact int_0^x rho u^2 dt for the fundamental solution (A,B)=(0,1) scaled by uA_u0^2.

	I2 in the run-notes derivation.  Uses the same closed block primitives."""
	A, B = 0.0, 1.0
	x0 = 0.0
	tot = 0.0
	for (l, rho) in hblocks:
		if x <= x0 + l + 1e-14:
			dx = x - x0
			k = np.sqrt(max(mu, 0.0) * rho)
			c = np.cos(k * dx)
			s = np.sin(k * dx)
			A2 = A * c + B * s / k
			B2 = -A * k * s + B * c
			tot += rho * (A ** 2 * (dx / 2 + np.sin(2 * k * dx) / (4 * k))
				+ 2 * A * B / k * (s ** 2 / (2 * k))
				+ (B / k) ** 2 * (dx / 2 - np.sin(2 * k * dx) / (4 * k)))
			return tot * uA_u0 ** 2
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
	return tot * uA_u0 ** 2


def _int_rho_u_v(hblocks, mu, x, uA_u0=1.0):
	"""Exact int_0^x rho u v dt (u fundamental (0,1), v second solution), I1 in notes."""
	uA, uB = 0.0, 1.0
	vA, vB = -1.0 / uA_u0, 0.0
	x0 = 0.0
	tot = 0.0
	for (l, rho) in hblocks:
		if x <= x0 + l + 1e-14:
			dx = x - x0
			k = np.sqrt(max(mu, 0.0) * rho)
			c = np.cos(k * dx)
			s = np.sin(k * dx)
			# u at dx: A c + (B/k) s ; v at dx: a c + (b/k) s
			return (tot + rho * _mixed_prim(dx, k, uA, uB / k, vA, vB / k)) * uA_u0
		k = np.sqrt(max(mu, 0.0) * rho)
		c = np.cos(k * l)
		s = np.sin(k * l)
		uA2 = uA * c + (uB / k) * s
		uB2 = -uA * k * s + uB * c
		vA2 = vA * c + (vB / k) * s
		vB2 = -vA * k * s + vB * c
		tot += rho * _mixed_prim(l, k, uA, uB / k, vA, vB / k)
		uA, uB = uA2, uB2
		vA, vB = vA2, vB2
		x0 += l
	return tot * uA_u0


def _mixed_prim(l, k, A, Ab, C, Cb):
	"""int_0^l (A Cx + Ab Sx)(C Cx + Cb Sx) dx with Cx=cos(kx), Sx=sin(kx)."""
	# int C^2 = l/2 + sin(2kl)/(4k); int S^2 = l/2 - sin(2kl)/(4k); int CS = sin^2(kl)/(2k)
	iCC = l / 2 + np.sin(2 * k * l) / (4 * k)
	iSS = l / 2 - np.sin(2 * k * l) / (4 * k)
	iCS = np.sin(k * l) ** 2 / (2 * k)
	return A * C * iCC + (A * Cb + Ab * C) * iCS + Ab * Cb * iSS


def green_regular(hblocks, mu, x, y, bc):
	"""Full Green function at non-eigenvalue mu: phi(x_<) psi(x_>)/W."""
	L = sum(b[0] for b in hblocks)
	# phi: u(0)=0, u'(0)=1; psi: right BC, propagate leftwards
	k_list = [(np.sqrt(max(mu, 0.0) * rho), l) for (l, rho) in hblocks]

	def psi(t):
		# propagate from x=L leftwards; D: psi(L)=0, psi'(L)=-1; N: psi(L)=1, psi'(L)=0
		if bc == 'D':
			A, B = 0.0, -1.0
		else:
			A, B = 1.0, 0.0
		xx = L
		for (k, l) in reversed(k_list):
			xx -= l
			if t >= xx - 1e-14:
				dx = t - (xx + l)
				c = np.cos(k * dx)
				s = np.sin(k * dx)
				return A * c + B * s / k, -A * k * s + B * c
			c = np.cos(k * l)
			s = np.sin(k * l)
			A2 = A * c - B * s / k
			B2 = A * k * s + B * c
			A, B = A2, B2
		return A, B
	# Wronskian phi psi' - phi' psi (constant in x)
	xm = L / 2
	p1 = _propagate(hblocks, mu, xm)
	ps, psp = psi(xm)
	W = p1[1] * ps - p1[0] * psp
	if x <= y:
		return _propagate(hblocks, mu, x)[0] * psi(y)[0] / W
	return _propagate(hblocks, mu, y)[0] * psi(x)[0] / W


def _prims_9(l, k):
	"""Closed integrals over [0,l] of C^2/S^2/CS times iCC/iCS/iSS (STRICT).

	C = cos(k xi), S = sin(k xi), iCC = xi/2 + sin(2kxi)/(4k),
	iSS = xi/2 - sin(2kxi)/(4k), iCS = (1-cos(2kxi))/(4k).
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
	"""Exact A1, A2 via per-block closed primitives (STRICT algebra, float64)."""
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


def green_regularized(hblocks, mu, x, y, bc):
	"""Regularized Green at the eigenvalue mu (pole removed): Gt_k(x,y).

	Closed form: Gt = B - u(x)P(y) (see module docstring), exact A1/A2.
	"""
	L = sum(b[0] for b in hblocks)
	u0 = 1.0 / np.sqrt(_norm2(hblocks, mu, (0.0, 1.0)))
	uf = lambda t: u0 * _propagate(hblocks, mu, t)[0]
	vf = second_solution(hblocks, mu)
	A1, A2 = _a1a2_exact(hblocks, mu, u0)

	def B(a, b):
		I1a = _int_rho_u_v(hblocks, mu, a, u0)
		I2a = _int_rho_u2(hblocks, mu, a, u0)
		heaviside = 1.0 if a > b else 0.0
		return (uf(a) * vf(b) - vf(a) * uf(b)) * heaviside \
			- uf(a) * uf(b) * I1a + vf(a) * uf(b) * I2a
	I1L = _int_rho_u_v(hblocks, mu, L, u0)
	I1y = _int_rho_u_v(hblocks, mu, y, u0)
	I2y = _int_rho_u2(hblocks, mu, y, u0)
	P = vf(y) * (1.0 - I2y) - uf(y) * (A1 - A2 + I1L - I1y)
	return B(x, y) - uf(x) * P


def _full_S(rc, zs, ed, N=1500):
	"""Full 2n x 2n collapsed S = eps Gt_{n+1} eps - (lam_n/lam_{n+1}) Gt_n (spectral)."""
	blocks = rc.blocks_from_z(zs)
	ss = roots_of(blocks, N + 1)
	x = ed['edges']
	m = len(x)
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	eps = ed['eps']
	Gn = np.zeros((m, m))
	Gnp1 = np.zeros((m, m))
	for l in range(N + 1):
		ul = eigfun(blocks, ss[l], x)
		if l != rc.n - 1:
			Gn += np.outer(ul, ul) / (ss[l] ** 2 - lam_n)
		if l != rc.n:
			Gnp1 += np.outer(ul, ul) / (ss[l] ** 2 - lam_np1)
	return np.diag(eps) @ Gnp1 @ np.diag(eps) - (lam_n / lam_np1) * Gn


def _green_table(hblocks, bc, N, Spectrum):
	Count = _positive_count(N, 'spectral truncation')
	Blocks = tuple(tuple(map(float, Block)) for Block in positive_blocks(hblocks))
	if Spectrum is None:
		Spectrum = HalfSpectrum(Blocks, bc, Count)
	if not isinstance(Spectrum, HalfSpectrum):
		raise ValueError('spectrum must be an indexed HalfSpectrum table')
	if Spectrum.blocks != Blocks or Spectrum.boundary != bc:
		raise ValueError('spectral table geometry or boundary does not match the equation')
	return Spectrum, Spectrum.prefix(Count)


def _green_sum(Table, Mu, X, Y, Count, PoleMode=None):
	"""Finite sum with validated one-based pole identity and resolvability."""
	for Value, Name in ((Mu, 'mu'), (X, 'x'), (Y, 'y')):
		if np.iscomplexobj(Value) or not np.isscalar(Value) or not np.isfinite(Value):
			raise ValueError(Name + ' must be a finite real scalar')
	Length = sum(Block[0] for Block in Table.blocks)
	if not (0 <= X <= Length and 0 <= Y <= Length):
		raise ValueError('Green evaluation point lies outside the half interval')
	AllModes = np.array(Table.eigenvalues)
	Tolerance = 4 * np.array(Table.error_radii) + 16 * np.finfo(float).eps * abs(Mu)
	Near = np.abs(AllModes - Mu) <= Tolerance
	if PoleMode is not None:
		PoleMode = _positive_count(PoleMode, 'one-based pole mode')
		if PoleMode > Count:
			raise ValueError('pole mode is outside the requested prefix')
		if np.flatnonzero(Near).tolist() != [PoleMode - 1]:
			raise ValueError('target eigenvalue does not uniquely match the specified pole mode')
	else:
		if np.any(Near):
			raise ValueError('full Green target is at or numerically near a tabulated pole')
		if Mu >= AllModes[-1] - Tolerance[-1]:
			raise ValueError('full Green target requires a larger table to resolve its spectral location')
	Modes = Table.prefix(Count)
	Keep = np.ones(Count, dtype=bool)
	if PoleMode is not None:
		Keep[PoleMode - 1] = False
	Denominators = Modes[Keep] - Mu
	if np.any(np.abs(Denominators) <= Tolerance[:Count][Keep]):
		raise ArithmeticError('retained spectral denominator is not resolvable')
	with np.errstate(divide='raise', invalid='raise', over='raise', under='ignore'):
		Norms = np.array([_norm2(Table.blocks, Value, (0.0, 1.0)) for Value in Modes[Keep]])
		if not np.all(np.isfinite(Norms)) or np.any(Norms <= 0):
			raise ArithmeticError('half-eigenfunction normalization is not resolvable')
		Left = np.array([_propagate(Table.blocks, Value, X)[0] for Value in Modes[Keep]])
		Right = np.array([_propagate(Table.blocks, Value, Y)[0] for Value in Modes[Keep]])
		Result = np.sum((Left / np.sqrt(Norms)) * (Right / np.sqrt(Norms)) / Denominators)
	if not np.isfinite(Result):
		raise ArithmeticError('Green spectral sum is not finite')
	return float(Result)


def _spectral_green(hblocks, mu, pole_idx, bc, x, y, N=80, *, spectrum=None):
	"""Reduced finite sum; legacy zero-based pole_idx is checked as mode idx+1.

	Pass the same table for N and 2N comparisons. When omitted, deterministic
	phase indexing constructs it and still verifies the target/pole identity.
	"""
	if isinstance(pole_idx, (bool, np.bool_)) or not isinstance(pole_idx, (int, np.integer)) or pole_idx < 0:
		raise ValueError('pole_idx must be a nonnegative integer')
	Table, Modes = _green_table(hblocks, bc, N, spectrum)
	return _green_sum(Table, mu, x, y, len(Modes), PoleMode=int(pole_idx) + 1)


def _spectral_full_green(hblocks, mu, bc, x, y, N=80, *, spectrum=None):
	"""Unreduced finite sum; target must be away from poles within the table."""
	Table, Modes = _green_table(hblocks, bc, N, spectrum)
	return _green_sum(Table, mu, x, y, len(Modes))


def _richardson(seq):
	"""seq = [S_N, S_2N]; return 2*S_2N - S_N (tail ~ 1/N -> O(1/N^2))."""
	return 2.0 * seq[1] - seq[0]


def main():
	R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
	mode = sys.argv[2] if len(sys.argv) > 2 else 'inf'
	N = int(sys.argv[3]) if len(sys.argv) > 3 else 80
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	key = 'n2_%s' % mode.upper()
	e0 = np.array(tab[key]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	z0 = rc0.widths_to_z(w0)
	rc = Recon(2, R, mode)
	zs = symmetric_root(rc, z0)
	ed = eigen_data(rc, zs)
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	edges = ed['edges']
	w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
	hb = half_blocks(rc, w)
	print('=== n=2 R=%g mode=%s: lam_2=%.8f lam_3=%.8f ==='
		% (R, mode, lam_n, lam_np1))
	print('    half blocks:', [(round(b[0], 8), b[1]) for b in hb])
	# C0 self-test: constant density 1 on [0, L]
	L = sum(b[0] for b in hb)
	muD1 = half_spectrum([(L, 1.0)], 'D', N=4)
	muN1 = half_spectrum([(L, 1.0)], 'N', N=4)
	exD = np.array([(k + 1) ** 2 * np.pi ** 2 / L ** 2 for k in range(4)])
	exN = np.array([(k + 0.5) ** 2 * np.pi ** 2 / L ** 2 for k in range(4)])
	print('C0 constant-density self-test: muD err=%.3e muN err=%.3e'
		% (np.max(np.abs(muD1 - exD)), np.max(np.abs(muN1 - exN))))
	TableD = half_spectrum(hb, 'D', N=2 * N, return_table=True)
	TableN = half_spectrum(hb, 'N', N=2 * N, return_table=True)
	muD = TableD.prefix(2 * N)
	muN = TableN.prefix(2 * N)
	print('C1 muD[:4] =', np.round(muD[:4], 8))
	print('   muN[:4] =', np.round(muN[:4], 8))
	print('   |lam_2 - mu_1^D| = %.3e, |lam_3 - mu_2^N| = %.3e'
		% (abs(lam_n - muD[0]), abs(lam_np1 - muN[1])))
	print('   interleaving mu_1^N < mu_1^D < mu_2^N < mu_2^D:',
		muN[0] < muD[0] < muN[1] < muD[1])
	# left-half switches
	x1 = w[0]
	x2 = w[0] + w[1]
	xs = [x1, x2]
	# C2: closed form vs Richardson-extrapolated spectral sums
	pts = [(x1, x1), (x1, x2), (x2, x2)]
	GtD_cf = np.zeros((2, 2))
	GtD_sp = np.zeros((2, 2))
	GtN_cf = np.zeros((2, 2))
	GtN_sp = np.zeros((2, 2))
	GD_cf = np.zeros((2, 2))
	GD_sp = np.zeros((2, 2))
	GN_cf = np.zeros((2, 2))
	GN_sp = np.zeros((2, 2))
	for (i, j) in [(0, 0), (0, 1), (1, 1)]:
		a, b = xs[i], xs[j]
		GtD_cf[i, j] = green_regularized(hb, muD[0], a, b, 'D')
		GtN_cf[i, j] = green_regularized(hb, muN[1], a, b, 'N')
		GD_cf[i, j] = green_regular(hb, muN[1], a, b, 'D')
		GN_cf[i, j] = green_regular(hb, muD[0], a, b, 'N')
		seqD = [_spectral_green(hb, muD[0], 0, 'D', a, b, N=nn, spectrum=TableD) for nn in (N, 2 * N)]
		seqN = [_spectral_green(hb, muN[1], 1, 'N', a, b, N=nn, spectrum=TableN) for nn in (N, 2 * N)]
		seqGD = [_spectral_full_green(hb, muN[1], 'D', a, b, N=nn, spectrum=TableD) for nn in (N, 2 * N)]
		seqGN = [_spectral_full_green(hb, muD[0], 'N', a, b, N=nn, spectrum=TableN) for nn in (N, 2 * N)]
		GtD_sp[i, j] = _richardson(seqD)
		GtN_sp[i, j] = _richardson(seqN)
		GD_sp[i, j] = _richardson(seqGD)
		GN_sp[i, j] = _richardson(seqGN)
	for (M_cf, M_sp) in ((GtD_cf, GtD_sp), (GtN_cf, GtN_sp), (GD_cf, GD_sp), (GN_cf, GN_sp)):
		M_cf[1, 0] = M_cf[0, 1]
		M_sp[1, 0] = M_sp[0, 1]
	print('C2 closed-form vs Richardson spectral (regularized at own pole):')
	print('   Gt_D: max err = %.3e' % np.max(np.abs(GtD_cf - GtD_sp)))
	print('   Gt_N: max err = %.3e' % np.max(np.abs(GtN_cf - GtN_sp)))
	print('C2 full Green at cross eigenvalue:')
	print('   G_D(mu_2^N): max err = %.3e' % np.max(np.abs(GD_cf - GD_sp)))
	print('   G_N(mu_1^D): max err = %.3e' % np.max(np.abs(GN_cf - GN_sp)))
	# C3: cross-parity Kp_odd and raw Ko have different kernel formulas.
	eps = ed['eps']
	Wv = ed['W']
	c = ed['c']
	sig = 1.0 if mode == 'sup' else -1.0
	d = sig * 2.0 * c * np.abs(Wv) / (R - 1.0)
	u = ed['u_n']
	sd = sector_data(rc, zs, N=121)
	Ko_ref = np.array(sd['Ko'])
	Ke_ref = np.array(sd['Ke'])
	Po = np.array([[1, 0, 0, -1], [0, 1, -1, 0]]) / np.sqrt(2.0)
	Pe = np.array([[1, 0, 0, 1], [0, 1, 1, 0]]) / np.sqrt(2.0)
	# (i) R-205 form: M = lam_3 eps (G_D/2) eps - lam_2 (G_N/2)
	E2 = np.diag(eps[:2])
	M = lam_np1 * (E2 @ (0.5 * GD_cf) @ E2) - lam_n * (0.5 * GN_cf)
	KpOddR205 = np.diag(d[:2]) + (4.0 * lam_n / lam_np1) * np.diag(u[:2]) @ M @ np.diag(u[:2])
	# (ii) collapsed-global form (R-206): odd sector of Kp; the rank term
	#     r vv^T drops out (v mirror-even on the symmetric branch) and the
	#     mirror projection gives Be^T S Be = G_D o ee^T - c^2 G_N, e=(1,-1).
	c2 = lam_n / lam_np1
	e = np.array([1.0, -1.0])
	BeSBe = GD_cf * np.outer(e, e) - c2 * GN_cf
	Kp_odd = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ BeSBe @ np.diag(u[:2])
	v = u ** 2
	r = 2.0 * lam_n * (lam_np1 - lam_n) / lam_np1 ** 2
	Kp_full = np.diag(d) + r * np.outer(v, v) \
		+ 2.0 * lam_n * np.diag(u) @ _full_S(rc, zs, ed) @ np.diag(u)
	RankVector = E2 @ (u[:2] ** 2)
	KoClosed = (np.diag(d[:2]) + 4.0 * lam_n * (lam_np1 - lam_n) / lam_np1 ** 2 * np.outer(RankVector, RankVector)
		+ 2.0 * lam_n * np.diag(u[:2]) @ (GtN_cf - c2 * E2 @ GtD_cf @ E2) @ np.diag(u[:2]))
	print('C3 cross-parity assemblies = Kp_odd = E Ke E; raw Ko is separate:')
	print('   R-205 vs collapsed assembly err = %.3e' % np.max(np.abs(KpOddR205 - Kp_odd)))
	print('   Ko_ref (raw-K odd sector, different object) =', np.round(Ko_ref, 6))
	print('   Kp_odd_R205 =', np.round(KpOddR205, 6))
	print('   Kp_odd =', np.round(Kp_odd, 6))
	print('   Ko_closed (reduced kernels + rank-one term) =', np.round(KoClosed, 6))
	print('   Ko_closed vs raw spectral Ko_ref err = %.3e' % np.max(np.abs(KoClosed - Ko_ref)))
	print('   eig(Ko_ref) =', np.round(np.linalg.eigvalsh(Ko_ref), 6))
	print('   Kp_odd vs Po Kp_full Po^T err = %.3e'
		% np.max(np.abs(Kp_odd - (Po @ Kp_full @ Po.T))))
	print('   eig(Kp_odd) =', np.round(np.linalg.eigvalsh(Kp_odd), 6))
	# FD sector check: Ko is the odd sector of K = diag(1/s) J
	s = np.array([rc.pat[i + 1] - rc.pat[i] for i in range(4)])
	Jfd = jac_fd(rc, zs)
	Kfd = np.diag(1.0 / s) @ Jfd
	Ko_fd = Po @ Kfd @ Po.T
	Ke_fd = Pe @ Kfd @ Pe.T
	print('   FD odd sector Ko_fd =', np.round(Ko_fd, 6))
	print('   Ko_closed vs raw Ko_fd err = %.3e' % np.max(np.abs(KoClosed - Ko_fd)))
	print('   FD even sector Ke_fd =', np.round(Ke_fd, 6))
	# convention (STRICT algebra, R-207): Bo^T Kp Bo = diag(1,-1) Be^T K Be diag(1,-1);
	# sector_data Ko = Bo^T K Bo is the odd sector of the RAW K (not Kp).
	print('   Kp_odd vs diag(1,-1) Ke_ref diag(1,-1) err = %.3e'
		% np.max(np.abs(Kp_odd - (np.diag([1.0, -1.0]) @ Ke_ref @ np.diag([1.0, -1.0])))))
	print('   Kp_odd vs diag(1,-1) Ke_fd diag(1,-1) err = %.3e'
		% np.max(np.abs(Kp_odd - (np.diag([1.0, -1.0]) @ Ke_fd @ np.diag([1.0, -1.0])))))


if __name__ == '__main__':
	main()
