"""Independent scoped checks for audit round 5.

Exact/symbolic identities and finite numerical comparisons are separated.
All-index density assertions are proved in cofinite_replacement_proof.md,
not inferred from these checks. Run from this directory with Python 3.
"""
from __future__ import annotations

from fractions import Fraction as F
import argparse
from math import factorial
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import time

import mpmath as mp
import sympy as s

ROOT = Path(__file__).resolve().parent
RESULTS = []
start = time.monotonic()


def record(name, kind, condition, details=None):
    ok = bool(condition)
    RESULTS.append({'name': name, 'kind': kind, 'confirmed': ok, 'details': details})
    print(('CONFIRMED' if ok else 'FAILED') + ': ' + name, flush=True)
    if not ok:
        raise AssertionError(name)


def coeff(e, j, c):
    j, c = F(j), F(c)
    return (4*c*j*(2*j+2*e-1)+c*c*j/(j-1),
            4*j*(j-1)*(2*j+2*e-1)*(2*j+2*e-3)+4*c*j*(2*j+2*e-3),
            4*j*(j-2)*(2*j+2*e-3)*(2*j+2*e-5))


def H(e, j):
    return F(factorial(2*j+e), 4**j*factorial(j)**2)


def tail(e, j, c):
    return F(j)*F(c)**j/factorial(2*j+e)


def phi_finite(e, j, c, N):
    return sum((F(r-j-1)*tail(e,r,c) for r in range(j+2,N+3)), F(0))


def raw_backward(e, c, N):
    c = F(c)
    mu = [F(0)]*(N+3)
    mu[N] = F(factorial(N)**2) * (4/c)**N  # z_N=1
    for j in range(N+2, 2, -1):
        P,Q,R = coeff(e,j,c)
        mu[j-3] = (c*c*mu[j]-P*mu[j-1]+Q*mu[j-2])/R
    return [mu[j]/(F(factorial(j)**2)*(4/c)**j) for j in range(N+3)]


def integrate_poly(p, x):
    p=s.Poly(s.expand(p),x)
    return sum((coef*s.Rational(2,k[0]+1) for k,coef in p.terms() if k[0]%2==0), s.S.Zero)


def sparse(n,x):
    if n in (0,1): return x**n
    m=n//2
    return x**n-s.Rational(m,m-1)*x**(n-2)


