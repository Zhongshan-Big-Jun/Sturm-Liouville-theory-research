"""Function/class excerpts from ec45bf99 scripts/_gapn2_second_variation_probe.py.
Imports adapted for the isolated audit. Not the whole repository module.
The checked numerical physics dependency is the corresponding source excerpt.
"""
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from physical_excerpt import roots_of, eigfun
from _sl_prufer import lifted_phase
N_MODES = 60


def finite_vector(Value, Name):
	if np.iscomplexobj(Value):
		raise ValueError(Name + ' must be real')
	try:
		Result = np.asarray(Value, dtype=float)
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError(Name + ' must be a finite real vector') from Error
	if Result.ndim != 1 or Result.size == 0 or not np.all(np.isfinite(Result)):
		raise ValueError(Name + ' must be a nonempty finite real vector')
	return Result


def positive_integer(Value, Name, Minimum=1):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, (int, np.integer)) or Value < Minimum:
		raise ValueError(Name + ' must be an integer >= ' + str(Minimum))
	return int(Value)


def validate_blocks(Blocks):
	if np.iscomplexobj(Blocks):
		raise ValueError('blocks must be real')
	try:
		Values = np.asarray(Blocks, dtype=float)
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError('blocks must have shape (m, 2)') from Error
	if Values.ndim != 2 or Values.shape[1] != 2 or not len(Values):
		raise ValueError('blocks must have shape (m, 2)')
	if not np.all(np.isfinite(Values)) or np.any(Values <= 0):
		raise ValueError('block lengths and densities must be finite and positive')
	if not math.isfinite(float(np.sum(Values[:, 0]))):
		raise ValueError('total length is not finite')
	Edges = np.r_[0.0, np.cumsum(Values[:, 0])]
	if np.any(np.diff(Edges) <= 0):
		raise ValueError('block endpoints cannot be resolved in double precision')
	return tuple(map(tuple, Values.tolist()))


def checked_roots(Blocks, Count, Refine=60):
	Count = positive_integer(Count, 'mode count')
	Refine = positive_integer(Refine, 'root refinement')
	Roots = roots_of(validate_blocks(Blocks), Count, refine=Refine)
	if len(Roots) != Count or not np.all(np.isfinite(Roots)) or np.any(Roots <= 0) or np.any(np.diff(Roots) <= 0):
		raise ArithmeticError('spectral root search failed to return ordered positive roots')
	if np.any(np.abs(lifted_phase(Blocks, Roots) - np.arange(1, Count + 1) * np.pi) > 2e-8):
		raise ArithmeticError('root list does not match its claimed spectral indices')
	return Roots


def quadrature_rule(Blocks, Order=64, Breaks=()):
	"""Gauss-Legendre on each TRUE density/direction interval, never clipped masks."""
	Blocks = validate_blocks(Blocks)
	Order = positive_integer(Order, 'quadrature order', 8)
	Edges = np.r_[0.0, np.cumsum([L for L, _ in Blocks])]
	Extra = np.asarray(Breaks)
	if Extra.size:
		Extra = finite_vector(Extra, 'direction breakpoints')
		if np.any(Extra <= 0) or np.any(Extra >= Edges[-1]):
			raise ValueError('direction breakpoints must be strictly internal')
	elif Extra.ndim != 1:
		raise ValueError('direction breakpoints must be a vector')
	Knots = np.unique(np.r_[Edges, Extra])
	Nodes, Weights = leggauss(Order)
	Points, Factors = [], []
	for Left, Right in zip(Knots[:-1], Knots[1:]):
		Points.extend((Left + Right) / 2 + (Right - Left) * Nodes / 2)
		Factors.extend((Right - Left) * Weights / 2)
	return np.asarray(Points), np.asarray(Factors), Knots


