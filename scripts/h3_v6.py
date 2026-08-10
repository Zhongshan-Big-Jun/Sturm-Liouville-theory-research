# -*- coding: utf-8 -*-
"""H3 v6: FIXED source term; verify z^u/z^v limit and w structure with correct source."""
import numpy as np, math

def scaled_z(c, parity, N, nu1, src, src_max=200):
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
		if src != 0.0 and j <= src_max:
			logs = math.log(abs(Tm*src)) - 2*lfac[j] - j*math.log(lam)
			srcj = math.copysign(math.exp(logs), Tm*src) if abs(logs) < 700 else 0.0
		z[j] = (term + srcj)/(c*c)
	return z

for c in (1.0, 3.0, 10.0):
	N = 100000
	u = scaled_z(c, 'e', N, 1.0, 0.0)
	v1 = scaled_z(c, 'e', N, 0.0, 1.0, src_max=40)
	v2 = scaled_z(c, 'e', N, 0.0, 1.0, src_max=300)
	print("=== c={} ===".format(c))
	print("  z^v[100000] src_max=40: {:.10f}   src_max=300: {:.10f}".format(v1[-1], v2[-1]))
	print("  ratio u/v at N (src_max=300): {:.8f}  (2c^2 = {})".format(u[-1]/v2[-1], 2*c*c))
	# w with correct source
	w = u - 2*c*c*v2
	g = w*np.sqrt(np.arange(N+1))
	print("  g_m for w (correct source):")
	for m in (2, 3, 5, 20, 100, 1000, 10000, 100000):
		print("    m={}: g={:.6f}".format(m, g[m]))
	idx = np.where(np.sign(w[2:]) != np.sign(w[1:-1]))[0]
	cross = idx[0]+2 if len(idx) else None
	print("  crossover:", cross, "  g[100000]={:.8f}".format(g[-1]))
	# sign of w at m=2 (exact check: should be negative for c=3)
	print("  w[2] = {:.4f}".format(w[2]))
