#!/usr/bin/env python3
"""Exact local checks of the R6 author repair. Not an infinite-dimensional proof."""
import hashlib
import json
import platform
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp

Project = Path('/mnt/f/LaTeX/BVE research')
Work = Path(__file__).resolve().parent
Source = Project / 'docs/SL_projection_moment_repairs.tex'
Groups = []
x = sp.Symbol('x')


def require(Condition, Message):
	if(not Condition):
		raise RuntimeError(Message)


def zero(Value):
	return sp.simplify(Value) == 0


def record(Name, Kind, Cases, Scope, **Details):
	Groups.append(dict(name=Name, kind=Kind, cases=Cases, scope=Scope, **Details))


def sparse_poly(n):
	if(n in (0, 1)):
		return x**n
	require(n >= 4, 'p_2 and p_3 are undefined')
	m = n // 2
	return x**n - sp.Rational(m, m - 1) * x**(n - 2)


def pair(f, g, Beta=0):
	F = sp.Poly(f, x)
	G = sp.Poly(g, x)
	Degree = max(F.degree(), G.degree(), 0)
	return sp.expand(sum(F.nth(k) * sp.conjugate(G.nth(k)) * (k + 1)**(2 * Beta)
		for k in range(int(Degree) + 1)))


def algebraic_moment(f, Parity):
	F = sp.Poly(f, x)
	return sum((k // 2) * F.nth(k) for k in range(2 + Parity, int(F.degree()) + 1, 2))


def input_and_source_checks():
	Manifest = json.loads((Work / 'input_manifest.json').read_text(encoding='utf-8'))
	for Entry in Manifest['inputs']:
		Digest = hashlib.sha256((Project / Entry['path']).read_bytes()).hexdigest()
		require(Digest == Entry['sha256'], 'input changed: ' + Entry['path'])
	record('frozen_input_bytes', 'byte_identity', len(Manifest['inputs']),
		'Only the nine declared inputs; not a whole-repository integrity audit.')
	Text = Source.read_text(encoding='utf-8')
	Clean = '\n'.join(re.split(r'(?<!\\)%', Line)[0] for Line in Text.splitlines())
	Stack = []
	for Match in re.finditer(r'\\(begin|end)\{([^}]+)\}', Clean):
		Action, Name = Match.groups()
		if(Action == 'begin'):
			Stack.append(Name)
		else:
			require(bool(Stack) and Stack.pop() == Name, 'unbalanced environment ' + Name)
	require(not Stack, 'unclosed TeX environment')
	Depth = 0
	for Index, Char in enumerate(Clean):
		if(Char not in '{}'):
			continue
		Backslashes = 0
		Previous = Index - 1
		while(Previous >= 0 and Clean[Previous] == '\\'):
			Backslashes += 1
			Previous -= 1
		if(Backslashes % 2):
			continue
		Depth += 1 if Char == '{' else -1
		require(Depth >= 0, 'unbalanced TeX closing brace')
	require(Depth == 0, 'unbalanced TeX opening brace')
	Labels = re.findall(r'\\label\{([^}]+)\}', Clean)
	Refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', Clean)
	require(len(Labels) == len(set(Labels)), 'duplicate label')
	require(set(Refs) <= set(Labels), 'undefined TeX reference')
	record('tex_structure_only', 'static', 3,
		'Balanced environments/braces and defined references. No TeX compiler or PDF layout check.',
		labels=len(Labels), references=len(Refs))


def algebra_checks():
	for m in range(1, 25):
		for Parity in (0, 1):
			Rhs = m * x**(2 + Parity) + sum(sp.Rational(m, j) * sparse_poly(2 * j + Parity)
				for j in range(2, m + 1))
			require(zero(x**(2 * m + Parity) - Rhs), 'monomial reconstruction')
	record('sparse_reconstruction', 'finite_exact', 48, 'Both parities, 1 <= m <= 24; general proof is in TeX.')
	for n in [0, 1] + list(range(4, 81)):
		for Parity in (0, 1):
			require(zero(algebraic_moment(sparse_poly(n), Parity)), 'algebraic quotient functional')
	Quotient = sp.Matrix([[algebraic_moment(x**k, Parity) for k in (2, 3)] for Parity in (0, 1)])
	require(Quotient == sp.eye(2), 'missing-direction quotient matrix')
	record('two_missing_directions', 'finite_exact', 159, 'All sparse n <= 80 and the x^2,x^3 quotient matrix.', matrix=str(Quotient))


def beta_two_checks():
	K = 24
	w = sum(sp.Rational(m, (2 * m + 1)**4) * x**(2 * m) for m in range(1, K + 1))
	for m in range(1, K + 1):
		require(pair(w, x**(2 * m), 2) == m, 'beta=2 even moment')
		require(pair(w, x**(2 * m + 1), 2) == 0, 'beta=2 odd moment')
	for n in [0, 1] + list(range(4, 2 * K + 2)):
		require(pair(w, sparse_poly(n), 2) == 0, 'truncated witness interior test')
	require(pair(w, 1, 2) == 0 and pair(w, x**2, 2) == 1, 'V membership or nonzero witness')
	require(pair(w, sparse_poly(2 * K + 2), 2) == -(K + 1), 'truncation boundary negative control')
	record('beta2_realized_witness_local_arithmetic', 'finite_exact_with_negative_control', 98,
		'K=24 polynomial truncation: 48 coordinate moments, 48 sparse tests, membership/nonzero, and one boundary control. Infinite convergence is proved only in TeX.',
		cutoff=K, next_even_test=-(K + 1))
	m = sp.Symbol('m', positive=True, integer=True)
	require(zero(m - m / (m - 1) * (m - 1)), 'symbolic witness recurrence')
	Difference = sp.expand((2 * m + 1)**4 - 16 * m**4)
	require(Difference == 32 * m**3 + 24 * m**2 + 8 * m + 1, 'norm bound polynomial')
	record('beta2_recurrence_and_norm_bound', 'symbolic_identity', 2,
		'Positive-coefficient denominator difference and recurrence identity; convergence uses the analytic comparison in TeX.',
		denominator_difference=str(Difference))
	for n in [0, 1] + list(range(4, 31)):
		p = sparse_poly(n)
		Constant = sp.Poly(p, x).nth(0)
		require((Constant != 0) == (n == 0), 'actual retained set')
		require(zero(p - Constant - (0 if n == 0 else p)), 'orthogonal projection')
	record('beta2_actual_retained_set', 'finite_exact', 29,
		'n <= 30 projection deletes constant coefficient; only p_0 is excluded in these exact samples.')


def first_moment_checks():
	for m0 in range(2, 10):
		L = 2 * m0 - 2
		for Parity, Seed in ((0, 2 + 3 * sp.I), (1, -1 + 2 * sp.I)):
			Value = Seed
			for m in range(m0, m0 + 13):
				Value *= sp.Rational(m, m - 1)
				require(zero(Value - sp.Rational(m, m0 - 1) * Seed), 'tail base index')
			require(pair(x**(L + Parity), sparse_poly(2 * m0 + Parity)) == -sp.Rational(m0, m0 - 1),
				'wrong L=2m0 must be rejected')
	record('tail_indices_and_initial_values', 'finite_exact_with_negative_control', 224,
		'm0=2..9, both parities, 13 steps each; 16 controls reject L=2m0 by a nonzero first-tail pairing.')
	Ranks = []
	for m0 in range(2, 7):
		for r in range(9):
			Vectors = [sparse_poly(2 * (m0 + j)) for j in range(r + 3)]
			Tests = [x**(2 * (m0 + i)) for i in range(r)] + [x**2, x**3]
			Matrix = sp.Matrix([[pair(u, t) for u in Vectors] for t in Tests])
			Kernel = Matrix.nullspace()
			require(Matrix.rank() <= r + 2 and len(Kernel) >= 1, 'rank kernel dimension')
			Witness = sp.expand(sum(Kernel[0][j] * Vectors[j] for j in range(r + 3)))
			require(Witness != 0 and all(zero(pair(Witness, t)) for t in Tests), 'rank kernel witness')
			Ranks.append(dict(m0=m0, r=r, rank=Matrix.rank(), nullity=len(Kernel)))
	record('F_rank_obstruction_instances', 'finite_exact', 45,
		'Actual polynomials in H_diag_0, m0=2..6 and r=0..8. Arbitrary-r proof is rank-nullity in TeX.',
		instances=Ranks)
	Positive = sp.Matrix([[pair(x, sparse_poly(1))]])
	Whole = sp.Matrix([[pair(z, sparse_poly(n)) for z in (1, x)] for n in (0, 1)])
	require(Positive == sp.ones(1) and Whole == sp.eye(2), 'nonvacuous finite test matrices')
	record('nonvacuous_beta0_examples', 'finite_exact', 2,
		'V=ker M0 and V=H, m0=2. Infinite-tail annihilator equality is the analytic theorem.',
		matrices=[str(Positive), str(Whole)])
	J = [n for n in [0, 1, 4, 5, 6, 7] if pair(sparse_poly(n), x**4) == 0]
	Basis = [1, x, x**2, x**3, x**5]
	Matrix = sp.Matrix([[pair(z, sparse_poly(n)) for z in Basis] for n in J])
	require(J == [0, 1, 5, 7] and Matrix.rank() == 4, 'actual low-index defect')
	require(Matrix * sp.Matrix([0, 0, 1, 0, 0]) == sp.zeros(4, 1), 'x^2 low-index defect')
	record('actual_low_index_failure', 'finite_exact', 1,
		'V=ker M4, m0=4, L=6: retained low tests have a one-dimensional defect.',
		retained=J, matrix=str(Matrix), rank=4)


def triangular_checks():
	for N in (0, 1, 2, 4, 6):
		K = N + 4
		Tail = [sum(((n - k + 1) + sp.I * (k + 1)) * x**k for k in range(n))
			+ ((n + 1) + sp.I) * x**n for n in range(N, K + 1)]
		Polys = [x**k for k in range(N)] + Tail
		Matrix = sp.Matrix([[sp.Poly(f, x).nth(k) for f in Polys] for k in range(K + 1)])
		Expected = sp.prod((n + 1) + sp.I for n in range(N, K + 1))
		require(zero(Matrix.det() - Expected), 'triangular reconstruction determinant')
		Tests = sp.Matrix([[sp.conjugate(sp.Poly(q, x).nth(k)) for k in range(K + 1)] for q in Tail])
		Kernel = Tests.nullspace()
		require(len(Kernel) == N, 'finite triangular tail nullity')
		if(N):
			Initial = sp.Matrix.hstack(*Kernel)[:N, :]
			require(Initial.rank() == N, 'initial moments injective on finite tail kernel')
	record('triangular_reconstruction_complex_coefficients', 'finite_exact', 5,
		'N=0,1,2,4,6 with K=N+4. Determinants and truncated annihilators only; infinite dim<=N uses reconstruction in TeX.')
	Coeffs = [3 * sp.I, 2 - sp.I, 1 + sp.I]
	Initial = [1 - 2 * sp.I, 2 + sp.I]
	Correct = -sum(sp.conjugate(Coeffs[k]) * Initial[k] for k in range(2)) / sp.conjugate(Coeffs[2])
	Wrong = -sum(Coeffs[k] * Initial[k] for k in range(2)) / Coeffs[2]
	Residual = lambda Last: sp.simplify(sum(sp.conjugate(Coeffs[k]) * (Initial + [Last])[k] for k in range(3)))
	require(Residual(Correct) == 0 and Residual(Wrong) != 0, 'complex conjugation control')
	record('triangular_moment_conjugation', 'symbolic_identity_with_negative_control', 2,
		'First-variable-linear inner product: correct conjugates give zero; omitted conjugates fail.',
		wrong_formula_residual=str(Residual(Wrong)))
	m = sp.Symbol('m', integer=True, nonnegative=True)
	Decay = lambda j: sp.Rational(1, 2)**j
	Normalized = lambda j: (2**j - sp.Rational(1, 2)**j) / sp.Rational(3, 2)
	for f in (Decay, Normalized):
		require(zero(f(m) - sp.Rational(5, 2) * f(m - 1) + f(m - 2)), 'growth recurrence solution')
	require(Normalized(0) == 0 and Normalized(1) == 1 and Decay(0) == 1, 'growth initial data')
	Norm = sp.summation(sp.Rational(1, 4)**m, (m, 0, sp.oo))
	require(Norm == sp.Rational(4, 3), 'realized decaying solution norm')
	record('growth_initial_data_counterexample', 'symbolic_identity', 4,
		'Two recurrence solutions, distinct initial data, and exact geometric norm 4/3. No universal growth claim.',
		norm_squared=str(Norm))


def representer_checks():
	v, w = x**2 + x**3, x**2 - x**3
	require(pair(v, x**2) == pair(v, x**3) == 1, 'nonzero detection')
	require(pair(w, v) == 0 and pair(w, x**2) == 1 and pair(w, x**3) == -1, 'separate moments not killed')
	require(pair(w, w) == 2, 'nonzero representer counterexample')
	record('representer_detection_counterexample', 'finite_exact', 3,
		'Exact x^2+x^3 / x^2-x^3 witness in H_diag_0.')
	V = [x**2 + sp.I * x**3, (1 + sp.I) * x**2 + x**3]
	Matrix = sp.Matrix([[sp.Poly(v, x).nth(k) for v in V] for k in (2, 3)])
	w = (2 + 3 * sp.I) * x**2 + (1 - sp.I) * x**3
	for Column, k in enumerate((2, 3)):
		Target = sp.eye(2)[:, Column]
		Coefficients = Matrix.inv() * Target
		require(zero(sum(Coefficients[j] * V[j] for j in range(2)) - x**k), 'representer vector inclusion')
		Rhs = sum(sp.conjugate(Coefficients[j]) * pair(w, V[j]) for j in range(2))
		require(zero(Rhs - pair(w, x**k)), 'representer functional conjugation')
	record('representer_inclusion_conjugation', 'finite_exact', 2,
		'Complex coefficient representations of x^2 and x^3 and the conjugated functional coefficients.')


def main():
	Report = dict(role='AUTHOR', independent_review=False,
		started_at_utc=datetime.now(timezone.utc).isoformat(),
		python=platform.python_version(), executable=sys.executable, sympy=sp.__version__,
		source=str(Source), source_sha256=hashlib.sha256(Source.read_bytes()).hexdigest(),
		script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), groups=Groups,
		limits=['No PDF build or TeX engine execution.', 'No Lean or old repository program execution.',
			'Finite arithmetic and symbolic identities do not certify the Hilbert-space proofs.',
			'No independent stateless review; no other historical branch is certified.'])
	ExitCode = 0
	try:
		input_and_source_checks()
		algebra_checks()
		beta_two_checks()
		first_moment_checks()
		triangular_checks()
		representer_checks()
		Report['status'] = 'CHECKS_COMPLETED'
	except Exception:
		ExitCode = 1
		Report['status'] = 'CHECK_FAILED'
		Report['failure'] = traceback.format_exc()
	Report['completed_groups'] = len(Groups)
	Report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
	print(json.dumps(Report, ensure_ascii=False, indent=2))
	return ExitCode


if(__name__ == '__main__'):
	sys.exit(main())
