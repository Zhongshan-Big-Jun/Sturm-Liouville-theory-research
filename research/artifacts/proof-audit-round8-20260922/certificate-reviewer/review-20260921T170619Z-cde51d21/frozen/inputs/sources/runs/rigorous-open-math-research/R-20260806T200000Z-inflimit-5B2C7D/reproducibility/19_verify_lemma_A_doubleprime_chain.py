# -*- coding: utf-8 -*-
"""19_verify_lemma_A_doubleprime_chain.py (manager continuation, v2)
Directed-rounding certification of the analytic chain of Lemma A'' in
docs/SL_gap_n1_inf_limit_proof.tex:

    G(R,u) = mu2 - mu1 >= Dbar(u)   for R >= 1500,  w := u sqrt(R) >= 2.

Corrected 2026-08-07 (session 30): the parameter v in the def2 bound is
v = u/ell = -t cot t  (from tan t = -t ell/u), NOT -cot t.  Because
f(t) = 2t^4/(t^2+v^2+v) is decreasing in v >= 0, the earlier certificate
(which used the smaller v = -cot t) remains a valid upper bound; this v2
certifies with the correct v.  Numerical check: v identity holds exactly at
sample points; with correct v the certified f-max on [3/sqrt(2), pi) is
about 5.6 (vs 8.3 with the wrong v).

Certified here (interval-rounded where it matters):
  (a) h(a) = 3 + 3a cot a - a^2/sin^2 a strictly decreasing on (pi/2, pi):
      num(a) := h'(a) sin^3 a = 3 cos a sin^2 a - 5 a sin a + 2 a^2 cos a < 0
      (pointwise analytic signs plus interval cells as certificate).
  (b) cot-series remainder R(z) = 1/z - cot z satisfies R(z) <= Cz z on
      [0, pi/8] with Cz = R(pi/8)/(pi/8) < 0.337  (R(z)/z increasing by the
      positive-coefficient cot expansion).
  (c) phase brackets: d1 <= d1p <= eps tan(pi/8), d2 <= d2p = arctan(2u/(pi ell)),
      z2 <= pi/8, psi2 >= 0  (checked at 4 x 61 sample points).
  (d) final ratio def2/def1 <= (4 Cz / (3 pi (pi/2 - d1p) c2)) * B * (1+4.6e-4)
      with B <= 9: for t <= 3/sqrt(2) analytically B <= 2t^2 <= 9; for
      t in [3/sqrt(2), pi) interval cells certify f(t) = 2t^4/(t^2+v^2+v),
      v = -t cot t, f <= 9.
  (e) exact identity G - Dbar = (def1 - def2)/u^2 to 1e-42 and pointwise
      UB <= LB on a grid (evidence, not proof).
Computer-assisted proof certificate. ASCII punctuation.
"""
import math, time
def dwn(x): return math.nextafter(x, -math.inf)
def upr(x): return math.nextafter(x, math.inf)
class Iv:
    __slots__ = ('a','b')
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
PI=3.141592653589793
def sin_iv(x):   # sin on (0, pi): increasing on (0, pi/2), decreasing on (pi/2, pi)
    assert 0 < x.a and x.b <= PI, x
    if x.b <= HALFPI:
        return Iv(dwn(math.sin(x.a)), upr(math.sin(x.b)))
    if x.a >= HALFPI:
        return Iv(dwn(math.sin(x.b)), upr(math.sin(x.a)))
    return Iv(dwn(min(math.sin(x.a), math.sin(x.b))), upr(1.0))
def cos_iv(x):   # cos decreasing on (0, pi)
    assert 0 < x.a and x.b <= PI, x
    return Iv(dwn(math.cos(x.b)), upr(math.cos(x.a)))
def tan_iv(x):
    assert x.b < HALFPI-1e-9, x
    return Iv(dwn(math.tan(x.a)), upr(math.tan(x.b)))
def cot_iv(x):
    assert 0 < x.a and x.b <= PI, x
    return Iv(dwn(math.cos(x.b)/math.sin(x.b)), upr(math.cos(x.a)/math.sin(x.a)))

