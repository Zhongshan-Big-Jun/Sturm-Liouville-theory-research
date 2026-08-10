# -*- coding: utf-8 -*-
"""H3 v56: (A) verify s-recurrence exactly for even u,v; (B) test whether the
odd homogeneous z-recurrence has an explicit solution z^o_j = prod(1+alpha/k),
find alpha; (C) high-precision gamma_u, gamma_v for even, check gamma_u/gamma_v = c/2."""
from fractions import Fraction as F
import math

C=F(3)
lam=F(4)/C

def a1(j,c,par):
    if par=='e':
        P=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    else:
        P=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
    return P/(c*c*j*j*(F(4)/c))
def a2(j,c,par):
    if par=='e':
        Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    else:
        Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
    return -Q/(c*c*j*j*(j-1)*(j-1)*(F(4)/c)**2)
def a3(j,c,par):
    if j<3: return F(0)
    if par=='e':
        R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*(F(4)/c)**3)

def solve_hm(cF,par,N,nu1):
    c=cF; nu=[F(0)]*(N+1); nu[1]=F(nu1)
    for j in range(2,N+1):
        rhs=(F(8)*c*j*j-(F(4) if par=='e' else -F(4))*c*j+c*c*F(j,j-1))*nu[j-1]
        if par=='e':
            Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
        else:
            Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
        rhs-=Q*nu[j-2]
        if j>=3:
            if par=='e':
                R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
            else:
                R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
            rhs+=R*nu[j-3]
        nu[j]=rhs/(c*c)
    return nu
def zof(nu,N):
    return [nu[j]/F(math.factorial(j))**2/lam**j for j in range(N+1)]

# (A) s-recurrence for even u
N=80
u=solve_hm(C,'e',N,F(1))
z=zof(u,N)
E=[F(1)]*(N+1)
for j in range(1,N+1): E[j]=E[j-1]*(F(1)+F(1)/(F(2)*j))
r=[z[j]/E[j] for j in range(N+1)]
s=[r[j]-r[j-1] for j in range(1,N+1)]
def Y(j,par):
    Ej=E[j]; Ej1=E[j-1]
    return a2(j,C,par)/(Ej*Ej1)
def Z(j,par):
    return a3(j,C,par)/(E[j]*E[j-1]*E[j-2])
def A(j,par): return -(Y(j,par)+Z(j,par))
def B(j,par): return -Z(j,par)
ok=True
for j in range(3,N+1):
    lhs=s[j]
    rhs=A(j,'e')*s[j-1]+B(j,'e')*s[j-2]
    if lhs!=rhs:
        ok=False; print("  s-rec FAIL at j=%d: %s vs %s"%(j,lhs,rhs)); break
print("(A) even u: s-recurrence exact for j=3..%d: %s"%(N,ok))

# (B) odd explicit solution search: E_j(a) = 1+a/j, test identity
def odd_resid(a,j):
    Ej=F(1)+a/F(j); Ejm1=F(1)+a/F(j-1); Ejm2=F(1)+a/F(j-2)
    return a1(j,C,'o') + a2(j,C,'o')/Ejm1 + a3(j,C,'o')/(Ejm1*Ejm2) - Ej
print("(B) odd identity residual for E_j = 1+a/j, a in 1..12:")
for a in range(1,13):
    res=[odd_resid(F(a),j) for j in range(4,12)]
    if all(x==0 for x in res):
        print("   a=%d: EXACT ZERO for j=4..11"%a)
    elif all(x!=0 for x in res):
        print("   a=%d: nonzero (min |res| %.2e)"%(a,min(abs(float(x)) for x in res)))
    else:
        print("   a=%d: MIXED zeros at %s"%(a,[j for j,x in zip(range(4,12),res) if x==0]))

# (B2) odd explicit E'_j = 1 + alpha/(2j-1)?
def odd_resid2(alpha_num,alpha_den,j):
    a=F(alpha_num,alpha_den)
    Ej=F(1)+a/F(2*j-1); Ejm1=F(1)+a/F(2*j-3); Ejm2=F(1)+a/F(2*j-5)
    return a1(j,C,'o') + a2(j,C,'o')/Ejm1 + a3(j,C,'o')/(Ejm1*Ejm2) - Ej
for (n,d) in ((1,1),(1,2),(3,2),(1,3)):
    res=[odd_resid2(n,d,j) for j in range(5,12)]
    if all(x==0 for x in res):
        print("   E=1+%d/(2j-1): EXACT ZERO for j=5..11"%(float(F(n,d))))
    else:
        print("   E=1+%d/(2j-1): nonzero min %.2e"%(float(F(n,d)),min(abs(float(x)) for x in res)))

# (C) gamma limits for even: gamma_u = lim r_j? compute r_N high precision
from decimal import Decimal as D, getcontext
getcontext().prec = 60
Nc=200
uc=solve_hm(C,'e',Nc,F(1))
vc=solve_hm(C,'e',Nc,F(0)) # nu1=0 -> identically? need D=1 forcing instead
zc=zof(uc,Nc)
Ec=[F(1)]*(Nc+1)
for j in range(1,Nc+1): Ec[j]=Ec[j-1]*(F(1)+F(1)/(F(2)*j))
rc=[D(zc[j].numerator)/D(zc[j].denominator)/ (D(Ec[j].numerator)/D(Ec[j].denominator)) for j in range(Nc+1)]
print("(C) even u: r_100=%.12f r_150=%.12f r_200=%.12f"%(float(rc[100]),float(rc[150]),float(rc[200])))
