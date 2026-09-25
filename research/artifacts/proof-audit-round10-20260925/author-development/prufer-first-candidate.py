"""Indexed Dirichlet frequencies for positive piecewise constant densities.

Each target is the lifted phase level n*pi, not an M01 sign-scan hit.
Floating-point brackets and residuals are diagnostics, NOT interval certificates.
"""
import math
import numpy as np


def positive_blocks(Blocks):
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
	with np.errstate(over='ignore', under='ignore'):
		Edges = np.r_[0.0, np.cumsum(Values[:, 0])]
		Optical = Values[:, 0] * np.sqrt(Values[:, 1])
	if not np.all(np.isfinite(Edges)) or np.any(np.diff(Edges) <= 0):
		raise ValueError('block endpoints are not resolvable in double precision')
	if not np.all(np.isfinite(Optical)) or np.any(Optical <= 0):
		raise ValueError('optical block lengths are not resolvable')
	return Values


def _angle_scale(Angle, Scale):
	"""Lift atan2(Scale*sin(Angle), cos(Angle)) without losing half turns."""
	Turns = np.floor(Angle / np.pi)
	Remainder = Angle - Turns * np.pi
	if Scale >= 1:
		Mapped = np.arctan2(np.sin(Remainder), np.cos(Remainder) / Scale)
	else:
		Mapped = np.arctan2(Scale * np.sin(Remainder), np.cos(Remainder))
	return Turns * np.pi + Mapped


def _phase(Values, Frequencies):
	Angle = np.zeros_like(Frequencies, dtype=float)
	for Length, Density in Values:
		RootDensity = math.sqrt(Density)
		Angle = _angle_scale(Angle, RootDensity)
		Angle += Frequencies * (RootDensity * Length)
		Angle = _angle_scale(Angle, 1 / RootDensity)
	return Angle


def lifted_phase(Blocks, Frequencies):
	"""Continuous spatial lift of atan2(omega*y, y'), starting from zero.

	y(0)=0, y'(0)=1. At a Dirichlet eigenfrequency omega_n, this is n*pi.
	Block-local angles rotate exactly by omega*sqrt(rho)*length; positive
	coordinate changes at the interfaces retain their integer half turns.
	"""
	Values = positive_blocks(Blocks)
	if np.iscomplexobj(Frequencies):
		raise ValueError('frequencies must be real')
	Frequencies = np.asarray(Frequencies, dtype=float)
	if not np.all(np.isfinite(Frequencies)) or np.any(Frequencies < 0):
		raise ValueError('frequencies must be finite and nonnegative')
	with np.errstate(over='ignore', invalid='ignore'):
		Phase = _phase(Values, Frequencies)
	if not np.all(np.isfinite(Phase)):
		raise ArithmeticError('phase exceeds floating-point range')
	return Phase


def indexed_roots(Blocks, Count, Refine=60):
	"""Return frequencies and per-index numerical phase brackets.

	For total length L and 0<m<=rho<=M, n*pi/(L*sqrt(M)) <= omega_n
	<= n*pi/(L*sqrt(m)). Each bracket is bisected against its own n*pi.
	Insufficient refinement or unresolved roots raise, rather than relabeling
	higher roots. No fixed frequency grid or secular sign alternation is used.
	"""
	Values = positive_blocks(Blocks)
	for Number, Name in ((Count, 'mode count'), (Refine, 'root refinement')):
		if isinstance(Number, (bool, np.bool_)) or not isinstance(Number, (int, np.integer)) or Number < 1:
			raise ValueError(Name + ' must be a positive integer')
	Indices = np.arange(1, Count + 1, dtype=float)
	Targets = np.pi * Indices
	Length = float(np.sum(Values[:, 0]))
	with np.errstate(over='ignore', under='ignore', invalid='ignore', divide='ignore'):
		LowerComparison = (Targets / Length) / np.sqrt(np.max(Values[:, 1]))
		UpperComparison = (Targets / Length) / np.sqrt(np.min(Values[:, 1]))
		Lo = np.zeros(Count)
		Hi = 1.125 * UpperComparison
	if not np.all(np.isfinite(Hi)) or np.any(LowerComparison <= 0):
		raise ArithmeticError('frequency comparison scale is not resolvable')
	with np.errstate(over='ignore', invalid='ignore'):
		InitialPhase = _phase(Values, Hi)
	if not np.all(np.isfinite(InitialPhase)) or np.any(InitialPhase <= Targets):
		raise ArithmeticError('comparison bound failed to bracket a phase index')
	if np.max(InitialPhase) * np.finfo(float).eps > 1e-5:
		raise ArithmeticError('phase winding is too large for double-precision enumeration')
	for _ in range(Refine):
		Mid = Lo + (Hi - Lo) / 2
		Phase = _phase(Values, Mid)
		Below = Phase < Targets
		Lo = np.where(Below, Mid, Lo)
		Hi = np.where(Below, Hi, Mid)
	Mid = Lo + (Hi - Lo) / 2
	Candidates = np.stack((Lo, Mid, Hi))
	Errors = np.abs(_phase(Values, Candidates) - Targets)
	Choice = np.argmin(Errors, axis=0)
	Roots = Candidates[Choice, np.arange(Count)]
	Residuals = Errors[Choice, np.arange(Count)]
	LoPhase, HiPhase = _phase(Values, Lo), _phase(Values, Hi)
	Tolerance = 128 * np.finfo(float).eps * np.maximum(Roots, LowerComparison)
	if (not np.all(np.isfinite(Roots)) or np.any(Roots <= 0)
		or np.any(np.diff(Roots) <= 0) or np.any(Hi - Lo > Tolerance)
		or np.any(Residuals > 2e-8) or np.any(LoPhase > Targets)
		or np.any(HiPhase < Targets)):
		raise ArithmeticError('indexed roots are unresolved; increase precision/refinement, not the scan grid')
	Records = [dict(index=i + 1, frequency=float(Roots[i]), bracket=[float(Lo[i]), float(Hi[i])],
		phase_bracket=[float(LoPhase[i]), float(HiPhase[i])], target_phase=float(Targets[i]),
		phase_residual=float(Residuals[i]), comparison=[float(LowerComparison[i]), float(UpperComparison[i])],
		certified=False) for i in range(Count)]
	return Roots, Records


def mp_lifted_phase(Blocks, Frequency):
	"""High-precision scalar lift; caller owns mpmath precision/context.

	This checks index in a different arithmetic precision, not an independent
	interval implementation or a proof of correct floating-point execution.
	"""
	import mpmath as mp
	Angle = mp.mpf(0)
	def ScaleAngle(Value, Scale):
		Turns = mp.floor(Value / mp.pi)
		Remainder = Value - Turns * mp.pi
		return Turns * mp.pi + mp.atan2(Scale * mp.sin(Remainder), mp.cos(Remainder))
	if not mp.isfinite(Frequency) or Frequency < 0:
		raise ValueError('frequency must be finite and nonnegative')
	for Length, Density in Blocks:
		if not mp.isfinite(Length) or not mp.isfinite(Density) or Length <= 0 or Density <= 0:
			raise ValueError('block lengths and densities must be finite and positive')
		RootDensity = mp.sqrt(Density)
		Angle = ScaleAngle(Angle, RootDensity) + Frequency * RootDensity * Length
		Angle = ScaleAngle(Angle, 1 / RootDensity)
	return Angle
