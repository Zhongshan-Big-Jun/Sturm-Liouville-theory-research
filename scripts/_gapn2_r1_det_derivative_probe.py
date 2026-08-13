# -*- coding: utf-8 -*-
"""R-207 route (ii) probe 3: chain-rule structure of d/dR det Kp_odd, det Ko
along the symmetric branch (n=2).

Direct FD in R (re-solve at R+-h) is compared against the composition
  d/dR M = dM/dR|_x  +  sum_j dM/dx_j * (dx_j/dR),
  dx/dR = - J^{-1} dF/dR,   J = analytic Jacobian of the band system,
so that the derivative formula to be signed is identified exactly.

EVIDENCE only.
Usage: python _gapn2_r1_det_derivative_probe.py [mode] [Rlist]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data, analytic_jacobian
from _gapn2_r1_anchor_probe import closed_sectors


def sector_matrices(rc, zs):
	Kp_odd, Ko, info = closed_sectors(rc, zs)
	return Kp_odd, Ko, info


def dFdR_fd(rc, zs, h=1e-4):
	"""dF/dR at fixed x: F_j = f(x_j)/lam_{n+1} (residual convention of rc)."""
	# residual depends on (R, x); use rc.R mutation
	R0 = rc.R
	m = 2 * rc.n
	Fp = np.zeros(m)
	Fm = np.zeros(m)
	# Recon caches pat at init, so build fresh objects instead of mutating rc.R
	from _gapn2_symmetry_recon import Recon as _Recon
	rcp = _Recon(rc.n, R0 * (1.0 + h), rc.mode)
	rcm = _Recon(rc.n, R0 * (1.0 - h), rc.mode)
	Fp[:] = rcp.residual(zs)
	Fm[:] = rcm.residual(zs)
	return (Fp - Fm) / (2.0 * h * R0)


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'inf'
	Rs = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1.5, 2.0, 4.0, 10.0, 30.0]
	h = 5e-4
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(2, R=4.0, mode=mode)
	key = 'n2_%s' % mode.upper()
	e0 = np.array(tab[key]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	zprev = rc0.widths_to_z(w0)
	print('=== mode=%s ===' % mode)
	for R in Rs:
		rcR = Recon(2, R, mode)
		zs = symmetric_root(rcR, zprev)
		if zs is None:
			print('R=%.4g: root not found' % R)
			continue
		zprev = zs
		Kp_odd, Ko, info = sector_matrices(rcR, zs)
		detp, deto = np.linalg.det(Kp_odd), np.linalg.det(Ko)
		# direct FD along the branch
		rcp = Recon(2, R * (1.0 + h), mode)
		rcm = Recon(2, R * (1.0 - h), mode)
		zsp = symmetric_root(rcp, zs)
		zsm = symmetric_root(rcm, zs)
		Kpp, Kop, _ = sector_matrices(rcp, zsp)
		Kpm, Kom, _ = sector_matrices(rcm, zsm)
		ddetp_fd = (np.linalg.det(Kpp) - np.linalg.det(Kpm)) / (2.0 * h * R)
		ddeto_fd = (np.linalg.det(Kop) - np.linalg.det(Kom)) / (2.0 * h * R)
		dtrp_fd = (np.trace(Kpp) - np.trace(Kpm)) / (2.0 * h * R)
		dtro_fd = (np.trace(Kop) - np.trace(Kom)) / (2.0 * h * R)
		# chain rule: dM/dx_j at fixed R, dM/dR at fixed x
		J = analytic_jacobian(rcR, zs)[0]
		FR = dFdR_fd(rcR, zs, h=5e-4)
		dxdR = -np.linalg.solve(J, FR)
		dMdx = np.zeros((2, 2, 4))
		hw = 1e-5
		for k in range(4):
			# x_k = edges[k]; vary widths to move x_k keeping total width 1
			ws = rcR.z_to_widths(zs)
			wp = ws.copy()
			wm = ws.copy()
			wp[k] += hw
			wm[k] -= hw
			ws0 = ws.copy()
			wp = ws0.copy()
			wm = ws0.copy()
			wp[k] += hw
			wp[k + 1] -= hw
			wm[k] -= hw
			wm[k + 1] += hw
			zp = rcR.widths_to_z(wp)
			zm = rcR.widths_to_z(wm)
			Kppx, Kopx, _ = sector_matrices(rcR, zp)
			Kpmx, Komx, _ = sector_matrices(rcR, zm)
			dMdx[:, :, k] = (Kppx - Kpmx) / (2.0 * hw)
			dMdx_o = (Kopx - Komx) / (2.0 * hw)
			if k == 0:
				dModx = np.zeros((2, 2, 4))
			dModx[:, :, k] = dMdx_o
		KpRp, KoRp, _ = sector_matrices(rcp, zs)
		KpRm, KoRm, _ = sector_matrices(rcm, zs)
		dMdR = (KpRp - KpRm) / (2.0 * h * R)
		dModR = (KoRp - KoRm) / (2.0 * h * R)
		dM_chain = dMdR + np.tensordot(dMdx, dxdR, axes=(2, 0))
		dMo_chain = dModR + np.tensordot(dModx, dxdR, axes=(2, 0))
		ddetp_ch = np.trace(np.linalg.inv(Kp_odd).T @ dM_chain) * detp \
			if abs(detp) > 1e-30 else np.nan
		ddeto_ch = np.trace(np.linalg.inv(Ko).T @ dMo_chain) * deto \
			if abs(deto) > 1e-30 else np.nan
		dtrp_ch = np.trace(dM_chain)
		dtro_ch = np.trace(dMo_chain)
		print('R=%.4g: d/dR detKp fd=%+.4e chain=%+.4e | d/dR detKo fd=%+.4e chain=%+.4e'
			% (R, ddetp_fd, ddetp_ch, ddeto_fd, ddeto_ch))
		print('        d/dR trKp  fd=%+.4e chain=%+.4e | d/dR trKo  fd=%+.4e chain=%+.4e'
			% (dtrp_fd, dtrp_ch, dtro_fd, dtro_ch))
		print('        dx/dR =', np.round(dxdR, 6))


if __name__ == '__main__':
	main()
