#!/usr/bin/env python3
"""Exact rational author certificate. Mathematical contract: README.md.

Normal proof arithmetic has no float, libm, mpmath, SymPy or oracle input.
Decimal is used only to display already established rational bounds.
"""
import argparse
import json
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from pathlib import Path


def require(condition, message):
	if not condition:
		raise ArithmeticError(message)


def rational(value):
	if type(value) is int:
		return Fraction(value)
	if isinstance(value, Fraction):
		return value
	else:
		raise TypeError("Only exact int or Fraction inputs are accepted")


@dataclass(frozen=True)
class Interval:
	lo: Fraction
	hi: Fraction

	def __post_init__(self):
		object.__setattr__(self, "lo", rational(self.lo))
		object.__setattr__(self, "hi", rational(self.hi))
		require(self.lo <= self.hi, "Reversed interval")

	@staticmethod
	def point(value):
		return Interval(rational(value), rational(value))

	@staticmethod
	def of(value):
		return value if isinstance(value, Interval) else Interval.point(value)

	def __add__(self, other):
		other = Interval.of(other)
		return Interval(self.lo + other.lo, self.hi + other.hi)

	__radd__ = __add__

	def __neg__(self):
		return Interval(-self.hi, -self.lo)

	def __sub__(self, other):
		return self + (-Interval.of(other))

	def __rsub__(self, other):
		return Interval.of(other) - self

	def __mul__(self, other):
		other = Interval.of(other)
		products = [x * y for x in (self.lo, self.hi) for y in (other.lo, other.hi)]
		return Interval(min(products), max(products))

	__rmul__ = __mul__

	def __truediv__(self, other):
		other = Interval.of(other)
		require(not other.lo <= 0 <= other.hi, "Divisor interval contains zero")
		return self * Interval(1 / other.hi, 1 / other.lo)

	def __rtruediv__(self, other):
		return Interval.of(other) / self

	def __pow__(self, exponent):
		require(type(exponent) is int, "Interval power must be an integer")
		if exponent < 0:
			return 1 / (self ** (-exponent))
		if exponent == 0:
			return Interval.point(1)
		if exponent % 2:
			return Interval(self.lo ** exponent, self.hi ** exponent)
		lower = Fraction(0) if self.lo <= 0 <= self.hi else min(self.lo ** exponent, self.hi ** exponent)
		return Interval(lower, max(self.lo ** exponent, self.hi ** exponent))


