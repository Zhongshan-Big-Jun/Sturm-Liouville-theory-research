# -*- coding: utf-8 -*-
"""Debug FH for well family: dlam/da vs -lam*(R-1)*u(a)^2 (E3)."""
import numpy as np
from scipy.optimize import brentq

def secular(blocks, s):
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for L, c in blocks:
		w = s*np.sqrt(c)
		wL = w*L
		cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
		M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	return M01

def eigs_fast(blocks, k=2):
	sp = np.linspace(1e-9, 160.0, 20000)
	d = secular(blocks, sp)
	signs = np.signbit(d[1:]) != np.signbit(d[:-1])
	idx = np.nonzero(signs)[0]
	out = []
	for i in idx[:k]:
		lo, hi = sp[i], sp[i+1]
		r = brentq(lambda x: secular(blocks, x), lo, hi, xtol=1e-13, rtol=1e-13)
		out.append(r*r)
	return np.sort(out)[:k]

def block_state(blocks, s, x):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1]+L)
	bi = max(i for i in range(len(xs)-1) if xs[i] <= x)
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for L, c in blocks[:bi]:
		w = s*np.sqrt(c); wL = w*L
		cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
		M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	L, c = blocks[bi]
	w = s*np.sqrt(c); d = x - xs[bi]
	cw = np.cos(w*d); sw = np.sin(w*d)/w; sw2 = -w*np.sin(w*d)
	n00, n01, n10, n11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	return n01, n11

def norm2_trap(blocks, s):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1]+L)
	tot = 0.0
	for bi, (L, c) in enumerate(blocks):
		n = 2000
		xx = np.linspace(xs[bi], xs[bi+1], n+1)
		yy = np.array([block_state(blocks, s, x)[0] for x in xx])
		tot += c*np.trapezoid(yy*yy, xx)
	return tot

R = 4.0
a, b = 0.35, 0.65
blocks = [(a, R), (b-a, 1.0), (1-b, R)]
lam1, lam2 = eigs_fast(blocks, 2)
print("lam1, lam2 =", lam1, lam2)
for k, lam in enumerate([lam1, lam2]):
	s = np.sqrt(lam)
	nt = norm2_trap(blocks, s)
	ya = block_state(blocks, s, a)[0]
	print(f"mode {k+1}: norm_trap={nt:.10f} y(a)={ya:.10f} lam*y(a)^2/norm={lam*ya*ya/nt:.10f}")
h = 1e-7
blocks_a = [(a+h, R), (b-a-h, 1.0), (1-b, R)]
lam1a, lam2a = eigs_fast(blocks_a, 2)
d1 = (lam1a - lam1)/h
print("dlam1/da =", d1, " -lam1*(R-1)*y(a)^2/n =", -lam1*(R-1)*(block_state(blocks, np.sqrt(lam1), a)[0])**2/norm2_trap(blocks, np.sqrt(lam1)))
print("dlam2/da =", (lam2a-lam2)/h, " -lam2*(R-1)*y(a)^2/n =", -lam2*(R-1)*(block_state(blocks, np.sqrt(lam2), a)[0])**2/norm2_trap(blocks, np.sqrt(lam2)))
