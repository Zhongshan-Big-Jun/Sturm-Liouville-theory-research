# -*- coding: utf-8 -*-
"""Check FH identity for well family: dD/da = (R-1)*R1, dD/db = -(R-1)*R2 (E3)."""
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

def D_and_f(ab, R):
	a, b = ab
	blocks = [(a, R), (b-a, 1.0), (1-b, R)]
	lam1, lam2 = eigs_fast(blocks, 2)
	n1 = norm2_fast(blocks, np.sqrt(lam1))
	n2 = norm2_fast(blocks, np.sqrt(lam2))
	f1 = lambda x: lam1*block_state(blocks, np.sqrt(lam1), x)[0]**2/n1 - lam2*block_state(blocks, np.sqrt(lam2), x)[0]**2/n2
	return lam2-lam1, f1(a), f1(b), lam1, lam2

R = 4.0
a, b = 0.35, 0.65
D0, R1, R2, lam1, lam2 = D_and_f((a, b), R)
h = 1e-6
Da, _, _, _, _ = D_and_f((a+h, b), R)
Db, _, _, _, _ = D_and_f((a, b+h), R)
print("a=%.4f b=%.4f D=%.8f" % (a, b, D0))
print("dD/da (FD) = %.6f  (R-1)R1 = %.6f" % ((Da-D0)/h, (R-1)*R1))
print("dD/db (FD) = %.6f  -(R-1)R2 = %.6f" % ((Db-D0)/h, -(R-1)*R2))
print("R1=%.6f R2=%.6f" % (R1, R2))
# symmetric point
u = 0.3825
a, b = u, 1-u
D0, R1, R2, lam1, lam2 = D_and_f((a, b), R)
print("sym: a=%.4f D=%.8f R1=%.6f R2=%.6f R1+R2=%.6f" % (u, D0, R1, R2, R1+R2))
# find symmetric-line critical point via minimization
from scipy.optimize import minimize_scalar
res = minimize_scalar(lambda u: D_and_f((u, 1-u), R)[0], bounds=(0.05, 0.45), method='bounded', options={'xatol': 1e-12})
u_star = res.x
D_star, R1s, R2s, _, _ = D_and_f((u_star, 1-u_star), R)
print("symmetric min: u*=%.12f D*=%.12f R1=%.3e R2=%.3e" % (u_star, D_star, R1s, R2s))
