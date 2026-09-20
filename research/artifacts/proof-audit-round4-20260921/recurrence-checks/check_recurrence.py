#!/usr/bin/env python3
"""Author checks only. Symbolic identities and finite checks are not an audit."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib
import json
import platform
import re
import sys
import sympy as s
import mpmath as mp

Scratch=Path(__file__).resolve().parent
Root=Path('/mnt/f/LaTeX/BVE research')
Target=Root/'docs/SL_third_order_recurrence_theory.tex'
Results=[]
ExactCount=0


def require_true(Value, Message):
	global ExactCount
	ExactCount+=1
	if not Value:
		raise AssertionError(Message)


def symbolic_zero(Value, Message):
	require_true(s.cancel(Value)==0, Message)


def record_group(Name, Function):
	Start=ExactCount
	Function()
	Results.append({'name':Name,'status':'PASS','assertions':ExactCount-Start})
	print(Name+': PASS ('+str(ExactCount-Start)+' assertions)',flush=True)


def raw_coeffs(J,C,Eps):
	P=4*C*J*(2*J+2*Eps-1)+C*C*F(J,J-1)
	Q=4*J*(J-1)*(2*J+2*Eps-1)*(2*J+2*Eps-3)+4*C*J*(2*J+2*Eps-3)
	R=4*J*(J-2)*(2*J+2*Eps-3)*(2*J+2*Eps-5)
	return P,Q,R


def z_coeffs(J,C,Eps):
	P,Q,R=raw_coeffs(J,C,Eps)
	return P/(4*C*J*J),-Q/F(16*J*J*(J-1)**2),C*R/F(64*J*J*(J-1)**2*(J-2)**2)


def weight(J,C,Eps):
	return J*C**J/F(factorial(2*J+Eps))


def h_scale(J,Eps):
	return F(factorial(2*J+Eps),4**J*factorial(J)**2)


def exact_phi(J,N,C,Eps):
	return sum(((R-J-1)*weight(R,C,Eps) for R in range(J+2,N+3)),F(0))


def basis(J,Eps,Plus):
	Sigma=F(2*Eps-1,2)
	return h_scale(J,Eps)*((J+Sigma+1)/(Sigma+1) if Plus else 1)


def symbolic_groups():
	J,C,T,Beta=s.symbols('j c t beta')
	for Eps in (0,1):
		Sigma=s.Rational(2*Eps-1,2)
		P=4*C*J*(2*J+2*Eps-1)+C*C*J/(J-1)
		Q=4*J*(J-1)*(2*J+2*Eps-1)*(2*J+2*Eps-3)+4*C*J*(2*J+2*Eps-3)
		R=4*J*(J-2)*(2*J+2*Eps-3)*(2*J+2*Eps-5)
		Theta=C/(2*(J-1)*(2*J+2*Eps-1))
		for Value in (P/(C*s.prod(2*J+Eps-K for K in range(2)))-2-Theta,
		 Q/s.prod(2*J+Eps-K for K in range(4))-1-2*Theta,
		 C*R/s.prod(2*J+Eps-K for K in range(6))-Theta,
		 C*J/((J-1)*(2*J+Eps)*(2*J+Eps-1))-Theta):
			symbolic_zero(Value,'factorial coefficient, parity '+str(Eps))
		A1=P/(4*C*J**2)
		A2=-Q/(16*J**2*(J-1)**2)
		A3=C*R/(64*J**2*(J-1)**2*(J-2)**2)
		Rows=[(Sigma+T+1,Sigma*(T+1),T,0,(J+Sigma)*(J+T+1)/(J*(J+T))),
		 (Sigma+T,Sigma*T,T,0,(J+Sigma)/J),
		 (Sigma+1+T,(Sigma+1)*T,T,0,(J+Sigma+1)/J),
		 (Sigma+T,Sigma*T,T-1,-T,(J+Sigma)/(J-1))]
		for A,B,G,D,Expected in Rows:
			Ratio=(J*J+A*J+B)/(J*J+G*J+D)
			symbolic_zero(Ratio-Expected,'quadratic representation')
			Residual=Ratio-A1-A2/Ratio.subs(J,J-1)-A3/(Ratio.subs(J,J-1)*Ratio.subs(J,J-2))
			symbolic_zero(Residual,'quadratic family recurrence')
		for Bval in (2*Eps-1,2*Eps+1):
			Ratio=1+s.Rational(Bval,2)/J
			symbolic_zero(Ratio-A1-A2/Ratio.subs(J,J-1)-A3/(Ratio.subs(J,J-1)*Ratio.subs(J,J-2)),'beta allowed')
		Ratio=1+Beta/(2*J)
		Numerator=s.factor(s.together(Ratio-A1-A2/Ratio.subs(J,J-1)-A3/(Ratio.subs(J,J-1)*Ratio.subs(J,J-2))).as_numer_denom()[0])
		Leading=s.Poly(Numerator,J).LC()
		require_true(s.Poly(Leading,Beta).degree()==2,'beta necessary leading degree')
		symbolic_zero(Leading.subs(Beta,2*Eps-1),'beta necessary first root')
		symbolic_zero(Leading.subs(Beta,2*Eps+1),'beta necessary second root')
		D=2*(J-1)*(2*J+2*Eps-1)/C
		for Degree in range(8):
			Poly=J**Degree+s.Rational(2,3)
			Expr=s.Poly(s.expand(Poly-2*D*Poly.subs(J,J-1)+D*D.subs(J,J-1)*Poly.subs(J,J-2)),J)
			require_true(Expr.degree()==Degree+4,'polynomial obstruction degree')
			symbolic_zero(Expr.LC()-(s.Rational(5,3) if Degree==0 else 1)*16/C**2,'polynomial obstruction leading coefficient')


def finite_backward():
	for Eps in (0,1):
		for C in (F(1,7),F(1),F(3),F(10),F(100)):
			for N in (2,3,5,10,20):
				Z=[F(0)]*(N+3)
				Z[N]=F(1)
				for J in range(N+2,2,-1):
					A1,A2,A3=z_coeffs(J,C,Eps)
					Z[J-3]=(Z[J]-A1*Z[J-1]-A2*Z[J-2])/A3
				require_true(Z[0]>0,'positive raw normalization')
				for J in range(N+3):
					Expected=h_scale(J,Eps)*exact_phi(J,N,C,Eps)/(h_scale(N,Eps)*weight(N+2,C,Eps))
					require_true(Z[J]==Expected,'raw terminal formula')
					require_true(Z[J]/Z[0]==h_scale(J,Eps)*exact_phi(J,N,C,Eps)/exact_phi(0,N,C,Eps),'normalized finite formula')
				for J in range(2,N+3):
					require_true(exact_phi(J,N,C,Eps)-2*exact_phi(J-1,N,C,Eps)+exact_phi(J-2,N,C,Eps)==weight(J,C,Eps),'finite difference including endpoint')


def reduction_and_reverse():
	for Eps in (0,1):
		for C in (F(1,3),F(1),F(3),F(10)):
			for Plus in (False,True):
				N=25
				E=[basis(J,Eps,Plus) for J in range(N+1)]
				Z=[F(1),F(-2),F(7,3)]
				for J in range(3,N+1):
					A1,A2,A3=z_coeffs(J,C,Eps)
					Z.append(A1*Z[J-1]+A2*Z[J-2]+A3*Z[J-3])
				Rel=[Z[J]/E[J] for J in range(N+1)]
				Diff=[None]+[Rel[J]-Rel[J-1] for J in range(1,N+1)]
				Srev=[None,Diff[1],Diff[2]]
				for J in range(3,N+1):
					A1,A2,A3=z_coeffs(J,C,Eps)
					A=-(A2*E[J-2]+A3*E[J-3])/E[J]
					B=-A3*E[J-3]/E[J]
					require_true(E[J]*Diff[J]+(A2*E[J-2]+A3*E[J-3])*Diff[J-1]+A3*E[J-3]*Diff[J-2]==0,'correct intermediate identity')
					Srev.append(A*Srev[J-1]+B*Srev[J-2])
				for J in range(N+1):
					require_true(E[J]*(Rel[0]+sum(Srev[1:J+1],F(0)))==Z[J],'reverse initial r0,s1,s2')
				if Plus:
					Sm=[None]+[basis(J,Eps,False)/E[J]-basis(J-1,Eps,False)/E[J-1] for J in range(1,N+1)]
					W=[None,None,F(1)]
					Times=[None,F(0),F(1)]
					Ind=[None,F(0),Sm[2]]
					for J in range(3,N+1):
						A1,A2,A3=z_coeffs(J,C,Eps)
						A=-(A2*E[J-2]+A3*E[J-3])/E[J]
						B=-A3*E[J-3]/E[J]
						W.append(-B*Sm[J-2]/Sm[J]*W[J-1])
						Times.append(Times[J-1]+W[J])
						Ind.append(Sm[J]*Times[J])
						require_true(Ind[J]==A*Ind[J-1]+B*Ind[J-2],'variation recurrence')
					require_true(Sm[1]*Ind[2]-Sm[2]*Ind[1]!=0,'initial Casoratian')


def boundaries_and_negative_controls():
	Sigma=F(-1,2)
	for J in range(1,12):
		T=F(-3,4)
		Ratio=(J*J+(T+F(1,2))*J+T/2)/(J*J+T*J)
		require_true(Ratio==1+F(1,2*J),'audited even plus counterexample')
		Wrong=(J*J+(T+F(1,2))*J+(abs(2*T+1)-1)/4)/(J*J+T*J)
		require_true(Wrong!=Ratio,'old absolute value row rejected')
	for Eps in (0,1):
		for T in (F(-3),F(-1),F(0),F(2),F(3,7)):
			Sigma=F(2*Eps-1,2)
			for J in range(6,12):
				Ratio=(J*J+(Sigma+T)*J+Sigma*T)/(J*J+(T-1)*J-T)
				require_true(Ratio==(J+Sigma)/(J-1),'nonzero d cancellation family')
		for Tau in (F(-1),F(-2),F(-3),F(1,2)):
			Z=[h_scale(J,Eps)*(J+Tau+1) for J in range(8)]
			for J in range(3,8):
				A1,A2,A3=z_coeffs(J,F(1),Eps)
				require_true(Z[J]==A1*Z[J-1]+A2*Z[J-2]+A3*Z[J-3],'valid sequence despite finite zero')
			require_true((Z[0]==0)==(Tau==-1),'tail A=0 versus normalization')
		E=[(1-F(J,3))*h_scale(J,Eps) for J in range(8)]
		require_true(E[0]==1 and E[3]==0,'normalized reference can have zero')
		for J in range(3,8):
			A1,A2,A3=z_coeffs(J,F(1),Eps)
			require_true(E[J]==A1*E[J-1]+A2*E[J-2]+A3*E[J-3],'zero-term reference still solution')
	E=[basis(J,0,True) for J in range(4)]
	Rel=[basis(J,0,False)/E[J] for J in range(4)]
	Diff=[None]+[Rel[J]-Rel[J-1] for J in range(1,4)]
	A1,A2,A3=z_coeffs(3,F(1),0)
	Old=A2*E[1]*(Diff[3]+Diff[2])+A3*E[0]*(Diff[3]+Diff[2]+Diff[1])-E[3]*Diff[3]
	require_true(Old==F(69,224),'old intermediate identity negative control')
	Z=[F(1),F(2),F(5,2)]
	Z.append(A1*Z[2]+A2*Z[1]+A3*Z[0])
	require_true(Z[3]/Z[2]-F(7,6)==-F(1,480),'box counterexample')
	V=[Z[J]/h_scale(J,0) for J in range(3)]
	require_true((V[2]-2*V[1]+V[0])/weight(2,F(1),0)==-4,'box nonrational component')
	for Eps in (0,1):
		for M in range(1,7):
			Z=[F(1)]
			for J in range(1,M+4):
				Z.append(Z[-1]*(1-F(M,J)))
			J=M+2
			A1,A2,A3=z_coeffs(J,F(1),Eps)
			require_true(Z[J]-A1*Z[J-1]-A2*Z[J-2]-A3*Z[J-3]!=0,'beta zero factor negative control')


def k_symbolic():
	C=s.symbols('c',positive=True)
	X=s.sqrt(C)
	Functions=[s.cosh(X),s.sinh(X)/X]
	Phi=[(C*s.cosh(X)-X*s.sinh(X))/4,((C+3)*s.sinh(X)-3*X*s.cosh(X))/(4*X)]
	for Eps in (0,1):
		require_true(s.simplify(C*C*s.diff(Functions[Eps],C,2)-Phi[Eps])==0,'D(D-1) closed denominator')
		require_true(s.limit(C*C/(16*Phi[Eps]),C,0,dir='+')==s.Rational(factorial(4+Eps),32),'K right limit')
	require_true(s.simplify(s.expand((1/(16*Phi[0])).subs(C,1),func=True)-s.E/4)==0,'even K(1) anchor')


def numerical_diagnostics():
	mp.mp.dps=100
	Diagnostics=[]
	for Eps in (0,1):
		for TextC in ('0.001','1','3','100'):
			C=mp.mpf(TextC)
			X=mp.sqrt(C)
			ClosedPhi=(C*mp.cosh(X)-X*mp.sinh(X))/4 if Eps==0 else ((C+3)*mp.sinh(X)-3*X*mp.cosh(X))/(4*X)
			Phi0=mp.fsum(R*(R-1)*C**R/mp.factorial(2*R+Eps) for R in range(2,260))
			require_true(abs(ClosedPhi/Phi0-1)<mp.mpf('1e-85'),'numerical closed denominator versus positive sum')
			K=C*C/(16*Phi0)
			Ratios=[]
			for J in (20,80,320):
				Tail=mp.fsum((R-J-1)*R*C**R/mp.factorial(2*R+Eps) for R in range(J+2,J+260))
				Mu=mp.factorial(2*J+Eps)/C**J*Tail/Phi0
				T1=C*C*(J+2)/Phi0/mp.fprod(2*J+Eps+I for I in range(1,5))
				Q=C/(2*J+5+Eps)**2
				Bound=(1+Q)/(1-Q)**3-1
				require_true(Mu/T1>=1-mp.mpf('1e-90') and Mu/T1-1<=Bound+mp.mpf('1e-90'),'positive tail bound numeric diagnostic')
				Ratios.append(mp.nstr(J**3*Mu/K,20))
			Diagnostics.append({'epsilon':Eps,'c':TextC,'j':[20,80,320],'j3_mu_over_K':Ratios})
	(Scratch/'numerical_diagnostics.json').write_text(json.dumps(Diagnostics,indent=2)+'\n')


def tex_static():
	Text=Target.read_text()
	Envs=[]
	for Match in re.finditer(r'\\(begin|end)\{([^}]+)\}',Text):
		Kind,Name=Match.groups()
		if Kind=='begin':
			Envs.append(Name)
		else:
			require_true(bool(Envs) and Envs.pop()==Name,'TeX environment '+Name)
	require_true(not Envs,'TeX environments closed')
	Labels=re.findall(r'\\label\{([^}]+)\}',Text)
	require_true(len(Labels)==len(set(Labels)),'unique TeX labels')
	for Ref in re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',Text):
		require_true(Ref in Labels,'resolved label '+Ref)
	Bibs=re.findall(r'\\bibitem\{([^}]+)\}',Text)
	for Ref in re.findall(r'\\cite\{([^}]+)\}',Text):
		require_true(Ref in Bibs,'resolved citation '+Ref)
	Clean=re.sub(r'(?<!\\)%[^\n]*','',Text)
	Depth=0
	for M in re.finditer(r'(?<!\\)[{}]',Clean):
		Depth+=1 if M.group()=='{' else -1
		require_true(Depth>=0,'TeX nonnegative brace depth')
	require_true(Depth==0,'TeX balanced braces')
	InputManifest=json.loads((Scratch/'inputs.json').read_text())['input_sha256']
	for Name,Hash in InputManifest.items():
		if Name in ('AGENTS.md','docs/SL_third_order_recurrence_theory.tex'):
			continue
		require_true(hashlib.sha256((Root/Name).read_bytes()).hexdigest()==Hash,'historical input preserved '+Name)
	for Label in ('thm:beta','thm:closed','thm:reduction','thm:minimal','thm:minimal2','thm:asym','thm:rigid','thm:free','thm:full','sec:K','sec:box','eq:rhos'):
		require_true(Label in Labels,'preserved existing label '+Label)


Groups=[('symbolic coefficient, ratio and degree identities',symbolic_groups),
 ('exact finite backward recurrences and terminal normalization',finite_backward),
 ('exact reduction, reverse initialization and variation',reduction_and_reverse),
 ('cancellation, zero domains and rejected old formulas',boundaries_and_negative_controls),
 ('symbolic K denominators and endpoint limits',k_symbolic),
 ('high precision diagnostics, not analytic proofs',numerical_diagnostics),
 ('TeX structure and original input preservation, no compilation',tex_static)]
try:
	for Name,Function in Groups:
		record_group(Name,Function)
except Exception as Error:
	(Scratch/'results.json').write_text(json.dumps({'status':'FAIL','error':repr(Error),'completed':Results},indent=2)+'\n')
	raise
Manifest={'status':'PASS','scope':'AUTHOR_CHECKS_NOT_INDEPENDENT_REVIEW','assertions':ExactCount,'groups':Results,'source_sha256':hashlib.sha256(Target.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'versions':{'python':platform.python_version(),'sympy':s.__version__,'mpmath':mp.__version__},'command':'python3 /mnt/f/tools/math-audit-round4-20260921/recurrence-author/check_recurrence.py','not_performed':['PDF build','TeX compilation','Lean formalization','fresh-context independent review','historical program reruns','canonical edits']}
(Scratch/'results.json').write_text(json.dumps(Manifest,indent=2)+'\n')
print('TOTAL',ExactCount,'assertions. Author checks only.',flush=True)
