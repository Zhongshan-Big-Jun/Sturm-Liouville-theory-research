"""Round13 author property checks: independent references, ordinary and -O."""
import json
import sys
import traceback
import warnings
from pathlib import Path
import numpy as np
import reference as Ref

Root = Path('/mnt/f/LaTeX/BVE research')
sys.path.insert(0,str(Root/'scripts'))
import _gapn2_symmetry_recon as ReconModule
import _gapn2_jacobian_analytic as Analytic
import _gapn2_jacobian_spectral as Spectral
import _gapn2_half_problem_probe as Half
from _gapn2_jacobian_probe import jac_fd, jacobian_cross_blocks, symmetric_root

warnings.simplefilter('error',RuntimeWarning)
Results=[]


def check(Name, Condition, Details=None):
	if not bool(Condition):
		raise RuntimeError('FAILED '+Name+': '+repr(Details))
	Results.append(dict(name=Name,details=Details))


def close(Name, Actual, Expected, Limit):
	Error=float(np.max(abs(np.asarray(Actual,float)-np.asarray(Expected,float))))
	check(Name,np.isfinite(Error) and Error<=Limit,dict(max_error=Error,limit=Limit))
	return Error


def rejects(Name, Operation):
	try:
		Operation()
	except (ValueError,ArithmeticError) as Error:
		check(Name,True,dict(error=type(Error).__name__,message=str(Error)))
	else:
		raise RuntimeError('FAILED expected rejection: '+Name)


def configuration(N,R,Edges,Mode='sup'):
	Rc=ReconModule.Recon(N,R,Mode)
	Z=Rc.widths_to_z(np.diff([0,*Edges,1]))
	return Rc,Z


def normalized_properties():
	Cases=[(2,1,[.1,.5,.6,.8],'sup'),(1,4,[.55,.6746455700142735],'sup'),
		(2,4,[.08,.22,.63,.85],'inf'),(1,100,[.499,.501],'sup')]
	Random=np.random.default_rng(130710)
	for i in range(5):
		Widths=Random.dirichlet(np.full(5,2.0))
		Cases.append((2,float(Random.uniform(1,12)),np.cumsum(Widths)[:-1].tolist(),'sup' if i%2 else 'inf'))
	for Case,(N,R,Edges,Mode) in enumerate(Cases):
		Rc,Z=configuration(N,R,Edges,Mode)
		Data=Analytic.eigen_data(Rc,Z)
		Blocks=Rc.blocks_from_z(Z)
		IndependentBlocks=Ref.blocks_from_edges(Data['edges'],Rc.pat)
		Lambdas=Ref.roots(IndependentBlocks,N+1)
		for Index,Tag in [(N-1,'n'),(N,'np1')]:
			Expected=Ref.normalized(Lambdas[Index],IndependentBlocks,Data['edges'])
			Actual=np.column_stack([Data['u_'+Tag],Data['up_'+Tag]])
			close(f'mass-state-{Case}-{Tag}',Actual,Expected,3e-10)
			Frequency=np.sqrt(Data['lam_'+Tag])
			close(f'value-identity-{Case}-{Tag}',Actual[:,0],ReconModule.eigfun(Blocks,Frequency,Data['edges']),2e-14)
			Nodes,Weights=np.polynomial.legendre.leggauss(64)
			AllPoints=[]; AllWeights=[]; Start=0.
			for Length,Density in Blocks:
				AllPoints.extend(Start+Length*(Nodes+1)/2)
				AllWeights.extend(Density*Length*Weights/2)
				Start+=Length
			Values=ReconModule.eigfun(Blocks,Frequency,AllPoints)
			close(f'quadrature-unit-mass-{Case}-{Tag}',np.dot(AllWeights,Values**2),1,3e-12)
	# Closed trigonometric derivatives test the exact-node case without a ratio.
	Rc,Z=configuration(2,1,[.1,.5,.6,.8]); Data=Analytic.eigen_data(Rc,Z)
	for K,Tag in [(2,'n'),(3,'np1')]:
		close('R1-closed-values-'+Tag,Data['u_'+Tag],np.sqrt(2)*np.sin(K*np.pi*Data['edges']),2e-13)
		close('R1-closed-derivatives-'+Tag,Data['up_'+Tag],np.sqrt(2)*K*np.pi*np.cos(K*np.pi*Data['edges']),2e-12)
	# Linear/small-wave mass limits exercise the midpoint Gram expression.
	for Frequency in [0.,1e-12,1e-5]:
		Blocks=[(.2,1.),(.3,7.),(.5,2.)]
		Points=[1.,0.,.2,.77,.3,.2]
		Expected=Ref.normalized(Ref.mp.mpf(Frequency)**2,[(Ref.mp.mpf(L),Ref.mp.mpf(D)) for L,D in Blocks],Points)
		close('small-wave-mass-'+str(Frequency),ReconModule.eigenfunction_states(Blocks,Frequency,Points),Expected,3e-13)
	for Point in [-1e-9,1.00001,np.nan,np.inf]:
		rejects('eigen-point-'+str(Point),lambda:ReconModule.eigenfunction_states([(1,1)],1,[Point]))


