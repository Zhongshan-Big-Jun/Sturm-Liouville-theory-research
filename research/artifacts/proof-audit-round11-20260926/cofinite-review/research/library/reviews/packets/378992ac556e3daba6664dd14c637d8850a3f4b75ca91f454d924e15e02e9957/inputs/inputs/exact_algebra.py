#!/usr/bin/env python3
"""Exact author self-checks. These do not certify the infinite-dimensional proof."""
import json
import platform
from collections import Counter
import sympy as sp

x = sp.Symbol("x")
L = sp.Symbol("L", integer=True, positive=True)
m = sp.Symbol("m", integer=True, positive=True)
Records = []


def check_zero(Name, Expression, Category, Scope):
	Reduced = sp.simplify(Expression)
	Passed = Reduced == 0
	Records.append({"name": Name, "category": Category, "scope": Scope,
		"passed": bool(Passed), "residual": str(Reduced)})
	if not Passed:
		raise RuntimeError(f"{Name}: nonzero residual {Reduced}")


def check_true(Name, Condition, Category, Scope, Evidence):
	Passed = bool(Condition)
	Records.append({"name": Name, "category": Category, "scope": Scope,
		"passed": Passed, "evidence": Evidence})
	if not Passed:
		raise RuntimeError(f"{Name}: condition failed")


def boundary(Polynomial):
	Derivative = sp.diff(Polynomial, x)
	Delta = Polynomial.subs(x, 1) - Polynomial.subs(x, -1)
	return sp.Matrix([sp.expand(Derivative.subs(x, 1) - Delta / 2),
		sp.expand(Derivative.subs(x, -1) - Delta / 2)])


def four_boundary(Polynomial):
	return boundary(Polynomial).col_join(boundary(sp.diff(Polynomial, x, 2)))


def member(Index):
	if Index == 0:
		return sp.Integer(1)
	if Index == 1:
		return x
	if Index < 4:
		raise ValueError("Index outside original family")
	HalfIndex = Index // 2
	return x**Index - sp.Rational(HalfIndex, HalfIndex - 1) * x**(Index - 2)


def tail_decompose(Polynomial, VanishingOrder):
	Remainder = sp.Poly(Polynomial, x)
	Coefficients = {}
	while not Remainder.is_zero and Remainder.degree() >= VanishingOrder + 2:
		Index = Remainder.degree()
		Coefficient = Remainder.LC()
		Coefficients[Index] = Coefficients.get(Index, 0) + Coefficient
		Remainder = sp.Poly(Remainder.as_expr() - Coefficient * member(Index), x)
	Reconstructed = sum(Coefficient * member(Index)
		for Index, Coefficient in Coefficients.items())
	return Remainder.as_expr(), sp.expand(Reconstructed), Coefficients


