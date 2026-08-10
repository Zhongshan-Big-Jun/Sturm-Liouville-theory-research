# -*- coding: utf-8 -*-
"""H3 v9: measure minimal solution decay (track scale), both parities."""
import numpy as np, math

def backward_minimal(c, parity, M, normalize_at=0):
	"""Backward iterate; return (z0,z1,z2) normalized + log10|z_j| samples."""
	lam = 4.0/c
	r = np.array((1.0, 0.0, 0.0), dtype=float)
	logacc = 0.0
	samples = []
	j = M
	while j > 4:
		if parity=='e':
			Pm = 8.0*c*j*j - 4.0*c*j + c*c*j/(j-1)
			Qm = 4.0*j*(j-1)*(2*j-1)*(2*j-3) + 4.0*c*j*(2*j-3)
			Rm = 4.0*j*(j-2)*(2*j-3)*(2*j-5)
		else:
			Pm = 8.0*c*j*j + 4.0*c*j + c*c*j/(j-1)
			Qm = 4.0*j*(j-1)*(2*j-1)*(2*j+1) + 4.0*c*j*(2*j-1)
			Rm = 4.0*j*(j-2)*(2*j-1)*(2*j-3)
		A_j = Pm/(4.0*c*j*j)
		B_j = -Qm/(16.0*j*j*(j-1)*(j-1))
		C_j = c*Rm/(64.0*j*j*(j-1)*(j-1)*(j-2)*(j-2))
		newv = (r[0] - A_j*r[1] - B_j*r[2])/C_j
		r[2], r[1], r[0] = r[1], r[2], newv
		s = abs(r[0]) if abs(r[0]) > 1e-300 else 1.0
		r = r/s
		logacc += math.log10(s)
		if j in (10000, 20000, 50000, 100000, 150000, 200000, 250000, 299000):
			samples.append((j, logacc + math.log10(abs(r[0]))))
		j -= 1
	# normalize to z_0 = 1
	s0 = r[0]
	z0, z1, z2 = r[0]/s0, r[1]/s0, r[2]/s0
	return z0, z1, z2, samples

print("=== minimal solution: initial triple + decay samples (log10|z_j|) ===")
for c in (1.0, 3.0, 10.0):
	for par, name in (('e','even'), ('o','odd')):
		z0, z1, z2, samples = backward_minimal(c, par, 300000)
		# fit log10|z_j| vs j on tail (should be linear if exponential decay)
		js = np.array([s[0] for s in samples]); lz = np.array([s[1] for s in samples])
		A = np.vstack([js, np.ones_like(js)]).T
		sl, ic = np.linalg.lstsq(A, lz, rcond=None)[0]
		# fit log|z| vs log j (power law)
		B = np.vstack([np.log(js), np.ones_like(js)]).T
		psl, pic = np.linalg.lstsq(B, lz, rcond=None)[0]
		print("c={} {}: (z0,z1,z2) ~ ({:.4f}, {:.4e}, {:.4e}) | log10|z| vs j: slope {:.6f} | vs log j: slope {:.4f}".format(
			c, name, z0, z1, z2, sl, psl))
		print("     samples:", [(j, round(v,3)) for j, v in samples])
		# estimate nu_j = z_j (j!)^2 (4/c)^j in log10: 2*lgamma(j+1) + j*log10(4/c) + lz
		for j, v in samples[-3:]:
			lnu = 2*math.lgamma(j+1)/math.log(10.0) + j*math.log10(4.0/c) + v
			print("       log10|nu_j| at j={}: {:.1f}".format(j, lnu))
