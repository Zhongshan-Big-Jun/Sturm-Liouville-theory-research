"""Shared numerical DD/DN spectrum identity for Green kernel entrypoints.

The left boundary is Dirichlet. Modes are one-based and bound to binary64
positive block geometry and right D/N boundary. Phase brackets and error
radii are floating diagnostics, not interval certificates or tail bounds.
"""
import numbers
from dataclasses import dataclass
import numpy as np

from _sl_prufer import indexed_roots, lifted_phase, positive_blocks


def positive_count(Value, Name):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, (int, np.integer)) or Value < 1:
		raise ValueError(Name + ' must be a positive integer')
	return int(Value)


def right_boundary(Value):
	if not isinstance(Value, str) or Value not in ('D', 'N'):
		raise ValueError('right boundary must be D or N')
	return Value


def real_parameter(Value, Name):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Real) or not np.isfinite(Value):
		raise ValueError(Name + ' must be a finite real scalar')
	return float(Value)


def legacy_pole_mode(Index, Name='pole index'):
	"""Explicitly convert a checked legacy zero-based index to a mode number."""
	if isinstance(Index, (bool, np.bool_)) or not isinstance(Index, (int, np.integer)) or Index < 0:
		raise ValueError(Name + ' must be a nonnegative integer')
	return int(Index) + 1


@dataclass(frozen=True, init=False)
class IndexedSpectrum:
	"""Immutable equation-derived mode table shared by full and half intervals."""
	blocks: tuple
	boundary: str
	eigenvalues: tuple
	error_radii: tuple
	phase_records: tuple

	def __init__(self, Blocks, Boundary, Count):
		Boundary = right_boundary(Boundary)
		Count = positive_count(Count, 'mode count')
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
			raise ArithmeticError('indexed eigenvalues are not numerically resolvable')
		object.__setattr__(self, 'blocks', tuple(tuple(map(float, Block)) for Block in Values))
		object.__setattr__(self, 'boundary', Boundary)
		object.__setattr__(self, 'eigenvalues', tuple(map(float, Eigenvalues)))
		object.__setattr__(self, 'error_radii', tuple(map(float, Radii)))
		object.__setattr__(self, 'phase_records', tuple(tuple((Key, tuple(Value) if isinstance(Value, list) else Value)
			for Key, Value in sorted(Record.items())) for Record in Records))

	def prefix(self, Count):
		Count = positive_count(Count, 'prefix count')
		if Count > len(self.eigenvalues):
			raise ValueError('requested prefix exceeds the indexed table')
		return np.array(self.eigenvalues[:Count])

	def frequency_prefix(self, Count):
		"""Retain the original indexed frequencies, without a square-root round trip."""
		self.prefix(Count)
		return np.array([dict(Record)['frequency'] for Record in self.phase_records[:Count]])


def spectrum_for(Blocks, Boundary, Count, Spectrum=None):
	Count = positive_count(Count, 'spectral truncation')
	Boundary = right_boundary(Boundary)
	Geometry = tuple(tuple(map(float, Block)) for Block in positive_blocks(Blocks))
	if Spectrum is None:
		Spectrum = IndexedSpectrum(Geometry, Boundary, Count)
	if not isinstance(Spectrum, IndexedSpectrum):
		raise ValueError('spectrum must be an indexed spectrum table')
	if Spectrum.blocks != Geometry or Spectrum.boundary != Boundary:
		raise ValueError('spectral table geometry or boundary does not match the equation')
	Spectrum.prefix(Count)
	return Spectrum


def green_points(Table, Points):
	if np.iscomplexobj(Points):
		raise ValueError('Green evaluation points must be real')
	try:
		Values = np.asarray(Points, dtype=float)
	except (TypeError, ValueError, OverflowError) as Error:
		raise ValueError('Green evaluation points must be a finite one-dimensional array') from Error
	if Values.ndim != 1 or not np.all(np.isfinite(Values)):
		raise ValueError('Green evaluation points must be a finite one-dimensional array')
	Length = float(np.cumsum(np.array(Table.blocks)[:, 0])[-1])
	if np.any(Values < 0) or np.any(Values > Length):
		raise ValueError('Green evaluation point lies outside the interval')
	return Values


def spectral_denominators(Table, Target, Count, *, PoleMode=None):
	"""Check coverage, target identity and every retained numerical denominator."""
	Target = real_parameter(Target, 'spectral target')
	Count = positive_count(Count, 'spectral truncation')
	Modes = Table.prefix(Count)
	AllModes = np.array(Table.eigenvalues)
	with np.errstate(over='raise', invalid='raise'):
		try:
			Tolerance = 4 * np.array(Table.error_radii) + 16 * np.finfo(float).eps * abs(Target)
			Differences = AllModes - Target
		except FloatingPointError as Error:
			raise ArithmeticError('spectral target differences exceed floating-point range') from Error
	if not np.all(np.isfinite(Differences)) or not np.all(np.isfinite(Tolerance)):
		raise ArithmeticError('spectral target differences are not finite')
	Near = np.abs(Differences) <= Tolerance
	if PoleMode is not None:
		PoleMode = positive_count(PoleMode, 'one-based pole mode')
		if PoleMode > Count:
			raise ValueError('pole mode is outside the requested prefix')
		if np.flatnonzero(Near).tolist() != [PoleMode - 1]:
			raise ValueError('target eigenvalue does not uniquely match the specified pole mode')
	else:
		if np.any(Near):
			raise ValueError('full Green target is at or numerically near a tabulated pole')
		if Target >= AllModes[-1] - Tolerance[-1]:
			raise ValueError('full Green target requires a larger table to resolve its spectral location')
	Keep = np.ones(Count, dtype=bool)
	if PoleMode is not None:
		Keep[PoleMode - 1] = False
	Denominators = Differences[:Count][Keep]
	if (not np.all(np.isfinite(Denominators))
		or np.any(np.abs(Denominators) <= Tolerance[:Count][Keep])):
		raise ArithmeticError('retained spectral denominator is not resolvable')
	return Modes, Keep, Denominators


def reduced_pole_table(Blocks, Target, Boundary, *, Mode=None, Spectrum=None):
	"""Resolve a closed reduced kernel's one-based pole, then verify its identity.

	For legacy calls without Mode, lifted phase proposes a mode number; the
	indexed table must still uniquely match Target. A positive parameter alone
	never establishes eigenvalue identity. A supplied table is geometry/BC bound.
	"""
	Target = real_parameter(Target, 'eigenvalue')
	if Target <= 0:
		raise ValueError('reduced Green requires a positive eigenvalue; use green_regular at mu<=0')
	Boundary = right_boundary(Boundary)
	Geometry = positive_blocks(Blocks)
	if Mode is not None:
		Mode = positive_count(Mode, 'one-based pole mode')
	Phase = float(lifted_phase(Geometry, np.sqrt(Target)))
	if Phase * np.finfo(float).eps > 1e-5:
		raise ArithmeticError('phase winding is too large for double-precision pole identity')
	PhaseMode = int(np.rint(Phase / np.pi + (0.5 if Boundary == 'N' else 0.0)))
	if Mode is None:
		Mode = PhaseMode
	Mode = positive_count(Mode, 'one-based pole mode')
	if Mode != PhaseMode:
		raise ValueError('target phase does not match the specified one-based pole mode')
	Count = Mode + 1 if Spectrum is None else Mode
	Table = spectrum_for(Geometry, Boundary, Count, Spectrum)
	spectral_denominators(Table, Target, len(Table.eigenvalues), PoleMode=Mode)
	return Table, Mode
