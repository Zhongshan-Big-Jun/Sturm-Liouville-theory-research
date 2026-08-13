# -*- coding: utf-8 -*-
"""R-209 route (iii): exact closed-form 4-equation solver for the n=2 symmetric
branch, valid at arbitrarily large R (no spectral engine, no near-degeneracy
breakdown).

Unknowns: (k2, k3, p1, p3), eps = 1/sqrt(R); p1t = k3 p1/k2, p3t = k3 p3/k2,
p2 = k2/2 - eps(p1+p3), p2t = k3/2 - eps(p1t+p3t) = k3/2 - eps(k3/k2)(p1+p3).

Equations (exact, verified at R=350 to 1e-12/1e-16 against the spectral engine):
  E1 = cos p2 sin(p1+p3) + sin p2 cos p3 cos p1/eps - eps sin p3 sin p2 sin p1
  E2 = cos p2t cos p1t cos p3t - sin p3t sin p2t cos p1t/eps
       - sin p3t cos p2t sin p1t - eps cos p3t sin p2t sin p1t
  E5 = I_D sin^2 p1t - I_N sin^2 p1      (band at x1)
  E6 = sin p1(eps cos p2t + sin p2t cot p1t) + eps cos p2 sin p1
       + sin p2 cos p1                   (band at x2)
with the exact mass integrals I_D (sin inner block), I_N (cos inner block);
left-half norm = 1/2 each.  E5, E6 are O(eps^2) at solutions and are scaled
by 1/eps^2 for conditioning.

All results EVIDENCE; the equation system is exact.
"""
import sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, r'scripts')


def mass(k, p1, p2, p3, eps, mode):
	if mode == 'D':
		BC = -(eps*np.cos(p2)*np.sin(p1)/k + np.sin(p2)*np.cos(p1)/k)/np.sin(p3)
		m3 = BC**2*(p3 - np.sin(2*p3)/2)/(2*k*eps)
	else:
		BC = (eps*np.cos(p2)*np.sin(p1)/k + np.sin(p2)*np.cos(p1)/k)/np.cos(p3)
		m3 = BC**2*(p3 + np.sin(2*p3)/2)/(2*k*eps)
	m1 = (p1 - np.sin(2*p1)/2)*eps/(2*k**3)
	a = eps*np.sin(p1)/k
	b = np.cos(p1)/k
	mL = ((a*a + b*b)*p2/(2*k) + (a*a - b*b)*np.sin(2*p2)/(4*k)
		+ a*b*(1 - np.cos(2*p2))/(2*k))
	return m1 + m3 + mL


def system(z, eps):
	k2, k3, p1, p3 = z
	p1t = k3*p1/k2
	p3t = k3*p3/k2
	p2 = k2/2 - eps*(p1 + p3)
	p2t = k3/2 - eps*k3/k2*(p1 + p3)
	E1 = (np.cos(p2)*np.sin(p1 + p3) + np.sin(p2)*np.cos(p3)*np.cos(p1)/eps
		- eps*np.sin(p3)*np.sin(p2)*np.sin(p1))
	E2 = (np.cos(p2t)*np.cos(p1t)*np.cos(p3t)
		- np.sin(p3t)*np.sin(p2t)*np.cos(p1t)/eps
		- np.sin(p3t)*np.cos(p2t)*np.sin(p1t)
		- eps*np.cos(p3t)*np.sin(p2t)*np.sin(p1t))
	ID = mass(k2, p1, p2, p3, eps, 'D')
	IN = mass(k3, p1t, p2t, p3t, eps, 'N')
	E5 = ID*np.sin(p1t)**2 - IN*np.sin(p1)**2
	E6 = (np.sin(p1)*(eps*np.cos(p2t) + np.sin(p2t)*np.cos(p1t)/np.sin(p1t))
		+ eps*np.cos(p2)*np.sin(p1) + np.sin(p2)*np.cos(p1))
	return np.array([E1, E2, E5, E6])


def f_scaled(z, eps):
	s = system(z, eps)
	return np.array([s[0], s[1], s[2]/eps**2, s[3]/eps**2])


def seed_from_engine(R0, mode):
	import json
	from _gapn2_symmetry_recon import Recon
	from _gapn2_jacobian_probe import symmetric_root
	from _gapn2_jacobian_analytic import eigen_data
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	e0 = np.array(tab['n2_%s' % mode.upper()]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	zprev = rc0.widths_to_z(w0)
	rc = Recon(2, R0, mode)
	zs = symmetric_root(rc, zprev)
	ed = eigen_data(rc, zs)
	lam2, lam3 = ed['lam_n'], ed['lam_np1']
	k2 = np.sqrt(lam2)
	k3 = np.sqrt(lam3)
	x1, x2 = ed['edges'][0], ed['edges'][1]
	kap2 = np.sqrt(lam2*R0)
	p1 = kap2*x1
	p3 = kap2*(0.5 - x2)
	return np.array([k2, k3, p1, p3])


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 350.0
	Rend = float(sys.argv[3]) if len(sys.argv) > 3 else 1e7
	step = float(sys.argv[4]) if len(sys.argv) > 4 else 1.3
	z = seed_from_engine(R0, mode)
	print('seed (unrefined):', z)
	R = R0
	while R <= Rend*1.0001:
		eps = 1/np.sqrt(R)
		sol = least_squares(f_scaled, z, args=(eps,), xtol=1e-14, ftol=1e-14,
			gtol=1e-14, max_nfev=400, diff_step=1e-7)
		z = sol.x
		res = f_scaled(z, eps)
		k2v, k3v, p1v, p3v = z
		D = k3v*k3v - k2v*k2v
		print('R=%12.4g k2=%.10f k3=%.10f p1=%.10f p3=%.10f D*R=%.8f |res|=%.2e'
			% (R, k2v, k3v, p1v, p3v, D*R, np.max(np.abs(res))))
		if np.max(np.abs(res)) > 1e-8:
			print('WARNING: large residual, stopping')
			break
		R *= step


if __name__ == '__main__':
	main()
