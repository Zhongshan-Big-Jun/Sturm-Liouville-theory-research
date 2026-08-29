"""Solve the rank-three level-4 system after its exact compatibility condition."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))
sys.path.insert(0, str(ROOT))

import sympy as sp

from fresh_cascade_even4 import a0, a2, a4, b0, build, c0, c2, k0, k2, k4


REL = sp.pi*k0**3 - 18*sp.pi**2 + 48


def mod_relation(expr: sp.Expr) -> sp.Expr:
	expr = sp.cancel(expr)
	num, den = sp.fraction(expr)
	num_r = sp.rem(sp.Poly(num, k0), sp.Poly(REL, k0)).as_expr()
	den_r = sp.rem(sp.Poly(den, k0), sp.Poly(REL, k0)).as_expr()
	return sp.factor(sp.cancel(num_r / den_r))


def main() -> None:
	s = build()
	a2_formula = -(k0**4 + 12*k0*k2 - 18*sp.pi*k0 + 24*k0) / (6*k0**3)
	seed = {a0: 2/k0, a2: a2_formula, c0: 16/(sp.pi*k0)}
	eqs = [sp.cancel(s[name].coeff(power).subs(seed)) for name, power in
		(("E1", 4), ("E2", 4), ("E5", 6), ("E6", 7))]
	partial = sp.solve(eqs[:3], (a4, b0, c2), dict=True, simplify=False)[0]
	rows = {str(key): mod_relation(value) for key, value in partial.items()}
	residual = mod_relation(eqs[3].subs(partial))
	rows["E6_7_residual_mod_relation"] = residual
	print(json.dumps({key: sp.sstr(value) for key, value in rows.items()}, indent=2))


if __name__ == "__main__":
	main()
