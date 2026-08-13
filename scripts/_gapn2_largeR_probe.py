# -*- coding: utf-8 -*-
"""R-208/209 route (iii) probe: large-R limit structure of the n=2 branch.

Continues the symmetric band-consistent root multiplicatively in R and
records: x1, x2, lam2, lam3, D*R, c, W(x_j), d_j(R-1), the four half-Green
diagonals at the switches, and the sector spectra.  All EVIDENCE; used to
fix the degenerate-perturbation setup of route (iii).

Usage: python _gapn2_largeR_probe.py [mode] [Rstart] [Rend] [step]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_half_problem_probe import half_blocks, half_spectrum, green_regular, green_regularized
from _gapn2_r1_anchor_probe import closed_sectors


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	Rstart = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
	Rend = float(sys.argv[3]) if len(sys.argv) > 3 else 2000.0
	step = float(sys.argv[4]) if len(sys.argv) > 4 else 1.1
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	e0 = np.array(tab['n2_%s' % mode.upper()]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	zprev = rc0.widths_to_z(w0)
	R = Rstart
	while R <= Rend * 1.001:
		rc = Recon(2, R, mode)
		zs = symmetric_root(rc, zprev)
		if zs is None:
			print('R=%.4g: continuation FAILED' % R)
			break
		zprev = zs
		ed = eigen_data(rc, zs)
		w = np.diff(np.concatenate([[0.0], ed['edges'], [1.0]]))
		hb = half_blocks(rc, w)
		muD = half_spectrum(hb, 'D', N=4)
		muN = half_spectrum(hb, 'N', N=4)
		x1, x2 = ed['edges'][0], ed['edges'][1]
		xs = [x1, x2]
		GD = np.zeros((2, 2)); GN = np.zeros((2, 2))
		GtD = np.zeros((2, 2)); GtN = np.zeros((2, 2))
		for (i, j) in [(0, 0), (0, 1), (1, 1)]:
			GD[i, j] = green_regular(hb, muN[1], xs[i], xs[j], 'D')
			GN[i, j] = green_regular(hb, muD[0], xs[i], xs[j], 'N')
			GtD[i, j] = green_regularized(hb, muD[0], xs[i], xs[j], 'D')
			GtN[i, j] = green_regularized(hb, muN[1], xs[i], xs[j], 'N')
		for M in (GD, GN, GtD, GtN):
			M[1, 0] = M[0, 1]
		Kp, Ko, _ = closed_sectors(rc, zs)
		ep = np.linalg.eigvalsh(Kp)
		eo = np.linalg.eigvalsh(Ko)
		D = ed['lam_np1'] - ed['lam_n']
		print('R=%9.3g x1=%.8f x2=%.8f lam2=%.6f D*R=%.6f c=%.6f'
			% (R, x1, x2, ed['lam_n'], D * R, ed['c']))
		print('    W(R-1)d=%s  GDdiag=%s GNdiag=%s GtDdiag=%s GtNdiag=%s'
			% (np.round(ed['W'] * (R - 1), 5), np.round(np.diag(GD), 5),
				np.round(np.diag(GN), 5), np.round(np.diag(GtD), 5),
				np.round(np.diag(GtN), 5)))
		print('    eigKp=%s eigKo=%s detKp=%.3e detKo=%.3e'
			% (np.round(ep, 6), np.round(eo, 6), np.linalg.det(Kp), np.linalg.det(Ko)))
		R *= step


if __name__ == '__main__':
	main()