class SpectralProbe:
	"""Finite double-precision spectral sum with endpoint-aligned quadrature."""
	def __init__(self, Blocks, Modes=N_MODES + 1, Order=64):
		self.blocks = validate_blocks(Blocks)
		self.order = positive_integer(Order, 'quadrature order', 8)
		self.roots = checked_roots(self.blocks, Modes)
		self.lam = self.roots ** 2
		if not np.all(np.isfinite(self.lam)):
			raise ArithmeticError('nonfinite eigenvalues')
		self.edges = np.r_[0.0, np.cumsum([L for L, _ in self.blocks])]
		self.cache = {}

	def quadrature(self, Breaks=()):
		Key = tuple(Breaks)
		if Key not in self.cache:
			Points, Weights, Knots = quadrature_rule(self.blocks, self.order, Key)
			Values = np.array([eigfun(self.blocks, Root, Points) for Root in self.roots])
			if not np.all(np.isfinite(Values)):
				raise ArithmeticError('nonfinite normalized eigenfunctions')
			self.cache[Key] = (Points, Weights, Values, Knots)
		return self.cache[Key]

	def pairings(self, drf, Breaks=()):
		Points, Weights, Values, _ = self.quadrature(Breaks)
		Direction = finite_vector(drf(Points), 'direction samples')
		if Direction.shape != Points.shape:
			raise ValueError('direction samples must match quadrature points')
		Index = np.clip(np.searchsorted(self.edges, Points, side='right') - 1, 0, len(self.blocks) - 1)
		Density = np.asarray([C for _, C in self.blocks])[Index]
		Unweighted = (Values * (Weights * Direction)) @ Values.T
		Weighted = (Values * (Weights * Direction * Density)) @ Values.T
		if not np.all(np.isfinite(Unweighted)) or not np.all(np.isfinite(Weighted)):
			raise ArithmeticError('nonfinite pairings')
		return self.lam, Unweighted, Weighted, np.diag(Unweighted).copy()


def q_formula(lam, Cu, Cw, n, dr_sq):
	"""Q with all retained modes; Cw retained for historical call compatibility."""
	Eigenvalues = finite_vector(lam, 'eigenvalues')
	n = positive_integer(n, 'n')
	if n >= len(Eigenvalues) or np.any(Eigenvalues <= 0) or np.any(np.diff(Eigenvalues) <= 0):
		raise ValueError('ordered positive eigenvalues must include n and n+1')
	Diagonal = finite_vector(dr_sq, 'diagonal pairings')
	if np.iscomplexobj(Cu) or np.iscomplexobj(Cw):
		raise ValueError('pairings must be real')
	Unweighted, Weighted = np.asarray(Cu, dtype=float), np.asarray(Cw, dtype=float)
	Shape = (len(Eigenvalues), len(Eigenvalues))
	if Unweighted.shape != Shape or Weighted.shape != Shape or Diagonal.shape != Eigenvalues.shape:
		raise ValueError('pairing dimensions differ from eigenvalues')
	if not np.all(np.isfinite(Unweighted)) or not np.all(np.isfinite(Weighted)):
		raise ValueError('pairings must be finite')
	Terms = []
	for k, Sign in ((n, 1.0), (n - 1, -1.0)):
		Other = np.arange(len(Eigenvalues)) != k
		Terms.append(Sign * (Eigenvalues[k] * Diagonal[k] ** 2 - Eigenvalues[k] ** 2
			* np.sum(Unweighted[k, Other] ** 2 / (Eigenvalues[Other] - Eigenvalues[k]))))
	Result = float(math.fsum(Terms))
	if not math.isfinite(Result):
		raise ArithmeticError('nonfinite Q')
	return Result


def block_direction(Coeff, Edges):
	Coeff = finite_vector(Coeff, 'block coefficients')
	Edges = finite_vector(Edges, 'edges')
	if len(Edges) != len(Coeff) + 1 or np.any(np.diff(Edges) <= 0):
		raise ValueError('edges must be strictly ordered and match coefficients')
	def Direction(Points):
		Index = np.clip(np.searchsorted(Edges, Points, side='right') - 1, 0, len(Coeff) - 1)
		return Coeff[Index]
	return Direction
