# -*- coding: utf-8 -*-
"""H3 v10: minimal solution decay fit (j, j*ln j, j^2), exact series of coefficients."""
import numpy as np, math

def backward_track(c, parity, M, samples):
	lam = 4.0/c
	r = np.array((1.0, 0.0, 0.0), dtype=float)
	logacc = 0.0
	out = {}
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
		if j in samples:
			out[j] = logacc + math.log10(abs(r[0]))
		j -= 1
	return out, (r[0], r[1], r[2])

c = 3.0
samples = [2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 400000]
res, triple = backward_track(c, 'e', 400000, samples)
print("c=3 minimal (z0,z1,z2) up to scale:", tuple(round(v,6) for v in triple))
js = sorted(res.keys())
print("samples (j, log10|z_j|):")
for j in js:
	print("  j={:6d}  log10={:12.4f}".format(j, res[j]))
# fits
ls = np.array([res[j] for j in js]); J = np.array(js, dtype=float)
# model 1: log10 = a + b*j
A1 = np.vstack([J, np.ones_like(J)]).T
b1 = np.linalg.lstsq(A1, ls, rcond=None)[0]
r1 = np.sum((A1@b1-ls)**2)
# model 2: log10 = a + b*j*ln j
A2 = np.vstack([J*np.log(J), np.ones_like(J)]).T
b2 = np.linalg.lstsq(A2, ls, rcond=None)[0]
r2 = np.sum((A2@b2-ls)**2)
# model 3: log10 = a + b*j^2
A3 = np.vstack([J*J, np.ones_like(J)]).T
b3 = np.linalg.lstsq(A3, ls, rcond=None)[0]
r3 = np.sum((A3@b3-ls)**2)
# model 4: log10 = a + b*j + c*j*ln j
A4 = np.vstack([J, J*np.log(J), np.ones_like(J)]).T
b4 = np.linalg.lstsq(A4, ls, rcond=None)[0]
r4 = np.sum((A4@b4-ls)**2)
print("fit residuals: j-linear: {:.6e} | j*lnj: {:.6e} | j^2: {:.6e} | j + jlnj: {:.6e}".format(r1,r2,r3,r4))
print("  j*lnj fit: log10|z| = {:.6f} * j ln j + {:.3f}".format(b2[0], b2[1]))
print("  j+jlnj fit: log10|z| = {:.6f} j + {:.6f} j ln j + {:.3f}".format(b4[0], b4[1], b4[2]))
# local slopes
print("local slopes d(log10)/dj on intervals:")
for i in range(len(js)-1):
	j1, j2 = js[i], js[i+1]
	print("  [{} , {}]: {:.4f}".format(j1, j2, (res[j2]-res[j1])/(j2-j1)))
