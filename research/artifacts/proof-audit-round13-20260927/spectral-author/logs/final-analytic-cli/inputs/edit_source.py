from pathlib import Path
Root = Path('/mnt/f/LaTeX/BVE research/scripts')

def replace_functions(Text, Start, End, Replacement):
	Left = Text.index('def '+Start+'(')
	Right = Text.index(End,Left)
	return Text[:Left]+Replacement.rstrip()+'\n\n\n'+Text[Right:]

PathName = Root/'_gapn2_symmetry_recon.py'
Text = PathName.read_text().replace('import sys, json, time, argparse, hashlib','import sys, json, time, argparse, hashlib\nimport numbers')
Text = Text.replace('from _sl_prufer import indexed_roots','from _sl_prufer import indexed_roots, positive_blocks')
Text = replace_functions(Text,'eigfun','class Recon:', '''def _real_parameter(Value, Name):
	if isinstance(Value, (bool, np.bool_)) or not isinstance(Value, numbers.Real) or not np.isfinite(Value):
		raise ValueError(Name + ' must be a finite real scalar')
	return float(Value)


def _propagation_input(blocks, mu, pts):
	Blocks = positive_blocks(blocks)
	Mu = _real_parameter(mu, 'mu')
	if np.iscomplexobj(pts):
		raise ValueError('evaluation points must be real')
	Points = np.asarray(pts, dtype=float)
	Ends = np.r_[0.0, np.cumsum(Blocks[:, 0])]
	if Points.ndim != 1 or not np.all(np.isfinite(Points)):
		raise ValueError('evaluation points must be a finite one-dimensional array')
	if np.any(Points < 0) or np.any(Points > Ends[-1]):
		raise ValueError('evaluation point lies outside the interval')
	return Blocks, Mu, Points, Ends


def _transfer_matrix(Mu, Length, Density):
	"""Physical (u,u') transfer. Caller guards floating range and input domain."""
	if Mu == 0:
		return np.array([[1.0, Length], [0.0, 1.0]])
	Wave = np.sqrt(abs(Mu)) * np.sqrt(Density)
	Angle = Wave * Length
	if Mu > 0:
		C = np.cos(Angle)
		S = Length * np.sinc(Angle / np.pi)
		Lower = -Wave * np.sin(Angle)
	else:
		C = np.cosh(Angle)
		S = Length * (np.sinh(Angle) / Angle if Angle != 0 else 1.0)
		Lower = Wave * np.sinh(Angle)
	return np.array([[C, S], [Lower, C]])


def _fundamental_states(Blocks, Mu, RightBoundary=None):
	States = np.empty((len(Blocks) + 1, 2))
	if RightBoundary is None:
		States[0] = [0.0, 1.0]
		for i, (Length, Density) in enumerate(Blocks):
			States[i + 1] = _transfer_matrix(Mu, Length, Density) @ States[i]
	else:
		States[-1] = [0.0, -1.0] if RightBoundary == 'D' else [1.0, 0.0]
		for i in range(len(Blocks) - 1, -1, -1):
			Length, Density = Blocks[i]
			States[i] = _transfer_matrix(Mu, -Length, Density) @ States[i + 1]
	return States


def _sample_solution(Blocks, Mu, Points, Ends, States, FromRight=False):
	Out = np.empty((len(Points), 2))
	for j, Point in enumerate(Points):
		i = min(int(np.searchsorted(Ends, Point, side='right')) - 1, len(Blocks) - 1)
		Anchor = i + 1 if FromRight else i
		Out[j] = _transfer_matrix(Mu, Point - Ends[Anchor], Blocks[i, 1]) @ States[Anchor]
	return Out


def solution_states(blocks, mu, pts, *, right_boundary=None):
	"""Physical states for real mu, including 0 and negative resolvent parameters.

	Default initial data are (0,1) at the left endpoint. Right D/N initial
	data are (0,-1)/(1,0). Endpoints, duplicates and arbitrary point order are
	legal. Invalid geometry/points raise ValueError; float overflow raises
	ArithmeticError. Hyperbolic propagation is unscaled, not arbitrary-range.
	"""
	if right_boundary is not None and right_boundary not in ('D', 'N'):
		raise ValueError('right boundary must be D or N')
	Blocks, Mu, Points, Ends = _propagation_input(blocks, mu, pts)
	with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
		States = _fundamental_states(Blocks, Mu, right_boundary)
		Out = _sample_solution(Blocks, Mu, Points, Ends, States, right_boundary is not None)
	if not np.all(np.isfinite(States)) or not np.all(np.isfinite(Out)):
		raise ArithmeticError('physical propagation is not finite')
	return Out


def real_green_matrix(blocks, mu, pts, *, right_boundary='D'):
	"""Kernel of -d^2/dx^2-mu*rho with left D and right D/N boundary.

	Real resolvent parameters, including all mu<=0, are supported subject to
	floating range. Numerically unresolved positive poles raise ArithmeticError.
	The coordinate comparison is invariant under permutations and duplicates.
	"""
	if right_boundary not in ('D', 'N'):
		raise ValueError('right boundary must be D or N')
	Blocks, Mu, Points, Ends = _propagation_input(blocks, mu, pts)
	with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
		Left = _fundamental_states(Blocks, Mu)
		Right = _fundamental_states(Blocks, Mu, right_boundary)
		Phi = _sample_solution(Blocks, Mu, Points, Ends, Left)[:, 0]
		Psi = _sample_solution(Blocks, Mu, Points, Ends, Right, True)[:, 0]
		# Evaluate -W at the right boundary, avoiding cancellation of products.
		Denominator = Left[-1, 0 if right_boundary == 'D' else 1]
		Scale = max(abs(Left[-1, 0]), Ends[-1] * abs(Left[-1, 1]))
		Residual = abs(Denominator) * (1.0 if right_boundary == 'D' else Ends[-1])
		if not np.isfinite(Scale) or Residual <= 64 * np.finfo(float).eps * Scale:
			raise ArithmeticError('Green target is at or numerically near a pole')
		Forward = np.outer(Phi, Psi)
		Kernel = np.where(Points[:, None] <= Points[None, :], Forward, Forward.T) / Denominator
	if not np.all(np.isfinite(Kernel)):
		raise ArithmeticError('Green kernel is not finite')
	return Kernel


def eigenfunction_states(blocks, s, pts):
	"""Values AND derivatives of one physical solution divided by its mass.

	The left solution has (u,u')=(0,1). Its exact block integrals are evaluated
	in midpoint coordinates, with a Taylor limit for small frequency*length.
	No normalization is reconstructed from point values, even at nodes.
	"""
	Frequency = _real_parameter(s, 'frequency')
	if Frequency < 0:
		raise ValueError('frequency must be nonnegative')
	with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
		Blocks, Mu, Points, Ends = _propagation_input(blocks, np.float64(Frequency)**2, pts)
		States = _fundamental_states(Blocks, Mu)
		Mass = 0.0
		for i, (Length, Density) in enumerate(Blocks):
			Angle = Frequency * np.sqrt(Density) * Length
			Midpoint = _transfer_matrix(Mu, Length / 2, Density) @ States[i]
			CosIntegral = Length * (1.0 + np.sinc(Angle / np.pi)) / 2
			if abs(Angle) < 0.01:
				Q = Angle**2
				SinIntegral = Length**3 * (1/12 - Q/240 + Q**2/10080 - Q**3/725760)
			else:
				SinIntegral = Length * (1.0 - np.sinc(Angle / np.pi)) / (2 * (Frequency * np.sqrt(Density))**2)
			Mass += Density * (Midpoint[0]**2 * CosIntegral + Midpoint[1]**2 * SinIntegral)
		if not np.isfinite(Mass) or Mass <= 0:
			raise ArithmeticError('eigenfunction mass is not finite and positive')
		Out = _sample_solution(Blocks, Mu, Points, Ends, States) / np.sqrt(Mass)
	if not np.all(np.isfinite(Out)):
		raise ArithmeticError('normalized eigenfunction states are not finite')
	return Out


def eigfun(blocks, s, pts):
	"""L2(rho)-normalized values; derivatives share exactly the same mass."""
	return eigenfunction_states(blocks, s, pts)[:, 0]
''')
PathName.write_text(Text)

