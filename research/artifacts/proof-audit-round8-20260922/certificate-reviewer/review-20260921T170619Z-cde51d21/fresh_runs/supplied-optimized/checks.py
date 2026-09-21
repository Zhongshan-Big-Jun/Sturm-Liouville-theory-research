#!/usr/bin/env python3
"""Independent round-8 audit checks; no repository code is imported.

Sources are identified in source_manifest.json. source05_* and old_cot_box
are minimal transcriptions of the inspected routines, not a repository test
suite. Rational Taylor/Machin bounds establish the reported counterexamples.
Numerical phase checks do NOT prove infinite-index or parameter limits.
Run: python checks.py [output.json]
"""
from __future__ import annotations
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from dataclasses import dataclass
import json
import math
import platform
import sys
from pathlib import Path
import mpmath as mp
from mpmath import iv
import sympy as sp

RESULTS: list[dict] = []

def require(condition: bool, name: str, kind: str, **details) -> None:
    if not bool(condition):
        raise ArithmeticError(f"Check failed: {name}")
    RESULTS.append(dict(name=name, kind=kind, confirmed=True, details=details))

def dec(x: F, up: bool = False, digits: int = 65) -> str:
    with localcontext() as ctx:
        ctx.prec = digits
        ctx.rounding = ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(x.numerator) / Decimal(x.denominator))

@dataclass(frozen=True)
class QI:
    lo: F
    hi: F
    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError('reversed interval')
    @staticmethod
    def of(x):
        return x if isinstance(x, QI) else QI(F(x), F(x))
    def __add__(self, y):
        y=self.of(y); return QI(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self): return QI(-self.hi,-self.lo)
    def __sub__(self,y): return self + (-self.of(y))
    def __rsub__(self,y): return self.of(y) + (-self)
    def __mul__(self,y):
        y=self.of(y); v=[a*b for a in (self.lo,self.hi) for b in (y.lo,y.hi)]
        return QI(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,y):
        y=self.of(y)
        if y.lo<=0<=y.hi: raise ZeroDivisionError('zero in divisor')
        return self*QI(1/y.hi,1/y.lo)
    def __rtruediv__(self,y): return self.of(y)/self
    def __pow__(self,n: int):
        if n<0: return QI.of(1)/(self**(-n))
        if n==0: return QI.of(1)
        if n%2==1: return QI(self.lo**n,self.hi**n)
        lo=F(0) if self.lo<=0<=self.hi else min(self.lo**n,self.hi**n)
        return QI(lo,max(self.lo**n,self.hi**n))
    def display(self): return [dec(self.lo),dec(self.hi,up=True)]

