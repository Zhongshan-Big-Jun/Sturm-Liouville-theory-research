import math

import numpy as np
from scipy.optimize import brentq


def values(m, c, alpha, theta):
	S = math.sin(theta)
	C = math.cos(theta)
	s = math.sin(c * theta)
	Cc = math.cos(c * theta)
	t = m * m - 1.0
	P = C * C + m * m * S * S
	Q = s * s + m * m * Cc * Cc
	x = 1.0 / math.tan(alpha)
	y = 1.0 / math.tan(c * alpha)
	lock = s * s * P * (1.0 + m * m * y * y)
	lock -= C * C * Q * (1.0 + m * m * x * x)
	Ttheta = S * C + c * s * Cc
	Dtheta = m * m * (math.tan(theta) + c / math.tan(c * theta)) / t - Ttheta
	V = (m * m * x - t * S * C) / P
	V -= c * s * s * (m * m * y + t * s * Cc) / (C * C * Q)
	W = Dtheta * V + Ttheta * Ttheta / (C * C)
	Lalpha = 1.0 / math.sin(c * alpha) ** 2 - c * c / math.sin(alpha) ** 2
	Bscalar = m * Lalpha - (m - 1.0 / m) * (1.0 - c * c)
	H = C * C - c * c * s * s
	return lock, W, Lalpha, Bscalar, H


def main():
	rng = np.random.default_rng(20260901)
	violations = []
	chambers = {}
	root_count = 0
	for _ in range(2000):
		m = math.exp(rng.uniform(math.log(1.001), math.log(100.0)))
		c = rng.uniform(0.01, 0.99)
		theta = rng.uniform(0.002, math.pi / 2.0 - 0.002)
		grid = np.linspace(0.002, math.pi - 0.002, 1200)
		last_alpha = float(grid[0])
		last_value = values(m, c, last_alpha, theta)[0]
		for alpha_value in grid[1:]:
			alpha = float(alpha_value)
			current_value = values(m, c, alpha, theta)[0]
			if last_value * current_value < 0.0:
				root = brentq(lambda a: values(m, c, a, theta)[0], last_alpha, alpha, xtol=1.0e-14)
				lock, W, Lalpha, Bscalar, H = values(m, c, root, theta)
				root_count += 1
				signs = tuple(np.sign(value) for value in (Lalpha, Bscalar, H))
				if signs not in chambers or W > chambers[signs][0]:
					chambers[signs] = (W, m, c, root, theta, Lalpha, Bscalar, H, lock)
				coherent = signs in ((1.0, 1.0, 1.0), (-1.0, -1.0, -1.0))
				if W > 1.0e-8 and not coherent:
					violations.append((W, m, c, root, theta, Lalpha, Bscalar, H, lock))
			last_alpha = alpha
			last_value = current_value
	print("root_count", root_count)
	print("violations", len(violations))
	for signs, row in sorted(chambers.items()):
		print("chamber", signs, " ".join(f"{value:.17g}" for value in row))
	for row in sorted(violations, reverse=True)[:10]:
		print("violation", " ".join(f"{value:.17g}" for value in row))


if __name__ == "__main__":
	main()
