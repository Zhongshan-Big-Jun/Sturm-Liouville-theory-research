"""Bounded behavior checks of actual functions/AST expressions; no historical scan.

All truth checks use explicit branches, so -O cannot disable them. Scalar
expressions are compiled unchanged from their source AST and bound to real
spectral data. The loader removes only module For scans and __main__ guards.
"""
import argparse
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import sys
import traceback
import types

import numpy as np
import scipy
from scipy.integrate import quad

from backend_probe import ivp_reference
import provenance

Base = Path(__file__).resolve().parents[1]
Rows = []
LoadLog = []
ExpressionLog = []
Trees = {}


def serial(Value):
	if isinstance(Value,np.ndarray): return Value.tolist()
	if isinstance(Value,np.generic): return Value.item()
	if isinstance(Value,dict): return {K:serial(V) for K,V in Value.items()}
	if isinstance(Value,(list,tuple)): return [serial(V) for V in Value]
	return Value


def record(Name, Passed, **Details):
	Rows.append(dict(name=Name,passed=bool(Passed),**serial(Details)))
	print(('PASS ' if Passed else 'FAIL ')+Name,flush=True)


def close(Name, Actual, Expected, atol=2e-5, rtol=2e-6, **Details):
	A, B = np.asarray(Actual),np.asarray(Expected)
	Passed = A.shape==B.shape and np.all(np.isfinite(A)) and np.all(np.isfinite(B)) and np.allclose(A,B,atol=atol,rtol=rtol)
	Error = float(np.max(np.abs(A-B))) if A.shape==B.shape else None
	record(Name,Passed,actual=A,expected=B,max_abs_error=Error,atol=atol,rtol=rtol,**Details)


def source_tree(Name):
	if Name not in Trees:
		P = Scripts/(Name+'.py')
		Trees[Name] = ast.parse(P.read_text(encoding='utf-8-sig'),filename=str(P))
	return Trees[Name]


def load_without_scan(Name):
	P = Scripts/(Name+'.py')
	Tree = source_tree(Name)
	Body, Removed = [],[]
	for Node in Tree.body:
		IsGuard = isinstance(Node,ast.If) and any(isinstance(N,ast.Name) and N.id=='__name__' for N in ast.walk(Node.test))
		if isinstance(Node,ast.For) or IsGuard:
			Removed.append(dict(kind=type(Node).__name__,line=Node.lineno,end=Node.end_lineno))
		else: Body.append(Node)
	Module = types.ModuleType(Name)
	Module.__file__=str(P)
	sys.modules[Name]=Module
	exec(compile(ast.Module(body=Body,type_ignores=[]),str(P),'exec'),Module.__dict__)
	LoadLog.append(dict(module=Name,sha256=hashlib.sha256(P.read_bytes()).hexdigest(),removed=Removed))
	return Module


def eval_node(Name,Node,Bindings,Label):
	Dump = ast.dump(Node,include_attributes=False)
	ExpressionLog.append(dict(source=Name+'.py',label=Label,line=Node.lineno,end=Node.end_lineno,ast_sha256=hashlib.sha256(Dump.encode()).hexdigest(),expression=ast.unparse(Node)))
	return eval(compile(ast.Expression(body=Node),str(Scripts/(Name+'.py')),'eval'),{'np':np,**Bindings})


def owner_tree(Name,Owner):
	Tree=source_tree(Name)
	if Owner is None: return Tree
	return next(N for N in Tree.body if isinstance(N,ast.FunctionDef) and N.name==Owner)


def assignment(Name,Target,Bindings,Owner=None):
	Nodes=[N.value for N in ast.walk(owner_tree(Name,Owner)) if isinstance(N,ast.Assign) and any(isinstance(T,ast.Name) and T.id==Target for T in N.targets)]
	if len(Nodes)!=1: raise RuntimeError(f'{Name}:{Target} has {len(Nodes)} assignments')
	return eval_node(Name,Nodes[0],Bindings,Target)


