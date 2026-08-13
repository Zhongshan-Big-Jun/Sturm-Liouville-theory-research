# -*- coding: utf-8 -*-
"""R-209 M3: fit the asymptotic observables of the corrected large-R branch
to test (i) pure power scaling, (ii) 1/log R convergence, (iii) power-law
approach to a limit.  All results EVIDENCE.
"""
import json
import numpy as np


def main():
	rows = json.load(open(r'scripts/_gapn2_largeR_big.json', encoding='utf-8'))
	A = np.array(rows)
	R, u, K, a, b, Dku7, DR, Mu5 = A.T
	print('rows:', len(A))
	print('R range: %.4g .. %.4g' % (R[0], R[-1]))
	print('u range: %.6f .. %.6f' % (u[0], u[-1]))
	names = ['K', 'a', 'b', 'Dk/u7', 'D*R', 'M/u5']
	vals = [K, a, b, Dku7, DR, Mu5]
	for name, v in zip(names, vals):
		print('%s: first=%.6f last=%.6f ratio=%.4f' % (name, v[0], v[-1], v[-1] / v[0]))
	logu = np.log(u)
	logR = np.log(R)
	h = len(v) // 2
	for name, v in zip(names, vals):
		logv = np.log(np.abs(v))
		slope_all, ic_all = np.polyfit(logu, logv, 1)
		slope_h2, _ = np.polyfit(logu[-h:], logv[-h:], 1)
		print('%-8s dlog/dlogu all=%.4f lastHalf=%.4f' % (name, slope_all, slope_h2))
	for name, v in zip(names, vals):
		X = np.column_stack([np.ones(len(v)), 1.0 / logR])
		coef, res, rank, sv = np.linalg.lstsq(X, v, rcond=None)
		Vinf, c = coef
		resid = float(res[0]) if len(res) else np.nan
		print('%-8s Vinf + c/logR: Vinf=%.6f c=%.4f resid=%.3e' % (name, Vinf, c, resid))
	for name, v in zip(names, vals):
		X = np.column_stack([np.ones(len(v)), logu])
		coef, res, rank, sv = np.linalg.lstsq(X, v, rcond=None)
		V0, m = coef
		resid = float(res[0]) if len(res) else np.nan
		print('%-8s V0 + m*logu:  V0=%.6f m=%.5f resid=%.3e' % (name, V0, m, resid))


if __name__ == '__main__':
	main()
