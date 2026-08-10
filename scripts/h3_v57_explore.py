# -*- coding: utf-8 -*-
"""H3 v57: comprehensive structural exploration (exact rational where possible).
(1) odd explicit solution search: e_j = 1 + beta/j, and e_j = 1 + beta/(2j-1)-type.
(2) mode constants: A=lim u/sqrt(j), B=lim v/sqrt(j), gamma=lim sqrt(j)*z^w (w=u-(c/2)v).
(3) ratio u/v -> c/2 and monotonicity.
(4) minimal solution h* (backward iteration, exact): h*_0 != 0; moment decay exponent.
(5) corrected s-recurrence (reduced 2nd-order) exact check for j>=3."""
from fractions import Fraction as F
import math
from decimal import Decimal as D, getcontext
getcontext().prec = 50

def coeffs(c, j, par):
    if par=='e':
        Pm=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
        Qm=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
        Rm=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Tm=F(4)*j*(4*j-5)
    else:
        Pm=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
        Qm=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
        Rm=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        Tm=F(4)*j*(4*j-3)
    lam=F(4)/c
    a1=Pm/(c*c*j*j*lam)
    a2=-Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3=(Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
    return a1,a2,a3,lam,Tm

def solve(cF, par, N, nu1, D):
    c=cF; lam=F(4)/c; nu=[F(0)]*(N+1); nu[1]=F(nu1)
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs(c,j,par)
        src=Tm*D/(c*c*F(math.factorial(j))**2*lam**j)
        nu[j]=a1*nu[j-1]+a2*nu[j-2]+(a3*nu[j-3] if j>=3 else F(0))+src
    return nu

def zof(nu,N):
    lam=F(4)/3 if False else None
    return nu

def solve_z(cF,par,N,z1,D):
    """solve directly in z-scale (z_j = nu_j/(j!^2 lam^j))."""
    c=cF; lam=F(4)/c; z=[F(0)]*(N+1); z[1]=F(z1)
    for j in range(2,N+1):
        a1,a2,a3,lam,Tm=coeffs(c,j,par)
        src=Tm*D/(c*c*F(math.factorial(j))**2*lam**j)
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else F(0))+src
    return z

# ---------- (1) odd explicit solution search ----------
print("(1) odd explicit solution search (identity: e_j = a1 + a2/e_{j-1} + a3/(e_{j-1}e_{j-2}))")
C=F(3)
def resid_even(e,j,c):
    if e(j-2)==0 or e(j-1)==0: return F(0)
    a1,a2,a3,lam,Tm=coeffs(c,j,'e')
    return a1+a2/e(j-1)+a3/(e(j-1)*e(j-2))-e(j)
def resid_odd(e,j,c):
    if e(j-2)==0 or e(j-1)==0: return F(0)
    a1,a2,a3,lam,Tm=coeffs(c,j,'o')
    return a1+a2/e(j-1)+a3/(e(j-1)*e(j-2))-e(j)
# even reference: e(j)=1+1/(2j)
ee=lambda j: F(1)+F(1)/(F(2)*j)
print("   even e=1+1/(2j): all zero j=3..40:", all(resid_even(ee,j,C)==0 for j in range(3,41)))
# odd candidates
def test_odd_e(name, e, J=range(4,41)):
    z=[resid_odd(e,j,C) for j in J]
    return name, all(x==0 for x in z), min(abs(float(x)) for x in z) if any(x!=0 for x in z) else 0.0
cands=[]
for beta_num in range(-5,13):
    cands.append(test_odd_e("1+%d/j"%beta_num, (lambda b: (lambda j: F(1)+F(b)/F(j)))(beta_num)))
for beta_num in range(1,9):
    cands.append(test_odd_e("1+%d/(2j-1)"%beta_num, (lambda b: (lambda j: F(1)+F(b)/F(2*j-1)))(beta_num)))
    cands.append(test_odd_e("1+%d/(2j+1)"%beta_num, (lambda b: (lambda j: F(1)+F(b)/F(2*j+1)))(beta_num)))
for name,ok,res in cands:
    if ok: print("   ODD EXPLICIT FOUND:", name)
    elif res < 1e-6: print("   %s: small residual %.2e"%(name,res))
