# -*- coding: utf-8 -*-
# Exact symbolic verification of the diagonal-coefficient lemma in
# candidate_proof.md.  EVIDENCE / reproducibility only; the proof is in the md.
# Tab-indented.
import sympy as sp

t = sp.symbols('t')
u = sp.symbols('u')
x2, x3, x4, x5, x6, x7, x8 = sp.symbols('x2 x3 x4 x5 x6 x7 x8')
xs = [x2, x3, x4, x5, x6, x7, x8]


def coeffs(parity):
	if parity == 'e':
		P = 8 * c * j * j - 4 * c * j + c * c * j / (j - 1)
		Q = 4 * j * (j - 1) * (2 * j - 1) * (2 * j - 3) + 4 * c * j * (2 * j - 3)
		R = 4 * j * (j - 2) * (2 * j - 3) * (2 * j - 5)
	else:
		P = 8 * c * j * j + 4 * c * j + c * c * j / (j - 1)
		Q = 4 * j * (j - 1) * (2 * j - 1) * (2 * j + 1) + 4 * c * j * (2 * j - 1)
		R = 4 * j * (j - 2) * (2 * j - 1) * (2 * j - 3)
	lam = sp.Rational(4) / c
	a1 = P / (c * c * j * j * lam)
	a2 = -Q / (c * c * j * j * (j - 1) * (j - 1) * lam * lam)
	a3 = R / (c * c * j * j * (j - 1) * (j - 1) * (j - 2) * (j - 2) * lam ** 3)
	return sp.cancel(a1), sp.cancel(a2), sp.cancel(a3)


j = sp.symbols('j', positive=True)
c = sp.symbols('c', positive=True)

print('Check A1/A2 expansions used in the diagonal lemma:')
for parity in ('e', 'o'):
	a1, a2, a3 = coeffs(parity)
	A1s = sp.series(a1.subs(j, 1 / t), t, 0, 3).removeO().expand()
	A2s = sp.series(a2.subs(j, 1 / t), t, 0, 3).removeO().expand()
	A3s = sp.series(a3.subs(j, 1 / t), t, 0, 3).removeO().expand()
	print(f'  parity={parity}: A1={A1s}, A2={A2s}, A3={A3s}')

print('\nDiagonal-coefficient formula check, m = 2..8:')
for parity in ('e', 'o'):
	for m in range(2, 9):
		coeffs_list = [1, u] + xs[:m]  # up to x_m
		E = sum(coeffs_list[k] * t ** k for k in range(m + 1))
		# prepare series for all needed shifts
		E1 = sp.series(E.subs(t, t / (1 - t)), t, 0, 10).removeO().expand()
		E2 = sp.series(E.subs(t, t / (1 - 2 * t)), t, 0, 10).removeO().expand()
		a1, a2, a3 = coeffs(parity)
		A1s = sp.series(a1.subs(j, 1 / t), t, 0, 10).removeO().expand()
		A2s = sp.series(a2.subs(j, 1 / t), t, 0, 10).removeO().expand()
		A3s = sp.series(a3.subs(j, 1 / t), t, 0, 10).removeO().expand()
		G = sp.expand(E * E1 * E2 - (A1s * E1 * E2 + A2s * E2 + A3s))
		coeff_m1 = sp.expand(G.coeff(t, m + 1))
		d_m = sp.simplify(sp.diff(coeff_m1, xs[m - 2]))
		d_next = sp.simplify(sp.diff(coeff_m1, xs[m - 1])) if m < len(xs) else sp.Integer(0)
		pred = 2 * u - (m - 1) if parity == 'e' else 2 * u - (m + 1)
		ok = sp.simplify(d_m - pred) == 0
		print(f'  parity={parity} m={m}: d/dx_m={d_m}, predicted={pred}, ok={ok}, d/dx_(m+1)={d_next}')
		if not ok:
			raise SystemExit('FAIL')
print('\nAll diagonal-coefficient checks PASS.')

print('\nKnown family expansions:')
t = sp.symbols('t')
tau = sp.symbols('tau')
for p, expr in [
	('even E^(tau)', (1 - sp.Rational(1, 2) / j) * (j + tau + 1) / (j + tau)),
	('odd  E^(tau)', (1 + sp.Rational(1, 2) / j) * (j + tau + 1) / (j + tau)),
]:
	print(p, '=', sp.series(expr.subs(j, 1 / t), t, 0, 6))
