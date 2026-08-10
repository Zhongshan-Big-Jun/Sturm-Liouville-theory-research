# -*- coding: utf-8 -*-
"""H3 v8: correct gamma = c/2 combination; measure z^w decay/limit; minimal solution."""
import numpy as np, math

def scaled_z(c, parity, N, nu1, src, src_max=10**9):
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
		if src != 0.0 and j <= src_max:
			logs = math.log(abs(Tm*src)) - 2*lfac[j] - j*math.log(lam)
			srcj = math.copysign(math.exp(logs), Tm*src) if abs(logs) < 700 else 0.0
		z[j] = (term + srcj)/(c*c)
	return z

print("=== key experiment: w = u - (c/2)*v, even parity ===")
for c in (1.0, 3.0, 10.0):
	N = 200000
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v = scaled_z(c, 'e', N, 0.0, 1.0)
	w = u - (c/2.0)*v
	aw = np.abs(w[2:])
	ms = np.arange(2, N+1)
	sl, _ = np.linalg.lstsq(np.vstack([np.log(ms), np.ones_like(ms)]).T, np.log(aw+1e-300), rcond=None)[0]
	print("c={}:".format(c))
	print("  log-log slope of |z^w| over [2,N]: {:.5f}".format(sl))
	sl2, _ = np.linalg.lstsq(np.vstack([np.log(ms[50000:]), np.ones_like(ms[50000:])]).T, np.log(aw[50000:]+1e-300), rcond=None)[0]
	print("  log-log slope over [50002,N]: {:.5f}".format(sl2))
	for m in (2, 10, 100, 1000, 10000, 50000, 100000, 200000):
		print("    m={}: z^w={:.6e}   z^w*sqrt(m)={:.4f}".format(m, w[m], w[m]*math.sqrt(m)))
	# sign pattern
	sgn = np.sign(w[3:])
	ncross = int(np.sum(sgn[1:] != sgn[:-1]))
	print("  sign changes in z^w over [3,N]:", ncross)
	# also v decay check: z^v * m^1/2
	zv = v*np.sqrt(ms)
	print("  z^v*sqrt(m) at N: {:.6f}".format(v[N]*math.sqrt(N)))
	print("  z^u*sqrt(m) at N: {:.6f}".format(u[N]*math.sqrt(N)))

print("")
print("=== minimal solution via backward iteration, measure decay rate ===")
c = 3.0
lam = 4.0/c
M = 400000
r = np.array((1.0, 0.0, 0.0), dtype=float)
# backward: given z_{j}, z_{j-1}, z_{j-2} compute z_{j-3}
# z_m = A_m z_{m-1} + B_m z_{m-2} + C_m z_{m-3}  =>  C_m z_{m-3} = z_m - A_m z_{m-1} - B_m z_{m-2}
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
	j -= 1
print("minimal solution initial triple (z0,z1,z2) up to scale (c=3):", r)
print("  z0 != 0 ?", abs(r[0]) > 1e-9)
