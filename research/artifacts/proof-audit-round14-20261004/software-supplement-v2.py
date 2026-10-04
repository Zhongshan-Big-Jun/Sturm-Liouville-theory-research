"""Independent reviewer probes of frozen round14 software only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import traceback

Parser = argparse.ArgumentParser()
Parser.add_argument('--root', type=Path, required=True)
Parser.add_argument('--output', type=Path, required=True)
Args = Parser.parse_args()
Root = Args.root.resolve()
Manifest = json.loads((Root / 'hashes.json').read_text(encoding='utf-8-sig'))
for Name, Digest in Manifest.items():
	if hashlib.sha256((Root / Name).read_bytes()).hexdigest() != Digest:
		raise RuntimeError('frozen input hash mismatch: ' + Name)
sys.dont_write_bytecode = True
sys.path.insert(0, str(Root / 'scripts'))
sys.path.insert(0, str(Root / 'research/artifacts/proof-audit-round14-20261004'))
import numpy as np
from _gapn2_symmetry_recon import Recon, one_solve
from _gapn2_jacobian_probe import symmetric_root
from _gapn2_jacobian_analytic import eigen_data, term_breakdown, analytic_jacobian
from _gapn2_jacobian_spectral import gtilde_spectral
from _gapn2_sector_decomposition import sector_data
from _gapn2_ktilde_positivity import run as positivity_run
from _gapn2_half_problem_probe import HalfSpectrum, green_regularized, _spectral_green
from _gapn2_reduced_endpoint_hunt import Reduced, one as reduced_one
from independent_physical import evaluate

Records = []
def record(Name, Condition, Details=None):
	Records.append(dict(name=Name, passed=bool(Condition), details=Details))

def rejects(Name, Function):
	try:
		Value = Function()
	except (ValueError, ArithmeticError) as Error:
		record(Name, True, dict(exception=type(Error).__name__, message=str(Error)))
	else:
		record(Name, False, dict(unexpected_result=str(Value)))

def error(Left, Right):
	return float(np.max(np.abs(np.asarray(Left)-np.asarray(Right))))

Failure = None
try:
	Seeds = {'sup':[.29343444668879154,.36546070235557726,.6345392976444227,.7065655533112085],
		'inf':[.2028824169434251,.4040382298316725,.5959617701683275,.7971175830565749]}
	for Mode, Edges in Seeds.items():
		Rc = Recon(2, 4., Mode)
		Z = symmetric_root(Rc, Rc.widths_to_z(np.diff(np.r_[0., Edges, 1.])))
		record(Mode+'_interior_root_retained', Z is not None)
		if Z is None:
			continue
		Data = eigen_data(Rc, Z)
		Hp = evaluate(Rc.blocks_from_z(Z), [(2,np.sqrt(Data['lam_n'])),(3,np.sqrt(Data['lam_np1']))],dps=80)
		ModeErrors = []
		for Reference, Name in zip(Hp['modes'], ['u_n','u_np1']):
			ModeErrors.append(error(np.array(Reference['values'],float),Data[Name]))
			ModeErrors.append(error(np.array(Reference['derivatives'],float),Data['up_n' if Name=='u_n' else 'up_np1']))
		record(Mode+'_physical_quadrature_mass_and_one_based_modes',
			max(ModeErrors)<1e-10 and [Item['internal_zero_count'] for Item in Hp['modes']]==[1,2],
			dict(errors=ModeErrors,reference=Hp))
		N = 40
		Terms = term_breakdown(Rc,Z,N=N)
		J = (np.diag(Terms['fprime'])+Terms['M1']+Terms['M2']+Terms['M3'])/Data['lam_np1']
		K = np.diag(1./np.diff(Rc.pat)) @ J
		S = np.diag(Data['eps'])
		Kp = S @ K @ S
		Be = np.array([[1,0],[0,1],[0,1],[1,0]])/np.sqrt(2.)
		Bo = np.array([[1,0],[0,1],[0,-1],[-1,0]])/np.sqrt(2.)
		RawEven, RawOdd = Be.T@K@Be, Bo.T@K@Bo
		ConjugateEven, ConjugateOdd = Be.T@Kp@Be, Bo.T@Kp@Bo
		Sd = sector_data(Rc,Z,N=N)
		RawErrors = [error(Sd['Ke'],RawEven),error(Sd['Ko'],RawOdd)]
		ConjugateErrors = [error(Sd['KpEven'],ConjugateEven),error(Sd['KpOdd'],ConjugateOdd)]
		record(Mode+'_sector_data_retains_raw_and_SKS_identity',max(RawErrors+ConjugateErrors)<1e-9,
			dict(raw_errors=RawErrors,conjugate_errors=ConjugateErrors))
		Po = positivity_run(2,Mode,4.,Z,N=N)
		RawEigenErrors = [error(Po['evKe'],np.linalg.eigvalsh(RawEven)),error(Po['evKo'],np.linalg.eigvalsh(RawOdd))]
		ConjugateEigenErrors = [error(Po['evKe'],np.linalg.eigvalsh(ConjugateEven)),error(Po['evKo'],np.linalg.eigvalsh(ConjugateOdd))]
		record(Mode+'_positivity_run_Ke_Ko_are_declared_raw_K',max(RawEigenErrors)<1e-9,
			dict(raw_eigen_errors=RawEigenErrors,SKS_eigen_errors=ConjugateEigenErrors,
				returned_even=Po['evKe'].tolist(),returned_odd=Po['evKo'].tolist(),
				raw_even=np.linalg.eigvalsh(RawEven).tolist(),raw_odd=np.linalg.eigvalsh(RawOdd).tolist()))
		ExplicitKpErrors = [error(Po['evKpEven'],np.linalg.eigvalsh(ConjugateEven)),error(Po['evKpOdd'],np.linalg.eigvalsh(ConjugateOdd))]
		record(Mode+'_positivity_run_explicit_Kp_parity_matches_SKS',max(ExplicitKpErrors)<1e-9,ExplicitKpErrors)
		rejects(Mode+'_stationary_positivity_insufficient_mode_coverage',lambda:positivity_run(2,Mode,4.,Z,N=1))
		rejects(Mode+'_full_target_slightly_off_own_eigenvalue',lambda:gtilde_spectral(Rc,Z,Data['lam_n']*(1.+1e-9),1,Data['edges'],N=20))
	Rc = Recon(2,4.,'sup')
	Delta = 1e-6
	Negative = Rc.widths_to_z([Delta,Delta,1.-4.*Delta,Delta,Delta])
	Report = Rc.full_report(Negative)
	record('full_report_does_not_label_small_absolute_residual_stationary',not Report['stationary'],Report['stationarity'])
	record('one_solve_does_not_accept_negative_control',one_solve((2,4.,'sup',Negative,'review-negative')) is None)
	General = analytic_jacobian(Rc,Negative,N=20)
	record('nonstationary_J_F_finite_and_stationary_Wronskian_identity_absent',np.all(np.isfinite(General[0])) and General[2] is None)
	for End in ['first','last','both']:
		Rd = Reduced(2,4.,'sup',End)
		Widths = np.full(Rd.nb,Delta); Widths[Rd.nb//2] = 1.-(Rd.nb-1)*Delta
		Z = Rd.widths_to_z(Widths)
		record('reduced_'+End+'_actual_one_rejects_collapsed_candidate',reduced_one((2,4.,'sup',End,Z)) is None)
	for Boundary in ['D','N']:
		Blocks = [(.11,1.),(.13,4.),(.26,1.)]
		Table = HalfSpectrum(Blocks,Boundary,20)
		Target = Table.eigenvalues[1]
		rejects('closed_'+Boundary+'_near_but_distinct_target_rejected',lambda:green_regularized(Blocks,Target*(1.+1e-9),.11,.24,Boundary,mode=2,spectrum=Table))
		rejects('spectral_'+Boundary+'_near_but_distinct_target_rejected',lambda:_spectral_green(Blocks,Target*(1.+1e-9),1,Boundary,.11,.24,N=20,spectrum=Table))
	Imported = {}
	for Name, Module in list(sys.modules.items()):
		FileName = getattr(Module,'__file__',None)
		if FileName:
			try:
				Relative = Path(FileName).resolve().relative_to(Root).as_posix()
			except ValueError:
				continue
			Imported[Name] = Relative
	record('all_imported_frozen_project_modules_are_manifest_listed',all(Value in Manifest for Value in Imported.values()),Imported)
	Final = {Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in Manifest}
	record('all_frozen_inputs_remained_unchanged',Final==Manifest)
except Exception as ErrorValue:
	Failure = dict(type=type(ErrorValue).__name__,message=str(ErrorValue),traceback=traceback.format_exc())
Result = dict(reviewer='/root/r14_software_review',root=str(Root),python=sys.version,optimization=sys.flags.optimize,
	manifest_sha256=hashlib.sha256((Root/'hashes.json').read_bytes()).hexdigest(),
	probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
	passed=Failure is None and all(Item['passed'] for Item in Records),checks=len(Records),records=Records,error=Failure,
	limitations='Finite floating point source and numerical audit; no analytic supplement or full parameter theorem proof; no Lean executed.')
Args.output.write_text(json.dumps(Result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=Result['passed'],checks=Result['checks'],failed=[Item['name'] for Item in Records if not Item['passed']],error=Failure)))
if not Result['passed']:
	raise SystemExit(1)
