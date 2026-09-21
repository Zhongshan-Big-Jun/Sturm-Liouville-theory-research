#!/usr/bin/env python3
"""Author-side probes, independently implemented from the supplied audit code.

No repository Python tool or submitted verification script is imported or run.
These probes do not establish the all-index closure theorem or independent approval.
"""

import argparse
import hashlib
import json
import platform
from pathlib import Path

import mpmath as mp
import sympy as sp


Results = []
X = sp.symbols('x', real=True)
A = sp.symbols('a', positive=True)
C = sp.symbols('c', positive=True)
M = sp.symbols('m', integer=True, positive=True)


def record_check(Name, Condition, Detail=None):
	Entry = {'name': Name, 'pass': bool(Condition)}
	if(Detail is not None):
		Entry['detail'] = Detail
	Results.append(Entry)
	if(not Condition):
		raise RuntimeError('FAILED: ' + Name + ' ' + str(Detail or ''))


def check_zero(Name, Expression):
	Reduced = sp.simplify(sp.expand(Expression))
	record_check(Name, Reduced == 0, str(Reduced))


def make_p(Index):
	if(Index == 0):
		return sp.Integer(1)
	if(Index == 1):
		return X
	DegreeHalf = Index // 2
	return X**Index - sp.Rational(DegreeHalf, DegreeHalf - 1) * X**(Index - 2)


def endpoint_vector(Polynomial):
	Derivative = sp.diff(Polynomial, X)
	DeltaHalf = (Polynomial.subs(X, 1) - Polynomial.subs(X, -1)) / 2
	return sp.Matrix([Derivative.subs(X, 1) - DeltaHalf, Derivative.subs(X, -1) - DeltaHalf])


def polynomial_integral(Expression):
	Expanded = sp.Poly(sp.expand(Expression), X)
	Value = sp.Integer(0)
	for((Degree,), Coefficient) in Expanded.terms():
		if(Degree % 2 == 0):
			Value += Coefficient * sp.Rational(2, Degree + 1)
	return sp.simplify(Value)


