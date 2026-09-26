"""Bounded round12 behavior checks. Numerical evidence, not certification."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import mpmath as mp

Root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(Root / 'scripts'))
import _gapn2_half_problem_probe as Half
from _sl_prufer import indexed_roots
from _gapn2_symmetry_recon import Recon
from _gapn2_jacobian_probe import symmetric_root, jac_fd
from _gapn2_jacobian_analytic import eigen_data
from _gapn2_sector_decomposition import sector_data
from _gapn2_jacobian_spectral import analytic_jacobian_spectral

Results = []
def check(Name, Condition, Details=None):
	if not bool(Condition):
		raise RuntimeError('FAILED ' + Name + ': ' + repr(Details))
	Results.append(dict(name=Name, details=Details))

def rejects(Name, Operation):
	try:
		Operation()
	except (ValueError, ArithmeticError) as Error:
		check(Name, True, str(Error))
	else:
		raise RuntimeError('Expected rejection: ' + Name)

for Density in [1e-6, 1.0, 100.0]:
	for Boundary in ['D', 'N']:
		Blocks = [(0.5, Density)]
		Table = Half.half_spectrum(Blocks, Boundary, 160, return_table=True)
		for Count in [4, 80, 160]:
			Exact = ((np.arange(1, Count + 1) - (0.5 if Boundary == 'N' else 0)) * np.pi / (0.5 * np.sqrt(Density))) ** 2
			Values = Half.half_spectrum(Blocks, Boundary, Count)
			check(f'constant-{Density}-{Boundary}-{Count}', np.max(abs(Values / Exact - 1)) < 3e-14)
			check(f'prefix-{Density}-{Boundary}-{Count}', np.array_equal(Values, Table.prefix(Count)))
		check(f'phase-target-{Density}-{Boundary}', all(dict(Record)['right_boundary'] == Boundary and dict(Record)['certified'] is False for Record in Table.phase_records))

Blocks = [(0.5, 100.0)]
Table = Half.half_spectrum(Blocks, 'N', 160, return_table=True)
Mu = Table.eigenvalues[1]
for Count in [80, 160]:
	Value = Half._spectral_green(Blocks, Mu, 1, 'N', 0.1, 0.1, Count, spectrum=Table)
	check(f'bound-pole-finite-{Count}', np.isfinite(Value))
rejects('old-wrong-pole-target', lambda: Half._spectral_green(Blocks, (5.5*np.pi/5)**2, 1, 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('right-target-wrong-mode', lambda: Half._spectral_green(Blocks, Mu, 0, 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('geometry-binding', lambda: Half._spectral_green([(0.5,101.0)], Mu, 1, 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('boundary-binding', lambda: Half._spectral_green(Blocks, Mu, 1, 'D', 0.1, 0.1, 80, spectrum=Table))
rejects('pole-outside-prefix', lambda: Half._spectral_green(Blocks, Mu, 1, 'N', 0.1, 0.1, 1, spectrum=Table))
rejects('insufficient-table', lambda: Half._spectral_green(Blocks, Mu, 1, 'N', 0.1, 0.1, 161, spectrum=Table))
rejects('full-pole', lambda: Half._spectral_full_green(Blocks, Mu, 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('full-near-pole', lambda: Half._spectral_full_green(Blocks, np.nextafter(Mu, np.inf), 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('uncovered-full-target', lambda: Half._spectral_full_green(Blocks, Table.eigenvalues[-1]*2, 'N', 0.1, 0.1, 80, spectrum=Table))
rejects('outside-point', lambda: Half._spectral_green(Blocks, Mu, 1, 'N', -0.1, 0.1, 80, spectrum=Table))
rejects('invalid-target', lambda: Half._spectral_green(Blocks, np.nan, 1, 'N', 0.1, 0.1, 80, spectrum=Table))
for Value in [False, 0, -1, 2.5]:
	rejects('count-' + repr(Value), lambda: Half.half_spectrum(Blocks, 'D', Value))
for Boundary in ['X', None, 1]:
	rejects('bc-' + repr(Boundary), lambda: Half.half_spectrum(Blocks, Boundary, 4))
for Bad in [[(0.0,1)], [(0.5,-1)], [(np.inf,1)], [(0.5,1+1j)], [(1,1),(1e-20,2)]]:
	rejects('blocks-' + repr(Bad), lambda: Half.half_spectrum(Bad, 'D', 4))
rejects('too-small-mumax', lambda: Half.half_spectrum(Blocks, 'D', 4, mumax=0.1))
rejects('unresolved-refinement', lambda: indexed_roots(Blocks, 4, Refine=1, RightBoundary='N'))
check('legacy-dirichlet-default', np.array_equal(indexed_roots(Blocks,4)[0], indexed_roots(Blocks,4,RightBoundary='D')[0]))

# Independent ODE transfer and physical zero count at high precision. This
# has no lifted-angle interface maps and does not import the phase engine.
mp.mp.dps = 70
def transfer(Blocks, Frequency, Boundary, CountZeros=False):
	Y, Derivative, Start = mp.mpf(0), mp.mpf(1), mp.mpf(0)
	Zeros = []
	Length = sum(mp.mpf(str(Block[0])) for Block in Blocks)
	for Width, Density in Blocks:
		Width, Density = mp.mpf(str(Width)), mp.mpf(str(Density))
		Wave = Frequency * mp.sqrt(Density)
		Angle = mp.atan2(Wave * Y, Derivative)
		if CountZeros:
			for J in range(int(mp.floor(Angle/mp.pi))-1, int(mp.ceil((Angle+Wave*Width)/mp.pi))+2):
				Local = (J*mp.pi-Angle)/Wave
				Position = Start + Local
				if -mp.mpf('1e-45') <= Local <= Width+mp.mpf('1e-45') and mp.mpf('1e-40') < Position < Length-mp.mpf('1e-40'):
					if all(abs(Position-Old)>mp.mpf('1e-40') for Old in Zeros):
						Zeros.append(Position)
		C, S = mp.cos(Wave*Width), mp.sin(Wave*Width)
		Y, Derivative = Y*C + Derivative*S/Wave, -Wave*Y*S + Derivative*C
		Start += Width
	return len(Zeros) if CountZeros else (Y if Boundary == 'D' else Derivative)

for Case, Blocks in enumerate([[(.1,1),(.05,100),(.35,2)],[(.499,1),(.001,1e4)]]):
	for Boundary in ['D','N']:
		Values = Half.half_spectrum(Blocks, Boundary, 20)
		check(f'piece-prefix-{Case}-{Boundary}', np.array_equal(Values[:4],Half.half_spectrum(Blocks,Boundary,4)))
		for Mode in [1,2,5,15]:
			Guess = mp.sqrt(mp.mpf(float(Values[Mode-1])))
			Frequency = mp.findroot(lambda W:transfer(Blocks,W,Boundary), (Guess*(1-mp.mpf('1e-7')), Guess*(1+mp.mpf('1e-7'))), tol=mp.mpf('1e-60'))
			check(f'physical-index-{Case}-{Boundary}-{Mode}', transfer(Blocks,Frequency,Boundary,True)==Mode-1)
			check(f'transfer-root-{Case}-{Boundary}-{Mode}', abs(float(Frequency**2)/Values[Mode-1]-1)<3e-12)

Tab = json.loads((Root/'scripts/op03_gap_table.json').read_text())
for N in [2,3]:
	for Mode in ['sup','inf']:
		Rc = Recon(N,4.0,Mode)
		Edges = np.array(Tab[f'n{N}_{Mode.upper()}']['edges'])
		Z = symmetric_root(Rc, Rc.widths_to_z(np.diff(np.r_[0.0,Edges,1.0])))
		Data = eigen_data(Rc,Z)
		Jumps = np.diff(Rc.pat)
		Raw = np.diag(1/Jumps) @ analytic_jacobian_spectral(Rc,Z,N=160)
		Identity = np.eye(2*N)
		Be = (Identity[:,:N]+Identity[:,::-1][:,:N])/np.sqrt(2)
		Bo = (Identity[:,:N]-Identity[:,::-1][:,:N])/np.sqrt(2)
		S = np.diag(Data['eps'])
		E = np.diag(Data['eps'][:N])
		Sector = sector_data(Rc,Z,N=160)
		for Key, Exact in [('Ke',Be.T@Raw@Be),('Ko',Bo.T@Raw@Bo),('KpEven',Be.T@S@Raw@S@Be),('KpOdd',Bo.T@S@Raw@S@Bo)]:
			Error = float(np.max(np.abs(np.array(Sector[Key])-Exact)))
			check(f'full-J-sector-{N}-{Mode}-{Key}',Error<3e-8,Error)
		check(f'sector-swap-{N}-{Mode}',np.max(abs(np.array(Sector['KpOdd'])-E@np.array(Sector['Ke'])@E))<1e-12)
		for Parity in ['e','o']:
			check(f'raw-pieces-{N}-{Mode}-{Parity}',np.max(abs(np.array(Sector['K'+Parity])-np.diag(Sector['d'])-np.array(Sector['H'+Parity])-np.array(Sector['E'+Parity])))<1e-12)

# Record every loaded project module, not a prefiltered list that could hide
# an import from a different checkout.
Loaded = {Name:str(Path(Module.__file__).resolve()) for Name,Module in sys.modules.items() if (Name.startswith('_gapn') or Name in ('_sl_prufer','reflection_seeds')) and getattr(Module,'__file__',None)}
check('actual-import-isolation', all(Path(PathValue).is_relative_to(Root/'scripts') for PathValue in Loaded.values()), Loaded)
Output = dict(status='PASS', optimized=not __debug__, count=len(Results), checks=Results, source_hashes={Name:hashlib.sha256(Path(PathValue).read_bytes()).hexdigest() for Name,PathValue in Loaded.items()}, scope='Finite floating/high-precision diagnostics, exact prefix identities and rejection controls; not interval certification or global SL theorem')
print(json.dumps(Output,ensure_ascii=False,indent=2))
