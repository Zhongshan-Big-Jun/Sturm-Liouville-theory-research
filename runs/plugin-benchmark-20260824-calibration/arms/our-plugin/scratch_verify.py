#!/usr/bin/env python3
# Scratch symbolic verification only. This is NOT the proof.
# It checks the exact formulas used in the proof for small n and known edge cases.
import sympy as sp

y = sp.symbols('y', real=True)
x = sp.symbols('x', real=True)
z = sp.symbols('z')
s = sp.symbols('s', positive=True)
c = sp.cos(y)
q = sp.sin(y)


def U(k):
	"""Chebyshev of the second kind, symbolic in z."""
	if k < 0:
		return sp.Integer(0)
	if k == 0:
		return sp.Integer(1)
	return sp.expand(2 * z * U(k - 1) - U(k - 2))


def C_matrix():
	return sp.Matrix([[c**2 - q**2 / s, (1 + 1 / s) * c * q],
	                  [-(1 + s) * c * q, c**2 - s * q**2]])


def E_matrix():
	return sp.Matrix([[c, q], [-q, c]])


def check_formula(n):
	M = E_matrix() * C_matrix() ** n
	G = sp.expand(M[0, 1])
	# z in terms of y
	a = s + 1 / s
	z_expr = sp.expand(((a + 2) * c**2 - a) / 2)
	alpha = 1 / s
	P = sp.expand(U(n) + alpha * U(n - 1))
	G_formula = sp.expand(q * P.subs(z, z_expr))
	diff = sp.simplify(G - G_formula)
	print(f"n={n}: formula identity holds? {diff == 0}")
	return diff == 0


def check_degree(n):
	# Replace cos(y) by x and sin(y) by sqrt(1-x^2); G=sin(y)*P(z(x)).
	# Check P is degree n and has n distinct roots in (-1,1) for a couple of s values.
	alpha = 1 / s
	P = sp.expand(U(n) + alpha * U(n - 1))
	print(f"n={n}: deg_z(P) = {sp.degree(P, z)}")
	for sval in [2, 5]:
		Ps = sp.expand(P.subs(s, sval))
		deg = sp.degree(sp.Poly(Ps, z), z)
		roots = sp.nroots(Ps, n=30)
		reals = [complex(r).real for r in roots if abs(complex(r).imag) < 1e-25]
		inside = [r for r in reals if -1 < r < 1]
		distinct = len(set(round(r, 25) for r in inside))
		print(f"   s={sval}: degree={deg}, roots={len(reals)}, "
		      f"distinct-in-(-1,1)={distinct}")


def check_edge_cases():
	print("Edge checks (using exact formulas):")
	# y=0 and y=pi
	E0 = E_matrix().subs(y, 0)
	C0 = C_matrix().subs(y, 0)
	M0 = E0 * C0 ** 1
	print("  y=0: M(0) =", M0, "G =", M0[0, 1])
	# y=pi for n=1
	Mp = E_matrix().subs(y, sp.pi) * C_matrix().subs(y, sp.pi) ** 1
	print("  y=pi: G =", sp.simplify(Mp[0, 1]))
	# y=pi/2 for n=1..4: need show G nonzero, P(z) with z=-(s+1/s)/2
	for n in range(1, 5):
		G_half = sp.simplify((E_matrix() * C_matrix() ** n)[0, 1].subs(y, sp.pi / 2))
		z_half = sp.simplify(((s + 1 / s + 2) * sp.cos(y)**2 - (s + 1 / s)) / 2).subs(y, sp.pi / 2)
		alpha = 1 / s
		P_half = sp.expand((U(n) + alpha * U(n - 1)).subs(z, z_half))
		print(f"  n={n}: G(pi/2)={sp.simplify(G_half)}, P(z(pi/2))={P_half}, z_half={z_half}")


def check_R1():
	# Boundary R=1 (s=1)
	print("R=1 boundary check:")
	for n in [1, 2, 3]:
		M = E_matrix().subs(s, 1) * C_matrix().subs(s, 1) ** n
		G = sp.simplify(sp.expand(M[0, 1]))
		print(f"  n={n}: G(s=1) = {G}; expected sin({2*n+1}y) = {sp.sin((2*n+1)*y)}")


if __name__ == "__main__":
	for n in range(1, 7):
		check_formula(n)
	for n in range(1, 5):
		check_degree(n)
	check_edge_cases()
	check_R1()
