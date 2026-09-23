"""Measured finite resolution/truncation/FD sensitivity, no threshold PASS."""
import importlib.util
import json
import hashlib
from pathlib import Path
import time
import numpy as np
import mpmath as mp

BASE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('candidate', BASE / '_gapn2_second_variation_probe.py')
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


def main():
	Start = time.monotonic()
	_, _, Blocks, _ = C.build_case(2, 4, 'sup')
	T = C.HighPrecisionTangent(Blocks, 2, 70)
	Rng = np.random.default_rng(20260813)
	Directions = []
	for i in range(11):
		Direction = C.project_tangent(Rng.standard_normal(len(Blocks)), T.A)
		if i < 3:
			Direction *= .01 / max(abs(Direction))
		Directions.append(Direction)
	Result = {'scope': 'finite numerical sensitivity only, no PASS threshold', 'case': 'n2R4SUP',
		'candidate_sha256': hashlib.sha256((BASE / '_gapn2_second_variation_probe.py').read_bytes()).hexdigest(),
		'coefficients_P1_then_P2': [D.tolist() for D in Directions], 'FD': [], 'resolution': [], 'truncation': []}
	References = []
	for i, Direction in enumerate(Directions[:3]):
		Row = {'sample': i, 'steps': []}
		for Step in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
			High = C.fd_gap(Blocks, Direction, 2, Step, 70)
			Double = C.fd_gap(Blocks, Direction, 2, Step, 0)
			Row['steps'].append({'h': Step, 'Q_fd_mp70': High, 'Q_fd_double': Double,
				'absolute_double_minus_mp70': abs(Double - High)})
		At90 = C.fd_gap(Blocks, Direction, 2, 1e-6, 90)
		Reference = Row['steps'][-1]['Q_fd_mp70']
		Row['mp90_at_h1e_minus6'] = At90
		Row['mp70_mp90_difference'] = abs(Reference - At90)
		References.append(Reference)
		Result['FD'].append(Row)
		print('FD sample=%d mp70=%.15e double_at_1e-6=%.15e' % (i, Reference, Row['steps'][-1]['Q_fd_double']), flush=True)
	for Group, Settings in [('resolution', [(61, Order) for Order in (16, 32, 64, 128)]),
		('truncation', [(Modes, 128) for Modes in (31, 61, 121, 241)])]:
		for Modes, Order in Settings:
			Probe = C.SpectralProbe(Blocks, Modes, Order)
			QValues = []
			for Direction in Directions:
				Lam, Cu, Cw, Diagonal = Probe.pairings(C.block_direction(Direction, Probe.edges))
				QValues.append(C.q_formula(Lam, Cu, Cw, 2, Diagonal))
			Row = {'retained_modes': Modes, 'gauss_order': Order, 'P1_Q': QValues[:3], 'P2_Q': QValues[3:],
				'P2_sampled_signs': np.sign(QValues[3:]).tolist(),
				'P1_absolute_error_vs_mp70_fd_h1e_minus6': [abs(Q - F) for Q, F in zip(QValues[:3], References)],
				'P1_relative_error_vs_mp70_fd_h1e_minus6': [abs(Q - F) / abs(F) for Q, F in zip(QValues[:3], References)]}
			Result[Group].append(Row)
			print(json.dumps({'group': Group, **Row}), flush=True)
	Result['elapsed_seconds'] = time.monotonic() - Start
	(BASE / 'sensitivity.json').write_text(json.dumps(Result, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
	main()