def main():
	EvenMatrix = sp.Matrix([[L, L + 2],
		[L * (L - 1) * (L - 2), L * (L + 1) * (L + 2)]])
	OddMatrix = sp.Matrix([[L, L + 2],
		[L * (L + 1) * (L - 2), L * (L + 2) * (L + 3)]])
	A = L * (L - 1) * (L - 2)
	B = L * (L + 1) * (L - 2)
	C = L * (L + 1) * (L + 2)
	D = L * (L + 2) * (L + 3)
	FullMatrix = sp.Matrix([[L, L, L + 2, L + 2],
		[-L, L, -L - 2, L + 2], [A, B, C, D], [-A, B, -C, D]])
	check_zero("even determinant", EvenMatrix.det() - 2 * L * (L + 2) * (2 * L - 1),
		"symbolic_identity", "Polynomial identity in L; invertibility used for even L>=4")
	check_zero("odd determinant", OddMatrix.det() - 2 * L * (L + 2) * (2 * L + 1),
		"symbolic_identity", "Polynomial identity in L; invertibility used for even L>=4")
	check_zero("four-residual determinant", FullMatrix.det() - 4 * EvenMatrix.det() * OddMatrix.det(),
		"symbolic_identity", "All formal L; ordering (+,-,+,-), columns L through L+3")
	check_zero("tail remainder determinant",
		sp.Matrix([[L, L], [-L, L]]).det() - 2 * L**2,
		"symbolic_identity", "All L; nonzero for the requested L>=4")
	ParityRows = sp.Matrix([[sp.Rational(1, 2), -sp.Rational(1, 2), 0, 0],
		[0, 0, sp.Rational(1, 2), -sp.Rational(1, 2)],
		[sp.Rational(1, 2), sp.Rational(1, 2), 0, 0],
		[0, 0, sp.Rational(1, 2), sp.Rational(1, 2)]])
	BlockResidual = ParityRows * FullMatrix[:, [0, 2, 1, 3]] - sp.diag(EvenMatrix, OddMatrix)
	for Row in range(4):
		for Column in range(4):
			check_zero(f"parity block {Row},{Column}", BlockResidual[Row, Column],
				"symbolic_identity", "All formal L; change of the four actual residual coordinates")
	InverseResidual = FullMatrix * FullMatrix.inv() - sp.eye(4)
	for Row in range(4):
		for Column in range(4):
			check_zero(f"right inverse {Row},{Column}", InverseResidual[Row, Column],
				"symbolic_identity", "Rational identity away from determinant zeros, in particular even L>=4")

	EvenFirst = 2 * m - m / (m - 1) * (2 * m - 2)
	OddFirst = (2 * m + 1 - 1) - m / (m - 1) * (2 * m - 1 - 1)
	EvenSecond = ((2 * m) * (2 * m - 1) * (2 * m - 2)
		- m / (m - 1) * (2 * m - 2) * (2 * m - 3) * (2 * m - 4))
	OddSecond = ((2 * m + 1) * (2 * m) * (2 * m - 2)
		- m / (m - 1) * (2 * m - 1) * (2 * m - 2) * (2 * m - 4))
	check_zero("all even first boundary", EvenFirst, "symbolic_identity", "Every integer m>=2")
	check_zero("all odd first boundary", OddFirst, "symbolic_identity", "Every integer m>=2")
	check_zero("all even second boundary", EvenSecond - 4 * m * (4 * m - 5),
		"symbolic_identity", "Every integer m>=2, includes m=2 zero derivative factors")
	check_zero("all odd second boundary", OddSecond - 4 * m * (4 * m - 3),
		"symbolic_identity", "Every integer m>=2, includes m=2 zero derivative factors")

	for VanishingOrder in [4, 6, 8, 10]:
		Directions = sp.Matrix([[x**(VanishingOrder + Shift) for Shift in range(4)]])
		ActualMatrix = sp.Matrix.hstack(*[four_boundary(Polynomial) for Polynomial in Directions])
		ExpectedMatrix = FullMatrix.subs(L, VanishingOrder)
		check_true(f"actual derivatives L={VanishingOrder}", ActualMatrix == ExpectedMatrix,
			"finite_exact_sample", "Direct differentiation at four even L values", str(ActualMatrix))
		InputPolynomial = x**VanishingOrder * sum(
			(sp.Rational(Shift + 2, Shift + 1) + sp.I * sp.Rational(Shift - 1, Shift + 3)) * x**Shift
			for Shift in range(10))
		Correction = (Directions * ActualMatrix.inv() * four_boundary(InputPolynomial))[0]
		Corrected = sp.expand(InputPolynomial - Correction)
		check_true(f"four-residual correction L={VanishingOrder}",
			four_boundary(Corrected) == sp.zeros(4, 1),
			"finite_exact_sample", "Exact complex rational coefficients", str(four_boundary(Corrected)))
		check_zero(f"high divisibility L={VanishingOrder}",
			sp.rem(Corrected, x**VanishingOrder, x),
			"finite_exact_sample", "Corrected polynomial retains divisibility by x^L")
		Remainder, Reconstruction, Coefficients = tail_decompose(Corrected, VanishingOrder)
		check_zero(f"tail remainder L={VanishingOrder}", Remainder,
			"finite_exact_sample", "Finite reconstruction checks the all-degree argument, not its quantifier")
		check_zero(f"tail reconstruction L={VanishingOrder}", Reconstruction - Corrected,
			"finite_exact_sample", "Exact polynomial equality")
		check_true(f"tail indices L={VanishingOrder}",
			all(Index >= VanishingOrder + 2 for Index in Coefficients),
			"finite_exact_sample", "Every used generator lies in the requested complete tail",
			sorted(Coefficients))

	ExpectedTraces = {0: [1, 0, 0, 0], 1: [0, 1, 0, 0],
		4: [0, 0, -4, 0], 5: [0, 0, 0, -12]}
	for Index in [0, 1] + list(range(4, 22)):
		ActualTraces = [sp.diff(member(Index), x, Order).subs(x, 0) for Order in range(4)]
		check_true(f"centre traces n={Index}",
			ActualTraces == ExpectedTraces.get(Index, [0, 0, 0, 0]),
			"finite_exact_sample", "Low trace table; n>=6 general proof is minimum monomial degree",
			[str(Value) for Value in ActualTraces])

	t, w = sp.symbols("t w", positive=True)
	ZReal, ZImag, BReal, BImag = sp.symbols("ZReal ZImag BReal BImag", real=True)
	Objective = (ZReal - BReal)**2 + (ZImag - BImag)**2 + t**2 * w * (BReal**2 + BImag**2)
	Minimizer = {BReal: ZReal / (1 + t**2 * w), BImag: ZImag / (1 + t**2 * w)}
	check_zero("quadratic K real stationary point",
		sp.diff(Objective, BReal).subs(Minimizer), "symbolic_identity",
		"One complex coordinate; analytic infinite-sum passage is in manuscript section 4.1")
	check_zero("quadratic K imaginary stationary point",
		sp.diff(Objective, BImag).subs(Minimizer), "symbolic_identity",
		"One complex coordinate")
	check_zero("quadratic K minimal value",
		Objective.subs(Minimizer) - t**2 * w / (1 + t**2 * w) * (ZReal**2 + ZImag**2),
		"symbolic_identity", "One complex coordinate with t,w>0")
	for Order in range(4):
		CriticalOrder = sp.Rational(2 * Order + 1, 2)
		check_zero(f"harmonic Fourier exponent r={Order}",
			2 * CriticalOrder - 2 * Order - 2 + 1,
			"finite_exact_sample", "Exact exponent check only; bounded sequence and divergence proved analytically")

	check_true("reject p4 as Hc4 member", four_boundary(member(4)) != sp.zeros(4, 1),
		"expected_rejection", "Negative control: one must not norm p4 in Hc4", str(four_boundary(member(4))))
	IncompleteCorrection = x**8 - 2 * x**4
	check_true("reject first-boundary-only repair",
		boundary(IncompleteCorrection) == sp.zeros(2, 1)
		and boundary(sp.diff(IncompleteCorrection, x, 2)) != sp.zeros(2, 1),
		"expected_rejection", "Two endpoint corrections do not generally enforce the square domain",
		str(four_boundary(IncompleteCorrection)))
	CompatibleCombination = sp.expand(member(6) - sp.Rational(7, 2) * member(4))
	check_true("compatible combination is not high-vanishing core member",
		four_boundary(CompatibleCombination) == sp.zeros(4, 1)
		and sp.diff(CompatibleCombination, x, 2).subs(x, 0) == 14,
		"expected_rejection", "Ordinary H4 polynomial core is not W4; high centre vanishing is necessary",
		str(CompatibleCombination))
	Counts = Counter(Record["category"] for Record in Records)
	print(json.dumps({
		"status": "AUTHOR_EXACT_SELF_CHECK_PASSED",
		"independent_review": False,
		"infinite_dimensional_proof_certified_by_this_script": False,
		"python": platform.python_version(), "sympy": sp.__version__,
		"total_checks": len(Records), "category_counts": dict(Counts),
		"checks": Records,
		"limitations": ["No numerical sampling is used as a density proof.",
			"No Lean formalization or independent acceptance is performed.",
			"Symbolic identities and finite exact examples are labelled separately."],
	}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
	main()