def symbolic_checks():
	Denominator = A * sp.cosh(A) - sp.sinh(A)
	KernelPieces = [
		[sp.cosh(A * (1 + X)) / (2 * A * sp.sinh(A)), sp.cosh(A * (1 - X)) / (2 * A * sp.sinh(A))],
		[-(A * sp.cosh(A * (1 + X)) - sp.sinh(A * (1 + X))) / (2 * Denominator),
		 (A * sp.cosh(A * (1 - X)) - sp.sinh(A * (1 - X))) / (2 * Denominator)]
	]
	for(Index, (Left, Right)) in enumerate(KernelPieces):
		for(Side, Piece) in (('left', Left), ('right', Right)):
			check_zero(f'kernel_{Index}_{Side}_ode', -sp.diff(Piece, X, 2) + A**2 * Piece)
		ValueJump = Right.subs(X, 0) - Left.subs(X, 0)
		DerivativeJump = sp.diff(Right, X).subs(X, 0) - sp.diff(Left, X).subs(X, 0)
		check_zero(f'kernel_{Index}_value_jump', ValueJump - [0, 1][Index])
		check_zero(f'kernel_{Index}_derivative_jump', DerivativeJump - [-1, 0][Index])
		DeltaHalf = (Right.subs(X, 1) - Left.subs(X, -1)) / 2
		check_zero(f'kernel_{Index}_left_endpoint', sp.diff(Left, X).subs(X, -1) - DeltaHalf)
		check_zero(f'kernel_{Index}_right_endpoint', sp.diff(Right, X).subs(X, 1) - DeltaHalf)
		for Degree in (0, 1):
			Scale = 2 * A * sp.sinh(A) if(Index == 0) else 2 * Denominator
			LeftNumerator = sp.simplify(Left * Scale) * X**Degree
			RightNumerator = sp.simplify(Right * Scale) * X**Degree
			Moment = (sp.integrate(LeftNumerator.rewrite(sp.exp), (X, -1, 0)) + sp.integrate(RightNumerator.rewrite(sp.exp), (X, 0, 1))) / Scale
			Expected = A**(-2) if(Index == Degree) else sp.Integer(0)
			check_zero(f'kernel_{Index}_moment_{Degree}', (Moment - Expected).rewrite(sp.exp))
	check_zero('denominator_positive_derivative_identity', sp.diff(Denominator, A) - A * sp.sinh(A))
	HomogeneousMatrix = sp.Matrix.hstack(endpoint_vector(sp.cosh(A * X)), endpoint_vector(sp.sinh(A * X)))
	check_zero('homogeneous_endpoint_determinant', HomogeneousMatrix.det() - 2 * A * sp.sinh(A) * Denominator)
	check_zero('even_q_trailing_coefficient', M / (M - 1) * (2 * M - 2) * (2 * M - 3) - 2 * M * (2 * M - 3))
	check_zero('odd_q_trailing_coefficient', M / (M - 1) * (2 * M - 1) * (2 * M - 2) - 2 * M * (2 * M - 1))
	for Index in (0, 1, 4, 5, 8, 13, 24, 25):
		P = make_p(Index)
		record_check(f'p_{Index}_boundary', endpoint_vector(P) == sp.zeros(2, 1))
	F = (2 + 3 * sp.I) + (1 - 2 * sp.I) * X + (3 - 5 * sp.I) * make_p(4) + sp.I * make_p(9) / 7
	G = (1 - sp.I) + (2 + sp.I) * X + (1 + 2 * sp.I) * make_p(6)
	KF = -sp.diff(F, X, 2) + C * F
	KG = -sp.diff(G, X, 2) + C * G
	DeltaF = F.subs(X, 1) - F.subs(X, -1)
	DeltaG = G.subs(X, 1) - G.subs(X, -1)
	Energy = polynomial_integral(KF * sp.conjugate(F))
	EnergyExpected = polynomial_integral(sp.diff(F, X) * sp.conjugate(sp.diff(F, X)) + C * F * sp.conjugate(F)) - DeltaF * sp.conjugate(DeltaF) / 2
	check_zero('complex_energy_identity', Energy - EnergyExpected)
	IsometryExpected = polynomial_integral(sp.diff(F, X, 2) * sp.conjugate(sp.diff(G, X, 2)) + 2 * C * sp.diff(F, X) * sp.conjugate(sp.diff(G, X)) + C**2 * F * sp.conjugate(G)) - C * DeltaF * sp.conjugate(DeltaG)
	check_zero('complex_left_definite_inner_product', polynomial_integral(KF * sp.conjugate(KG)) - IsometryExpected)
	Margin = sp.simplify(Energy - C * polynomial_integral(F * sp.conjugate(F)))
	record_check('complex_energy_nonnegative_sample', Margin.is_positive, str(Margin))
	for MinHalf in (2, 3, 5):
		L = 2 * MinHalf - 2
		CorrectionMatrix = sp.Matrix.hstack(endpoint_vector(X**L), endpoint_vector(X**(L + 1)))
		record_check(f'correction_matrix_L{L}', CorrectionMatrix == sp.Matrix([[L, L], [-L, L]]))
		for MaxDegree in range(L, L + 7):
			Monomials = [X**Degree for Degree in range(L, MaxDegree + 1)]
			BoundaryMatrix = sp.Matrix.hstack(*[endpoint_vector(Item) for Item in Monomials])
			Generators = [make_p(Index) for Index in range(L + 2, MaxDegree + 1)]
			TailMatrix = sp.zeros(len(Monomials), len(Generators))
			for(Column, Generator) in enumerate(Generators):
				for(Row, Degree) in enumerate(range(L, MaxDegree + 1)):
					TailMatrix[Row, Column] = sp.expand(Generator).coeff(X, Degree)
			Condition = BoundaryMatrix * TailMatrix == sp.zeros(2, len(Generators)) and TailMatrix.rank() == len(Monomials) - BoundaryMatrix.rank()
			record_check(f'finite_tail_nullspace_L{L}_degree{MaxDegree}', Condition)
	FirstValue = 2 + 3 * sp.I
	FirstDerivative = 1 - 2 * sp.I
	Alpha = 2 + sp.I
	Beta = -3 + 2 * sp.I
	CorrectPair = sp.conjugate(Alpha) * FirstValue + sp.conjugate(Beta) * FirstDerivative
	check_zero('first_linear_complex_pairing_value', CorrectPair - 8 * sp.I)
	WrongPair = Alpha * FirstValue + Beta * FirstDerivative
	record_check('unconjugated_coefficients_detectably_wrong', sp.simplify(CorrectPair - WrongPair) != 0)


