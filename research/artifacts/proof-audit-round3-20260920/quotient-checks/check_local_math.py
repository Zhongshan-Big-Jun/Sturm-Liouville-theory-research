"""Author-side exact cross-checks, not an independent proof verification."""

import json
from pathlib import Path

import sympy as s

Root = Path(__file__).resolve().parent
x = s.symbols("x", real=True)
n = s.symbols("n", integer=True, positive=True)
mu, c = s.symbols("mu c", positive=True)
Results = []


def integral(f):
	return s.integrate(s.expand(f), (x, -1, 1))


def delta(f):
	return s.simplify(f.subs(x, 1) - f.subs(x, -1))


def image_t(f):
	return s.simplify(s.diff(f, x) - delta(f) / 2)


def inner(f, g):
	return integral(f * s.conjugate(g))


def form(f, g, Shift=0):
	return s.simplify(inner(s.diff(f, x), s.diff(g, x))
		- delta(f) * s.conjugate(delta(g)) / 2 + Shift * inner(f, g))


def check(Name, Actual, Expected=0):
	Residual = s.simplify(s.expand(Actual - Expected))
	assert Residual == 0, (Name, Residual)
	Results.append({"check": Name, "status": "PASS", "exact_value": str(Expected)})


a, b = s.symbols("a b", complex=True)
check("T annihilates every complex affine function", image_t(a + b * x))
RealParts = s.symbols("r0:4", real=True)
ImagParts = s.symbols("s0:4", real=True)
f = sum((RealParts[j] + s.I * ImagParts[j]) * x**j for j in range(4))
check("sesquilinear norm identity for a general complex cubic",
	form(f, f) - inner(image_t(f), image_t(f)))
check("complex affine ix has zero form norm", form(s.I * x, s.I * x))
WrongExpression = inner(s.I, s.I) - delta(s.I * x)**2 / 2
check("the old non-modulus expression gives 4 for ix", WrongExpression, 4)
check("actual T cosine image for every positive integer n",
	image_t(s.cos(n * s.pi * x)), -n * s.pi * s.sin(n * s.pi * x))
check("actual T sine image for every positive mu",
	image_t(s.sin(mu * x)), mu * s.cos(mu * x) - s.sin(mu))
check("T cosine image has zero mean", integral(image_t(s.cos(n * s.pi * x))))
check("T sine image has zero mean", integral(image_t(s.sin(mu * x))))
check("h=x has zero mean", integral(x))
check("h=x is nonzero", inner(x, x), s.Rational(2, 3))
check("h=x is orthogonal to every original cosine", inner(x, s.cos(n * s.pi * x)))
SineMoment = inner(x, s.sin(mu * x))
check("h=x original sine moment", SineMoment,
	2 * (s.sin(mu) - mu * s.cos(mu)) / mu**2)
check("h=x original sine moment vanishes at a positive tangent root",
	s.expand(SineMoment).subs(s.sin(mu), mu * s.cos(mu)))
check("h=x is not orthogonal to the actual T cosine image",
	inner(x, image_t(s.cos(s.pi * x))), -2)
OperatorVector = (1 + s.I) + (2 - s.I) * x + (3 + 2*s.I) * (x**4 - 2*x**2)
OperatorVector += (1 - 3*s.I) * (x**5 - 2*x**3)
for Endpoint in (-1, 1):
	check(f"operator test vector satisfies Krein boundary condition at {Endpoint}",
		s.diff(OperatorVector, x).subs(x, Endpoint) - delta(OperatorVector) / 2)
FormVector = x**2 + s.I * x**3
assert s.simplify(s.diff(FormVector, x).subs(x, 1) - delta(FormVector)/2) != 0
check("operator-form identity with second vector in H1 but not D(Kc)",
	form(OperatorVector, FormVector, c),
	inner(-s.diff(OperatorVector, x, 2) + c*OperatorVector, FormVector))
check("shifted form differs from the quotient form by c times L2 norm squared",
	form(f, f, c) - form(f, f), c * inner(f, f))

Payload = {
	"role": "AUTHOR",
	"scope": "Exact local algebra/integrals only; spectral convergence is an analytic argument.",
	"sympy_version": s.__version__,
	"checks": Results,
}
(Root / "exact-checks.json").write_text(json.dumps(Payload, indent=2) + "\n", encoding="utf-8")
print(f"{len(Results)} exact author-side checks passed; output: {Root / 'exact-checks.json'}")
