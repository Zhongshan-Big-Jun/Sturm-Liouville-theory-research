"""Pure reflection-sector seeds for interior interfaces of the unit interval.

R(x) = 1 - x[::-1], so DR(v) = -v[::-1]. The preserve sector is
reversal-odd and the break sector is reversal-even. All certification here
is a finite-precision geometry check, not a stationary-point/spectral claim.
This module performs no file I/O and imports no research-project code.
"""

from dataclasses import asdict, dataclass
import numbers

import numpy as np


class ZeroProjectionError(ValueError):
	"""The selected projection cannot provide a nonzero direction."""

	def __init__(self, Message, Evidence=None):
		super().__init__(Message)
		self.Evidence = _json_ready(Evidence or {})


class SeedValidationError(ValueError):
	"""Invalid actual geometry, with JSON-compatible measured evidence."""

	def __init__(self, Message, Evidence=None):
		super().__init__(Message)
		self.Evidence = _json_ready(Evidence or {})


class UnresolvedPerturbationError(SeedValidationError):
	"""Actual interface motion is below the resolution guard."""


class SeedGenerationError(RuntimeError):
	"""Bounded seed generation failed; Evidence includes attempted steps."""

	def __init__(self, Message, Evidence):
		super().__init__(Message)
		self.Evidence = _json_ready(Evidence)


@dataclass(frozen=True)
class ReflectionSeed:
	"""Immutable coordinate tuples; Evidence is a caller-owned JSON record.

	UsedStep is the accepted coefficient before any callback round trip.
	ActualStep is the measured coefficient along the unit Direction afterwards.
	Edges is cumsum(Widths)[:-1]. Z is None unless both callbacks were supplied.
	"""

	Sector: str
	BaseEdges: tuple[float, ...]
	Direction: tuple[float, ...]
	RequestedStep: float
	UsedStep: float
	ActualStep: float
	Edges: tuple[float, ...]
	Widths: tuple[float, ...]
	Z: tuple[float, ...] | None
	Evidence: dict

	def to_dict(self):
		"""Return a detached JSON-compatible evidence record."""
		return _json_ready(asdict(self))


def _json_ready(Value):
	if isinstance(Value, dict):
		return {Key: _json_ready(Item) for Key, Item in Value.items()}
	if isinstance(Value, (list, tuple, np.ndarray)):
		return [_json_ready(Item) for Item in Value]
	if isinstance(Value, (float, np.floating)):
		return float(Value) if np.isfinite(Value) else str(Value)
	if isinstance(Value, np.integer):
		return int(Value)
	return Value


def _vector(Vector, Name):
	try:
		Array = np.asarray(Vector)
		if Array.ndim != 1 or Array.size == 0 or Array.dtype.kind not in 'iuf':
			raise ValueError('expected a nonempty one-dimensional real numeric vector')
		with np.errstate(over='ignore', invalid='ignore'):
			Array = np.array(Array, dtype=float, copy=True)
		if not np.all(np.isfinite(Array)):
			raise ValueError('expected finite float64 values')
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError(f'{Name}: {Error}') from Error
	return Array


def _sector(Sector):
	if not isinstance(Sector, str) or Sector not in ('preserve', 'break'):
		raise ValueError("Sector must be exactly 'preserve' or 'break'")


def _scalar(Value, Name, Lower, Upper, IncludeLower=False):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Real):
		raise ValueError(f'{Name} must be a finite real number')
	Value = float(Value)
	if not np.isfinite(Value) or Value > Upper or (Value < Lower if IncludeLower else Value <= Lower):
		raise ValueError(f'{Name} is outside the allowed range')
	return Value


def _integer(Value, Name, Minimum):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Integral) or Value < Minimum:
		raise ValueError(f'{Name} must be an integer >= {Minimum}')
	return int(Value)


def _width_floor(MinWidth):
	return _scalar(MinWidth, 'MinWidth', 1e-7, 0.5, IncludeLower=True)


def _max_abs(Vector):
	return float(np.max(np.abs(Vector)))


def _reflection_residual(Edges):
	return _max_abs(Edges + Edges[::-1] - 1.)


