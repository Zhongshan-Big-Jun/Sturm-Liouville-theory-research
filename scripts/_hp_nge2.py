# -*- coding: utf-8 -*-
"""High-precision (mpmath) spot checks + smooth oscillatory weight FD check."""
import sys, json, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import mpmath as mp
from scipy.linalg import eigh

mp.mp.dps = 50

def secular_mp(blocks, s):
	M00 = mp.mpf(1); M01 = mp.mpf(0); M10 = mp.mpf(0); M11 = mp.mpf(1)
	s = mp.mpf(s)
	for L, c in blocks:
		w = s * mp.sqrt(mp.mpf(c)); wL = w * mp.mpf(L)
		cw = mp.cos(wL); sw = mp.sin(wL) / w; sw2 = -w * mp.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return M01

def eigvals_mp(blocks, n):
	# coarse float scan then mpmath brentq
	import importlib.util
	spec = importlib.util.spec_from_file_location("aud", r"F:\LaTeX\BVE research\scripts\audit_nge2_pdfs.py")
	m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
	ss = m.eigvals(blocks, n)
	out = []
	for s0 in ss[: n + 1]:
		lo, hi = mp.mpf(s0) * 0.99999, mp.mpf(s0) * 1.00001
		f = lambda t: secular_mp(blocks, t)
		z = mp.findroot(f, (lo, hi))
		out.append(z)
	return out

def norm2_mp(blocks, s):
	xs = [mp.mpf(0)]
	for L, c in blocks:
		xs.append(xs[-1] + mp.mpf(L))
	nrm = mp.mpf(0)
	M00 = mp.mpf(1); M01 = mp.mpf(0); M10 = mp.mpf(0); M11 = mp.mpf(1)
	for bi, (L, c) in enumerate(blocks):
		w = s * mp.sqrt(mp.mpf(c)); wL = w * mp.mpf(L)
		A = M01; B = M11 / w
		Icos = 0.5 * (mp.mpf(L) + mp.sin(2 * w * mp.mpf(L)) / (2 * w))
		Isin = 0.5 * (mp.mpf(L) - mp.sin(2 * w * mp.mpf(L)) / (2 * w))
		Icross = mp.sin(w * mp.mpf(L)) ** 2 / (2 * w)
		nrm += mp.mpf(c) * (A * A * Icos + B * B * Isin + 2 * A * B * Icross)
		cw = mp.cos(wL); sw = mp.sin(wL) / w; sw2 = -w * mp.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return nrm

def state_mp(blocks, s, x):
	xs = [mp.mpf(0)]
	for L, c in blocks:
		xs.append(xs[-1] + mp.mpf(L))
	x = mp.mpf(x)
	bi = max(i for i in range(len(xs) - 1) if xs[i] <= x)
	M00 = mp.mpf(1); M01 = mp.mpf(0); M10 = mp.mpf(0); M11 = mp.mpf(1)
	for L, c in blocks[:bi]:
		w = s * mp.sqrt(mp.mpf(c)); wL = w * mp.mpf(L)
		cw = mp.cos(wL); sw = mp.sin(wL) / w; sw2 = -w * mp.sin(wL)
		M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	L, c = blocks[bi]; w = s * mp.sqrt(mp.mpf(c)); d = x - xs[bi]
	cw = mp.cos(w * d); sw = mp.sin(w * d) / w; sw2 = -w * mp.sin(w * d)
	M00, M01, M10, M11 = cw * M00 + sw * M10, cw * M01 + sw * M11, sw2 * M00 + cw * M10, sw2 * M01 + cw * M11
	return M01, M11