def formatted_product(Name,Variable,Bindings):
	Nodes=[N.value for N in ast.walk(source_tree(Name)) if isinstance(N,ast.FormattedValue) and any(isinstance(V,ast.Name) and V.id==Variable for V in ast.walk(N.value)) and any(isinstance(V,ast.BinOp) for V in ast.walk(N.value))]
	if len(Nodes)!=1: raise RuntimeError(f'{Name}: formatted {Variable}: {len(Nodes)}')
	return eval_node(Name,Nodes[0],Bindings,'formatted '+Variable)


def hess_gradient(F,S):
	Name='_gapn2_hess_verify'
	Nodes=[N.args[0] for N in ast.walk(source_tree(Name)) if isinstance(N,ast.Call) and isinstance(N.func,ast.Attribute) and N.func.attr=='round' and N.args and any(isinstance(V,ast.Name) and V.id=='f' for V in ast.walk(N.args[0]))]
	if len(Nodes)!=1: raise RuntimeError('gradient print expression ambiguous')
	return eval_node(Name,Nodes[0],{'s':S,'f':F},'gradient printed comparison')


def central_gradient(Function,X,H):
	Basis=np.eye(len(X))
	return np.array([(Function(X+H*E)-Function(X-H*E))/(2*H) for E in Basis])


def central_hessian(Function,X,H):
	Basis=np.eye(len(X))
	return np.array([[(Function(X+H*A+H*B)-Function(X+H*A-H*B)-Function(X-H*A+H*B)+Function(X-H*A-H*B))/(4*H*H) for B in Basis] for A in Basis])


def blocks_from_edges(Edges,Pattern):
	return list(zip(np.diff(np.r_[0.0,Edges,1.0]),Pattern))


def spectral_gap(Blocks):
	Roots=ReconModule.roots_of(Blocks,2)
	return Roots[1]**2-Roots[0]**2


def test_selected_backend():
	for Label,Blocks in [('symmetric',[(.3,1.),(.4,4.),(.3,1.)]),('asymmetric',[(.23,1.),(.36,4.),(.41,1.)])]:
		Roots=FH.lams_precise(Blocks,2)
		Points=np.array([.1,.23,.4,.59,.8,1.])
		U=FH.eigfuns_precise(Blocks,Roots,Points)
		Refs=[ivp_reference(Blocks,S*S,Points) for S in Roots]
		close(f'op03 backend/{Label}/IVP values',U,np.array([R[0] for R in Refs]),atol=2e-8,rtol=2e-8,backend=FH.eigfuns_precise.__module__,blocks=Blocks)
		close(f'op03 backend/{Label}/IVP boundary',[R[1] for R in Refs],np.zeros(2),atol=2e-8)
		Xs=np.r_[0.,np.cumsum([L for L,_ in Blocks])]
		Mass=[sum(Rho*quad(lambda X:FH.eigfuns_precise(Blocks,np.array([S]),np.array([X]))[0,0]**2,Xs[I],Xs[I+1],epsabs=1e-10)[0] for I,(_,Rho) in enumerate(Blocks)) for S in Roots]
		close(f'op03 backend/{Label}/weighted mass',Mass,np.ones(2),atol=2e-9,rtol=2e-9)
		close(f'op03 backend/{Label}/roots versus recon',Roots,ReconModule.roots_of(Blocks,2),atol=2e-11,rtol=2e-11)
	for U in (.30,.43):
		D,F=FH.Df_at(U)
		Expected=(FH.Df_at(U+1e-5)[0]-FH.Df_at(U-1e-5)[0])/(2e-5)
		Actual=formatted_product('op03_gap_fh','f',{'R':4.,'f':F})
		close(f'op03_gap_fh paired SUP u={U}',Actual,Expected,atol=3e-5,u=U,D=D,f=F)


def test_single_interface():
	R=4.
	X=np.array([.37])
	for Mode,Pattern in [('SUP',[1.,R]),('INF',[R,1.])]:
		Blocks=blocks_from_edges(X,Pattern)
		Roots=Grad.lams_fast(Blocks,2)
		Lams=Roots**2
		Values=np.array([Grad.y_at(Blocks,S,X)[0]/np.sqrt(Grad.norm2(Blocks,S)) for S in Roots])
		F=Lams[0]*Values[0]**2-Lams[1]*Values[1]**2
		S=Pattern[1]-Pattern[0]
		for H in (2e-5,1e-5):
			Numeric=central_gradient(lambda E:Grad.D_of(blocks_from_edges(E,Pattern)),X,H)
			close(f'single interface {Mode}/gap h={H}',-S*F,Numeric[0],blocks=Blocks,f=F)
			Lp=Grad.lams_fast(blocks_from_edges(X+H,Pattern),2)**2
			Lm=Grad.lams_fast(blocks_from_edges(X-H,Pattern),2)**2
			close(f'single interface {Mode}/lambda h={H}',Lams*S*Values**2,(Lp-Lm)/(2*H))


