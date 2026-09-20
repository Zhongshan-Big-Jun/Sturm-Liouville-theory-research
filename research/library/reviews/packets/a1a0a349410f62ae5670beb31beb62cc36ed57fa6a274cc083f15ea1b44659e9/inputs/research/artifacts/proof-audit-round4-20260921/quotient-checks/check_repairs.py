#!/usr/bin/env python3
"""Finite exact regression checks; no claim of independent/universal proof."""

from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import sys
import time

import sympy as sp


Scratch = Path(__file__).resolve().parent
Root = Path('/mnt/f/LaTeX/BVE research')
Source = Root / 'docs/SL_krein_c0_limit.tex'
X, T = sp.symbols('x t', real=True)
Results = []
Start = time.monotonic()


def check(Category, Name, Condition, Detail=None):
	Row = {'category': Category, 'name': Name, 'passed': bool(Condition)}
	if(Detail is not None):
		Row['detail'] = str(Detail)
	Results.append(Row)
	if(not Row['passed']):
		print('FAIL:', Category, Name, Detail, flush=True)


def equal(Left, Right):
	return sp.cancel(sp.expand(Left - Right)) == 0


def integral(Polynomial):
	return sp.expand(sum(
		Coefficient * sp.Rational(2, Power[0] + 1)
		for Power, Coefficient in sp.Poly(sp.expand(Polynomial), X).terms()
		if(Power[0] % 2 == 0)
	))


def l2_form(Left, Right):
	return integral(Left * Right)


def zero_form(Left, Right):
	return sp.expand(
		integral(sp.diff(Left, X) * sp.diff(Right, X))
		- (Left.subs(X, 1) - Left.subs(X, -1))
		* (Right.subs(X, 1) - Right.subs(X, -1)) / 2
	)


def sobolev_form(Left, Right):
	return l2_form(Left, Right) + integral(sp.diff(Left, X) * sp.diff(Right, X))


def shifted_form(Left, Right):
	return zero_form(Left, Right) + l2_form(Left, Right) / T


def parity_data(N):
	Epsilon = N % 2
	M = (N - Epsilon) // 2
	return M - 1, sp.prod(4 * (2 * J + Epsilon) ** 2 - 1 for J in range(1, M))


P = [sp.legendre(N, X) for N in range(25)]
S = P[:2] + [sp.expand(P[N] - P[N - 2]) for N in range(2, 25)]
A = [sp.Integer(1)] * 4
for N in range(2, 23):
	A.append(sp.expand(
		(1 + (4 * N ** 2 - 1) * T) * A[N]
		+ sp.Rational(2 * N + 1, 2 * N - 3) * (A[N] - A[N - 2])
	))
K = P[:2]
for N in range(2, 17):
	K.append(sp.expand(A[N] * S[N] + K[N - 2]))

for N in range(2, 15):
	check('Legendre', f'endpoints n={N}', S[N].subs(X, 1) == S[N].subs(X, -1) == 0)
	check('Legendre', f'derivative n={N}', equal(sp.diff(S[N], X), (2 * N - 1) * P[N - 1]))
for N in range(2, 13):
	for M in range(2, N + 1):
		check('zero Gram', f'n={N},m={M}', equal(zero_form(S[N], S[M]), 2 * (2 * N - 1) if(M == N) else 0))

for N in range(2, 25):
	R, Leading = parity_data(N)
	Polynomial = sp.Poly(A[N], T)
	check('parity asymptotics', f'n={N}', Polynomial.degree() == R and Polynomial.LC() == Leading,
		f'r={R}, C={Leading}')
