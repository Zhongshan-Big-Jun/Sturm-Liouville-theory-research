# -*- coding: utf-8 -*-
"""H3 v12: odd-parity w = u - (c/2)v structure - measure slope."""
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

c = 1.0
N = 300000
for par in ('e','o'):
	u = scaled_z(c, par, N, 1.0, 0.0)
	v = scaled_z(c, par, N, 0.0, 1.0)
	w = u - (c/2.0)*v
	ms = np.arange(2, N+1)
	aw = np.abs(w[2:])
	sl, _ = np.linalg.lstsq(np.vstack([np.log(ms), np.ones_like(ms)]).T, np.log(aw+1e-300), rcond=None)[0]
	sl2, _ = np.linalg.lstsq(np.vstack([np.log(ms[100000:]), np.ones_like(ms[100000:])]).T, np.log(aw[100000:]+1e-300), rcond=None)[0]
	print("par={}: log-log slope of |z^w| over [2,N]: {:.5f} ; over [1e5,N]: {:.5f}".format(par, sl, sl2))
	for m in (10, 100, 1000, 10000, 100000, 200000, 300000):
		print("    m={:7d}: z^w={:12.6e}  z^w*sqrt(m)={:12.4f}".format(m, w[m], w[m]*math.sqrt(m)))
	# also log-log slope of z^v and z^u
	for name, zz in (('u', u), ('v', v)):
		az = np.abs(zz[100000:])
		slz, _ = np.linalg.lstsq(np.vstack([np.log(ms[100000:]), np.ones_like(ms[100000:])]).T, np.log(az+1e-300), rcond=None)[0]
		print("    {} slope [1e5,N]: {:.5f}".format(name, slz))
