# -*- coding: utf-8 -*-
"""H3 v7: CORRECTED z-initialization (z1 = nu1/lam); validate vs exact fractions."""
from fractions import Fraction as F
import numpy as np, math

def scaled_z(c, parity, N, nu1, src, src_max=300):
	lam = 4.0/c
	z = np.zeros(N+1); z[1] = nu1/lam   # z_1 = nu_1 / lambda
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
		if src != 0.0 and j <= src_max:
			logs = math.log(abs(Tm*src)) - 2*lfac[j] - j*math.log(lam)
			srcj = math.copysign(math.exp(logs), Tm*src) if abs(logs) < 700 else 0.0
		z[j] = (term + srcj)/(c*c)
	return z

# validation vs exact fractions
def solve_even(cF, nu1, D, N):
	c = F(cF); nu = [F(0)]*(N+1); nu[1] = F(nu1)
	for j in range(2, N+1):
		Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
		Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
		Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
		Tm = F(4)*j*(4*j-5)
		rhs = Pm*nu[j-1] - Qm*nu[j-2] + (Rm*nu[j-3] if j >= 3 else F(0)) + Tm*D
		nu[j] = rhs/(c*c)
	return nu

c = 3
exact_u = solve_even(c, 1, 0, 10)
exact_v = solve_even(c, 0, 1, 10)
lam = 4.0/c
u = scaled_z(c, 'e', 10, 1.0, 0.0)
v = scaled_z(c, 'e', 10, 0.0, 1.0)
print("validation (m: exact_u vs float u, exact_v vs float v):")
ok = True
for m in range(0, 11):
	uf = u[m]*math.factorial(m)**2*lam**m
	vf = v[m]*math.factorial(m)**2*lam**m
	match_u = abs(uf - float(exact_u[m])) < 1e-9
	match_v = abs(vf - float(exact_v[m])) < 1e-9
	ok &= match_u and match_v
	print("  m={}: u exact={} float={:.6f} {} | v exact={} float={:.6f} {}".format(
		m, exact_u[m], uf, "OK" if match_u else "BAD", exact_v[m], vf, "OK" if match_v else "BAD"))
print("all match:", ok)

print("")
print("=== corrected asymptotics ===")
for c in (1.0, 3.0, 10.0):
	N = 100000
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v = scaled_z(c, 'e', N, 0.0, 1.0)
	print("c={}:".format(c))
	ms = np.arange(50000, 100001)
	sl, _ = np.linalg.lstsq(np.vstack([np.log(ms), np.ones_like(ms)]).T, np.log(u[50000:100001]), rcond=None)[0]
	print("  growth exponent of z^u over [50000,100000]: {:.5f}".format(sl))
	print("  ratio u/v at N: {:.8f}   (2c^2 = {})".format(u[-1]/v[-1], 2*c*c))
	w = u - 2*c*c*v
	print("  w[2] = {:.4f} (exact -38 for c=3)".format(w[2]))
	# z^w decay: z^w = w (already z-scaled); check z^w * sqrt(m)
	g = w*np.sqrt(np.arange(N+1))
	print("  z^w*sqrt(m) at m=100000: {:.6f}".format(g[-1]))
	# sign of z^w
	sgn = np.sign(w[2:])
	print("  sign of z^w for m in [2,100000]: all same =", bool(np.all(sgn==sgn[0])), " sign =", sgn[0])
