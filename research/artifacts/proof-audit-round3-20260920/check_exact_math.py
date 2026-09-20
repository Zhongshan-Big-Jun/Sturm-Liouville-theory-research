from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sympy as S

Results = []
def check(Name, Condition, Scope):
	assert bool(Condition), Name
	Results.append({'name': Name, 'passed': True, 'scope': Scope})

M, C, D, U, V, A, B = S.symbols('m c delta u v A B', real=True)
Alpha = M/(M-1)+D
Ae = 2*M*(2*M-1)+C*Alpha
Be = Alpha*(2*M-2)*(2*M-3)
Ao = 2*M*(2*M+1)+C*Alpha
Bo = Alpha*(2*M-1)*(2*M-2)
for Name, Left, Factor in [('even', Ae-Be, (2*M-2)*(2*M-3)), ('odd', Ao-Bo, (2*M-1)*(2*M-2))]:
	check(Name+' perturbed gap identity', S.factor(Left-(4*M+C*M/(M-1)+D*(C-Factor)))==0, 'symbolic identity; m != 1')
check('real gap at c=3,m=4,delta=1', [Ae.subs({M:4,C:3,D:1}), Be.subs({M:4,C:3,D:1})]==[63,70], 'exact rational counterexample')
check('old gap 23 rejected', (Ae-Be).subs({M:4,C:3,D:1}) != 23, 'negative control')
Eps = (A-B-C)/C
check('recurrence decomposition', S.factor((A*U-B*V)/C-((1+Eps)*U+B/C*(U-V)))==0, 'symbolic identity; c != 0')
X = S.symbols('x', real=True)
Pe = X**8-Alpha.subs(M,4)*X**6
Po = X**9-Alpha.subs(M,4)*X**7
check('even derivative domain defect', S.diff(Pe,X).subs(X,1)==-6*D, 'degree 8 domain counterexample')
check('odd derivative domain defect', S.expand((S.diff(Po,X)-Po).subs(X,1))==-6*D, 'degree 9 domain counterexample')
G = (3*X**2-1)/2
check('P2 norm and affine orthogonality', [S.integrate(F,(X,-1,1)) for F in [G**2,G,X*G]]==[S.Rational(2,5),0,0], 'exact integrals')
Mu = 4*M/((2*M+1)*(2*M+3))
Nu = -4*M*(4*M**2+2*M-9)/((2*M+1)*(2*M+3))
Delta = 6*M*(2*M+5)/((M-1)*(2*M+3)*(4*M**2-6*M-7))
check('counterexample delta rational identity', S.factor(Nu/Nu.subs(M,M-1)-M/(M-1)-Delta)==0, 'symbolic rational identity')
check('bounded delta factorization', S.factor(1-Delta-(M-3)*(2*M-1)*(4*M**2+10*M+7)/((M-1)*(2*M+3)*(4*M**2-6*M-7)))==0, 'symbolic rational identity; signs require analytic m>=3 argument')
check('delta prefix and asymptotic coefficient', [Delta.subs(M,2),Delta.subs(M,3),S.limit(M**2*Delta,M,S.oo)]==[-S.Rational(36,7),1,S.Rational(3,2)], 'exact prefix and rational-function limit')
for N in range(1,17):
	check(f'P2 moments m={N}', S.integrate(G*X**(2*N),(X,-1,1))==Mu.subs(M,N) and S.integrate(G*(3*X**(2*N)-S.diff(X**(2*N),X,2)),(X,-1,1))==Nu.subs(M,N), 'finite exact integral cross-check; not universal proof')
for N in range(2,17):
	P = X**(2*N)-(S.Rational(N,N-1)+Delta.subs(M,N))*X**(2*N-2)
	check(f'nonzero orthogonal witness m={N}', S.integrate(G*(3*P-S.diff(P,X,2)),(X,-1,1))==0, 'finite exact cross-check of symbolically proved identity')
Seq, Prod, Growth = [Q(0),Q(1)], [Q(0),Q(1)], [Q(0),Q(1)]
for N in range(2,41):
	Seq.append(3*Seq[-1]-2*Seq[-2])
	Prod.append((1+Q(2,N))*Prod[-1])
	Growth.append((3+Q(2,N))*Growth[-1]-2*Growth[-2])
check('A3 B2 exact closed form finite cross-check', all(Seq[N]==2**N-1 for N in range(41)), 'm=0..40; induction is in proof and Lean')
check('B0 product normalization finite cross-check', all(Prod[N]==Q((N+1)*(N+2),6) for N in range(1,41)), 'm=1..40; Gamma identity in proof')
check('B2 product equality rejected', Growth[2]==4 and Prod[2]==2 and Growth[2]!=Prod[2], 'negative control against old all-B claim')
check('B2 exponent lower bound finite cross-check', all(Growth[N]>=2**N-1 for N in range(41)), 'finite exact cross-check; universal proof by differences')
Krein = [Q(0),Q(1)]
for N in range(2,5):
	Ak = 2*N*(2*N-1)+3*Q(N,N-1)
	Bk = 2*N*(2*N-3)
	Krein.append((Ak*Krein[-1]-Bk*Krein[-2])/3)
check('corrected Krein example', Krein[2:]==[6,63,1180], 'exact rational example')
check('old A/c lower bound rejected', Krein[4]<Q(60,3)*Krein[3], 'negative control')
check('all-index sufficient perturbation alpha bound', S.factor(M/(M-1)-1/(8*M)-1)==(7*M+1)/(8*M*(M-1)), 'identity with positive numerator/denominator for m>=2')
for Factor in [(2*M-2)*(2*M-3),(2*M-1)*(2*M-2)]:
	check('derivative factor below 4m^2: '+str(Factor), S.Poly(S.expand(4*M**2-Factor),M).degree()==1, 'coordinator analytic check: 10m-6 or 6m-2 positive for m>=2')
J = S.symbols('j', positive=True, integer=True)
check('quotient actual cosine image rejects h=x', S.integrate(X*(-S.pi*S.sin(S.pi*X)),(X,-1,1))==-2, 'exact integral negative control')
check('wrong original cosine moments vanish', S.simplify(S.integrate(X*S.cos(J*S.pi*X),(X,-1,1)))==0, 'symbolic parity integral')
Out = {'status':'PASS','count':len(Results),'sympy_version':S.__version__,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Algebraic identities, rational-function limits and finite exact cross-checks only. Universal completeness conclusions require analytic and independent review. Supplied report check_round3.py was not available or run.','checks':Results}
Path(__file__).with_name('exact-math-results.json').write_text(json.dumps(Out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({K:Out[K] for K in ['status','count','sympy_version','scope']},ensure_ascii=False))
