"""Round16 repaired properties on COMPLETE active modules; no assert acceptance.

Finite diagnostics and exact low-degree examples do not prove infinite tails
or the all-integer Riesz theorem. The original defect-confirming suite is kept
separately in input/, with its original expectations and failures unchanged.
"""
import argparse
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import importlib
import json
import math
import mpmath as mp
from pathlib import Path
import platform
import sys
import time
import numpy as np
import sympy as sp


ROWS = []


def check(Name, Condition, **Data):
	Passed = bool(Condition)
	ROWS.append({'name': Name, 'passed': Passed, **Data})
	if not Passed:
		raise RuntimeError(Name)


def rejects(Name, Fn, Types=(ValueError, TypeError, ArithmeticError)):
	try:
		Fn()
	except Types as Error:
		check(Name, True, error_type=type(Error).__name__, error=str(Error))
	else:
		check(Name, False)


def taylor_checks(T):
	FalseInt = lambda z: (z-z*z/2)/15-F(1, 2**62)*z
	FalseFloat = lambda z: (F(1)+F(3, 2**54))*z-z*z/2
	for Name, Fn, A, B, Count in (
		('integer', FalseInt, 0, 1, 3),
		('Fraction-integer', FalseInt, F(0), F(1), 3),
		('adjacent-float', FalseFloat, 1., math.nextafter(1., 2.), 1),
		('Fraction-adjacent', FalseFloat, F(1), F(math.nextafter(1., 2.)), 1)):
		check('Taylor rejects false '+Name, not T.der_sign2(Fn, A, B, True, base_n=Count, max_n=Count)[0])
		check('adaptive rejects false '+Name, not T.der_sign_adaptive(Fn, A, B, True, max_boxes=80)[0])
	for A, B in ((0, 1), (F(0), F(1)), (0., 1.)):
		check('honest strict polynomial '+str(type(A)), T.der_sign2(lambda z:z+z*z, A, B, True, base_n=3, max_n=3)[0])
		check('honest adaptive negative '+str(type(A)), T.der_sign_adaptive(lambda z:-z, A, B, False)[0])
	for Name, Fn in (('sin', T.d2_sin), ('cos', lambda z:-T.d2_cos(z)), ('atan', T.d2_atan)):
		check('rational transcendental '+Name, T.der_sign2(Fn, F(1, 3), F(1, 2), True, base_n=3, max_n=24)[0])
	for Value in (True, '0', Decimal('0'), complex(0), float('nan'), float('inf')):
		for Fn in (T.der_sign2, T.der_sign_adaptive):
			rejects('unsupported endpoint '+repr(Value)+' '+Fn.__name__, lambda Fn=Fn,Value=Value:Fn(lambda z:z, Value, 1, True))
	for A, B in ((1, 0), (0, 0)):
		for Fn in (T.der_sign2, T.der_sign_adaptive):
			rejects('invalid ordering '+str((A,B))+' '+Fn.__name__, lambda Fn=Fn,A=A,B=B:Fn(lambda z:z, A, B, True))
	for Value in (0, -1, True, 2.5, F(3,2)):
		rejects('invalid grid count '+str(Value), lambda Value=Value:T.der_sign2(lambda z:z,0,1,True,base_n=Value))
		rejects('invalid adaptive budget '+str(Value), lambda Value=Value:T.der_sign_adaptive(lambda z:z,0,1,True,max_boxes=Value))
	rejects('base beyond max', lambda:T.der_sign2(lambda z:z,0,1,True,base_n=4,max_n=3))
	for Value in (0, -1, 2, True, '0.1', float('inf')):
		rejects('invalid adaptive width '+repr(Value), lambda Value=Value:T.der_sign_adaptive(lambda z:z,0,1,True,min_w=Value))
	Calls = []
	def BudgetFn(z):
		Calls.append(z)
		return z*z
	check('budget ends before evaluating another box', not T.der_sign_adaptive(BudgetFn,-1,1,True,max_boxes=1)[0] and len(Calls)==2, evaluations=len(Calls))
	Pieces = []
	def ExactFn(z):
		Pieces.append((z.v.lo,z.v.hi))
		return z
	check('exact nonbinary partition positivity', T.der_sign2(ExactFn,0,1,True,base_n=3,max_n=3)[0])
	check('exact partition complete and adjacent', Pieces[0]==(F(0),F(1,3)) and Pieces[2]==(F(1,3),F(2,3)) and Pieces[4]==(F(2,3),F(1)))
	check('all partition coordinates Fraction', all(isinstance(v,F) for p in Pieces for v in p))
	Seen = []
	def FloatFn(z):
		Seen.append((z.v.lo,z.v.hi));return z
	check('adjacent floats retain whole real interval', T.der_sign2(FloatFn,1.,math.nextafter(1.,2.),True,base_n=1,max_n=1)[0] and Seen[0]==(F(1),F(math.nextafter(1.,2.))))
	rejects('unsupported callback result', lambda:T.der_sign2(lambda z:1,0,1,True))


