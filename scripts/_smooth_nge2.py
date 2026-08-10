# -*- coding: utf-8 -*-
"""Smooth oscillatory weight: check zero-count formula (4.4) via FD eigenfunctions."""
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq

def fd_data(rho, n, N=8001):
	xs = np.linspace(0, 1, N); h = xs[1] - xs[0]
	r = rho(xs)
	m = N - 2
	A = 2 * np.eye(m) - np.diag(np.ones(m - 1), 1) - np.diag(np.ones(m - 1), -1)
	B = np.diag(h * h * r[1:-1])
	w, V = eigh(A, B)
	lam = w[n - 1:n + 1]
	us = []
	for k in range(2):
		y = np.zeros(N); y[1:-1] = V[:, n - 1 + k]
		if y[1] < 0:
			y = -y
		nrm = np.sqrt(np.trapezoid(rho(xs) * y ** 2, xs))
		us.append(y / nrm)
	return lam, us, xs

def check(rho, n, label):
	lam, (un, v), xs = fd_data(rho, n)
	a, b = lam
	c = np.sqrt(a / b)
	h = xs[1] - xs[0]
	# derivative via central differences (interior)
	dun = np.gradient(un, h); dv = np.gradient(v, h)
	F = a * un ** 2 - b * v ** 2
	q0 = (v[1] - v[0]) / (un[1] - un[0])
	q1 = (v[-1] - v[-2]) / (un[-1] - un[-2])
	# u_n nodes via sign changes
	idx = np.where(np.sign(un[1:]) != np.sign(un[:-1]))[0]
	nodes = [float(xs[i]) for i in idx]
	pts = [0.0] + nodes + [1.0]
	cnt = 0
	for j in range(len(pts) - 1):
		mask = (xs > pts[j] + 1e-6) & (xs < pts[j + 1] - 1e-6)
		Q = v[mask] / un[mask]
		xsq = xs[mask]
		for lev in (c, -c):
			sgn = np.signbit(Q - lev)
			fl = np.nonzero(sgn[1:] != sgn[:-1])[0]
			for i in fl:
				z = brentq(lambda t: float(np.interp(t, xsq, Q) - lev), xsq[i], xsq[i + 1], xtol=1e-12, rtol=1e-12)
				cnt += 1
	exp = 2 * n - 2 + (1 if q0 > c else 0) + (1 if q1 < -c else 0)
	W = dv * un - v * dun
	ok_W = np.all(W[un != 0] <= 1e-6 * max(1.0, np.max(np.abs(W))))
	print("%s: n=%d cnt=%d exp=%d q0=%.5f q1=%.5f c=%.5f W<0=%s -> %s" % (label, n, cnt, exp, q0, q1, c, ok_W, "OK" if cnt == exp and ok_W else "FAIL"))

for R, n in [(1.5, 2), (4.0, 3), (10.0, 5), (100.0, 4)]:
	rho = lambda x, R=R: 1 + (R - 1) * (0.5 + 0.5 * np.sin(37 * np.pi * x + 0.3)) ** 2
	check(rho, n, "smooth R=%g" % R)