PathName = Root/'_gapn2_jacobian_analytic.py'
Text = PathName.read_text()
Text = Text.replace('from _gapn2_symmetry_recon import Recon, roots_of, eigfun','from _gapn2_symmetry_recon import (Recon, roots_of, eigfun, eigenfunction_states,\n\tsolution_states, real_green_matrix, _real_parameter, _transfer_matrix, positive_blocks)')
Text = replace_functions(Text,'prop_matrix','def regularized_green(', '''def prop_matrix(blocks, s):
	"""Physical transfer for frequency s, including the linear limit s=0."""
	Frequency = _real_parameter(s, 'frequency')
	Blocks = positive_blocks(blocks)
	M = np.eye(2)
	with np.errstate(over='raise', invalid='raise', divide='raise', under='ignore'):
		Mu = np.float64(Frequency)**2
		for Length, Density in Blocks:
			M = _transfer_matrix(Mu, Length, Density) @ M
	if not np.all(np.isfinite(M)):
		raise ArithmeticError('transfer matrix is not finite')
	return M


def uv_at(blocks, s, pts, left=True):
	"""Physical states at arbitrary points, with endpoint data (0,1)/(0,-1).

	The compatibility parameter s is frequency; use solution_states for a
	real spectral parameter mu (including mu<0).
	"""
	Frequency = _real_parameter(s, 'frequency')
	with np.errstate(over='raise', invalid='raise'):
		Mu = np.float64(Frequency)**2
	return solution_states(blocks, Mu, pts, right_boundary=None if left else 'D')


def green_kernel(blocks, mu, pts):
	"""DD Green matrix for real resolvent mu, in the supplied coordinate order."""
	return real_green_matrix(blocks, mu, pts)
''')
Text = replace_functions(Text,'eigen_data','def main():', '''def eigen_data(rc, z):
	"""Adjacent eigenvalues and mass-normalized physical states at switches.

	eps is sign(u_n)*sign(u_{n+1}); its band sign interpretation and the
	Wronskian f' identity require stationarity and nonzero interface values.
	"""
	Blocks = rc.blocks_from_z(z)
	Frequencies = roots_of(Blocks, rc.n + 1)
	A, B = Frequencies[rc.n - 1]**2, Frequencies[rc.n]**2
	Edges = np.cumsum(rc.z_to_widths(z))[:-1]
	U = eigenfunction_states(Blocks, Frequencies[rc.n - 1], Edges)
	V = eigenfunction_states(Blocks, Frequencies[rc.n], Edges)
	return dict(lam_n=A, lam_np1=B, edges=Edges, u_n=U[:, 0], u_np1=V[:, 0],
		up_n=U[:, 1], up_np1=V[:, 1], c=np.sqrt(A / B),
		eps=np.sign(U[:, 0]) * np.sign(V[:, 0]), W=V[:, 1] * U[:, 0] - V[:, 0] * U[:, 1])


def jacobian_terms(Data, Jumps, Gn, Gnp1):
	"""Unscaled terms of d(f/b)/dx at any feasible configuration.

	A=lambda_n, B=lambda_{n+1}, f=A*u^2-B*v^2. Moving switch i gives
	d_i B=B*s_i*v_i^2, so the quotient contributes -s_i*f_j*v_i^2.
	M1 includes that term. At f=0 it reduces to the stationary rank-one
	term 2*s_i*w_i*w_j*(B-A)/(A*B). Green sums remain finite evidence.
	"""
	A, B = Data['lam_n'], Data['lam_np1']
	U, V = Data['u_n'], Data['u_np1']
	F = A * U**2 - B * V**2
	M1 = (2*A*np.outer(U**2, U**2) - 2*B*np.outer(V**2, V**2) - np.outer(F, V**2)) * Jumps[None, :]
	M2 = -2*A**2 * np.outer(U, U) * Gn * Jumps[None, :]
	M3 = 2*B**2 * np.outer(V, V) * Gnp1 * Jumps[None, :]
	Fprime = 2*A*U*Data['up_n'] - 2*B*V*Data['up_np1']
	Stationary = 2*A*(B-A)/B * np.outer(U**2, U**2) * Jumps[None, :]
	return dict(fprime=Fprime, M1=M1, M2=M2, M3=M3, s=Jumps, wj=A*U**2, D=B-A,
		M1_stationary=Stationary, correction=M1-Stationary, eigen_data=Data)


def term_breakdown(rc, z, N=2000):
	"""General Jacobian terms; J=(diag(fprime)+M1+M2+M3)/lambda_{n+1}.

	M1 is the full normalization/quotient term. M1_stationary and correction
	separate its old stationary specialization from the nonstationary part.
	"""
	Data = eigen_data(rc, z)
	from _gapn2_jacobian_spectral import gtilde_spectral
	Gn = gtilde_spectral(rc, z, Data['lam_n'], rc.n - 1, Data['edges'], N=N)
	Gnp1 = gtilde_spectral(rc, z, Data['lam_np1'], rc.n, Data['edges'], N=N)
	return jacobian_terms(Data, np.diff(rc.pat), Gn, Gnp1)


def analytic_jacobian(rc, z, N=2000):
	"""General physical-interface Jacobian with finite spectral Green sums.

	The returned fprime_id is a stationary Wronskian diagnostic only; it is
	not used to assemble J. N controls the numerical spectral truncation.
	"""
	Terms = term_breakdown(rc, z, N=N)
	Data = Terms['eigen_data']
	B = Data['lam_np1']
	J = (np.diag(Terms['fprime']) + Terms['M1'] + Terms['M2'] + Terms['M3']) / B
	FprimeId = -2*B*Data['eps']*Data['c']*Data['W']
	return J, Terms['fprime'], FprimeId, Terms['wj'], B*Data['u_np1']**2
''')
Text = Text.replace('Claims (all to be verified numerically, EVIDENCE):','Round13: all three Jacobian entrypoints use the general quotient derivative.\nThe stationary identities below are preserved at F=0. Finite Green sums are\nnumerical evidence, not certified tail bounds.\n\nClaims (all to be verified numerically, EVIDENCE):')
Text = Text.replace('gtilde_spectral from\n    _gapn2_jacobian_spectral (Richardson-accelerated).','gtilde_spectral from\n    _gapn2_jacobian_spectral (finite spectral sum; no certified tail bound).')
PathName.write_text(Text)

