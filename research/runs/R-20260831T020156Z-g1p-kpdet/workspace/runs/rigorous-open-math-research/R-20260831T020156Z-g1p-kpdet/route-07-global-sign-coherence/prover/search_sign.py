import math

import numpy as np
from scipy.optimize import least_squares


def quantities(m, c, alpha, beta, theta):
	S = math.sin(theta)
	C = math.cos(theta)
	s = math.sin(c * theta)
	Cc = math.cos(c * theta)
	X = C * math.cos(beta) - m * S * math.sin(beta)
	Z = S * math.cos(beta) + C * math.sin(beta) / m
	D = S * math.cos(beta) + m * C * math.sin(beta)
	Y = s * math.cos(c * beta) + m * Cc * math.sin(c * beta)
	T = Cc * math.cos(c * beta) - s * math.sin(c * beta) / m
	N = Cc * math.cos(c * beta) - m * s * math.sin(c * beta)
	r = m * m / (m * m - 1.0)
	Ttheta = S * C + c * s * Cc
	Dtheta = r * (math.tan(theta) + c / math.tan(c * theta)) - Ttheta
	U = D - c * s * N / C
	G = Dtheta * U + X * Ttheta * Ttheta / (C * C)
	Lalpha = 1.0 / math.sin(c * alpha) ** 2 - c * c / math.sin(alpha) ** 2
	mu = m - 1.0 / m
	A = s * s * X * X * Lalpha
	B = s * s * X * X * (m * Lalpha - mu * (1.0 - c * c))
	H = C * C - c * c * s * s
	F3 = X * math.cos(alpha) - Z * math.sin(alpha)
	F2 = Y * math.cos(c * alpha) + T * math.sin(c * alpha)
	Fband = Y + s * X / C
	return {
		"X": X,
		"Y": Y,
		"G": G,
		"A": A,
		"B": B,
		"H": H,
		"Lalpha": Lalpha,
		"residual": np.array([F3, F2, Fband]),
	}


def admissible(m, c, alpha, beta, theta, q):
	if not (m > 1.0 and 0.0 < c < 1.0 and 0.0 < alpha < math.pi):
		return False
	if not (0.0 < c * alpha < math.pi and 0.0 < theta < math.pi / 2.0):
		return False
	if not (0.0 < c * theta < math.pi / 2.0 and q["X"] < 0.0 and q["Y"] > 0.0):
		return False
	delta3 = math.atan(math.cos(theta) / (m * math.sin(theta)))
	delta2 = math.pi - math.atan(math.sin(c * theta) / (m * math.cos(c * theta)))
	return delta3 < beta < delta3 + math.pi and 0.0 < c * beta < delta2


def main():
	rng = np.random.default_rng(20260901)
	reduced_violations = []
	for _ in range(200000):
		m = math.exp(rng.uniform(math.log(1.001), math.log(100.0)))
		c = rng.uniform(0.001, 0.999)
		alpha = rng.uniform(0.001, math.pi - 0.001)
		theta = rng.uniform(0.001, math.pi / 2.0 - 0.001)
		S = math.sin(theta)
		C = math.cos(theta)
		s = math.sin(c * theta)
		Cc = math.cos(c * theta)
		t = m * m - 1.0
		P = C * C + m * m * S * S
		Q = s * s + m * m * Cc * Cc
		Ttheta = S * C + c * s * Cc
		Dtheta = m * m * (math.tan(theta) + c / math.tan(c * theta)) / t - Ttheta
		V = (m * m / math.tan(alpha) - t * S * C) / P
		V -= c * s * s * (m * m / math.tan(c * alpha) + t * s * Cc) / (C * C * Q)
		W = Dtheta * V + Ttheta * Ttheta / (C * C)
		Lalpha = 1.0 / math.sin(c * alpha) ** 2 - c * c / math.sin(alpha) ** 2
		Bsign = m * Lalpha - (m - 1.0 / m) * (1.0 - c * c)
		H = C * C - c * c * s * s
		coherent = (Lalpha > 0.0 and Bsign > 0.0 and H > 0.0) or (Lalpha < 0.0 and Bsign < 0.0 and H < 0.0)
		if W > 1.0e-8 and not coherent:
			reduced_violations.append((W, m, c, alpha, theta, Lalpha, Bsign, H))
	print("reduced_violations", len(reduced_violations))
	for row in sorted(reduced_violations, reverse=True)[:5]:
		print("reduced", " ".join(f"{value:.17g}" for value in row))

	best = []
	root_count = 0
	chamber_stats = {}
	for _ in range(5000):
		m = math.exp(rng.uniform(math.log(1.01), math.log(20.0)))
		c = rng.uniform(0.08, 0.98)
		x0 = np.array([
			rng.uniform(0.02, math.pi - 0.02),
			rng.uniform(0.02, min(2.0 * math.pi, (math.pi - 0.02) / c)),
			rng.uniform(0.02, math.pi / 2.0 - 0.02),
		])

		def residual(x):
			return quantities(m, c, x[0], x[1], x[2])["residual"]

		upper_beta = min(2.0 * math.pi, (math.pi - 1.0e-5) / c)
		fit = least_squares(
			residual,
			x0,
			bounds=([1.0e-5, 1.0e-5, 1.0e-5], [math.pi - 1.0e-5, upper_beta, math.pi / 2.0 - 1.0e-5]),
			xtol=1.0e-13,
			ftol=1.0e-13,
			gtol=1.0e-13,
			max_nfev=3000,
		)
		alpha, beta, theta = fit.x
		q = quantities(m, c, alpha, beta, theta)
		resnorm = float(np.linalg.norm(q["residual"], ord=np.inf))
		if resnorm > 1.0e-9 or not admissible(m, c, alpha, beta, theta, q):
			continue
		root_count += 1
		signs = tuple(np.sign(q[k]) for k in ("A", "B", "H"))
		if signs not in chamber_stats or q["G"] < chamber_stats[signs][0]:
			chamber_stats[signs] = (q["G"], m, c, alpha, beta, theta, q["Lalpha"], resnorm)
		if q["G"] < -1.0e-7 and signs not in ((1.0, 1.0, 1.0), (-1.0, -1.0, -1.0)):
			best.append((q["G"], resnorm, m, c, alpha, beta, theta, q["A"], q["B"], q["H"], q["Lalpha"]))
	best.sort()
	print("root_count", root_count)
	print("mixed_g_negative_count", len(best))
	for signs, row in sorted(chamber_stats.items()):
		print("chamber", signs, " ".join(f"{value:.17g}" for value in row))
	for row in best[:20]:
		print(" ".join(f"{value:.17g}" for value in row))


if __name__ == "__main__":
	main()
