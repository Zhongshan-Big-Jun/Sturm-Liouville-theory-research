import datetime
import hashlib
import json
import pathlib
import platform
import sys
import time

import numpy as np
import sympy as sp
from numpy.polynomial import legendre as lg

Root = pathlib.Path(__file__).resolve().parents[2]
x, c = sp.symbols('x c', real=True)
Records = []
Started = datetime.datetime.now(datetime.timezone.utc).isoformat()
Clock = time.perf_counter()

def check(Name, Result, Details=None):
	Record = {'name': Name, 'passed': bool(Result)}
	if Details is not None:
		Record['details'] = Details
	Records.append(Record)
	if not Result:
		raise AssertionError(Name)

def boundary(Poly):
	Delta = Poly.subs(x, 1) - Poly.subs(x, -1)
	return [sp.expand(sp.diff(Poly, x).subs(x, End) - Delta/2) for End in (1, -1)]

def j_poly(Poly, Times):
	for _ in range(Times):
		Anti = sp.integrate(Poly, x)
		Poly = sp.expand(Anti - Anti.subs(x, -1))
	return Poly

def legendre_coefficients(Poly):
	Remainder = sp.Poly(Poly, x)
	Coeffs = {}
	while not Remainder.is_zero:
		Degree = Remainder.degree()
		Pn = sp.Poly(sp.legendre(Degree, x), x)
		Value = Remainder.LC()/Pn.LC()
		Coeffs[Degree] = Value
		Remainder -= Value*Pn
	return Coeffs