def test_n1_diagnostics():
	R=4.
	for Mode in ('SUP','INF'):
		A,B=.23,.36
		Blocks=Grad.make_blocks(Mode,R,A,B)
		F=Grad.f_vals(Blocks,[A,A+B])
		Actual=assignment('gap_n1_grad','gFH',{'R':R,'f':F,'mode':Mode})
		Numeric=central_gradient(lambda W:Grad.D_of(Grad.make_blocks(Mode,R,*W)),np.array([A,B]),1e-5)
		close(f'gap_n1_grad {Mode}/width chain rule',Actual,Numeric,a=A,b=B,f=F)
		close(f'gap_n1_grad {Mode}/actual num_grad',np.array(Grad.num_grad(Mode,R,A,B)),Numeric,atol=.004,rtol=5e-5)
		U=.30
		D,F,_=Paradox.D_and_f(Mode,R,U,npts=5000)
		Numeric=(Paradox.D_and_f(Mode,R,U+1e-5,npts=5000)[0]-Paradox.D_and_f(Mode,R,U-1e-5,npts=5000)[0])/(2e-5)
		record(f'paired {Mode}/nonstationary fixture',abs(Numeric)>1.,derivative=Numeric,f=F)
		for Target in ('fh','fh2'):
			Actual=assignment('_tmp_fh_paradox',Target,{'R':R,'f':F,'mode':Mode})
			close(f'_tmp_fh_paradox {Mode}/{Target}',Actual,Numeric,atol=3e-5)
		D,F,_=Endpoints.D_and_f(Mode,R,U,npts=5000)
		Numeric=(Endpoints.D_and_f(Mode,R,U+1e-5,npts=5000)[0]-Endpoints.D_and_f(Mode,R,U-1e-5,npts=5000)[0])/(2e-5)
		Actual=assignment('tmp_verify_endpoints','fh',{'R':R,'f':F,'mode':Mode})
		close(f'tmp_verify_endpoints {Mode}/paired',Actual,Numeric,atol=3e-5)
	U=.20
	Lams,Blocks,Roots=LamProbe.lam_of('INF',R,U,npts=5000)
	Values=[LamProbe.y_at(Blocks,S,np.array([U,1-U]))/np.sqrt(LamProbe.norm2(Blocks,S)) for S in Roots]
	Numeric=(LamProbe.lam_of('INF',R,U+1e-5,npts=5000)[0]-LamProbe.lam_of('INF',R,U-1e-5,npts=5000)[0])/(2e-5)
	Env={'R':R,'lam':Lams,'u1':Values[0],'u2':Values[1]}
	for I,Target in enumerate(('fh1','fh2')):
		close(f'tmp_fh_test INF/{Target}',assignment('tmp_fh_test',Target,Env),Numeric[I],atol=3e-5)
	Actual=formatted_product('tmp_fh_test','R',Env)
	close('tmp_fh_test INF/gap',Actual,Numeric[1]-Numeric[0],atol=3e-5)


def data_at(Rc,Edges):
	Z=Rc.widths_to_z(np.diff(np.r_[0.,Edges,1.]))
	Ed=Analytic.eigen_data(Rc,Z)
	Env={'ed':Ed,'lam':Ed['lam_np1']}
	F=assignment('_gapn2_hess_verify','f',Env,'main')
	S=np.diff(Rc.pat)
	return Z,Ed,F,S


