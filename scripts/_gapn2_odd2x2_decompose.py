# -*- coding: utf-8 -*-
"""R-207: STRICT decomposition of the 2x2 odd-sector Kp at n=2.

On the symmetric branch (n=2), with E = diag(1,-1), c^2 = lam_2/lam_3:
  Kp_odd = diag(d) + 2 lam_2 diag(u)[G_D o ee^T - c^2 G_N] diag(u),  e=(1,-1),
  G_D = D-half full Green at mu = lam_3 = mu_2^N,
  G_N = N-half full Green at mu = lam_2 = mu_1^D.
STRICT spectral split (interleaving mu_1^N < mu_1^D < mu_2^N < mu_2^D):
  G_D|2 = -alpha v^ v^T + P^,   alpha = 1/(lam_3 - mu_1^D) > 0,
  G_N|2 = -beta  w^ w^T + Q^,   beta  = 1/(lam_2 - mu_1^N) > 0,
  P^ = sum_{m>=2} v_m v_m^T/(mu_m^D - lam_3)  (PD on the 2-point grid),
  Q^ = sum_{m>=2} w_m w_m^T/(mu_m^N - lam_2)  (PD),
  v_m, w_m = normalized D-/N-half eigenfunctions at x1, x2.
Two exact reassemblies of Kp_odd:
  (A) Kp_odd = diag(d) + 2 lam_2 diag(u)[-alpha (Ev)(Ev)^T + E P^ E
              + c^2 beta w w^T - c^2 Q^] diag(u);
  (B) Kp_odd = B1 + 2 lam_2 D diag(u)[E T_D E] diag(u),
      B1 = diag(d) + 2 lam_2 diag(u)[E Gt_D E + c^2 beta w w^T - c^2 Q^] diag(u),
      Gt_D = sum_{m>=2} v_m v_m^T/(mu_m^D - mu_1^D) (PD),
      T_D = sum_{m>=2} v_m v_m^T/((mu_m^D - mu_1^D)(mu_m^D - lam_3)) (PD core),
      D = lam_3 - lam_2 = lam_3 - mu_1^D.
All numerics EVIDENCE.
Usage: python _gapn2_odd2x2_decompose.py [R] [mode] [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import (half_blocks, half_spectrum, _norm2,
	_propagate, second_solution, green_regular, green_regularized)

import warnings
warnings.filterwarnings('ignore')


def main():
	R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
	mode = sys.argv[2] if len(sys.argv) > 2 else 'inf'
	N = int(sys.argv[3]) if len(sys.argv) > 3 else 400
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
	L = sum(b[0] for b in hb)
	x1 = w[0]
	x2 = w[0] + w[1]
	muD = half_spectrum(hb, 'D', N=N)
	muN = half_spectrum(hb, 'N', N=N)
	u0D = 1.0 / np.sqrt(_norm2(hb, muD[0], (0.0, 1.0)))
	u0N = 1.0 / np.sqrt(_norm2(hb, muN[1], (0.0, 1.0)))
	v1 = np.array([u0D * _propagate(hb, muD[0], x1)[0], u0D * _propagate(hb, muD[0], x2)[0]])
	w2 = np.array([u0N * _propagate(hb, muN[1], x1)[0], u0N * _propagate(hb, muN[1], x2)[0]])
	# band identity check: w2(x_j) = c v1(x_j)
	c = ed['c']
	print('=== n=2 R=%g %s: lam_2=%.9f lam_3=%.9f ===' % (R, mode, lam_n, lam_np1))
	print('    x1=%.9f x2=%.9f L=%.6f' % (x1, x2, L))
	print('    band identity w2/v1 = %.9f, %.9f  (c = %.9f)'
		% (w2[0] / v1[0], w2[1] / v1[1], c))
	# poles
	alpha = 1.0 / (lam_np1 - muD[0])
	beta = 1.0 / (lam_n - muN[0])
	print('    alpha=1/(lam_3-mu_1^D)=%.9f beta=1/(lam_2-mu_1^N)=%.9f' % (alpha, beta))
	# tails P^, Q^, Gt_D, T_D via spectral sums
	normsD = np.array([np.sqrt(_norm2(hb, m, (0.0, 1.0))) for m in muD])
	normsN = np.array([np.sqrt(_norm2(hb, m, (0.0, 1.0))) for m in muN])
	vecD = np.array([[_propagate(hb, m, x1)[0] / normsD[l], _propagate(hb, m, x2)[0] / normsD[l]]
		for l, m in enumerate(muD)])
	vecN = np.array([[_propagate(hb, m, x1)[0] / normsN[l], _propagate(hb, m, x2)[0] / normsN[l]]
		for l, m in enumerate(muN)])
	Phat = np.zeros((2, 2))
	Qhat = np.zeros((2, 2))
	GtD = np.zeros((2, 2))
	TD = np.zeros((2, 2))
	for l in range(1, N):
		Phat += np.outer(vecD[l], vecD[l]) / (muD[l] - lam_np1)
		Qhat += np.outer(vecN[l], vecN[l]) / (muN[l] - lam_n)
		GtD += np.outer(vecD[l], vecD[l]) / (muD[l] - muD[0])
		TD += np.outer(vecD[l], vecD[l]) / ((muD[l] - muD[0]) * (muD[l] - lam_np1))
	# closed-form references for P^, Q^, Gt_D, T_D at the 2x2 points
	GD_cf = np.array([[green_regular(hb, lam_np1, a, b, 'D') for b in (x1, x2)] for a in (x1, x2)])
	GN_cf = np.array([[green_regular(hb, lam_n, a, b, 'N') for b in (x1, x2)] for a in (x1, x2)])
	GtD_cf = np.array([[green_regularized(hb, muD[0], a, b, 'D') for b in (x1, x2)] for a in (x1, x2)])
	Phat_cf = GD_cf + alpha * np.outer(v1, v1)
	w1 = np.array([u0N * _propagate(hb, muN[0], x1)[0], u0N * _propagate(hb, muN[0], x2)[0]])
	Qhat_cf = GN_cf + beta * np.outer(w1, w1)
	TD_cf = (GD_cf - GtD_cf + alpha * np.outer(v1, v1)) / D
	print('    P^ spectral vs closed err=%.2e  Q^ err=%.2e  Gt_D err=%.2e  T_D err=%.2e'
		% (np.max(np.abs(Phat - Phat_cf)), np.max(np.abs(Qhat - Qhat_cf)),
			np.max(np.abs(GtD - GtD_cf)), np.max(np.abs(TD - TD_cf))))
	# Kp_odd and its exact decomposition
	eps = ed['eps']
	Wv = ed['W']
	sig = 1.0 if mode == 'sup' else -1.0
	d = sig * 2.0 * c * np.abs(Wv) / (R - 1.0)
	u = ed['u_n']
	e = np.array([1.0, -1.0])
	E = np.diag(e)
	BeSBe = GD_cf * np.outer(e, e) - (lam_n / lam_np1) * GN_cf
	Kp_odd = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ BeSBe @ np.diag(u[:2])
	c2 = lam_n / lam_np1
	A_form = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ (
		-alpha * np.outer(E @ v1, E @ v1) + E @ Phat_cf @ E
		+ c2 * beta * np.outer(w1, w1) - c2 * Qhat_cf) @ np.diag(u[:2])
	B1 = np.diag(d[:2]) + 2.0 * lam_n * np.diag(u[:2]) @ (
		E @ GtD_cf @ E - alpha * np.outer(E @ v1, E @ v1) + c2 * beta * np.outer(w1, w1) - c2 * Qhat_cf) @ np.diag(u[:2])
	B2 = B1 + 2.0 * lam_n * D * np.diag(u[:2]) @ (E @ TD_cf @ E) @ np.diag(u[:2])
	print('    Kp_odd =', np.round(Kp_odd, 9))
	print('    eig(Kp_odd) =', np.round(np.linalg.eigvalsh(Kp_odd), 9))
	print('    A-form err=%.2e, B1 err=%.2e, B2 err=%.2e'
		% (np.max(np.abs(A_form - Kp_odd)), np.max(np.abs(B1 - Kp_odd)),
			np.max(np.abs(B2 - Kp_odd))))
	print('    d =', np.round(d[:2], 9), ' u =', np.round(u[:2], 9))
	print('    v1 =', np.round(v1, 9), ' w1 =', np.round(w1, 9), ' w2 =', np.round(w2, 9))
	print('    GD_cf =', np.round(GD_cf, 9))
	print('    GN_cf =', np.round(GN_cf, 9))
	print('    P^ =', np.round(Phat_cf, 9), ' eig=', np.round(np.linalg.eigvalsh(Phat_cf), 9))
	print('    Q^ =', np.round(Qhat_cf, 9), ' eig=', np.round(np.linalg.eigvalsh(Qhat_cf), 9))
	print('    Gt_D =', np.round(GtD_cf, 9), ' eig=', np.round(np.linalg.eigvalsh(GtD_cf), 9))
	print('    T_D =', np.round(TD_cf, 9), ' eig=', np.round(np.linalg.eigvalsh(TD_cf), 9))
	print('    B1 =', np.round(B1, 9), ' eig=', np.round(np.linalg.eigvalsh(B1), 9))
	print('    PD core term 2lam2*D*diag(u)ET_D E diag(u) eig=',
		np.round(np.linalg.eigvalsh(2.0 * lam_n * D * np.diag(u[:2]) @ (E @ TD_cf @ E) @ np.diag(u[:2])), 9))


if __name__ == '__main__':
	main()
