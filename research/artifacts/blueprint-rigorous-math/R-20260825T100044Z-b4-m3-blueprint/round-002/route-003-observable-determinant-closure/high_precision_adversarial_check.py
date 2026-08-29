"""High-precision adversarial check; this file is EVIDENCE, not proof.

It solves the exact four closed equations at two small positive u values,
compares the reduced-Green delta-jet formula with a direct pole-subtracted
limit, and evaluates the two determinant ratios in the frozen orthonormal
mirror conventions.  Only mpmath is used.
"""

from __future__ import annotations

import mpmath as mp


mp.mp.dps = 100
p = mp.pi
kappa = (18*p-48/p)**(mp.mpf(1)/3)


def inv2(a):
	det = a[0][0]*a[1][1]-a[0][1]*a[1][0]
	return [[a[1][1]/det, -a[0][1]/det], [-a[1][0]/det, a[0][0]/det]]


def det2(a):
	return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def mass(k, p1, p2, p3, eps, boundary):
	if boundary == "D":
		bc = -(eps*mp.cos(p2)*mp.sin(p1)/k+mp.sin(p2)*mp.cos(p1)/k)/mp.sin(p3)
		m3 = bc**2*(p3-mp.sin(2*p3)/2)/(2*k*eps)
	else:
		bc = (eps*mp.cos(p2)*mp.sin(p1)/k+mp.sin(p2)*mp.cos(p1)/k)/mp.cos(p3)
		m3 = bc**2*(p3+mp.sin(2*p3)/2)/(2*k*eps)
	m1 = (p1-mp.sin(2*p1)/2)*eps/(2*k**3)
	a, b = eps*mp.sin(p1)/k, mp.cos(p1)/k
	middle = (a*a+b*b)*p2/(2*k)+(a*a-b*b)*mp.sin(2*p2)/(4*k)+a*b*(1-mp.cos(2*p2))/(2*k)
	return m1+m3+middle, m3


def coordinates(u, K, B, X, Y):
	q0 = (18*p-24-K**3)/(6*K)
	q = q0+X*u**2
	C = 16/(p*K)+Y*u**2
	A = (2+q*u**2)/K
	k2 = K*u
	k3 = K*u+C*u**5
	p1 = p/2+A*u**2
	p3 = p/4+B*u**2
	p2 = k2/2-u**3*(p1+p3)
	ratio = k3/k2
	return k2, k3, p1, p2, p3, ratio*p1, ratio*p2, ratio*p3


def residual(u, K, B, X, Y):
	eps = u**3
	k2, k3, p1, p2, p3, p1t, p2t, p3t = coordinates(u, K, B, X, Y)
	ID, _ = mass(k2, p1, p2, p3, eps, "D")
	IN, _ = mass(k3, p1t, p2t, p3t, eps, "N")
	E1 = mp.cos(p2)*mp.sin(p1+p3)+mp.sin(p2)*mp.cos(p3)*mp.cos(p1)/eps-eps*mp.sin(p3)*mp.sin(p2)*mp.sin(p1)
	E2 = mp.cos(p2t)*mp.cos(p1t)*mp.cos(p3t)-mp.sin(p3t)*mp.sin(p2t)*mp.cos(p1t)/eps-mp.sin(p3t)*mp.cos(p2t)*mp.sin(p1t)-eps*mp.cos(p3t)*mp.sin(p2t)*mp.sin(p1t)
	E5 = ID*mp.sin(p1t)**2-IN*mp.sin(p1)**2
	E6 = mp.sin(p1)*(eps*mp.cos(p2t)+mp.sin(p2t)*mp.cos(p1t)/mp.sin(p1t))+eps*mp.cos(p2)*mp.sin(p1)+mp.sin(p2)*mp.cos(p1)
	return E1/u**4, E2/u**4, E5/u**6, E6/u**7


def branch_seed(u):
	K2 = (-272*p**2+576+81*p**4)/(30*p*(3*p**2-8))
	B2 = -(-272*p**2-480*p+576+180*p**3+81*p**4)/(30*p*kappa**2*(3*p**2-8))
	X0 = -(kappa**6-90*p*kappa**3+120*kappa**3-1620*p**2-3360+4320*p)/(360*kappa**2)
	X2 = (-306180*p**7-2462336*p**4-3465216-16896*p**2+3870720*p+698880*p**3+816480*p**5+413424*p**6+59049*p**8)/(37800*p**2*(3*p**2-8)**2)
	Y0 = 4*(p*kappa**3-96+36*p**2)/(3*p**2*kappa**2)
	Y2 = 2*(-792*p**2-160*p+1536+81*p**4)/(15*p**2*(3*p**2-8))
	return kappa+K2*u**2, 1/kappa+B2*u**2, X0+X2*u**2, Y0+Y2*u**2


def left_values(wave, k2, p1, p2, eps):
	scale = wave/k2
	a, b = scale*p1, scale*p2
	qh, ql = wave/eps, wave
	y1, dy1 = mp.sin(a)/qh, mp.cos(a)
	y2 = y1*mp.cos(b)+dy1*mp.sin(b)/ql
	dy2 = -ql*y1*mp.sin(b)+dy1*mp.cos(b)
	return [y1, y2], [dy1, dy2]


def stiffness(wave, k2, p1, p2, p3, eps, boundary):
	scale = wave/k2
	a, b, c = scale*p1, scale*p2, scale*p3
	qh, ql = wave/eps, wave
	a11 = qh/mp.tan(a)+ql/mp.tan(b)
	a12 = -ql/mp.sin(b)
	a22 = ql/mp.tan(b)+(qh/mp.tan(c) if boundary == "D" else -qh*mp.tan(c))
	return [[a11, a12], [a12, a22]]


