import sympy as sp


def assert_zero(expression, name):
	numerator = sp.factor(sp.together(expression).as_numer_denom()[0])
	if numerator != 0:
		raise AssertionError(f"{name}: {numerator}")
	print(f"PASS {name}")


def main():
	M, c, x, y, u, v = sp.symbols("M c x y u v", positive=True)
	k = M - 1
	P = (1 + M * u**2) / (1 + u**2)
	Q = (M + v**2) / (1 + v**2)
	Ttheta = u / (1 + u**2) + c * v / (1 + v**2)
	Dtheta = (P * u + c * Q / v) / k
	V = (M * x - k * u / (1 + u**2)) / P
	V -= c * v**2 * (1 + u**2) * (M * y + k * v / (1 + v**2)) / ((1 + v**2) * Q)
	W = Dtheta * V + Ttheta**2 * (1 + u**2)
	R = v**2 * (1 + M * u**2) / (M + v**2)
	H0 = u * v * (1 + v**2) * (1 + M * u**2)
	H0 += c * (1 + u**2) * (M + v**2)
	E = M * c * u * k * (u**2 * v**2 - 1) ** 2 / ((M + v**2) * H0)
	assert_zero(W - M * Dtheta * (x - c * R * y - E) / P, "G_over_X_factorization")

	Lalpha = 1 + y**2 - c**2 * (1 + x**2)
	Bscaled = M * Lalpha - k * (1 - c**2)
	Rleft = (1 + M * x**2) / (1 + M * y**2)
	assert_zero(Bscaled - (1 + M * y**2) * (1 - c**2 * Rleft), "left_B_identity")

	C2 = 1 / (1 + u**2)
	s2 = v**2 / (1 + v**2)
	H = C2 - c**2 * s2
	J = M * H - k * (1 - c**2) * C2 * s2
	assert_zero(1 - c**2 * R - J / (C2 * Q), "right_B_H_identity")


if __name__ == "__main__":
	main()
