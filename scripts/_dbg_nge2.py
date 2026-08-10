# -*- coding: utf-8 -*-
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("aud", r"F:\LaTeX\BVE research\scripts\audit_nge2_pdfs.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rng = np.random.default_rng(11)
allblocks = []
for trial in range(40):
	R = float(rng.choice([1.1, 1.5, 2.0, 4.0, 10.0, 100.0]))
	n = int(rng.choice([2, 2, 3, 4, 5]))
	nb = int(rng.integers(3, 2 * n + 6))
	edges = np.sort(rng.uniform(0.01, 0.99, nb - 1))
	edges = np.r_[0.0, edges, 1.0]
	vals = rng.choice([1.0, R], size=nb)
	blocks = [(float(edges[i + 1] - edges[i]), float(vals[i])) for i in range(nb)]
	allblocks.append((trial, R, n, blocks))
for trial, R, n, blocks in allblocks:
	if trial not in (35, 36, 37, 38, 39):
		continue
	d = m.eigdata(blocks, n)
	c = d["c"]
	exp = 2 * n - 2 + (1 if d["q0"] > c else 0) + (1 if d["q1"] < -c else 0)
	nodes = m.nodes_of(blocks, d)
	pts = [0.0] + nodes + [1.0]
	cnt = 0
	for j in range(len(pts) - 1):
		tt = np.linspace(pts[j] + 1e-7, pts[j + 1] - 1e-7, 3001)
		Q = np.array([m.qfun(blocks, d, t) for t in tt])
		for lev in (c, -c):
			sgn = np.signbit(Q - lev)
			cnt += int(np.sum(sgn[1:] != sgn[:-1]))
	W = d["dv"] * d["un"] - d["v"] * d["dun"]
	Wbad = int(np.sum(W[d["un"] != 0] >= -1e-7))
	print("trial %d: R=%g n=%d nodes=%d cnt=%d exp=%d q0=%.5f q1=%.5f c=%.5f Wbad=%d Wmin=%.2e Wmax=%.2e" % (trial, R, n, len(nodes), cnt, exp, d["q0"], d["q1"], c, Wbad, W.min(), W.max()))
