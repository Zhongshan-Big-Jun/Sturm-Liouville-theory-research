# -*- coding: utf-8 -*-
"""H3 decisive v5b (reduced N): g_m structure + subdominant backward iteration."""
import numpy as np, math

def scaled_z(c, parity, N, nu1, src):
	lam = 4.0/c
	z = np.zeros(N+1); z[1] = nu1
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
		if src != 0.0 and j <= 40:
			logs = math.log(abs(Tm*src)) - math.log(c*c) - 2*lfac[j] - j*math.log(lam)
			srcj = math.copysign(math.exp(logs), Tm*src) if abs(logs) < 700 else 0.0
		z[j] = (term + srcj)/(c*c)
	return z

for c in (1.0, 3.0, 10.0):
	N = 100000
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v = scaled_z(c, 'e', N, 0.0, 1.0)
	w = u - 2*c*c*v
	g = w*np.sqrt(np.arange(N+1))
	idx = np.where(np.sign(w[2:]) != np.sign(w[1:-1]))[0]
	cross = idx[0]+2 if len(idx) else None
	print("=== c={}: w = u - {}*v ===".format(c, 2*c*c))
	print("  crossover m:", cross)
	for m in (5, 20, 50, 200, 1000, 5000, 20000, 100000):
		print("    m={}: g={:.6f}".format(m, g[m]))
	tail = g[50000:]
	print("  g monotone increasing in [50000,100000]:", bool(np.all(np.diff(tail) > 0)))
	print("  g[100000] = {:.8f}".format(g[100000]))
	# find min of g
	mmin = np.argmin(g[2:])+2
	print("  min of g at m={}: g={:.4f}".format(mmin, g[mmin]))

print("")
print("=== subdominant mode backward iteration (M=200000) ===")
c = 3.0
lam = 4.0/c
M = 200000
for tail0 in ((1.0,0.5,0.25), (1.0,-0.3,0.7), (0.2,1.0,0.1)):
	r = np.array(tail0, dtype=float)
	j = M
	while j > 4:
		Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
		Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
		Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
		A_j = Pm/(lam*j*j); B_j = Qm/(lam*lam*j*j*(j-1)*(j-1))
		C_j = (lam**3*j*j*(j-1)*(j-1)*(j-2)*(j-2))/Rm
		newv = (c*c*r[0] - A_j*r[1] + B_j*r[2])*C_j
		r[2], r[1], r[0] = r[1], r[2], newv
		s = abs(r[0]) if abs(r[0]) > 1e-300 else 1.0
		r = r/s
		j -= 1
	print("  tail={}: (z0,z1,z2) = ({:.6e}, {:.6e}, {:.6e})".format(tail0, r[0], r[1], r[2]))
