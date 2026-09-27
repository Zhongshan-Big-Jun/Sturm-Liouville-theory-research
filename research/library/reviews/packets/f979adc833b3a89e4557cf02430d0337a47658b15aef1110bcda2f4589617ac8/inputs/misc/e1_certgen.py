"""Generate the 57 exact E1 obligations and fail closed on incomplete evidence.

The retired Decimal programs remain historical files. Decimal displays here
are derived by integer floor/ceiling; exact rational witnesses are authoritative.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import argparse
import hashlib
import json
import sys
import time

from rigid1d import I, D2, d2_sin, d2_cos, d2_atan, I_sin, I_cos, PI
from e1_certificate_io import (SCHEMA, FACT_SPECS, PRIMITIVE_POINTS, require,
    fraction_text, decimal_endpoint, display_interval, exact_interval, predicate,
    source_hashes, atomic_json, validate_ledger)

sys.set_int_max_str_digits(1000000)
GLO, GHI = F(131, 200), F(1309, 1250)
mconst = F(791, 2500)

def comps2(g):
	"""D2-valued quantities (g : D2)."""
	A = PI - g
	sg = d2_sin(g); cg = d2_cos(g)
	D2v = I(1) + 3*sg*sg
	B1 = A*cg - 2*sg
	B2 = 4*A*A*cg*cg - A*A - 12*A*cg*sg + 6*sg*sg
	M  = 2*A*A*cg*cg - A*A - 8*A*cg*sg + 6*sg*sg
	B4 = 7*A*cg*cg - A*sg*sg - 4*cg*sg
	B5 = A*A*cg*cg - A*A*sg*sg + 2*A*A + 12*A*cg*sg - 12*sg*sg
	B7 = 3*A*cg*cg + A*sg*sg + 8*cg*sg
	G5 = B5 - A*B4
	tan = sg/cg
	tmax = d2_atan(2*tan)
	TA_B2 = 4*(-B2)*A*A*sg*sg*cg**4/(D2v*D2v)
	TA_M  = 4*(-M)*A*A*sg*sg*cg**4/(D2v*D2v)
	TC = mconst*G5*A*sg*cg*cg
	TB = 2*A**3*sg*sg*tmax*cg**5/(D2v*D2v*D2v.sqrt())
	z = cg*cg/D2v
	Qlo = 4*A*A*z*z - A*B7*z + 6*cg*cg*sg*sg
	Qhi = 4*A*A*cg**4 - A*B7*cg*cg + 6*cg*cg*sg*sg
	Fv = tmax*tmax*cg*sg*sg
	return dict(A=A, sg=sg, cg=cg, B1=B1, B2=B2, M=M, B4=B4, B5=B5, B7=B7,
				G5=G5, tmax=tmax, TA_B2=TA_B2, TA_M=TA_M, TC=TC, TB=TB,
				Qlo=Qlo, Qhi=Qhi, Fv=Fv)

@lru_cache(maxsize=512)
def _components(lo, hi):
	return comps2(D2(I(lo, hi), I(1), I(0)))


def quantity(Key, g):
	if Key == 'h':
		return g * d2_sin(g) * d2_cos(g)
	return _components(g.v.lo, g.v.hi)[Key]


def _taylor(fn, a, b, Comparison, Target, n, Derivative):
	a, b, Target = F(a), F(b), F(Target)
	require(type(n) is int and n >= 1 and a <= b, 'invalid Taylor partition')
	predicate((F(0), F(0)), Comparison, Target)
	Pieces = []
	w = (b - a) / (2 * n)
	for i in range(n):
		lo, hi = a + (b - a) * i / n, a + (b - a) * (i + 1) / n
		c = (lo + hi) / 2
		fp, fc = fn(D2(I(lo, hi), I(1), I(0))), fn(D2(I(c), I(1), I(0)))
		Center = fc.d1 if Derivative else fc.v
		Slope = fp.d2 if Derivative else fp.d1
		CenterSlope = fc.d2 if Derivative else fc.d1
		M = max(Slope.abs().hi, CenterSlope.abs().hi)
		Correction = M * w
		Bounds = (Center.lo - Correction, Center.hi + Correction)
		Passed, Margin = predicate(Bounds, Comparison, Target)
		CenterKey = 'fpc' if Derivative else 'fvc'
		Piece = dict(cell=[fraction_text(lo), fraction_text(hi)], c=fraction_text(c),
			slope_exact=exact_interval(Slope), slope_center_exact=exact_interval(CenterSlope),
			M_exact=fraction_text(M), M=decimal_endpoint(M, 'upper'),
			corr_exact=fraction_text(Correction), corr=decimal_endpoint(Correction, 'upper'),
			bound_exact=list(map(fraction_text, Bounds)), bound=display_interval(Bounds),
			margin_exact=fraction_text(Margin), margin=decimal_endpoint(Margin, 'lower'), ok=Passed)
		Piece[CenterKey + '_exact'] = exact_interval(Center)
		Piece[CenterKey] = display_interval((Center.lo, Center.hi))
		Pieces.append(Piece)
	return all(Piece['ok'] for Piece in Pieces), Pieces


def taylor_sign(fn, a, b, want_pos, n):
	return _taylor(fn, a, b, 'gt' if want_pos else 'lt', F(0), n, True)


def taylor_value(fn, a, b, want_pos, n, *, target=F(0), comparison=None):
	Comparison = comparison if comparison is not None else ('gt' if want_pos else 'lt')
	return _taylor(fn, a, b, Comparison, target, n, False)


def point_cert(fn, x, cmp, target):
	x, target = F(x), F(target)
	v = fn(D2(I(x), I(1), I(0))).v
	Passed, Margin = predicate((v.lo, v.hi), cmp, target)
	return dict(point=fraction_text(x), val_exact=exact_interval(v), val=display_interval((v.lo, v.hi)),
		target=fraction_text(target), cmp=cmp, ok=Passed,
		margin_exact=fraction_text(Margin), margin=decimal_endpoint(Margin, 'lower'))


def _primitive_rows():
	Rows = []
	for Text in PRIMITIVE_POINTS:
		c = _components(F(Text), F(Text))
		Values = dict(sg=c['sg'].v, cg=c['cg'].v, tau=c['tmax'].v, A=c['A'].v,
			D=(I(1) + 3 * c['sg'].v * c['sg'].v).sqrt())
		Row = dict(point=Text)
		for Key, Value in Values.items():
			Row[Key + '_exact'] = exact_interval(Value)
			Row[Key] = display_interval((Value.lo, Value.hi))
		Rows.append(Row)
	return Rows


def _concavity_proof():
	a, b = F(131, 200), F(13, 10)
	Cells = []
	for i in range(8):
		lo, hi = a + (b - a) * i / 8, a + (b - a) * (i + 1) / 8
		g = D2(I(lo, hi), I(1), I(0))
		Value = quantity('h', g).d2
		Cells.append(dict(cell=[fraction_text(lo), fraction_text(hi)], second_derivative_exact=exact_interval(Value)))
	return dict(domain=[fraction_text(a), fraction_text(b)], formula="h''(t)=2cos(2t)-2t sin(2t)", cells=Cells)


def _evaluate(Spec, Ledger):
	Kind, Key = Spec['kind'], Spec['expression']
	Cmp, Target = Spec['comparison'], F(Spec['target'])
	fn = lambda g: quantity(Key, g)
	if Kind == 'point':
		Detail = point_cert(fn, F(Spec['point']), Cmp, Target)
		return Detail['ok'], Detail
	if Kind in ('value-taylor', 'deriv-taylor'):
		a, b = map(F, Spec['domain'])
		Passed, Pieces = _taylor(fn, a, b, Cmp, Target, Spec['n'], Kind == 'deriv-taylor')
		return Passed, dict(n=Spec['n'], cmp=Cmp, target=Spec['target'], pieces=Pieces)
	if Kind == 'analytic':
		g = I(GLO, GHI)
		A, S, C = PI - g, I_sin(g), I_cos(g)
		Derivative = -3 * C - A * S
		Passed, Margin = predicate((Derivative.lo, Derivative.hi), 'lt', F(0))
		Passed = Passed and min(A.lo, S.lo, C.lo) > 0
		return Passed, dict(formula="B1'=-3cos(gamma)-(pi-gamma)sin(gamma)",
			A_exact=exact_interval(A), sin_exact=exact_interval(S), cos_exact=exact_interval(C),
			bound_exact=exact_interval(Derivative), bound=display_interval((Derivative.lo, Derivative.hi)),
			margin_exact=fraction_text(Margin), margin=decimal_endpoint(Margin, 'lower'), ok=Passed)
	if Kind == 'concavity-reduction':
		Dependencies = ['h(gamma) >= m at 0.655', 'h(13/10) >= m']
		ByName = {Row['name']: Row for Row in Ledger['facts']}
		Concave = all(F(Cell['second_derivative_exact'][1]) < 0 for Cell in Ledger['proofs']['h-concavity']['cells'])
		if Spec['name'] == 'h(gamma) >= m':
			Range = (GLO, GHI)
		elif Spec['name'] == 'h(tau) >= m':
			Range = (F(Ledger['primitives'][0]['tau_exact'][0]), F(Ledger['primitives'][-1]['tau_exact'][1]))
		else:
			Range = (GLO, F(13, 10))
		Branch = F(0) < GLO < GHI < PI.lo / 2
		Passed = Concave and Branch and all(ByName[Name]['ok'] for Name in Dependencies) and GLO <= Range[0] <= Range[1] <= F(13, 10)
		return Passed, dict(proof='h-concavity', dependencies=Dependencies,
			argument_range_exact=list(map(fraction_text, Range)),
			argument_rule='gamma inclusion; tau strictly increasing since 2/(cos^2+4sin^2)>0 on the checked tangent branch; endpoint minimum for concave h')
	raise ValueError('unknown fact kind')


def build_ledger(Ledger):
	Ledger['primitives'] = _primitive_rows()
	Ledger['proofs'] = {'h-concavity': _concavity_proof(), 'pi_exact': exact_interval(PI)}
	for Spec in FACT_SPECS:
		Passed, Detail = _evaluate(Spec, Ledger)
		Row = dict(name=Spec['name'], kind=Spec['kind'], statement=Spec, ok=bool(Passed),
			status='PASS' if Passed else 'NOT_CERTIFIED', detail=Detail)
		Ledger['facts'].append(Row)
		print(Row['status'], Row['name'], flush=True)
		if not Passed:
			return


def main(argv=None):
	Parser = argparse.ArgumentParser(description=__doc__)
	Parser.add_argument('--output', type=Path, default=Path(__file__).resolve().with_name('e1_cert_ledger.json'))
	Args = Parser.parse_args(argv)
	Output = Args.output.resolve()
	StatusPath = Output.with_suffix('.status.json')
	FailedPath = Output.with_suffix('.failed.json')
	Started = time.time()
	Sources = source_hashes()
	atomic_json(StatusPath, dict(status='RUNNING', started_unix=Started, source_sha256=Sources))
	Ledger = dict(schema=SCHEMA, status='RUNNING', meta=dict(title='57 complete E1 obligations', GLO=fraction_text(GLO), GHI=fraction_text(GHI), m=fraction_text(mconst), source_sha256=Sources,
		method='Exact Fraction range envelopes and Taylor bounds; rational endpoints authoritative; integer-directed decimal display.', expected_facts=len(FACT_SPECS)), facts=[], primitives=[], proofs={})
	ExitCode = 2
	try:
		build_ledger(Ledger)
		Passed = sum(Row['ok'] is True for Row in Ledger['facts'])
		Ledger['summary'] = dict(total=len(Ledger['facts']), passed=Passed, failed=len(Ledger['facts']) - Passed, errors=0)
		Complete = len(Ledger['facts']) == len(FACT_SPECS) and Passed == len(FACT_SPECS)
		Ledger['status'] = 'PASS' if Complete else 'NOT_CERTIFIED'
		ExitCode = 0 if Complete else 1
		if Complete:
			validate_ledger(Ledger)
			atomic_json(Output, Ledger)
			Status = dict(status='PASS', ledger_sha256=hashlib.sha256(Output.read_bytes()).hexdigest(), facts=Passed)
		else:
			atomic_json(FailedPath, Ledger)
			Status = dict(status='NOT_CERTIFIED', failure=str(FailedPath), completed_facts=len(Ledger['facts']))
	except Exception as Error:
		Ledger['status'] = 'ERROR'
		Ledger['error'] = dict(type=type(Error).__name__, message=str(Error))
		Ledger['summary'] = dict(total=len(Ledger['facts']), passed=sum(Row['ok'] is True for Row in Ledger['facts']), failed=sum(Row['ok'] is False for Row in Ledger['facts']), errors=1)
		atomic_json(FailedPath, Ledger)
		Status = dict(status='ERROR', failure=str(FailedPath), error=Ledger['error'])
		ExitCode = 2
	Status.update(started_unix=Started, elapsed_seconds=time.time() - Started, source_sha256=Sources)
	atomic_json(StatusPath, Status)
	print(json.dumps(Status, ensure_ascii=False), flush=True)
	return ExitCode


if __name__ == '__main__':
	raise SystemExit(main())
