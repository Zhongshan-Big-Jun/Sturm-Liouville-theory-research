"""Selected unmodified function bodies from _gapn2_jacobian_probe.py.
Commit be7c0912849a50a46869773eab4b3a2ec655ce88, full-source blob
b0c3372db4b997606229a0de2c4402ad0080b792. Not a whole-file byte copy.
Only this header and the required numpy/numbers imports are added.
"""
import numbers
import numpy as np

def _positive_integer(Value, Name):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Integral) or Value < 1:
		raise ValueError(Name + ' must be a positive integer')
	return int(Value)


def _real_array(Value, Shape, Name):
	Array = np.asarray(Value)
	if Array.shape != Shape or Array.dtype.kind not in 'iuf':
		raise ValueError(Name + ' has invalid shape or non-real entries')
	Array = np.array(Array, dtype=float, copy=True)
	if not np.all(np.isfinite(Array)):
		raise ValueError(Name + ' must be finite')
	return Array


def jac_fd(rc, z, h=1e-6, *, return_diagnostics=False):
	"""Central edge differences after checking BOTH physical endpoints.

	Each column perturbs only x_k; h is an upper bound, reduced separately
	for local widths and converter feasibility. The unchanged legacy converter
	may clip widths, so every round trip must match its intended endpoint.
	Off-axis drift and step error must be <= min(32*(m+1)*eps, 1e-6*step).
	Unresolvable steps, modified base points and nonfinite residuals raise.
	This checks geometry to float64 tolerance, not derivative truncation error.
	"""
	M = 2 * _positive_integer(rc.n, 'n')
	if isinstance(h, (bool, np.bool_)) or not isinstance(h, numbers.Real) or not np.isfinite(h) or h <= 0:
		raise ValueError('h must be positive and finite')
	if not isinstance(return_diagnostics, (bool, np.bool_)):
		raise ValueError('return_diagnostics must be boolean')
	Z = _real_array(z, (M + 1,), 'z')
	Eps = np.finfo(float).eps
	Tolerance = 32 * (M + 1) * Eps
	MinimumStep = 64 * Eps

	def checked_widths(Values):
		Widths = _real_array(Values, (M + 1,), 'widths')
		if np.any(Widths <= 0) or abs(float(np.sum(Widths)) - 1.) > Tolerance:
			raise ValueError('widths must be positive and sum to one without repair')
		return Widths

	def roundtrip(Edges, ErrorBudget):
		Widths = checked_widths(np.diff(np.r_[0., Edges, 1.]))
		Converted = _real_array(rc.widths_to_z(Widths.copy()), (M + 1,), 'converted z')
		ActualWidths = checked_widths(rc.z_to_widths(Converted.copy()))
		Actual = np.cumsum(ActualWidths)[:-1]
		Error = max(float(np.max(np.abs(Actual - Edges))), float(np.max(np.abs(ActualWidths - Widths))))
		if Error > ErrorBudget:
			raise ValueError('coordinate conversion changes the intended endpoint')
		return Converted, Actual, ActualWidths, Error

	Widths = checked_widths(rc.z_to_widths(Z.copy()))
	Edges = np.cumsum(Widths)[:-1]
	roundtrip(Edges, Tolerance)  # Reject an already clipped/unrepresentable base.
	J = np.empty((M, M))
	Columns = []
	for K in range(M):
		Step = min(float(h), 0.25 * min(float(Widths[K]), float(Widths[K + 1])))
		LastError = 'step is below the floating-point resolution guard'
		for Attempt in range(40):
			if Step <= MinimumStep:
				break
			Plus, Minus = Edges.copy(), Edges.copy()
			Plus[K] += Step
			Minus[K] -= Step
			Budget = min(Tolerance, 1e-6 * Step)
			try:
				Zp, Xp, Wp, Ep = roundtrip(Plus, Budget)
				Zm, Xm, Wm, Em = roundtrip(Minus, Budget)
				Target = np.zeros(M); Target[K] = Step
				MotionError = max(float(np.max(np.abs((Xp - Edges) - Target))),
					float(np.max(np.abs((Xm - Edges) + Target))))
				if MotionError > Budget or Xp[K] <= Edges[K] or Xm[K] >= Edges[K]:
					raise ValueError('converted displacement does not preserve the central edge direction')
			except (ValueError, ArithmeticError) as Error:
				LastError = str(Error)
				Step *= 0.5
				continue
			Fp = _real_array(rc.residual(Zp.copy()), (M,), 'positive residual')
			Fm = _real_array(rc.residual(Zm.copy()), (M,), 'negative residual')
			with np.errstate(over='ignore', invalid='ignore'):
				Column = (Fp - Fm) / (2 * Step)
			if not np.all(np.isfinite(Column)):
				raise ArithmeticError('finite-difference column overflowed')
			J[:, K] = Column
			Columns.append({'edge_index': K, 'used_step': Step, 'backtracks': Attempt,
				'plus_edges': Xp.tolist(), 'minus_edges': Xm.tolist(),
				'minimum_endpoint_width': float(min(np.min(Wp), np.min(Wm))),
				'max_roundtrip_error': max(Ep, Em), 'max_motion_error': MotionError,
				'geometry_error_budget': Budget})
			break
		if len(Columns) != K + 1:
			raise ArithmeticError(f'edge {K}: no faithful resolvable central difference; {LastError}')
	Evidence = {'certified': False, 'method': 'independent-edge central differences with checked round trips',
		'requested_step': float(h), 'base_edges': Edges.tolist(), 'columns': Columns,
		'limitation': 'finite float64 geometry checks; no interval or derivative-error bound'}
	return (J, Evidence) if return_diagnostics else J


