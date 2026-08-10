# -*- coding: utf-8 -*-
"""Well-family rigidity exploration (INF side, n=1 gap).
Checks: (1) transport identity y(b)^2/y(a)^2 = Jt_m(sm(1-b))/Jt_m(sma);
(2) shape of r_tau(x)=Jt_m(tau x)/Jt_m(x); (3) asymmetric good-root search.
E3 evidence only.
"""
import numpy as np
from numpy.polynomial import polynomial as P

def tm_blocks(blocks, s):
	"""Transfer matrix from 0 to 1 for given s. Returns (M00, M01, M10, M11)."""
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for L, c in blocks:
		w = s*np.sqrt(c)
		wL = w*L
		cw = np.cos(wL)
		sw = np.sin(wL)/w
		sw2 = -w*np.sin(wL)
		M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	return M00, M01, M10, M11

def secular(blocks, s):
	"""Dirichlet secular value: y(1) with (y,y')=(0,1) at 0."""
	M00, M01, M10, M11 = tm_blocks(blocks, s)
	return M01

def solve_eigs(blocks, k=2):
	"""First k eigenvalues via bracket scan."""
	smax = 2.0 + k*np.pi*np.sqrt(max(c for _, c in blocks)) + 4
	sp = np.linspace(1e-9, smax, 8000)
	d = secular(blocks, sp)
	signs = np.signbit(d[1:]) != np.signbit(d[:-1])
	idx = np.nonzero(signs)[0]
	out = []
	for i in idx[:k]:
		lo, hi = sp[i], sp[i+1]
		for _ in range(6):
			sg = np.linspace(lo, hi, 3000)
			dg = secular(blocks, sg)
			sg_s = np.signbit(dg[1:]) != np.signbit(dg[:-1])
			j2 = np.nonzero(sg_s)[0]
			if len(j2) == 0:
				break
			lo, hi = sg[j2[0]], sg[j2[0]+1]
		out.append(((lo+hi)/2)**2)
	return np.sort(out)[:k]

def y_at(blocks, s, x):
	"""y(x) with (y,y')=(0,1) at 0; also y'(x)."""
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1] + L)
	bi = max(i for i in range(len(xs)-1) if xs[i] <= x)
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for L, c in blocks[:bi]:
		w = s*np.sqrt(c)
		wL = w*L
		cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
		M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	L, c = blocks[bi]
	w = s*np.sqrt(c)
	d = x - xs[bi]
	cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
	n00, n01, n10, n11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	return n01, n11  # y, y'

def Jt(m, x):
	"""Jt_m(x) = sin^2 x / (sin^2 x + m^2 cos^2 x)."""
	s = np.sin(x); c = np.cos(x)
	return s*s/(s*s + m*m*c*c)

def norm2(blocks, s):
	"""int rho y^2 dx for the slope-normalized solution (for normalization factor)."""
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1] + L)
	tot = 0.0
	for bi, (L, c) in enumerate(blocks):
		n = 400
		xx = np.linspace(xs[bi], xs[bi+1], n+1)
		yy = np.array([y_at(blocks, s, x)[0] for x in xx])
		tot += c*np.trapezoid(yy*yy, xx)
	return tot

# (1) transport identity for well family
R = 4.0
m = np.sqrt(R)
for (a, b) in [(0.3, 0.7), (0.25, 0.62), (0.4, 0.8), (0.3825, 0.6175)]:
	blocks = [(a, R), (b-a, 1.0), (1-b, R)]
	lams = solve_eigs(blocks, 2)
	print("well a,b =", a, b, "lam =", lams)
	for k, lam in enumerate(lams):
		s = np.sqrt(lam)
		ya, ypa = y_at(blocks, s, a)
		yb, ypb = y_at(blocks, s, b)
		rhs = Jt(m, s*m*(1-b))/Jt(m, s*m*a)
		lhs = (yb/ya)**2
		print("  mode", k+1, "lhs", lhs, "rhs", rhs, "rel err", abs(lhs-rhs)/max(abs(lhs), 1e-300))