def trig_point(x: F, degree: int = 100) -> tuple[QI,QI]:
    """Taylor polynomials with Lagrange remainder |x|^(N+1)/(N+1)!.
    This is exact rational arithmetic, with no calls to floating trig.
    """
    x=F(x)
    s=sum(((-1)**j*x**(2*j+1)/math.factorial(2*j+1)
           for j in range((degree-1)//2+1)),F(0))
    c=sum(((-1)**j*x**(2*j)/math.factorial(2*j)
           for j in range(degree//2+1)),F(0))
    rem=abs(x)**(degree+1)/math.factorial(degree+1)
    return QI(s-rem,s+rem),QI(c-rem,c+rem)

def atan_small(x: F,n: int) -> QI:
    if not 0<x<1: raise ValueError('requires 0<x<1')
    s=sum(((-1)**j*x**(2*j+1)/(2*j+1) for j in range(n)),F(0))
    sn=s+(-1)**n*x**(2*n+1)/(2*n+1)
    return QI(min(s,sn),max(s,sn))

# Machin identity pi = 16 atan(1/5) - 4 atan(1/239).
PI=16*atan_small(F(1,5),85)-4*atan_small(F(1,239),28)

def mp_fraction(x) -> F:
    sign,man,ex,_=x._mpf_
    return F((-1 if sign else 1)*man)*F(2)**ex

def source05_bracket_root(fun,lo,hi,tol):
    L,H=mp.mpf(lo),mp.mpf(hi)
    fl,fh=fun(L),fun(H)
    if not (fl.b<0 and fh.a>0): raise ArithmeticError('initial bracket')
    while H-L>tol:
        m=(L+H)/2; fm=fun(m)
        if fm.b<0: L=m
        elif fm.a>0: H=m
        else: break
    return L,H

def source05_F_a(a,u):
    uu=mp.mpf(u)
    aa=iv.mpf((mp.mpf(a),mp.mpf(a)))
    return iv.tan(aa)-aa*(1-1/(2*uu))

def source05_a_root(u):
    lo=mp.mpf('1.57079632679489661923132169163975144209858469968755')+mp.mpf('1e-45')
    hi=mp.mpf('3.14159265358979323846264338327950288419716939937511')-mp.mpf('1e-45')
    return source05_bracket_root(lambda a:source05_F_a(a,u),lo,hi,mp.mpf('1e-40'))

def old_cot_box(x: float):
    y=math.cos(x)/math.sin(x)
    return math.nextafter(y,-math.inf),math.nextafter(y,math.inf)

def G_point(x: F) -> QI:
    s,_=trig_point(x,110)
    s2,_=trig_point(2*x,130)
    return 8*x**3*s**2 - PI**2*(2*x-s2)

def u_point(x: F) -> QI:
    s,c=trig_point(x,110)
    return x/(2*(QI.of(x)-s/c))

def main():
    # R8-F01: endpoint choice in 05_interval_value.py.
    mp.mp.dps=50; iv.dps=45
    a_lower,a_upper=source05_a_root(mp.mpf(3)/8)
    al,ah=mp_fraction(a_lower),mp_fraction(a_upper)
    slo,clo=trig_point(al,100); shi,chi=trig_point(ah,100)
    flow=slo/clo+al/3; fhigh=shi/chi+ah/3
    require(flow.hi<0,'05 lower endpoint is strictly below a(3/8)',
            'exact rational Taylor counterexample',a_lower=dec(al),F_bounds=flow.display())
    require(fhigh.lo>0,'05 genuine upper endpoint is above a(3/8)',
            'exact rational Taylor repair check',a_upper=dec(ah),F_bounds=fhigh.display())

    # R8-F02: cot_iv is not guaranteed to be an interval extension.
    x=0.004240726009745246
    lo,hi=old_cot_box(x)
    s,c=trig_point(F.from_float(x),30); qb=c/s
    require(qb.hi<F.from_float(lo),'cot_iv misses its exact point value',
            'exact rational Taylor counterexample',x_hex=x.hex(),x_repr=repr(x),
            returned=[repr(lo),repr(hi)],correct_enclosure=qb.display(),
            gap_lower=dec(F.from_float(lo)-qb.hi))

    tc=3/math.sqrt(2); xx=tc+(math.pi-tc)/500
    vv=-xx*math.cos(xx)/math.sin(xx)
    s,c=trig_point(F.from_float(xx),100); vq=-F.from_float(xx)*(c/s)
    require(F.from_float(vv)>vq.hi,'19 f_cell raw v1 is not an enclosing lower bound',
            'exact rational Taylor counterexample',x=repr(xx),v1=repr(vv),
            true_enclosure=vq.display())
    require(F.from_float(math.pi)<PI.lo,'19 grid ends strictly below mathematical pi',
            'exact rational Machin comparison',pi_float=repr(math.pi))

    # R8-F03: exact witnesses to uncovered strips in the first R-cell.
    R=F(3015,2); Rlo=F(1500); Rhi=F(1515)
    wB=F('0.48743'); threshold=(2*wB/(1-2*wB))**2
    require(Rlo<threshold<R,'16 Region B has an uncovered curved-boundary strip',
            'exact rational comparison',R=str(R),w=str(wB),
            squared_boundary_parameter=dec(threshold))
    wD=F('0.4995815'); b3factor=1/(4*wD*wD)-1
    at_R=PI**2*R*b3factor; at_hi=PI**2*Rhi*b3factor
    require(at_R.hi<25<at_hi.lo,'16 Region D starts above the needed curved boundary',
            'exact rational Machin comparison',R=str(R),w=str(wD),
            B3_at_R=at_R.display(),B3_at_cell_top=at_hi.display())
    require(F('1e-10')<F.from_float(1e-9),'16 Region A explicitly starts at 1e-9, not zero',
            'exact rational domain comparison',w='1e-10',R='1500')
    wt=F('0.4999999995'); Rt=F(10**9)
    val=PI**2*Rt*(1/(4*wt*wt)-1)
    require(wt<F(1,2) and val.hi<25,
            '16 stated analytic D-tail excludes a nonempty wcap<w<1/2 strip',
            'exact rational Machin comparison',R=str(Rt),w=str(wt),B3=val.display())

    # R8-F04: unqualified theta2 branch is false; min-max gives lambda2<=4pi².
    require(2*F(40)*F(1,1600)==F(1,20)<F(1,2),
            'theta2 is at most pi/20 for R=1600,u=1/1600',
            'exact coefficient comparison plus analytic min-max premise')

    # Elementary replacement of the scalar constants in source19.
    sin2,_=trig_point(F(2),80)
    sin23,cos23=trig_point(F(23,10),90)
    require(PI.hi/2<2 and PI.lo>F(23,10) and sin2.hi<F(91,100)
            and sin23.hi<F(3,4) and cos23.hi<-F(3,5)
            and 2*F(23,10)**2*F(91,100)**2<9
            and 2*(F(23,10)*F(3,4))**2<9,
            'elementary three-region replacement for B(t)<=9',
            'exact rational trig bounds plus analytic monotonicity in appendix')
    sqrt2=QI(F('1.414213562373095'),F('1.414213562373096'))
    if not sqrt2.lo**2<2<sqrt2.hi**2: raise ArithmeticError('sqrt2 enclosure')
    x8=PI/8; cz=1/(x8**2)-(1+sqrt2)/x8
    require(cz.hi<F(337,1000),'Cz<0.337 independently certified',
            'exact rational Machin and square-root enclosure',Cz=cz.display())
    rat=F(4)*F(337,1000)*9*F(100046,100000)/(F(3)*F(333,106)*F(156,100)*F(99996,100000))
    require(PI.lo>F(333,106) and PI.lo/2-F(29,2709)>F(156,100)
            and 1-PI.hi**2*F(10,387)**2/192>F(99996,100000)
            and 1/(1-F(45,100000))<F(100046,100000)
            and rat<F(8256,10000),
            'main scalar ratio <0.8256 has exact rational replacement',
            'exact rational inequalities',ratio_upper=dec(rat,up=True))

    # T2 chain: universal symbolic equalities, not sample signs.
    a=sp.symbols('a',real=True)
    uu=a/(2*(a-sp.tan(a)))
    DD=(a*a-sp.pi**2/4)/uu**2
    GG=8*a**3*sp.sin(a)**2-sp.pi**2*(2*a-sp.sin(2*a))
    JJ=4*a**3*sp.cot(a)+6*a*a-sp.pi**2
    KK=-a*a+3*sp.sin(a)**2+sp.Rational(3,2)*a*sp.sin(2*a)
    sexpr=-4*(a-sp.tan(a))**3/(a**3*(2*a-sp.sin(2*a)))*GG
    identities=[sp.diff(JJ,a)-4*a*KK/sp.sin(a)**2,
                sp.diff(GG,a)-4*sp.sin(a)**2*JJ,
                sp.diff(DD,a)/sp.diff(uu,a)-sexpr]
    require(all(sp.trigsimp(z)==0 for z in identities),'T2 three symbolic sign-chain identities',
            'symbolic identities')

    # Independent exact-rational re-enclosure of T3; no source05 routine used.
    AL=F('2.27651323902643307501655540074525185589672')
    AH=F('2.27651323902643307501655540074525185589673')
    gL,gH=G_point(AL),G_point(AH)
    require(gL.lo>0 and gH.hi<0,'T3 root of G bracketed by exact rational trigonometric bounds',
            'exact rational Taylor/Machin enclosure',a=[str(AL),str(AH)],
            G_left=gL.display(),G_right=gH.display())
    ul,uh=u_point(AL),u_point(AH)
    UI=QI(ul.lo,uh.hi)  # u(a) increasing analytically on (pi/2,pi).
    DI=(QI(AL,AH)**2-PI**2/4)/UI**2
    target_u=QI(F('0.32992250812006654958'),F('0.32992250812006654960'))
    target_d=QI(F('24.9438661384324768968'),F('24.9438661384324769084'))
    require(target_u.lo<UI.lo and UI.hi<target_u.hi and
            target_d.lo<DI.lo and DI.hi<target_d.hi,
            'Both displayed T3 enclosures are supported independently',
            'exact rational Taylor/Machin enclosure',u=UI.display(),D=DI.display())
    require(DI.hi<25 and (3*PI**2-DI).lo>F('4.664947'),
            'T3 comparison with 25 and 3pi² survives',
            'exact rational comparison',margin=(3*PI**2-DI).display())

    # Fixed-u expansion: a is limiting odd phase, b=ell/u; no numerical proof.
    a,b,u=sp.symbols('a b u',positive=True)
    theta1_prime=-sp.pi*b/2
    theta2_prime=-a**3*b**3/(3*(1+b+b*b*a*a))
    C=sp.pi**2*b/(2*u*u)-2*a**4*b**3/(3*u*u*(1+b+b*b*a*a))
    require(sp.simplify((2*a*theta2_prime-sp.pi*theta1_prime)/u**2-C)==0,
            'fixed-u 1/R coefficient from implicit phase derivatives', 'symbolic identity')
    m1,ell=sp.symbols('m1 ell',positive=True)
    require(sp.simplify(2*m1*ell/u-(2*m1/u)*ell/3-4*m1*ell/(3*u))==0,
            'coefficient simplifies at the limiting stationary point', 'symbolic identity')

    # Numerical verification of asymptotic scale, explicitly non-certified.
    mp.mp.dps=80
    G=lambda a:8*a**3*mp.sin(a)**2-mp.pi**2*(2*a-mp.sin(2*a))
    ast=mp.findroot(G,(mp.mpf('2.2'),mp.mpf('2.4')))
    ust=ast/(2*(ast-mp.tan(ast))); bst=(mp.mpf('.5')-ust)/ust
    dst=(ast*ast-mp.pi**2/4)/ust**2
    coef=mp.pi**2*(mp.mpf('.5')-ust)/(3*ust**3)
    rows=[]
    for Rint in (10**3,10**4,10**6,10**8):
        R=mp.mpf(Rint); ep=1/mp.sqrt(R)
        E=lambda th:mp.cos(th)*mp.cos(ep*bst*th)-ep*mp.sin(th)*mp.sin(ep*bst*th)
        O=lambda th:mp.sin(th)*mp.cos(ep*bst*th)+mp.cos(th)*mp.sin(ep*bst*th)/ep
        te=mp.findroot(E,(mp.pi/2-mp.mpf('.01'),mp.pi/2))
        to=mp.findroot(O,(ast-mp.mpf('.01'),ast))
        diff=(to*to-te*te)/ust**2-dst
        rows.append(dict(R=Rint,diff=mp.nstr(diff,38),R_diff=mp.nstr(R*diff,38),
                         sqrt_R_diff=mp.nstr(mp.sqrt(R)*diff,38)))
    require(abs(mp.mpf(rows[-1]['R_diff'])-coef)<mp.mpf('2e-7'),
            'large-R phase numerics agree with 1/R coefficient',
            'high-precision numerical evidence, not a limit proof',
            coefficient=mp.nstr(coef,60),rows=rows)

    # Selected regression algebra for newly repaired round7 source.
    require(sp.Rational(40960)**2/sp.Integer(9)**4*sp.Rational(1,16)*sp.Rational(65,144)**3
            ==sp.Rational(7030400000,4782969),
            'round7 exact n=2 Jacobian constant', 'exact rational identity')
    th=sp.symbols('th',real=True)
    ss,cc=sp.symbols('ss cc')
    remainders=[]
    for n in range(1,5):
        ex=sp.sin((2*n+1)*th)-(2*n+1)*sp.sin(th)+4*sp.sin(th)*sum(sp.sin(j*th)**2 for j in range(1,n+1))
        poly=sp.expand(sp.expand_trig(ex)).subs({sp.sin(th):ss,sp.cos(th):cc})
        remainders.append(sp.simplify(sp.rem(poly,ss**2+cc**2-1,ss)))
    require(all(z==0 for z in remainders),
            'round7 Wronskian identity n=1..4 regression',
            'finite polynomial-remainder checks; universal proof read separately')

    output=dict(audit='round8',repository='Zhongshan-Big-Jun/Sturm-Liouville-theory-research',
                commit='d1462eb444938554b17da1db398763b31efb4ef4',
                python=sys.version,platform=platform.platform(),mpmath=mp.__version__,
                sympy=sp.__version__,optimized=bool(sys.flags.optimize),
                confirmed_groups=len(RESULTS),checks=RESULTS,
                limitations=['No repository test suite imported or executed',
                             'No Lean or whole repository verification',
                             'No full repaired sliver certificate was generated',
                             'New asymptotic limit follows from the analytic appendix, not finite checks'])
    out=Path(sys.argv[1] if len(sys.argv)>1 else 'results.json')
    out.write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
    for row in RESULTS: print('CONFIRMED:',row['name'])
    print(f'{len(RESULTS)} groups confirmed; output: {out}')

if __name__=='__main__': main()
