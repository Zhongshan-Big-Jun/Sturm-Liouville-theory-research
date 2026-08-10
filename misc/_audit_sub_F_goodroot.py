# _audit_sub_F_goodroot.py - E3 cross-checks (v4, final)
import numpy as np
from scipy.optimize import root, brentq

PassCount = 0
FailCount = 0

def Check(Name, Cond):
	global PassCount, FailCount
	if Cond:
		PassCount += 1
		print("PASS", Name)
	else:
		FailCount += 1
		print("FAIL", Name)

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
	left = x <= a
	mid = (x > a) & (x < b)
	right = x >= b
	res[left] = np.sin(s*x[left])/s
	sa = s*a
	theta = m*s*(b-a)
	ya = np.sin(sa)/s
	ypa = np.cos(sa)
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

def IsInterior(a, b):
	return EPS < a and b < 1-EPS and a + EPS < b

def AllInteriorZeroRoots(Rval, coarse=80):
	aa = np.linspace(0.005, 0.4995, 400)
	vals = [Residuals(Rval, xi, 1-xi)[0] for xi in aa]
	roots = []
	for i in range(len(aa)-1):
		if vals[i]*vals[i+1] < 0:
			z = brentq(lambda t: Residuals(Rval, t, 1-t)[0], aa[i], aa[i+1])
			fa, fb, va, vb, _, _ = Residuals(Rval, z, 1-z)
			if IsInterior(z, 1-z):
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
			if abs(fa) + abs(fb) < 1.0:
				cands.append((a0, b0))
	cands.sort(key=lambda t: abs(Residuals(Rval, t[0], t[1])[0]) + abs(Residuals(Rval, t[0], t[1])[1]))
	seen = []
	for a0, b0 in cands[:40]:
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
		if not IsInterior(a, b):
			continue
		fa, fb, va, vb, _, _ = Residuals(Rval, a, b)
		if abs(fa) + abs(fb) > 1e-5:
			continue
		if any(abs(a-p[0]) < 0.02 and abs(b-p[1]) < 0.02 for p in roots):
			continue
		roots.append((a, b, va, vb, abs(fa)+abs(fb)))
	return roots

Check("sanity: uniform string (R=1) gives s1=pi, s2=2pi",
      abs(Eigenvalues(0.4, 0.6, 1.0)[0]-PI) < 1e-6 and abs(Eigenvalues(0.4, 0.6, 1.0)[1]-2*PI) < 1e-6)

RootData = {}
for Rv in [1.2, 1.5, 2.0, 4.0, 10.0, 100.0]:
	roots = AllInteriorZeroRoots(Rv)
	RootData[Rv] = roots
	sig = [r for r in roots if r[2] > 0 and r[3] < 0]
	Check("E3: R=%s: exactly one interior sign-consistent root, on a+b=1" % Rv,
		  len(sig) == 1 and abs(sig[0][0]+sig[0][1]-1) < 1e-6)
	Check("E3: R=%s: every other interior root fails sign condition" % Rv,
		  all(r is sig[0] or not (r[2] > 0 and r[3] < 0) for r in roots) if sig else len(roots) == 0)

# closed-triangle artifacts: R2 identically 0 on edge b=1; R1 has zeros there
EdgeOK = True
for a0 in [0.1, 0.3, 0.4438]:
	fa, fb, _, _, _, _ = Residuals(4.0, a0, 1.0 - 1e-9)
	if abs(fb) > 1e-8:
		EdgeOK = False
Check("E3: R2 = f(1) = 0 on the closed edge b=1 (R1=R2=0 artifacts there, outside open triangle)", EdgeOK)

def Jm(xx, m):
	return np.sin(xx)**2/(np.cos(xx)**2 + m**2*np.sin(xx)**2)

RigidOK = True
for Rv in [1.2, 1.5, 2.0, 4.0, 10.0, 100.0]:
	sig = [r for r in RootData[Rv] if r[2] > 0 and r[3] < 0]
	a, b = sig[0][0], sig[0][1]
	m = np.sqrt(Rv)
	s1, s2 = Eigenvalues(a, b, m)
	tau = s2/s1
	alpha = s1*a
	beta = s1*(1-b)
	if not (0 < alpha < PI/tau and 0 < beta < PI/tau):
		RigidOK = False
		break
	if abs(Jm(tau*alpha, m)/Jm(alpha, m) - Jm(tau*beta, m)/Jm(beta, m)) > 1e-7:
		RigidOK = False
		break
	if s2*a >= PI or s2*(1-b) >= PI:
		RigidOK = False
		break
