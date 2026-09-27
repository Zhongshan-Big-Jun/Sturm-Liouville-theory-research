"""Exact certificate transport and fail-closed reception, round13.

This checks contracts and finite rational witness arithmetic. Functional
enclosures additionally rely on the recorded generator/engine and their proof;
this module is not an independent transcendental engine or a Lean proof.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import os
import sys
import tempfile

sys.set_int_max_str_digits(1000000)
SCHEMA = 'e1-exact-certificate/v2'


def require(Condition, Message):
	if not Condition:
		raise ValueError(Message)


def fraction_text(Value):
	Value = F(Value)
	return str(Value.numerator) + '/' + str(Value.denominator)


def decimal_endpoint(Value, Direction, Digits=12):
	"""Integer division only: floor for a lower bound, ceiling for an upper."""
	require(Direction in ('lower', 'upper'), 'unknown rounding direction')
	require(type(Digits) is int and 0 <= Digits <= 1000, 'invalid decimal places')
	Value = F(Value)
	Scale = 10 ** Digits
	Numerator = Value.numerator * Scale
	Rounded = Numerator // Value.denominator if Direction == 'lower' else -((-Numerator) // Value.denominator)
	Sign = '-' if Rounded < 0 else ''
	Rounded = abs(Rounded)
	if not Digits:
		return Sign + str(Rounded)
	return Sign + str(Rounded // Scale) + '.' + str(Rounded % Scale).zfill(Digits)


def display_interval(Bounds, Digits=12):
	return [decimal_endpoint(Bounds[0], 'lower', Digits), decimal_endpoint(Bounds[1], 'upper', Digits)]


def exact_interval(Value):
	return [fraction_text(Value.lo), fraction_text(Value.hi)]


def read_interval(Value):
	require(isinstance(Value, list) and len(Value) == 2 and all(isinstance(x, str) for x in Value), 'invalid exact interval')
	Bounds = tuple(F(x) for x in Value)
	require(Bounds[0] <= Bounds[1], 'reversed certificate interval')
	return Bounds


def predicate(Bounds, Comparison, Target):
	Target = F(Target)
	require(Comparison in ('gt', 'ge', 'lt', 'le'), 'unknown comparison')
	Margin = Bounds[0] - Target if Comparison in ('gt', 'ge') else Target - Bounds[1]
	return (Margin > 0 if Comparison in ('gt', 'lt') else Margin >= 0), Margin


def check_display(Bounds, Display):
	Shown = read_interval(Display)
	require(Shown[0] <= Bounds[0] <= Bounds[1] <= Shown[1], 'display does not enclose exact endpoints')


def source_hashes():
	Root = Path(__file__).resolve().parent
	return {Name: hashlib.sha256((Root / Name).read_bytes()).hexdigest() for Name in ('rigid1d.py', 'e1_certgen.py', 'e1_certificate_io.py')}


def atomic_json(PathValue, Data):
	Target = Path(PathValue)
	Target.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=Target.parent, delete=False) as Stream:
		Temporary = Path(Stream.name)
		json.dump(Data, Stream, ensure_ascii=False, indent=1)
		Stream.write('\n')
		Stream.flush()
		os.fsync(Stream.fileno())
	try:
		os.replace(Temporary, Target)
	finally:
		if Temporary.exists():
			Temporary.unlink()


def _check_witness(Detail, Comparison, Target, IntervalKey):
	Bounds = read_interval(Detail[IntervalKey + '_exact'])
	check_display(Bounds, Detail[IntervalKey])
	Passed, Margin = predicate(Bounds, Comparison, Target)
	require(F(Detail['margin_exact']) == Margin, 'incorrect exact margin')
	require(F(Detail['margin']) <= Margin, 'margin rounded upward')
	require(Detail['ok'] is Passed and Passed, 'unproved/false predicate')
	return Bounds


def validate_ledger(Ledger, CheckSources=True):
	"""Accept every named complete contract or raise; never trust summary alone."""
	require(Ledger.get('schema') == SCHEMA and Ledger.get('status') == 'PASS', 'not a complete current certificate')
	if CheckSources:
		require(Ledger['meta']['source_sha256'] == source_hashes(), 'certificate source has changed')
	require(Ledger['meta']['GLO'] == '131/200' and Ledger['meta']['GHI'] == '1309/1250' and Ledger['meta']['m'] == '791/2500', 'mathematical parameters differ')
	Facts = Ledger['facts']
	require([Row['name'] for Row in Facts] == [Spec['name'] for Spec in FACT_SPECS], 'missing, extra or reordered fact')
	require(Ledger['summary'] == dict(total=len(FACT_SPECS), passed=len(FACT_SPECS), failed=0, errors=0), 'summary does not certify all facts')
	for Row, Spec in zip(Facts, FACT_SPECS):
		require(Row['statement'] == Spec and Row['kind'] == Spec['kind'], 'label/contract mismatch')
		require(Row['ok'] is True and Row['status'] == 'PASS', 'failed or unknown fact')
		Detail = Row['detail']
		Cmp, Target = Spec['comparison'], F(Spec['target'])
		if Spec['kind'] == 'point':
			require(Detail['point'] == Spec['point'] and Detail['cmp'] == Cmp and F(Detail['target']) == Target, 'point contract mismatch')
			_check_witness(Detail, Cmp, Target, 'val')
		elif Spec['kind'] in ('value-taylor', 'deriv-taylor'):
			n = Spec['n']
			require(Detail['n'] == n and len(Detail['pieces']) == n and Detail['cmp'] == Cmp and F(Detail['target']) == Target, 'Taylor contract mismatch')
			a, b = map(F, Spec['domain'])
			for i, Piece in enumerate(Detail['pieces']):
				lo, hi = a + (b - a) * i / n, a + (b - a) * (i + 1) / n
				require(read_interval(Piece['cell']) == (lo, hi) and F(Piece['c']) == (lo + hi) / 2, 'missing or wrong Taylor cell')
				CenterKey = 'fvc' if Spec['kind'] == 'value-taylor' else 'fpc'
				Center = read_interval(Piece[CenterKey + '_exact'])
				check_display(Center, Piece[CenterKey])
				Slope = read_interval(Piece['slope_exact']) + read_interval(Piece['slope_center_exact'])
				M = max(map(abs, Slope))
				Correction = M * (hi - lo) / 2
				require(F(Piece['M_exact']) == M and F(Piece['corr_exact']) == Correction, 'incorrect Taylor radius')
				require(F(Piece['M']) >= M and F(Piece['corr']) >= Correction, 'radius rounded inward')
				Bounds = _check_witness(Piece, Cmp, Target, 'bound')
				require(Bounds == (Center[0] - Correction, Center[1] + Correction), 'incorrect final Taylor bound')
		elif Spec['kind'] == 'analytic':
			A, S, C = [read_interval(Detail[Key]) for Key in ('A_exact', 'sin_exact', 'cos_exact')]
			require(min(A[0], S[0], C[0]) > 0, 'B1 derivative assumptions missing')
			Bounds = _check_witness(Detail, 'lt', F(0), 'bound')
			require(Bounds == (-3 * C[1] - A[1] * S[1], -3 * C[0] - A[0] * S[0]), 'incorrect B1 derivative identity witness')
		elif Spec['kind'] == 'concavity-reduction':
			require(Detail['proof'] == 'h-concavity' and Detail['dependencies'] == ['h(gamma) >= m at 0.655', 'h(13/10) >= m'], 'invalid concavity dependencies')
			Domain = read_interval(Detail['argument_range_exact'])
			require(F(131, 200) <= Domain[0] <= Domain[1] <= F(13, 10), 'h argument leaves proved interval')
		else:
			raise ValueError('unsupported proof rule')
	Proof = Ledger['proofs']['h-concavity']
	require(Proof['domain'] == ['131/200', '13/10'] and len(Proof['cells']) == 8, 'incomplete concavity coverage')
	for i, Cell in enumerate(Proof['cells']):
		a, b = F(131, 200), F(13, 10)
		require(read_interval(Cell['cell']) == (a + (b - a) * i / 8, a + (b - a) * (i + 1) / 8), 'concavity cell mismatch')
		require(read_interval(Cell['second_derivative_exact'])[1] < 0, 'h concavity unproved')
	Primitives = Ledger['primitives']
	require([Row['point'] for Row in Primitives] == PRIMITIVE_POINTS, 'primitive point coverage differs')
	for Row in Primitives:
		for Key in ('sg', 'cg', 'tau', 'A', 'D'):
			check_display(read_interval(Row[Key + '_exact']), Row[Key])
	Pi = read_interval(Ledger['proofs']['pi_exact'])
	require(F(0) < F(131, 200) < F(1309, 1250) < Pi[0] / 2, 'tangent branch not justified')
	Tau = (read_interval(Primitives[0]['tau_exact'])[0], read_interval(Primitives[-1]['tau_exact'])[1])
	ExpectedRanges = {'h(gamma) >= m': (F(131, 200), F(1309, 1250)), 'h(tau) >= m': Tau, 'h(t) >= m on [0.655,13/10]': (F(131, 200), F(13, 10))}
	for Row in Facts:
		if Row['kind'] == 'concavity-reduction':
			require(read_interval(Row['detail']['argument_range_exact']) == ExpectedRanges[Row['name']], 'wrong h argument range')
	return dict(status='PASS', facts=len(Facts), primitives=len(Primitives), scope='Exact contracts, finite witness arithmetic, directed display and source binding; analytic enclosure lemmas remain explicit dependencies.')


def load_accepted_ledger(PathValue):
	Target = Path(PathValue)
	Status = json.loads(Target.with_suffix('.status.json').read_text(encoding='utf-8'))
	require(Status.get('status') == 'PASS', 'last generation did not succeed')
	Raw = Target.read_bytes()
	require(hashlib.sha256(Raw).hexdigest() == Status.get('ledger_sha256'), 'ledger differs from successful generation')
	Ledger = json.loads(Raw)
	validate_ledger(Ledger)
	return Ledger


# Full named contracts are populated from the inspected baseline declarations.
FACT_SPECS = json.loads(r'''
[
 {
  "name": "B1 decreasing [0.655,1.0472]",
  "kind": "analytic",
  "expression": "dB1",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ]
 },
 {
  "name": "B1(0.85) >= 1/200",
  "kind": "point",
  "expression": "B1",
  "comparison": "ge",
  "target": "1/200",
  "point": "17/20"
 },
 {
  "name": "B1(0.86) <= -1/50",
  "kind": "point",
  "expression": "B1",
  "comparison": "le",
  "target": "-1/50",
  "point": "43/50"
 },
 {
  "name": "B2 < 0",
  "kind": "value-taylor",
  "expression": "B2",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 4
 },
 {
  "name": "M < 0",
  "kind": "value-taylor",
  "expression": "M",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 2
 },
 {
  "name": "B4 > 0",
  "kind": "value-taylor",
  "expression": "B4",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 8
 },
 {
  "name": "G5 > 0",
  "kind": "value-taylor",
  "expression": "G5",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 8
 },
 {
  "name": "Qhi < 0",
  "kind": "value-taylor",
  "expression": "Qhi",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 8
 },
 {
  "name": "TA_B2 >= 27/10 on [0.723,0.724]",
  "kind": "value-taylor",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "27/10",
  "domain": [
   "723/1000",
   "181/250"
  ],
  "n": 4
 },
 {
  "name": "TC >= 19/10 on [0.82,0.83]",
  "kind": "value-taylor",
  "expression": "TC",
  "comparison": "ge",
  "target": "19/10",
  "domain": [
   "41/50",
   "83/100"
  ],
  "n": 4
 },
 {
  "name": "Qlo increasing",
  "kind": "deriv-taylor",
  "expression": "Qlo",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 4
 },
 {
  "name": "F increasing [1.0014,1.0472]",
  "kind": "deriv-taylor",
  "expression": "Fv",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "5007/5000",
   "1309/1250"
  ],
  "n": 2
 },
 {
  "name": "TA_B2 inc [0.655,0.72]",
  "kind": "deriv-taylor",
  "expression": "TA_B2",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "131/200",
   "18/25"
  ],
  "n": 8
 },
 {
  "name": "TA_B2 inc [0.72,0.723]",
  "kind": "deriv-taylor",
  "expression": "TA_B2",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "18/25",
   "723/1000"
  ],
  "n": 2
 },
 {
  "name": "TA_B2 dec [0.724,0.73]",
  "kind": "deriv-taylor",
  "expression": "TA_B2",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "181/250",
   "73/100"
  ],
  "n": 2
 },
 {
  "name": "TA_B2 dec [0.73,0.85]",
  "kind": "deriv-taylor",
  "expression": "TA_B2",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "73/100",
   "17/20"
  ],
  "n": 8
 },
 {
  "name": "TA_B2 dec [0.85,0.86]",
  "kind": "deriv-taylor",
  "expression": "TA_B2",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "17/20",
   "43/50"
  ],
  "n": 2
 },
 {
  "name": "TA_M dec [0.85,0.86]",
  "kind": "deriv-taylor",
  "expression": "TA_M",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "17/20",
   "43/50"
  ],
  "n": 2
 },
 {
  "name": "TA_M dec [0.86,1.0472]",
  "kind": "deriv-taylor",
  "expression": "TA_M",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "43/50",
   "1309/1250"
  ],
  "n": 4
 },
 {
  "name": "TB decreasing",
  "kind": "deriv-taylor",
  "expression": "TB",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "131/200",
   "1309/1250"
  ],
  "n": 8
 },
 {
  "name": "TC inc [0.655,0.82]",
  "kind": "deriv-taylor",
  "expression": "TC",
  "comparison": "gt",
  "target": "0/1",
  "domain": [
   "131/200",
   "41/50"
  ],
  "n": 16
 },
 {
  "name": "TC dec [0.83,1.0472]",
  "kind": "deriv-taylor",
  "expression": "TC",
  "comparison": "lt",
  "target": "0/1",
  "domain": [
   "83/100",
   "1309/1250"
  ],
  "n": 8
 },
 {
  "name": "TA_B2(0.655) >= 11/5",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "11/5",
  "point": "131/200"
 },
 {
  "name": "TA_B2(0.72) >= 13/5",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "13/5",
  "point": "18/25"
 },
 {
  "name": "TA_B2(0.73) >= 13/5",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "13/5",
  "point": "73/100"
 },
 {
  "name": "TA_B2(0.82) >= 2",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "2/1",
  "point": "41/50"
 },
 {
  "name": "TA_B2(0.83) >= 2",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "2/1",
  "point": "83/100"
 },
 {
  "name": "TA_B2(0.85) >= 19/10",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "19/10",
  "point": "17/20"
 },
 {
  "name": "TA_B2(0.86) >= 47/25",
  "kind": "point",
  "expression": "TA_B2",
  "comparison": "ge",
  "target": "47/25",
  "point": "43/50"
 },
 {
  "name": "TA_M(0.86) >= 9/5",
  "kind": "point",
  "expression": "TA_M",
  "comparison": "ge",
  "target": "9/5",
  "point": "43/50"
 },
 {
  "name": "TA_M(1.0014) >= 3/5",
  "kind": "point",
  "expression": "TA_M",
  "comparison": "ge",
  "target": "3/5",
  "point": "5007/5000"
 },
 {
  "name": "TA_M(1.0472) >= 3/8",
  "kind": "point",
  "expression": "TA_M",
  "comparison": "ge",
  "target": "3/8",
  "point": "1309/1250"
 },
 {
  "name": "TB(0.72) >= 3/10",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "3/10",
  "point": "18/25"
 },
 {
  "name": "TB(0.73) >= 3/10",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "3/10",
  "point": "73/100"
 },
 {
  "name": "TB(0.82) >= 3/20",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "3/20",
  "point": "41/50"
 },
 {
  "name": "TB(0.83) >= 3/20",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "3/20",
  "point": "83/100"
 },
 {
  "name": "TB(0.85) >= 1/10",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "1/10",
  "point": "17/20"
 },
 {
  "name": "TB(0.86) >= 1/10",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "1/10",
  "point": "43/50"
 },
 {
  "name": "TB(1.0014) >= 1/25",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "1/25",
  "point": "5007/5000"
 },
 {
  "name": "TB(1.0472) >= 1/40",
  "kind": "point",
  "expression": "TB",
  "comparison": "ge",
  "target": "1/40",
  "point": "1309/1250"
 },
 {
  "name": "TC(0.655) >= 57/50",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "57/50",
  "point": "131/200"
 },
 {
  "name": "TC(0.72) >= 3/2",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "3/2",
  "point": "18/25"
 },
 {
  "name": "TC(0.73) >= 3/2",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "3/2",
  "point": "73/100"
 },
 {
  "name": "TC(0.85) >= 19/10",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "19/10",
  "point": "17/20"
 },
 {
  "name": "TC(0.86) >= 19/10",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "19/10",
  "point": "43/50"
 },
 {
  "name": "TC(1.0014) >= 4/3",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "4/3",
  "point": "5007/5000"
 },
 {
  "name": "TC(1.0472) >= 11/10",
  "kind": "point",
  "expression": "TC",
  "comparison": "ge",
  "target": "11/10",
  "point": "1309/1250"
 },
 {
  "name": "B4(1.0472) >= 9/25",
  "kind": "point",
  "expression": "B4",
  "comparison": "ge",
  "target": "9/25",
  "point": "1309/1250"
 },
 {
  "name": "Qlo(1.0014) <= -1/10000",
  "kind": "point",
  "expression": "Qlo",
  "comparison": "le",
  "target": "-1/10000",
  "point": "5007/5000"
 },
 {
  "name": "Qlo(1.0472) <= 33/200",
  "kind": "point",
  "expression": "Qlo",
  "comparison": "le",
  "target": "33/200",
  "point": "1309/1250"
 },
 {
  "name": "F(1.0472) <= 63/100",
  "kind": "point",
  "expression": "Fv",
  "comparison": "le",
  "target": "63/100",
  "point": "1309/1250"
 },
 {
  "name": "tau(1.0472) < 13/10",
  "kind": "point",
  "expression": "tmax",
  "comparison": "lt",
  "target": "13/10",
  "point": "1309/1250"
 },
 {
  "name": "h(gamma) >= m at 0.655",
  "kind": "point",
  "expression": "h",
  "comparison": "ge",
  "target": "791/2500",
  "point": "131/200"
 },
 {
  "name": "h(13/10) >= m",
  "kind": "point",
  "expression": "h",
  "comparison": "ge",
  "target": "791/2500",
  "point": "13/10"
 },
 {
  "name": "h(gamma) >= m",
  "kind": "concavity-reduction",
  "expression": "h",
  "comparison": "ge",
  "target": "791/2500"
 },
 {
  "name": "h(tau) >= m",
  "kind": "concavity-reduction",
  "expression": "h",
  "comparison": "ge",
  "target": "791/2500"
 },
 {
  "name": "h(t) >= m on [0.655,13/10]",
  "kind": "concavity-reduction",
  "expression": "h",
  "comparison": "ge",
  "target": "791/2500"
 }
]
''')
PRIMITIVE_POINTS = ['131/200', '18/25', '723/1000', '181/250', '73/100', '41/50', '83/100', '17/20', '43/50', '5007/5000', '1309/1250']
