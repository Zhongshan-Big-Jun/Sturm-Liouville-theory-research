# -*- coding: utf-8 -*-
"""H3 v47: derive exact ODE for G(z)=sum_{n>=0} nu_n z^n from the polynomial
coefficient recurrence.  L(G) = RHS(z; D) + init corrections.
All exact rational arithmetic (c=3)."""
from fractions import Fraction as F

C = F(3)

def Pmul(a,b):
    r=[F(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            r[i+j]+=ai*bj
    return r
def Padd(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0))
    return r
def Psub(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))-(b[i] if i<len(b) else F(0))
    return r
def Pscal(a,s):
    return [s*x for x in a]
def Pshift(a,s):  # p(n+s) as polynomial in n
    # p(n+s) = sum_k a_k (n+s)^k ; expand via repeated (n+s)
    out=[F(0)]
    for k,ak in enumerate(a):
        base=[F(1)]
        for _ in range(k):
            base=Pmul(base,[s,F(1)])
        out=Padd(out,Pscal(base,ak))
    return out

c=C
q0 = [-c*c, c*c]
q1 = [F(0), -(4*c+c*c), 12*c, -8*c]
q2 = [F(0), F(12)+F(12)*c, -(F(56)+F(20)*c), F(92)+F(8)*c, -F(64), F(16)]
q3 = [F(0), -F(120), F(308), -F(284), F(112), -F(16)]
qrhs = [F(0), F(20), -F(36), F(16)]

# powers of (z d/dz): theta^k G in terms of derivatives G^(j)
# theta^k G = sum_j S(k,j) z^j G^(j)  (Stirling numbers of 2nd kind)
from math import factorial
def stirling2(k,j):
    s=F(0)
    for i in range(j+1):
        s += ((-1)**(j-i))*F(factorial(j),factorial(i)*factorial(j-i))*F(i)**k
    return s
# theta^k in terms of derivatives: theta^k = sum_{j=0}^k S(k,j) z^j D^j
def theta_k_coeffs(k):
    return [stirling2(k,j) for j in range(k+1)]  # coeff of z^j G^(j)

# represent G^{(j)} as a "basis index j"; an ODE term is (poly in z)*(G^(j)).
# We accumulate ODE as dict: (j, deg) -> coeff, i.e., list of poly coeffs per j.
DEG = 12  # max z-degree we track
def term_add(ode, j, poly):
    # poly: list of coeffs (z^deg)
    if j not in ode: ode[j]=[F(0)]*DEG
    for d,val in enumerate(poly):
        if d<DEG: ode[j][d]+=val

# contribution of sum_{m>=M} p(m) nu_m z^m : p(m) = sum_k a_k m^k
def sum_poly_M(p, M):
    # returns (dict j->poly(z)) for theta form + constant corrections (dict m->val not needed
    # since we know nu_0=0, nu_1 free): we handle corrections by subtracting m<M terms.
    out={}
    for k,ak in enumerate(p):
        tk = theta_k_coeffs(k)
        for j,S in enumerate(tk):
            term_add(out, j, Pscal([S],ak))
    # corrections: subtract sum_{m=0}^{M-1} p(m) nu_m z^m  (as constant terms per z^m)
    # we store corrections as dict m->value added to z^m G^0
    corr={}
    for m in range(0,M):
        val=polyval(p,m)
        if val!=0:
            corr[m]=corr.get(m,F(0))-val
    return out, corr

def polyval(p,n):
    return sum(p[k]*F(n)**k for k in range(len(p)))

ode={}   # j -> list of z-poly coeffs
corr={}  # m -> extra coefficient for z^m (constant term in G)
# accumulate in order: ode_j(z) * G^(j); final equation: sum_j ode_j G^(j) = RHS(z) + corr(z)

def add_sum(zpower, pshift, M, extra_shift_power=0):
    """add z^(zpower) * sum_{m>=M} pshift(m) nu_m z^m"""
    d, cor = sum_poly_M(pshift, M)
    for j,poly in d.items():
        poly2 = Pscal(poly, F(1))  # shifted by zpower
        # multiply by z^zpower: shift degrees
        poly3=[F(0)]*DEG
        for dd,vv in enumerate(poly):
            if dd+zpower<DEG: poly3[dd+zpower]+=vv
        term_add(ode, j, poly3)
    for m,val in cor.items():
        corr[m+zpower]=corr.get(m+zpower,F(0))+val

# k=0: sum_{n>=2} q0(n) nu_n z^n ; q0(m) for m>=2
add_sum(0, q0, 2)
# k=1: z * sum_{m>=1} q1(m+1) nu_m z^m
add_sum(1, Pshift(q1,1), 1)
# k=2: z^2 * sum_{m>=0} q2(m+2) nu_m z^m
add_sum(2, Pshift(q2,2), 0)
# k=3: z^3 * sum_{m>=0} q3(m+3) nu_m z^m
add_sum(3, Pshift(q3,3), 0)

# RHS: D * sum_{n>=2} qrhs(n) z^n  (pure series)
rhs={}
for n in range(2,30):
    rhs[n]=polyval(qrhs,n)
rhs[2] = rhs.get(2,F(0)) + 0  # nothing

print("ODE order info: max j with nonzero coeff:")
for j in sorted(ode):
    poly=ode[j]
    deg=max(d for d in range(DEG) if poly[d]!=0)
    print("  G^(%d): degree %d : %s" % (j, deg, " ".join("%s z^%d"%(poly[d],d) for d in range(deg+1) if poly[d]!=0)))

# corrections (from nu_0=0, nu_1=nu1) contribute: corr[m] z^m for m in corr (times nu_1?)
# nu_1 appears only through m=1 in the M=1 or 2 sums: the correction terms involve nu_1 (free).
print()
print("corrections corr[m] (these multiply nu_1 or nu_0):")
for m in sorted(corr):
    print("  m=%d: %s" % (m, corr[m]))
