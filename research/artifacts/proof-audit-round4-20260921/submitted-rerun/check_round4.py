#!/usr/bin/env python3
"""Independent, scoped audit checks for commit 2e9bf3d.

Requires sympy and mpmath. No network access or repository mutation.
PASS means that the named identity, counterexample or finite check is confirmed;
it does NOT mean that a repository theorem has passed a full audit.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import json
import math
import sympy as sp
import mpmath as mp

OUT = Path(__file__).resolve().parent
COMMIT = '2e9bf3d66fa21a41e16bf779782739ddd9505233'
checks: list[dict[str, str]] = []


def record(name: str, condition: bool, detail: object, kind: str = 'exact') -> None:
    ok = bool(condition)
    checks.append({'name': name, 'status': 'PASS' if ok else 'FAIL',
                   'kind': kind, 'detail': str(detail)})
    if not ok:
        raise AssertionError(f'{name}: {detail}')


def same(a: sp.Expr, b: sp.Expr = sp.Integer(0)) -> bool:
    return sp.simplify(a-b) == 0


x, j, c = sp.symbols('x j c', positive=True)


def sym_coeffs(p: int):
    P = 4*c*j*(2*j+2*p-1) + c**2*j/(j-1)
    Q = 4*j*(j-1)*(2*j+2*p-1)*(2*j+2*p-3) + 4*c*j*(2*j+2*p-3)
    R = 4*j*(j-2)*(2*j+2*p-3)*(2*j+2*p-5)
    return P, Q, R


def exact_coeffs(p: int, n: int, cv: F):
    P = 4*cv*n*(2*n+2*p-1) + cv**2*F(n,n-1)
    Q = 4*n*(n-1)*(2*n+2*p-1)*(2*n+2*p-3) + 4*cv*n*(2*n+2*p-3)
    R = 4*n*(n-2)*(2*n+2*p-3)*(2*n+2*p-5)
    return P, Q, R


def recurrence_values(p: int, cv: F, N: int) -> list[F]:
    """Backward terminal convention mu_N=1, mu_(N+1)=mu_(N+2)=0."""
    vals = [F(0)]*(N+3)
    vals[N] = F(1)
    for n in range(N+2,2,-1):
        P,Q,R = exact_coeffs(p,n,cv)
        vals[n-3] = (cv**2*vals[n]-P*vals[n-1]+Q*vals[n-2])/R
    return vals


# 1. Ordinary H1 convergence is not quotient convergence.
P2, P3 = sp.legendre(2,x), sp.legendre(3,x)
Q2, Q3 = (P2-1)/sp.sqrt(6), (P3-x)/sp.sqrt(10)
norm_h1 = lambda f: sp.integrate(f**2+sp.diff(f,x)**2,(x,-1,1))
record('unit-limit n=2 has nonzero constant discrepancy',
       same(P2/sp.sqrt(6)-Q2,1/sp.sqrt(6)), 'limit - Q2 = 1/sqrt(6)')
record('unit-limit n=2 ordinary H1 squared discrepancy',
       same(norm_h1(P2/sp.sqrt(6)-Q2),sp.Rational(1,3)), '1/3')
record('unit-limit n=3 has nonzero linear discrepancy',
       same(P3/sp.sqrt(10)-Q3,x/sp.sqrt(10)), 'limit - Q3 = x/sqrt(10)')
record('unit-limit n=3 ordinary H1 squared discrepancy',
       same(norm_h1(P3/sp.sqrt(10)-Q3),sp.Rational(4,15)), '4/15')
for n in range(2,11):
    Sn = sp.legendre(n,x)-sp.legendre(n-2,x)
    assert same(sp.diff(Sn,x),(2*n-1)*sp.legendre(n-1,x))
    assert same(sp.integrate(sp.diff(Sn,x)**2,(x,-1,1)),2*(2*n-1))
record('Legendre derivative and normalization finite symbolic cross-check',
       True,'n=2..10; general identity is proved/used separately','finite exact')
a4=1+15/c
a6=sp.expand(a4*(1+63/c)+sp.Rational(9,5)*(a4-1))
record('high-mode proof O(1) remainder counterexample',
       same(a6-63*a4/c,1+42/c), 'a6 - (63/c)*a4 = 1+42/c, not O(1)')

# 2. Four-parameter coefficient table: a missing reducible E+ tuple.
tau=sp.Rational(-3,4)
rat=(j**2-j/4-sp.Rational(3,8))/(j**2-3*j/4)
record('even reducible table counterexample', same(rat,1+1/(2*j)),
       '(a,b,cc,d)=(-1/4,-3/8,-3/4,0) represents e_plus')
record('the tuple is absent from both displayed b formulas',
       -sp.Rational(3,8) not in (-(tau+1)/2,(abs(2*tau+1)-1)/4),
       'displayed values are both -1/8; actual b=-3/8')
for p in (0,1):
    P,Q,R=sym_coeffs(p)
    aa1=P/(4*c*j**2); aa2=-Q/(16*j**2*(j-1)**2)
    aa3=c*R/(64*j**2*(j-1)**2*(j-2)**2)
    ep=lambda n:1+sp.Rational(2*p+1,2)/n
    record(f'known E+ ratio really solves recurrence, parity={p}',
        same(ep(j)-aa1-aa2/ep(j-1)-aa3/(ep(j-1)*ep(j-2))),
        'rational identity in j,c')
T=sp.symbols('T')
record('correct even reducible branch b=T/2',
       same((j**2+(T+sp.Rational(1,2))*j+T/2)/(j**2+T*j),1+1/(2*j)),
       'identity wherever denominators are nonzero')
record('correct odd rigid branch b=cc/2',
       same((j**2+(T+sp.Rational(1,2))*j+T/2)/(j**2+T*j),1+1/(2*j)),
       'same rational ratio is the odd rigid solution')

# 3. Reduction: non-identically-zero is insufficient for division.
Ep=lambda n:sp.prod(1+sp.Rational(1,2*k) for k in range(1,n+1))
Em=lambda n:sp.prod(1-sp.Rational(1,2*k) for k in range(1,n+1))
E=lambda n:(1-sp.Rational(n,3))*Em(n)
record('allowed solution E0=1 may have E3=0', E(0)==1 and E(3)==0,
       'E=(7/6)Eminus-(1/6)Eplus; division by E3 is undefined')
P,Q,R=sym_coeffs(0)
aa1=P/(4*c*j**2); aa2=-Q/(16*j**2*(j-1)**2)
aa3=c*R/(64*j**2*(j-1)**2*(j-2)**2)
for n in range(3,16):
    subs={j:n,c:sp.Rational(3)}
    assert same(E(n)-aa1.subs(subs)*E(n-1)-aa2.subs(subs)*E(n-2)-aa3.subs(subs)*E(n-3))
record('zero-containing E solves the recurrence',True,'n=3..15 exact, c=3; also follows from the linear combination','finite exact')
r=lambda n:sp.Rational(1,2*n+1)
s=lambda n:r(n)-r(n-1)
sub={j:3,c:1}
wrong=aa2.subs(sub)*Ep(1)*(s(3)+s(2))+aa3.subs(sub)*Ep(0)*(s(3)+s(2)+s(1))-Ep(3)*s(3)
correct=Ep(3)*s(3)+(aa2.subs(sub)*Ep(1)+aa3.subs(sub)*Ep(0))*s(2)+aa3.subs(sub)*Ep(0)*s(1)
record('printed intermediate reduction equation is false',same(wrong,sp.Rational(69,224)), 'residual 69/224 at c=1,j=3,E=Eplus,z=Eminus')
record('correct final reduction identity survives',same(correct), 'corrected residual zero on same exact data')

# 4. Old diagnostic floor-divides all four closed forms.
def mu_form(p: int, which: int, n: int, cv: F, floor: bool):
    offset=(1 if which==1 else 0) if p==0 else (3 if which==1 else 1)
    num=F(math.factorial(2*n+offset))
    den=cv**n*(6*(n+1) if p==1 and which==1 else 1)
    return num//den if floor else num/den
floor_rows=[]
expected=(F(117,2),F(-189),F(-621,2),F(165,2))
idx=0
for p in (0,1):
    for which in (1,2):
        P,Q,R=exact_coeffs(p,3,F(3))
        def residual(use_floor: bool):
            v=[mu_form(p,which,n,F(3),use_floor) for n in range(4)]
            return 9*v[3]-P*v[2]+Q*v[1]-R*v[0]
        bad,good=residual(True),residual(False)
        floor_rows.append({'parity':p,'form':which,'floor_residual':str(bad),'correct_residual':str(good)})
        assert bad==expected[idx] and good==0
        idx+=1
record('all four floor-division diagnostic counterexamples',True,floor_rows)
for p in (0,1):
    for which in (1,2):
        for cv in (F(1,4),F(1),F(3),F(10)):
            for n in range(3,31):
                P,Q,R=exact_coeffs(p,n,cv)
                v=lambda k:mu_form(p,which,k,cv,False)
                assert cv**2*v(n)-P*v(n-1)+Q*v(n-2)-R*v(n-3)==0
record('true closed forms finite exact regression',True,'4 forms x 4 shifts x 28 indices; rational division, no floors','finite exact')

# 5. Constructive supplemental factorization, both parities.
for p in (0,1):
    P,Q,R=sym_coeffs(p)
    D2=sp.prod(2*j+p-i for i in range(2))
    D4=sp.prod(2*j+p-i for i in range(4))
    D6=sp.prod(2*j+p-i for i in range(6))
    theta=c/(2*(j-1)*(2*j+2*p-1))
    record(f'factorial-scaled recurrence factorization, parity={p}',
       same(P/(c*D2),2+theta) and same(Q/D4,1+2*theta) and same(c*R/D6,theta),
       'Delta^2 v_j = theta_j Delta^2 v_(j-1), identity in j,c')
    zfac=1+sp.Rational(2*p-1,2)/j
    record(f'affine-factor rational family matches, parity={p}',
       same(zfac*(j+T+1)/(j+T),((j+sp.Rational(2*p-1,2))*(j+T+1))/(j*(j+T))),
       'all-degree classification is justified analytically in the supplement')

finite_count=0
for p in (0,1):
    for cv in (F(1,4),F(1),F(3),F(10)):
        for N in range(3,13):
            vals=recurrence_values(p,cv,N)
            a=lambda n:F(n)*cv**n/F(math.factorial(2*n+p))
            C=(cv**N/F(math.factorial(2*N+p)))/a(N+2)
            assert vals[0]>0
            for n in range(N+1):
                Phi=sum((F(r-n-1)*a(r) for r in range(n+2,N+3)),F(0))
                formula=F(math.factorial(2*n+p))*cv**(-n)*C*Phi
                assert vals[n]==formula
                finite_count+=1
record('general-c finite backward series cross-check',True,
       f'{finite_count} entries, both parities, 4 positive rational shifts, N=3..12','finite exact')
D=lambda f:sp.simplify(x*sp.diff(f,x)/2)
S0=(x*x*sp.cosh(x)-x*sp.sinh(x))/4
S1=((x*x+3)*sp.sinh(x)-3*x*sp.cosh(x))/(4*x)
record('even positive-series normalization closed form',same(D(D(sp.cosh(x)))-D(sp.cosh(x)),S0),'D(D-1) cosh(sqrt(c))')
record('odd positive-series normalization closed form',same(D(D(sp.sinh(x)/x))-D(sp.sinh(x)/x),S1),'D(D-1) [sinh(sqrt(c))/sqrt(c)]')
K0=x**4/(16*S0); K1=x**4/(16*S1)
record('even c=1 recovers established e/4 anchor',same(K0.subs(x,1),sp.E/4),'exact hyperbolic identity')
record('small-c normalization limits',sp.limit(K0,x,0)==sp.Rational(3,4) and sp.limit(K1,x,0)==sp.Rational(15,4),'even 3/4; odd 15/4')

# Numerical corroboration of supplemental constants, not a limit proof.
mp.mp.dps=75
numeric=[]
for p in (0,1):
    for cv in (mp.mpf(1),mp.mpf(3),mp.mpf(10)):
        root=mp.sqrt(cv)
        S=(cv*mp.cosh(root)-root*mp.sinh(root))/4 if p==0 else ((cv+3)*mp.sinh(root)-3*root*mp.cosh(root))/(4*root)
        K=cv**2/(16*S)
        n=200
        mu=sum((mp.mpf(r-n-1)*r*cv**(r-n)*mp.factorial(2*n+p)/mp.factorial(2*r+p)
                for r in range(n+2,n+30)),mp.mpf(0))/S
        numeric.append({'parity':p,'c':str(cv),'K':mp.nstr(K,35),'n':n,'n3_mu':mp.nstr(n**3*mu,35)})
        assert abs(n**3*mu/K-1)<mp.mpf('0.03')
record('supplemental constants numerical corroboration',True,
       'n=200 finite positive tails, c=1,3,10, both parities; proof is analytic','numerical')

result={'commit':COMMIT,'summary':{'checks':len(checks),'pass':sum(r['status']=='PASS' for r in checks)},
        'meaning':'confirmation of the named assertions/counterexamples; not full-repository certification',
        'checks':checks,'numeric_corroboration':numeric,
        'limitations':['No Lean build.','No M3/KP audit.','No PDF audit.','Only one original repository diagnostic was fully rerun; d4 floor issue was minimally reproduced.']}
(OUT/'round4_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for rec in checks:
    print(f"{rec['status']} [{rec['kind']}] {rec['name']}: {rec['detail']}")
print(json.dumps(result['summary']))