def _sector_residual(Vector, Sector):
	Other = 0.5 * Vector + 0.5 * Vector[::-1] if Sector == 'preserve' else 0.5 * Vector - 0.5 * Vector[::-1]
	return _max_abs(Other)


def reflection_direction(Vector, Sector, *, Normalize=False):
	"""Project v to (v-v[::-1])/2 or (v+v[::-1])/2, without mutation.

	Normalize=True gives unit Euclidean norm. A zero/unrepresentable
	projection raises ZeroProjectionError in both modes; it is never a seed.
	"""
	_sector(Sector)
	if not isinstance(Normalize, (bool, np.bool_)):
		raise ValueError('Normalize must be boolean')
	Vector = _vector(Vector, 'Vector')
	Sign = -1. if Sector == 'preserve' else 1.
	with np.errstate(over='ignore', under='ignore', invalid='ignore'):
		Projected = (Vector + Sign * Vector[::-1]) * 0.5
		Overflow = ~np.isfinite(Projected)
		if np.any(Overflow):
			Safe = 0.5 * Vector + Sign * (0.5 * Vector[::-1])
			Projected[Overflow] = Safe[Overflow]
	Scale = _max_abs(Projected)
	if Scale == 0.:
		raise ZeroProjectionError(f'{Sector} projection is zero or unrepresentable')
	if Normalize:
		Projected = Projected / Scale
		Projected = Projected / np.linalg.norm(Projected)
	return Projected


def interfaces_to_widths(Edges, *, MinWidth=1e-7):
	"""Check 0 < x_1 < ... < x_m < 1 and every width > MinWidth.

	The floor cannot be weakened below 1e-7. This function never clips,
	sorts or renormalizes; it returns diff([0, *Edges, 1]) unchanged.
	"""
	MinWidth = _width_floor(MinWidth)
	Edges = _vector(Edges, 'Edges')
	if np.any(Edges <= 0.) or np.any(Edges >= 1.):
		raise ValueError('Interfaces must lie strictly inside (0, 1)')
	Widths = np.diff(np.r_[0., Edges, 1.])
	if not np.all(Widths > MinWidth):
		raise ValueError('Interfaces must be ordered with every actual width > MinWidth')
	return Widths


def _prepare_base(BaseEdges, MinWidth, SymmetrizeBase=False, SymmetryTolerance=1e-12):
	if not isinstance(SymmetrizeBase, (bool, np.bool_)):
		raise ValueError('SymmetrizeBase must be boolean')
	SymmetryTolerance = _scalar(SymmetryTolerance, 'SymmetryTolerance', 0., 1e-8, IncludeLower=True)
	Original = _vector(BaseEdges, 'BaseEdges')
	interfaces_to_widths(Original, MinWidth=MinWidth)
	Residual = _reflection_residual(Original)
	if Residual > SymmetryTolerance:
		raise ValueError('BaseEdges is not reflection-symmetric within SymmetryTolerance')
	if Residual != 0. and not SymmetrizeBase:
		raise ValueError('BaseEdges requires explicit SymmetrizeBase=True within tolerance')
	Base = Original.copy()
	if Residual != 0.:
		Half = len(Base) // 2
		if Half:
			Left = 0.5 * Original[:Half] + 0.5 * (1. - Original[-Half:][::-1])
			Base[:Half] = Left
			Base[-Half:] = 1. - Left[::-1]
		if len(Base) % 2:
			Base[Half] = 0.5
	interfaces_to_widths(Base, MinWidth=MinWidth)
	if _reflection_residual(Base) != 0.:
		raise ValueError('Unable to represent a reflection-symmetric base')
	return Base, {
		'InputBaseEdges': Original,
		'BaseEdges': Base,
		'InputBaseReflectionResidual': Residual,
		'BaseReflectionResidual': _reflection_residual(Base),
		'BaseWasSymmetrized': bool(np.any(Base != Original)),
		'BaseCorrectionMax': _max_abs(Base - Original),
		'SymmetrizeBaseRequested': bool(SymmetrizeBase),
		'SymmetryTolerance': SymmetryTolerance,
	}


