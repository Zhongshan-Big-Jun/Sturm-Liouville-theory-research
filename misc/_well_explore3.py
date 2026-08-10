# -*- coding: utf-8 -*-
"""Well-family good-root search, corrected norms + Newton (E3 evidence)."""
import numpy as np
from scipy.optimize import brentq, root

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

def norm2(blocks, s):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1]+L)
	tot = 0.0
	for bi, (L, c) in enumerate(blocks):
		n = 600
		xx = np.linspace(xs[bi], xs[bi+1], n+1)
		yy = np.array([block_state(blocks, s, x)[0] for x in xx])
		tot += c*np.trapezoid(yy*yy, xx)
	return tot

def residuals(ab, R):
	a, b = ab
	blocks = [(a, R), (b-a, 1.0), (1-b, R)]
	lam1, lam2 = eigs_fast(blocks, 2)
	n1 = norm2(blocks, np.sqrt(lam1))
	n2 = norm2(blocks, np.sqrt(lam2))
	y1a = block_state(blocks, np.sqrt(lam1), a)[0]; y1b = block_state(blocks, np.sqrt(lam1), b)[0]
	y2a = block_state(blocks, np.sqrt(lam2), a)[0]; y2b = block_state(blocks, np.sqrt(lam2), b)[0]
	f1 = lam1*y1a**2/n1 - lam2*y2a**2/n2
	f2 = lam1*y1b**2/n1 - lam2*y2b**2/n2
	return np.array([f1, f2]), (lam2-lam1), ((y2a > 0) and (y2b < 0))

R = 4.0
# symmetric line critical point
from scipy.optimize import minimize_scalar
def Dsym(u):
	return residuals((u, 1-u), R)[1]
res = minimize_scalar(Dsym, bounds=(0.05, 0.45), method='bounded', options={'xatol': 1e-12})
u_star = res.x
r, D, sok = residuals((u_star, 1-u_star), R)
print("sym min u*=%.12f D*=%.12f R1=%.3e R2=%.3e sign_ok=%s" % (u_star, D, r[0], r[1], sok))

# Newton from random seeds
rng = np.random.default_rng(7)
found = []
for _ in range(80):
	ab = rng.uniform(0.02, 0.98, 2)
	ab = np.sort(ab)
	if ab[1] - ab[0] < 0.02:
		ab[1] = ab[0] + 0.02
	try:
		sol = root(lambda x: residuals(x, R)[0], ab, method='hybr', options={'xtol': 1e-11})
	except Exception:
		continue
	if sol.success and 0 < sol.x[0] < sol.x[1] < 1:
		r, D, sok = residuals(sol.x, R)
		if abs(r[0]) < 1e-6 and abs(r[1]) < 1e-6:
			found.append((sol.x[0], sol.x[1], r[0], r[1], D, sok))
uniq = []
for row in found:
	if not any(abs(row[0]-u[0]) < 1e-6 and abs(row[1]-u[1]) < 1e-6 for u in uniq):
		uniq.append(row)
print("unique Newton-converged good roots:", len(uniq))
for row in uniq:
	print("  a=%.10f b=%.10f R1=%.2e R2=%.2e D=%.10f sign_ok=%s" % row)
