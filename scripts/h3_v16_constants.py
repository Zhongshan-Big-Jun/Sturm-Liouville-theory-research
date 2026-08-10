# -*- coding: utf-8 -*-
"""H3 v16: precise constants (Richardson) + ratio structure for the record."""
import numpy as np, math

def scaled_z(c, parity, N, nu1, src):
	lam = 4.0/c
	z = np.zeros(N+1); z[1] = nu1/lam
	lfac = [math.lgamma(j+1) for j in range(N+1)]
	for j in range(2, N+1):
		if parity=='e':
			Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
			Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
			Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
			Tm = 4.0*j*(4*j-5)
		else:
			Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
			Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
			Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
			Tm = 4.0*j*(4*j-3)
		term = Pm*z[j-1]/(lam*j*j) - Qm*z[j-2]/(lam*lam*j*j*(j-1)*(j-1))
		if j >= 3:
			term += Rm*z[j-3]/(lam**3*j*j*(j-1)*(j-1)*(j-2)*(j-2))
		srcj = 0.0
		if src != 0.0:
			logs = math.log(abs(Tm*src)) - 2*lfac[j] - j*math.log(lam)
			srcj = math.copysign(math.exp(logs), Tm*src) if abs(logs) < 700 else 0.0
		z[j] = (term + srcj)/(c*c)
	return z

print("=== constants (Richardson extrapolation on the tail) ===")
for c in (1.0, 3.0, 10.0):
	N = 1000000
	# even
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v = scaled_z(c, 'e', N, 0.0, 1.0)
	w = u - (c/2.0)*v
	# gamma_c = lim z^w*sqrt(m): Richardson on m1,2m1,4m1
	m1 = 250000
	g1 = w[m1]*math.sqrt(m1); g2 = w[2*m1]*math.sqrt(2*m1); g3 = w[4*m1]*math.sqrt(4*m1)
	gamma = g3 + (g3-g2)  # first-order extrapolation
	print("c={}: even gamma_c ~ {:.8f} (g at m,2m,4m: {:.6f},{:.6f},{:.6f})".format(c, gamma, g1, g2, g3))
	# beta_c = lim z^v/sqrt(m)
	b1 = v[m1]/math.sqrt(m1); b2 = v[2*m1]/math.sqrt(2*m1); b3 = v[4*m1]/math.sqrt(4*m1)
	beta = b3 + (b3-b2)
	print("       even beta_c ~ {:.8f}".format(beta))
	# odd
	uo = scaled_z(c, 'o', N, 1.0, 0.0)
	vo = scaled_z(c, 'o', N, 0.0, 1.0)
	wo = uo - (c/2.0)*vo
	# odd w ~ gp * m^{1/2}
	o1 = wo[m1]/math.sqrt(m1); o2 = wo[2*m1]/math.sqrt(2*m1); o3 = wo[4*m1]/math.sqrt(4*m1)
	gpo = o3 + (o3-o2)
	print("       odd  gamma'_c ~ {:.8f}".format(gpo))
	b1o = vo[m1]/(m1**1.5); b2o = vo[2*m1]/((2*m1)**1.5); b3o = vo[4*m1]/((4*m1)**1.5)
	bpo = b3o + (b3o-b2o)
	print("       odd  beta'_c ~ {:.8f}".format(bpo))

print("")
print("=== ratio structure for even v (c=3): r_j - 1 - 1/(2j) ===")
c = 3.0
N = 400000
v = scaled_z(c, 'e', N, 0.0, 1.0)
r = v[1:]/v[:-1]
ms = np.arange(1, N)
for m in (1000, 10000, 100000, 300000):
	print("  m={:7d}: r_m = {:.10f} ; r - 1 - 1/(2m) = {:.3e} ; r - 1 - 1/(2m) - c/(4m^2) = {:.3e}".format(
		m, r[m], r[m]-1-0.5/m, r[m]-1-0.5/m-c/(4*m*m)))
