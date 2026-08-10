# -*- coding: utf-8 -*-
"""audit_nge2_pdfs.py (v3): independent audit of the two n>=2 gap-extremal proofs.
A1: Wronskian W<0 on (0,1);  A2: Q strictly decreasing per nodal interval;
A3: exact zero formula #Z(F) = 2n-2 + [q0>c] + [q1<-c] via Q=+-c crossings, zeros simple.
B:  extremal configs: exactly 2n zeros, q0>1, q1<-1, K==-2D, zero interface jumps,
    material ordering (max starts/ends 1, min starts/ends R).
Numerical pressure test only (EVIDENCE, not a proof)."""
import numpy as np
from scipy.optimize import brentq
import sys, json
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
from gap_lib import norm2

def secular(blocks, s):
	M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
	for L, c in blocks:
		w = s * np.sqrt(c); wL = w * L
		cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return M01

def eigvals(blocks, n, N=60000):
	smax = np.pi * np.sqrt(max(c for _, c in blocks)) * (n + 2) + 20
	g = np.linspace(1e-7, smax, N)
	vals = np.array([secular(blocks, t) for t in g])
	sgn = np.signbit(vals[1:]) != np.signbit(vals[:-1])
	idx = np.nonzero(sgn)[0]
	roots = []
	for i in idx[: n + 1]:
		z = brentq(lambda t: float(secular(blocks, t)), g[i], g[i + 1], xtol=1e-14, rtol=1e-14)
		roots.append(z)
	return np.sort(np.array(roots))[: n + 1]

def state_at(blocks, s, x):
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1] + L)
	bi = max(i for i in range(len(xs) - 1) if xs[i] <= x)
	M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
	for L, c in blocks[:bi]:
		w = s * np.sqrt(c); wL = w * L
		cw = np.cos(wL); sw = np.sin(wL) / w; sw2 = -w * np.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	L, c = blocks[bi]; w = s * np.sqrt(c); d = x - xs[bi]
	cw = np.cos(w * d); sw = np.sin(w * d) / w; sw2 = -w * np.sin(w * d)
	M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return M01, M11

def eigdata(blocks, n):
	ss = eigvals(blocks, n)
	sn, snp1 = ss[n - 1], ss[n]
	a, b = sn * sn, snp1 * snp1
	c = np.sqrt(a / b)
	xg = np.linspace(0.0, 1.0, 30001)
	un = np.zeros(len(xg)); dun = np.zeros(len(xg))
	v = np.zeros(len(xg)); dv = np.zeros(len(xg))
	for j, x in enumerate(xg):
		y0, dy0 = state_at(blocks, sn, x)
		y1, dy1 = state_at(blocks, snp1, x)
		un[j] = y0; dun[j] = dy0; v[j] = y1; dv[j] = dy1
	n0, n1 = norm2(blocks, sn), norm2(blocks, snp1)
	un /= np.sqrt(n0); dun /= np.sqrt(n0)
	v /= np.sqrt(n1); dv /= np.sqrt(n1)
	_, sl0n = state_at(blocks, sn, 1e-12); _, sl0v = state_at(blocks, snp1, 1e-12)
	sl1n_p, _ = state_at(blocks, sn, 1 - 1e-12); sl1v_p, _ = state_at(blocks, snp1, 1 - 1e-12)
	q0 = (sl0v / np.sqrt(n1)) / (sl0n / np.sqrt(n0))
	q1 = (sl1v_p / np.sqrt(n1)) / (sl1n_p / np.sqrt(n0))
	return dict(sn=sn, snp1=snp1, a=a, b=b, c=c, x=xg, un=un, v=v, dun=dun, dv=dv, q0=q0, q1=q1, n0=n0, n1=n1)

def nodes_of(blocks, d):
	"""u_n interior zeros via sign changes + brentq."""
	x = d["x"]; un = d["un"]; sn = d["sn"]
	idx = np.where(np.sign(un[1:]) != np.sign(un[:-1]))[0]
	nodes = []
	for i in idx:
		z = brentq(lambda t: float(state_at(blocks, sn, t)[0]), x[i], x[i + 1], xtol=1e-13, rtol=1e-13)
		if 1e-9 < z < 1 - 1e-9:
			nodes.append(z)
	return nodes

def qfun(blocks, d, t):
	y0, _ = state_at(blocks, d["sn"], t)
	y1, _ = state_at(blocks, d["snp1"], t)
	return (y1 / np.sqrt(d["n1"])) / (y0 / np.sqrt(d["n0"]))

