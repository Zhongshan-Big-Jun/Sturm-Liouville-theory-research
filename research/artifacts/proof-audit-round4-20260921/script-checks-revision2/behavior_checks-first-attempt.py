"""Behavior tests against independently computed finite recurrence solutions."""
from pathlib import Path
from fractions import Fraction as F
import contextlib
import importlib.util
import io
import json
import math
import os
import subprocess
import sys
import mpmath as mp

Root = Path(os.environ.get('AUDIT_SOURCE_ROOT', '/mnt/f/LaTeX/BVE research'))
Source = Root / 'scripts/d4_third_order_theory.py'
Spec = importlib.util.spec_from_file_location('d4_under_test', Source)
Module = importlib.util.module_from_spec(Spec)
Capture = io.StringIO()
with contextlib.redirect_stdout(Capture), contextlib.redirect_stderr(Capture):
	Spec.loader.exec_module(Module)
Checks = []


def record(Name, Condition, Detail):
	if not Condition:
		raise AssertionError(Name + ': ' + str(Detail))
	Checks.append({'name': Name, 'status': 'PASS', 'detail': Detail})


def must_reject(Name, Action):
	try:
		Action()
	except (ValueError, ArithmeticError):
		record(Name, True, 'explicit rejection')
	else:
		raise AssertionError(Name + ': unexpectedly accepted')


def exact_backward(Epsilon, C, N):
	Values = [F(0)] * (N + 3)
	Values[N] = F(1)
	for J in range(N + 2, 2, -1):
		P = 4*C*J*(2*J+2*Epsilon-1) + C*C*F(J,J-1)
		Q = 4*J*(J-1)*(2*J+2*Epsilon-1)*(2*J+2*Epsilon-3) + 4*C*J*(2*J+2*Epsilon-3)
		R = 4*J*(J-2)*(2*J+2*Epsilon-3)*(2*J+2*Epsilon-5)
		Values[J-3] = (C*C*Values[J] - P*Values[J-1] + Q*Values[J-2])/R
	Z = [Values[J] / (F(math.factorial(J)**2) * (4/C)**J) for J in range(N+1)]
	return [Value/Z[0] for Value in Z]


record('quiet import', Capture.getvalue() == '', 'No diagnostic execution or output on import')
record('fractional closed form retained', Module.even_form2(3, 3) == F(80,3), '80/3, not floor 26')
Forms = [('e', Module.even_form1), ('e', Module.even_form2), ('o', Module.odd_form1), ('o', Module.odd_form2)]
for Parity, Form in Forms:
	Broken = lambda J,C: Form(J,C).__floor__()
	Passed, Index = Module.check_mu_form(Parity, Broken, 3)
	record('floor negative control '+Form.__name__, not Passed and Index == 3, {'first_failure':Index})
# Independent review R4-d4-current-01: c=64,j=3, positive E=(1+5j)H_j.
A, B = Module.reduction_coefficients(F(-37,8),1,5,3,1)
record('mixed integer and Fraction reduction coefficients', (A,B)==(F(103,40),F(-1,5)) and isinstance(B,F), 'exact (103/40,-1/5), no binary float')
record('valid c64 positive-baseline identity', A*0+B*1==F(-1,5), 'z=(0,3,33/8,4), s=(1,0,-1/5)')
record('integer coefficient helper remains rational', Module.coefficients('e',4,3)[0]==F(96) and isinstance(Module.coefficients('e',4,3)[0],F), 'P4=96 with integer inputs')
SA2,SA3,SE0,SE2,SE3=Module.sp.symbols('A2 A3 E0 E2 E3', nonzero=True)
SA,SB=Module.reduction_coefficients(SA2,SA3,SE0,SE2,SE3)
record('symbolic reduction retained', Module.sp.simplify(SA+(SA2*SE2+SA3*SE3)/SE0)==0 and Module.sp.simplify(SB+SA3*SE3/SE0)==0, 'both exact symbolic identities')
Count = 0
with mp.workdps(100):
	for Epsilon, Parity in enumerate(('e','o')):
		for C in (F(1,100),F(1,4),F(1),F(3),F(10),F(1000)):
			for N in (0,1,2,3,7,12,20):
				Expected = exact_backward(Epsilon,C,N)
				Actual = Module.minimal_solution(Parity,C,N=N,Precision=100)
				for A,B in zip(Actual,Expected,strict=True):
					Exact = mp.mpf(B.numerator)/B.denominator
					if abs(A/Exact-1) > mp.mpf('1e-90'):
						raise AssertionError((Parity,str(C),N,mp.nstr(A/Exact-1)))
					Count += 1
record('positive-difference implementation versus independent exact mu backward recurrence', True, {'entries':Count,'shifts':['1/100','1/4','1','3','10','1000'],'N':[0,1,2,3,7,12,20]})
for Parity in ('e','o'):
	Values=Module.minimal_solution(Parity,3,N=2000)
	record('large finite backward '+Parity, len(Values)==2001 and Values[0]==1 and all(mp.isfinite(V) and V>0 for V in Values), 'N=2000, positive finite arbitrary-exponent values including terminal')
must_reject('invalid parity',lambda:Module.minimal_solution('x',3))
must_reject('zero shift',lambda:Module.even_form1(3,0))
must_reject('negative shift',lambda:Module.check_s_recurrence('e',-1))
must_reject('negative index',lambda:Module.odd_form2(-1,3))
must_reject('too short validation range',lambda:Module.check_mu_form('e',Module.even_form1,3,N=2))
must_reject('zero baseline division',lambda:Module.reduction_coefficients(F(2),F(3),F(0),F(1),F(1)))

Imports = 'import importlib.util; S=importlib.util.spec_from_file_location("d4",'+repr(str(Source))+'); M=importlib.util.module_from_spec(S); S.loader.exec_module(M); '
Injected = [
	('floor-return', 'Original=M.even_form1; M.even_form1=lambda J,C: Original(J,C).__floor__(); '),
	('ratio-identity', 'M.z_residual_poly=lambda *Args: M.sp.Integer(1); '),
	('reduction', 'M.check_s_recurrence=lambda *Args: False; '),
	('nan-numerical', 'M.minimal_solution=lambda *Args: [M.mp.nan]*2001; ')
]
Runs=[]
for Optimized in (False,True):
	for Label, Injection in Injected:
		Args=[sys.executable]+(['-O'] if Optimized else [])+['-c',Imports+Injection+'raise SystemExit(M.main())']
		Result=subprocess.run(Args,capture_output=True,text=True,timeout=90)
		record('nonzero failure '+Label+(' optimized' if Optimized else ''),Result.returncode!=0,{'exit_code':Result.returncode})
		Runs.append({'case':Label,'optimized':Optimized,'argv':Args,'exit_code':Result.returncode,'stdout':Result.stdout,'stderr':Result.stderr})
Out=Path(os.environ.get('AUDIT_CHECK_OUTPUT', str(Path(__file__).parent/'behavior-results.json')))
Out.write_text(json.dumps({'status':'PASS','checks':len(Checks),'results':Checks,'failure_runs':Runs},indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(Checks),'independent_finite_entries':Count,'failure_exit_controls':len(Runs)}))
