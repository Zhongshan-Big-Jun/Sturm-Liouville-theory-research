"""Fresh even-parity cascade through level j=4."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))
sys.path.insert(0, str(ROOT))

import sympy as sp

from fresh_series_fast import LS, cos_s, mass_components, sin_s


k0, k2, k4 = sp.symbols("k0 k2 k4", positive=True, real=True)
a0, a2, a4 = sp.symbols("a0 a2 a4", real=True)
b0 = sp.symbols("b0", real=True)
c0, c2 = sp.symbols("c0 c2", real=True)


def build() -> dict[str, LS]:
	u = LS.monomial(1)
	eps = LS.monomial(3)
	kfun = LS.scalar(k0) + LS.monomial(2, k2) + LS.monomial(4, k4)
	afun = LS.scalar(a0) + LS.monomial(2, a2) + LS.monomial(4, a4)
	bfun = LS.scalar(b0)
	cfun = LS.scalar(c0) + LS.monomial(2, c2)
	kd = u * kfun
	kn = kd + LS.monomial(5) * cfun
	p1d = LS.scalar(sp.pi / 2) + LS.monomial(2) * afun
	p3d = LS.scalar(sp.pi / 4) + LS.monomial(2) * bfun
	ratio = kn / kd
	p1n = ratio * p1d
	p3n = ratio * p3d
	p2d = kd / 2 - eps * (p1d + p3d)
	p2n = kn / 2 - eps * ratio * (p1d + p3d)
	e1 = (cos_s(p2d) * sin_s(p1d + p3d)
		+ sin_s(p2d) * cos_s(p3d) * cos_s(p1d) / eps
		- eps * sin_s(p3d) * sin_s(p2d) * sin_s(p1d))
	e2 = (cos_s(p2n) * cos_s(p1n) * cos_s(p3n)
		- sin_s(p3n) * sin_s(p2n) * cos_s(p1n) / eps
		- sin_s(p3n) * cos_s(p2n) * sin_s(p1n)
		- eps * cos_s(p3n) * sin_s(p2n) * sin_s(p1n))
	m1d, m3d, mld = mass_components(kd, p1d, p2d, p3d, eps, "D")
	m1n, m3n, mln = mass_components(kn, p1n, p2n, p3n, eps, "N")
	e5 = (m1d + m3d + mld) * sin_s(p1n)**2 \
		- (m1n + m3n + mln) * sin_s(p1d)**2
	e6 = (sin_s(p1d) * (eps * cos_s(p2n) + sin_s(p2n) * cos_s(p1n) / sin_s(p1n))
		+ eps * cos_s(p2d) * sin_s(p1d) + sin_s(p2d) * cos_s(p1d))
	return {"E1": e1, "E2": e2, "E5": e5, "E6": e6}


def main() -> None:
	s = build()
	a2_formula = -(k0**4 + 12*k0*k2 - 18*sp.pi*k0 + 24*k0) / (6*k0**3)
	seed = {a0: 2/k0, a2: a2_formula, c0: 16/(sp.pi*k0)}
	equations = {
		"E1_4": s["E1"].coeff(4),
		"E2_4": s["E2"].coeff(4),
		"E5_6": s["E5"].coeff(6),
		"E6_7": s["E6"].coeff(7),
	}
	reduced = {name: sp.factor(sp.cancel(expr.subs(seed))) for name, expr in equations.items()}
	unknowns = (a4, b0, c2, k4)
	matrix, rhs = sp.linear_eq_to_matrix(list(reduced.values()), unknowns)
	left_null = matrix.T.nullspace()
	right_null = matrix.nullspace()
	consistency = [sp.factor(sp.cancel((vec.T * rhs)[0])) for vec in left_null]
	linear_solution = sp.solve(list(reduced.values()) + consistency, unknowns,
		dict=True, simplify=False)
	payload = {"equations": {name: sp.sstr(expr) for name, expr in reduced.items()},
		"matrix_det": sp.sstr(sp.factor(matrix.det())),
		"matrix_rank": matrix.rank(),
		"left_null": [[sp.sstr(sp.factor(v)) for v in vec] for vec in left_null],
		"right_null": [[sp.sstr(sp.factor(v)) for v in vec] for vec in right_null],
		"consistency": [sp.sstr(v) for v in consistency],
		"solutions": [{sp.sstr(key): sp.sstr(sp.factor(sp.cancel(value)))
			for key, value in row.items()} for row in linear_solution]}
	print(json.dumps(payload, indent=2))


if __name__ == "__main__":
	main()