def green_properties():
	Cases=[[(1.,1.)],[(.18,1.),(.31,7.),(.51,2.)],[(.1,1.),(.17,30.),(.23,3.)]]
	Random=np.random.default_rng(130809)
	for Case,Blocks in enumerate(Cases):
		Length=float(np.cumsum(np.array(Blocks)[:,0])[-1])
		Points=np.array([0.,Length,.16*Length,.77*Length,.3*Length,.16*Length])
		Independent=[(Ref.mp.mpf(L),Ref.mp.mpf(D)) for L,D in Blocks]
		# Exact binary64 cumulative endpoint can differ from high precision sum.
		for Mu in [-100.,-1.,-1e-16,0.,1e-16,.7]:
			for Boundary in ['D','N']:
				Actual=ReconModule.real_green_matrix(Blocks,Mu,Points,RightBoundary=Boundary)
				Expected=np.array([[float(Ref.green(Ref.mp.mpf(Mu),Independent,X,Y,Boundary)) for Y in Points] for X in Points])
				close(f'green-independent-{Case}-{Mu}-{Boundary}',Actual,Expected,2e-12)
				Permutation=Random.permutation(len(Points))
				Permuted=ReconModule.real_green_matrix(Blocks,Mu,Points[Permutation],RightBoundary=Boundary)
				close(f'green-permutation-{Case}-{Mu}-{Boundary}',Permuted,Actual[np.ix_(Permutation,Permutation)],0)
				close(f'green-symmetry-{Case}-{Mu}-{Boundary}',Actual,Actual.T,0)
				close(f'green-duplicate-{Case}-{Mu}-{Boundary}',Actual[2],Actual[5],0)
				close(f'green-left-end-{Case}-{Mu}-{Boundary}',Actual[0],np.zeros(len(Points)),0)
				if Boundary=='D':
					close(f'green-right-end-{Case}-{Mu}',Actual[1],np.zeros(len(Points)),1e-14)
					close(f'full-green-route-{Case}-{Mu}',Analytic.green_kernel(Blocks,Mu,Points),Actual,0)
				close(f'half-green-route-{Case}-{Mu}-{Boundary}',Half.green_regular(Blocks,Mu,Points[3],Points[2],Boundary),Actual[3,2],0)
				if Mu<=0:
					Interior=Actual[2:5,2:5]
					check(f'green-positive-{Case}-{Mu}-{Boundary}',np.min(np.linalg.eigvalsh(Interior))>0)
		for Mu in [-1.,0.,.7]:
			for Boundary in [None,'D','N']:
				State=ReconModule.solution_states(Blocks,Mu,Points,RightBoundary=Boundary)
				if Boundary is None:
					Expected=[Ref.physical(Ref.mp.mpf(Mu),Independent,Ref.mp.mpf(X)) for X in Points]
				else:
					Reversed=list(reversed(Independent)); ExactLength=sum(L for L,_ in Independent)
					Initial=(0,1) if Boundary=='D' else (1,0)
					Expected=[]
					for X in Points:
						Y,D=Ref.physical(Ref.mp.mpf(Mu),Reversed,ExactLength-Ref.mp.mpf(X),Initial)
						Expected.append([Ref.mp.re(Y),-Ref.mp.re(D)])
				close(f'physical-state-{Case}-{Mu}-{Boundary}',State,np.array(Expected,dtype=complex).real,2e-11)
	close('zero-DD',Half.green_regular([(.5,1)],0,.1,.2,'D'),.06,2e-16)
	close('zero-DN',Half.green_regular([(.5,1)],0,.1,.2,'N'),.1,2e-16)
	close('linear-prop-matrix',Analytic.prop_matrix([(.3,2),(.7,4)],0),[[1,1],[0,1]],0)
	close('uv-endpoints',Analytic.uv_at([(1,1)],0,[1,0,.5]),[[1,1],[0,1],[.5,1]],0)
	check('empty-green-shape',Analytic.green_kernel([(1,1)],0,[]).shape==(0,0))
	for Mu in [np.nan,np.inf,1j,'1',False]:
		rejects('full-mu-'+str(Mu),lambda:Analytic.green_kernel([(1,1)],Mu,[.2]))
		rejects('half-mu-'+str(Mu),lambda:Half.green_regular([(.5,1)],Mu,.1,.2,'N'))
	for Point in [-np.finfo(float).eps,1+np.finfo(float).eps,np.inf,np.nan,1j]:
		rejects('full-point-'+str(Point),lambda:Analytic.green_kernel([(1,1)],0,[Point]))
		rejects('half-point-'+str(Point),lambda:Half.green_regular([(.5,1)],0,Point,.2,'D'))
	for Boundary in ['X',None,False]:
		rejects('half-BC-'+str(Boundary),lambda:Half.green_regular([(.5,1)],0,.1,.2,Boundary))
	for Blocks in [[],[(0,1)],[(1,0)],[(1,-1)],[(np.inf,1)],[(1,1),(1e-20,1)]]:
		rejects('green-geometry-'+str(Blocks),lambda:Analytic.green_kernel(Blocks,0,[]))
	for Boundary,Mu in [('D',np.pi**2),('N',(np.pi/2)**2)]:
		rejects('closed-pole-'+Boundary,lambda:ReconModule.real_green_matrix([(1,1)],Mu,[0,.2,1],RightBoundary=Boundary))
	for Boundary in ['D','N']:
		for Mu in [0.,-1.,np.nan,np.inf]:
			rejects(f'reduced-positive-domain-{Boundary}-{Mu}',lambda:Half.green_regularized([(.5,1)],Mu,.1,.2,Boundary))
		rejects('hyperbolic-overflow-'+Boundary,lambda:Half.green_regular([(1,1)],-1e12,.1,.2,Boundary))
	# Kernel jump in first derivative and continuity at a physical density step.
	Blocks=[(.3,1),(.4,4),(.3,2)]; Mu=-2.; Y=.51; H=1e-6
	G=lambda X:Half.green_regular(Blocks,Mu,X,Y,'D')
	close('Green-derivative-jump',(G(Y+H)-G(Y))/H-(G(Y)-G(Y-H))/H,-1,1e-5)
	close('Green-interface-derivative',(G(.3+H)-G(.3))/H,(G(.3)-G(.3-H))/H,1e-5)
	# Finite sums at nonpositive mu retain the R12 bound-table path.
	for Boundary in ['D','N']:
		Table=Half.HalfSpectrum([(.5,1)],Boundary,640)
		for Mu in [0.,-1.]:
			Truth=Half.green_regular([(.5,1)],Mu,.1,.2,Boundary)
			Errors=[]
			for Count in [160,640]:
				Value=Half._spectral_full_green([(.5,1)],Mu,Boundary,.1,.2,Count,spectrum=Table)
				Errors.append(abs(Value-Truth))
			check(f'nonpositive-spectral-{Boundary}-{Mu}',Errors[1]<2e-7 and Errors[1]<Errors[0],Errors)


