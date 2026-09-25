"""Round10 author regression, with a separate physical-state zero counter.

Usage: python check_spectrum.py SCRIPTS OUTPUT_JSON
No project outputs or historical evidence are rewritten.
"""
from pathlib import Path
import hashlib, importlib.util, json, math, platform, sys, time
import numpy as np
import mpmath as mp
Scripts = Path(sys.argv[1]).resolve()
Output = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(Scripts))
from _sl_prufer import indexed_roots, lifted_phase, mp_lifted_phase
import _gapn2_symmetry_recon as Recon
import _gapn2_second_variation_probe as Probe
Rows = []


def check(Name, Condition, Detail=None):
	if not bool(Condition):
		raise RuntimeError('FAILED: ' + Name)
	Rows.append(dict(name=Name, passed=True, detail=Detail))


def rejects(Name, Function, Types=(ValueError, ArithmeticError)):
	try:
		Function()
	except Types as Error:
		check(Name, True, str(Error))
	else:
		raise RuntimeError('FAILED rejection: ' + Name)


def physical_zero_count(Blocks, Frequency):
	"""Count spatial zeros of propagated y=A*cos(w*t)+B*sin(w*t).

	Independent 70-digit physical (y,y') state, with local zero locations
	listed explicitly. Does not call either phase implementation under test.
	At chosen inter-eigenvalue frequencies, zeros must not lie at interfaces.
	"""
	with mp.workdps(70):
		Value, Derivative, Count = mp.mpf(0), mp.mpf(1), 0
		for Position, (Length, Density) in enumerate(Blocks):
			Length, Density = mp.mpf(float(Length)), mp.mpf(float(Density))
			W = mp.mpf(float(Frequency)) * mp.sqrt(Density)
			A, B = Value, Derivative / W
			Offset = mp.atan2(A, B)
			Angle = W * Length
			First = int(mp.floor(Offset / mp.pi)) - 1
			Last = int(mp.ceil((Offset + Angle) / mp.pi)) + 1
			for J in range(First, Last + 1):
				Zero = (J * mp.pi - Offset) / W
				if 0 < Zero <= Length:
					Count += 1
			Cos, Sin = mp.cos(Angle), mp.sin(Angle)
			Value, Derivative = A * Cos + B * Sin, W * (-A * Sin + B * Cos)
			if abs(Value) < mp.mpf('1e-45'):
				raise ArithmeticError('test sample lands on a block-boundary zero')
			Scale = max(abs(Value), abs(Derivative))
			Value, Derivative = Value / Scale, Derivative / Scale
		return Count


Started = time.monotonic()
Cluster = [(0.02, 10000.0), (0.96, 1.0), (0.02, 10000.0)]
Intervals = [(0.783424012239, 0.783424012240), (0.797807654414, 0.797807654415),
	(2.345707847544, 2.345707847545), (2.358540421082, 2.358540421083)]
Prefix = None
for Count in (2, 3, 4, 61, 401, 2001):
	Roots, Records = indexed_roots(Cluster, Count)
	for J, (Left, Right) in enumerate(Intervals[:Count]):
		check('cluster-index-%d-count-%d' % (J + 1, Count), Left < Roots[J] < Right, float(Roots[J]))
	if Prefix is not None:
		check('prefix-consistency-%d' % Count, np.allclose(Roots[:len(Prefix)], Prefix, rtol=0, atol=2e-13))
	Prefix = Roots[:min(Count, 61)]
	check('bracket-records-%d' % Count, all(X['index'] == I + 1 and X['phase_bracket'][0] <= X['target_phase'] <= X['phase_bracket'][1] and not X['certified'] for I, X in enumerate(Records)))
Roots = indexed_roots(Cluster, 62)[0]
for J in range(62):
	Frequency = Roots[0] * 0.371 if J == 0 else Roots[J-1] + 0.371 * (Roots[J] - Roots[J-1])
	Count = physical_zero_count(Cluster, Frequency)
	check('cluster-physical-zero-count-%d' % J, Count == J, dict(frequency=float(Frequency), count=Count))
check('first-frequency-rayleigh-bound', Roots[0] < np.pi)
for Density, Length in [(1.0, 1.0), (4.0, 2.5), (0.125, 0.4), (1e6, 1.0), (1e-6, 1.0)]:
	Constant = [(Length * .3, Density), (Length * .7, Density)]
	Actual = indexed_roots(Constant, 25)[0]
	Exact = np.arange(1, 26) * np.pi / (Length * np.sqrt(Density))
	check('constant-%g-%g' % (Density, Length), np.allclose(Actual, Exact, rtol=2e-13, atol=0))
