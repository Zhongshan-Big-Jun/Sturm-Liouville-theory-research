# -*- coding: utf-8 -*-
"""Exact checks for the two specified third-order recurrences, c > 0.

Finite checks and a numerical finite backward solution are not proofs of an
infinite-index limit. Analytic proofs are in SL_third_order_recurrence_theory.tex.
Run as a script to check all sections; any failed check exits nonzero.
"""
from fractions import Fraction as F
import math

import mpmath as mp
import sympy as sp

Shift = sp.symbols("c", positive=True)
Beta = sp.symbols("beta")


def parity_value(Parity):
	if Parity not in ("e", "o"):
		raise ValueError("parity must be 'e' or 'o'")
	return int(Parity == "o")


def positive_shift(Value):
	Result = F(Value)
	if Result <= 0:
		raise ValueError("c must be positive")
	return Result


def integer_at_least(Value, Minimum, Name):
	if isinstance(Value, bool) or not isinstance(Value, int) or Value < Minimum:
		raise ValueError(f"{Name} must be an integer >= {Minimum}")


def exact_scalar(Value):
	"""Keep SymPy expressions; rationalize ordinary numeric inputs before division.

	Python floats denote their represented binary rationals, not an intended
	decimal value. SymPy expressions retain their supplied symbolic semantics.
	"""
	return Value if isinstance(Value, sp.Basic) else F(Value)


def coefficients(Parity, Index, C):
	"""P,Q,R; symbolic inputs are supported without asserting inequalities."""
	Epsilon = parity_value(Parity)
	Index, C = exact_scalar(Index), exact_scalar(C)
	P = 4 * C * Index * (2 * Index + 2 * Epsilon - 1) + C * C * Index / (Index - 1)
	Q = 4 * Index * (Index - 1) * (2 * Index + 2 * Epsilon - 1) * (2 * Index + 2 * Epsilon - 3) + 4 * C * Index * (2 * Index + 2 * Epsilon - 3)
	R = 4 * Index * (Index - 2) * (2 * Index + 2 * Epsilon - 3) * (2 * Index + 2 * Epsilon - 5)
	return P, Q, R


def even_coeffs(Index, C):
	return coefficients("e", Index, C)


def odd_coeffs(Index, C):
	return coefficients("o", Index, C)


def closed_form(Parity, Plus, Index, C):
	Epsilon = parity_value(Parity)
	integer_at_least(Index, 0, "index")
	C = positive_shift(C)
	Offset = (1 if Plus else 0) if Epsilon == 0 else (3 if Plus else 1)
	Divisor = 6 * (Index + 1) if Epsilon == 1 and Plus else 1
	return F(math.factorial(2 * Index + Offset)) / (Divisor * C ** Index)


def even_form1(Index, C):
	return closed_form("e", True, Index, C)


def even_form2(Index, C):
	return closed_form("e", False, Index, C)


def odd_form1(Index, C):
	return closed_form("o", True, Index, C)


def odd_form2(Index, C):
	return closed_form("o", False, Index, C)


def check_mu_form(Parity, Form, C, N=40):
	parity_value(Parity)
	C = positive_shift(C)
	integer_at_least(N, 3, "N")
	for Index in range(3, N + 1):
		P, Q, R = coefficients(Parity, Index, C)
		Residual = C * C * Form(Index, C) - P * Form(Index - 1, C) + Q * Form(Index - 2, C) - R * Form(Index - 3, C)
		if Residual != 0:
			return False, Index
	return True, None


def z_residual_poly(Parity, Index):
	Index = sp.sympify(Index)
	P, Q, R = coefficients(Parity, Index, Shift)
	A1 = P / (4 * Shift * Index ** 2)
	A2 = -Q / (16 * Index ** 2 * (Index - 1) ** 2)
	A3 = Shift * R / (64 * Index ** 2 * (Index - 1) ** 2 * (Index - 2) ** 2)
	Ratio = lambda J: 1 + Beta / (2 * J)
	return sp.factor(sp.together(A1 + A2 / Ratio(Index - 1) + A3 / (Ratio(Index - 1) * Ratio(Index - 2)) - Ratio(Index)))


def reduction_coefficients(A2, A3, E0, E2, E3):
	"""E0=E_j, E2=E_(j-2), E3=E_(j-3).

	Reject known zero baselines. An undecidable symbolic E0 requires the
	caller to establish E0 != 0; no symbolic inequality is inferred here.
	"""
	A2, A3, E0, E2, E3 = map(exact_scalar, (A2, A3, E0, E2, E3))
	if E0 == 0 or (isinstance(E0, sp.Basic) and E0.is_zero is True):
		raise ValueError("the baseline solution must be nonzero at this index")
	return -(A2 * E2 + A3 * E3) / E0, -A3 * E3 / E0