def analyze(blocks, n, report=False):
	d = eigdata(blocks, n)
	x = d["x"]; un = d["un"]; v = d["v"]; dun = d["dun"]; dv = d["dv"]
	a, b, c = d["a"], d["b"], d["c"]
	nodes = nodes_of(blocks, d)
	if len(nodes) != n - 1:
		return None, ("node count mismatch", len(nodes), n - 1)
	pts = [0.0] + nodes + [1.0]
	cnt = 0; dec = True
	for j in range(len(pts) - 1):
		lo, hi = pts[j], pts[j + 1]
		tt = np.linspace(lo + 1e-7, hi - 1e-7, 3001)
		Q = np.array([qfun(blocks, d, t) for t in tt])
		if np.any(np.diff(Q) > 1e-6 * max(1.0, np.max(np.abs(Q)))):
			dec = False
		for lev in (c, -c):
			sgn = np.signbit(Q - lev)
			flips = np.nonzero(sgn[1:] != sgn[:-1])[0]
			for i in flips:
				z = brentq(lambda t: float(qfun(blocks, d, t) - lev), tt[i], tt[i + 1], xtol=1e-12, rtol=1e-12)
				if abs(qfun(blocks, d, z) - lev) > 1e-6:
					dec = False
				cnt += 1
	expected = 2 * n - 2 + (1 if d["q0"] > c else 0) + (1 if d["q1"] < -c else 0)
	W = dv * un - v * dun
	bad = int(np.sum(W[un != 0] > 1e-6 * max(1.0, np.max(np.abs(W)))))
	if report:
		print(f"  n={n}: #Z={cnt} expected={expected} q0={d['q0']:.5f} q1={d['q1']:.5f} c={c:.5f} Wbad={bad} dec={dec}")
	ok = (cnt == expected) and bad == 0 and dec
	return (cnt, expected, d), ok

def partA():
	print("=== Part A: universal claims on random bang-bang weights ===")
	rng = np.random.default_rng(11)
	passed = 0; total = 0; fails = []
	for trial in range(40):
		R = float(rng.choice([1.1, 1.5, 2.0, 4.0, 10.0, 100.0]))
		n = int(rng.choice([2, 2, 3, 4, 5]))
		nb = int(rng.integers(3, 2 * n + 6))
		edges = np.sort(rng.uniform(0.01, 0.99, nb - 1))
		edges = np.r_[0.0, edges, 1.0]
		vals = rng.choice([1.0, R], size=nb)
		blocks = [(float(edges[i + 1] - edges[i]), float(vals[i])) for i in range(nb)]
		res, ok = analyze(blocks, n)
		total += 1
		if ok:
			passed += 1
		else:
			fails.append((trial, R, n, res))
	for f in fails:
		print("  FAIL", f[0], "R=", f[1], "n=", f[2], f[3])
	print(f"Part A: {passed}/{total} passed")

def partB():
	print("=== Part B: extremal configs from session 13 table (R=4) ===")
	tab = json.load(open(r"F:\LaTeX\BVE research\scripts\op03_gap_table.json", encoding="utf-8"))
	R = 4.0
	passed = 0; total = 0
	for kind in ["SUP", "INF"]:
		for n in range(1, 9):
			key = f"n{n}_{kind}"
			if key not in tab:
				continue
			edges = [0.0] + tab[key]["edges"] + [1.0]
			vals = [(1.0 if j % 2 == 0 else R) if kind == "SUP" else (R if j % 2 == 0 else 1.0) for j in range(len(edges) - 1)]
			blocks = [(float(edges[i + 1] - edges[i]), float(vals[i])) for i in range(len(edges) - 1)]
			res, ok = analyze(blocks, n)
			if res is None:
				print(f"  {key}: {ok} -> FAIL")
				total += 1
				continue
			cnt, expected, d = res
			xs = np.cumsum([0.0] + [L for L, _ in blocks])
			Kvals = []; jumps = []
			for j, (L, r) in enumerate(blocks):
				xc = 0.5 * (xs[j] + xs[j + 1])
				un2 = np.interp(xc, d["x"], d["un"]) ** 2
				up2 = np.interp(xc, d["x"], d["v"]) ** 2
				dun2 = np.interp(xc, d["x"], d["dun"]) ** 2
				dup2 = np.interp(xc, d["x"], d["dv"]) ** 2
				Kvals.append((dun2 - dup2) + (d["a"] * r * un2 - d["b"] * r * up2))
			for j in range(len(blocks) - 1):
				Fj = d["a"] * np.interp(xs[j + 1], d["x"], d["un"]) ** 2 - d["b"] * np.interp(xs[j + 1], d["x"], d["v"]) ** 2
				jumps.append(abs((vals[j + 1] - vals[j]) * Fj))
			K = np.mean(Kvals); D = d["b"] - d["a"]
			ok_count = (cnt == 2 * n)
			ok_q = (d["q0"] > 1.0) and (d["q1"] < -1.0)
			ok_K = abs(K + 2 * D) < 5e-4 * max(1.0, 2 * D)
			ok_spread = (max(Kvals) - min(Kvals)) < 5e-4 * max(1.0, abs(K))
			ok_jump = max(jumps) < 1e-3 * max(1.0, D)
			F0 = d["a"] * d["un"][100] ** 2 - d["b"] * d["v"][100] ** 2
			F1 = d["a"] * d["un"][-100] ** 2 - d["b"] * d["v"][-100] ** 2
			ok_ord = (F0 < 0) and (F1 < 0)
			ok = ok_count and ok_q and ok_K and ok_spread and ok_jump and ok_ord
			total += 1
			if ok:
				passed += 1
			print(f"  {key}: #Z={cnt} (2n={2*n}) q0={d['q0']:.4f} q1={d['q1']:.4f} K+2D={K+2*D:.2e} spread={max(Kvals)-min(Kvals):.2e} maxjump={max(jumps):.2e} F0={F0:+.1e} -> {'OK' if ok else 'FAIL'}")
	print(f"Part B: {passed}/{total} passed")

if __name__ == "__main__":
	partA()
	partB()