for N in range(2, 23):
	B = sp.Rational(2 * N + 1, 2 * N - 3)
	Delta = sp.expand(A[N] - A[N - 2])
	Remainder = sp.expand(A[N + 2] - (4 * N ** 2 - 1) * T * A[N])
	check('recurrence remainder', f'difference and bounds n={N}',
		equal(Remainder, A[N] + B * Delta)
		and all(Coefficient >= 0 for Coefficient in sp.Poly(Delta, T).all_coeffs())
		and all(Coefficient >= 0 for Coefficient in sp.Poly(A[N - 2], T).all_coeffs()),
		'Finite coefficient check implies a_n <= R_n <= (1+b_n)a_n for t>0 at this n')

for N in range(0, 11):
	for M in range(0, N + 1):
		Expected = 2 * A[N] * A[N + 2] / (T * (2 * N + 1)) if(M == N) else 0
		check('direct shifted form', f'n={N},m={M}', equal(shifted_form(K[N], K[M]), Expected))

for N in range(2, 17):
	R, Leading = parity_data(N)
	LeadingK = sp.Poly(K[N], T).nth(R)
	Expected = Leading * (P[N] if(N < 4) else S[N])
	check('representative leading polynomial', f'n={N}', equal(LeadingK, Expected))
	NormTimesT = sp.Poly(2 * A[N] * A[N + 2] / (2 * N + 1), T)
	check('norm leading constant', f'n={N}',
		NormTimesT.degree() - 1 == 2 * R
		and NormTimesT.LC() == 2 * (2 * N - 1) * Leading ** 2)
	if(N >= 4):
		check('H1 polynomial remainder order', f'n={N}', sp.Poly(K[N - 2], T).degree() <= R - 1)

for N, Expected in [(2, sp.Rational(1, 3)), (3, sp.Rational(4, 15))]:
	Difference = (P[N] - S[N]) / sp.sqrt(2 * (2 * N - 1))
	check('low representative counterexample', f'H1 discrepancy n={N}', equal(sobolev_form(Difference, Difference), Expected), Expected)
	check('low quotient agreement', f'n={N}', equal(zero_form(Difference, Difference), 0))

Norm4 = sp.cancel(shifted_form(K[4], K[4]))
Norm4Expected = 3150 * T ** 2 + 560 * T + sp.Rational(80, 3) + 2 / (9 * T)
check('explicit n=4', 'exact squared norm', equal(Norm4, Norm4Expected), Norm4)
Value = Norm4.subs(T, 1000)
check('explicit n=4', 'c=1/1000 exact value', Value == 3150560026 + sp.Rational(3001, 4500), Value)
BadRemainder = sp.expand(A[6] - 63 * T * A[4])
check('negative control', 'old O(1) remainder diverges', BadRemainder == 1 + 42 * T, BadRemainder)
ProjectionGap = sp.expand(Norm4 - 14 * A[4] ** 2)
check('negative control', 'old projection coefficient not exact', equal(ProjectionGap, 140 * T + sp.Rational(38, 3) + 2 / (9 * T)), ProjectionGap)
check('projection residual', 'n=4 quotient numerator', equal(zero_form(K[4] - A[4] * S[4], K[4] - A[4] * S[4]), 6))

for N in [5, 8, 11]:
	Target = sum(sp.Rational((-1) ** J * (J + 3), J + 1) * X ** J for J in range(N + 1))
	Residual = Target
	for J in range(N, 1, -1):
		Coefficient = sp.Poly(Residual, X).nth(J) / sp.Poly(S[J], X).LC()
		Residual = sp.expand(Residual - Coefficient * S[J])
	check('polynomial spanning', f'degree {N}', sp.degree(Residual, X) <= 1, Residual)
for F in [X ** 2, S[4], S[7]]:
	check('radical', str(F), equal(zero_form(sp.Integer(1), F), 0) and equal(zero_form(X, F), 0))

OldBytes = (Scratch / 'SL_krein_c0_limit.before.tex').read_bytes()
NewBytes = Source.read_bytes()
Old = OldBytes.decode('utf-8-sig')
New = NewBytes.decode('utf-8-sig')