def check_s_recurrence(Parity, C, N=80):
	Epsilon = parity_value(Parity)
	C = positive_shift(C)
	integer_at_least(N, 3, "N")
	E = [F(1)] * (N + 1)
	for Index in range(1, N + 1):
		E[Index] = E[Index - 1] * (1 + F(2 * Epsilon + 1, 2 * Index))
	Z = [F(1), F(2), F(3)] + [F(0)] * (N - 2)
	Coefficients = {}
	for Index in range(3, N + 1):
		P, Q, R = coefficients(Parity, Index, C)
		A1 = P / (4 * C * Index ** 2)
		A2 = -F(Q) / (16 * Index ** 2 * (Index - 1) ** 2)
		A3 = C * R / (64 * Index ** 2 * (Index - 1) ** 2 * (Index - 2) ** 2)
		Coefficients[Index] = (A2, A3)
		Z[Index] = A1 * Z[Index - 1] + A2 * Z[Index - 2] + A3 * Z[Index - 3]
	Ratios = [Z[Index] / E[Index] for Index in range(N + 1)]
	Differences = [F(0)] + [Ratios[Index] - Ratios[Index - 1] for Index in range(1, N + 1)]
	for Index in range(3, N + 1):
		A2, A3 = Coefficients[Index]
		A, B = reduction_coefficients(A2, A3, E[Index], E[Index - 2], E[Index - 3])
		if Differences[Index] != A * Differences[Index - 1] + B * Differences[Index - 2]:
			return False
	return True


def minimal_solution(Parity, C, N=2000, K=12, Precision=80):
	"""Numerical FINITE backward solution, normalized at zero; indices 0..N.

	Terminal z_(N+1)=z_(N+2)=0 with nonzero z_N. Positive second
	differences avoid catastrophic subtractive backward steps. mpmath's
	arbitrary exponent avoids binary64 overflow/underflow. K is retained as
	the legacy unused argument; it does not truncate the returned list.
	No interval certificate or infinite-terminal convergence is asserted.
	"""
	Epsilon = parity_value(Parity)
	C = positive_shift(C)
	integer_at_least(N, 0, "N")
	integer_at_least(Precision, 20, "Precision")
	with mp.workdps(Precision):
		CReal = mp.mpf(C.numerator) / C.denominator
		V = [mp.mpf(0)] * (N + 1)
		Weight, Slope, Value = mp.mpf(1), mp.mpf(0), mp.mpf(0)
		for Index in range(N + 2, 1, -1):
			Slope += Weight
			Value += Slope
			V[Index - 2] = Value
			if Index > 2:
				Weight *= 2 * (Index - 1) * (2 * Index + 2 * Epsilon - 1) / CReal
		H = mp.mpf(1)
		Result = []
		for Index in range(N + 1):
			if Index:
				H *= 1 + mp.mpf(2 * Epsilon - 1) / (2 * Index)
			Result.append(H * (V[Index] / V[0]))
		if not all(mp.isfinite(Value) and Value > 0 for Value in Result):
			raise ArithmeticError("nonfinite or nonpositive finite backward solution")
		return Result


def require(Condition, Message):
	if not Condition:
		raise ArithmeticError(Message)


def main():
	print("(A) exact rational closed forms; every reported check must pass")
	Forms = [("e", even_form1), ("e", even_form2), ("o", odd_form1), ("o", odd_form2)]
	for C in (F(1, 4), F(1), F(3), F(5), F(10)):
		for Parity, Form in Forms:
			Passed, FirstFailure = check_mu_form(Parity, Form, C)
			require(Passed, f"closed form {Form.__name__}, c={C}, failed at j={FirstFailure}")
		print(f"  c={C}: all four forms PASS, j=3..40")
	print("(B) symbolic ratio identities and necessary coefficient conditions")
	Index = sp.symbols("j")
	for Parity, Expected in (("e", {-1, 1}), ("o", {1, 3})):
		Equations = [z_residual_poly(Parity, J).as_numer_denom()[0] for J in (3, 4, 5)]
		Solutions = sp.solve(Equations, Beta, dict=True)
		require({Row[Beta] for Row in Solutions} == Expected, f"unexpected beta candidates: {Solutions}")
		for Value in Expected:
			require(sp.simplify(z_residual_poly(Parity, Index).subs(Beta, Value)) == 0, "symbolic all-index ratio identity failed")
		print(f"  parity={Parity}: candidates {sorted(Expected)}, general identities PASS")
	print("(C) exact reduction, positive baseline Eplus; arbitrary initial data 1,2,3")
	for Parity in ("e", "o"):
		for C in (F(1, 4), F(1), F(3), F(10)):
			require(check_s_recurrence(Parity, C, 119), f"reduction failed: parity={Parity}, c={C}")
		print(f"  parity={Parity}: j=3..119 PASS for four rational shifts")
	print("(D) finite backward numerical diagnostics; not an infinite-index certificate")
	for Parity in ("e", "o"):
		Values = minimal_solution(Parity, 3)
		with mp.workdps(60):
			Ratios = [Values[J + 1] / Values[J] for J in (10, 100, 1000)]
			require(all(mp.isfinite(Value) and Value > 0 for Value in Ratios), "invalid finite ratio")
			print(f"  parity={Parity}, N=2000: h0={mp.nstr(Values[0], 8)}, h1={mp.nstr(Values[1], 12)}")
			print("  ratios at j=10,100,1000:", [mp.nstr(Value, 12) for Value in Ratios])
	print("All requested finite/symbolic checks completed successfully.")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