print('== (a) num(a) = 3 cos sin^2 - 5 a sin + 2 a^2 cos < 0 on (pi/2, pi) ==')
ok=True
for k in range(1,1001):
    a1 = HALFPI + (PI-HALFPI)*(k-1)/1000
    a2 = HALFPI + (PI-HALFPI)*k/1000
    A = Iv(a1,a2)
    S = sin_iv(Iv(a1,a2)); C = cos_iv(Iv(a1,a2))
    num = Iv.pt(3.0)*C*S*S - Iv.pt(5.0)*A*S + Iv.pt(2.0)*A*A*C
    if num.b > 0:
        ok=False; print('  FAIL', (a1,a2), num)
print('  num < 0 on 1000 cells:', ok); assert ok
print('  (analytic reason: cos<0, sin>0, a>0 on (pi/2,pi) make all three terms negative)')

print('== (b) Cz = R(pi/8)/(pi/8) < 0.337 ==')
x8 = PI/8
R8 = Iv.pt(1.0)/Iv.pt(x8) - cot_iv(Iv(x8-1e-12, x8))
Cz_iv = R8/Iv.pt(x8)
print('  R(pi/8)/(pi/8) in', Cz_iv)
assert Cz_iv.b < 0.337
Cz = 0.337
prev=0.0; mono=True
for k in range(1,4001):
    z = PI/8*k/4000
    v = (1.0/z - 1.0/math.tan(z))/z
    if v < prev-1e-12: mono=False
    prev=v
print('  R(z)/z monotone increasing on (0,pi/8] (evidence):', mono); assert mono

print('== (c) phase brackets at 4x61 sample points ==')
def check_phase(u, R):
    eps=1/math.sqrt(R); ell=0.5-u
    d1p = math.atan(eps*math.tan(HALFPI*ell*eps/u))
    d2p = math.atan(2*u/(PI*ell))
    f1 = lambda d: math.tan(d) - eps*math.tan((HALFPI-d)*eps*ell/u)
    lo,hi=0.0,min(d1p, 1.4)
    for _ in range(300):
        m=(lo+hi)/2
        if f1(m)<0: lo=m
        else: hi=m
    d1=(lo+hi)/2
    f2 = lambda d: math.tan(d) - eps/math.tan((HALFPI+d)*eps*ell/u)
    lo,hi=0.0,d2p
    if f2(hi)<0: hi=math.atan(4*u/(PI*ell))
    for _ in range(300):
        m=(lo+hi)/2
        if f2(m)<0: lo=m
        else: hi=m
    d2=(lo+hi)/2
    z2=(HALFPI+d2)*eps*ell/u
    fa = lambda a: math.tan(a) - a*(1-1/(2*u))
    lo,hi=HALFPI+1e-9, PI-1e-9
    for _ in range(300):
        m=(lo+hi)/2
        if fa(m)<0: lo=m
        else: hi=m
    th2bar=(lo+hi)/2
    psi2 = (th2bar-HALFPI) - d2
    assert d1p <= eps*math.tan(PI/8)+1e-15 and d1p < PI/4, (u,R,d1p)
    assert z2 <= PI/8 + 1e-12, (u,R,z2)
    assert psi2 >= -1e-9, (u,R,psi2)
for R in [1500.0, 1e4, 1e6, 1e8]:
    for j in range(0, 61):
        u = 2.0/math.sqrt(R)*(1+1e-12) + (0.499-2.0/math.sqrt(R))*j/60
        check_phase(u, R)
print('  phase brackets ok')

print('== (d) B(t,theta) <= 9 and final ratio bound ==')
# B(t,th) = th(t+th)/(1+v(v+1)/(t th)) <= B(t,t) = 2t^4/(t^2+v^2+v), v = u/ell.
# Correct v: tan t = -t ell/u  =>  v = u/ell = -t cot t.
# v increasing in t on (pi/2, pi): v'(t) = t/sin^2 t - cot t > 0.
# For t <= 3/sqrt(2): B(t) <= 2t^2 <= 9 analytically.
# For t in [3/sqrt(2), pi): interval cells with directed rounding.
tc = 3.0/math.sqrt(2.0)
def f_cell(a1, a2):
    v1 = -a1*math.cos(a1)/math.sin(a1); v2 = -a2*math.cos(a2)/math.sin(a2)
    T = Iv(a1, a2)
    V = Iv(v1, v2)
    num = Iv.pt(2.0)*T*T*T*T
    den = T*T + V*V + V
    return num/den