def test_nonstationary_full():
	for Mode in ('sup','inf'):
		Rc=ReconModule.Recon(1,4.,Mode)
		Edges=np.array([.23,.59])
		Z,Ed,F,S=data_at(Rc,Edges)
		Gap=lambda E:HessVerify.D_edges(Rc,E)
		TrueF,_,_=Rc.f_at(Z,Edges)
		close(f'hess_verify {Mode}/lower eigenvalue in f',F,TrueF,atol=1e-10,rtol=1e-10)
		for H in (2e-5,1e-5):
			Numeric=central_gradient(Gap,Edges,H)
			close(f'hess_verify {Mode}/nonstationary gradient h={H}',hess_gradient(F,S),Numeric,atol=3e-5)
		J=Probe.jac_fd(Rc,Z,h=1e-6)
		Lam=Ed['lam_np1']
		GradLam=Lam*S*Ed['u_np1']**2
		Full=-np.diag(S)@(Lam*J+np.outer(TrueF/Lam,GradLam))
		Simple=-Lam*np.diag(S)@J
		Hfd=central_hessian(Gap,Edges,2e-4)
		close(f'nonstationary {Mode}/product rule Hessian',Full,Hfd,atol=.01,rtol=3e-5)
		record(f'nonstationary {Mode}/simple Hessian excluded',np.max(np.abs(Simple-Hfd))>1.,omitted_term=np.diag(S)@np.outer(TrueF/Lam,GradLam),simple_error=float(np.max(np.abs(Simple-Hfd))))
		ActualGradJac=np.column_stack([(hess_gradient(data_at(Rc,Edges+1e-5*E)[2],S)-hess_gradient(data_at(Rc,Edges-1e-5*E)[2],S))/(2e-5) for E in np.eye(2)])
		close(f'hess_verify {Mode}/differentiate actual gradient',ActualGradJac,Hfd,atol=.01,rtol=3e-5)


def test_stationary_hessian():
	Table=json.loads((Scripts/'op03_gap_table.json').read_text(encoding='utf-8-sig'))
	for N in (1,2):
		for Mode in ('sup','inf'):
			Rc=ReconModule.Recon(N,4.,Mode)
			E0=np.array(Table[f'n{N}_{Mode.upper()}']['edges'])
			Z=Probe.symmetric_root(Rc,Rc.widths_to_z(np.diff(np.r_[0.,E0,1.])))
			if Z is None: raise RuntimeError('bounded stationary solve failed')
			Edges=np.cumsum(Rc.z_to_widths(Z))[:-1]
			Residual=Rc.residual(Z)
			record(f'n={N} {Mode}/stationary premise',np.max(np.abs(Residual))<1e-9,edges=Edges,residual=Residual)
			Ed=Analytic.eigen_data(Rc,Z)
			S=np.diff(Rc.pat)
			Lam=Ed['lam_np1']
			J=Probe.jac_fd(Rc,Z,h=1e-6)
			Gap=lambda E:HessVerify.D_edges(Rc,E)
			Hfd=central_hessian(Gap,Edges,1e-4)
			Hcoarse=central_hessian(Gap,Edges,2e-4)
			close(f'n={N} {Mode}/FD step convergence',Hcoarse,Hfd,atol=.04,rtol=1e-4)
			FromWidths=HessSign.hess_fd(Rc,Z,h=5e-5)
			close(f'hess_sign n={N} {Mode}/actual hess_fd coordinates',FromWidths,Hfd,atol=.02,rtol=6e-5)
			Off=Hfd-np.diag(np.diag(Hfd))
			record(f'n={N} {Mode}/nonzero offdiagonal fixture',np.max(np.abs(Off))>1.,max_offdiag=float(np.max(np.abs(Off))))
			Env={'lam':Lam,'lam_np1':Lam,'s':S,'J':J,'Jfd':J,'sign':-1.}
			Checks=[('_gapn2_hess_verify','H1'),('_gapn2_hess_verify','H2'),('_gapn2_hess_sign_and_bigR','H'),('_gapn2_jacobian_analytic','H'),('_gapn2_second_variation_probe','Hess')]
			for Name,Target in Checks:
				Actual=assignment(Name,Target,Env,'main')
				close(f'{Name} n={N} {Mode}/{Target} actual matrix',Actual,Hfd,atol=.015,rtol=5e-5)
				close(f'{Name} n={N} {Mode}/{Target} inertia spectrum',np.linalg.eigvalsh(Actual),np.linalg.eigvalsh(Hfd),atol=.02,rtol=6e-5)
			Actual=assignment('_gapn2_o3_scan','evH',Env,'main')
			close(f'_gapn2_o3_scan n={N} {Mode}/evH',Actual,np.linalg.eigvalsh(Hfd),atol=.02,rtol=6e-5)
			Plus=assignment('_gapn2_hess_sign_and_bigR','H',{**Env,'sign':1.},'main')
			close(f'hess_sign n={N} {Mode}/positive-sign negative control',Plus,-Hfd,atol=.015,rtol=5e-5)
			B=np.eye(2*N)[:,:N]-np.eye(2*N)[:,::-1][:,:N]
			Reduced=central_hessian(lambda Y:Gap(Edges+B@Y),np.zeros(N),1e-4)
			Full=assignment('_gapn2_hess_verify','H1',Env,'main')
			close(f'mirror chain rule n={N} {Mode}/B.T H B',B.T@Full@B,Reduced,atol=.05,rtol=7e-5)
			close(f'mirror chain rule n={N} {Mode}/B.T grad',B.T@hess_gradient(assignment('_gapn2_hess_verify','f',{'ed':Ed,'lam':Lam},'main'),S),central_gradient(lambda Y:Gap(Edges+B@Y),np.zeros(N),1e-5),atol=1e-4)


