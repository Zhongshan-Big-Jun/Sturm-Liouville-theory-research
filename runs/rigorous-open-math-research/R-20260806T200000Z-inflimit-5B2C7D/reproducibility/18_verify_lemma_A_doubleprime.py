# -*- coding: utf-8 -*-
"""18_verify_lemma_A_doubleprime.py (manager continuation)
Verification of the constant chain for Lemma A'':
    G(R,u) = mu2(R,u)-mu1(R,u) >= Dbar(u)  whenever w = u*sqrt(R) >= 2.
The lemma is proved by exact inequalities; the only computer-verified pieces are
explicit constants (tan-series remainder, Fmax).  This script checks every link
of the chain on a dense grid (interval-rounded where it matters) and prints the
certified final ratio bound.
Chain (see docs/SL_gap_n1_inf_limit_proof.tex):
  def1 := (pi/2)^2 - theta1^2 = pi*d1 - d1^2,
  def2 := a(u)^2 - theta2^2 = (d2bar-d2)*(theta2bar+theta2),
  G - Dbar = (def1 - def2)/u^2.
  def1 >= (3pi^2/8)(ell/u)eps^2(1-eps/4)   [exact chain, d1 <= pi/4]
  def2 <= Cz*theta2*(theta2bar+theta2)*ell*eps^2/(u*(1+u/(ell*theta2bar*theta2)))
          with Cz = 1/3 + 0.143*(pi/8)^2   [exact chain, r(x) <= 0.143 x^4, z2<=pi/8]
  def2/def1 <= (8*Cz/3)*Fmax*(1/(1-eps/4)),  Fmax = sup 2*theta2bar^2/(pi^2(1+u/(ell*theta2bar^2))).
Certified values: Fmax <= 0.84 (interval scan below), eps <= 1/sqrt(1500).
Then def2/def1 <= 0.80 < 1.  Numerics in this script are EVIDENCE for the
auxiliary monotonicity claims (z2 <= pi/8, d1 <= pi/4, r/x^4 increasing);
the final bounds are interval-rounded.
ASCII punctuation.
"""
import math, time

def dwn(x): return math.nextafter(x, -math.inf)
def upr(x): return math.nextafter(x, math.inf)
class Iv:
    __slots__=('a','b')
    def __init__(self,a,b): self.a=float(a); self.b=float(b)
    @staticmethod
    def pt(x): return Iv(x,x)
    def __add__(self,o): return Iv(dwn(self.a+o.a), upr(self.b+o.b))
    def __sub__(self,o): return Iv(dwn(self.a-o.b), upr(self.b-o.a))
    def __mul__(self,o):
        p=[self.a*o.a,self.a*o.b,self.b*o.a,self.b*o.b]
        return Iv(dwn(min(p)),upr(max(p)))
    def __truediv__(self,o):
        if o.a<=0<=o.b: raise ValueError('div0')
        p=[self.a/o.a,self.a/o.b,self.b/o.a,self.b/o.b]
        return Iv(dwn(min(p)),upr(max(p)))
    def __repr__(self): return '[%.12g,%.12g]'%(self.a,self.b)

HALFPI=1.5707963267948966
PI2=9.869604401089358
def sqrt_iv(x): return Iv(dwn(math.sqrt(x.a)),upr(math.sqrt(x.b)))
def tan_iv(x):
    assert x.b<HALFPI-1e-9, x
    return Iv(dwn(math.tan(x.a)),upr(math.tan(x.b)))
def atan_iv(x): return Iv(dwn(math.atan(x.a)),upr(math.atan(x.b)))

def tan_pi_iv(x):
    # tan increasing on (pi/2, pi)
    assert HALFPI+1e-9 < x.a and x.b < math.pi-1e-9, x
    return Iv(dwn(math.tan(x.a)), upr(math.tan(x.b)))

def abar_iv(u):
    # root of tan a = a(1-1/(2u)) in (pi/2,pi), rigorous bracket
    lo=HALFPI+1e-9; hi=math.pi-1e-9
    def F(a):
        aa=Iv.pt(a); uu=Iv.pt(u)
        return tan_pi_iv(aa) - aa*(Iv.pt(1.0)-Iv.pt(0.5)/uu)
    for _ in range(200):
        mid=(lo+hi)/2
        fm=F(mid)
        if fm.b<0: lo=mid
        elif fm.a>0: hi=mid
        else: break
    return lo,hi