PathName = Root/'_gapn2_jacobian_spectral.py'
Text = PathName.read_text()
Text = Text.replace('from _gapn2_jacobian_analytic import eigen_data','from _gapn2_jacobian_analytic import term_breakdown')
Text = replace_functions(Text,'analytic_jacobian_spectral','def main():', '''def analytic_jacobian_spectral(rc, z, N=2000):
	"""General residual Jacobian; exact shape formula, finite Green truncation."""
	Terms = term_breakdown(rc, z, N=N)
	return (np.diag(Terms['fprime']) + Terms['M1'] + Terms['M2'] + Terms['M3']) / Terms['eigen_data']['lam_np1']
''')
Text = Text.replace('Jacobian formula (verified','The implementation uses the general nonstationary quotient derivative in\nterm_breakdown; the following formula is its F=0 specialization.\n\nStationary Jacobian formula (verified')
PathName.write_text(Text)

PathName = Root/'_gapn2_half_problem_probe.py'
Text = PathName.read_text().replace('from _gapn2_symmetry_recon import Recon, roots_of, eigfun','from _gapn2_symmetry_recon import Recon, roots_of, eigfun, solution_states, real_green_matrix')
Text = replace_functions(Text,'_propagate','def _norm2(', '''def _propagate(hblocks, mu, x):
	"""Physical left solution for finite real mu, including mu<=0."""
	return tuple(solution_states(hblocks, mu, [x])[0])
''')
Text = replace_functions(Text,'green_regular','def _prims_9(', '''def green_regular(hblocks, mu, x, y, bc):
	"""DD/DN Green kernel at real resolvent mu, including linear/hyperbolic cases.

	Endpoints and either coordinate order are legal. Out-of-domain inputs,
	invalid BCs and unresolved poles/overflow raise instead of returning nan.
	"""
	return float(real_green_matrix(hblocks, mu, [x, y], right_boundary=bc)[0, 1])
''')
PathName.write_text(Text)
print('Edited only the four authorized source files.')
