from pathlib import Path
import json
import sympy as S

Out = Path(__file__).resolve().parent / 'coordinator-checks'
Out.mkdir(exist_ok=True)
Rows = []

def record(Name, Kind, Condition, Detail=''):
	Passed = bool(Condition)
	Rows.append(dict(name=Name, kind=Kind, passed=Passed, detail=Detail))
	print(('PASS ' if Passed else 'FAIL ') + Name, flush=True)
	if not Passed:
		raise ArithmeticError(Name)

x = S.symbols('x', real=True)
a = S.symbols('a', positive=True)
k = S.symbols('k', integer=True, nonnegative=True)
g0 = S.cosh(a*(1-x))/(2*a*S.sinh(a))
D = a*S.cosh(a)-S.sinh(a)
g1 = (a*S.cosh(a*(1-x))-S.sinh(a*(1-x)))/(2*D)
record('g1 denominator derivative and zero base', 'symbolic identity', S.simplify(S.diff(D,a)-a*S.sinh(a))==0 and D.subs(a,0)==0, 'D positive for a>0 follows analytically from its derivative.')
for Name, g in [('g0',g0),('g1',g1)]:
	record(Name+' positive-half homogeneous ODE', 'symbolic identity', S.simplify(-S.diff(g,x,2)+a*a*g)==0)
record('g0 zero endpoint derivative', 'symbolic identity', S.diff(g0,x).subs(x,1)==0)
record('g0 derivative jump is minus one', 'symbolic identity', S.simplify(2*S.diff(g0,x).subs(x,0)+1)==0)
record('g1 value jump is one', 'symbolic identity', S.simplify(2*g1.subs(x,0)-1)==0)
record('g1 endpoint derivative equals endpoint value', 'symbolic identity', S.simplify((S.diff(g1,x)-g1).subs(x,1))==0)
fL,fR,f0,df0 = S.symbols('fL fR f0 df0')
Slope = (fR-fL)/2
Boundary0 = -Slope*g0.subs(x,1)+Slope*g0.subs(x,1)-2*S.diff(g0,x).subs(x,0)*f0
Boundary1 = -2*Slope*g1.subs(x,1)+(fR-fL)*S.diff(g1,x).subs(x,1)+2*g1.subs(x,0)*df0
record('even Green integration interface gives evaluation', 'symbolic boundary identity', S.simplify(Boundary0-f0)==0, 'Piecewise integration by parts for H2 functions is analytic, not inferred from this algebra.')
record('odd Green integration interface gives derivative', 'symbolic boundary identity', S.simplify(Boundary1-df0)==0)
record('nonzero even kernel integral equals 1/c', 'symbolic integral', S.simplify(2*S.integrate(g0,(x,0,1))-1/a**2)==0)
record('odd kernel first moment equals 1/c', 'symbolic integral', S.simplify(2*S.integrate(x*g1,(x,0,1))-1/a**2)==0)

def boundary(P):
	Delta = (P.subs(x,1)-P.subs(x,-1))/2
	return S.Matrix([S.diff(P,x).subs(x,1)-Delta,S.diff(P,x).subs(x,-1)-Delta])

m = k+2
Even = x**(2*m)-m/(m-1)*x**(2*m-2)
Odd = x**(2*m+1)-m/(m-1)*x**(2*m-1)
DiffEven = 2*m*x**(2*m-1)-m/(m-1)*(2*m-2)*x**(2*m-3)
DiffOdd = (2*m+1)*x**(2*m)-m/(m-1)*(2*m-1)*x**(2*m-2)
for Name,P,Dp in [('even',Even,DiffEven),('odd',Odd,DiffOdd)]:
	record(Name+' polynomial power-rule derivative', 'symbolic identity', S.simplify(S.diff(P,x)-Dp)==0)
	record(Name+' sparse polynomial has both zero central traces', 'symbolic arbitrary-index identity', S.simplify(P.subs(x,0))==0 and S.simplify(Dp.subs(x,0))==0, 'm=k+2 with k a nonnegative integer; explicit nonnegative polynomial powers avoid the CAS removable 1/x representation')
	record(Name+' sparse polynomial satisfies Krein boundary equations', 'symbolic arbitrary-index identity', boundary(P).applyfunc(S.simplify)==S.zeros(2,1))
L = 2*(k+1)
Mat = S.Matrix.hstack(boundary(x**L),boundary(x**(L+1))).applyfunc(S.simplify)
record('all even tail orders have stated endpoint matrix', 'symbolic arbitrary-index identity', Mat==S.Matrix([[L,L],[-L,L]]), 'L=2(k+1)>0')
record('endpoint correction matrix determinant', 'symbolic identity', S.simplify(Mat.det()-2*L**2)==0)
rPlus,rMinus = S.symbols('rPlus rMinus')
Correction = S.Matrix([(rPlus-rMinus)/(2*L),(rPlus+rMinus)/(2*L)])
record('endpoint correction inverse', 'symbolic identity', (Mat*Correction-S.Matrix([rPlus,rMinus])).applyfunc(S.simplify)==S.zeros(2,1))
record('old odd norm equality is false', 'exact counterexample', S.integrate(x*x,(x,-1,1))==S.Rational(2,3) and S.integrate(S.sqrt(x),(x,0,1))/2==S.Rational(1,3))
record('correct odd norm equality holds for x', 'exact example', S.integrate(x*x,(x,-1,1))==S.integrate(S.sqrt(x),(x,0,1)))
record('oblique retained subspace contains 1+x with nonzero traces', 'exact counterexample', boundary(1+x)==S.zeros(2,1) and (1+x).subs(x,0)==S.diff(1+x,x).subs(x,0)==1)
record('oblique retained subspace excludes both low basis members', 'exact counterexample', S.S.One.subs(x,0)!=S.diff(S.S.One,x).subs(x,0) and x.subs(x,0)!=S.diff(x,x).subs(x,0))

Result = {'status':'PASS','checks':Rows,'named_checks':len(Rows),'limits':'Exact algebra, symbolic identities and explicit counterexamples. Sobolev cutoff, all-cofinite closure and Green integration for arbitrary H2 functions require the separately reviewed analytic proof.'}
(Out/'results.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print('PASS',len(Rows),'scoped checks')