def check_sector_seed(
	BaseEdges, Widths, Sector, *, Direction=None, ExpectedStep=None,
	MinWidth=1e-7, SectorTolerance=1e-8, RoundTripTolerance=1e-8,
):
	"""Check the actual interfaces reconstructed from the supplied widths.

	BaseEdges must already be symmetric (explicit repair belongs to generation).
	Widths are never repaired. Both the supplied widths and endpoint-anchored
	physical widths must exceed MinWidth. Sum error is limited to 8*m*eps.
	A nonzero displacement must exceed 32*eps in max norm and its unwanted
	sector component must be <= SectorTolerance times its max norm.
	Supply Direction and ExpectedStep together to additionally reject changes
	of direction or step, including sector-preserving softmax clipping.
	"""
	_sector(Sector)
	MinWidth = _width_floor(MinWidth)
	SectorTolerance = _scalar(SectorTolerance, 'SectorTolerance', 0., 1e-6)
	RoundTripTolerance = _scalar(RoundTripTolerance, 'RoundTripTolerance', 0., 1e-6)
	Base, _ = _prepare_base(BaseEdges, MinWidth)
	if (Direction is None) != (ExpectedStep is None):
		raise ValueError('Direction and ExpectedStep must be supplied together')
	if Direction is not None:
		Direction = _vector(Direction, 'Direction')
		if len(Direction) != len(Base) or _max_abs(Direction) == 0.:
			raise ValueError('Direction must be nonzero and match BaseEdges')
		if _sector_residual(Direction, Sector) > SectorTolerance * _max_abs(Direction):
			raise ValueError('Direction itself is outside the requested sector')
		ExpectedStep = _scalar(ExpectedStep, 'ExpectedStep', 0., np.finfo(float).max)
	try:
		Widths = _vector(Widths, 'Widths')
	except ValueError as Error:
		raise SeedValidationError(str(Error)) from Error
	Check = {'Widths': Widths, 'Sector': Sector, 'MinWidth': MinWidth}
	if len(Widths) != len(Base) + 1:
		raise SeedValidationError('Wrong number of widths', Check)
	Check['MinimumWidth'] = float(np.min(Widths))
	if not np.all(Widths > MinWidth):
		raise SeedValidationError('Actual converted widths do not strictly exceed MinWidth', Check)
	with np.errstate(over='ignore', invalid='ignore'):
		Check['SumResidual'] = abs(float(np.sum(Widths)) - 1.)
	Check['SumTolerance'] = 8. * len(Widths) * np.finfo(float).eps
	if Check['SumResidual'] > Check['SumTolerance']:
		raise SeedValidationError('Actual widths do not sum to one within roundoff', Check)
	Edges = np.cumsum(Widths)[:-1]
	try:
		InterfaceWidths = interfaces_to_widths(Edges, MinWidth=MinWidth)
	except ValueError as Error:
		Check['CheckedEdges'] = Edges
		raise SeedValidationError(str(Error), Check) from Error
	Delta = Edges - Base
	ActualMax = _max_abs(Delta)
	Check.update({
		'CheckedEdges': Edges,
		'InterfaceWidths': InterfaceWidths,
		'MinimumInterfaceWidth': float(np.min(InterfaceWidths)),
		'Displacement': Delta,
		'ActualMaxDisplacement': ActualMax,
		'ActualLength': float(np.linalg.norm(Delta)),
		'ResolutionFloor': 32. * np.finfo(float).eps,
		'FinalReflectionResidual': _reflection_residual(Edges),
		'SectorResidual': _sector_residual(Delta, Sector),
		'SectorTolerance': SectorTolerance,
		'RoundTripTolerance': RoundTripTolerance,
	})
	if ActualMax <= Check['ResolutionFloor']:
		raise UnresolvedPerturbationError('No resolvable nonzero actual interface displacement', Check)
	Check['SectorRelativeResidual'] = Check['SectorResidual'] / ActualMax
	Errors = []
	if Check['SectorRelativeResidual'] > SectorTolerance:
		Errors.append('actual displacement is outside the requested sector')
	if Direction is not None:
		Scale = _max_abs(Direction)
		Scaled = Direction / Scale
		ActualStep = float(np.dot(Delta, Scaled) / np.dot(Scaled, Scaled) / Scale)
		with np.errstate(over='ignore', invalid='ignore'):
			Expected = ExpectedStep * Direction
			DirectionResidual = _max_abs(Delta - ActualStep * Direction)
			ExpectedResidual = _max_abs(Delta - Expected)
		Check.update({
			'ActualStep': ActualStep,
			'ExpectedStep': ExpectedStep,
			'DirectionResidual': DirectionResidual,
			'DirectionRelativeResidual': DirectionResidual / ActualMax,
			'ExpectedDisplacementResidual': ExpectedResidual,
			'ExpectedRelativeResidual': ExpectedResidual / ActualMax,
		})
		if not np.isfinite(ActualStep) or ActualStep <= 0. or not np.isfinite(ExpectedResidual):
			Errors.append('actual step is not a finite positive perturbation')
		elif max(Check['DirectionRelativeResidual'], Check['ExpectedRelativeResidual']) > RoundTripTolerance:
			Errors.append('round trip changed the requested direction or step')
	if Errors:
		raise SeedValidationError('; '.join(Errors), Check)
	return _json_ready(Check)


