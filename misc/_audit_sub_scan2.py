# debug: print all R1=R2=0 roots for R=1.2, 10; probe boundary values
import numpy as np
from scipy.optimize import root, brentq

PI = np.pi
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

for Rv in [1.2, 10.0]:
	aa = np.linspace(0.005, 0.495, 300)
	vals = [Residuals(Rv, xi, 1-xi)[0] for xi in aa]
	print('=== R =', Rv)
	for i in range(len(aa)-1):
		if vals[i]*vals[i+1] < 0:
			z = brentq(lambda t: Residuals(Rv, t, 1-t)[0], aa[i], aa[i+1])
			fa, fb, va, vb, s1, s2 = Residuals(Rv, z, 1-z)
			print('line root xi* = %.6f  R1,R2 = %.3e,%.3e  v(a)=%.4f v(b)=%.4f' % (z, fa, fb, va, vb))
	aa2 = np.linspace(0.02, 0.98, 90)
	cands = []
	for ia in range(90):
		for ib in range(ia+1, 90):
			try:
				fa, fb, va, vb, _, _ = Residuals(Rv, aa2[ia], aa2[ib])
			except Exception:
				continue
			cands.append((abs(fa)+abs(fb), aa2[ia], aa2[ib]))
	cands.sort(key=lambda t: t[0])
	print('top 2D candidates:')
	for mag, a0, b0 in cands[:6]:
		try:
			sol = root(lambda z: Residuals(Rv, z[0], z[1])[:2], [a0, b0], method='hybr')
			if sol.success:
				a, b = sol.x
				fa, fb, va, vb, _, _ = Residuals(Rv, a, b)
				print('  refined (a,b)=(%.5f,%.5f) R1,R2=%.2e,%.2e va=%.4f vb=%.4f' % (a, b, fa, fb, va, vb))
			else:
				print('  refine failed from (%.3f,%.3f)' % (a0, b0))
		except Exception as e:
			print('  exception', e)

# boundary probes
print('=== boundary probes')
xi_lim = np.arccos(0.25)/PI
fa, fb, va, vb, s1, s2 = Residuals(1.01, xi_lim, xi_lim+1e-3)
print('R=1.01 near-diag a=xi_lim: R1=%.4f R2=%.4f va=%.4f vb=%.4f z~%.4f' % (fa, fb, va, vb, 1/2))
fa1, fb1, va1, vb1, _, _ = Residuals(4.0, 0.499, 0.501)
print('R=4 at (0.499,0.501): R1=%.5f (2pi^2=%.5f)' % (fa1, 2*PI**2))
fa0, fb0, _, _, _, _ = Residuals(4.0, 0.002, 0.998)
print('R=4 at (0.002,0.998): R1=%.6f' % fa0)
# xi* for larger R
for Rv in [4.0, 10.0, 100.0, 1000.0]:
	aa = np.linspace(0.005, 0.495, 400)
	vals = [Residuals(Rv, xi, 1-xi)[0] for xi in aa]
	for i in range(len(aa)-1):
		if vals[i]*vals[i+1] < 0:
			z = brentq(lambda t: Residuals(Rv, t, 1-t)[0], aa[i], aa[i+1])
			fa, fb, va, vb, _, _ = Residuals(Rv, z, 1-z)
			print('R=%-6g xi* = %.6f  v(a)=%.4f v(b)=%.4f' % (Rv, z, va, vb))