def outward_grid(box, digits=90):
	"""Exact floor/ceiling on a rational decimal grid, not decimal arithmetic."""
	require(type(digits) is int and 0 <= digits <= 200, "Invalid rational grid precision")
	scale = 10 ** digits
	LowerNumerator = box.lo.numerator * scale // box.lo.denominator
	UpperNumerator = -((-box.hi.numerator * scale) // box.hi.denominator)
	return Interval(Fraction(LowerNumerator, scale), Fraction(UpperNumerator, scale))


def atan_small(x, count):
	x = rational(x)
	require(0 < x < 1, "Arctan series requires 0 < x < 1")
	require(type(count) is int and count >= 1, "Arctan term count must be positive")
	partial = sum(((-1) ** k * x ** (2 * k + 1) / (2 * k + 1) for k in range(count)), Fraction(0))
	adjacent = partial + (-1) ** count * x ** (2 * count + 1) / (2 * count + 1)
	return Interval(min(partial, adjacent), max(partial, adjacent))


def machin_pi():
	return outward_grid(16 * atan_small(Fraction(1, 5), 85) - 4 * atan_small(Fraction(1, 239), 28))


def trig_point(x, degree=110):
	"""Degree-N Maclaurin polynomials +/- |x|^(N+1)/(N+1)!.

	All sine and cosine derivatives have absolute value <= 1 on the real
	axis. This Lagrange remainder works for either parity and any real x.
	"""
	x = rational(x)
	require(type(degree) is int and degree >= 1, "Taylor degree must be a positive integer")
	s, c, term = Fraction(0), Fraction(1), Fraction(1)
	for k in range(1, degree + 1):
		term = term * x / k
		if k % 4 == 1:
			s += term
		elif k % 4 == 3:
			s -= term
		elif k % 4 == 2:
			c -= term
		else:
			c += term
	remainder = abs(term * x) / (degree + 1)
	return outward_grid(Interval(s - remainder, s + remainder)), outward_grid(Interval(c - remainder, c + remainder))


def phase_domain(a, PiBox):
	a = rational(a)
	require(PiBox.hi / 2 < a < PiBox.lo, "Phase must be certified inside (pi/2, pi)")


def g_point(a, PiBox):
	a = rational(a)
	phase_domain(a, PiBox)
	s, _ = trig_point(a, 110)
	DoubleSin, _ = trig_point(2 * a, 130)
	return 8 * a ** 3 * s ** 2 - PiBox ** 2 * (2 * a - DoubleSin)


def u_point(a, PiBox):
	a = rational(a)
	phase_domain(a, PiBox)
	s, c = trig_point(a, 110)
	require(s.lo > 0 and c.hi < 0, "Phase trigonometric signs not certified")
	return a / (2 * (a - s / c))


def f_point(a, u, PiBox):
	a, u = rational(a), rational(u)
	phase_domain(a, PiBox)
	require(0 < u < Fraction(1, 2), "Root parameter must lie in (0, 1/2)")
	s, c = trig_point(a, 110)
	return s / c + a * (1 / (2 * u) - 1)


def increasing_image(LowerValueBox, UpperValueBox):
	"""Conditional on monotonicity, use lower(L) and upper(H), never lower(H)."""
	require(LowerValueBox.lo <= UpperValueBox.hi, "Inconsistent increasing endpoint images")
	return Interval(LowerValueBox.lo, UpperValueBox.hi)


def check_root_bracket(u, bracket, PiBox):
	require(bracket.lo < bracket.hi, "Root bracket needs distinct ordered endpoints")
	LeftValue = f_point(bracket.lo, u, PiBox)
	RightValue = f_point(bracket.hi, u, PiBox)
	require(LeftValue.hi < 0, "Root lower endpoint must have strictly negative F")
	require(RightValue.lo > 0, "Root upper endpoint must have strictly positive F")
	return LeftValue, RightValue


def monotone_root_image(LowerU, UpperU, LowerRootBracket, UpperRootBracket, PiBox):
	"""F_a > 0 and F_u < 0 imply a(u) increases; README proves this globally."""
	LowerU, UpperU = rational(LowerU), rational(UpperU)
	require(0 < LowerU <= UpperU < Fraction(1, 2), "Invalid parameter interval")
	check_root_bracket(LowerU, LowerRootBracket, PiBox)
	check_root_bracket(UpperU, UpperRootBracket, PiBox)
	return increasing_image(LowerRootBracket, UpperRootBracket)


def check_g_bracket(bracket, PiBox):
	require(bracket.lo < bracket.hi, "G bracket needs distinct ordered endpoints")
	LeftValue = g_point(bracket.lo, PiBox)
	RightValue = g_point(bracket.hi, PiBox)
	require(LeftValue.lo > 0, "G lower endpoint must have strictly positive G")
	require(RightValue.hi < 0, "G upper endpoint must have strictly negative G")
	return LeftValue, RightValue


def check_sqrt_two(box):
	require(0 < box.lo < box.hi and box.lo ** 2 < 2 < box.hi ** 2, "Invalid sqrt(2) enclosure")


def require_encloses(outer, inner, label):
	require(outer.lo <= inner.lo and inner.hi <= outer.hi, label + ": proposed enclosure does not contain certified enclosure")


RootBracket = Interval(Fraction("2.27651323902643307501655540074525185589672"), Fraction("2.27651323902643307501655540074525185589673"))
OldRootBracket = Interval(
	Fraction(57422840420798164132636532169819408433127719830251, 23384026197294446691258957323460528314494920687616),
	Fraction(14355710105199541033159133042454852108282351614991, 5846006549323611672814739330865132078623730171904),
)
LegacyCotX = Fraction(4889224211780879, 1152921504606846976)
LegacyCotBox = Interval(Fraction(1037091322688373, 4398046511104), Fraction(4148365290753493, 17592186044416))
BinaryPi = Fraction(884279719003555, 281474976710656)


def certificate_checks():
	rows = []

	def record(condition, name, **evidence):
		require(condition, name)
		rows.append({"name": name, "exact_comparison_passed": True, "evidence": evidence})

	PiBox = machin_pi()
	record(4 * (Fraction(1, 5) - Fraction(1, 5) ** 3 / 3) > Fraction(1, 239), "Machin angle positive rational bound")
	DoubleTan = 2 * Fraction(1, 5) / (1 - Fraction(1, 5) ** 2)
	QuadrupleTan = 2 * DoubleTan / (1 - DoubleTan ** 2)
	MachinTan = (QuadrupleTan - Fraction(1, 239)) / (1 + QuadrupleTan / 239)
	record(DoubleTan == Fraction(5, 12) and QuadrupleTan == Fraction(120, 119) and MachinTan == 1,
		"Machin tangent identity", pi=PiBox)
	record(3 < PiBox.lo < PiBox.hi < Fraction(22, 7) and PiBox.hi ** 2 < 12,
		"Pi location and T2 h(pi/2)>0", pi=PiBox)

	LeftG, RightG = check_g_bracket(RootBracket, PiBox)
	record(True, "T3 strict G root signs", a=RootBracket, g_left=LeftG, g_right=RightG)
	LeftU, RightU = u_point(RootBracket.lo, PiBox), u_point(RootBracket.hi, PiBox)
	UBox = increasing_image(LeftU, RightU)
	DBox = (RootBracket ** 2 - PiBox ** 2 / 4) / UBox ** 2
	TargetU = Interval(Fraction("0.32992250812006654958"), Fraction("0.32992250812006654960"))
	TargetD = Interval(Fraction("24.9438661384324768968"), Fraction("24.9438661384324769084"))
	record(TargetU.lo < UBox.lo and UBox.hi < TargetU.hi, "T3 monotone u image is strictly inside public interval", u=UBox, u_at_lower=LeftU, u_at_upper=RightU, target=TargetU)
	record(TargetD.lo < DBox.lo and DBox.hi < TargetD.hi, "T3 value is strictly inside public interval", value=DBox, target=TargetD)
	MarginPi = 3 * PiBox ** 2 - DBox
	Margin25 = 25 - DBox
	record(MarginPi.lo > Fraction("4.664947") and Margin25.lo > Fraction("0.0561"), "T3 strict comparison margins", margin_three_pi_squared=MarginPi, margin_25=Margin25)

	LeftRootBracket = Interval(Fraction(2), Fraction(12, 5))
	RootImage = monotone_root_image(Fraction(1, 3), Fraction(3, 8), LeftRootBracket, OldRootBracket, PiBox)
	OldLeftF, OldRightF = check_root_bracket(Fraction(3, 8), OldRootBracket, PiBox)
	record(OldLeftF.hi < 0 < OldRightF.lo, "Old lower(H) is strictly below a(H), true upper(H) works",
		h=Fraction(3, 8), bracket=OldRootBracket, f_at_lower=OldLeftF, f_at_upper=OldRightF)
	record(RootImage.lo == LeftRootBracket.lo and RootImage.hi == OldRootBracket.hi,
		"General root monotone image uses lower(L), upper(H)", parameter=Interval(Fraction(1, 3), Fraction(3, 8)), image=RootImage)

	CotSin, CotCos = trig_point(LegacyCotX, 30)
	CotBox = CotCos / CotSin
	record(CotBox.hi < LegacyCotBox.lo, "Pinned legacy cot output provably misses exact input value",
		x=LegacyCotX, legacy_box=LegacyCotBox, certified_cot=CotBox, gap=LegacyCotBox.lo - CotBox.hi)
	record(BinaryPi < PiBox.lo, "Legacy binary pi leaves a strict tail", binary_pi=BinaryPi, gap=PiBox.lo - BinaryPi)

	Sin2, _ = trig_point(Fraction(2), 80)
	Sin23, Cos23 = trig_point(Fraction(23, 10), 90)
	FirstBound = Fraction(8)
	SecondBound = 2 * Fraction(23, 10) ** 2 * Fraction(91, 100) ** 2
	ThirdBound = 2 * (Fraction(23, 10) * Fraction(3, 4)) ** 2
	DerivativeUpper = Fraction(3, 4) - Fraction(23, 10) * Fraction(3, 5)
	record(PiBox.hi / 2 < 2 < Fraction(23, 10) < PiBox.lo,
		"B three ranges cover (pi/2, pi)", cut_points=[Fraction(2), Fraction(23, 10)])
	record(Sin2.hi < Fraction(91, 100) and Sin23.hi < Fraction(3, 4) and Cos23.hi < -Fraction(3, 5),
		"B endpoint Taylor inequalities", sin_2=Sin2, sin_23_over_10=Sin23, cos_23_over_10=Cos23)
	record(DerivativeUpper < 0 and max(FirstBound, SecondBound, ThirdBound) < 9,
		"B(t)<9 using the documented analytic three-range argument", upper_bounds=[FirstBound, SecondBound, ThirdBound], q_prime_upper=DerivativeUpper)

	SqrtTwo = Interval(Fraction("1.414213562373095"), Fraction("1.414213562373096"))
	check_sqrt_two(SqrtTwo)
	PiOver8 = PiBox / 8
	CzBox = (1 / PiOver8 - (1 + SqrtTwo)) / PiOver8
	record(0 < CzBox.lo and CzBox.hi < Fraction(337, 1000), "0<Cz<0.337", sqrt_two=SqrtTwo, cz=CzBox)
	EpsilonUpper = Fraction(10, 387)
	TanUpper = Fraction(29, 70)
	record(1500 * EpsilonUpper ** 2 > 1 and SqrtTwo.hi - 1 < TanUpper,
		"Rational epsilon0 and tan(pi/8) upper bounds", epsilon_upper=EpsilonUpper, tan_upper=TanUpper)
	PhaseLower = PiBox.lo / 2 - EpsilonUpper * TanUpper
	C2Lower = 1 - PiBox.hi ** 2 * EpsilonUpper ** 2 / 192
	DeltaUpper = Fraction(45, 100000)
	CorrectionUpper = Fraction(100046, 100000)
	record(2 * Fraction(337, 1000) / 1500 < DeltaUpper and 1 / (1 - DeltaUpper) < CorrectionUpper,
		"Scalar denominator correction", delta_upper=DeltaUpper, reciprocal=1 / (1 - DeltaUpper), correction_upper=CorrectionUpper)
	record(PiBox.lo > Fraction(333, 106) and PhaseLower > Fraction(156, 100) and C2Lower > Fraction(99996, 100000),
		"Strict positive scalar denominator bounds", phase_lower=PhaseLower, c2_lower=C2Lower)
	RatioUpper = 4 * Fraction(337, 1000) * 9 * CorrectionUpper / (3 * Fraction(333, 106) * Fraction(156, 100) * Fraction(99996, 100000))
	record(RatioUpper < Fraction(8256, 10000), "Final scalar ratio <0.8256", ratio_upper=RatioUpper, gap=Fraction(8256, 10000) - RatioUpper)
	return {"pi": PiBox, "a_star": RootBracket, "u_star": UBox, "d_star": DBox, "cz": CzBox,
		"ratio_upper": RatioUpper, "legacy_cot_certified": CotBox, "checks": rows}


NegativeControls = (
	"wrong-g-right", "old-upper-endpoint", "wrong-u-enclosure", "wrong-value-enclosure",
	"unsafe-cot-enclosure", "binary-pi-enclosure", "wrong-sqrt-enclosure",
	"omitted-taylor-remainder", "zero-divisor", "reversed-interval", "float-input",
	"invalid-taylor-degree", "invalid-atan-domain", "wrong-ratio-bound",
)


def run_negative(name):
	"""Every branch passes a false candidate into a real mathematical guard."""
	PiBox = machin_pi()
	if name == "wrong-g-right":
		check_g_bracket(Interval(RootBracket.lo - Fraction(1, 10 ** 40), RootBracket.lo), PiBox)
	elif name == "old-upper-endpoint":
		monotone_root_image(Fraction(1, 3), Fraction(3, 8), Interval(2, Fraction(12, 5)), Interval(Fraction(12, 5), OldRootBracket.lo), PiBox)
	elif name == "wrong-u-enclosure":
		ComputedBox = increasing_image(u_point(RootBracket.lo, PiBox), u_point(RootBracket.hi, PiBox))
		require_encloses(Interval(Fraction("0.32992250812006654958"), Fraction("0.32992250812006654959")), ComputedBox, name)
	elif name == "wrong-value-enclosure":
		values = certificate_checks()
		require_encloses(Interval(Fraction("24.9438661384324768"), Fraction("24.9438661384324769")), values["d_star"], name)
	elif name == "unsafe-cot-enclosure":
		s, c = trig_point(LegacyCotX, 30)
		require_encloses(LegacyCotBox, c / s, name)
	elif name == "binary-pi-enclosure":
		require_encloses(Interval.point(BinaryPi), PiBox, name)
	elif name == "wrong-sqrt-enclosure":
		check_sqrt_two(Interval(Fraction("1.41421356237309"), Fraction("1.414213562373095")))
	elif name == "omitted-taylor-remainder":
		s, _ = trig_point(Fraction(1), 110)
		require_encloses(Interval.point(Fraction(1) - Fraction(1, 6)), s, name)
	elif name == "zero-divisor":
		Interval.point(1) / Interval(-1, 1)
	elif name == "reversed-interval":
		Interval(2, 1)
	elif name == "float-input":
		Interval.point(float("0.1"))
	elif name == "invalid-taylor-degree":
		trig_point(Fraction(1), -1)
	elif name == "invalid-atan-domain":
		atan_small(Fraction(1), 10)
	elif name == "wrong-ratio-bound":
		values = certificate_checks()
		require(values["ratio_upper"] < Fraction(825, 1000), "Proposed scalar upper bound 0.825 is not certified")
	else:
		raise ValueError("Unknown negative control")


def directed_decimal(value, upward, digits=60):
	value = rational(value)
	with localcontext() as context:
		context.prec = digits
		context.rounding = ROUND_CEILING if upward else ROUND_FLOOR
		return str(Decimal(value.numerator) / Decimal(value.denominator))


def encode(value):
	if isinstance(value, Fraction):
		return {"exact": str(value.numerator) + "/" + str(value.denominator),
			"display_lower": directed_decimal(value, False), "display_upper": directed_decimal(value, True)}
	if isinstance(value, Interval):
		return {"lower": encode(value.lo), "upper": encode(value.hi),
			"outward_display": [directed_decimal(value.lo, False), directed_decimal(value.hi, True)]}
	if isinstance(value, dict):
		return {key: encode(item) for key, item in value.items()}
	if isinstance(value, (list, tuple)):
		return [encode(item) for item in value]
	return value


def main():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--output", type=Path)
	parser.add_argument("--negative", choices=NegativeControls)
	args = parser.parse_args()
	if args.negative:
		run_negative(args.negative)
		print("NEGATIVE CONTROL UNEXPECTEDLY ACCEPTED:", args.negative, file=sys.stderr)
		return 0
	values = certificate_checks()
	output = {
		"status": "AUTHOR_SCOPED_ARITHMETIC_CHECKED",
		"role": "certificate author; no independent final review",
		"python": sys.version, "optimized": bool(sys.flags.optimize),
		"proof_arithmetic": "Exact Fraction/int; 90-place exact outward rational grid; Decimal only for directed display",
		"analytic_contract": "README.md: Machin/Taylor, T2 uniqueness, monotonicity and three-range B proof",
		"limitations": ["No deep-sliver coverage proof", "No complete INF-limit certification", "No main TeX or canonical changes", "No Lean execution"],
		**encode(values),
	}
	if args.output:
		args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
	print("AUTHOR SCOPED CERTIFICATE:", len(values["checks"]), "exact obligation groups checked")
	for name in ("a_star", "u_star", "d_star", "cz"):
		print(name + ":", output[name]["outward_display"])
	print("ratio_upper:", output["ratio_upper"]["display_upper"])
	return 0


if __name__ == "__main__":
	sys.exit(main())
