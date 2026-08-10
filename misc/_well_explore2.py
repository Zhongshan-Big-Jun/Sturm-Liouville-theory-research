# -*- coding: utf-8 -*-
"""Well-family r~_tau shape and asymmetric good-root search (E3 evidence)."""
import numpy as np

def Jt(m, x):
	s = np.sin(x); c = np.cos(x)
	return s*s/(s*s + m*m*c*c)

def rtau(m, tau, x):
	return Jt(m, tau*x)/Jt(m, x)

# (2) shape of r~_tau for several (m, tau)
for m in [1.1, 1.5, 2.0, 3.0]:
	for tau in [1.2, 2.0, 4.0]:
		xs = np.linspace(1e-6, np.pi/tau - 1e-6, 20001)
		vals = rtau(m, tau, xs)
		# detect monotonicity: count sign changes of diff
		d = np.diff(vals)
		sc = np.signbit(d[1:]) != np.signbit(d[:-1])
		nmono = int(sc.sum())
		print(f"m={m} tau={tau}: rmax={vals.max():.6f} rmin={vals.min():.6f} monotonicity-violations={nmono}")
