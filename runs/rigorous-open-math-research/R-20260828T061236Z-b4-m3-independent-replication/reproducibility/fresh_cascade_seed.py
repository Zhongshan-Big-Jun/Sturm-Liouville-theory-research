"""Build and solve the joint level-0..2 seed without prior M3 coefficients."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))
sys.path.insert(0, str(ROOT))

import sympy as sp

from fresh_series_fast import LS, cos_s, mass_components, sin_s


k0, k1, k2c = sp.symbols("k0 k1 k2", positive=True, real=True)
a0, a1, a2 = sp.symbols("a0 a1 a2", real=True)
b0, c0 = sp.symbols("b0 c0", real=True)


def build() -> dict[str, LS]:
	one_u = LS.monomial(1)
	eps = LS.monomial(3)
	kfun = LS.scalar(k0) + LS.monomial(1, k1) + LS.monomial(2, k2c)
	afun = LS.scalar(a0) + LS.monomial(1, a1) + LS.monomial(2, a2)
	bfun = LS.scalar(b0)
	cfun = LS.scalar(c0)
	kd = one_u * kfun
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
	return {
		"E1": e1,
		"E2": e2,
		"E5": e5,
		"E6": e6,
		"m1D-m1N": m1d - m1n,
		"m3D-m3N": m3d - m3n,
		"mLD-mLN": mld - mln,
	}


def reduce_seed(expr: sp.Expr) -> sp.Expr:
	return sp.factor(sp.cancel(expr.subs({a0: 2 / k0, a1: -2 * k1 / k0**2})))


def main() -> None:
	s = build()
	requested = {
		"E1_0": s["E1"].coeff(0),
		"E2_0": s["E2"].coeff(0),
		"E6_3": s["E6"].coeff(3),
		"E1_1": s["E1"].coeff(1),
		"E2_1": s["E2"].coeff(1),
		"E6_4": s["E6"].coeff(4),
		"E1_2": s["E1"].coeff(2),
		"E2_2": s["E2"].coeff(2),
		"E5_4": s["E5"].coeff(4),
		"E6_5": s["E6"].coeff(5),
		"m1diff_4": s["m1D-m1N"].coeff(4),
		"m3diff_4": s["m3D-m3N"].coeff(4),
	}
	out: dict[str, dict[str, str]] = {}
	for name, expr in requested.items():
		out[name] = {
			"raw": sp.sstr(sp.factor(expr)),
			"after_AK_and_level1": sp.sstr(reduce_seed(expr)),
		}
	a2_formula = (-k0**4 - 12 * k0 * k2c + 18 * sp.pi * k0 - 24 * k0
		+ 12 * k1**2) / (6 * k0**3)
	c0_formula = 16 / (sp.pi * k0)
	seed_subs = {a0: 2 / k0, a1: -2 * k1 / k0**2,
		a2: a2_formula, c0: c0_formula}
	out["seed_elimination"] = {
		"a2": sp.sstr(sp.factor(a2_formula)),
		"c0": sp.sstr(c0_formula),
		"E1_2": sp.sstr(sp.factor(s["E1"].coeff(2).subs(seed_subs))),
		"E2_2": sp.sstr(sp.factor(s["E2"].coeff(2).subs(seed_subs))),
		"E6_5": sp.sstr(sp.factor(s["E6"].coeff(5).subs(seed_subs))),
		"E5_4": sp.sstr(sp.factor(sp.cancel(s["E5"].coeff(4).subs(seed_subs)))),
		"m1diff_4": sp.sstr(sp.factor(sp.cancel(s["m1D-m1N"].coeff(4).subs(seed_subs)))),
		"m3diff_4": sp.sstr(sp.factor(sp.cancel(s["m3D-m3N"].coeff(4).subs(seed_subs)))),
	}
	print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
	main()
