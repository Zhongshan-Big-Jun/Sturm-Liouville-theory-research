# -*- coding: utf-8 -*-
# Verify the key asymptotic facts used in the no-go proof for higher-degree
# rational product solutions (root-1 branch).
# Tab-indented, exact symbolic (sympy) computations.  EVIDENCE only; the proof
# itself is in candidate_proof.md.
import sympy as sp

j, c, t = sp.symbols('j c t', positive=True)
tau = sp.symbols('tau')


def a_coeffs(parity):
	if parity == 'e':
		P = 8*c*j*j - 4*c*j + c*c*j/(j-1)
		Q = 4*j*(j-1)*(2*j-1)*(2*j-3) + 4*c*j*(2*j-3)
		R = 4*j*(j-2)*(2*j-3)*(2*j-5)
	else:
		P = 8*c*j*j + 4*c*j + c*c*j/(j-1)
		Q = 4*j*(j-1)*(2*j-1)*(2*j+1) + 4*c*j*(2*j-1)
		R = 4*j*(j-2)*(2*j-1)*(2*j-3)
	lam = sp.Rational(4)/c
	a1 = P/(c*c*j*j*lam)
	a2 = -Q/(c*c*j*j*(j-1)**2*lam**2)
	a3 = R/(c*c*j*j*(j-1)**2*(j-2)**2*lam**3)
	return sp.cancel(a1), sp.cancel(a2), sp.cancel(a3)


def base_ratio(parity, branch):
	if parity == 'e':
		if branch == 'free':
			return lambda x: (1 - sp.Rational(1, 2)/x)*(x+tau+1)/(x+tau)
		else:
			return lambda x: 1 - sp.Rational(1, 2)/x
	else:
		if branch == 'free':
			return lambda x: (1 + sp.Rational(1, 2)/x)*(x+tau+1)/(x+tau)
		else:
			return lambda x: 1 + sp.Rational(1, 2)/x


def f1(parity, branch):
	a1, a2, a3 = a_coeffs(parity)
	e = base_ratio(parity, branch)
	e1 = e(1/t - 1)
	e2 = e(1/t - 2)
	Fx = -a2/e1**2 - a3/(e1**2*e2)
	ser = sp.expand(sp.series(Fx.subs(j, 1/t), t, 0, 4).removeO())
	return sp.simplify(sp.expand(ser.coeff(t, 1)))


print('f1 = coefficient of t in F_x = -a2/e(j-1)^2 - a3/(e(j-1)^2 e(j-2))')
for parity in ('e', 'o'):
	for branch in ('free', 'rigid'):
		val = f1(parity, branch)
		print(f'  parity={parity} branch={branch}: f1 = {val}')
		# predicted diagonal coefficient of A_{m-1} in the t^m residual is (m-1)+f1
		print('    predicted diagonal coefficients (m-1+f1) for m=3..8:',
		      [sp.simplify((m-1) + val) for m in range(3, 9)])

print('\nExplicit a2 first two terms (to show epsilon):')
for parity in ('e', 'o'):
	a1, a2, a3 = a_coeffs(parity)
	ser = sp.expand(sp.series(a2.subs(j, 1/t), t, 0, 3).removeO())
	print(f'  parity={parity}: a2 = {ser}')
