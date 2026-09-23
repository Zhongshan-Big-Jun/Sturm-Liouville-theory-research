"""Exact finite algebra only. No Sobolev or infinite-dimensional certification."""
from pathlib import Path
import datetime, hashlib, json
import sympy as S

Root = Path(__file__).resolve().parents[1]
x, c = S.symbols('x c', real=True)
Results = []

def check(Name, Actual, Expected):
	Difference = Actual - Expected
	if isinstance(Difference, S.MatrixBase):
		Pass = all(S.simplify(Entry) == 0 for Entry in Difference)
	else:
		Pass = S.simplify(Difference) == 0
	Results.append({'name':Name,'passed':bool(Pass),'actual':str(Actual),'expected':str(Expected)})
	if not Pass:
		raise RuntimeError(Name)

def boundary(Polynomial):
	Delta = Polynomial.subs(x,1)-Polynomial.subs(x,-1)
	Derivative = S.diff(Polynomial,x)
	return S.Matrix([Derivative.subs(x,1)-Delta/2,Derivative.subs(x,-1)-Delta/2])

def centre(Polynomial):
	return S.Matrix([S.diff(Polynomial,x,k).subs(x,0) for k in range(3)])

def family(n):
	if n == 0: return S.Integer(1)
	if n == 1: return x
	m = n//2
	return x**n-S.Rational(m,m-1)*x**(n-2)

Unitary = S.Matrix([[1,1],[1,-1]])/S.sqrt(2)
check('unitary sqrt2 normalization',Unitary.T*Unitary,S.eye(2))
check('negative control unnormalized squared norm',Unitary.T*Unitary/2,S.eye(2)/2)
B4 = S.Matrix.hstack(*[boundary(x**n).col_join(boundary(S.diff(x**n,x,2))) for n in range(2,6)])
check('four-trace matrix',B4,S.Matrix([[2,2,4,4],[-2,2,-4,4],[0,0,24,40],[0,0,-24,40]]))
check('four-trace determinant',B4.det(),S.Integer(15360))
check('four-trace right inverse',B4*B4.inv(),S.eye(4))
for n in [0,1]+list(range(4,41)):
	Polynomial=family(n)
	check(f'Krein boundary p{n}',boundary(Polynomial),S.zeros(2,1))
	Target={0:S.Matrix([1,0,0]),1:S.Matrix([0,1,0]),4:S.Matrix([0,0,-4])}.get(n,S.zeros(3,1))
	check(f'centre traces p{n}',centre(Polynomial),Target)
check('p4 second boundary',boundary(S.diff(family(4),x,2)),S.Matrix([24,-24]))
check('Kc p4 violates domain',boundary(-S.diff(family(4),x,2)+c*family(4)),S.Matrix([-24,24]))
q6 = S.expand(family(6)-S.Rational(7,2)*family(4))
check('q6 polynomial',q6,x**6-5*x**4+7*x**2)
check('q6 four traces',boundary(q6).col_join(boundary(S.diff(q6,x,2))),S.zeros(4,1))
check('q6 centre second trace',centre(q6),S.Matrix([0,0,14]))
check('x2 domain exclusion',boundary(x*x),S.Matrix([2,-2]))
check('p5 critical Robin residual',x*S.diff(family(5),x,3)-S.diff(family(5),x,2),40*x**3)
check('q6 critical even residual',S.diff(q6,x,3),120*x*(x*x-1))

m = S.symbols('m',integer=True,positive=True)
pEven = x**(2*m)-m*x**(2*m-2)/(m-1)
pOdd = x*pEven
check('universal even leading residual m>=2',S.diff(pEven,x,3).subs(x,1),4*m*(4*m-5))
check('universal odd leading residual m>=2',(S.diff(pOdd,x,3)-S.diff(pOdd,x,2)).subs(x,1),4*m*(4*m-3))
L = 2*m
Tail = S.Matrix.hstack(boundary(x**L),boundary(x**(L+1))).applyfunc(S.simplify)
check('universal tail trace matrix L=2m',Tail,S.Matrix([[L,L],[-L,L]]))
check('universal tail determinant',Tail.det(),2*L**2)
u,v = S.symbols('u v')
Corrector = (u-v)*x**L/(2*L)+(u+v)*x**(L+1)/(2*L)
check('universal tail corrector',boundary(Corrector),S.Matrix([u,v]))

# Complex conjugates of the second function's endpoint data are independent variables.
a,b,d,e,A,B,D,E = S.symbols('a b d e A B D E')
fPrime=(b-a)/2; fThird=(e-d)/2
gPrime=(B-A)/2; gThird=(E-D)/2

def green4(F,F1,F2,F3,G,G1,G2,G3):
	return F3*G-F2*G1+F1*G2-F*G3-2*c*(F1*G-F*G1)
GreenDiff=green4(b,fPrime,e,fThird,B,gPrime,E,gThird)-green4(a,fPrime,d,fThird,A,gPrime,D,gThird)
check('fourth-order boundary isotropy for complex jets',GreenDiff,S.Integer(0))
check('second-order boundary isotropy',(-fPrime*B+b*gPrime)-(-fPrime*A+a*gPrime),S.Integer(0))

# Counterfactual statements are explicitly rejected, not silently expected to pass.
Negatives = {
 'omit sqrt2 and claim isometry': (Unitary.T*Unitary/2 == S.eye(2)),
 'reuse two-trace closure when p4 deleted': (centre(family(4))[2] == 0),
 'claim p4 belongs to square domain': (boundary(S.diff(family(4),x,2)) == S.zeros(2,1)),
 'replace Krein Delta/2 by Delta while retaining x': (S.diff(x,x).subs(x,1)-(x.subs(x,1)-x.subs(x,-1)) == 0)
}
if any(Negatives.values()): raise RuntimeError('A negative control was incorrectly accepted')
Result={'run_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'AUTHOR_EXACT_ALGEBRA_PASS','sympy_version':S.__version__,'checks':Results,'negative_controls':[{'claim':K,'rejected':not V} for K,V in Negatives.items()],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Exact normalization, finite boundary/centre algebra, symbolic all-m residual identities, and negative controls. No Sobolev, density, fractional-domain or independent-verifier certification.'}
(Root/'evidence'/'exact-checks.json').write_text(json.dumps(Result,indent=2)+'\n')
print(json.dumps({'status':Result['status'],'checks_passed':len(Results),'negative_controls_rejected':len(Negatives),'script_sha256':Result['script_sha256']}))
