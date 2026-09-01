import math
import random

import numpy as np


def js(t):
	return t / 2.0 - math.sin(2.0 * t) / 4.0


def jc(t):
	return t / 2.0 + math.sin(2.0 * t) / 4.0


def jquad(a, b, t):
	return a * a * jc(t) + b * b * js(t) + a * b * math.sin(t) ** 2


def data(m, u):
	c, alpha, beta, theta = u
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
	i3 = (
		m * m * X * X * js(alpha) / math.sin(alpha) ** 2
		+ m * jquad(C, -m * S, beta)
		+ m * m * jc(theta)
	)
	i2 = (
		m * m * Y * Y * js(c * alpha) / math.sin(c * alpha) ** 2
		+ m * jquad(s, m * Cc, c * beta)
		+ m * m * js(c * theta)
	)
	r = m * m / (m * m - 1.0)
	tt = S * C + c * s * Cc
	dt = r * (math.tan(theta) + c / math.tan(c * theta)) - tt
	psi = X * X * (D - c * s * N / C) - r * (c * C * T / s - Z)
	xi = dt * psi + X ** 3 * tt ** 2 / C ** 2
	u_mid = D - c * s * N / C
	k_left = c * C * T / s - Z
	neg = X ** 3 * tt ** 2 / C ** 2
	core = dt * u_mid + X * tt ** 2 / C ** 2
	return locals()


def equations(m, u):
	d = data(m, u)
	c = d["c"]
	alpha = d["alpha"]
	C = d["C"]
	s = d["s"]
	X = d["X"]
	Z = d["Z"]
	Y = d["Y"]
	T = d["T"]
	i2 = d["i2"]
	i3 = d["i3"]
	return np.array([
		X * math.cos(alpha) - Z * math.sin(alpha),
		Y * math.cos(c * alpha) + T * math.sin(c * alpha),
		C * Y + s * X,
		C * C * i2 - c ** 3 * s * s * i3,
	])


def admissible(m, u):
	d = data(m, u)
	c, alpha, beta, theta = u
	d3 = math.atan(d["C"] / (m * d["S"]))
	d2 = math.pi - math.atan(d["s"] / (m * d["Cc"]))
	return (
		0.0 < c < 1.0
		and 0.0 < alpha < math.pi
		and 0.0 < theta < math.pi / 2.0
		and d3 < beta < d3 + math.pi
		and 0.0 < c * beta < d2
		and d["X"] < 0.0
		and d["Y"] > 0.0
	)


def reduced(m, v):
	c, beta, theta = v
	S = math.sin(theta)
	C = math.cos(theta)
	X = C * math.cos(beta) - m * S * math.sin(beta)
	Z = S * math.cos(beta) + C * math.sin(beta) / m
	alpha = math.atan2(-X, -Z)
	d = data(m, np.array([c, alpha, beta, theta]))
	alpha2 = math.atan2(d["Y"], -d["T"])
	return np.array([
		c * alpha - alpha2,
		(d["C"] * d["Y"] + d["s"] * d["X"]) / m,
		math.log(d["C"] ** 2 * d["i2"] / (c ** 3 * d["s"] ** 2 * d["i3"])),
	])


def newton(m, v):
	v = np.array(v, dtype=float)
	for _ in range(80):
		f = reduced(m, v)
		if np.linalg.norm(f, ord=np.inf) < 1e-12:
			return v
		h = 1e-6
		jac = np.column_stack([(reduced(m, v + h * np.eye(3)[j]) - reduced(m, v - h * np.eye(3)[j])) / (2.0 * h) for j in range(3)])
		step = np.linalg.solve(jac, -f)
		base = np.linalg.norm(f)
		accepted = False
		for k in range(20):
			w = v + step / (2.0 ** k)
			if not (0.01 < w[0] < 0.999 and 0.01 < w[1] < 8.0 and 0.01 < w[2] < math.pi / 2.0 - 0.001):
				continue
			if np.linalg.norm(reduced(m, w)) < base:
				v = w
				accepted = True
				break
		if not accepted:
			return None
	return None


def bisect(f, a, b):
	fa = f(a)
	for _ in range(100):
		mid = (a + b) / 2.0
		fm = f(mid)
		if fa * fm <= 0.0:
			b = mid
		else:
			a = mid
			fa = fm
	return (a + b) / 2.0


if __name__ == "__main__":
	c = 2.0 / 3.0
	theta = bisect(lambda t: math.cos(t) / math.sin(c * t) - c, 0.01, math.pi / 2.0 - 0.01)
	alpha = bisect(lambda a: math.sin(a) - c * math.sin(c * a), 2.0, math.pi - 0.01)
	beta = 1.5 * math.pi - alpha - theta
	v = np.array([c, beta, theta])
	for m in np.concatenate((np.linspace(1.0001, 2.0, 40), np.linspace(2.1, 10.0, 40), np.linspace(11.0, 100.0, 30))):
		v = newton(float(m), v)
		if v is None:
			print("FAILED", m)
			break
		c, beta, theta = v
		S = math.sin(theta)
		C = math.cos(theta)
		X = C * math.cos(beta) - m * S * math.sin(beta)
		Z = S * math.cos(beta) + C * math.sin(beta) / m
		alpha = math.atan2(-X, -Z)
		u = np.array([c, alpha, beta, theta])
		if not admissible(float(m), u):
			print("INADMISSIBLE", m, u)
			break
		if m < 1.1 or abs(m - round(m)) < 0.03 or m > 90.0:
			d = data(float(m), u)
			print(
				"m=%.8g c=%.12g alpha=%.12g beta=%.12g theta=%.12g Xi=%.12g Psi=%.12g X=%.12g U=%.12g K=%.12g Dt=%.12g Neg=%.12g Core=%.12g"
				% (m, *u, d["xi"], d["psi"], d["X"], d["u_mid"], d["k_left"], d["dt"], d["neg"], d["core"])
			)
