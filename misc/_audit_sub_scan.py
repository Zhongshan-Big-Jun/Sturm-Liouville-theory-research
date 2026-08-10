import numpy as np
from scipy.optimize import brentq
import importlib.util
spec = importlib.util.spec_from_file_location("F", r"F:\LaTeX\BVE research\misc\_audit_sub_F_goodroot.py")
# Instead of importing (it runs everything), re-implement the needed pieces inline quickly:
import numpy as np
from scipy.optimize import brentq

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

def Weight(a, b, m, x):
	return np.where((x > a) & (x < b), m*m, 1.0)

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

# R=4: scan S_R(xi) on the symmetric line
Rv = 4.0
xis = np.linspace(0.01, 0.49, 200)
vals = [Residuals(Rv, xi, 1-xi)[0] for xi in xis]
# find sign changes
for i in range(len(xis)-1):
	if vals[i]*vals[i+1] < 0:
		print('sign change near xi =', xis[i], xis[i+1], vals[i], vals[i+1])
		z = brentq(lambda t: Residuals(Rv, t, 1-t)[0], xis[i], xis[i+1])
		print('S_R zero at xi* =', z, 'R1,R2,v(a),v(b):', Residuals(Rv, z, 1-z))
# min abs
i = int(np.argmin(np.abs(vals)))
print('min |S_R| at xi =', xis[i], vals[i])
# also near a=b diagonal and other lines: quick 2D coarse map of min residual
aa = np.linspace(0.02, 0.98, 60)
best = []
for ia, a0 in enumerate(aa):
	for ib in range(ia+1, 60):
		b0 = aa[ib]
		fa, fb, va, vb, _, _ = Residuals(Rv, a0, b0)
		best.append((abs(fa)+abs(fb), a0, b0, fa, fb, va, vb))
best.sort(key=lambda t: t[0])
for row in best[:12]:
	print('%.4f at (a,b)=(%.4f,%.4f) fa=%.4f fb=%.4f va=%.3f vb=%.3f' % row)
