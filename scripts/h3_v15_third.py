# -*- coding: utf-8 -*-
"""H3 v15: third homogeneous solution t (nu0=0, nu1=0, nu2=1, D=0): check it is NOT minimal.
If t ~ j^{-1/2} (nonzero), then minimal solution must have nu0 != 0."""
import numpy as np, math

def scaled_z(c, parity, N, nu1, src, nu2_init=0.0):
	lam = 4.0/c
	z = np.zeros(N+1); z[1] = nu1/lam
	if nu2_init != 0.0:
		# solve forward to get z2 exactly from nu2=1: z2 = 1/((2!)^2 lam^2)
		z[2] = 1.0/(4.0*lam*lam)
	lfac = [math.lgamma(j+1) for j in range(N+1)]
	for j in range(3, N+1):
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

print("=== homogeneous solution t (nu0=0, nu1=0, nu2=1): is it minimal? ===")
for c in (1.0, 3.0, 10.0):
	for par, nm in (('e','even'), ('o','odd')):
		N = 400000
		t = scaled_z(c, par, N, 0.0, 0.0, nu2_init=1.0)
		# local log-log slope
		ms = np.arange(2, N+1)
		at = np.abs(t[2:])
		for a, b in ((2, 1000), (100000, 400000)):
			mask = (ms >= a) & (ms <= b)
			sl, _ = np.linalg.lstsq(np.vstack([np.log(ms[mask]), np.ones_like(ms[mask])]).T, np.log(at[mask]+1e-300), rcond=None)[0]
			print("  c={} {}: slope t [{} , {}]: {:.4f}".format(c, nm, a, b, sl))
		print("     t scaled by m^-1/2 at 1e5,4e5: {:.4e}, {:.4e}".format(t[100000]/math.sqrt(100000), t[400000]/math.sqrt(400000)))
		if par=='o':
			print("     t scaled by m^1/2 at 1e5,4e5: {:.4e}, {:.4e}".format(t[100000]*math.sqrt(100000), t[400000]*math.sqrt(400000)))
