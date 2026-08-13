# -*- coding: utf-8 -*-
"""R-209 route (iii): large-R continuation of the n=2 symmetric branch beyond
R ~ 7e3, via Newton on the UNSCALED closed 4-equation band/secular system
(see _gapn2_largeR_closed.py) with central finite-difference Jacobians,
convergence tested on |dz|, and log-R steps with halving/growth.

Records the asymptotic observables (K = k2/u, a = (p1-pi/2)/u^2,
b = (p3-pi/4)/u^2, Dk/u^7, D*R, M/u^5) at every step.

All numerics EVIDENCE.
"""
import sys
import json
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, r'scripts')
import _gapn2_largeR_closed as C


def jac_cs(z, eps):
	J = np.zeros((4, 4))
	for j in range(4):
		zc = z.astype(complex)
		zc[j] += 1e-20j
		J[:, j] = C.f_scaled(zc, eps).imag / 1e-20
	return J


def newton(z, eps, maxit=40):
	for it in range(maxit):
		f = C.f_scaled(z, eps)
		J = jac_cs(z, eps)
		try:
			dz = np.linalg.solve(J, f)
		except np.linalg.LinAlgError:
			return z, False
		if not np.all(np.isfinite(dz)):
			return z, False
		z = z - dz
		if np.max(np.abs(dz)) < 1e-11 * (1.0 + np.max(np.abs(z))):
			return z, True
	return z, False


def main():
	R0 = 6894.817068303348
	eps0 = 1.0 / np.sqrt(R0)
	z0 = np.array([0.8254090772942543, 0.8264512154938226,
		1.5995776512784283, 0.799370865594971])
	sol = least_squares(C.f_scaled, z0, args=(eps0,), method='lm',
		xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
	z = sol.x
	print('refined seed, max|f_scaled| = %.1e' %
		np.max(np.abs(C.f_scaled(z, eps0))))

	target = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
	step = 0.002
	rows = []
	logR = np.log(R0)
	count = 0
	while logR < target - 1e-9:
		logR += step
		Rnew = np.exp(logR)
		eps2 = 1.0 / np.sqrt(Rnew)
		znew, ok = newton(z, eps2)
		k2n, k3n, p1n, p3n = znew
		good = ok and k3n > k2n and np.pi / 2 < p1n < np.pi / 2 + 0.5 \
			and np.pi / 4 < p3n < np.pi / 4 + 0.5 and 0.1 < k2n < 5.0
		if not good:
			logR -= step
			step *= 0.5
			if step < 1e-8:
				print('GAVE UP at logR=%.4f' % logR)
				break
			continue
		z = znew
		step = min(step * 1.5, 0.05)
		k2, k3, p1, p3 = z
		u = eps2 ** (1.0 / 3.0)
		K = k2 / u
		q1 = p1 - np.pi / 2
		q3 = p3 - np.pi / 4
		Dk = k3 - k2
		D = k3 * k3 - k2 * k2
		p2 = k2 / 2 - eps2 * (p1 + p3)
		M = eps2 * np.cos(p2) * np.sin(p1) + np.sin(p2) * np.cos(p1)
		row = [Rnew, u, K, q1 / u ** 2, q3 / u ** 2, Dk / u ** 7,
			D * Rnew, M / u ** 5]
		rows.append(row)
		count += 1
		if count % 25 == 0:
			print('R=%.4g u=%.4e K=%.6f a=%.6f b=%.6f Dk/u7=%.4f D*R=%.4f M/u5=%.4f'
				% (Rnew, u, K, q1 / u ** 2, q3 / u ** 2, Dk / u ** 7,
					D * Rnew, M / u ** 5))
		with open(r'scripts/_gapn2_largeR_big.json', 'w') as fh:
			json.dump(rows, fh)
	print('done, rows:', len(rows))


if __name__ == '__main__':
	main()
