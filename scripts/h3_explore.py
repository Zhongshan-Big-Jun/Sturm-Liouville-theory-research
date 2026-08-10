# -*- coding: utf-8 -*-
"""H3 exploration v3: z-asymptotics + minimal-combo decay (guarded R term)."""
from fractions import Fraction as F
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

print("=== Part 2: z-asymptotics ===")
for c in (1.0, 3.0, 5.0, 10.0):
	for par in ('e','o'):
		z1 = scaled_z(c, par, 6000, 1.0, 0.0)
		z2 = scaled_z(c, par, 6000, 0.0, 1.0)
		g = z1[-1]/z2[-1]
		zb = z1 - g*z2
		m = 5900
		print(f"  c={c} par={par}: z^u->{z1[-1]:.10f} z^v->{z2[-1]:.10f} gamma={g:.10f}")
		print(f"     zbal[{m}]={zb[m]:.4e} |zbal|*m={abs(zb[m])*m:.4e} |zbal|*m^2={abs(zb[m])*m*m:.4e}")
		rm = zb[m]/zb[m-1]
		print(f"     zbal ratio={rm:.8f} vs 1/m-decay={(m-1)/m:.8f} vs 1/m^2={((m-1)/m)**2:.8f}")
		ms = np.arange(4000, 6001)
		A = np.vstack([np.log(ms), np.ones_like(ms)]).T
		slope, _ = np.linalg.lstsq(A, np.log(np.abs(zb[4000:6001])+1e-300), rcond=None)[0]
		print(f"     log-log slope of |zbal| over [4000,6000]: {slope:.3f}")

print("=== Part 3: SVD minimal-growth decay rate ===")
for c in (3.0, 10.0):
	for par in ('e','o'):
		N = 60000
		u = scaled_z(c, par, N, 1.0, 0.0)
		v = scaled_z(c, par, N, 0.0, 1.0)
		print(f"  c={c} par={par}:")
		for win_end in (8000, 16000, 32000, 60000):
			L = 4000
			W = np.column_stack([u[win_end-L:win_end], v[win_end-L:win_end]])
			_, s, Vt = np.linalg.svd(W)
			x = Vt[-1]
			zmin = x[0]*u + x[1]*v
			a = win_end-1
			rate = abs(zmin[win_end])/abs(zmin[a])
			alpha = math.log(rate)/math.log(a/(a+1.0))
			print(f"    win_end={win_end}: params=({x[0]:.6f},{x[1]:.6f}) |zmin|={abs(zmin[win_end]):.3e} decay-slope~{alpha:.2f}")
