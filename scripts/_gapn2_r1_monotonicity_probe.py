# -*- coding: utf-8 -*-
"""R-207 route (ii) probe: monotonicity of det Kp_odd and det Ko in R along
the symmetric branch (n=2), plus wide-range definiteness scan.

EVIDENCE only.  Reports det, trace, eig for both sectors over a geometric
R ladder; flags non-monotone steps.
Usage: python _gapn2_r1_monotonicity_probe.py [mode] [Rmax] [Rmin] [npts]
"""
import sys
import json
import numpy as np

sys.path.insert(0, r'scripts')
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_r1_anchor_probe import closed_sectors


def main():
	mode = sys.argv[1] if len(sys.argv) > 1 else 'both'
	Rmax = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
	Rmin = float(sys.argv[3]) if len(sys.argv) > 3 else 1.05
	npts = int(sys.argv[4]) if len(sys.argv) > 4 else 30
	Rs = np.geomspace(Rmax, Rmin, npts)[::-1]
	tab = json.load(open(r'scripts/op03_gap_table.json', encoding='utf-8'))
	for m in (['sup', 'inf'] if mode == 'both' else [mode]):
		rc0 = Recon(2, R=4.0, mode=m)
		key = 'n2_%s' % m.upper()
		e0 = np.array(tab[key]['edges'])
		w0 = np.diff(np.concatenate([[0.0], e0, [1.0]]))
		zprev = rc0.widths_to_z(w0)
		prev = None
		print('=== mode=%s ===' % m)
		print('R      detKp_odd  detKo     trKp_odd  trKo     eigKp          eigKo')
		mono_p_ok = True
		mono_o_ok = True
		for R in Rs:
			rcR = Recon(2, R, m)
			zs = symmetric_root(rcR, zprev)
			if zs is None:
				print('  R=%.4g: root not found' % R)
				break
			zprev = zs
			Kp_odd, Ko, info = closed_sectors(rcR, zs)
			dp, do = np.linalg.det(Kp_odd), np.linalg.det(Ko)
			tp, to = np.trace(Kp_odd), np.trace(Ko)
			ep = np.linalg.eigvalsh(Kp_odd)
			eo = np.linalg.eigvalsh(Ko)
			flag = ''
			if prev is not None:
				if (dp - prev[0]) * (1.0 if m == 'sup' else -1.0) > 0.0:
					mono_p_ok = False
					flag += ' P!'
				if (do - prev[1]) * (1.0 if m == 'sup' else -1.0) > 0.0:
					mono_o_ok = False
					flag += ' O!'
			print('%.4g %.4e %.4e %+.3e %+.3e [%.3e,%.3e] [%.3e,%.3e]%s'
				% (R, dp, do, tp, to, ep[0], ep[1], eo[0], eo[1], flag))
			prev = (dp, do)
		print('det Kp_odd monotone in R on this ladder:', mono_p_ok)
		print('det Ko     monotone in R on this ladder:', mono_o_ok)


if __name__ == '__main__':
	main()
