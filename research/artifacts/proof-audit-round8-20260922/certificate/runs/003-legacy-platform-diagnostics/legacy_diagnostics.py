"""Platform observations only; none of this module is certificate arithmetic."""
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import checks


def fraction_text(value):
	return str(value.numerator) + "/" + str(value.denominator)


def main():
	checks.mp.mp.dps = 50
	checks.iv.dps = 45
	LeftRoot, RightRoot = checks.source05_a_root(checks.mp.mpf(3) / 8)
	x = float.fromhex("0x1.15eb9385ed50fp-8")
	OldLow, OldHigh = checks.old_cot_box(x)
	s, c = checks.trig_point(Fraction.from_float(x), 30)
	TruthBox = c / s
	row = {
		"role": "Non-certified diagnostic, proposed exact inputs for independent rechecking",
		"root_u": "3/8",
		"old_root_lower": fraction_text(checks.mp_fraction(LeftRoot)),
		"old_root_upper": fraction_text(checks.mp_fraction(RightRoot)),
		"cot_x_hex": x.hex(), "cot_x": fraction_text(Fraction.from_float(x)),
		"cot_output_repr": [repr(OldLow), repr(OldHigh)],
		"cot_output_exact": [fraction_text(Fraction.from_float(OldLow)), fraction_text(Fraction.from_float(OldHigh))],
		"supplied_miss_reproduced_here": TruthBox.hi < Fraction.from_float(OldLow),
		"cot_reference_display_from_supplied_checker": TruthBox.display(),
		"mpmath": checks.mp.__version__, "sympy": checks.sp.__version__,
		"math_pi_exact": fraction_text(Fraction.from_float(math.pi)),
	}
	Path(sys.argv[1]).write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")
	print(json.dumps(row, indent=2))


if __name__ == "__main__":
	main()
