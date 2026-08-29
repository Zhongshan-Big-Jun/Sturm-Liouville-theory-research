"""Independent exact truncated-series algebra for the B4/P1 M3 system.

This avoids importing either the old M3 coefficient builder or any saved
coefficient dictionary.  All coefficients are regenerated from the four exact
band equations using a small Laurent-series implementation below.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))

import sympy as sp


MAX_ORDER = 14
MIN_ORDER = -12
K, A, B, C = sp.symbols("K A B C", nonzero=True, real=True)


@dataclass(frozen=True)
class LS:
	c: dict[int, sp.Expr]

	def __post_init__(self) -> None:
		clean = {
			int(p): sp.sympify(v)
			for p, v in self.c.items()
			if MIN_ORDER <= int(p) <= MAX_ORDER and v != 0
		}
		object.__setattr__(self, "c", clean)

	@staticmethod
	def scalar(value: sp.Expr) -> "LS":
		return LS({0: sp.sympify(value)})

	@staticmethod
	def monomial(power: int, value: sp.Expr = 1) -> "LS":
		return LS({power: sp.sympify(value)})

	def __add__(self, other: "LS | sp.Expr") -> "LS":
		o = other if isinstance(other, LS) else LS.scalar(other)
		powers = set(self.c) | set(o.c)
		return LS({p: self.c.get(p, 0) + o.c.get(p, 0) for p in powers})

	__radd__ = __add__

	def __neg__(self) -> "LS":
		return LS({p: -v for p, v in self.c.items()})

	def __sub__(self, other: "LS | sp.Expr") -> "LS":
		return self + (-other if isinstance(other, LS) else -sp.sympify(other))

	def __rsub__(self, other: sp.Expr) -> "LS":
		return LS.scalar(other) - self

	def __mul__(self, other: "LS | sp.Expr") -> "LS":
		o = other if isinstance(other, LS) else LS.scalar(other)
		out: dict[int, sp.Expr] = {}
		for p, a in self.c.items():
			for q, b in o.c.items():
				r = p + q
				if MIN_ORDER <= r <= MAX_ORDER:
					out[r] = out.get(r, 0) + a * b
		return LS(out)

	__rmul__ = __mul__

	def __pow__(self, power: int) -> "LS":
		if power < 0:
			return self.inv() ** (-power)
		out = LS.scalar(1)
		base = self
		n = power
		while n:
			if n & 1:
				out = out * base
			base = base * base
			n //= 2
		return out

	def inv(self) -> "LS":
		if not self.c:
			raise ZeroDivisionError("zero Laurent series")
		lead = min(self.c)
		lead_coef = self.c[lead]
		q = LS({p - lead: v / lead_coef for p, v in self.c.items() if p != lead})
		term = LS.scalar(1)
		geom = LS.scalar(1)
		# q has strictly positive valuation, so this finite geometric series is exact
		# through MAX_ORDER.
		for _ in range(MAX_ORDER - MIN_ORDER + 2):
			term = -term * q
			if not term.c:
				break
			geom = geom + term
		return LS.monomial(-lead, 1 / lead_coef) * geom

	def __truediv__(self, other: "LS | sp.Expr") -> "LS":
		o = other if isinstance(other, LS) else LS.scalar(other)
		return self * o.inv()

	def coeff(self, power: int) -> sp.Expr:
		return sp.factor(sp.cancel(self.c.get(power, 0)))


def sin_s(x: LS) -> LS:
	constant = x.c.get(0, 0)
	h = LS({p: v for p, v in x.c.items() if p != 0})
	sinh = LS.scalar(0)
	cosh = LS.scalar(1)
	power = LS.scalar(1)
	for n in range(1, MAX_ORDER + 2):
		power = power * h
		if not power.c:
			break
		if n % 2:
			sinh = sinh + ((-1) ** ((n - 1) // 2)) * power * sp.Rational(1, sp.factorial(n))
		else:
			cosh = cosh + ((-1) ** (n // 2)) * power * sp.Rational(1, sp.factorial(n))
	return sp.sin(constant) * cosh + sp.cos(constant) * sinh


def cos_s(x: LS) -> LS:
	constant = x.c.get(0, 0)
	h = LS({p: v for p, v in x.c.items() if p != 0})
	sinh = LS.scalar(0)
	cosh = LS.scalar(1)
	power = LS.scalar(1)
	for n in range(1, MAX_ORDER + 2):
		power = power * h
		if not power.c:
			break
		if n % 2:
			sinh = sinh + ((-1) ** ((n - 1) // 2)) * power * sp.Rational(1, sp.factorial(n))
		else:
			cosh = cosh + ((-1) ** (n // 2)) * power * sp.Rational(1, sp.factorial(n))
	return sp.cos(constant) * cosh - sp.sin(constant) * sinh


def mass_components(k: LS, p1: LS, p2: LS, p3: LS, eps: LS,
		mode: str) -> tuple[LS, LS, LS]:
	base = eps * cos_s(p2) * sin_s(p1) / k + sin_s(p2) * cos_s(p1) / k
	if mode == "D":
		bc = -base / sin_s(p3)
		m3 = bc**2 * (p3 - sin_s(2 * p3) / 2) / (2 * k * eps)
	else:
		bc = base / cos_s(p3)
		m3 = bc**2 * (p3 + sin_s(2 * p3) / 2) / (2 * k * eps)
	m1 = (p1 - sin_s(2 * p1) / 2) * eps / (2 * k**3)
	a = eps * sin_s(p1) / k
	b = cos_s(p1) / k
	ml = ((a**2 + b**2) * p2 / (2 * k)
		+ (a**2 - b**2) * sin_s(2 * p2) / (4 * k)
		+ a * b * (1 - cos_s(2 * p2)) / (2 * k))
	return m1, m3, ml


def build() -> dict[str, LS]:
	eps = LS.monomial(3)
	k2 = LS.monomial(1, K)
	k3 = LS.monomial(1, K) + LS.monomial(5, C)
	p1 = LS.scalar(sp.pi / 2) + LS.monomial(2, A)
	p3 = LS.scalar(sp.pi / 4) + LS.monomial(2, B)
	ratio = k3 / k2
	p1t = ratio * p1
	p3t = ratio * p3
	p2 = k2 / 2 - eps * (p1 + p3)
	p2t = k3 / 2 - eps * ratio * (p1 + p3)

	e1 = (cos_s(p2) * sin_s(p1 + p3)
		+ sin_s(p2) * cos_s(p3) * cos_s(p1) / eps
		- eps * sin_s(p3) * sin_s(p2) * sin_s(p1))
	e2 = (cos_s(p2t) * cos_s(p1t) * cos_s(p3t)
		- sin_s(p3t) * sin_s(p2t) * cos_s(p1t) / eps
		- sin_s(p3t) * cos_s(p2t) * sin_s(p1t)
		- eps * cos_s(p3t) * sin_s(p2t) * sin_s(p1t))
	m1d, m3d, mld = mass_components(k2, p1, p2, p3, eps, "D")
	m1n, m3n, mln = mass_components(k3, p1t, p2t, p3t, eps, "N")
	id_ = m1d + m3d + mld
	in_ = m1n + m3n + mln
	e5 = id_ * sin_s(p1t)**2 - in_ * sin_s(p1)**2
	e6 = (sin_s(p1) * (eps * cos_s(p2t) + sin_s(p2t) * cos_s(p1t) / sin_s(p1t))
		+ eps * cos_s(p2) * sin_s(p1) + sin_s(p2) * cos_s(p1))
	return {
		"E1": e1,
		"E2": e2,
		"E5": e5,
		"E6": e6,
		"m1D-m1N": m1d - m1n,
		"m3D-m3N": m3d - m3n,
		"mLD-mLN": mld - mln,
	}


def main() -> None:
	series = build()
	out: dict[str, dict[str, str]] = {}
	for name, value in series.items():
		rows: dict[str, str] = {}
		for power in sorted(value.c):
			if power <= 10:
				coef = value.coeff(power)
				if coef != 0:
					rows[str(power)] = sp.sstr(coef)
		out[name] = rows
	print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
	main()
