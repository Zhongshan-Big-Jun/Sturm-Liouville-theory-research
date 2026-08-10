# -*- coding: utf-8 -*-
"""H3 v13: odd parity local slopes + identify power exponents precisely."""
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

c = 3.0
N = 600000
par = 'o'
u = scaled_z(c, par, N, 1.0, 0.0)
v = scaled_z(c, par, N, 0.0, 1.0)
w = u - (c/2.0)*v
ms = np.arange(2, N+1)
for name, zz in (('u', u), ('v', v), ('w', w)):
	az = np.abs(zz[2:])
	print("=== {} local slopes ===".format(name))
	for a, b in ((2, 10000), (100000, 300000), (300000, 600000)):
		mask = (ms >= a) & (ms <= b)
		sl, _ = np.linalg.lstsq(np.vstack([np.log(ms[mask]), np.ones_like(ms[mask])]).T, np.log(az[mask]+1e-300), rcond=None)[0]
		print("  [{} , {}]: slope {:.5f}".format(a, b, sl))
	# test specific exponents: m^1.5, m^0.5, m^2.5 at tail
	idx = np.arange(400000, 600001)
	zzz = np.abs(zz[idx])
	for ex in (2.5, 1.5, 0.5, -0.5):
		val = zzz/np.power(idx, ex)
		print("  m^(-{}) scaled tail: {:.6e} (first), {:.6e} (last)  ratio: {:.4f}".format(-ex, val[0], val[-1], val[-1]/val[0]))
