# -*- coding: utf-8 -*-
"""Finite spectral decomposition of raw K and Kp=S K S at symmetric roots.

The historical Sigma'/Sigma_+ assemblies below are the blocks of Kp.
Raw blocks use Ke=E KpOdd E and Ko=E KpEven E, E=diag(eps[:n]).
The additive H/E pieces transform by the same swap and congruence.

Return keys Ke/Ko/He/Ho/Ee/Eo now consistently refer to raw K. Explicit
Kp* keys preserve the conjugated assemblies and their c_e/c_o coefficients.
Older saved scans used the Kp convention under raw labels; their individual
sector identities and dominance explanations require this correction. Their
bytes are historical and are not rewritten by this program.

Finite truncated sums and branch samples are EVIDENCE, not interval bounds
or all-R sign/uniqueness theorems. Usage:
python _gapn2_sector_decomposition.py <n> <sup|inf> [N]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon, roots_of, eigfun
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data


def sector_data(rc, zs, N=121):
	"""Truncated spectral blocks at a numerically symmetric stationary root."""
	if not np.isfinite(rc.R) or rc.R <= 1:
		raise ValueError("sector decomposition requires finite R>1")
	if isinstance(N, (bool, np.bool_)) or not isinstance(N, (int, np.integer)) or N < rc.n + 1:
		raise ValueError("spectral truncation must cover the adjacent pair")
	ed = eigen_data(rc, zs)
	n = rc.n
	mode = rc.mode
	lam_n, lam_np1 = ed['lam_n'], ed['lam_np1']
	D = lam_np1 - lam_n
	EdgeValues = np.asarray(ed['edges'])
	Residual = np.asarray(rc.residual(zs))
	if not np.all(np.isfinite(Residual)) or np.max(np.abs(Residual)) > 1e-8:
		raise ValueError('sector decomposition requires a stationary point')
	if np.max(np.abs(EdgeValues + EdgeValues[::-1] - 1.0)) > 1e-10:
		raise ValueError('sector decomposition requires mirror-symmetric geometry')
	u_n = ed['u_n']
	eps = ed['eps']
	W = ed['W']
	c = ed['c']
	m = 2 * n
	wj = lam_n * u_n ** 2
	blocks = rc.blocks_from_z(zs)
	ss = roots_of(blocks, N + 1)
	lam_all = ss ** 2
	ni, nj = n - 1, n
	x = ed['edges']
	xbar = 1.0 - x
	U = np.zeros((N + 1, m))
	Ubar = np.zeros((N + 1, m))
	for l in range(N + 1):
		U[l] = eigfun(blocks, ss[l], x)
		Ubar[l] = eigfun(blocks, ss[l], xbar)
	wgt_s1 = np.zeros(N + 1)
	wgt_s2 = np.zeros(N + 1)
	for l in range(N + 1):
		if l != ni and l != nj:
			wgt_s1[l] = lam_all[l] * D / ((lam_all[l] - lam_np1) * (lam_all[l] - lam_n))
			wgt_s2[l] = lam_n / (lam_all[l] - lam_n) + lam_np1 / (lam_all[l] - lam_np1)
	S1 = U.T @ np.diag(wgt_s1) @ U
	S2 = U.T @ np.diag(wgt_s2) @ U
	S1b = U.T @ np.diag(wgt_s1) @ Ubar
	S2b = U.T @ np.diag(wgt_s2) @ Ubar
	sigma = 1.0 if mode == 'sup' else -1.0
	R = rc.R
	d = sigma * 2.0 * c * np.abs(W) / (R - 1.0)
	wh = wj[:n]
	eh = eps[:n]
	c_e = 4.0 * D / (lam_n * lam_np1 ** 2)
	c_o = -4.0 * (lam_n ** 2 + lam_np1 ** 2) / (lam_n * lam_np1 * D * lam_np1)
	pn = 1.0 if n % 2 == 1 else -1.0
	pmask = np.fromfunction(lambda i, j: (i + j) % 2 == 0, (n, n))
	uu = np.outer(u_n[:n], u_n[:n])
	fac = 2.0 * lam_n / lam_np1
	He = fac * uu * (np.where(pmask, S1[:n, :n] - pn * S2b[:n, :n], -S2[:n, :n] + pn * S1b[:n, :n]))
	Ho = fac * uu * (np.where(pmask, S1[:n, :n] + pn * S2b[:n, :n], -S2[:n, :n] - pn * S1b[:n, :n]))
	Ee = c_e * np.outer(wh, wh)
	Eo = c_o * np.outer(eh * wh, eh * wh)
	KpHe, KpHo, KpEe, KpEo = He, Ho, Ee, Eo
	KpEven = np.diag(d[:n]) + KpEe + KpHe
	KpOdd = np.diag(d[:n]) + KpEo + KpHo
	E = np.diag(eh)
	He, Ho = E @ KpHo @ E, E @ KpHe @ E
	Ee, Eo = E @ KpEo @ E, E @ KpEe @ E
	Ke, Ko = E @ KpOdd @ E, E @ KpEven @ E
	out = dict(d=d[:n].tolist(), c_e=c_e, c_o=c_o,
			   coefficient_target='c_e/c_o belong to KpEe/KpEo',
			   sector_convention='Ke/Ko are raw K; KpEven/KpOdd are S K S',
			   KpEven=KpEven.tolist(), KpOdd=KpOdd.tolist(),
			   KpHe=KpHe.tolist(), KpHo=KpHo.tolist(), KpEe=KpEe.tolist(), KpEo=KpEo.tolist(),
			   He=He.tolist(), Ho=Ho.tolist(), Ee=Ee.tolist(), Eo=Eo.tolist(), Ke=Ke.tolist(), Ko=Ko.tolist())
	for k, M in (('Ke', Ke), ('Ko', Ko), ('He', He), ('Ho', Ho), ('Ee', Ee), ('Eo', Eo)):
		out[k + '_ev'] = np.linalg.eigvalsh(M).tolist()
	return out


def main():
	n = int(sys.argv[1])
	mode = sys.argv[2]
	N = int(sys.argv[3]) if len(sys.argv) > 3 else 121
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	rc0 = Recon(n, R=4.0, mode=mode)
	key = f'n{n}_{mode.upper()}'
	e0 = np.array(tab[key]['edges'])
	w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
	z0 = rc0.widths_to_z(w0)
	if n == 2:
		Rs = [1.05, 1.2, 2.0, 4.0, 10.0, 30.0, 100.0]
	else:
		Rs = [1.2, 2.0, 4.0, 10.0, 30.0, 100.0]
	results = {}
	prev = z0
	for R in Rs:
		rc = Recon(n, R, mode)
		zs = symmetric_root(rc, prev)
		if zs is None:
			results[str(R)] = {'status': 'no root'}
			continue
		prev = zs
		try:
			sd = sector_data(rc, zs, N=N)
			sd['status'] = 'ok'
			results[str(R)] = sd
		except Exception as e:
			results[str(R)] = {'status': 'fail: %s: %s' % (type(e).__name__, e)}
		print('n=%d %s R=%s: %s' % (n, mode, R, results[str(R)]['status']), flush=True)
	out = r'scripts/_gapn2_sector_scan_%d_%s.json' % (n, mode)
	json.dump(results, open(out, 'w'), indent=1)
	print('saved', out)


if __name__ == '__main__':
	main()
