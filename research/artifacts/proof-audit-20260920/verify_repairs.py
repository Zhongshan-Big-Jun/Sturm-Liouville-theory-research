"""Independent exact checks for the 2026-09-20 local repairs, not a global audit."""
from pathlib import Path
from fractions import Fraction
from math import factorial
import ast
import contextlib
import io
import json
import subprocess
import sys
import sympy as S

Root = Path(__file__).resolve().parents[3]
Artifact = Path(__file__).resolve().parent
Checks = []
def check(Name, Condition, Detail):
	Passed = bool(Condition)
	Checks.append({'name': Name, 'passed': Passed, 'detail': str(Detail)})
	if not Passed:
		raise AssertionError(Name + ': ' + str(Detail))

def partial_sum(X, Degree, Sine):
	# Independent degree-based interface, unlike the production term-count API.
	return sum((Fraction((-1)**((K-int(Sine))//2), factorial(K))*X**K
		for K in range(int(Sine), Degree+1, 2)), Fraction(0))

X, C = S.symbols('x c', real=True)
P4 = X**4-2*X**2
Kp4 = S.expand(C*P4-S.diff(P4,X,2))
check('F01: p4 in D(Kc)', S.diff(P4,X).subs(X,1)==0 and P4.subs(X,1)==P4.subs(X,-1), P4)
check('F01: p4 not in D(Kc^2), all c', [S.diff(Kp4,X).subs(X,V) for V in [1,-1]]==[-24,24], Kp4)
Residuals = S.Matrix([[S.diff(X**K,X).subs(X,V)-(1-(-1)**K)/2 for K in [2,3]] for V in [1,-1]])
check('F05: two independent polynomial boundary constraints', Residuals.det()!=0, Residuals)
check('F05: x2 is outside D(Kc)', Residuals[0,0]!=0, Residuals[:,0])
check('Growth hypothesis: omitted sign has counterexample', -1*1-(-2)*0==-1, 'c0=1, A2=-1, B2=-2, A2-B2=1, u2=-1')
for Q in [Fraction(1),Fraction(3),Fraction(10),Fraction(50)]:
	Prev2,Prev1 = Fraction(0),Fraction(1)
	for J in range(2,31):
		A = 2*J*(2*J-1)+Q*J/(J-1)
		B = 2*J*(2*J-3)
		Current = (A*Prev1-B*Prev2)/Q
		assert Current >= Prev1 and Current >= (4/Q)**(J-1)*factorial(J)
		Prev2,Prev1 = Prev1,Current
check('Growth: exact finite checks supplement the induction', True, 'c=1,3,10,50; j=2..30; proof still requires B_j>=0')

T = Fraction(961,1000)
Old = Fraction(5104691704723563842653351044859938032346287993281,3566219119511749539487170630605640000000000000000)
Upper = partial_sum(T,13,True)/partial_sum(T,10,False)
Lower = partial_sum(T,15,True)/partial_sum(T,12,False)
check('F02: old R1 equals S13/C8', Old==partial_sum(T,13,True)/partial_sum(T,8,False), Old)
check('F02: certified lower bound already exceeds old upper', Lower>Old, Lower-Old)
check('F02: corrected endpoint chain', Upper<Fraction(14315,10000)<Fraction(14472,10000)<2*(Fraction(223,71)-T)/3, Upper)
T2 = Fraction(97,100)
Lower2 = partial_sum(T2,11,True)/partial_sum(T2,8,False)
check('C1: second endpoint chain', Lower2>Fraction(14591,10000)>Fraction(14546,10000)>2*(Fraction(22,7)-T2)/3, Lower2)
PiLo,PiHi = Fraction(223,71),Fraction(22,7)
YLo,YHi=PiLo-T2,PiHi-T
WLo,WHi=YLo-PiHi/2,YHi-PiLo/2
C2=4*YLo**4/(9+4*YHi**2)
C3=6-Fraction(7,2)*PiLo**2*(1-2*WHi**2)+2*YHi*(2*YHi**2-9)
C4=6*YHi-12*YLo**2*Fraction(93,200)-2*YLo**3*Fraction(63,250)+PiHi**2/2
C5=16*YLo**4-4*PiHi**2*YHi**2-15*PiHi**2
check('C2: squared endpoint bound', C2>Fraction(1623,912)**2 and Fraction(1623,912)>PiHi/2, C2)
check('C3: derivative upper bound', C3 < -Fraction(56,129), C3)
check('C4: auxiliary sine lower bound', partial_sum(2*WLo,7,True)/2>=Fraction(93,200), partial_sum(2*WLo,7,True)/2)
check('C4: auxiliary cosine lower bound', 1-2*WHi**2>=Fraction(63,250), 1-2*WHi**2)
check('C4: second derivative upper bound', C4 < -13, C4)
check('C5: positive endpoint bound', C5>19, C5)
check('G second derivative at zero', PiHi**2<12, 'Gpp(0)=pi*(3-pi^2/4)>0')

# Load only mathematical bound function definitions for API/regression checks.
Production = Root/'scripts/_symline_allR_certificates.py'
Tree = ast.parse(Production.read_text())
FunctionNodes = [Node for Node in Tree.body if isinstance(Node,ast.FunctionDef) and Node.name!='check']
Namespace={'F':Fraction,'factorial':factorial}
exec(compile(ast.Module(body=FunctionNodes,type_ignores=[]),str(Production),'exec'),Namespace)
for T in [Fraction(0),Fraction(1,10),Fraction(1,2),Fraction(961,1000),Fraction(97,100),Fraction(1)]:
	# Alternating remainder gives refined reference intervals at degrees 23..26.
	assert Namespace['sin_lo'](T)<=partial_sum(T,23,True)<=partial_sum(T,25,True)<=Namespace['sin_up'](T)
	assert 0<Namespace['cos_lo'](T)<=partial_sum(T,26,False)<=partial_sum(T,24,False)<=Namespace['cos_up'](T)
check('F02: production envelopes enclose tighter exact intervals', True, 'six rational points including 0 and 1; alternating remainder is analytic justification')
for Function,N in [('sin_up',6),('sin_lo',7),('cos_lo',5),('cos_up',6)]:
	try:
		Namespace[Function](Fraction(1,2),N)
	except ValueError:
		continue
	raise AssertionError('Invalid parity accepted: '+Function)
check('F02: invalid parity rejected', True, 'Old cos_lo n=5 is rejected')
for Function in ['sin_up','sin_lo','cos_lo','cos_up']:
	for T in [Fraction(-1,10),Fraction(11,10)]:
		try:
			Namespace[Function](T)
		except ValueError:
			continue
		raise AssertionError('Unsupported domain accepted')
check('F02: unsupported domains rejected', True, '[0,1] contract')
Run = subprocess.run([sys.executable,str(Production)],capture_output=True,text=True)
(Artifact/'certificate-output.txt').write_text(Run.stdout+Run.stderr)
check('Revised C1-C5 certificate program', Run.returncode==0 and Run.stdout.rstrip().endswith('ALL PASS'), f'exit={Run.returncode}; checks={Run.stdout.count("PASS")-1}')

Q,Cv = S.symbols('q cv',positive=True)
Ftilde = S.Function('Ftilde')(Cv)
check('F03: normalization derivative factor', S.diff(Q*(Q**2-1)*Ftilde,Cv,2)==Q*(Q**2-1)*S.diff(Ftilde,Cv,2), 'Fpp=q(q^2-1)*Ftildepp, q fixed')
check('F03: unnormalized q=1 boundary', (Q*(Q**2-1)*S.diff(Ftilde,Cv,2)).subs(Q,1)==0, 'Fpp=0 at q=1')
# B4's polynomial identity is the independent sign proof in the original package.
P=3*X**2+6*X*S.sin(X)-3*S.pi*X-3*S.pi*S.sin(X)+S.pi**2
check('F03: B4 polynomial sign identity', S.expand(P-(S.pi-3*X)**2-3*(X-S.sin(X))*(S.pi-2*X))==0, 'P-(pi-3x)^2=3(x-sin x)(pi-2x)>0, 0<x<pi/3')
Z,T=S.symbols('z t',real=True)
Q=Z/(1-Z)
Phi=2*Z**2/(1-Z)
Denominator=Q+Phi/2
def normalized_m_prime(Angle, Cosine):
	AnglePrime=-Angle*Phi/Denominator
	return (2*Angle*T*T+2*Angle*Angle*T*Cosine)*AnglePrime/Denominator-Angle*Angle*T*T*(Phi+T*Cosine*(Q*Q-1)*AnglePrime)/Denominator**2
Expected=2*S.pi*(Z-1)**3*(3*X*X+6*X*T-3*S.pi*X-3*S.pi*T+S.pi**2)/T**3
Numerator=S.fraction(S.factor(normalized_m_prime(X,Z)-normalized_m_prime(S.pi-X,-Z)-Expected))[0]
Remainder=S.rem(Numerator,S.Poly(T*T+Z*Z-1,T),T)
check('F03: full B4 formula from normalized M derivative', Remainder.is_zero, 'q=z/(1-z), z=cos x, t=sin x, c=1/2; exact polynomial remainder zero')
check('F03: printed box lower bound is rounded down', Fraction(83793,10000)<Fraction(83793828,10000000), '8.3793 < archived audit bound 8.3793828; 8.3794 was rounded upward')
check('C5: monotonicity domain is sufficient', YLo>2 and 8*YLo**2>PiHi**2, 'hprime(y)=8y(8y^2-pi^2)>0 on the actual endpoint interval')
N1,N2,L1,L2 = S.symbols('n1 n2 lambda1 lambda2',positive=True)
V = S.symbols('v', real=True)
Ratio = S.sqrt(N1/N2)*V
check('F04: normalized quotient square', S.simplify(Ratio**2-N1/N2*V**2)==0, 'vhat=sqrt(n1/n2)*v; positive constant preserves monotonicity')
check('F04: corrected left endpoint', S.simplify((L1-L2*Ratio**2).subs(V,1)-(L1-L2*N1/N2))==0, 'left sign is not fixed by lambda1<lambda2 alone')
U,Up,Lambda,R = S.symbols('u up lambda r')
check('F06: block energy derivative', S.expand(2*Up*(-Lambda*R*U)+2*Lambda*R*U*Up)==0, '2uprime*(usecond+lambda*r*u)=0')
A,B=S.symbols('a b')
check('F06: normalized global energy', S.expand((A-B)+(A-B)+2*(B-A))==0, 'K=(a-b)+(a-b)=-2(b-a)')
Z=S.symbols('z')
KernelSquare=S.integrate((Z*(1-X))**2,(Z,0,X))+S.integrate((X*(1-Z))**2,(Z,X,1))
check('F07: Green kernel squared integral', S.simplify(KernelSquare-X**2*(1-X)**2/3)==0, KernelSquare)
check('F07: exact supremum 1/48', S.simplify(KernelSquare.subs(X,S.Rational(1,2)))==S.Rational(1,48), 'x(1-x)<=1/4, 0<=x<=1')
def green_integral(Expression):
	return S.integrate(Z*(1-X)*Expression,(Z,0,X))+S.integrate(X*(1-Z)*Expression,(Z,X,1))
Commutator=S.expand(green_integral(1+Z)-(1+X)*green_integral(1))
check('F07: noncommutativity counterexample', S.simplify(Commutator-X*(X-1)*(2*X-1)/6)==0 and Commutator!=0, Commutator)
Tau,T=S.symbols('tau t',positive=True)
Reflection=S.pi-Tau*(S.pi*T/(1+Tau))-S.pi*T/(1+Tau)
check('F08: reflected angle is larger than x', S.simplify(Reflection-S.pi*(1-T))==0, 'x=pi*t/(1+tau), 0<t<1; reflected angle minus x=pi(1-t)>0')

Payload={'scope':'Local counterexamples, repaired rational certificates and identities. Not a full theorem, interval-engine or Lean audit.','sympy_version':S.__version__,'checks':Checks,'passed':len(Checks),'failed':0,'C3_decimal':float(C3),'C4_decimal':float(C4),'C5_decimal':float(C5),'R1_new':str(Upper)}
(Artifact/'verification-results.json').write_text(json.dumps(Payload,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({Key:Value for Key,Value in Payload.items() if Key!='checks'},ensure_ascii=False,indent=2))