def numeric_kernels(Parameter):
	Root = mp.sqrt(Parameter)
	Denominator = Root * mp.cosh(Root) - mp.sinh(Root)
	def kernel_zero(Value):
		return mp.cosh(Root * (1 - abs(Value))) / (2 * Root * mp.sinh(Root))
	def kernel_one(Value):
		return mp.sign(Value) * (Root * mp.cosh(Root * (1 - abs(Value))) - mp.sinh(Root * (1 - abs(Value)))) / (2 * Denominator)
	return kernel_zero, kernel_one


def integral(Function):
	return mp.quad(Function, [-1, 0, 1])


def check_close(Name, Observed, Expected, Tolerance=mp.mpf('1e-38')):
	Error = abs(Observed - Expected)
	record_check(Name, Error <= Tolerance * max(1, abs(Expected)), {'absolute_error': mp.nstr(Error, 8), 'expected': mp.nstr(Expected, 16)})


def numerical_checks():
	mp.mp.dps = 60
	Parameters = [('0.01', mp.mpf('0.01')), ('1', mp.mpf(1)), ('7', mp.mpf(7)), ('64', mp.mpf(64))]
	for(ParameterName, Parameter) in Parameters:
		G0, G1 = numeric_kernels(Parameter)
		for Index in (0, 1, 4, 5, 8, 13, 24, 25):
			P = make_p(Index)
			QFunction = sp.lambdify((X, C), -sp.diff(P, X, 2) + C * P, 'mpmath')
			for(KernelIndex, Kernel) in enumerate((G0, G1)):
				Observed = integral(lambda Value: QFunction(Value, Parameter) * Kernel(Value))
				Expected = 1 if(Index == KernelIndex) else 0
				check_close(f'green_pair_c{ParameterName}_p{Index}_g{KernelIndex}', Observed, Expected)
		Alpha = mp.mpc(2, 3)
		Beta = mp.mpc(-1, 1)
		def complex_g(Value):
			return Alpha * G0(Value) + Beta * G1(Value)
		Moments = [integral(lambda Value: complex_g(Value) * Value**Degree) for Degree in range(16)]
		check_close(f'complex_M0_c{ParameterName}', Moments[0], Alpha / Parameter)
		check_close(f'complex_M1_c{ParameterName}', Moments[1], Beta / Parameter)
		for Half in range(2, 8):
			EvenA = 2 * Half * (2 * Half - 1) + Parameter * Half / (Half - 1)
			EvenB = 2 * Half * (2 * Half - 3)
			OddA = 2 * Half * (2 * Half + 1) + Parameter * Half / (Half - 1)
			OddB = 2 * Half * (2 * Half - 1)
			check_close(f'even_recurrence_c{ParameterName}_m{Half}', Parameter * Moments[2 * Half] - EvenA * Moments[2 * Half - 2] + EvenB * Moments[2 * Half - 4], 0)
			check_close(f'odd_recurrence_c{ParameterName}_m{Half}', Parameter * Moments[2 * Half + 1] - OddA * Moments[2 * Half - 1] + OddB * Moments[2 * Half - 3], 0)
		for Value in (mp.mpf('-0.7'), mp.mpf('0.125'), mp.mpf('0.9')):
			Recovered = Parameter * Moments[0] * G0(Value) + Parameter * Moments[1] * G1(Value)
			check_close(f'complex_normalization_c{ParameterName}_x{Value}', Recovered, complex_g(Value))
		F = (2 + 3 * sp.I) + (1 - 2 * sp.I) * X + (3 - 5 * sp.I) * make_p(4) + sp.I * make_p(9) / 7
		KF = sp.lambdify((X, C), -sp.diff(F, X, 2) + C * F, 'mpmath')
		Probe = lambda Value: mp.mpc(2, 1) * G0(Value) + mp.mpc(-3, 2) * G1(Value)
		Pair = integral(lambda Value: KF(Value, Parameter) * mp.conj(Probe(Value)))
		check_close(f'complex_green_conjugation_c{ParameterName}', Pair, mp.mpc(0, 8))