print("   (nonzero candidates min residual shown above; nothing with exact zero => no simple 1+beta/j odd solution)")

# ---------- (2)(3) mode constants, both parities ----------
print()
print("(2) mode constants (float128 via mpmath precision 50):")
from mpmath import mp, mpf, sqrt, log, factorial, fabs
mp.dps = 40
for par in ('e','o'):
    for c in (1,3,10):
        N=4000
        z1 = mpf(1)/mpf(4/c) if False else 1  # z1=1 means nu1=lam
        u=solve_z(F(c),par,N,F(1),F(0)); v=solve_z(F(c),par,N,F(0),F(1))
        w=[u[j]-F(c,2)*v[j] for j in range(N+1)]
        def l(x):
            return mpf(x.numerator)/mpf(x.denominator)
        m=3000
        Au=l(u[m])/mp.sqrt(m); Bv=l(v[m])/mp.sqrt(m)
        Gw=l(w[m])*mp.sqrt(m)
        ruv=l(u[m])/l(v[m])
        # u/v monotone?
        mono=True
        prev=float(l(u[20])/l(v[20]))
        for j in range(21,min(400,N)):
            cur=float(l(u[j])/l(v[j]))
            if cur>prev: mono=False; break
            prev=cur
        print("   par=%s c=%d: A=u/sqrt(j)=%.8f  B=v/sqrt(j)=%.8f  gamma=sqrt(j)*z^w=%.8f  u/v=%.8f (c/2=%s) mono_decreasing:%s"
              %(par,c,float(Au),float(Bv),float(Gw),float(ruv),str(F(c,2)),mono))

# ---------- (4) minimal solution h* ----------
print()
print("(4) minimal solution h* (exact backward iteration):")
def backward_min(cF,par,M):
    c=cF; lam=F(4)/c
    r=[F(1),F(0),F(0)]  # (z_{M}, z_{M-1}, z_{M-2})
    for j in range(M,3,-1):
        a1,a2,a3,lam,Tm=coeffs(c,j,par)
        newv=(r[0]-a1*r[1]-a2*r[2])/a3
        r=[r[1],r[2],newv]
    return [r[2],r[1],r[0]]  # (z0,z1,z2)
for par in ('e','o'):
    for c in (1,3,10):
        z0,z1,z2=backward_min(F(c),par,1500)
        print("   par=%s c=%d: h*: z1/z0=%.12f z2/z0=%.12f z0=%s"%(par,c,float(z1/z0),float(z2/z0),str(z0)))

# ---------- (5) corrected s-recurrence ----------
print()
print("(5) corrected reduced 2nd-order s-recurrence (even, j>=3):")
c=F(3); N=60; par='e'
E=[F(1)]*(N+1)
for j in range(1,N+1): E[j]=E[j-1]*(F(1)+F(1)/(F(2)*j))
for (name,nu1,D) in (("u",1,0),("v",0,1)):
    z=solve_z(c,par,N,nu1,D) if False else None
    # need nu-scale -> z-scale: z1 = nu1/lam
    lam=F(4)/c
    zz=solve_z(c,par,N,F(nu1)/lam,D)
    r=[zz[j]/E[j] for j in range(N+1)]
    s=[r[j]-r[j-1] for j in range(1,N+1)]
    def beta(j):  # 1/(e_j e_{j-1})
        return F(1)/((F(1)+F(1)/(F(2)*j))*(F(1)+F(1)/(F(2)*(j-1))))
    def gamma(j): # 1/(e_j e_{j-1} e_{j-2})
        return F(1)/((F(1)+F(1)/(F(2)*j))*(F(1)+F(1)/(F(2)*(j-1)))*(F(1)+F(1)/(F(2)*(j-2))))
    ok=True; bad=None
    for j in range(3,N+1):
        a1,a2,a3,lam,Tm=coeffs(c,j,par)
        b2=beta(j); b3=gamma(j)
        Aj=-(a2*b2+a3*b3); Bj=-a3*b3
        if s[j]!=Aj*s[j-1]+Bj*s[j-2]:
            ok=False; bad=j; break
    print("   %s: s-recurrence exact j=3..%d: %s %s"%(name,N,ok,"" if ok else ("FAIL at j=%d"%bad)))
