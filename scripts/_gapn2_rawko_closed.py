# -*- coding: utf-8 -*-
"""R-207: closed form of the RAW-K odd sector Ko = Bo^T K Bo at n=2 (even n).

Derivation (STRICT algebra, R-207): from the R-206 collapsed identity
  Kp = diag(eps) K diag(eps) = diag(d) + r vv^T + 2 lam_n diag(u) S diag(u),
  r = 2 lam_n D / lam_{n+1}^2,  S = eps Gt_{n+1} eps - c^2 Gt_n,
conjugating back gives
  K = diag(d) + r (eps v)(eps v)^T + 2 lam_n diag(u) [eps S eps] diag(u),
  eps S eps = Gt_{n+1} - c^2 eps Gt_n eps.
On the symmetric branch (n even: lam_n = mu_{n/2}^D odd, lam_{n+1} =
mu_{n/2+1}^N even), the mirror projection identities are
  Be^T Gt_{n+1} Be = Gt_N(lam_{n+1}),              (regularized N-half Green)
  Be^T eps Gt_n eps Be = Gt_D(lam_n) o ee^T,       (regularized D-half Green)
  Bo^T (eps v) = sqrt(2) (eps v)[:n]               (v = u_n^2 mirror-even),
hence
  Ko = diag(d[:n]) + 2 r (eps v)(eps v)^T
       + 2 lam_n diag(u[:n]) [Gt_N - c^2 Gt_D o ee^T] diag(u[:n]).
Together with Kp_odd = diag(d[:n]) + 2 lam_n diag(u[:n]) [G_D o ee^T
- c^2 G_N] diag(u[:n]) (= diag(beta) Ke diag(beta), beta = -(-1)^j), this
gives exact closed forms for BOTH 2x2 mirror sectors of the raw K at n=2.

Checks vs FD (EVIDENCE): Ko_closed vs Bo^T K_fd Bo; Kp_odd vs
diag(1,-1) Ke_fd diag(1,-1).
Usage: python _gapn2_rawko_closed.py [R] [mode] [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum, green_regular,
	green_regularized)

import warnings
warnings.filterwarnings('ignore')


def main():
	R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
	mode = sys.argv[2] if len(sys.argv) > 2 else 'inf'
	N = int(sys.argv[3]) if len(sys.argv) > 3 else 120
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	key = 'n2_%s' % mode.upper()
	e0 = np.array(tab[key]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	z0 = rc0.widths_to_z(w0)
	rc = Recon(2, R, mode)
	zs = symmetric_root(rc, z0)
	ed = eigen_data(rc, zs)
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	D = lam_np1 - lam_n
	edges = ed['edges']
	w = np.diff(np.concatenate([[0.0], edges, [1.0]]))
	hb = half_blocks(rc, w)
	x1 = w[0]
	x2 = w[0] + w[1]
	muD = half_spectrum(hb, 'D', N=N)
	muN = half_spectrum(hb, 'N', N=N)
	GtD_cf = np.array([[green_regularized(hb, muD[0], a, b, 'D') for b in (x1, x2)] for a in (x1, x2)])
	GtN_cf = np.array([[green_regularized(hb, muN[1], a, b, 'N') for b in (x1, x2)] for a in (x1, x2)])
	GD_cf = np.array([[green_regular(hb, lam_np1, a, b, 'D') for b in (x1, x2)] for a in (x1, x2)])
	GN_cf = np.array([[green_regular(hb, lam_n, a, b, 'N') for b in (x1, x2)] for a in (x1, x2)])
	eps = ed['eps']
	Wv = ed['W']
	c = ed['c']
	sig = 1.0 if mode == 'sup' else -1.0
	d = sig * 2.0 * c * np.abs(Wv) / (R - 1.0)
	u = ed['u_n']
	v = u ** 2
	r = 2.0 * lam_n * D / lam_np1 ** 2
	c2 = lam_n / lam_np1
	e = np.array([1.0, -1.0])
	E2 = np.diag(e)
	Kp_odd = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ (GD_cf * np.outer(e, e) - c2 * GN_cf) @ np.diag(u[:2])
	ev = eps[:2] * v[:2]
	Ko_closed = np.diag(d[:2]) + 2.0 * r * np.outer(ev, ev) \
		+ 2.0 * lam_n * np.diag(u[:2]) @ (GtN_cf - c2 * (GtD_cf * np.outer(e, e))) @ np.diag(u[:2])
	# FD reference
	pat = rc.pat
	s = np.array([pat[i + 1] - pat[i] for i in range(4)])
	Jfd = jac_fd(rc, zs)
	Kfd = np.diag(1.0 / s) @ Jfd
	Po = np.array([[1, 0, 0, -1], [0, 1, -1, 0]]) / np.sqrt(2.0)
	Pe = np.array([[1, 0, 0, 1], [0, 1, 1, 0]]) / np.sqrt(2.0)
	Ko_fd = Po @ Kfd @ Po.T
	Ke_fd = Pe @ Kfd @ Pe.T
	print('=== n=2 R=%g %s ===' % (R, mode))
	print('   Ko_closed =', np.round(Ko_closed, 6))
	print('   Ko_fd     =', np.round(Ko_fd, 6))
	print('   Ko err = %.3e' % np.max(np.abs(Ko_closed - Ko_fd)))
	print('   eig(Ko_closed) =', np.round(np.linalg.eigvalsh(Ko_closed), 6))
	print('   eig(Ko_fd)     =', np.round(np.linalg.eigvalsh(Ko_fd), 6))
	print('   Kp_odd =', np.round(Kp_odd, 6))
	print('   diag(1,-1)Ke_fd diag(1,-1) =',
		np.round(np.diag([1.0, -1.0]) @ Ke_fd @ np.diag([1.0, -1.0]), 6))
	print('   Kp_odd vs diag(1,-1)Ke_fd diag(1,-1) err = %.3e'
		% np.max(np.abs(Kp_odd - (np.diag([1.0, -1.0]) @ Ke_fd @ np.diag([1.0, -1.0])))))
	print('   det(Ko)=%.6e det(Kp_odd)=%.6e detKfd=%.6e' %
		(np.linalg.det(Ko_closed), np.linalg.det(Kp_odd), np.linalg.det(Kfd)))


if __name__ == '__main__':
	main()
