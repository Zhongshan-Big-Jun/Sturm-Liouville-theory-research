# -*- coding: utf-8 -*-
"""H3 v11: full numerical suite - both parities, constants, explicit contradiction check."""
import numpy as np, math
from fractions import Fraction as F

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

print("=== mode structure, both parities ===")
for c in (1.0, 3.0, 10.0):
	for par, nm in (('e','even'), ('o','odd')):
		N = 300000
		u = scaled_z(c, par, N, 1.0, 0.0)
		v = scaled_z(c, par, N, 0.0, 1.0)
		# u/v at two points to check convergence to c/2
		g1, g2 = u[N//2]/v[N//2], u[N]/v[N]
		w = u - (c/2.0)*v
		R = w*np.sqrt(np.arange(N+1))
		gamma = R[300000]
		print("c={} {}: u/v at N/2,N = {:.8f},{:.8f} (c/2={}) ; z^w*sqrt(m)-> {:.6f}".format(c, nm, g1, g2, c/2.0, gamma))
		# sign checks
		print("    z^u>0: {}, z^v>0: {}, z^w sign const: {}".format(
			bool(np.all(u[1:]>0)), bool(np.all(v[1:]>0)), bool(np.all(np.sign(w[2:])==np.sign(w[2])))))
		# minimal-solution initial triple for this parity
		# (quick backward at moderate M)
		M = 60000
		r = np.array((1.0, 0.0, 0.0))
		j = M
		while j > 4:
			if par=='e':
				Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1); Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3); Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
			else:
				Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1); Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1); Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
			A_j = Pm/(4.0*c*j*j); B_j = -Qm/(16.0*j*j*(j-1)*(j-1)); C_j = c*Rm/(64.0*j*j*(j-1)*(j-1)*(j-2)*(j-2))
			newv = (r[0] - A_j*r[1] - B_j*r[2])/C_j
			r[2], r[1], r[0] = r[1], r[2], newv
			s = abs(r[0]) if abs(r[0]) > 1e-300 else 1.0
			r = r/s
			j -= 1
		print("    minimal (z0,z1,z2) up to scale: ({:.6f},{:.6e},{:.6e})".format(r[0]/r[0], r[1]/r[0], r[2]/r[0]))

print("")
print("=== explicit contradiction check (c=3, even, w-direction) ===")
c = 3.0; N = 50000
u = scaled_z(c, 'e', N, 1.0, 0.0)
v = scaled_z(c, 'e', N, 0.0, 1.0)
w = u - (c/2.0)*v
# nu_j for w: nu = z*(j!)^2*(4/c)^j, in log10
for j in (100, 500, 1000, 5000, 10000, 50000):
	lognu = math.log10(abs(w[j])) + 2*math.lgamma(j+1)/math.log(10.0) + j*math.log10(4.0/c)
	logbd = 0.5*math.log10(2.0/(4*j+1))  # log10 of L2 moment bound sqrt(2/(4j+1))
	print("  j={:6d}: log10|nu_j| = {:8.2f}  vs bound log10 = {:6.3f}".format(j, lognu, logbd))

print("")
print("=== exact rational values (c=3, even): u, v, w for small m ===")
cF = F(3)
def solve(cF, nu1, D, N):
	c = cF; nu = [F(0)]*(N+1); nu[1] = F(nu1)
	for j in range(2, N+1):
		Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
		Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
		Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
		Tm = F(4)*j*(4*j-5)
		rhs = Pm*nu[j-1] - Qm*nu[j-2] + (Rm*nu[j-3] if j>=3 else F(0)) + Tm*D
		nu[j] = rhs/(c*c)
	return nu
uE = solve(cF, 1, 0, 8); vE = solve(cF, 0, 1, 8)
print("  m : u_m | v_m | w_m = u - (3/2)v")
for m in range(1, 9):
	wm = uE[m] - F(3,2)*vE[m]
	print("  {}: {} | {} | {}".format(m, uE[m], vE[m], wm))