def power_integral(Expression, Lower, Upper):
	Value = sp.Integer(0)
	for Term in sp.Add.make_args(sp.expand(Expression)):
		Coefficient, Power = Term.as_coeff_exponent(X)
		if(Coefficient.has(X)):
			raise RuntimeError('not a power sum')
		Value += Coefficient * (Upper**(Power + 1) - Lower**(Power + 1)) / (Power + 1)
	return sp.simplify(Value)


def cutoff_checks():
	# On x > 0; the actual test function is |x|^(7/4) (1-x^2)^2.
	# Its second derivative is unbounded near 0 but is square integrable.
	F = X**sp.Rational(7, 4) * (1 - X**2)**2
	PreviousNorm = None
	Rows = []
	for Denominator in (8, 16, 32, 64):
		Delta = sp.Rational(1, Denominator)
		Transition = X / Delta - 1
		Eta = 10 * Transition**3 - 15 * Transition**4 + 6 * Transition**5
		# This explicit C^2 cutoff satisfies the same estimates as the smooth proof cutoff.
		LocalSecondSquared = 2 * power_integral(sp.diff(F, X, 2)**2, 0, 2 * Delta)
		ErrorsSquared = []
		for Order in range(3):
			Central = 2 * power_integral(sp.diff(F, X, Order)**2, 0, Delta)
			TransitionError = 2 * power_integral(sp.diff((Eta - 1) * F, X, Order)**2, Delta, 2 * Delta)
			ErrorsSquared.append(sp.simplify(Central + TransitionError))
		ESquared = sp.N(LocalSecondSquared, 60)
		Bounds = [(2 / sp.sqrt(3))**2 * Delta**4 * ESquared,
			(sp.sqrt(2) + 4 / sp.sqrt(3))**2 * Delta**2 * ESquared,
			(1 + 4 * sp.sqrt(2) + 12 / sp.sqrt(3))**2 * ESquared]
		for Order in range(3):
			record_check(f'cutoff_local_bound_delta1over{Denominator}_order{Order}', 0 <= sp.N(ErrorsSquared[Order], 50) <= sp.N(Bounds[Order], 50))
		Norm = float(sp.sqrt(sum(ErrorsSquared)).evalf(40))
		if(PreviousNorm is not None):
			record_check(f'cutoff_error_decreases_delta1over{Denominator}', Norm < PreviousNorm)
		PreviousNorm = Norm
		Rows.append({'delta': str(Delta), 'H2_error': Norm, 'local_second_derivative_norm': float(sp.sqrt(LocalSecondSquared).evalf(40))})
	return Rows


def negative_control(Choice):
	if(Choice == 'g1_sign'):
		mp.mp.dps = 50
		_, G1 = numeric_kernels(mp.mpf(1))
		check_close('negative_control_flipped_g1_first_moment', integral(lambda Value: -Value * G1(Value)), 1)
	if(Choice == 'odd_half'):
		record_check('negative_control_old_odd_half_factor', sp.Rational(2, 3) == sp.Rational(1, 2) * sp.Rational(2, 3))
	if(Choice == 'conjugation'):
		Wrong = (2 + sp.I) * (2 + 3 * sp.I) + (-3 + 2 * sp.I) * (1 - 2 * sp.I)
		check_zero('negative_control_missing_conjugation', Wrong - 8 * sp.I)


def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument('--negative-control', choices=('g1_sign', 'odd_half', 'conjugation'))
	Args = Parser.parse_args()
	if(Args.negative_control):
		negative_control(Args.negative_control)
		raise RuntimeError('negative control unexpectedly passed')
	symbolic_checks()
	numerical_checks()
	CutoffRows = cutoff_checks()
	Output = {'role': 'author-side checks, not independent review', 'python': platform.python_version(),
		'sympy': sp.__version__, 'mpmath': mp.__version__, 'mpmath_dps': mp.mp.dps,
		'check_count': len(Results), 'all_passed': all(Item['pass'] for Item in Results),
		'scope': 'Symbolic identities and specified finite probes only. No all-index or Lean certification.',
		'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		'cutoff_samples': CutoffRows, 'checks': Results}
	Destination = Path(__file__).with_name('author_checks.json')
	Destination.write_text(json.dumps(Output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
	print(json.dumps({'all_passed': Output['all_passed'], 'check_count': len(Results), 'result': str(Destination), 'cutoff_samples': CutoffRows}, indent=2))


if(__name__ == '__main__'):
	main()
