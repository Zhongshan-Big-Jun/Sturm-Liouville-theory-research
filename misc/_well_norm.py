# -*- coding: utf-8 -*-
"""Compare norm2_fast vs norm2_trap to find the bug."""
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

def block_lincoefs(blocks, s, bi):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1]+L)
	M00, M01, M10, M11 = 1.0, 0.0, 0.0, 1.0
	for L, c in blocks[:bi]:
		w = s*np.sqrt(c); wL = w*L
		cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
		M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
	L, c = blocks[bi]
	w = s*np.sqrt(c)
	return M11/w, M01

def norm2_fast(blocks, s):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1]+L)
	tot = 0.0
	for bi, (L, c) in enumerate(blocks):
		A, B = block_lincoefs(blocks, s, bi)
		w = s*np.sqrt(c); wL = w*L
		IA = L/2 - np.sin(2*wL)/(4*w)
		IB = L/2 + np.sin(2*wL)/(4*w)
		IAB = (1-np.cos(2*wL))/(2*w)
		tot += c*(A*A*IA + B*B*IB + 2*A*B*IAB)
	return tot

R = 4.0
a, b = 0.35, 0.65
blocks = [(a, R), (b-a, 1.0), (1-b, R)]
lam1, lam2 = eigs_fast(blocks, 2)
for k, lam in enumerate([lam1, lam2]):
	s = np.sqrt(lam)
	nt = norm2_trap(blocks, s)
	nf = norm2_fast(blocks, s)
	print(f"mode {k+1}: trap={nt:.12f} fast={nf:.12f} ratio={nf/nt:.6f}")