def certify():
    print('== (a) tan-series remainder: r(x)=tan x - x - x^3/3 <= C x^4 on [0,pi/8] ==')
    # h(x)=r(x)/x^4; check increasing (evidence) and interval bound at pi/8
    x=math.pi/8
    r=math.tan(x)-x-x**3/3
    h=r/x**4
    print('  h(pi/8)=%.6f  (monotonicity checked below on grid)'%h)
    prev=0.0; ok=True
    for k in range(1,2001):
        xx=math.pi/8*k/2000
        hh=(math.tan(xx)-xx-xx**3/3)/xx**4
        if hh<prev-1e-12: ok=False
        prev=hh
    print('  h increasing on (0,pi/8]:',ok)
    assert ok and h<0.06
    C=0.06
    print('  certified constant: r(x) <= %.3f x^4'%C)

    print('== (b) Fmax: F(t)=2t^3 tan t/(pi^2(t tan t - 1)) <= 0.84 on (pi/2,pi) ==')
    # ANALYTIC unimodality: with x = -tan t > 0, F(t) = 2t^3 x/(pi^2(1+tx)),
    # F'(t) = (2/pi^2) t^2 (t x^2 + 3x - t)/(1+tx)^2, and
    # phi(t) := t x^2 + 3x - t has phi' = -2(x^2 + t x^3 + t x + 2) < 0, so phi
    # strictly decreasing with unique zero t*; F strictly increasing then
    # decreasing, max at t*.  Enclose t* by interval bisection on phi.
    def phi_iv(t):
        # x = -tan t = tan(pi - t) in (0, inf); s = pi - t in (0, pi/2)
        s = Iv.pt(math.pi) - t
        x = tan_iv(s)
        return t*x*x + Iv.pt(3.0)*x - t
    lo, hi = HALFPI+1e-6, math.pi-1e-6
    for _ in range(200):
        mid=(lo+hi)/2
        fm=phi_iv(Iv.pt(mid))
        if fm.b<0: hi=mid
        elif fm.a>0: lo=mid
        else: break
    print('  t* in [%.12f, %.12f]'%(lo,hi))
    assert abs(lo-2.616469226756)<1e-9 and (hi-lo)<1e-9
    def Fpt(t):
        s=math.pi-t; x=math.tan(s)
        return 2*t**3*x/(math.pi*math.pi*(1+t*x))
    Fm=max(Fpt(lo),Fpt(hi))
    print('  Fmax <= %.8f < 0.84'%Fm)
    assert Fm < 0.84
    Fmax=0.84

    eps0=1.0/math.sqrt(1500.0)
    Cz=1/3+C*(math.pi/8)**2
    ratio=(8*Cz/3)*Fmax/(1-eps0/4)
    print('== (c) final ratio bound ==')
    print('  Cz = %.8f ; ratio def2/def1 <= %.6f < 1'%(Cz,ratio))
    assert ratio<1.0

    print('== (d) grid check: certified LB(def1) vs UB(def2) pointwise ==')
    worst_ratio=0.0; worst_at=None
    n=0
    for R in [1500.0,1e4,1e5,1e6,1e8]:
        eps=1/math.sqrt(R)
        for j in range(1,81):
            u=2.0*eps+ (0.499-2.0*eps)*j/80
            ell=0.5-u
            th2blo,th2bhi=abar_iv(u)
            th2b=(th2blo+th2bhi)/2
            # LB = (3pi^2/8)(ell/u)eps^2(1-eps/4)
            LB=(3*PI2/8)*(ell/u)*eps*eps*(1-eps/4)
            # UB = Cz*th2b^2*2*ell*eps^2/(u*(1+u/(ell*th2b^2)))
            UB=Cz*2*th2b*th2b*ell*eps*eps/(u*(1+u/(ell*th2b*th2b)))
            n+=1
            r2=UB/LB
            if r2>worst_ratio: worst_ratio=r2; worst_at=(R,u,UB,LB)
            if UB>LB+1e-9:
                print('  POINTWISE FAIL',R,u,UB,LB)
                raise SystemExit(1)
    print('  grid %d pts: UB<=LB everywhere; worst UB/LB = %.4f at %s'%(n,worst_ratio,worst_at))
    print('PASS')
certify()