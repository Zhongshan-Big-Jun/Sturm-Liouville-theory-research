#!/usr/bin/env python3
"""Independent round-9 checks of pinned repository statements.
No repository module is imported; this is not the author's full test suite.
Exact checks prove finite identities/inequalities only. The attached analysis
supplies all universal statements and infinite-dimensional limiting arguments.
Usage: python checks.py [output.json]
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
import json, math, sys, platform
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp

HEAD = '2a81b608d53e3decee04c46716a8d8f8c2d9b1b4'
ROWS = []
def check(ok, name, kind, **evidence):
    if not bool(ok):
        raise ArithmeticError(name)
    ROWS.append(dict(name=name, kind=kind, confirmed=True, evidence=evidence))

def display(q, up=False):
    with localcontext() as c:
        c.prec=62
        c.rounding=ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(q.numerator)/Decimal(q.denominator))

@dataclass(frozen=True)
class QI:
    lo:F
    hi:F
    def __post_init__(self):
        if self.lo>self.hi: raise ArithmeticError('reversed interval')
    @staticmethod
    def of(x): return x if isinstance(x,QI) else QI(F(x),F(x))
    def __add__(self,x):
        x=self.of(x); return QI(self.lo+x.lo,self.hi+x.hi)
    __radd__=__add__
    def __neg__(self): return QI(-self.hi,-self.lo)
    def __sub__(self,x): return self+-self.of(x)
    def __rsub__(self,x): return self.of(x)+-self
    def __mul__(self,x):
        x=self.of(x); p=[a*b for a in (self.lo,self.hi) for b in (x.lo,x.hi)]
        return QI(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.of(x)
        if x.lo<=0<=x.hi: raise ZeroDivisionError('zero in divisor')
        return self*QI(1/x.hi,1/x.lo)
    def __rtruediv__(self,x): return self.of(x)/self
    def __pow__(self,n):
        if n<0: return QI.of(1)/(self**(-n))
        if n==0:return QI.of(1)
        if n%2:return QI(self.lo**n,self.hi**n)
        return QI(F(0) if self.lo<=0<=self.hi else min(self.lo**n,self.hi**n),max(self.lo**n,self.hi**n))
    def show(self): return [display(self.lo),display(self.hi,True)]

def trig(x, degree=110):
    x=F(x); sn=F(0); cs=F(1); term=F(1)
    for j in range(1,degree+1):
        term*=x/j
        if j%4==1: sn+=term
        elif j%4==3:sn-=term
        elif j%4==2:cs-=term
        else:cs+=term
    rem=abs(term*x)/(degree+1)
    return QI(sn-rem,sn+rem),QI(cs-rem,cs+rem)

def atan_small(x,n):
    if not 0<x<1:raise ValueError('domain')
    a=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(n)),F(0))
    b=a+(-1)**n*x**(2*n+1)/(2*n+1)
    return QI(min(a,b),max(a,b))
PI=16*atan_small(F(1,5),85)-4*atan_small(F(1,239),28)

def gbox(a):
    sn,_=trig(a); sn2,_=trig(2*a,130)
    return 8*a**3*sn**2-PI**2*(2*a-sn2)

def ubox(a):
    sn,cs=trig(a); return a/(2*(a-sn/cs))

def bisect(fun,lo,hi,n=210):
    fl,fh=fun(lo),fun(hi)
    if not fl<=0<=fh:raise ArithmeticError('root not bracketed')
    for _ in range(n):
        md=(lo+hi)/2
        if fun(md)<0:lo=md
        else:hi=md
    return (lo+hi)/2

def phase(theta,eps):
    period=mp.floor(theta/mp.pi)
    rem=theta-period*mp.pi
    return period*mp.pi+mp.atan2(eps*mp.sin(rem),mp.cos(rem))

def inf_data(R,u):
    R,u=mp.mpf(R),mp.mpf(u); eps=1/mp.sqrt(R); ell=mp.mpf('.5')-u; w=u/eps
    roots=[]
    for target in (mp.pi/2,mp.pi):
        roots.append(bisect(lambda k:ell*k+phase(w*k,eps)-target,mp.mpf(0),2*target))
    k1,k2=roots
    G=R*(k2*k2-k1*k1)
    LB=mp.pi**2/(2*eps*(w+ell)*(w+eps*ell))
    return G,LB,w,w*k1,w*k2

def limit_phase(u):
    u=mp.mpf(u); ratio=u/(mp.mpf('.5')-u)
    tiny=mp.mpf('1e-75')
    return bisect(lambda a:-a*mp.cot(a)-ratio,mp.pi/2+tiny,mp.pi-tiny)

def segment_data(lam,widths,rhos):
    a,b=mp.mpf(0),mp.mpf(1); ints=[]
    for L,rho in zip(widths,rhos):
        k=mp.sqrt(lam*rho); z=k*L; c,s=mp.cos(z),mp.sin(z); d=b/k
        integ=a*a*(L/2+mp.sin(2*z)/(4*k))+d*d*(L/2-mp.sin(2*z)/(4*k))+a*d*s*s/k
        ints.append(integ)
        a,b=a*c+d*s,-k*a*s+b*c
    return a,ints

def main():
    mp.mp.dps=80
    check(F(2888,765)>F(15,4)>3 and 38**2<1500,
          'R8 revised whole-sliver constants','exact rational inequalities',sliver_factor=str(F(2888,765)))
    check(F(20097,5000)>4 and F(2800,999)<3 and F(7,20)/1500<F(1,1000),
          'R8 revised large-w difference margins','exact rational inequalities')
    sn,cs=trig(F(2),80)
    check(sn.hi<F(91,100) and cs.hi<-F(2,5) and F(681,350)<2,
          'R8 continuous B(t)<8 proof constants','exact Taylor bounds and rational comparisons')
    aL=F('2.27651323902643307501655540074525185589672')
    aH=F('2.27651323902643307501655540074525185589673')
    GL,GH=gbox(aL),gbox(aH)
    check(GL.lo>0 and GH.hi<0,'Current T3 root endpoints have opposite signs','exact rational Taylor/Machin',left_G=GL.show(),right_G=GH.show())
    UL,UH=ubox(aL),ubox(aH); U=QI(UL.lo,UH.hi)
    V=(QI(aL,aH)**2-PI**2/4)/U**2
    check(F('0.32992250812006654958')<U.lo<U.hi<F('0.32992250812006654960') and F('24.9438661384324768968')<V.lo<V.hi<F('24.9438661384324769084'),
          'Current T3 public intervals re-enclosed','exact rational interval arithmetic',u=U.show(),value=V.show())
    check((3*PI**2-V).lo>F('4.664947') and (25-V).lo>F('0.0561'),
          'Current T3 strict comparison margins','exact rational interval arithmetic')
    guard=0
    try:QI.of(1)/QI(F(-1),F(1))
    except ZeroDivisionError:guard+=1
    try:check(False,'deliberate-false-candidate','negative control')
    except ArithmeticError:guard+=1
    check(guard==2,'Independent checker rejects false arithmetic candidates','negative controls')
    samples=[]
    for R in ['1','2','1500','1600','100000','100000000']:
        for u in ['0.000000001','0.01','0.1','0.33','0.4999']:
            G,LB,w,t1,t2=inf_data(R,u)
            if not G>LB:raise ArithmeticError('numerical gap lower bound')
            samples.append({'R':R,'u':u,'G':mp.nstr(G,20),'lower':mp.nstr(LB,20)})
    check(True,'Pole-free phase sampling of the new global bound','finite high-precision check; not proof of the whole domain',samples=samples)
    diffs=[]
    for R in ['1500','1000000','100000000']:
        for u in [2/mp.sqrt(mp.mpf(R)),mp.mpf('.2'),mp.mpf('.49')]:
            G,LB,w,t1,t2=inf_data(R,u)
            if w<2-mp.mpf('1e-60'):continue
            a=limit_phase(u); alpha=(mp.mpf('.5')-u)/(mp.mpf(R)*u)
            d1=mp.pi**2/4-t1*t1;d2=a*a-t2*t2
            if not(d1>4*alpha and 0<d2<3*alpha):raise ArithmeticError('large w difference test')
            diffs.append({'R':R,'u':mp.nstr(u,18),'d1/alpha':mp.nstr(d1/alpha,20),'d2/alpha':mp.nstr(d2/alpha,20)})
    check(True,'New large-w difference estimates sampled','finite high-precision check, not universal proof',samples=diffs)

    # Physical F_n includes omega(y)^(-1); normalized matrix avoids that factor.
    C,S,s=sp.symbols('C S s',real=True,nonzero=True)
    J=sp.diag(1,-1)
    Nc=sp.Matrix([[C*C-S*S/s,(s+1)*S*C/s],[-(s+1)*S*C,C*C-s*S*S]])
    Ne=sp.Matrix([[C,S],[-S,C]])
    check(Nc.subs(C,-C)==J*Nc*J and Ne.subs(C,-C)==-J*Ne*J,
          'Correct reflection identity for normalized matrices','symbolic matrix identity')
    def exact_phys(y):
        w=5*y/2;return sp.simplify(sp.sin(y)*(sp.Rational(9,2)*sp.cos(y)**2-2)/w)
    f1,f2=exact_phys(sp.pi/3),exact_phys(2*sp.pi/3)
    check(sp.simplify(f2-f1/2)==0 and sp.simplify(f1-f2)!=0,
          'Unnormalized F reflection theorem is false','exact symbolic counterexample',F_pi_over3=str(f1),F_2pi_over3=str(f2))
    checks=[]
    for sr in [1.2,2.,5.]:
        delta=1/sr; A=(sr+1)**2/sr; B=sr+1/sr; cinf=(np.pi/np.arccos((sr-1)/(sr+1))-1)**2
        vals=[]
        for n in range(1,41):
            mat=np.diag([-delta]+[0.]*(n-1))
            if n>1: mat+=np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1)
            ev=np.linalg.eigvalsh(mat)
            if not (ev[0]>-2 and ev[-1]<2):raise ArithmeticError('Jacobi bounds')
            xn=(B+ev[0])/A; yn=np.arccos(np.sqrt(xn));cn=(np.pi/yn-1)**2
            vals.append(cn)
        checks.append({'s':sr,'c1':vals[0],'c40':vals[-1],'limit':cinf})
        if not(all(vals[j]>vals[j+1] for j in range(len(vals)-1)) and vals[-1]>cinf):raise ArithmeticError('candidate monotonicity')
    check(True,'Balanced candidate monotonicity and limiting value sampled','finite matrix check, universal proof in appendix',examples=checks)

    # Tangency error: avg vector versus integral vector.
    p=sp.pi
    av=sp.Matrix([-3*p*p-2*p,-3*p*p+sp.Rational(2,3)*p])
    integ=sp.diag(sp.Rational(1,4),sp.Rational(3,4))*av
    direction=sp.Matrix([av[1]/(-av[0]),1])
    old=sp.simplify(direction.dot(av)); true=sp.simplify(direction.dot(integ))
    check(old==0 and sp.simplify(true-(-sp.Rational(3,2)*p*p+p/3))==0,
          'Block-average orthogonality is not density tangency','exact symbolic SL counterexample',old_constraint=str(old),true_first_variation=str(true),true_numeric=str(sp.N(true,20)),direction=[str(v) for v in direction])
    edges=list(map(mp.mpf,['0','0.29343444668879154','0.36546070235557726','0.6345392976444227','0.7065655533112085','1']))
    widths=[edges[i+1]-edges[i] for i in range(5)];rhos=list(map(mp.mpf,[1,4,1,4,1]))
    roots=[]; sums=[]
    for guess in ['22.50044205115215','85.59364088540627']:
        g=mp.mpf(guess)
        lam=mp.findroot(lambda l:segment_data(l,widths,rhos)[0],(g-mp.mpf('.005'),g+mp.mpf('.005')))
        end,I=segment_data(lam,widths,rhos)
        mass=sum(r*v for r,v in zip(rhos,I))
        roots.append(lam); sums.append([v/mass for v in I])
    ints=mp.matrix([roots[0]*sums[0][j]-roots[1]*sums[1][j] for j in range(5)])
    avg=mp.matrix([ints[j]/widths[j] for j in range(5)])
    v0=mp.matrix([1,0,0,0,0]);vbad=v0-avg*(mp.fdot(v0,avg)/mp.fdot(avg,avg))
    vgood=v0-ints*(mp.fdot(v0,ints)/mp.fdot(ints,ints))
    badprint=mp.fdot(vbad,avg);badtrue=mp.fdot(vbad,ints)
    check(abs(badprint)<mp.mpf('1e-65') and abs(badtrue)>mp.mpf('.001') and abs(mp.fdot(vgood,ints))<mp.mpf('1e-65'),
          'Source n2 R4 table also exposes false tangency','high-precision recomputation at source decimal configuration; not exact stationarity certification',eigenvalues=[mp.nstr(z,30) for z in roots],wrong_reported=mp.nstr(badprint,20),actual_variation=mp.nstr(badtrue,30),correct_variation=mp.nstr(mp.fdot(vgood,ints),20),block_integrals=[mp.nstr(z,25) for z in ints])

    t,L=sp.symbols('t L',real=True)
    check(sp.diff((1+t)**sp.Rational(-1,2),t).subs(t,0)==-sp.Rational(1,2) and sp.diff(L/(1+t),t,2).subs(t,0)==2*L,
          'Normalized eigenfunction derivative needs the kernel component','exact symbolic counterexample to displayed v equality',source_resolvent_rhs='0 for dr=rho',actual_v='-u/2',lambda_second='2 lambda, consistent with the main formula')
    m,N=sp.symbols('m N',integer=True,positive=True)
    telesc=sp.summation(1/(4*m*(m+1)),(m,1,N))
    check(sp.simplify(telesc-N/(4*(N+1)))==0 and sp.limit(telesc,N,sp.oo)==sp.Rational(1,4),
          'Reduced Green diagonal at the midpoint is finite','exact telescoping identity and symbolic limit',finite_sum=str(telesc),diagonal='1/(2*pi^2)')
    check(sp.simplify(2*p*p*4-2*p**4*(1/p**2)-6*p*p)==0,
          'Normalized narrow bumps have finite lambda1 second-variation limit','exact algebra plus dominated-series proof in appendix',limit='6*pi^2')
    ell=np.arange(2,100001,dtype=float); bumps=[]
    for eta in [.05,.02,.005,.001]:
        Bkl=np.cos((1-ell)*np.pi/2)*np.sinc((1-ell)*eta)-np.cos((1+ell)*np.pi/2)*np.sinc((1+ell)*eta)
        h=1+np.sinc(2*eta)
        val=2*np.pi**2*h*h-2*np.pi**2*np.sum(Bkl**2/(ell**2-1))
        tail=4*np.pi**2*(1/100000+1/100001)
        bumps.append({'eta':eta,'truncated_second_variation':val,'absolute_tail_upper':tail})
    check(all(abs(z['truncated_second_variation'])<100 for z in bumps) and abs(bumps[-1]['truncated_second_variation']-6*np.pi**2)<.4,
          'Narrow-bump finite sums corroborate the finite limit','finite floating-point check with analytical truncation bound',samples=bumps)
    gap_samples=[]
    ls=np.arange(1,100001,dtype=float)
    for eta in [.02,.005,.001]:
        derv=[]
        for k in [1,2]:
            mask=ls!=k; js=ls[mask]
            Bkl=np.cos((k-js)*np.pi/2)*np.sinc((k-js)*eta)-np.cos((k+js)*np.pi/2)*np.sinc((k+js)*eta)
            hk=1-np.cos(k*np.pi)*np.sinc(2*k*eta)
            val=2*k*k*np.pi**2*hk*hk-2*k**4*np.pi**2*np.sum(Bkl**2/(js**2-k*k))
            derv.append(val)
        gap_samples.append({'eta':eta,'Q_half_gap_second':(derv[1]-derv[0])/2})
    check(abs(gap_samples[-1]['Q_half_gap_second']+3*np.pi**2)<.1,
          'The adjacent-gap narrow-bump form also has a finite limit',
          'finite numerical check; analytic limit is -3*pi^2',samples=gap_samples)
    # One moving Heaviside interface: second derivative acts on test functions.
    x,a,h,sig=sp.symbols('x a h sig',real=True)
    primitive=x**3/3
    integral=-sig*primitive.subs(x,a+t*h)
    check(sp.diff(integral,t,2).subs(t,0)==-2*sig*a*h*h,
          'Moving-interface acceleration gives a finite delta-prime term','exact polynomial test identity',pairing='-jump * velocity^2 * test_derivative(interface)')

    out={'head':HEAD,'python':sys.version,'platform':platform.platform(),'optimized':bool(sys.flags.optimize),
         'check_count':len(ROWS),'checks':ROWS,
         'scope':'Independent checks only. No full repository suite or Lean. Exact comparison checks do not by themselves certify the accompanying universal theorems.'}
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('results.json')
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for row in ROWS:print('CONFIRMED:',row['name'])
    print('TOTAL',len(ROWS))
    print('SOURCE CASE ACTUAL FIRST VARIATION:',mp.nstr(badtrue,30))
    print('BUMP CHECKS:',bumps)

if __name__=='__main__':main()