def main():
	global Scripts,FH,Grad,Paradox,LamProbe,Endpoints,ReconModule,Probe,Analytic,HessVerify,HessSign
	Parser=argparse.ArgumentParser()
	Parser.add_argument('--tree',choices=('originals','candidates'),required=True)
	Parser.add_argument('--output',required=True)
	provenance.control_arguments(Parser)
	Args=Parser.parse_args()
	ImportedControl=provenance.import_control(Args,Base)
	Scripts=Base/Args.tree/'scripts'
	os.chdir(Base/Args.tree)
	# backend_probe's reference import adds originals; remove it before any target import.
	sys.path[:]=[str(Scripts)]+[P for P in sys.path if P not in (str(Base/'originals'/'scripts'),str(Base/'candidates'/'scripts'))]
	Output=(Base/Args.output).resolve()
	if not Output.is_relative_to(Base): raise RuntimeError('Output outside author directory')
	FH=load_without_scan('op03_gap_fh')
	Grad=load_without_scan('gap_n1_grad')
	Paradox=load_without_scan('_tmp_fh_paradox')
	LamProbe=load_without_scan('tmp_fh_test')
	Endpoints=load_without_scan('tmp_verify_endpoints')
	ReconModule=importlib.import_module('_gapn2_symmetry_recon')
	Probe=importlib.import_module('_gapn2_jacobian_probe')
	Analytic=importlib.import_module('_gapn2_jacobian_analytic')
	HessVerify=importlib.import_module('_gapn2_hess_verify')
	HessSign=importlib.import_module('_gapn2_hess_sign_and_bigR')
	for Test in (test_selected_backend,test_single_interface,test_n1_diagnostics,test_nonstationary_full,test_stationary_hessian):
		try: Test()
		except Exception:
			record(Test.__name__+'/exception',False,traceback=traceback.format_exc())
			traceback.print_exc()
	Sources={P.name:hashlib.sha256(P.read_bytes()).hexdigest() for P in sorted(Scripts.iterdir()) if P.is_file()}
	Gate=provenance.report(Base,Args.tree,'numerical',Args,ImportedControl)
	Bindings=Gate['module_files']
	Summary=dict(tree=Args.tree,python=sys.version,executable=sys.executable,platform=platform.platform(),optimize=sys.flags.optimize,numpy=np.__version__,scipy=scipy.__version__,tests=len(Rows),passed=sum(R['passed'] for R in Rows),failed=sum(not R['passed'] for R in Rows),source_sha256=Sources,module_files=Bindings,provenance=Gate,loader=LoadLog,expressions=ExpressionLog,checks=Rows)
	Output.parent.mkdir(exist_ok=True,parents=True)
	Output.write_text(json.dumps(Summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
	print(json.dumps({K:Summary[K] for K in ('tree','optimize','tests','passed','failed')}))
	return provenance.GATE_EXIT if not Gate['accepted'] else int(Summary['failed']!=0)

if __name__=='__main__':
	sys.exit(main())
