"""R14-02 tests of actual working sources; numerical checks, not a proof audit.

Run with the same interpreter normally and with -O. Checks use explicit
exceptions, never assert. Baseline defect observations are saved separately.
"""
import argparse
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import warnings

sys.dont_write_bytecode = True
Root = Path(__file__).resolve().parents[3]
if '--root' in sys.argv:
	Root = Path(sys.argv[sys.argv.index('--root')+1]).resolve()
Work = Path(__file__).resolve().parent
Sources = ['scripts/_sl_spectral_identity.py','scripts/_gapn2_jacobian_spectral.py',
	'scripts/_gapn2_half_problem_probe.py','scripts/_gapn2_gtilde_print.py',
	'scripts/_gapn2_symmetry_recon.py','scripts/_gapn2_jacobian_analytic.py',
	'scripts/_gapn2_jacobian_probe.py','scripts/_gapn2_sector_decomposition.py',
	'scripts/_sl_prufer.py']
InitialHashes = {Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in Sources}
sys.path.insert(0, str(Root / 'scripts'))
import numpy as np
from _sl_spectral_identity import IndexedSpectrum, spectral_denominators
from _gapn2_symmetry_recon import Recon, roots_of, eigfun, eigenfunction_states
from _gapn2_jacobian_spectral import gtilde_spectral, gtilde_spectral_blocks, analytic_jacobian_spectral
from _gapn2_gtilde_print import gtilde_spectral as print_spectral
from _gapn2_half_problem_probe import (HalfSpectrum, half_spectrum, green_regularized,
	green_regular, _spectral_green, _spectral_full_green, _full_S)
from _gapn2_jacobian_analytic import eigen_data

Records = []


def check(Name, Condition, Details=None):
	Passed = bool(Condition)
	Records.append(dict(name=Name, passed=Passed, details=Details))
	if not Passed:
		raise RuntimeError('failed check: ' + Name)


def reject(Name, Function):
	try:
		Result = Function()
	except (ValueError, ArithmeticError) as Error:
		check(Name, True, dict(exception=type(Error).__name__, message=str(Error)))
		return
	check(Name, False, dict(unexpected_result=str(Result)))


def max_error(Left, Right):
	return float(np.max(np.abs(np.asarray(Left) - np.asarray(Right))))


