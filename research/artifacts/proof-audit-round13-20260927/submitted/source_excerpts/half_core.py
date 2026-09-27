"""Current half-spectrum/Green function excerpts (not a whole-file copy).
Source: scripts/_gapn2_half_problem_probe.py at commit
4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983. Imports added for isolation.
"""
from dataclasses import dataclass
import numpy as np
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
	with np.errstate(over='raise', invalid='raise'):
		try:
			Differences = AllModes - Mu
		except FloatingPointError as Error:
			raise ArithmeticError('spectral target differences exceed floating-point range') from Error
	if not np.all(np.isfinite(Differences)):
		raise ArithmeticError('spectral target differences are not finite')
	Near = np.abs(Differences) <= Tolerance
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
	Denominators = Differences[:Count][Keep]
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