def reduced_green_jet(wave, k2, phases, eps, boundary):
	p1, p2, p3 = phases
	qh, ql = wave/eps, wave

	def cot(q, x):
		co, si = mp.cos(x), mp.sin(x); ct, cs = co/si, 1/si
		return q*ct, q*(ct-x*cs**2), q*(-x*cs**2+x**2*cs**2*ct)

	def csc(q, x):
		co, si = mp.cos(x), mp.sin(x); cs, ct = 1/si, co/si
		return q*cs, q*(cs-x*cs*ct), q*(-x*cs*ct+x**2*cs*(ct**2+cs**2)/2)

	def tan(q, x):
		tn, sc = mp.tan(x), 1/mp.cos(x)
		return q*tn, q*(tn+x*sc**2), q*(x*sc**2+x**2*sc**2*tn)

	h1, l2, x2 = cot(qh, p1), cot(ql, p2), csc(ql, p2)
	h3 = cot(qh, p3) if boundary == "D" else tan(qh, p3)
	jet = []
	for n in range(3):
		jet.append([[h1[n]+l2[n], -x2[n]], [-x2[n], l2[n]+h3[n] if boundary == "D" else l2[n]-h3[n]]])
	a0, a1, a2 = jet
	d1 = a1[0][0]*a0[1][1]+a0[0][0]*a1[1][1]-2*a0[0][1]*a1[0][1]
	d2 = a2[0][0]*a0[1][1]+a1[0][0]*a1[1][1]+a0[0][0]*a2[1][1]-a1[0][1]**2-2*a0[0][1]*a2[0][1]
	n0 = [[a0[1][1], -a0[0][1]], [-a0[1][0], a0[0][0]]]
	n1 = [[a1[1][1], -a1[0][1]], [-a1[1][0], a1[0][0]]]
	return [[n1[i][j]/d1-n0[i][j]*d2/d1**2+n0[i][j]/(2*d1) for j in range(2)] for i in range(2)]


def reduced_green_limit(wave, k2, phases, eps, boundary, y, norm):
	h = mp.mpf("1e-35")
	projection = [[y[i]*y[j]/norm for j in range(2)] for i in range(2)]
	out = []
	for sign in (-1, 1):
		delta = sign*h
		z = wave*(1+delta)
		G = inv2(stiffness(z, k2, phases[0], phases[1], phases[2], eps, boundary))
		den = wave**2-z**2
		out.append([[G[i][j]-projection[i][j]/den for j in range(2)] for i in range(2)])
	return [[(out[0][i][j]+out[1][i][j])/2 for j in range(2)] for i in range(2)]


def check(u):
	initial = branch_seed(u)
	K, B, X, Y = mp.findroot(lambda K, B, X, Y: residual(u, K, B, X, Y), initial, tol=mp.mpf("1e-80"), maxsteps=100)
	res = max(abs(z) for z in residual(u, K, B, X, Y))
	eps = u**3
	k2, k3, p1, p2, p3, p1t, p2t, p3t = coordinates(u, K, B, X, Y)
	ID, _ = mass(k2, p1, p2, p3, eps, "D")
	IN, _ = mass(k3, p1t, p2t, p3t, eps, "N")
	yD, dyD = left_values(k2, k2, p1, p2, eps)
	yN, dyN = left_values(k3, k2, p1, p2, eps)
	W = [yD[j]*dyN[j]-yN[j]*dyD[j] for j in range(2)]
	GD = inv2(stiffness(k3, k2, p1, p2, p3, eps, "D"))
	GN = inv2(stiffness(k2, k2, p1, p2, p3, eps, "N"))
	GtD = reduced_green_jet(k2, k2, (p1, p2, p3), eps, "D")
	GtN = reduced_green_jet(k3, k3, (p1t, p2t, p3t), eps, "N")
	limD = reduced_green_limit(k2, k2, (p1, p2, p3), eps, "D", yD, ID)
	limN = reduced_green_limit(k3, k3, (p1t, p2t, p3t), eps, "N", yN, IN)
	finite_error = max(abs(GtD[i][j]-limD[i][j]) for i in range(2) for j in range(2))
	finite_error = max(finite_error, max(abs(GtN[i][j]-limN[i][j]) for i in range(2) for j in range(2)))
	c = k2/k3
	d = [-c*abs(w)/(mp.sqrt(ID*IN)*(u**-6-1)) for w in W]
	UD = [z/mp.sqrt(2*ID) for z in yD]
	e = [1, -1]
	Kp = [[2*k2**2*UD[i]*(e[i]*e[j]*GD[i][j]-c**2*GN[i][j])*UD[j]+(d[i] if i == j else 0) for j in range(2)] for i in range(2)]
	r = 2*k2**2*(k3**2-k2**2)/k3**4
	v = [z*z for z in UD]
	Ko = [[2*k2**2*UD[i]*(GtN[i][j]-c**2*e[i]*e[j]*GtD[i][j])*UD[j]+2*r*e[i]*v[i]*e[j]*v[j]+(d[i] if i == j else 0) for j in range(2)] for i in range(2)]
	cKp = 128*kappa**2/p**2
	cKo = 2048*kappa**2/p**4
	print("u=", mp.nstr(u, 8))
	print("scaled_residual=", mp.nstr(res, 8))
	print("finite_part_max_error=", mp.nstr(finite_error, 8))
	print("detKp/u^20=", mp.nstr(det2(Kp)/u**20, 30), " exact_lead=", mp.nstr(cKp, 30))
	print("detKo/u^26=", mp.nstr(det2(Ko)/u**26, 30), " exact_lead=", mp.nstr(cKo, 30))


if __name__ == "__main__":
	for value in (mp.mpf("0.08"), mp.mpf("0.05")):
		check(value)