def pairing_checks(V, Physical):
	for Order in (32,64,128):
		for Blocks in ([(1.,2.)],[(.5,2.)]*2,[(.25,2.)]*4):
			P = V.SpectralProbe(Blocks,61,Order)
			Lam,C,W,D,Info = P.pairings(V.block_direction([2.]*len(Blocks),P.edges),return_diagnostics=True)
			check('analytic constant identity '+str((Order,len(Blocks))), np.max(np.abs(C-np.eye(61)))<2e-12, error=float(np.max(np.abs(C-np.eye(61)))))
			for n in (2,20,60):
				Q = V.q_formula(Lam,C,W,n,D); Exact=(2*n+1)*math.pi**2/2
				check('correct Q '+str((Order,len(Blocks),n)), abs(Q-Exact)<2e-7, Q=Q, exact=Exact)
			check('analytic diagnostic finite-not-certified '+str((Order,len(Blocks))), Info['quadrature_error']==0 and Info['roundoff_enclosure'] is None and not Info['sign_certified'])
	P = V.SpectralProbe([(1.,2.)],61,32)
	rejects('callback insufficient phase/budget rejected',lambda:P.pairings(lambda x:2*np.ones_like(x),MaxOrder=64))
	check('unresolved callback explicit status',P.last_pairing_diagnostics['status']=='UNRESOLVED')
	Lam,C,W,D,Info = P.pairings(lambda x:2*np.ones_like(x),return_diagnostics=True)
	check('resolved callback constant Q',abs(V.q_formula(Lam,C,W,20,D)-41*math.pi**2/2)<2e-7)
	check('callback records error and no enclosure', Info['status']=='CONVERGED_NUMERICAL_ESTIMATE' and len(Info['estimated_absolute_errors'])==4 and Info['black_box_error_enclosure'] is None)
	rejects('direct retained high-mode underresolution', lambda:P.quadrature())
	for Exponent in (40,50):
		Delta=2.**(-Exponent); Blocks=[(.5,1.),(Delta,1.),(.5-Delta,1.)]
		for Order in (64,128):
			P=V.SpectralProbe(Blocks,3,Order); Direction=V.block_direction([0,1/Delta,0],P.edges)
			_,C,_,_,Info=P.pairings(Direction,return_diagnostics=True)
			check('thin analytic pairing '+str((Exponent,Order)),abs(C[0,0]-2)<2e-12, pairing=float(C[0,0]))
			check('thin exact direction mass '+str((Exponent,Order)),F(float(Direction.coefficients[1]))*(F(float(Direction.edges[2]))-F(float(Direction.edges[1])))==1)
			check('thin common normalization unchanged '+str((Exponent,Order)),Info['modal_Gram_error']<2e-12)
			if Exponent==50:
				for Callback in (lambda:V.quadrature_rule(Blocks,Order),lambda:P.pairings(lambda x:Direction(x))):
					rejects('folded ordinary nodes reject '+str(Order),Callback)
			else:
				Points,Weights,Knots=V.quadrature_rule(Blocks,Order)
				check('resolved ordinary cell '+str(Order),len(np.unique(Points))==len(Points) and abs(Weights@Direction(Points)-1)<2e-12)
	P=V.SpectralProbe([(1.,1.)],4,64)
	DefaultResult=P.pairings(V.block_direction([1.],[0.,1.]))
	check('default compatible result carries diagnostics',len(DefaultResult)==4 and DefaultResult.diagnostics['sign_certified'] is False)
	Direction=V.block_direction([2.,-1.],[0.,.2,1.])
	_,C,W,_,Info=P.pairings(Direction,return_diagnostics=True)
	_,Cq,Wq,_,_=P.pairings(lambda x:Direction(x),(.2,),return_diagnostics=True)
	check('direction-only breakpoint analytic vs resolved callback',np.max(np.abs(C-Cq))<2e-11 and np.max(np.abs(W-Wq))<2e-11)
	check('all direction cuts included',Info['intervals']==2)
	# The density has no cut here. A one-ulp DIRECTION cell still needs its
	# own left anchor; compare the same binary-frequency IVP, not an exact
	# DD eigenvalue or a certified sign at a near-nodal floating coefficient.
	Left=.5;Right=math.nextafter(Left,1.);Delta=Right-Left
	_,C,_,_,_=P.pairings(V.block_direction([0.,1/Delta,0.],[0.,Left,Right,1.]),return_diagnostics=True)
	with mp.workdps(90):
		Waves=[mp.mpf(float(w)) for w in P.roots]
		Mass=[mp.quad(lambda x,w=w:(mp.sin(w*x)/w)**2,[0,1]) for w in Waves]
		def Reference(i,j):
			return float(mp.quad(lambda x:mp.sin(Waves[i]*x)*mp.sin(Waves[j]*x)/(Waves[i]*Waves[j]*mp.sqrt(Mass[i]*Mass[j])),[mp.mpf(Left),mp.mpf(Right)])/mp.mpf(Delta))
		Cross,Square=Reference(0,1),Reference(1,1)
	check('direction-only one-ulp cell retains half-width cross',abs(C[0,1]-Cross)<3e-30,actual=float(C[0,1]),same_IVP_reference=Cross)
	check('direction-only one-ulp nodal square stable',abs(C[1,1]/Square-1)<2e-12,actual=float(C[1,1]),same_IVP_reference=Square)
	# A binary-rounded 1/3 anchor and an interior node of a nonconstant
	# density also require accurate phase propagation before local centering.
	for Blocks,Left,Index in (([(1.,1.)],float(1/3),2),
		([(.25,1.),(.5,4.),(.25,1.)],.5,1), ([(1.,2.)],float(1/3),2)):
		Pn=V.SpectralProbe(Blocks,6,8);Right=math.nextafter(Left,1.);Delta=Right-Left
		_,Cn,_,_=Pn.pairings(V.block_direction([0.,1/Delta,0.],[0.,Left,Right,1.]))
		with mp.workdps(100):
			Functions=[]
			for RootFrequency in Pn.roots:
				Frequency=mp.mpf(float(RootFrequency));Parts=[];Start=mp.mpf(0);U=mp.mpf(0);D=mp.mpf(1);Mass=mp.mpf(0)
				for Length,Density in Blocks:
					Width,Rho=mp.mpf(Length),mp.mpf(Density);Wave=Frequency*mp.sqrt(Rho)
					A,B=U,D/Wave;Parts.append((Start,Wave,A,B))
					Mass+=Rho*mp.quad(lambda x:A*A*mp.cos(Wave*x)**2+2*A*B*mp.cos(Wave*x)*mp.sin(Wave*x)+B*B*mp.sin(Wave*x)**2,[0,Width])
					U,D=A*mp.cos(Wave*Width)+B*mp.sin(Wave*Width),Wave*(-A*mp.sin(Wave*Width)+B*mp.cos(Wave*Width))
					Start+=Width
				def Sample(Point,Parts=Parts,Mass=Mass):
					Start,Wave,A,B=next(Part for Part in reversed(Parts) if Part[0]<=Point)
					return (A*mp.cos(Wave*(Point-Start))+B*mp.sin(Wave*(Point-Start)))/mp.sqrt(Mass)
				Functions.append(Sample)
			Cross=float(mp.quad(lambda t:Functions[0](mp.mpf(Left)+mp.mpf(Delta)*t)*Functions[Index](mp.mpf(Left)+mp.mpf(Delta)*t),[0,1]))
			Square=float(mp.quad(lambda t:Functions[Index](mp.mpf(Left)+mp.mpf(Delta)*t)**2,[0,1]))
		check('near-node phase cross '+str((Blocks,Left,Index)),abs(Cn[0,Index]-Cross)<3e-29,actual=float(Cn[0,Index]),same_IVP_reference=Cross)
		check('near-node phase square '+str((Blocks,Left,Index)),abs(Cn[Index,Index]/Square-1)<2e-12,actual=float(Cn[Index,Index]),same_IVP_reference=Square)
	Anchors=P._analytic_anchor_states(np.array([0.,.5]))
	Scales=np.array([Physical.eigenfunction_states(P.blocks,Root,[0.])[0,1] for Root in P.roots])
	check('analytic anchors retain existing common mass',np.array_equal(Anchors[:,0,1],Scales))
	rejects('positive local integral underflow refused',lambda:V._cos_sin_integrals(np.array([1.]),2.**-400))
	for Waves,Length in ((np.array([1e-9,1.,10.]),.75),(np.array([1.,2.,3.]),1e-10)):
		Cosine,Sine=V._cos_sin_integrals(Waves,Length)
		with mp.workdps(80):
			for i in range(3):
				for j in range(i,3):
					Wi,Wj,L=mp.mpf(float(Waves[i])),mp.mpf(float(Waves[j])),mp.mpf(Length)
					Exact=mp.quad(lambda x:mp.sin(Wi*x)*mp.sin(Wj*x)/(Wi*Wj),[-L/2,L/2])
					check('small/unequal phase sine integral '+str((float(Length),i,j)),abs(mp.mpf(float(Sine[i,j]))-Exact)<mp.mpf('2e-14')*abs(Exact))
	Zeros=V.block_direction([0.],[0.,1.]);_,C,W,D,Info=P.pairings(Zeros,return_diagnostics=True)
	check('zero direction no invented tail',np.all(C==0) and np.all(D==0) and Info['parseval_remainder_raw']==[0.]*4 and not Info['sign_certified'])
	rejects('direction domain mismatch',lambda:P.pairings(V.block_direction([1.],[0.,2.])))
	for Coeff,Edges in (([1.],[0.,0.]),([1.,2.],[0.,1.]),([float('nan')],[0.,1.])):
		rejects('invalid structured direction '+str((Coeff,Edges)),lambda Coeff=Coeff,Edges=Edges:V.block_direction(Coeff,Edges))
	for Bad in ((0.,), (1.,), (float('nan'),), 1.):
		rejects('invalid extra cuts '+str(Bad),lambda Bad=Bad:P.pairings(Zeros,Bad))
	for n in (2,):
		for Mode in ('sup','inf'):
			Rc,Z,Blocks,_=V.build_case(n,4.,Mode)
			P=V.SpectralProbe(Blocks,12,64)
			_,C,_,_,Info=P.pairings(V.block_direction([1.]*len(Blocks),P.edges),return_diagnostics=True)
			check('normal R4 '+Mode+' common mass and balance',Rc.stationarity_diagnostics(Z)['accepted'] and Info['modal_Gram_error']<2e-10 and np.all(np.isfinite(C)), diagnostics=Rc.stationarity_diagnostics(Z))


