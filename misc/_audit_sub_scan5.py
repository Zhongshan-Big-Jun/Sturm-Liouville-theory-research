import numpy as np
from scipy.optimize import root, brentq

PI = np.pi
EPS = 1e-3
def Secular(s, a, b, m):
	sa = s*a
	theta = m*s*(b-a)
	syb = np.cos(theta)*np.sin(sa) + np.sin(theta)/m*np.cos(sa)
	ypb = -m*np.sin(theta)*np.sin(sa) + np.cos(theta)*np.cos(sa)
	yb = syb/s
	return ypb*np.sin(s*(1-b)) + s*yb*np.cos(s*(1-b))

GridS = np.linspace(1e-6, 3*PI, 4000)
def Eigenvalues(a, b, m, n=2):
	g = Secular(GridS, a, b, m)
	roots = []
	for i in range(len(GridS)-1):
		if g[i]*g[i+1] < 0:
			roots.append(brentq(lambda s: Secular(s, a, b, m), GridS[i], GridS[i+1]))
		if len(roots) >= n:
			break
	return roots

def Eigenfunction(s, a, b, m, x):
	res = np.empty_like(x)
	left = x <= a; mid = (x > a) & (x < b); right = x >= b
	res[left] = np.sin(s*x[left])/s
	sa = s*a; theta = m*s*(b-a)
	ya = np.sin(sa)/s; ypa = np.cos(sa)
	res[mid] = ya*np.cos(m*s*(x[mid]-a)) + ypa/(m*s)*np.sin(m*s*(x[mid]-a))
	sb = s*(1-b)
	yb = (np.cos(theta)*np.sin(sa) + np.sin(theta)/m*np.cos(sa))/s
	C = s*yb/np.sin(sb)
	res[right] = C*np.sin(s*(1-x[right]))/s
	return res

GQ, GW = np.polynomial.legendre.leggauss(200)
def Norm(a, b, m, s):
	tot = 0.0
	for (lo, hi, w) in [(0.0, a, 1.0), (a, b, m*m), (b, 1.0, 1.0)]:
		xs = 0.5*(hi-lo)*GQ + 0.5*(hi+lo)
		ys = Eigenfunction(s, a, b, m, xs)
		tot += w*0.5*(hi-lo)*np.sum(GW*ys**2)
	return tot

def Residuals(Rval, a, b):
	m = np.sqrt(Rval)
	s1, s2 = Eigenvalues(a, b, m)
	pts = np.array([a, b])
	y1 = Eigenfunction(s1, a, b, m, pts)
	y2 = Eigenfunction(s2, a, b, m, pts)
	n1 = Norm(a, b, m, s1)
	n2 = Norm(a, b, m, s2)
	f_a = s1**2*y1[0]**2/n1 - s2**2*y2[0]**2/n2
	f_b = s1**2*y1[1]**2/n1 - s2**2*y2[1]**2/n2
	v_a = y2[0]/y1[0]
	v_b = y2[1]/y1[1]
	return f_a, f_b, v_a, v_b, s1, s2

def AllInteriorZeroRoots(Rval, coarse=80, verbose=False):
	aa = np.linspace(0.005, 0.495, 300)
	vals = [Residuals(Rval, xi, 1-xi)[0] for xi in aa]
	roots = []
	for i in range(len(aa)-1):
		if vals[i]*vals[i+1] < 0:
			z = brentq(lambda t: Residuals(Rval, t, 1-t)[0], aa[i], aa[i+1])
			fa, fb, va, vb, _, _ = Residuals(Rval, z, 1-z)
			if EPS < z < 1-EPS:
				roots.append((z, 1-z, va, vb, abs(fa)+abs(fb)))
	aa2 = np.linspace(0.01, 0.99, coarse)
	cands = []
	for ia in range(coarse):
		a0 = aa2[ia]
		for ib in range(ia+1, coarse):
			b0 = aa2[ib]
			try:
				fa, fb, va, vb, _, _ = Residuals(Rval, a0, b0)
			except Exception:
				continue
			mag = abs(fa) + abs(fb)
			if mag < 1.0:
				cands.append((a0, b0, mag))
	cands.sort(key=lambda t: t[2])
	seen = []
	for a0, b0, m0 in cands[:40]:
		if any(abs(a0-p[0]) < 0.03 and abs(b0-p[1]) < 0.03 for p in seen):
			continue
		seen.append((a0, b0))
		try:
			sol = root(lambda z: Residuals(Rval, z[0], z[1])[:2], [a0, b0], method='hybr')
		except Exception:
			continue
		if not sol.success:
			continue
		a, b = sol.x
		if not (EPS < a < b-EPS < 1-EPS):
			if verbose:
				print("  rejected boundary (a,b)=(%.6f,%.6f)" % (a, b))
			continue
		fa, fb, va, vb, _, _ = Residuals(Rval, a, b)
		if abs(fa) + abs(fb) > 1e-5:
			continue
		if any(abs(a-p[0]) < 0.02 and abs(b-p[1]) < 0.02 for p in roots):
			continue
		if verbose:
			print("  NEW interior root (a,b)=(%.6f,%.6f) va=%.4f vb=%.4f from (%.4f,%.4f)" % (a, b, va, vb, a0, b0))
		roots.append((a, b, va, vb, abs(fa)+abs(fb)))
	return roots

for Rv in [1.2, 10.0]:
	print("R =", Rv)
	rts = AllInteriorZeroRoots(Rv, verbose=True)
	print("  total:", len(rts))
	for r in rts:
		print("    (a,b)=(%.6f,%.6f) va=%.4f vb=%.4f mag=%.2e" % (r[0], r[1], r[2], r[3], r[4]))

# R=1000 probe
for Rv in [1000.0]:
	aa = np.linspace(0.005, 0.495, 500)
	vals = []
	for xi in aa:
		try:
			vals.append(Residuals(Rv, xi, 1-xi)[0])
		except Exception as e:
			vals.append(np.nan)
	print('R=1000 S_R sample: min=', np.nanmin(vals), 'at xi=', aa[np.nanargmin(vals)])
	for i in range(len(aa)-1):
		if not np.isnan(vals[i]) and not np.isnan(vals[i+1]) and vals[i]*vals[i+1] < 0:
			z = brentq(lambda t: Residuals(Rv, t, 1-t)[0], aa[i], aa[i+1])
			fa, fb, va, vb, _, _ = Residuals(Rv, z, 1-z)
			print('  line root xi*=%.6f va=%.4f vb=%.4f' % (z, va, vb))
