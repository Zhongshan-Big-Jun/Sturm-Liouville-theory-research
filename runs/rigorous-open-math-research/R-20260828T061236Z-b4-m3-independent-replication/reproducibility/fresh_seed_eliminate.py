"""Exact elimination of the level-0..2 cascade seed."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))
sys.path.insert(0, str(ROOT))

import sympy as sp

from fresh_cascade_seed import a0, a1, a2, build, c0, k0, k1, k2c


def main() -> None:
	s = build()
	a2_formula = (-k0**4 - 12 * k0 * k2c + 18 * sp.pi * k0 - 24 * k0
		+ 12 * k1**2) / (6 * k0**3)
	c0_formula = 16 / (sp.pi * k0)
	subs = {a0: 2 / k0, a1: -2 * k1 / k0**2,
		a2: a2_formula, c0: c0_formula}
	rows = {
		"a0": 2 / k0,
		"a1": -2 * k1 / k0**2,
		"a2": a2_formula,
		"c0": c0_formula,
		"E1_2": s["E1"].coeff(2).subs(subs),
		"E2_2": s["E2"].coeff(2).subs(subs),
		"E6_5": s["E6"].coeff(5).subs(subs),
		"E5_4": s["E5"].coeff(4).subs(subs),
		"m1diff_4": s["m1D-m1N"].coeff(4).subs(subs),
		"m3diff_4": s["m3D-m3N"].coeff(4).subs(subs),
		"mLdiff_4": s["mLD-mLN"].coeff(4).subs(subs),
	}
	print(json.dumps({name: sp.sstr(sp.factor(sp.cancel(expr)))
		for name, expr in rows.items()}, indent=2))


if __name__ == "__main__":
	main()