def check_case(blocks, n, label):
	ss = eigvals_mp(blocks, n)
	sn, snp1 = ss[n - 1], ss[n]
	a, b = sn * sn, snp1 * snp1
	c = mp.sqrt(a / b)
	n0, n1 = norm2_mp(blocks, sn), norm2_mp(blocks, snp1)
	_, sl0n = state_mp(blocks, sn, mp.mpf("1e-30")); _, sl0v = state_mp(blocks, snp1, mp.mpf("1e-30"))
	sl1n_p, _ = state_mp(blocks, sn, 1 - mp.mpf("1e-30")); sl1v_p, _ = state_mp(blocks, snp1, 1 - mp.mpf("1e-30"))
	q0 = (sl0v / mp.sqrt(n1)) / (sl0n / mp.sqrt(n0))
	q1 = (sl1v_p / mp.sqrt(n1)) / (sl1n_p / mp.sqrt(n0))
	# count zeros of F via Q=+-c using float helper on mp evaluation
	import importlib.util
	spec = importlib.util.spec_from_file_location("aud", r"F:\LaTeX\BVE research\scripts\audit_nge2_pdfs.py")
	m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
	# nodes of u_n
	xx = np.linspace(0, 1, 40001)
	vals = np.array([float(state_mp(blocks, sn, t)[0]) for t in xx])
	idx = np.where(np.sign(vals[1:]) != np.sign(vals[:-1]))[0]
	nodes = []
	for i in idx:
		z = mp.findroot(lambda t: state_mp(blocks, sn, t)[0], (mp.mpf(xx[i]), mp.mpf(xx[i + 1])))
		if mp.mpf("1e-9") < z < 1 - mp.mpf("1e-9"):
			nodes.append(float(z))
	def qf(t):
		y0, _ = state_mp(blocks, sn, t); y1, _ = state_mp(blocks, snp1, t)
		return float((y1 / mp.sqrt(n1)) / (y0 / mp.sqrt(n0)))
	cnt = 0
	pts = [0.0] + nodes + [1.0]
	for j in range(len(pts) - 1):
		tt = np.linspace(pts[j] + 1e-9, pts[j + 1] - 1e-9, 2000)
		Q = np.array([qf(t) for t in tt])
		for lev in (float(c), -float(c)):
			sgn = np.signbit(Q - lev)
			cnt += int(np.sum(sgn[1:] != sgn[:-1]))
	exp = 2 * n - 2 + (1 if q0 > c else 0) + (1 if q1 < -c else 0)
	print("%s: n=%d cnt=%d exp=%d q0=%.6f q1=%.6f c=%.6f" % (label, n, cnt, exp, q0, q1, c))
	# K identity on extremal-type config: check piecewise constancy via two sample points per block
	xs = [0.0]
	for L, _ in blocks:
		xs.append(xs[-1] + L)
	Kvals = []
	for j, (L, r) in enumerate(blocks):
		for t in (xs[j] + 0.3 * L, xs[j] + 0.7 * L):
			y0, dy0 = state_mp(blocks, sn, t); y1, dy1 = state_mp(blocks, snp1, t)
			u0 = y0 / mp.sqrt(n0); du0 = dy0 / mp.sqrt(n0)
			u1 = y1 / mp.sqrt(n1); du1 = dy1 / mp.sqrt(n1)
			Kvals.append((du0 * du0 - du1 * du1) + mp.mpf(r) * (a * u0 * u0 - b * u1 * u1))
	K = Kvals[0]
	ok = all(abs(k - K) < mp.mpf("1e-25") for k in Kvals)
	D = b - a
	print("   K=-2D residual: %.2e   per-block constant: %s" % (float(abs(K + 2 * D)), ok))

tab = json.load(open(r"F:\LaTeX\BVE research\scripts\op03_gap_table.json", encoding="utf-8"))
for key in ["n1_SUP", "n4_INF", "n8_INF"]:
	edges = [0.0] + tab[key]["edges"] + [1.0]
	kind = key.split("_")[1]; R = 4.0
	vals = [(1.0 if j % 2 == 0 else R) if kind == "SUP" else (R if j % 2 == 0 else 1.0) for j in range(len(edges) - 1)]
	blocks = [(float(edges[i + 1] - edges[i]), float(vals[i])) for i in range(len(edges) - 1)]
	n = int(key[1:key.index("_")])
	check_case(blocks, n, "extremal " + key)
# random weight with fractional/oscillatory values cannot use TM; use FD for smooth weight separately
