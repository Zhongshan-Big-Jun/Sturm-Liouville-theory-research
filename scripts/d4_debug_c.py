# -*- coding: utf-8 -*-
"""Debug (C) s-recurrence: compare with original h3_v56 logic exactly."""
from fractions import Fraction as F
import math

C = F(3); lam = F(4)/C
N = 80

def a1(j,c,par):
    if par=='e': P=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    else:        P=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
    return P/(c*c*j*j*lam)
def a2(j,c,par):
    if par=='e': Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    else:        Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j,c,par):
    if j<3: return F(0)
    if par=='e': R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:        R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

# replicate h3_v56 exactly
def solve_hm(cF,par,N,nu1):
    c=cF; nu=[F(0)]*(N+1); nu[1]=F(nu1)
    for j in range(2,N+1):
        rhs=(F(8)*c*j*j-(F(4) if par=='e' else -F(4))*c*j+c*c*F(j,j-1))*nu[j-1]
        if par=='e': Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
        else:        Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
        rhs-=Q*nu[j-2]
        if j>=3:
            if par=='e': R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
            else:        R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
            rhs+=R*nu[j-3]
        nu[j]=rhs/(c*c)
    return nu

def zof(nu,N):
    return [nu[j]/F(math.factorial(j))**2/lam**j for j in range(N+1)]

for par in ('e','o'):
    u = solve_hm(C,par,N,F(1))
    z = zof(u,N)
    E=[F(1)]*(N+1)
    beta = 1 if par=='e' else 3
    for j in range(1,N+1): E[j]=E[j-1]*(F(1)+F(beta)/(F(2)*j))
    r=[z[j]/E[j] for j in range(N+1)]
    s=[r[j]-r[j-1] for j in range(1,N+1)]
    def Y(j): return a2(j,C,par)/(E[j]*E[j-1])
    def Z(j): return a3(j,C,par)/(E[j]*E[j-1]*E[j-2])
    def A(j): return -(Y(j)+Z(j))
    def B(j): return -Z(j)
    ok=True
    for j in range(3,N+1):
        lhs=s[j]; rhs=A(j)*s[j-1]+B(j)*s[j-2]
        if lhs!=rhs:
            ok=False
            if j<=6:
                print(f"  par={par} j={j}: lhs={float(lhs):.6e} rhs={float(rhs):.6e} | s[j]={float(s[j]):.6e} A={float(A(j)):.4f} B={float(B(j)):.4f} s[j-1]={float(s[j-1]):.4f} s[j-2]={float(s[j-2]):.4f}")
            break
    print(f"  par={par}: s-recurrence (exact replication) = {ok}")
    # also verify z itself solves the z-recurrence
    okz = all(z[j]==a1(j,C,par)*z[j-1]+a2(j,C,par)*z[j-2]+(a3(j,C,par)*z[j-3] if j>=3 else F(0)) for j in range(2,N+1))
    print(f"    z solves z-recurrence: {okz}; E solves z-recurrence: {all(E[j]==a1(j,C,par)*E[j-1]+a2(j,C,par)*E[j-2]+(a3(j,C,par)*E[j-3] if j>=3 else F(0)) for j in range(2,N+1))}")