Check("E3: good roots: phases in (0,pi/tau), r_tau(alpha)=r_tau(beta) (lem:phases+eq:rtaueq)", RigidOK)

def SolvePhaseN(qq, cc, branch):
	if branch == 0:
		return brentq(lambda xx: np.arctan(1/(qq*np.tan(xx))) - cc*xx, 1e-12, PI/2-1e-12)
	def f(xx):
		if xx < PI/2:
			return PI - np.arctan(qq*np.tan(xx)) - cc*xx
		return np.arctan(-qq*np.tan(xx)) - cc*xx
	return brentq(f, 1e-12, PI-1e-12)

def Ftilde(qq, cc):
	a1 = SolvePhaseN(qq, cc, 0)
	a2 = SolvePhaseN(qq, cc, 1)
	Phi = lambda xx: np.cos(xx)**2 + qq**2*np.sin(xx)**2
	Mf = lambda xx: xx**2*np.sin(xx)**2/(qq + cc*Phi(xx))
	return Mf(a1) - Mf(a2)

DimredOK = True
for Rv in [1.5, 4.0, 10.0]:
	q = np.sqrt(Rv)
	for xi in [0.1, 0.2, 0.3, 0.42]:
		c = q*(0.5-xi)/xi
		fa, fb, _, _, _, _ = Residuals(Rv, xi, 1-xi)
		RHS = 2*(c+q)/xi**2*Ftilde(q, c)
		if abs(fa - RHS) > 1e-6*max(1.0, abs(fa)):
			DimredOK = False
			break
	if not DimredOK:
		break
Check("E3: lem:dimred identity S_R(xi) = 2(c+q)/xi^2 Ftilde_e(c) sampled", DimredOK)

def LamK(a, b, m, k):
	return Eigenvalues(a, b, m)[k]**2

FhOK = True
for Rv in [1.5, 4.0, 10.0]:
	m = np.sqrt(Rv)
	for xi in [0.15, 0.3, 0.42]:
		h = 1e-5
		s1, s2 = Eigenvalues(xi, 1-xi, m)
		for k in [0, 1]:
			sk = (s1, s2)[k]
			d = (LamK(xi+h, 1-xi-h, m, k) - LamK(xi-h, 1-xi+h, m, k))/(2*h)
			y1 = Eigenfunction(sk, xi, 1-xi, m, np.array([xi]))
			nn = Norm(xi, 1-xi, m, sk)
			fh = (Rv-1)*sk**2*(2*y1[0]**2/nn)
			if abs(d - fh) > 1e-3*max(1.0, abs(d)):
				FhOK = False
				break
		if not FhOK:
			break
	if not FhOK:
		break
Check("E3: FH formula d lambda_k/d xi = (R-1) lambda_k (yhat^2(xi)+yhat^2(1-xi)) sampled", FhOK)

xi_lim = np.arccos(0.25)/PI
for eps in [0.02, 0.1]:
	Rv = 1 + eps
	roots = AllInteriorZeroRoots(Rv, coarse=90)
	sig = [r for r in roots if r[2] > 0 and r[3] < 0]
	Check("E3: R=1+%s: xi*=%.6f near arccos(1/4)/pi=%.6f" % (eps, sig[0][0] if sig else -1, xi_lim),
		  len(sig) == 1 and abs(sig[0][0] - xi_lim) < 0.02)

xiR = {}
for Rv in [4.0, 10.0, 100.0, 1000.0]:
	roots = AllInteriorZeroRoots(Rv, coarse=70)
	sig = [r for r in roots if r[2] > 0 and r[3] < 0]
	xiR[Rv] = sig[0][0] if sig else None
Check("E3: xi*(R) increasing for R=4,10,100,1000 (trend to 1/2)",
      None not in xiR.values() and xiR[4.0] < xiR[10.0] < xiR[100.0] < xiR[1000.0] and xiR[1000.0] < 0.5)

fa1, fb1, _, _, _, _ = Residuals(4.0, 0.4999, 0.5001)
fa0, fb0, _, _, _, _ = Residuals(4.0, 0.002, 0.998)
Check("E3: S_R(1/2-) ~ 2 pi^2 > 0 (uniform limit)", abs(fa1 - 2*PI**2) < 0.05)
Check("E3: S_R(xi) < 0 for small xi and -> 0 as xi -> 0+", fa0 < 0 and abs(fa0) < 0.1)

print("F_goodroot: PASS=%d FAIL=%d" % (PassCount, FailCount))