def fragment(Text, Begin, End=None):
	StartIndex = Text.index(Begin)
	return Text[StartIndex:Text.index(End, StartIndex)] if(End) else Text[StartIndex:]


Preserved = {
	'preamble': Old.split('\\begin{abstract}')[0] == New.split('\\begin{abstract}')[0],
	'setting through complete third-round quotient proof':
		fragment(Old, r'\section{Setting}', r'\section{Structural stability')
		== fragment(New, r'\section{Setting}', r'\begin{lemma}[explicit orthonormal representatives]'),
	'defining recurrence and norm':
		fragment(Old, r'\section{Structural stability', r'\begin{theorem}[degeneration')
		== fragment(New, r'\section{Structural stability', r'\begin{theorem}[degeneration'),
	'low-mode theorem and proof':
		fragment(Old, r'\begin{theorem}[degeneration', r'\begin{theorem}[divergence')
		== fragment(New, r'\begin{theorem}[degeneration', r'\begin{theorem}[fixed-index asymptotics'),
	'spectral interpretation':
		fragment(Old, r'\begin{remark}[spectral interpretation]', r'\section{Numerical audit}')
		== fragment(New, r'\begin{remark}[spectral interpretation]', r'\section{Exact checks'),
	'glossary bibliography and EOF': fragment(Old, r'\section{Mathematics involved}') == fragment(New, r'\section{Mathematics involved}'),
	'UTF8 BOM': OldBytes.startswith(b'\xef\xbb\xbf') and NewBytes.startswith(b'\xef\xbb\xbf'),
	'LF line endings': b'\r' not in OldBytes and b'\r' not in NewBytes,
	'trailing newlines': len(OldBytes) - len(OldBytes.rstrip(b'\n')) == len(NewBytes) - len(NewBytes.rstrip(b'\n')),
}
for Name, Passed in Preserved.items():
	check('source preservation', Name, Passed)

Labels = re.findall(r'\\label\{([^}]+)\}', New)
Refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', New)
check('TeX structure', 'unique labels', len(Labels) == len(set(Labels)))
check('TeX structure', 'resolved local references', not (set(Refs) - set(Labels)), sorted(set(Refs) - set(Labels)))
Stack = []
EnvironmentErrors = []
for Kind, Name in re.findall(r'\\(begin|end)\{([^}]+)\}', New):
	if(Kind == 'begin'):
		Stack.append(Name)
	elif(not Stack or Stack.pop() != Name):
		EnvironmentErrors.append(Name)
check('TeX structure', 'balanced environments', not Stack and not EnvironmentErrors)
BraceDepth = 0
BraceErrors = []
for Match in re.finditer(r'(?<!\\)[{}]', New):
	BraceDepth += 1 if(Match.group() == '{') else -1
	if(BraceDepth < 0):
		BraceErrors.append(Match.start())
check('TeX structure', 'balanced braces', BraceDepth == 0 and not BraceErrors)
check('TeX structure', 'balanced inline math delimiters', len(re.findall(r'(?<!\\)\$', New)) % 2 == 0)

Counts = Counter(Row['category'] for Row in Results)
Failures = [Row for Row in Results if(not Row['passed'])]
Report = {
	'role': 'AUTHOR',
	'status': 'PASS' if(not Failures) else 'FAIL',
	'scope': 'Finite symbolic/rational regression and source-structure checks; not independent acceptance or a universal proof.',
	'python': sys.version,
	'sympy': sp.__version__,
	'tests': len(Results),
	'failed': len(Failures),
	'counts': dict(Counts),
	'source_sha256': hashlib.sha256(NewBytes).hexdigest(),
	'test_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
	'elapsed_seconds': round(time.monotonic() - Start, 3),
	'results': Results,
}
(Scratch / 'check_results.json').write_text(json.dumps(Report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({Key: Value for Key, Value in Report.items() if(Key != 'results')}, indent=2))
if(Failures):
	raise SystemExit(1)
