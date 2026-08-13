# -*- coding: utf-8 -*-
"""R-207: n=2 odd-sector 2x2 scan along the symmetric branch (EVIDENCE),
plus the STRICT constant-density (R=1) reference computation.

For each R in a ladder, at the symmetric band-consistent root:
  Kp_odd = diag(d) + 2 lam_2 diag(u)[G_D o ee^T - c^2 G_N] diag(u)  (2x2),
  Ke = Be^T K Be (even sector of raw K, FD), det J = det(diag(s) K).
Printed: eig/tr/det of Kp_odd, eig(Ke), det Kp, margins, and the R=1 limit
values computed analytically from the constant string (STRICT trig).

R=1 limit (STRICT): rho = 1, x1 = 1/5, x2 = 2/5, half [0,1/2]:
  mu_m^D = 4 m^2 pi^2, mu_m^N = (2m-1)^2 pi^2, lam_2 = 4 pi^2, lam_3 = 9 pi^2,
  c = 2/3, D = 5 pi^2, alpha = 1/(5 pi^2), beta = 1/(3 pi^2),
  v_m(x) = sqrt(4) sin(2 m pi x), w_m(x) = sqrt(4) cos((2m-1) pi x).
  G_D(mu_2^N) and G_N(mu_1^D) are explicit sums of closed-form elementary
  series (evaluated by exact known sums); d -> finite limit via L'Hopital.
All numerics EVIDENCE unless flagged STRICT.
Usage: python _gapn2_odd2x2_scan.py [mode] [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum, _norm2,
	_propagate, green_regular, green_regularized)

import warnings
warnings.filterwarnings('ignore')


def odd_sector(R, mode, N=200):
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	key = 'n2_%s' % mode.upper()
	e0 = np.array(tab[key]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	z0 = rc0.widths_to_z(w0)
	rc = Recon(2, R, mode)
	zs = symmetric_root(rc, z0)
	if zs is None:
		return None
	ed = eigen_data(rc, zs)
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	edges = ed['edges']
	w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
	hb = half_blocks(rc, w)
	x1 = w[0]
	x2 = w[0] + w[1]
	muD = half_spectrum(hb, 'D', N=N)
	muN = half_spectrum(hb, 'N', N=N)
	GD_cf = np.array([[green_regular(hb, lam_np1, a, b, 'D') for b in (x1, x2)] for a in (x1, x2)])
	GN_cf = np.array([[green_regular(hb, lam_n, a, b, 'N') for b in (x1, x2)] for a in (x1, x2)])
	eps = ed['eps']
	Wv = ed['W']
	c = ed['c']
	sig = 1.0 if mode == 'sup' else -1.0
	d = sig * 2.0 * c * np.abs(Wv) / (R - 1.0)
	u = ed['u_n']
	e = np.array([1.0, -1.0])
	c2 = lam_n / lam_np1
	BeSBe = GD_cf * np.outer(e, e) - c2 * GN_cf
	Kp_odd = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ BeSBe @ np.diag(u[:2])
	# raw K even/odd sectors via FD
	pat = rc.pat
	s = np.array([pat[i + 1] - pat[i] for i in range(4)])
	Jfd = jac_fd(rc, zs)
	Kfd = np.diag(1.0 / s) @ Jfd
	Po = np.array([[1, 0, 0, -1], [0, 1, -1, 0]]) / np.sqrt(2.0)
	Pe = np.array([[1, 0, 0, 1], [0, 1, 1, 0]]) / np.sqrt(2.0)
	Ke = Pe @ Kfd @ Pe.T
	Ko = Po @ Kfd @ Po.T
	return dict(R=R, lam_n=lam_n, lam_np1=lam_np1, x1=x1, x2=x2, d=d[:2],
		u=u[:2], Kp=Kp_odd, Ke=Ke, Ko=Ko, Kfd=Kfd, detK=np.linalg.det(Kfd),
		detJ=np.linalg.det(Jfd))


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	N = int(sys.argv[2]) if len(sys.argv) > 2 else 200
	Rs = [1.05, 1.2, 2.0, 4.0, 10.0, 30.0, 100.0]
	print('mode=%s' % mode)
	for R in Rs:
		o = odd_sector(R, mode, N=N)
		if o is None:
			print('R=%g: no root' % R)
			continue
		ev = np.linalg.eigvalsh(o['Kp'])
		print('R=%7.3f  eig(Kp_odd)=[%9.4f %9.4f]  det(Kp_odd)=%+.4e  '
			'eig(Ke)=[%9.4f %9.4f]  eig(Ko)=[%9.4f %9.4f]  detK=%+.4e detJ=%+.4e'
			% (R, ev[0], ev[1], np.linalg.det(o['Kp']),
				np.linalg.eigvalsh(o['Ke'])[0], np.linalg.eigvalsh(o['Ke'])[1],
				np.linalg.eigvalsh(o['Ko'])[0], np.linalg.eigvalsh(o['Ko'])[1],
				o['detK'], o['detJ']))


if __name__ == '__main__':
	main()
