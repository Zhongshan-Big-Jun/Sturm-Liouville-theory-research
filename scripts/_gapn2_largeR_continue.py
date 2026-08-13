# -*- coding: utf-8 -*-
"""R-209 route (iii): continuation of the n=2 symmetric branch to huge R via
the exact closed 4-equation system, in the well-scaled variables
(k2, k3, q1, p3) with p1 = pi/2 + eps*q1.  Saves the ladder to JSON for
scaling-law fits.  All EVIDENCE; the equation system is exact.

Usage: python _gapn2_largeR_continue.py [mode] [Rstart] [Rend] [step] [outjson]
"""
import sys
import json
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, r'scripts')
from _gapn2_largeR_closed import mass, seed_from_engine


def system_v(z, eps):
	k2, k3, q1, p3 = z
	p1 = np.pi/2 + eps*q1
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
	return np.array([E1, E2, E5/eps**2, E6/eps**2])


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 200.0
	Rend = float(sys.argv[3]) if len(sys.argv) > 3 else 1e8
	step = float(sys.argv[4]) if len(sys.argv) > 4 else 1.08
	out = sys.argv[5] if len(sys.argv) > 5 else 'scripts/_gapn2_largeR_ladder.json'
	z0 = seed_from_engine(R0, mode)
	k2, k3, p1, p3 = z0
	q1 = (p1 - np.pi/2)*np.sqrt(R0)
	z = np.array([k2, k3, q1, p3])
	rows = []
	R = R0
	while R <= Rend*1.0001:
		eps = 1/np.sqrt(R)
		sol = least_squares(system_v, z, args=(eps,), method='lm',
			xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=500)
		z = sol.x
		res = system_v(z, eps)
		k2v, k3v, q1v, p3v = z
		p1v = np.pi/2 + eps*q1v
		D = k3v*k3v - k2v*k2v
		rows.append([R, k2v, k3v, p1v, p3v, D])
		if np.max(np.abs(res)) > 1e-8:
			print('WARNING residual at R=%.6g: %.2e' % (R, np.max(np.abs(res))))
			break
		if len(rows) % 5 == 0 or R*step > Rend:
			print('R=%14.6g k2=%.10f k3=%.10f q1=%.8f p3=%.10f D*R=%.8f'
				% (R, k2v, k3v, q1v, p3v, D*R))
		R *= step
	json.dump(rows, open(out, 'w', encoding='utf-8'), indent=1)
	print('saved', len(rows), 'rows to', out)


if __name__ == '__main__':
	main()