def execute():
	warnings.simplefilter('error', RuntimeWarning)
	Rc = Recon(1, 1., 'sup')
	Z = Rc.widths_to_z([.25, .5, .25])
	Blocks = Rc.blocks_from_z(Z)
	Points = np.array([.75, 0., .25, 1., .25])
	Table = IndexedSpectrum(Blocks, 'D', 10)
	for Index in (0, 1, 9):
		Lam = Table.eigenvalues[Index]
		Expected = np.zeros((len(Points), len(Points)))
		for Mode in range(1, 11):
			if Mode == Index + 1:
				continue
			Values = np.sqrt(2.) * np.sin(Mode * np.pi * Points)
			Expected += np.outer(Values, Values) / ((Mode*np.pi)**2 - Lam)
		Result = gtilde_spectral(Rc, Z, Lam, Index, Points, N=9, spectrum=Table)
		Error = max_error(Result, Expected)
		check('full_DD_mode_%d_exact_finite_constant_sum' % (Index+1), Error < 4e-15, Error)
		check('print_mode_%d_uses_same_guarded_kernel' % (Index+1),
			np.array_equal(print_spectral(Blocks, Lam, Index, Points, N=9, spectrum=Table), Result))
		check('full_mode_%d_matrix_symmetry' % (Index+1), np.array_equal(Result, Result.T))
	Lam = Table.eigenvalues[0]
	reject('full_wrong_lam1_k1_rejected', lambda:gtilde_spectral(Rc, Z, Lam, 1, [.25,.75], N=9))
	reject('print_wrong_lam1_k1_rejected', lambda:print_spectral(Blocks, Lam, 1, [.25,.75], N=9))
	reject('full_wrong_lam2_k0_rejected', lambda:gtilde_spectral(Rc, Z, Table.eigenvalues[1], 0, [.25,.75], N=9))
	for Target in (0., -1., 1., float('inf'), float('nan'), complex(Lam), True):
		reject('full_invalid_target_%r' % Target, lambda Target=Target:gtilde_spectral(Rc,Z,Target,0,[.25,.75],N=9))
	for Index in (-1, True, 1.5, 10):
		reject('full_invalid_or_uncovered_k_%r' % Index, lambda Index=Index:gtilde_spectral(Rc,Z,Lam,Index,[.25,.75],N=9))
	for Count in (0, -1, True, 2.5):
		reject('full_invalid_truncation_%r' % Count, lambda Count=Count:gtilde_spectral(Rc,Z,Lam,0,[.25,.75],N=Count))
	for BadPoints in ([-1e-5,.25], [.25,1.000001], [.25,float('nan')], [complex(.25),.75], [[.25,.75]]):
		reject('full_invalid_points_%r' % BadPoints, lambda BadPoints=BadPoints:gtilde_spectral(Rc,Z,Lam,0,BadPoints,N=9))
	reject('full_wrong_geometry_table', lambda:gtilde_spectral(Rc,Z,Lam,0,[.25,.75],N=9,spectrum=IndexedSpectrum([(1.,2.)],'D',10)))
	reject('full_wrong_DN_boundary_table', lambda:gtilde_spectral(Rc,Z,Lam,0,[.25,.75],N=9,spectrum=IndexedSpectrum(Blocks,'N',10)))
	reject('full_short_table', lambda:gtilde_spectral(Rc,Z,Lam,0,[.25,.75],N=9,spectrum=IndexedSpectrum(Blocks,'D',4)))
	for BadBlocks in ([(0.,1.)], [(.5,0.)], [(.5,-1.)], [(float('inf'),1.)], [(1.,complex(1.))], [(1.,)]):
		reject('full_invalid_geometry_%r' % BadBlocks, lambda BadBlocks=BadBlocks:gtilde_spectral_blocks(BadBlocks,Lam,0,[.25],N=9))
	try:
		Table.eigenvalues = (1.,)
	except (AttributeError, TypeError):
		check('indexed_table_assignment_rejected', True)
	else:
		check('indexed_table_assignment_rejected', False)
	LargeTable = IndexedSpectrum([(1., 1e-305)], 'D', 4)
	reject('retained_denominator_overflow_rejected', lambda:spectral_denominators(LargeTable,-1.79e308,4))
	reject('unresolved_eigenvalue_overflow_rejected', lambda:IndexedSpectrum([(1.,1e-309)],'D',4))
	for Boundary in ('D','N'):
		Half = [(.5,100.)]
		HalfTable = half_spectrum(Half,Boundary,N=160,return_table=True)
		Shift = .5 if Boundary == 'N' else 0.
		Expected = ((np.arange(1,161)-Shift)*np.pi/5.)**2
		Error = max_error(HalfTable.prefix(160)/Expected, np.ones(160))
		check('half_%s_160_indexed_constant_modes' % Boundary, Error < 2e-13, Error)
		for Count in (4,80):
			check('half_%s_prefix_%d_invariance' % (Boundary,Count),
				np.array_equal(HalfTable.prefix(Count),half_spectrum(Half,Boundary,N=Count)))
		Target = HalfTable.eigenvalues[1]
		check('half_%s_valid_reduced_sum_finite' % Boundary,
			np.isfinite(_spectral_green(Half,Target,1,Boundary,.1,.2,N=80,spectrum=HalfTable)))
		reject('half_%s_mismatched_pole_rejected' % Boundary,
			lambda:_spectral_green(Half,Target,0,Boundary,.1,.2,N=80,spectrum=HalfTable))
		reject('half_%s_uncovered_pole_rejected' % Boundary,
			lambda:_spectral_green(Half,Target,1,Boundary,.1,.2,N=1,spectrum=HalfTable))
		reject('half_%s_full_sum_at_pole_rejected' % Boundary,
			lambda:_spectral_full_green(Half,Target,Boundary,.1,.2,N=80,spectrum=HalfTable))
		reject('half_%s_full_sum_above_table_rejected' % Boundary,
			lambda:_spectral_full_green(Half,HalfTable.eigenvalues[-1]*1.01,Boundary,.1,.2,N=80,spectrum=HalfTable))
		reject('half_%s_wrong_geometry_rejected' % Boundary,
			lambda:_spectral_green([(.5,99.)],Target,1,Boundary,.1,.2,N=80,spectrum=HalfTable))
		for TargetValue in (float('nan'),float('inf'),True,complex(Target)):
			reject('half_%s_invalid_target_%r' % (Boundary,TargetValue),
				lambda TargetValue=TargetValue:_spectral_green(Half,TargetValue,1,Boundary,.1,.2,N=80,spectrum=HalfTable))
		for Mode in (1,2):
			Target = HalfTable.eigenvalues[Mode-1]
			Closed = green_regularized(Half,Target,.1,.2,Boundary,mode=Mode,spectrum=HalfTable)
			Legacy = green_regularized(Half,Target,.1,.2,Boundary)
			check('closed_%s_mode_%d_legacy_inference_matches' % (Boundary,Mode), Closed == Legacy)
			check('closed_%s_mode_%d_symmetry' % (Boundary,Mode),
				abs(Closed-green_regularized(Half,Target,.2,.1,Boundary,mode=Mode,spectrum=HalfTable)) < 2e-14)
			reject('closed_%s_mode_%d_wrong_mode' % (Boundary,Mode),
				lambda:green_regularized(Half,Target,.1,.2,Boundary,mode=3-Mode,spectrum=HalfTable))
			reject('closed_%s_mode_%d_wrong_boundary' % (Boundary,Mode),
				lambda:green_regularized(Half,Target,.1,.2,'N' if Boundary=='D' else 'D'))
		Target = HalfTable.eigenvalues[0]
		for TargetValue in (0.,-1.,1.,float('nan'),float('inf'),True,complex(Target)):
			reject('closed_%s_invalid_target_%r' % (Boundary,TargetValue),
				lambda TargetValue=TargetValue:green_regularized(Half,TargetValue,.1,.2,Boundary,mode=1))
		for BoundaryValue in ('bad',None,True, ['D']):
			reject('closed_%s_invalid_bc_%r' % (Boundary,BoundaryValue),
				lambda BoundaryValue=BoundaryValue:green_regularized(Half,Target,.1,.2,BoundaryValue,mode=1))
		for Mode in (0,-1,True,1.5,1000000000):
			reject('closed_%s_invalid_mode_%r' % (Boundary,Mode),
				lambda Mode=Mode:green_regularized(Half,Target,.1,.2,Boundary,mode=Mode))
		reject('closed_%s_unresolvable_phase_rejected' % Boundary,
			lambda:green_regularized(Half,1e308,.1,.2,Boundary))
		reject('closed_%s_outside_point_rejected' % Boundary,
			lambda:green_regularized(Half,Target,-1e-5,.2,Boundary,mode=1,spectrum=HalfTable))
		reject('closed_%s_table_geometry_mismatch' % Boundary,
			lambda:green_regularized([(.5,99.)],Target,.1,.2,Boundary,mode=1,spectrum=HalfTable))
		reject('closed_%s_table_coverage_rejected' % Boundary,
			lambda:green_regularized(Half,Target,.1,.2,Boundary,mode=2,spectrum=HalfSpectrum(Half,Boundary,1)))
	for GeometryName, Half in [('constant',[(.5,1.)]),('jump',[(.11,1.),(.13,4.),(.26,1.)])]:
		for Boundary, Mode in [('D',1),('N',2)]:
			HalfTable = HalfSpectrum(Half,Boundary,1280)
			Target = HalfTable.eigenvalues[Mode-1]
			Errors = []
			CoarseErrors = []
			for X,Y in [(.11,.11),(.11,.24),(.24,.11),(.24,.24),(0.,.24),(.11,.5)]:
				Closed = green_regularized(Half,Target,X,Y,Boundary,mode=Mode,spectrum=HalfTable)
				Values = [_spectral_green(Half,Target,Mode-1,Boundary,X,Y,N=Count,spectrum=HalfTable) for Count in (320,640,1280)]
				CoarseErrors.append(abs(Closed-(2*Values[1]-Values[0])))
				Errors.append(abs(Closed-(2*Values[2]-Values[1])))
			check('closed_%s_%s_correct_formula_vs_extrapolated_spectrum' % (GeometryName,Boundary),
				max(Errors)<2e-6 and max(CoarseErrors)<2e-6,
				dict(errors=Errors,coarse_errors=CoarseErrors,maximum=max(Errors),threshold=2e-6,truncations=[320,640,1280]))
	for Boundary in ('D','N'):
		Points = np.array([.4,0.,.1,.5,.1])
		X,Y = np.minimum(Points[:,None],Points[None,:]), np.maximum(Points[:,None],Points[None,:])
		for Target in (0.,-1.):
			Expected = X*(.5-Y)/.5 if Boundary=='D' else X
			if Target == -1.:
				Expected = np.sinh(X)*(np.sinh(.5-Y)/np.sinh(.5) if Boundary=='D' else np.cosh(.5-Y)/np.cosh(.5))
			Result = np.array([[green_regular([(.5,1.)],Target,A,B,Boundary) for B in Points] for A in Points])
			Error = max_error(Result,Expected)
			check('ordinary_%s_mu_%s_coordinate_order_and_limits_preserved' % (Boundary,Target),Error<2e-14,Error)
	Points = np.array([0.,.25,.5,.75,1.])
	States = eigenfunction_states([(1.,1.)],2*np.pi,Points)
	Expected = np.column_stack((np.sqrt(2.)*np.sin(2*np.pi*Points),2*np.pi*np.sqrt(2.)*np.cos(2*np.pi*Points)))
	check('physical_common_mass_values_and_derivatives_preserved',max_error(States,Expected)<2e-13,max_error(States,Expected))
	Rc = Recon(1,4.,'sup'); Z = Rc.widths_to_z([.25,.5,.25]); Data = eigen_data(Rc,Z)
	Result = _full_S(Rc,Z,Data,N=80)
	check('collapsed_full_S_finite',np.all(np.isfinite(Result)))
	BadData = dict(Data,lam_n=Data['lam_np1'])
	reject('collapsed_full_S_wrong_target_rejected',lambda:_full_S(Rc,Z,BadData,N=80))
	IndependentPath = Work / 'independent_threeblock.py'
	Spec = importlib.util.spec_from_file_location('round14_independent_threeblock',IndependentPath)
	Reference = importlib.util.module_from_spec(Spec);Spec.loader.exec_module(Reference)
	HighPrecision = Reference.run(); Expected = np.array(HighPrecision['jacobian'],float)
	Errors = [max_error(analytic_jacobian_spectral(Rc,Z,N=Count),Expected) for Count in (160,640)]
	check('general_nonstationary_Jacobian_converges_to_independent_implicit_reference',
		Errors[0]<.037 and Errors[1]<.010 and Errors[1]<Errors[0]/3,
		dict(errors=Errors,reference=HighPrecision,reference_sha256=hashlib.sha256(IndependentPath.read_bytes()).hexdigest()))
	for Order in [('_gapn2_jacobian_analytic','_gapn2_jacobian_spectral'),
		('_gapn2_jacobian_spectral','_gapn2_jacobian_analytic'),
		('_gapn2_half_problem_probe','_gapn2_jacobian_spectral'),
		('_gapn2_gtilde_print','_gapn2_half_problem_probe')]:
		Code = "import sys,importlib;sys.dont_write_bytecode=True;sys.path.insert(0,"+repr(str(Root/'scripts'))+");"+''.join('importlib.import_module('+repr(Name)+');' for Name in Order)
		Command = [sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',Code]
		Process = subprocess.run(Command,cwd=Root,capture_output=True,text=True,timeout=30)
		check('fresh_process_import_order_'+'_then_'.join(Order),Process.returncode==0,
			dict(returncode=Process.returncode,stderr=Process.stderr,stdout=Process.stdout))


def main():
	Parser = argparse.ArgumentParser()
	Parser.add_argument('--root',type=Path,default=Root)
	Parser.add_argument('--output',required=True)
	Arguments = Parser.parse_args()
	Error = None
	try:
		execute()
		check('executed_sources_remained_unchanged',
			InitialHashes=={Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in Sources})
	except Exception as ExceptionValue:
		Error = dict(type=type(ExceptionValue).__name__,message=str(ExceptionValue))
	Output = dict(passed=Error is None,optimization=sys.flags.optimize,
		python=sys.version,checks=Records,error=Error,
		test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
		executed_source_sha256=InitialHashes,
		source_sha256={Name:hashlib.sha256((Root/Name).read_bytes()).hexdigest() for Name in Sources})
	Path(Arguments.output).write_text(json.dumps(Output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
	print(json.dumps(dict(passed=Output['passed'],checks=len(Records),optimization=sys.flags.optimize,error=Error)))
	if Error is not None:
		raise SystemExit(1)


if __name__ == '__main__':
	main()
