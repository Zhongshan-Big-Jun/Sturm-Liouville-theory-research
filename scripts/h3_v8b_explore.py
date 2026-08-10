# -*- coding: utf-8 -*-
"""H3 v8b: constants of dominant modes, minimal solution decay rate."""
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

print("=== constants of modes (even) ===")
for c in (1.0, 3.0, 10.0):
	N = 300000
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v = scaled_z(c, 'e', N, 0.0, 1.0)
	g = u[N]/v[N]   # ratio -> c/2
	w = u - g*v     # exact null combination of sqrt(m) mode (using measured g)
	# residual: should be A/sqrt(m)
	r = w*N*np.sqrt(np.arange(N+1))  # r_j = z^w * j * sqrt(j) / ... hmm define R_j = z^w_j * sqrt(j)
	R = w*np.sqrt(np.arange(N+1))
	val = R[300000]
	val2 = R[200000]
	print("c={}: measured gamma=u/v={:.10f} (c/2={}) ; z^w*sqrt(m)-> {}".format(c, g, c/2.0, val))
	# asymptotic constant via Richardson-ish: extrapolate R at 3 different points
	R1, R2, R3 = R[100000], R[200000], R[300000]
	print("  R at 1e5, 2e5, 3e5: {:.8f}, {:.8f}, {:.8f}".format(R1, R2, R3))
	# now with exact gamma = c/2:
	w2 = u - (c/2.0)*v
	R2v = w2*np.sqrt(np.arange(N+1))
	print("  exact-gamma R at 1e5,2e5,3e5: {:.8f}, {:.8f}, {:.8f}".format(R2v[100000], R2v[200000], R2v[300000]))

print("")
print("=== minimal solution: backward iteration + decay rate ===")
for c in (1.0, 3.0, 10.0):
	lam = 4.0/c
	M = 300000
	r = np.array((1.0, 0.0, 0.0), dtype=float)
	# store tail values to measure decay
	tail = []
	j = M
	while j > 4:
		Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
		Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
		Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
		A_j = Pm/(4.0*c*j*j)
		B_j = -Qm/(16.0*j*j*(j-1)*(j-1))
		C_j = c*Rm/(64.0*j*j*(j-1)*(j-1)*(j-2)*(j-2))
		newv = (r[0] - A_j*r[1] - B_j*r[2])/C_j
		r[2], r[1], r[0] = r[1], r[2], newv
		s = abs(r[0]) if abs(r[0]) > 1e-300 else 1.0
		r = r/s
		if j in (5000, 10000, 50000, 100000, 200000, 299000):
			tail.append((j, r[0]))
		j -= 1
	print("c={}: initial triple (z0,z1,z2) up to scale: ({:.6e}, {:.6e}, {:.6e})".format(c, r[0], r[1], r[2]))
	# the backward iteration gives the minimal solution normalized so that z_M = 1 (roughly).
	# decay rate: z_j ~ exp(-kappa * j)? measure log(z_{j1}/z_{j2})/(j2-j1) along the tail
	print("  tail points (j, log10|z_j|):", [(j, math.log10(abs(v))) for j, v in tail])
