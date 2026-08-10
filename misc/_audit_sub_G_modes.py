# _audit_sub_G_modes.py - E3 cross-checks: lem:modes, parity split, phase-branch identification, signs on line
import numpy as np
from scipy.optimize import brentq

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

def Yp(s, a, b, m, x):
	# y' piecewise
	res = np.empty_like(x)
	left = x <= a
	mid = (x > a) & (x < b)
	right = x >= b
	res[left] = np.cos(s*x[left])
	sa = s*a
	theta = m*s*(b-a)
	ya = np.sin(sa)/s
	ypa = np.cos(sa)
	res[mid] = -ya*m*s*np.sin(m*s*(x[mid]-a)) + ypa*np.cos(m*s*(x[mid]-a))
	sb = s*(1-b)
	yb = (np.cos(theta)*np.sin(sa) + np.sin(theta)/m*np.cos(sa))/s
	C = s*yb/np.sin(sb)
	res[right] = -C*np.cos(s*(1-x[right]))
	return res

# ---- lem:modes checks on asymmetric configurations
ModesOK = True
for (Rv, a, b) in [(1.5, 0.2, 0.6), (4.0, 0.3, 0.8), (10.0, 0.15, 0.45)]:
	m = np.sqrt(Rv)
	s1, s2 = Eigenvalues(a, b, m)
	xs = np.linspace(1e-6, 1-1e-6, 2000)
	y1 = Eigenfunction(s1, a, b, m, xs)
	y2 = Eigenfunction(s2, a, b, m, xs)
	if np.min(y1) < 0:
		ModesOK = False
		break
	if Yp(s1, a, b, m, np.array([1.0]))[0] >= 0:
		ModesOK = False
		break
	if Yp(s2, a, b, m, np.array([1.0]))[0] <= 0:
		ModesOK = False
		break
	sgn = np.sign(y2)
	changes = np.sum(sgn[1:] != sgn[:-1])
	if changes != 1:
		ModesOK = False
		break
	if y2[0] <= 0 or y2[-1] >= 0:
		ModesOK = False
		break
Check("E3: lem:modes: y1>0, y1'(1)<0, y2 one zero with y2>0 before, <0 after, y2'(1)>0", ModesOK)

# ---- parity split on the symmetric line
ParityOK = True
for (Rv, xi) in [(1.5, 0.2), (4.0, 0.3), (10.0, 0.42)]:
	m = np.sqrt(Rv)
	s1, s2 = Eigenvalues(xi, 1-xi, m)
	t = 0.05
	pts = np.array([xi + t, 1 - (xi + t), xi])
	y1p = Eigenfunction(s1, xi, 1-xi, m, pts)
	y2p = Eigenfunction(s2, xi, 1-xi, m, pts)
	if abs(y1p[0] - y1p[1]) > 1e-9:
		ParityOK = False
		break
	if abs(y2p[0] + y2p[1]) > 1e-9:
		ParityOK = False
		break
	if abs(Yp(s1, xi, 1-xi, m, np.array([0.5]))[0]) > 1e-7:
		ParityOK = False
		break
	if abs(Eigenfunction(s2, xi, 1-xi, m, np.array([0.5]))[0]) > 1e-9:
		ParityOK = False
		break
Check("E3: symmetric line: y1 even, y2 odd, y1'(1/2)=0 (Neumann), y2(1/2)=0 (Dirichlet)", ParityOK)

# ---- phase-branch identification: actual alpha_k satisfy E/O phase equations
BranchOK = True
for (Rv, xi) in [(1.5, 0.1), (1.5, 0.3), (4.0, 0.2), (4.0, 0.42), (10.0, 0.35), (100.0, 0.45)]:
	m = np.sqrt(Rv)
	q = m
	c = q*(0.5-xi)/xi
	s1, s2 = Eigenvalues(xi, 1-xi, m)
	a1 = s1*xi
	a2 = s2*xi
	E = lambda xx: np.arctan(1/(q*np.tan(xx)))
	if abs(E(a1) - c*a1) > 1e-7:
		BranchOK = False
		break
	if not (0 < a1 < PI/2):
		BranchOK = False
		break
	O = lambda xx: (PI - np.arctan(q*np.tan(xx)) if xx < PI/2 else np.arctan(-q*np.tan(xx)))
	if abs(O(a2) - c*a2) > 1e-7:
		BranchOK = False
		break
	if not (0 < a2 < PI):
		BranchOK = False
		break
	# c alpha1 in (0, pi/2): even-mode barrier phase stays below pi/2
	if not (0 < c*a1 < PI/2):
		BranchOK = False
		break
	# tan matching equations
	if abs(np.tan(a1)*np.tan(c*a1)*q - 1) > 1e-7:
		BranchOK = False
		break
	if abs(q*np.tan(a2) + np.tan(c*a2)) > 1e-7:
		BranchOK = False
		break
Check("E3: phase-branch identification: actual alpha_k solve E/O equations, branches correct, matching holds", BranchOK)

# ---- signs automatic on the symmetric line: v(xi) > 0, v(1-xi) < 0 for ANY xi in (0,1/2)
SignOK = True
for (Rv, xi) in [(1.5, 0.1), (1.5, 0.49), (4.0, 0.2), (10.0, 0.3), (100.0, 0.45)]:
	m = np.sqrt(Rv)
	s1, s2 = Eigenvalues(xi, 1-xi, m)
	pts = np.array([xi, 1-xi])
	y1 = Eigenfunction(s1, xi, 1-xi, m, pts)
	y2 = Eigenfunction(s2, xi, 1-xi, m, pts)
	va = y2[0]/y1[0]
	vb = y2[1]/y1[1]
	if not (va > 0 and vb < 0):
		SignOK = False
		break
Check("E3: on symmetric line v(xi) > 0 and v(1-xi) < 0 automatically (any xi in (0,1/2))", SignOK)

# ---- alpha_k'(c) formula (eq:alphap) against numerical differentiation of actual phases
DerivOK = True
for (Rv, xi) in [(4.0, 0.2), (4.0, 0.42)]:
	q = np.sqrt(Rv)
	h = 1e-6
	for xi2 in [xi, xi + h*2]:
		pass
	# c(xi): c = q(0.5-xi)/xi ; alpha1 = s1(xi)*xi ; compare d alpha1/dc from chain rule
	# dc/dxi = -q/(2 xi^2);  d alpha1/dxi via finite diff of (s1(xi)*xi)
	cp = -q/(2*xi**2)
	for k in [0, 1]:
		sA = Eigenvalues(xi, 1-xi, q)[k]
		sB = Eigenvalues(xi+h, 1-xi-h, q)[k]
		dA = (sB*(xi+h) - sA*xi)/h
		cA = (q*(0.5-(xi+h))/(xi+h) - q*(0.5-xi)/xi)/h
		alpha = sA*xi
		Phi = np.cos(alpha)**2 + q**2*np.sin(alpha)**2
		pred = -alpha*Phi/(q + cA*0 + (q*(0.5-xi)/xi)*Phi)   # using c at xi
		cval = q*(0.5-xi)/xi
		pred = -alpha*Phi/(q + cval*Phi)
		if abs(dA/cA - pred) > 1e-3*max(1.0, abs(pred)):
			DerivOK = False
			break
	if not DerivOK:
		break
Check("E3: eq:alphap alpha_k'(c) = -alpha Phi/(q + c Phi) matches numerical chain-rule derivative", DerivOK)

print("G_modes: PASS=%d FAIL=%d" % (PassCount, FailCount))