def boundary(p,x):
    d=(p.subs(x,1)-p.subs(x,-1))/2
    return s.Matrix([s.diff(p,x).subs(x,1)-d,s.diff(p,x).subs(x,-1)-d])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'d4_third_order_theory.py', help='Exact scripts/d4_third_order_theory.py from the audited commit')
    path=parser.parse_args().source.resolve()
    data=path.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    record('current d4 source identity', 'byte identity', blob=='951e316d9d483d46eeb61a3a16a555f3b72e0a40', {'git_blob':blob})
    spec=importlib.util.spec_from_file_location('audited_d4',path)
    d4=importlib.util.module_from_spec(spec); spec.loader.exec_module(d4)

    j,c=s.symbols('j c', positive=True)
    changes=[]
    for e in (0,1):
        P=4*c*j*(2*j+2*e-1)+c*c*j/(j-1)
        Q=4*j*(j-1)*(2*j+2*e-1)*(2*j+2*e-3)+4*c*j*(2*j+2*e-3)
        R=4*j*(j-2)*(2*j+2*e-3)*(2*j+2*e-5)
        th=c/(2*(j-1)*(2*j+2*e-1))
        fall=lambda k:s.prod(2*j+e-i for i in range(k))
        changes += [s.cancel(P/c/fall(2)-(2+th))==0,
                    s.cancel(Q/fall(4)-(1+2*th))==0,
                    s.cancel(c*R/fall(6)-th)==0]
    record('both parity factorial reductions', 'symbolic identity', all(changes))

    rows=[]
    for e in (0,1):
        for C in (F(1,4),F(1),F(3),F(10)):
            for plus in (False,True):
                def mu(k):
                    base=F(factorial(2*k+e))/C**k
                    return base*(F(k)+F(2*e+1,2))/F(2*e+1,2) if plus else base
                for J in range(3,21):
                    P,Q,R=coeff(e,J,C)
                    rows.append(C*C*mu(J)-P*mu(J-1)+Q*mu(J-2)-R*mu(J-3)==0)
    record('four repaired closed forms', 'exact finite check', all(rows), {'instances':len(rows)})
    record('non-integer factorial quotient not rounded', 'exact counter-regression', d4.even_form2(3,3)==F(80,3))

    counts=0; ok=True
    for e in (0,1):
        for C in (F(1,4),F(1),F(3),F(10)):
            for N in (2,3,5,9):
                z=raw_backward(e,C,N)
                for J in range(N+3):
                    direct=H(e,J)*phi_finite(e,J,C,N)/(H(e,N)*tail(e,N+2,C))
                    ok &= z[J]==direct; counts+=1
    record('finite backward formula versus original mu recurrence', 'exact finite check', ok, {'instances':counts})
    ok=True;counts=0
    for e in (0,1):
        for C in (F(1,4),F(1),F(3)):
            for N in (2,5,12):
                z=raw_backward(e,C,N)
                zz=d4.minimal_solution('e' if e==0 else 'o',C,N=N,Precision=70)
                with mp.workdps(70):
                    for J in range(N+1):
                        rr=z[J]/z[0]; exact=mp.mpf(rr.numerator)/rr.denominator
                        ok &= abs(zz[J]/exact-1)<mp.mpf('1e-64');counts+=1
    record('current d4 finite minimal solution versus exact terminal problem','finite multiprecision comparison',ok,{'instances':counts,'dps':70})

    a=s.symbols('a', positive=True)
    D=lambda f:s.expand(a*s.diff(f,a)/2)
    Ph0=(a*a*s.cosh(a)-a*s.sinh(a))/4
    Ph1=((a*a+3)*s.sinh(a)-3*a*s.cosh(a))/(4*a)
    record('two Phi0 hyperbolic identities','symbolic identity',
           s.simplify(D(D(s.cosh(a)))-D(s.cosh(a))-Ph0)==0 and
           s.simplify(D(D(s.sinh(a)/a))-D(s.sinh(a)/a)-Ph1)==0)
    K0=a**4/(16*Ph0); K1=a**4/(16*Ph1)
    record('K0(1)=e/4','symbolic identity',s.simplify(s.expand_func(K0.subs(a,1)).rewrite(s.exp)-s.E/4)==0)
    record('right limits of K0,K1 at c=0','symbolic limits',s.limit(K0,a,0)==s.Rational(3,4) and s.limit(K1,a,0)==s.Rational(15,4))
    record('pole argument leading coefficient','symbolic identity',s.LC(s.Poly((2*(j-1)*(2*j-1)/c)*(2*(j-2)*(2*j-3)/c),j))==16/c**2)

    t=s.symbols('t');checks=[]
    for e in (0,1):
        sig=s.Rational(2*e-1,2)
        P=4*c*j*(2*j+2*e-1)+c*c*j/(j-1)
        Q=4*j*(j-1)*(2*j+2*e-1)*(2*j+2*e-3)+4*c*j*(2*j+2*e-3)
        R=4*j*(j-2)*(2*j+2*e-3)*(2*j+2*e-5)
        A1=P/(4*c*j*j); A2=-Q/(16*j*j*(j-1)**2); A3=c*R/(64*j*j*(j-1)**2*(j-2)**2)
        ratios=[(j+sig)*(j+t+1)/(j*(j+t)),(j+sig)*(j+t)/(j*(j+t)),
                (j+sig+1)*(j+t)/(j*(j+t)),(j+sig)*(j+t)/((j-1)*(j+t))]
        for r in ratios:
            checks.append(s.cancel(r-A1-A2/r.subs(j,j-1)-A3/(r.subs(j,j-1)*r.subs(j,j-2)))==0)
    record('all four parameter-table rows for both parities','symbolic identity',all(checks),{'rows':len(checks)})
    record('baseline normalized at zero can still vanish later','exact counter-regression',(1-F(3,3))*H(0,3)==0 and H(0,0)==1)
    record('ordinary zero baseline rejected by current d4','behavioral check',raises_value_error(lambda:d4.reduction_coefficients(1,2,0,3,4)))
    record('symbolic zero baseline rejected by current d4','behavioral check',raises_value_error(lambda:d4.reduction_coefficients(1,2,s.S.Zero,3,4)))

    x=s.symbols('x');checks=[]
    for n in range(2,11):
        Sn=s.legendre(n,x)-s.legendre(n-2,x)
        checks.append(s.expand(s.diff(Sn,x)-(2*n-1)*s.legendre(n-1,x))==0)
        checks.append(integrate_poly(s.diff(Sn,x)**2,x)==2*(2*n-1))
    record('zero-parameter Legendre Gram identities','exact finite polynomial checks',all(checks),{'indices':'2..10'})
    record('low-mode representative differences persist in ordinary H1','exact integral',
           integrate_poly(s.Rational(1,6),x)==s.Rational(1,3) and
           integrate_poly((x*x+1)/10,x)==s.Rational(4,15))
    ac={0:s.S.One,1:s.S.One,2:s.S.One,3:s.S.One}
    for n in range(2,11):
        ac[n+2]=s.expand(ac[n]*(1+(4*n*n-1)/c)+s.Rational(2*n+1,2*n-3)*(ac[n]-ac[n-2]))
    checks=[]
    for n in range(2,11):
        m,e=divmod(n,2);power=m-1
        leading=s.prod(4*(2*k+e)**2-1 for k in range(1,m))
        checks.append(s.limit(ac[n]*c**power,c,0)==leading)
        norm=2*c*ac[n]*ac[n+2]/(2*n+1)
        checks.append(s.limit(norm*c**(2*power),c,0)==2*(2*n-1)*leading**2)
    record('fixed-index coefficient and norm leading terms','symbolic finite-index checks',all(checks),{'indices':'2..10'})

    xp=s.symbols('x',real=True)
    gp=s.cosh(a*(1-xp))/(2*a*s.sinh(a))
    hp=(a*s.cosh(a*(1-xp))-s.sinh(a*(1-xp)))/(2*(a*s.cosh(a)-s.sinh(a)))
    record('evaluation Green kernel ODE and endpoint traces','symbolic identity',
           s.simplify(-s.diff(gp,xp,2)+a*a*gp)==0 and s.diff(gp,xp).subs(xp,1)==0 and s.simplify(s.diff(gp,xp).subs(xp,0)+s.Rational(1,2))==0)
    record('derivative Green kernel ODE and endpoint traces','symbolic identity',
           s.simplify(-s.diff(hp,xp,2)+a*a*hp)==0 and s.simplify(s.diff(hp,xp).subs(xp,1)-hp.subs(xp,1))==0 and s.simplify(hp.subs(xp,0)-s.Rational(1,2))==0)
    fL,fR,f0,fp0=s.symbols('fL fR f0 fp0'); delta=(fR-fL)/2
    # Exact interface formula for piecewise homogeneous g:
    # endpoint terms + [g]_0 f'(0) - [g']_0 f(0).
    ev=-gp.subs(xp,1)*delta+gp.subs(xp,1)*delta+f0
    der=-hp.subs(xp,1)*delta+hp.subs(xp,1)*fR-hp.subs(xp,1)*delta-hp.subs(xp,1)*fL+fp0
    record('Green pairing reduces to f(0) and fprime(0)','symbolic boundary identity',s.simplify(ev-f0)==0 and s.simplify(der-fp0)==0)
    checks=[]
    for n in [0,1]+list(range(4,31)):
        p=sparse(n,x)
        checks += [all(s.expand(v)==0 for v in boundary(p,x)),p.subs(x,0)==(1 if n==0 else 0),s.diff(p,x).subs(x,0)==(1 if n==1 else 0)]
    record('sparse polynomials have exactly the two low jet modes','exact finite polynomial checks',all(checks),{'indices':'0,1,4..30'})

    mp.mp.dps=60; worst=mp.mpf(0); cases=0
    for C in (mp.mpf('0.25'),mp.mpf(1),mp.mpf(3)):
        aa=mp.sqrt(C)
        g=lambda xx:mp.cosh(aa*(1-xx))/(2*aa*mp.sinh(aa))
        for n in [0]+list(range(4,17,2)):
            if n==0:
                q=lambda xx:C
            else:
                m=n//2;al=mp.mpf(m)/(m-1)
                q=lambda xx,n=n,al=al:C*(xx**n-al*xx**(n-2))-n*(n-1)*xx**(n-2)+al*(n-2)*(n-3)*xx**(n-4)
            val=2*mp.quad(lambda xx:g(xx)*q(xx),[0,1]); target=int(n==0)
            worst=max(worst,abs(val-target));cases+=1
    record('nonzero L2 obstruction satisfies every tested high recurrence','finite multiprecision comparison',worst<mp.mpf('1e-50'),{'instances':cases,'worst_absolute_residual':mp.nstr(worst,8),'dps':60})

    record('odd norm factor in old STRICT lemma is wrong','exact counterexample',
           integrate_poly(x*x,x)==s.Rational(2,3) and s.Rational(1,2)*s.integrate(s.sqrt(x),(x,0,1))==s.Rational(1,3))
    checks=[]
    for L in (2,4,6,10):
        mat=s.Matrix.hstack(boundary(x**L,x),boundary(x**(L+1),x))
        checks.append(mat.det()==2*L**2)
        p=x**L*(3+x-2*x**4+x**9)
        b=boundary(p,x); sol=mat.inv()*b
        p=s.expand(p-sol[0]*x**L-sol[1]*x**(L+1))
        remainder=p
        while remainder!=0:
            pol=s.Poly(remainder,x); n=pol.degree()
            if n<L+2: checks.append(False);break
            remainder=s.expand(remainder-pol.LC()*sparse(n,x))
        checks.append(remainder==0)
    record('tail polynomial space and trace-correction matrix','exact finite algebra check',all(checks))
    checks=[]
    for n in [0,1]+list(range(4,30)):
        p=sparse(n,x)
        checks.append((s.simplify(p.subs(x,0)-s.diff(p,x).subs(x,0))==0)==(n>=4))
    record('oblique trace constraint keeps exactly all high sparse members','exact finite polynomial check',all(checks))
    p6=x**6-5*x**4+7*x**2
    record('historical all-polynomials-affine statement not valid','symbolic counterexample',
           boundary(p6,x)==s.zeros(2,1) and s.simplify(boundary(c*p6-s.diff(p6,x,2),x))==s.zeros(2,1))

    out={'commit':'c0b36b90004cffb0552c9fa9f229e1f7cec8a706','duration_seconds':time.monotonic()-start,
         'all_confirmed':all(r['confirmed'] for r in RESULTS),'named_checks':len(RESULTS),'checks':RESULTS,
         'limitations':'Finite and symbolic checks do not certify the entire repository. See analytic replacement proof. No Lean build, PDF audit, M3/KP or global test-suite rerun.'}
    (ROOT/'round5_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('ALL CONFIRMED:',len(RESULTS))
    return 0


def raises_value_error(f):
    try: f()
    except ValueError: return True
    return False


if __name__=='__main__':
    sys.exit(main())