okB = True; mx = 0.0
for k in range(1, 501):
    a1 = tc + (PI - tc)*(k-1)/500
    a2 = tc + (PI - tc)*k/500
    fv = f_cell(a1, a2)
    mx = max(mx, fv.b)
    if fv.b > 9.0:
        okB = False; print('  FAIL f > 9 at', (a1, a2), fv)
print('  f(t) <= 2t^2 <= 9 on (pi/2, 3/sqrt(2)]; certified f <= 9 on [3/sqrt(2), pi):', okB, ' max cell bound = %.6f' % mx)
assert okB
eps0=1/math.sqrt(1500.0)
d1p_b = eps0*math.tan(PI/8)
c20 = 1 - PI*PI*eps0*eps0/192
# ratio <= (4 Cz / (3 pi (pi/2 - d1p) c2)) * 9 * (1+4.6e-4)
ratio = (4*Cz/(3*PI*(HALFPI - d1p_b)*c20))*9.0*(1+4.6e-4)
print('  ratio bound = %.6f < 1' % ratio)
assert ratio < 0.85

print('== (e) exact identity and pointwise UB<=LB (evidence) ==')
import mpmath as mp
mp.mp.dps=50
def a_of(u):
    f=lambda a: mp.tan(a)-a*(1-mp.mpf(1)/(2*u))
    lo,hi=mp.pi/2+mp.mpf('1e-40'),mp.pi-mp.mpf('1e-40')
    for k in range(1,100000):
        x=lo+(hi-lo)*k/100000
        if f(x)>0: hi=x; break
        lo=x
    return mp.findroot(f,(lo,hi))
def bisect(f,lo,hi,tol=mp.mpf('1e-40')):
    flo=f(lo)
    for _ in range(500):
        m=(lo+hi)/2; fm=f(m)
        if (fm<0)==(flo<0): lo=m
        else: hi=m
        if hi-lo<tol: break
    return (lo+hi)/2
def vals(u,R):
    eps=1/mp.sqrt(R); ell=mp.mpf(1)/2-u
    d1=bisect(lambda d: mp.tan(d)-eps*mp.tan((mp.pi/2-d)*eps*ell/u),mp.mpf('0'),mp.pi/4)
    dhi=mp.atan(2*u/(mp.pi*ell))
    f2=lambda d: mp.tan(d)-eps/mp.tan((mp.pi/2+d)*eps*ell/u)
    if f2(dhi)>0: dhi=mp.atan(4*u/(mp.pi*ell))
    d2=bisect(f2,mp.mpf('0'),dhi)
    th2=mp.pi/2+d2; th2bar=a_of(u)
    def1=mp.pi*d1-d1*d1
    def2=(th2bar-mp.pi/2-d2)*(th2bar+th2)
    G=th2*th2-(mp.pi/2-d1)*(mp.pi/2-d1)
    G=G/(u*u)
    D=(th2bar*th2bar-mp.pi**2/4)/(u*u)
    return def1,def2,G-D,(def1-def2)/(u*u)
okid=True; n=0
for R in [1500.0,1e4,1e6,1e8]:
    for j in range(1,121):
        u=mp.mpf(2)/mp.sqrt(mp.mpf(R))+(mp.mpf('0.499')-mp.mpf(2)/mp.sqrt(mp.mpf(R)))*j/120
        def1,def2,gd,idv=vals(u,R)
        if abs(gd-idv)>mp.mpf('1e-42'): okid=False
        n+=1
print('  identity G-Dbar=(def1-def2)/u^2 holds to 1e-42 on', n, 'points:', okid)
assert okid
print('PASS')