def jacobian_cross_blocks(J, n, *, rtol=1e-6, atol=1e-8, return_diagnostics=False):
	"""Return C,D of the reversal-even/odd CROSS decomposition of JP=-PJ.

	C maps odd input (physical-preserving) to even output; D maps even input
	(physical-breaking) to odd output. Reject incompatible matrices; do not
	apply this function to a commuting Hessian. Tolerances are diagnostics.
	"""
	N = _positive_integer(n, 'n')
	J = _real_array(J, (2 * N, 2 * N), 'J')
	for Value in (rtol, atol):
		if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Real) or not np.isfinite(Value) or Value < 0:
			raise ValueError('block tolerances must be finite and nonnegative')
	if not isinstance(return_diagnostics, (bool, np.bool_)):
		raise ValueError('return_diagnostics must be boolean')
	S = np.zeros_like(J)
	for K in range(N):
		S[K, K] = S[K, 2 * N - 1 - K] = 1.
		S[N + K, K] = 1.
		S[N + K, 2 * N - 1 - K] = -1.
	with np.errstate(over='ignore', invalid='ignore'):
		Matrix = S @ J @ (S.T / 2.)
		AntiError = float(np.max(np.abs(J[:, ::-1] + J[::-1, :])))
	if not np.all(np.isfinite(Matrix)) or not np.isfinite(AntiError):
		raise ArithmeticError('reflection block calculation overflowed')
	DiagonalError = float(max(np.max(np.abs(Matrix[:N, :N])), np.max(np.abs(Matrix[N:, N:]))))
	Limit = float(atol + rtol * np.max(np.abs(J)))
	if not np.isfinite(Limit) or AntiError > Limit or DiagonalError > Limit:
		raise ValueError(f'J is not reversal-anticommuting within tolerance: JP+PJ={AntiError:g}, diagonal={DiagonalError:g}, limit={Limit:g}')
	C, D = Matrix[:N, N:].copy(), Matrix[N:, :N].copy()
	Evidence = {'certified': False, 'coordinate_order': 'reversal-even then reversal-odd',
		'C_map': 'odd input to even output', 'D_map': 'even input to odd output',
		'anticommutator_max': AntiError, 'diagonal_block_max': DiagonalError, 'tolerance': Limit,
		'determinant_identity': 'det(J)=(-1)^n det(C) det(D) when JP=-PJ exactly'}
	return (C, D, Evidence) if return_diagnostics else (C, D)