def integer_examples():
	x=sp.Symbol('x'); c=sp.Symbol('c',positive=True)
	def Integral(Poly):
		Result=sp.integrate(Poly,x);return sp.expand(Result-Result.subs(x,-1))
	for r in range(1,7):
		Matrix=sp.Matrix([[sp.diff(x**k,x,j).subs(x,Side) for k in range(2*r)] for Side in (-1,1) for j in range(r)])
		Free=[(j,Side) for j in range(0,r,2) for Side in (-1,1)]
		Lifts=[]
		for Target in Free:
			Data=[]
			for Side in (-1,1):
				for j in range(r):
					Data.append(sp.Integer((j,Side)==Target) if j%2==0 else (sp.Integer((j-1,1)==Target)-sp.Integer((j-1,-1)==Target))/2)
			Coefficients=Matrix.inv()*sp.Matrix(Data)
			Lifts.append(sp.expand(sum(Coefficients[k]*x**k for k in range(2*r))))
		Jet=sp.Matrix([[sp.diff(P,x,j).subs(x,Side) for P in Lifts] for j,Side in Free])
		check('integer Hermite identity r'+str(r),Jet==sp.eye(2*math.ceil(r/2)))
		for n in range(r,r+3):
			P=sp.legendre(n,x)
			for _ in range(r):P=Integral(P)
			check('integer clamped high column '+str((r,n)),all(sp.diff(P,x,j).subs(x,Side)==0 for j in range(r) for Side in (-1,1)) and sp.expand(sp.diff(P,x,r)-sp.legendre(n,x))==0)
			Lifts.append(P)
		N=2*r+2; Coeff=sp.Matrix([[sp.expand(P).coeff(x,k) for P in Lifts] for k in range(N+1)])
		check('integer finite exact span r'+str(r),Coeff.rank()==N+1-2*(r//2))
	n=sp.Symbol('n',integer=True,positive=True); b=(n+1)**2*sp.pi**2/2; d=(n+2)**2*sp.pi**2/2
	check('tail lower equality exact symbolic',sp.simplify(-b*b/(4*(d-b))+sp.pi**2*(n+1)**4/(8*(2*n+3)))==0)
	check('rate negative-t counterexample preserved',F(47,45)>F(3,4))


def main():
	Parser=argparse.ArgumentParser();Parser.add_argument('--root',type=Path,required=True);Parser.add_argument('--output',type=Path,required=True);Args=Parser.parse_args()
	Root=Args.root.resolve();sys.path.insert(0,str(Root/'scripts'));sys.path.insert(0,str(Root/'misc'))
	T=importlib.import_module('rigid1d');V=importlib.import_module('_gapn2_second_variation_probe');Physical=importlib.import_module('_gapn2_symmetry_recon')
	Start=time.monotonic();Error=None
	try:
		taylor_checks(T);pairing_checks(V,Physical);integer_examples()
	except Exception as Exc:
		Error=repr(Exc)
	finally:
		Paths=[Path(T.__file__),Path(V.__file__),Path(Physical.__file__),Root/'scripts/_sl_prufer.py',Root/'scripts/op03_gap_fixed.py']
		Result={'meaning':'repaired finite software properties and finite exact examples; no all-integer or interval certification', 'all_passed':Error is None and all(R['passed'] for R in ROWS),'count':len(ROWS),'checks':ROWS,'error':Error,'elapsed_seconds':time.monotonic()-Start,'environment':{'python':sys.version,'optimize':sys.flags.optimize,'numpy':np.__version__,'sympy':sp.__version__,'platform':platform.platform()},'sources':{str(P):hashlib.sha256(P.read_bytes()).hexdigest() for P in Paths}}
		Args.output.parent.mkdir(parents=True,exist_ok=True);Args.output.write_text(json.dumps(Result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
	print('PASS' if Result['all_passed'] else 'FAIL',Result['count'],'properties',Error or '')
	if Error:
		raise RuntimeError(Error)


if __name__=='__main__':
	main()