def jacobian_properties():
	Cases=[(1,4,[.25,.75],'sup'),(1,4,[.55,.6746455700142735],'sup'),
		(1,3,[.19,.66],'inf'),(2,4,[.12,.28,.61,.83],'sup'),(2,1,[.1,.5,.6,.8],'sup')]
	for Case,(N,R,Edges,Mode) in enumerate(Cases):
		Rc,Z=configuration(N,R,Edges,Mode)
		ActualEdges=np.cumsum(Rc.z_to_widths(Z))[:-1]
		Lambdas,F,Reference=Ref.implicit_jacobian(ActualEdges,Rc.pat,N)
		Truth=np.array(Reference.tolist(),float)
		Counts=[160,640,2560] if Case==0 else [240,960]
		Errors=[]
		for Count in Counts:
			Actual=Spectral.analytic_jacobian_spectral(Rc,Z,N=Count)
			Errors.append(float(np.max(abs(Actual-Truth))))
		check(f'nonstationary-high-precision-{Case}',Errors[-1]<.045 and (R==1 or Errors[-1]<Errors[0]*.35),dict(N=Counts,errors=Errors,reference=Truth.tolist()))
		Fd,Geometry=jac_fd(Rc,Z,h=2e-6,return_diagnostics=True)
		close(f'physical-FD-high-precision-{Case}',Fd,Truth,4e-6)
		check(f'physical-FD-geometry-{Case}',all(Row['max_motion_error']<=Row['geometry_error_budget'] for Row in Geometry['columns']))
		Count=160
		Direct=Analytic.analytic_jacobian(Rc,Z,N=Count)[0]
		Terms=Analytic.term_breakdown(Rc,Z,N=Count)
		ViaTerms=(np.diag(Terms['fprime'])+Terms['M1']+Terms['M2']+Terms['M3'])/Terms['eigen_data']['lam_np1']
		close(f'direct-entry-{Case}',Direct,Spectral.analytic_jacobian_spectral(Rc,Z,N=Count),0)
		close(f'direct-breakdown-{Case}',ViaTerms,Direct,0)
		Data=Terms['eigen_data']; A=Data['lam_n']; B=Data['lam_np1']; U=Data['u_n']
		RawF=A*U**2-B*Data['u_np1']**2
		Delta=(A*np.outer(RawF,U**2)+2*A*np.outer(U**2,RawF)-np.outer(RawF,RawF))*np.diff(Rc.pat)[None,:]/B**2
		close(f'correction-algebra-{Case}',Terms['correction']/B,Delta,5e-13)
		if Case==0:
			C,D=jacobian_cross_blocks(Direct,1)
			close('symmetric-nonstationary-cross-det',np.linalg.det(Direct),-np.linalg.det(C)*np.linalg.det(D),2e-13)
	# At an actual stationary configuration correction vanishes and old formula remains.
	Tab=json.loads((Root/'scripts/op03_gap_table.json').read_text())
	for N in [1,2]:
		for Mode in ['sup','inf']:
			Rc,Z=configuration(N,4,Tab[f'n{N}_{Mode.upper()}']['edges'],Mode)
			Z=symmetric_root(Rc,Z)
			check(f'stationary-found-{N}-{Mode}',Z is not None)
			Terms=Analytic.term_breakdown(Rc,Z,N=240); B=Terms['eigen_data']['lam_np1']
			close(f'stationary-correction-{N}-{Mode}',Terms['correction']/B,np.zeros((2*N,2*N)),3e-9)
			Direct,Fprime,Identity,_,_=Analytic.analytic_jacobian(Rc,Z,N=240)
			close(f'stationary-Wronskian-{N}-{Mode}',Fprime,Identity,1e-6)
			C,D=jacobian_cross_blocks(Direct,N)
			close(f'stationary-cross-det-{N}-{Mode}',np.linalg.det(Direct),(-1)**N*np.linalg.det(C)*np.linalg.det(D),1e-7)


try:
	normalized_properties()
	green_properties()
	jacobian_properties()
except Exception:
	print(json.dumps(dict(status='AUTHOR_TEST_FAILED',optimized=not __debug__,completed=len(Results),checks=Results),indent=2))
	traceback.print_exc()
	sys.exit(1)
print(json.dumps(dict(status='AUTHOR_TESTS_PASSED',optimized=not __debug__,count=len(Results),checks=Results,
	limits='Finite floating/high-precision evidence. No independent approval, certified tail bound or global theorem.'),indent=2))