Rng = np.random.default_rng(20260925)
for Case in range(8):
	Widths = Rng.dirichlet(np.ones(5))
	Densities = np.exp(Rng.uniform(-2, 8, 5))
	Blocks = list(zip(Widths.tolist(), Densities.tolist()))
	Roots = indexed_roots(Blocks, 13)[0]
	Reverse = indexed_roots(Blocks[::-1], 13)[0]
	check('reflection-spectrum-%d' % Case, np.allclose(Roots, Reverse, rtol=2e-12, atol=1e-13))
	Scaled = indexed_roots([(L, 7*C) for L, C in Blocks], 13)[0]
	check('density-scaling-%d' % Case, np.allclose(Scaled*np.sqrt(7), Roots, rtol=2e-12, atol=1e-13))
	Split = [(L/2, C) for L,C in Blocks for _ in range(2)]
	check('block-splitting-%d' % Case, np.allclose(indexed_roots(Split, 13)[0], Roots, rtol=2e-12, atol=1e-13))
	for J in range(1, 13):
		Frequency = Roots[J-1] + .371*(Roots[J]-Roots[J-1])
		check('random-physical-count-%d-%d' % (Case,J), physical_zero_count(Blocks, Frequency) == J)
for Bad in [[], [(0,1)], [(1,0)], [(1,float('nan'))], [(1,1j)], [(1,1),(1e-30,1)]]:
	rejects('invalid-blocks-'+str(Bad), lambda B=Bad: indexed_roots(B,2))
for Count in [0,-1,True,1.5]:
	rejects('invalid-index-'+str(Count), lambda C=Count:indexed_roots(Cluster,C))
rejects('insufficient-refinement',lambda:indexed_roots(Cluster,3,1))
check('zero-phase-origin',lifted_phase(Cluster,0)==0)
check('zero-frequency-transfer-limit',abs(Recon.D_scalar(Cluster,0)-1)<1e-15)
OldRoots = Probe.roots_of
try:
	Probe.roots_of = lambda Blocks, Count, refine=60: np.array([3.2671480773046255,3.925370522341491])[:Count]
	rejects('positive-ordered-wrong-index-list',lambda:Probe.checked_roots(Cluster,2))
finally:
	Probe.roots_of = OldRoots
with mp.workdps(60):
	Precise = [(mp.mpf(L),mp.mpf(C)) for L,C in Cluster]
	for Index in (1,2,3,4):
		Root, _, Mass = Probe.refine_mp_root(Precise,3.2671480773046255,60,Index)
		Left, Right = Intervals[Index-1]
		check('mp-refinement-retains-index-%d' % Index,mp.mpf(Left)<Root<mp.mpf(Right) and Mass>0,mp.nstr(Root,45))
	Tangent = Probe.HighPrecisionTangent(Cluster,1,60)
	check('tangent-actual-low-modes',all(mp.mpf(Intervals[J][0])<Tangent.modes[J][0]<mp.mpf(Intervals[J][1]) for J in range(2)))
	FD, Base, Plus, Minus = Probe.fd_second(Cluster,[C for _,C in Cluster],0,h=.001,dps=60)
	Expected = 2*Base/(1-mp.mpf(.001)**2)
	check('fd-keeps-first-index-on-scaled-path',abs(FD-Expected)<mp.mpf('1e-40'),mp.nstr(FD,40))
check('spectral-probe-low-mode-identity',np.allclose(Probe.SpectralProbe(Cluster,8,32).roots[:4],[sum(B)/2 for B in Intervals],atol=6e-13,rtol=0))
Result = dict(status='PASS',scope='author finite regression including separate physical-state nodal counts; not interval certification or independent acceptance',
	python=sys.version,numpy=np.__version__,mpmath=mp.__version__,optimization=sys.flags.optimize,seconds=time.monotonic()-Started,
	source_hashes={str(Scripts/N):hashlib.sha256((Scripts/N).read_bytes()).hexdigest() for N in ['_sl_prufer.py','_gapn2_symmetry_recon.py','_gapn2_second_variation_probe.py']},
	checks=Rows,count=len(Rows))
Output.write_text(json.dumps(Result,indent=2)+'\n')
print(json.dumps(dict(status='PASS',count=len(Rows),seconds=Result['seconds'])))
