# -*- coding: utf-8 -*-
"""Finite numerical probes of D_n = lambda_{n+1} - lambda_n.

For the LINEAR density path rho + e*h, with integral rho*u_k**2 = 1,
Q(h) = D_n''(0)/2 = lambda_{n+1}*a_{n+1}**2 - lambda_n*a_n**2
  + lambda_n**2 * sum_{l != n} <h,u_n*u_l>**2/(lambda_l-lambda_n)
  - lambda_{n+1}**2 * sum_{l != n+1} <h,u_{n+1}*u_l>**2/(lambda_l-lambda_{n+1}).
Here a_k = integral h*u_k**2 and all pairings are unweighted.
This implementation truncates the sums. It supplies numerical evidence only.

P1 compares the finite sum with high-precision, finite-step central differences.
P2 samples block directions with b.A=0, A_i=integral over the TRUE block of f,
f=lambda_n*u_n**2-lambda_{n+1}*u_{n+1}**2. Euclidean projection is default;
optional width-weighted projection uses diag(widths). Direct tanh-sinh
integration of f*h checks tangency separately from analytic block integrals.
P2b already used integrals in the historical code. It shares the robust
projection/integration here; it was not the block-average projection defect.
P3 is a finite, FIXED-width bump exploration. For moving edges a_i+e*d_i,
rho'=-sum s_i*d_i*delta_i and rho''=sum s_i*d_i**2*delta'_i. Thus the
interface-path half second derivative also contains
  -(1/2)*sum s_i*d_i**2*f'(a_i).
It is different from the linear-density Hessian. A finite bump comparison,
sign difference or insufficient resolution proves neither divergence nor
failure of a limiting identity. No bump-width limit is evaluated here.
Unresolved supports or quadrature nodes are rejected before producing P3 values.

The R-206 (2026-08-13) P1 PASS/P2 definiteness/P3 NEGATIVE labels are historical,
not current validation. P1 did not require tangency for its formula, but its
old tangent label was wrong; P2 block directions must be recomputed. Sampled
signs never certify definiteness, the density-box tangent cone, or optimality.
Neither decimal input edges nor a numerical stationary solve are certificates.
R=1 remains supported as the degenerate constant-density case (all jumps zero).

Compatible CLI: python -B _gapn2_second_variation_probe.py [n] [R] [mode]
Optional --help flags expose finite resolution, truncation and FD parameters.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
import mpmath as mp
from numpy.polynomial.legendre import leggauss

# Installed replacement uses sibling dependencies; an external candidate can
# run with explicit repository cwd, without copying or editing dependencies.
SCRIPT_DIR = Path(__file__).resolve().parent
if not (SCRIPT_DIR / '_gapn2_symmetry_recon.py').is_file():
	SCRIPT_DIR = Path.cwd() / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _sl_prufer import indexed_roots, lifted_phase, mp_lifted_phase
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data

N_MODES = 60  # Historical loop retained 61 eigenfunctions, indices 0..60.


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


def positive_scalar(Value, Name):
	try:
		Result = float(Value)
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError(Name + ' must be finite and positive') from Error
	if not math.isfinite(Result) or Result <= 0:
		raise ValueError(Name + ' must be finite and positive')
	return Result


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


def project_tangent(b, A, widths=None, metric='euclidean'):
	"""Project coefficients onto b.A=0; A=0 returns a separate unchanged copy.

	The optional metric is diag(widths). Scaling in extended precision avoids
	squaring an unscaled tiny/large normal. No tolerance turns a nonzero A into 0.
	"""
	Coeff = finite_vector(b, 'b')
	Normal = finite_vector(A, 'A')
	if Coeff.shape != Normal.shape:
		raise ValueError('b and A dimensions differ')
	if metric not in ('euclidean', 'width-weighted'):
		raise ValueError('unknown coefficient metric')
	Width = None
	if widths is not None:
		Width = finite_vector(widths, 'widths')
		if Width.shape != Coeff.shape or np.any(Width <= 0):
			raise ValueError('widths must match b and be positive')
	if metric == 'width-weighted' and Width is None:
		raise ValueError('width-weighted projection requires widths')
	Scale = np.max(np.abs(Normal))
	if Scale == 0:
		return Coeff.copy()
	Normal = Normal.astype(np.longdouble) / np.longdouble(Scale)
	Direction = Normal.copy()
	if metric == 'width-weighted':
		Direction /= Width.astype(np.longdouble)
	Direction /= np.max(np.abs(Direction))
	Denominator = np.dot(Normal, Direction)
	if not np.isfinite(Denominator) or Denominator <= 0:
		raise ValueError('projection metric is not numerically resolvable')
	Projected = Coeff.astype(np.longdouble) - Direction * (np.dot(Coeff, Normal) / Denominator)
	with np.errstate(over='ignore', invalid='ignore'):
		Projected = np.asarray(Projected, dtype=float)
	if not np.all(np.isfinite(Projected)):
		raise ValueError('projected coefficients exceed finite floating-point range')
	return Projected


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


def checked_bump_breaks(Blocks, Centers, HalfWidth, Order):
	"""Reject unresolved fixed-width bumps; this is no quadrature certificate.

	Keep at least 2**20 coordinate spacings per half-width, so endpoint
	rounding cannot silently remove a finite fraction of the requested mass.
	Also check the actual interval quadrature nodes, including high orders.
	"""
	Centers = finite_vector(Centers, 'bump centers')
	HalfWidth = positive_scalar(HalfWidth, 'bump width')
	Blocks = validate_blocks(Blocks)
	Total = float(np.sum([L for L, _ in Blocks]))
	Left, Right = Centers - HalfWidth, Centers + HalfWidth
	if np.any(Left <= 0) or np.any(Right >= Total):
		raise ValueError('bumps must remain inside the domain')
	Spacing = np.spacing(np.abs(Centers))
	if np.any(HalfWidth < (2 ** 20) * Spacing):
		raise ValueError('bump width cannot be resolved reliably in double-precision coordinates')
	if np.any(Left >= Centers) or np.any(Right <= Centers):
		raise ValueError('bump support endpoints collapse in double precision')
	RadiusErrors = np.r_[np.abs((Centers - Left) / HalfWidth - 1),
		np.abs((Right - Centers) / HalfWidth - 1)]
	if np.any(RadiusErrors > 1e-6):
		raise ValueError('bump support rounding changes the requested width')
	Breaks = tuple(np.r_[Left, Right])
	Points, _, Knots = quadrature_rule(Blocks, Order, Breaks)
	Rows = Points.reshape(len(Knots) - 1, Order)
	if (np.any(np.diff(Rows, axis=1) <= 0)
		or np.any(Rows[:, 0] <= Knots[:-1]) or np.any(Rows[:, -1] >= Knots[1:])):
		raise ValueError('bump quadrature nodes cannot be resolved in double-precision coordinates')
	return Breaks


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


def mp_state(Blocks, Root):
	"""Transfer solution and exact trigonometric square integrals at mp precision."""
	Value, Derivative = mp.mpf(0), mp.mpf(1)
	Segments, Mass = [], mp.mpf(0)
	for Length, Density in Blocks:
		Omega = Root * mp.sqrt(Density)
		CosCoeff, SinCoeff = Value, Derivative / Omega
		Phase = Omega * Length
		Cos, Sin = mp.cos(Phase), mp.sin(Phase)
		Square = (CosCoeff ** 2 * (Length / 2 + mp.sin(2 * Phase) / (4 * Omega))
			+ SinCoeff ** 2 * (Length / 2 - mp.sin(2 * Phase) / (4 * Omega))
			+ CosCoeff * SinCoeff * Sin ** 2 / Omega)
		Segments.append((Omega, CosCoeff, SinCoeff, Square))
		Mass += Density * Square
		Value, Derivative = CosCoeff * Cos + SinCoeff * Sin, Omega * (-CosCoeff * Sin + SinCoeff * Cos)
	return Value, Segments, Mass


def refine_mp_root(Blocks, Guess, Digits, Index):
	"""Safeguarded high-precision refinement of the SAME one-based phase index.

	No unconstrained secant/Newton jump to a neighbouring clustered mode.
	This is high-precision numerical evidence, not interval certification.
	"""
	Index = positive_integer(Index, 'spectral index')
	Guess = mp.mpf(float(Guess))
	Target = Index * mp.pi
	Lo, Hi = Guess * mp.mpf('0.999'), Guess * mp.mpf('1.001')
	if mp_lifted_phase(Blocks, Lo) >= Target or mp_lifted_phase(Blocks, Hi) <= Target:
		Lo = mp.mpf(0)
		Hi = mp.mpf('1.125') * Target / (mp.fsum(L for L, _ in Blocks) * mp.sqrt(min(C for _, C in Blocks)))
	if not (mp_lifted_phase(Blocks, Lo) < Target < mp_lifted_phase(Blocks, Hi)):
		raise ArithmeticError('high-precision phase index was not bracketed')
	for _ in range(4 * Digits + 32):
		Mid = (Lo + Hi) / 2
		if Mid == Lo or Mid == Hi:
			break
		if mp_lifted_phase(Blocks, Mid) < Target:
			Lo = Mid
		else:
			Hi = Mid
	Root = (Lo + Hi) / 2
	End, Segments, Mass = mp_state(Blocks, Root)
	Tolerance = mp.mpf(10) ** (-(Digits - 15))
	if (Root <= 0 or abs(mp_lifted_phase(Blocks, Root) - Target) > Tolerance
		or abs(End) > Tolerance or Mass <= 0):
		raise ArithmeticError('high-precision indexed root refinement failed')
	return Root, Segments, Mass


class HighPrecisionTangent:
	"""Analytic block integrals vs separate direct tanh-sinh f*h quadrature."""
	def __init__(self, Blocks, n, Digits=60):
		self.blocks = validate_blocks(Blocks)
		self.n = positive_integer(n, 'n')
		self.digits = positive_integer(Digits, 'digits', 30)
		Guesses = checked_roots(self.blocks, n + 1)
		with mp.workdps(self.digits):
			self.mp_blocks = tuple((mp.mpf(L), mp.mpf(C)) for L, C in self.blocks)
			self.modes = [refine_mp_root(self.mp_blocks, Guesses[k], self.digits, k + 1) for k in (n - 1, n)]
			self.integrals = []
			for i in range(len(self.blocks)):
				self.integrals.append(self.modes[0][0] ** 2 * self.modes[0][1][i][3] / self.modes[0][2]
					- self.modes[1][0] ** 2 * self.modes[1][1][i][3] / self.modes[1][2])
		self.A = np.array([float(Value) for Value in self.integrals])

	def f_local(self, i, Offset):
		Values = []
		for Root, Segments, Mass in self.modes:
			Omega, CosCoeff, SinCoeff, _ = Segments[i]
			Value = CosCoeff * mp.cos(Omega * Offset) + SinCoeff * mp.sin(Omega * Offset)
			Values.append(Root ** 2 * Value ** 2 / Mass)
		return Values[0] - Values[1]

	def direct_residual(self, Coeff, Kind='block'):
		Coeff = finite_vector(Coeff, 'coefficients')
		if Kind not in ('block', 'trig') or (Kind == 'block' and len(Coeff) != len(self.blocks)):
			raise ValueError('invalid direct residual kind or dimensions')
		with mp.workdps(self.digits):
			Coefficients = [mp.mpf(float(C)) for C in Coeff]
			Parts, Start = [], mp.mpf(0)
			for i, (Length, _) in enumerate(self.mp_blocks):
				def Integrand(t):
					H = Coefficients[i] if Kind == 'block' else mp.fsum(C * mp.sin((j + 1) * mp.pi * (Start + t)) for j, C in enumerate(Coefficients))
					return self.f_local(i, t) * H
				Parts.append(mp.quad(Integrand, [0, Length], method='tanh-sinh'))
				Start += Length
			return mp.fsum(Parts)

	def integrals_text(self):
		return [mp.nstr(Value, self.digits - 5) for Value in self.integrals]


def block_direction(Coeff, Edges):
	Coeff = finite_vector(Coeff, 'block coefficients')
	Edges = finite_vector(Edges, 'edges')
	if len(Edges) != len(Coeff) + 1 or np.any(np.diff(Edges) <= 0):
		raise ValueError('edges must be strictly ordered and match coefficients')
	def Direction(Points):
		Index = np.clip(np.searchsorted(Edges, Points, side='right') - 1, 0, len(Coeff) - 1)
		return Coeff[Index]
	return Direction


def trig_direction(Coeff):
	Coeff = finite_vector(Coeff, 'trig coefficients')
	return lambda Points: np.sum(Coeff[:, None] * np.sin(np.arange(1, len(Coeff) + 1)[:, None] * np.pi * Points), axis=0)


def fd_second(blocks, dr_blocks, k, h=1e-4, refine=60, dps=60):
	"""Central difference on an actual linear path, with no density clamping.

	Default uses mp root refinement; dps=0 exposes double cancellation. k is
	zero-based for historical compatibility. Finite h error is NOT certified.
	"""
	Base = validate_blocks(blocks)
	Direction = finite_vector(dr_blocks, 'FD direction')
	k = positive_integer(k, 'zero-based k', 0)
	h = positive_scalar(h, 'FD step')
	refine = positive_integer(refine, 'root refinement')
	if len(Direction) != len(Base):
		raise ValueError('FD direction and blocks dimensions differ')
	Densities = np.array([C for _, C in Base])
	with np.errstate(over='ignore', invalid='ignore'):
		Delta = h * np.abs(Direction)
	if not np.all(np.isfinite(Delta)) or np.any(Densities - Delta <= 0):
		raise ValueError('FD endpoints must have positive density; no clamping')
	if dps != 0:
		positive_integer(dps, 'digits', 30)
	with mp.workdps(dps if dps else 30):
		def Eigenvalue(Sign):
			Perturbed = [(L, C + Sign * h * D) for (L, C), D in zip(Base, Direction)]
			Guess = checked_roots(Perturbed, k + 1, refine)[k]
			if not dps:
				return float(Guess ** 2)
			Precise = [(mp.mpf(L), mp.mpf(C) + Sign * mp.mpf(h) * mp.mpf(float(D))) for (L, C), D in zip(Base, Direction)]
			return refine_mp_root(Precise, Guess, dps, k + 1)[0] ** 2
		Plus, Minus, BaseValue = Eigenvalue(1), Eigenvalue(-1), Eigenvalue(0)
		Step = mp.mpf(h) if dps else h
		return (Plus - 2 * BaseValue + Minus) / Step ** 2, BaseValue, Plus, Minus


def fd_gap(Blocks, Direction, n, Step, Digits=60):
	with mp.workdps(Digits if Digits else 30):
		Upper = fd_second(Blocks, Direction, n, Step, dps=Digits)[0]
		Lower = fd_second(Blocks, Direction, n - 1, Step, dps=Digits)[0]
		return float((Upper - Lower) / 2)


def build_case(n, R, mode, TablePath=None):
	n = positive_integer(n, 'n')
	R = positive_scalar(R, 'R')
	if R < 1 or mode not in ('sup', 'inf'):
		raise ValueError('density-box case requires R >= 1 and mode sup or inf')
	TablePath = Path(TablePath) if TablePath else SCRIPT_DIR / 'op03_gap_table.json'
	with TablePath.open(encoding='utf-8') as Handle:
		Table = json.load(Handle)
	Key = 'n%d_%s' % (n, mode.upper())
	if Key not in Table:
		raise ValueError('input table has no ' + Key)
	Edges = finite_vector(Table[Key]['edges'], 'table edges')
	if len(Edges) != 2 * n or np.any(np.diff(np.r_[0, Edges, 1]) <= 0):
		raise ValueError('table edges must define 2n+1 positive blocks in (0,1)')
	SeedRecon = Recon(n, R=4.0, mode=mode)
	Seed = SeedRecon.widths_to_z(np.diff(np.r_[0, Edges, 1]))
	Reconstruction = Recon(n, R, mode)
	Stationary = symmetric_root(Reconstruction, Seed)
	if Stationary is None or not np.all(np.isfinite(Stationary)):
		raise ArithmeticError('symmetric stationary solve did not converge')
	Blocks = validate_blocks(Reconstruction.blocks_from_z(Stationary))
	return Reconstruction, Stationary, Blocks, TablePath


def run_probe(n=2, R=4.0, mode='sup', Modes=N_MODES + 1, Order=64, Digits=60,
	Metric='euclidean', Steps=(1e-2, 1e-3, 1e-4), BumpWidth=5e-4, TablePath=None, IncludeP3=True):
	positive_integer(n, 'n')
	positive_integer(Modes, 'modes', n + 1)
	positive_integer(Order, 'quadrature order', 8)
	positive_integer(Digits, 'digits', 30)
	Steps = finite_vector(Steps, 'FD steps')
	if np.any(Steps <= 0):
		raise ValueError('FD steps must be positive')
	BumpWidth = positive_scalar(BumpWidth, 'bump width')
	if Metric not in ('euclidean', 'width-weighted'):
		raise ValueError('invalid coefficient metric')
	Rc, Stationary, Blocks, TablePath = build_case(n, R, mode, TablePath)
	Widths = np.array([L for L, _ in Blocks])
	if IncludeP3:
		checked_bump_breaks(Blocks, np.cumsum(Widths)[:-1], BumpWidth, Order)
	Probe = SpectralProbe(Blocks, Modes, Order)
	Tangent = HighPrecisionTangent(Blocks, n, Digits)
	A = Tangent.A
	Ln, Lp = float(Tangent.modes[0][0] ** 2), float(Tangent.modes[1][0] ** 2)
	Result = {'scope': 'software-author finite numerical evidence; no independent audit verdict',
		'n': n, 'R': R, 'mode': mode, 'retained_modes': Modes, 'gauss_order_per_interval': Order,
		'digits': Digits, 'metric': Metric, 'seed': 20260813, 'blocks': Blocks, 'edges': Probe.edges.tolist(),
		'lambda_n': Ln, 'lambda_np1': Lp, 'stationary_residual_max': float(np.max(np.abs(Rc.residual(Stationary)))),
		'root_index_records': indexed_roots(Blocks, Modes)[1],
		'block_integrals_mp': Tangent.integrals_text(), 'P1': [], 'P2': [], 'P2b': [], 'P3': [],
		'limitations': ['finite spectral cutoff; no rigorous tail bound', 'lifted-phase indices and safeguarded mp refinement are numerical, not interval-certified enumeration', 'mp and Gauss quadrature are not interval certificates',
			'input decimals and numerical stationary solve are not exact stationary certificates',
			'random signs do not establish definiteness, density-box admissibility or optimality',
			'P3 is fixed-width only; neither convergence nor divergence inferred']}
	Paths = [Path(__file__).resolve(), TablePath.resolve()] + [Path(sys.modules[Name].__file__).resolve() for Name in
		('_gapn2_symmetry_recon', '_sl_prufer', 'reflection_seeds', '_gapn2_jacobian_probe', '_gapn2_jacobian_analytic')]
	Result['source_sha256'] = {str(P): hashlib.sha256(P.read_bytes()).hexdigest() for P in Paths}
	print('=== n=%d R=%g mode=%s; FINITE EVIDENCE, modes=%d order=%d ===' % (n, R, mode, Modes, Order), flush=True)
	print('  metric=%s; A from %d-digit analytic block integrals; independent direct f*h quadrature' % (Metric, Digits), flush=True)
	Rng = np.random.default_rng(20260813)
	for Group, Count, Scale in (('P1', 3, 1e-2), ('P2', 8, None)):
		print('  %s: %s' % (Group, 'finite-sum vs finite-step FD errors' if Group == 'P1' else '8 sampled tangent directions (no definiteness claim)'), flush=True)
		for t in range(Count):
			Coeff = project_tangent(Rng.standard_normal(len(Blocks)), A, Widths, Metric)
			if Scale is not None and np.max(np.abs(Coeff)) != 0:
				Coeff *= Scale / np.max(np.abs(Coeff))
			Lam, Cu, Cw, Diagonal = Probe.pairings(block_direction(Coeff, Probe.edges))
			Q = q_formula(Lam, Cu, Cw, n, Diagonal)
			Residual = Tangent.direct_residual(Coeff)
			Row = {'t': t, 'coefficients': Coeff.tolist(), 'Q': Q, 'dot_A': float(Coeff @ A),
				'direct_fh': mp.nstr(Residual, 30)}
			print('    t=%d: Q=%.12e  direct integral f*h=%s' % (t, Q, Row['direct_fh']), flush=True)
			if Group == 'P1':
				Row['FD'] = []
				for Step in Steps:
					Qfd = fd_gap(Blocks, Coeff, n, Step, Digits)
					Error = abs(Q - Qfd)
					Rel = Error / abs(Qfd) if Qfd != 0 else None
					Row['FD'].append({'h': float(Step), 'Q_fd': Qfd, 'absolute_error': Error, 'relative_error': Rel})
					print('      h=%.1e Q_FD=%.12e abs_error=%.3e rel_error=%s' % (Step, Qfd, Error, Rel), flush=True)
				Row['double_fd_at_last_step'] = fd_gap(Blocks, Coeff, n, Steps[-1], 0)
			Result[Group].append(Row)
		if Group == 'P2':
			print('    sampled signs: %s (finite samples only)' % np.sign([Row['Q'] for Row in Result[Group]]), flush=True)
	print('  P2b: integral-based trig projection, shared robustness changes only:', flush=True)
	Points, Weights, Values, _ = Probe.quadrature()
	F = Probe.lam[n - 1] * Values[n - 1] ** 2 - Probe.lam[n] * Values[n] ** 2
	G = np.array([np.sum(Weights * F * np.sin((j + 1) * np.pi * Points)) for j in range(8)])
	for t in range(6):
		Coeff = project_tangent(Rng.standard_normal(8), G)
		Lam, Cu, Cw, Diagonal = Probe.pairings(trig_direction(Coeff))
		Q = q_formula(Lam, Cu, Cw, n, Diagonal)
		Residual = Tangent.direct_residual(Coeff, 'trig')
		Row = {'t': t, 'coefficients': Coeff.tolist(), 'Q': Q, 'direct_fh': mp.nstr(Residual, 30)}
		Result['P2b'].append(Row)
		print('    t=%d: Q=%.12e direct integral f*h=%s' % (t, Q, Row['direct_fh']), flush=True)
	if IncludeP3:
		print('  P3: fixed bump half-width %.3e; no limiting or sign theorem:' % BumpWidth, flush=True)
		Data = eigen_data(Rc, Stationary)
		Edges = Data['edges']
		if BumpWidth >= min(Edges[0], Probe.edges[-1] - Edges[-1]):
			raise ValueError('bumps must remain inside the domain')
		Jumps = np.diff([C for _, C in Blocks])
		Hessian = (-Data['lam_np1'] * np.diag(Jumps)) @ jac_fd(Rc, Stationary)
		Fprime = 2 * Data['lam_n'] * Data['u_n'] * Data['up_n'] - 2 * Data['lam_np1'] * Data['u_np1'] * Data['up_np1']
		Breaks = checked_bump_breaks(Blocks, Edges, BumpWidth, Order)
		for t in range(3):
			Displacement = Rng.standard_normal(2 * n)
			def Bump(Points):
				return np.sum((-Jumps * Displacement / (2 * BumpWidth))[:, None]
					* (np.abs(Points[None, :] - Edges[:, None]) < BumpWidth), axis=0)
			Lam, Cu, Cw, Diagonal = Probe.pairings(Bump, Breaks)
			Qbump = q_formula(Lam, Cu, Cw, n, Diagonal)
			Qedge = float(Displacement @ Hessian @ Displacement / 2)
			Acceleration = float(-np.sum(Jumps * Displacement ** 2 * Fprime) / 2)
			Row = {'t': t, 'half_width': BumpWidth, 'displacement': Displacement.tolist(),
				'Q_interface_hessian_fd': Qedge, 'Q_linear_fixed_bump': Qbump,
				'half_interface_acceleration': Acceleration, 'finite_comparison_difference': Qedge - (Qbump + Acceleration)}
			Result['P3'].append(Row)
			print('    t=%d Q_edge=%.8e Q_linear_bump=%.8e half_accel=%.8e finite_diff=%.3e'
				% (t, Qedge, Qbump, Acceleration, Row['finite_comparison_difference']), flush=True)
	return Result


def main(argv=None):
	Parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	Parser.add_argument('n', nargs='?', type=int, default=2)
	Parser.add_argument('R', nargs='?', type=float, default=4.0)
	Parser.add_argument('mode', nargs='?', type=str.lower, choices=('sup', 'inf'), default='sup')
	Parser.add_argument('--modes', type=int, default=N_MODES + 1, help='number of retained eigenfunctions (old default: 61)')
	Parser.add_argument('--quad-order', type=int, default=64, help='Gauss nodes per actual interval')
	Parser.add_argument('--dps', type=int, default=60)
	Parser.add_argument('--metric', choices=('euclidean', 'width-weighted'), default='euclidean')
	Parser.add_argument('--fd-steps', nargs='+', type=float, default=[1e-2, 1e-3, 1e-4])
	Parser.add_argument('--bump-width', type=float, default=5e-4, help='fixed half-width, not a limiting sequence')
	Parser.add_argument('--table', type=Path)
	Parser.add_argument('--skip-p3', action='store_true')
	Parser.add_argument('--output', type=Path, help='optional structured numerical evidence')
	Args = Parser.parse_args(argv)
	try:
		Result = run_probe(Args.n, Args.R, Args.mode, Args.modes, Args.quad_order, Args.dps,
			Args.metric, Args.fd_steps, Args.bump_width, Args.table, not Args.skip_p3)
	except (ValueError, ArithmeticError, KeyError, OSError) as Error:
		Parser.error(str(Error))
	if Args.output:
		Args.output.write_text(json.dumps(Result, indent=2, allow_nan=False) + '\n', encoding='utf-8')
	return 0


if __name__ == '__main__':
	sys.exit(main())
