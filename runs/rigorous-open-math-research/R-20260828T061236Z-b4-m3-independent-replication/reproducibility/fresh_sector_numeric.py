"""Independent high-precision Jacobian and mirror-sector determinants.

The full five-block string is rebuilt from transfer matrices.  Eigenvalue and
eigenfunction derivatives are obtained by implicit differentiation of the
Dirichlet secular equation; no old sector-evaluation script is imported.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / ".deps"))
sys.path.insert(0, str(ROOT))

import mpmath as mp

from fresh_numeric_branch import conditioned_equations, derived, serializable


mp.mp.dps = 60


def advance(k, rho, length, state):
	q = k * mp.sqrt(rho)
	c = mp.cos(q * length)
	s = mp.sin(q * length)
	y, yp = state
	return y*c + yp*s/q, -y*q*s + yp*c


def block_norm(k, rho, length, state):
	q = k * mp.sqrt(rho)
	y, yp = state
	b = yp/q
	icc = length/2 + mp.sin(2*q*length)/(4*q)
	iss = length/2 - mp.sin(2*q*length)/(4*q)
	ics = (1-mp.cos(2*q*length))/(4*q)
	return rho * (y*y*icc + 2*y*b*ics + b*b*iss)


def spectral_data(k, edges, rvalue):
	points = [mp.mpf("0"), *edges, mp.mpf("1")]
	rhos = [rvalue, mp.mpf("1"), rvalue, mp.mpf("1"), rvalue]
	state = (mp.mpf("0"), mp.mpf("1"))
	values = []
	norm = mp.mpf("0")
	for index, rho in enumerate(rhos):
		length = points[index+1] - points[index]
		norm += block_norm(k, rho, length, state)
		state = advance(k, rho, length, state)
		if index < 4:
			values.append(state[0])
	return {"secular": state[0], "values": values, "norm": norm}


def replace(values, index, value):
	out = list(values)
	out[index] = value
	return out


def switch_function(kd, kn, edges, rvalue, row):
	dd = spectral_data(kd, edges, rvalue)
	dn = spectral_data(kn, edges, rvalue)
	ud = dd["values"][row] / mp.sqrt(dd["norm"])
	un = dn["values"][row] / mp.sqrt(dn["norm"])
	return (kd*kd*ud*ud - kn*kn*un*un)/(kn*kn)


def jacobian(kd, kn, edges, rvalue):
	skd = mp.diff(lambda kval: spectral_data(kval, edges, rvalue)["secular"], kd)
	skn = mp.diff(lambda kval: spectral_data(kval, edges, rvalue)["secular"], kn)
	dkd = []
	dkn = []
	for col in range(4):
		dsd = mp.diff(lambda xval: spectral_data(kd, replace(edges, col, xval), rvalue)["secular"], edges[col])
		dsn = mp.diff(lambda xval: spectral_data(kn, replace(edges, col, xval), rvalue)["secular"], edges[col])
		dkd.append(-dsd/skd)
		dkn.append(-dsn/skn)
	jmat = mp.matrix(4, 4)
	for row in range(4):
		gkd = mp.diff(lambda kval: switch_function(kval, kn, edges, rvalue, row), kd)
		gkn = mp.diff(lambda kval: switch_function(kd, kval, edges, rvalue, row), kn)
		for col in range(4):
			gx = mp.diff(lambda xval: switch_function(kd, kn,
				replace(edges, col, xval), rvalue, row), edges[col])
			jmat[row, col] = gx + gkd*dkd[col] + gkn*dkn[col]
	return jmat


def mat_to_list(matrix):
	return [[matrix[i, j] for j in range(matrix.cols)] for i in range(matrix.rows)]


def sectors(u, root):
	kval, aval, bval, cval = root
	eps = u**3
	rvalue = u**-6
	kd = kval*u
	kn = kval*u + cval*u**5
	p1 = mp.pi/2 + aval*u**2
	p3 = mp.pi/4 + bval*u**2
	x1 = eps*p1/kd
	x2 = mp.mpf("0.5") - eps*p3/kd
	edges = [x1, x2, 1-x2, 1-x1]
	jmat = jacobian(kd, kn, edges, rvalue)
	sjumps = [1-rvalue, rvalue-1, 1-rvalue, rvalue-1]
	kmat = mp.matrix(4, 4)
	for i in range(4):
		for j in range(4):
			kmat[i, j] = jmat[i, j] / sjumps[i]
	sq2 = mp.sqrt(2)
	bo = mp.matrix([[1/sq2, 0], [0, 1/sq2], [0, -1/sq2], [-1/sq2, 0]])
	epsdiag = mp.diag([1, -1, 1, -1])
	ko = bo.T * kmat * bo
	kpodd = bo.T * epsdiag * kmat * epsdiag * bo
	fvals = [switch_function(kd, kn, edges, rvalue, row) for row in range(4)]
	return {
		"u": u,
		"R": rvalue,
		"root": derived(u, root),
		"edges": edges,
		"secular_D": spectral_data(kd, edges, rvalue)["secular"],
		"secular_N": spectral_data(kn, edges, rvalue)["secular"],
		"F": fvals,
		"K_symmetry_error": max(abs(kmat[i,j]-kmat[j,i]) for i in range(4) for j in range(4)),
		"Kp_odd": mat_to_list(kpodd),
		"Ko": mat_to_list(ko),
		"det_Kp_odd": mp.det(kpodd),
		"det_Ko": mp.det(ko),
	}


def main():
	if len(sys.argv) != 6:
		raise SystemExit("usage: fresh_sector_numeric.py u K A B C")
	u = mp.mpf(sys.argv[1])
	seed = tuple(mp.mpf(v) for v in sys.argv[2:6])
	root = tuple(mp.findroot(lambda kk, aa, bb, cc: conditioned_equations(u, kk, aa, bb, cc),
		seed, tol=mp.mpf("1e-45"), maxsteps=100))
	print(json.dumps(serializable(sectors(u, root)), indent=2))


if __name__ == "__main__":
	main()