def generate_sector_seed(
	BaseEdges, Sector, Step, *, Vector=None, Rng=None,
	WidthsToZ=None, ZToWidths=None, SymmetrizeBase=False,
	SymmetryTolerance=1e-12, MinWidth=1e-7,
	MaxResamples=32, MaxHalvings=80,
	SectorTolerance=1e-8, RoundTripTolerance=1e-8,
):
	"""Generate a checked pure-sector seed with bounded projection/backtracking.

	Exactly one of Vector or Rng is required. Rng must implement
	standard_normal(size); at most MaxResamples draws are made. The selected
	direction is always unit norm. Step must be finite and positive; direction
	sign controls the opposite ray. Try Step, Step/2, ..., Step/2**MaxHalvings.
	Both conversion callbacks or neither must be supplied. They receive copies
	and must be deterministic, side-effect-free conversions. Their actual output
	is checked for feasibility, resolved motion, sector and requested displacement.
	No callback means return feasible Widths and Z=None; the caller can use
	check_sector_seed after its later conversion. Numerical generation failures
	carry evidence; invalid API inputs raise ValueError before generation.
	"""
	_sector(Sector)
	Step = _scalar(Step, 'Step', 0., np.finfo(float).max)
	MinWidth = _width_floor(MinWidth)
	MaxResamples = _integer(MaxResamples, 'MaxResamples', 1)
	MaxHalvings = _integer(MaxHalvings, 'MaxHalvings', 0)
	SectorTolerance = _scalar(SectorTolerance, 'SectorTolerance', 0., 1e-6)
	RoundTripTolerance = _scalar(RoundTripTolerance, 'RoundTripTolerance', 0., 1e-6)
	Base, Evidence = _prepare_base(BaseEdges, MinWidth, SymmetrizeBase, SymmetryTolerance)
	if (Vector is None) == (Rng is None):
		raise ValueError('Provide exactly one of Vector or Rng')
	if (WidthsToZ is None) != (ZToWidths is None):
		raise ValueError('Supply both WidthsToZ and ZToWidths or neither')
	UseCallbacks = WidthsToZ is not None
	if UseCallbacks and (not callable(WidthsToZ) or not callable(ZToWidths)):
		raise ValueError('Conversion callbacks must be callable')
	if Rng is not None and not callable(getattr(Rng, 'standard_normal', None)):
		raise ValueError('Rng must implement standard_normal(size)')
	Evidence.update({
		'Origin': 'pure_reflection_sector',
		'DirectionSource': 'provided_vector' if Vector is not None else 'projected_rng',
		'Sector': Sector,
		'RequestedStep': Step,
		'MinWidth': MinWidth,
		'MaxResamples': MaxResamples,
		'MaxHalvings': MaxHalvings,
		'UsedCallbacks': UseCallbacks,
		'SectorTolerance': SectorTolerance,
		'RoundTripTolerance': RoundTripTolerance,
		'Draws': [],
		'Attempts': [],
	})
	for DrawIndex in range(1 if Vector is not None else MaxResamples):
		Raw = _vector(Vector if Vector is not None else Rng.standard_normal(len(Base)), 'Vector')
		if len(Raw) != len(Base):
			raise ValueError('Vector length must match the number of interior interfaces')
		Draw = {'Index': DrawIndex, 'RawVector': Raw}
		Evidence['Draws'].append(Draw)
		try:
			Direction = reflection_direction(Raw, Sector, Normalize=True)
		except ZeroProjectionError as Error:
			Draw['Status'] = 'zero_projection'
			if Vector is not None:
				raise ZeroProjectionError(str(Error), Evidence) from Error
			continue
		Draw['Status'] = 'selected'
		break
	else:
		raise SeedGenerationError('No nonzero projection within MaxResamples', Evidence)
	Evidence.update({
		'RawVector': Raw,
		'Direction': Direction,
		'DirectionNorm': float(np.linalg.norm(Direction)),
		'DirectionSectorResidual': _sector_residual(Direction, Sector),
	})
	UsedStep = Step
	for Halvings in range(MaxHalvings + 1):
		with np.errstate(over='ignore', invalid='ignore'):
			Target = Base + UsedStep * Direction
		Attempt = {'Halvings': Halvings, 'Step': UsedStep, 'TargetEdges': Target}
		Evidence['Attempts'].append(Attempt)
		try:
			TargetWidths = interfaces_to_widths(Target, MinWidth=MinWidth)
		except ValueError as Error:
			Attempt.update({'Status': 'infeasible_target', 'Reason': str(Error)})
			UsedStep *= 0.5
			continue
		Attempt['TargetWidths'] = TargetWidths
		Z = None
		Widths = TargetWidths
		if UseCallbacks:
			try:
				Z = _vector(WidthsToZ(TargetWidths.copy()), 'Z')
				Widths = _vector(ZToWidths(Z.copy()), 'ConvertedWidths')
			except Exception as Error:
				Attempt.update({'Status': 'callback_error', 'Reason': f'{type(Error).__name__}: {Error}'})
				raise SeedGenerationError('Conversion callback failed', Evidence) from Error
		Attempt.update({'Z': Z, 'Widths': Widths})
		try:
			Check = check_sector_seed(
				Base, Widths, Sector, Direction=Direction, ExpectedStep=UsedStep,
				MinWidth=MinWidth, SectorTolerance=SectorTolerance, RoundTripTolerance=RoundTripTolerance,
			)
		except SeedValidationError as Error:
			Attempt.update({
				'Status': 'rejected_roundtrip' if UseCallbacks else 'rejected_geometry',
				'Reason': str(Error), 'Check': Error.Evidence,
			})
			if isinstance(Error, UnresolvedPerturbationError):
				raise SeedGenerationError('No resolvable nonzero actual perturbation; refusing further step reduction', Evidence) from Error
			UsedStep *= 0.5
			continue
		Attempt.update({'Status': 'accepted', 'Check': Check})
		Evidence.update({
			'Halvings': Halvings,
			'UsedStep': UsedStep,
			'ActualStep': Check['ActualStep'],
			'TargetEdges': Target,
			'TargetWidths': TargetWidths,
			'FinalWidths': Widths,
			'FinalCheck': Check,
		})
		return ReflectionSeed(
			Sector=Sector, BaseEdges=tuple(Base.tolist()), Direction=tuple(Direction.tolist()),
			RequestedStep=Step, UsedStep=UsedStep, ActualStep=Check['ActualStep'],
			Edges=tuple(Check['CheckedEdges']), Widths=tuple(Widths.tolist()),
			Z=None if Z is None else tuple(Z.tolist()), Evidence=_json_ready(Evidence),
		)
	raise SeedGenerationError('No feasible, resolved, faithful pure-sector seed within MaxHalvings', Evidence)