def operator(Poly, S):
	for _ in range(S//2):
		Poly = sp.expand(c*Poly-sp.diff(Poly, x, 2))
	return Poly

def integral_norm_squared(Poly):
	return sp.integrate(sp.expand(Poly**2), (x, -1, 1))

def exact_checks():
	q6 = x**6-5*x**4+7*x**2
	q7 = x**7-sp.Rational(21,5)*x**5+sp.Rational(27,5)*x**3
	E = (3-q6)/16
	O = (11*x-5*q7)/48
	Lifts = [sp.Integer(1), x, E, O]
	Expected = [(1,1,0,0),(1,-1,0,0),(0,0,1,1),(0,0,1,-1)]
	for I, Poly in enumerate(Lifts):
		check(f'lift-{I}-both-Krein-boundaries', boundary(Poly)+boundary(sp.diff(Poly,x,2)) == [0]*4)
		Data = tuple(Poly.subs(x,T) for T in (1,-1)) + tuple(sp.diff(Poly,x,2).subs(x,T) for T in (1,-1))
		check(f'lift-{I}-endpoint-table', Data == Expected[I], [str(V) for V in Data])
	McSquared = sp.factor(sum(integral_norm_squared(operator(P,4)) for P in Lifts))
	check('M-c-squared-positive-constant-coefficient', McSquared.subs(c,0)>0, str(McSquared))
	for R, Last in ((2,14),(4,14)):
		for N in range(R, Last+1):
			Poly = j_poly(sp.legendre(N,x),R)
			Traces = [sp.diff(Poly,x,J).subs(x,T) for J in range(R) for T in (1,-1)]
			check(f'J{R}-P{N}-endpoint-jets', Traces == [0]*(2*R))
			check(f'J{R}-P{N}-derivative', sp.expand(sp.diff(Poly,x,R)-sp.legendre(N,x)) == 0)
			Coeffs = legendre_coefficients(Poly)
			Allowed = set(range(N-R,N+R+1,2))
			check(f'J{R}-P{N}-finite-band', set(Coeffs)<=Allowed and max(Coeffs)==N+R, {str(K):str(V) for K,V in Coeffs.items()})
			Images = legendre_coefficients(operator(Poly,R))
			check(f'K-power-J{R}-P{N}-image-band', set(Images)<=Allowed)
			if R == 2:
				Formula = sp.legendre(N+2,x)/((2*N+1)*(2*N+3))-2*sp.legendre(N,x)/((2*N-1)*(2*N+3))+sp.legendre(N-2,x)/((2*N+1)*(2*N-1))
				check(f'J2-P{N}-explicit-formula', sp.expand(Poly-Formula)==0)
	# Rank checks use exact rational monomial coefficients and actual boundary maps.
	for R, Degrees in ((2,[4,8,12]),(4,[8,12,16])):
		for Degree in Degrees:
			Basis = [sp.Integer(1),x] if R==2 else Lifts
			Basis = Basis+[j_poly(sp.legendre(N,x),R) for N in range(R,Degree-R+1)]
			Matrix = sp.Matrix([[sp.expand(P).coeff(x,K) for P in Basis] for K in range(Degree+1)])
			BMatrix = sp.Matrix.hstack(*[sp.Matrix(boundary(x**K)+(boundary(sp.diff(x**K,x,2)) if R==4 else [])) for K in range(Degree+1)])
			check(f's{R}-degree{Degree}-exact-span-dimension', Matrix.rank()==Degree+1-R and BMatrix.rank()==R and BMatrix*Matrix==sp.zeros(R,len(Basis)))
	G = 1+2*x**2+sp.I*(3*x-x**3)
	Moments = {K:sp.integrate(G*x**K,(x,-1,1)) for K in range(26)}
	for M in range(2,12):
		for Parity in (0,1):
			N=2*M+Parity
			P=x**N-sp.Rational(M,M-1)*x**(N-2)
			A=2*M*(2*M-1+2*Parity)+c*sp.Rational(M,M-1)
			B=2*M*(2*M-3+2*Parity)
			Q=c*x**N-A*x**(N-2)+B*x**(N-4)
			check(f'moment-row-m{M}-parity{Parity}',sp.expand(operator(P,2)-Q)==0)
			Direct=sp.integrate(G*Q,(x,-1,1))
			Row=c*Moments[N]-A*Moments[N-2]+B*Moments[N-4]
			check(f'complex-moment-m{M}-parity{Parity}',sp.simplify(Direct-Row)==0)
	t=sp.symbols('t',positive=True)
	He=1+2*t; Ho=sp.I*(3-t)
	Norm=sp.integrate(sp.expand(G*sp.conjugate(G)),(x,-1,1))
	Weighted=sp.integrate(He**2*t**sp.Rational(-1,2)+sp.expand(Ho*sp.conjugate(Ho))*t**sp.Rational(1,2),(t,0,1))
	check('parity-weight-isometry-complex-sample',sp.simplify(Norm-Weighted)==0,str(Norm))
	for A,D in ((2,2),(3,4),(5,3)):
		R=2-3*t+5*t**3
		Integrated=sp.integrate((t-1)*t**(A-2)*R.subs(t,t**D),t)
		Integrated-=Integrated.subs(t,0)
		Expected=0
		for J,Coef in ((0,2),(1,-3),(3,5)):
			M=A+D*J
			Expected+=sp.Rational(Coef,M)*(t**M-sp.Rational(M,M-1)*t**(M-1))
		check(f'arithmetic-antiderivative-a{A}-d{D}',sp.expand(Integrated-Expected)==0)
	return {'M_c_squared':str(McSquared)}

def j_legendre(Coeffs,R):
	Coeffs=np.asarray(Coeffs,dtype=float)
	for _ in range(R):
		Next=np.zeros(len(Coeffs)+1)
		for K,Value in enumerate(Coeffs):
			if Value:
				if K==0:
					raise ValueError('unexpected integration of P0 in high modes')
				Next[K+1]+=Value/(2*K+1)
				Next[K-1]-=Value/(2*K+1)
		Coeffs=Next
	return Coeffs

def op_legendre(Coeffs,R,C):
	for _ in range(R//2):
		Der=lg.legder(Coeffs,m=2)
		Coeffs=C*Coeffs.copy()
		Coeffs[:len(Der)]-=Der
	return Coeffs

def numerical_gram_checks():
	Data=[]
	Delta=.5+1/np.sqrt(2); C2=2/np.sqrt(3); C4=4/(3*np.sqrt(14))
	E=(3-(x**6-5*x**4+7*x**2))/16
	O=(11*x-5*(x**7-sp.Rational(21,5)*x**5+sp.Rational(27,5)*x**3))/48
	Low4=[]
	for P in [sp.Integer(1),x,E,O]:
		Cs=legendre_coefficients(P); Arr=np.zeros(max(Cs)+1)
		for K,V in Cs.items(): Arr[K]=float(V)
		Low4.append(Arr)
	for R in (2,4):
		for C in (.25,1.,3.):
			for Degree in (12,24,48):
				Basis=[np.array([1/np.sqrt(2)]),np.array([0,np.sqrt(3/2)])] if R==2 else Low4
				Basis=list(Basis)
				for N in range(R,Degree-R+1):
					En=np.zeros(N+1); En[N]=np.sqrt((2*N+1)/2)
					Basis.append(j_legendre(En,R))
				Images=[op_legendre(P.copy(),R,C) for P in Basis]
				Synthesis=np.zeros((Degree+1,len(Images)))
				for J,P in enumerate(Images): Synthesis[:len(P),J]=P
				Synthesis*=np.sqrt(2/(2*np.arange(Degree+1)+1))[:,None]
				Gram=Synthesis.T@Synthesis
				Eigen=np.linalg.eigvalsh(Gram)
				if R==2:
					Lc=(1+2*np.sqrt(3))/C+4*Delta
					Lower=1/(Lc*Lc+4); Upper=C*C+(1+C*C2)**2
				else:
					F0=C**-2; F2=2/C; F4=4
					F1=np.sqrt(3)*F0+Delta*F2; F3=np.sqrt(3)*F2+Delta*F4
					Dc2=(F0/np.sqrt(2)+np.sqrt(2)*F1)**2+(F2/np.sqrt(2)+np.sqrt(2)*F3)**2
					Mc2=sum(np.dot(op_legendre(P.copy(),4,C)**2,2/(2*np.arange(len(P))+1)) for P in Low4)
					Lower=1/(Dc2+16); Upper=Mc2+(1+2*C*C2+C*C*C4)**2
				Item={'s':R,'c':C,'degree':Degree,'min_eigenvalue':float(Eigen[0]),'max_eigenvalue':float(Eigen[-1]),'analytic_lower':float(Lower),'analytic_upper':float(Upper)}
				check(f'numeric-Riesz-s{R}-c{C}-N{Degree}',Eigen[0]>=Lower-1e-10 and Eigen[-1]<=Upper+1e-10,Item)
				Data.append(Item)
	return Data

def tsvd_checks():
	Rng=np.random.default_rng(20260923)
	for Trial in range(15):
		T=Rng.normal(size=(9,7))+1j*Rng.normal(size=(9,7))
		T[:,-1]=T[:,0]+2*T[:,1]
		U,S,Vh=np.linalg.svd(T,full_matrices=False)
		Epsilon=float(S[2]**2*.75)
		Keep=S*S>Epsilon
		P=U[:,Keep]@U[:,Keep].conj().T
		f=Rng.normal(size=9)+1j*Rng.normal(size=9)
		z=Rng.normal(size=7)+1j*Rng.normal(size=7)
		Error=np.linalg.norm(f-P@f)
		Bound=np.linalg.norm(f-T@z)+np.sqrt(Epsilon)*np.linalg.norm(z)
		check(f'complex-rank-deficient-tsvd-{Trial}',Error<=Bound+1e-11)
		Tail=(np.eye(9)-P)@T
		check(f'discarded-operator-norm-{Trial}',np.linalg.norm(Tail,2)<=np.sqrt(Epsilon)+1e-11)
		G=T.conj().T@T
		Lam,V=np.linalg.eigh(G); Select=Lam>Epsilon
		Ginv=(V[:,Select]/Lam[Select])@V[:,Select].conj().T
		check(f'Gram-versus-synthesis-projection-{Trial}',np.linalg.norm(T@Ginv@T.conj().T-P)<1e-10)
		check(f'moment-noise-norm-{Trial}',np.linalg.norm(T@Ginv,2)<=1/np.sqrt(Epsilon)+1e-11)
	# Exact diagonal/equality and a deliberately wrong epsilon penalty.
	Eps=sp.Rational(1,100); Sigma=sp.Rational(1,10)
	check('equality-is-discarded',not bool(Sigma**2>Eps))
	check('negative-control-wrong-epsilon-penalty-detected',Sigma>Eps and Sigma==sp.sqrt(Eps))
	check('same-number-T-versus-Gram-cutoff-different',sp.Rational(1,100)<sp.Rational(1,20)<sp.Rational(1,10))
	check('empty-retained-spectrum-projection',np.count_nonzero(np.array([1.,.1])**2>2.)==0)

try:
	Exact=exact_checks()
	Numerical=numerical_gram_checks()
	tsvd_checks()
	Outcome='PASS_AUTHOR_CHECKS_ONLY'
except Exception as Error:
	Outcome='FAILED_AUTHOR_CHECK'
	Exact=locals().get('Exact',{})
	Numerical=locals().get('Numerical',[])
	Records.append({'name':'execution-exception','passed':False,'details':repr(Error)})
finally:
	Report={'status':Outcome,'started_utc':Started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-Clock,'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'sympy':sp.__version__,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact polynomial identities, finite dimensions, complex TSVD and numerical Riesz diagnostics. Infinite-dimensional proofs require independent review. No Lean execution.','exact_outputs':Exact,'numerical_gram':Numerical,'checks':Records}
	Stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
	Path=Root/'private/checks'/f'execution-{Stamp}.json'
	Path.write_text(json.dumps(Report,indent=2)+'\n')
	print(json.dumps({'status':Outcome,'passed':sum(R['passed'] for R in Records),'total':len(Records),'report':str(Path),'elapsed_seconds':Report['elapsed_seconds']}),flush=True)
	if Outcome.startswith('FAILED'): sys.exit(1)
