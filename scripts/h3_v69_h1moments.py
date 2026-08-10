# -*- coding: utf-8 -*-
"""H3 v69: decisive verification of the H1-moment (M_k) route.
Claim: (w, K_c p_n)_1 = 0  =>  M_k := (w, x^k)_1 satisfy the SAME 2nd-order
recurrence as the H2 case: c M_{2m} = A_m M_{2m-2} - B_m M_{2m-4}, and
|M_{2m}| = |2m int w' x^{2m-1} + c mu_{2m}| <= C sqrt(m).  Growth lemma gives
|M_{2m}| >= |M_2| (4/c)^{m-1} m! -- contradiction unless M_2 = 0.
Also checks H1-projections of x^2, x^3 onto span{K_c p_n} decay super-fast.
"""
from fractions import Fraction as F
import math

def ev(p, x): return sum(a*x**k for k, a in enumerate(p))
def deriv(p): return [F(k)*p[k] for k in range(1, len(p))]
def l2(p, q):
    n = max(len(p), len(q))
    P = list(p)+[F(0)]*(n-len(p)); Q = list(q)+[F(0)]*(n-len(q))
    return sum(P[j]*Q[k]*F(2, j+k+1) for j in range(n) for k in range(n) if (j+k)%2==0)
def h1(p, q, c):
    Dp = ev(p,F(1))-ev(p,F(-1)); Dq = ev(q,F(1))-ev(q,F(-1))
    return -F(1,2)*Dp*Dq + l2(deriv(p), deriv(q)) + c*l2(p, q)
def kc(p, c):
    n = len(p)-1; out=[F(0)]*(n+1)
    for j in range(n+1):
        out[j] += c*p[j]
        if j+2 <= n: out[j] -= F((j+1)*(j+2))*p[j+2]
    return out
def A_e(m,c): return F(2)*m*(2*m-1) + c*F(m, m-1)
def B_e(m,c): return F(2)*m*(2*m-3)
def A_o(m,c): return F(2)*m*(2*m+1) + c*F(m, m-1)
def B_o(m,c): return F(2)*m*(2*m-1)

print("=== 1. exact H1-moment recurrence for polynomial test w, c=3 ===")
c=F(3)
for wname, w in (("x^2",[F(0),F(0),F(1)]), ("x^3",[F(0),F(0),F(0),F(1)]), ("x^2+x^4",[F(0),F(0),F(1),F(0),F(1)])):
    N=20
    M=[F(0)]*(N+1)
    for k in range(N+1):
        xk=[F(0)]*(k+1); xk[k]=F(1)
        M[k]=h1(w, xk, c)
    # even recurrence m=2..N/2
    ok_e = all(c*M[2*m] == A_e(m,c)*M[2*m-2] - B_e(m,c)*M[2*m-4] for m in range(2, N//2+1))
    ok_o = all(c*M[2*m+1] == A_o(m,c)*M[2*m-1] - B_o(m,c)*M[2*m-3] for m in range(2, N//2))
    print("  w=%s: M0=%s M1=%s even-recurrence OK=%s odd-recurrence OK=%s"%(wname,M[0],M[1],ok_e,ok_o))

print()
print("=== 2. growth lemma on the M-sequence (M_2=1): M_{2m} >= (4/c)^{m-1} m! ===")
for c in (1,3,10,50):
    cF=F(c); N=30
    u=[F(0)]*(N+1); u[1]=F(1)
    for m in range(2,N+1):
        u[m]=(A_e(m,cF)*u[m-1]-B_e(m,cF)*u[m-2])/cF
    ok=all(u[m] >= (F(4)/cF)**(m-1)*F(math.factorial(m)) for m in range(1,N+1))
    print("  c=%d: u_m >= (4/c)^{m-1} m!  OK=%s ; u_15 digits=%d"%(c,ok,len(str(u[15].numerator))))

print()
print("=== 3. H1-moment size bound vs superfactorial growth (float demo) ===")
# simulate w in H1: bound C*sqrt(m) with C=10; growth (4/c)^{m-1} m!
for c in (1.0,3.0,10.0):
    for m in (5,10,15,20,30):
        grow = (4.0/c)**(m-1)*math.factorial(m)
        bnd = 10.0*math.sqrt(m)
        print("  c=%-4g m=%2d: growth=%.3e bound=%.3e ratio=%.3e"%(c,m,grow,bnd,grow/bnd))
    print()

print("=== 4. H1-completeness check: H1 projections of x^2, x^3 onto span{K_c p_n} ===")
# use float Gram with monomial basis of K_c p_n for n admissible
import numpy as np
c=3.0
def kc_flt(poly, c):
    n=len(poly)-1; out=np.zeros(n+1)
    out += c*np.array(poly)
    for j in range(n+1):
        if j+2<=n: out[j] -= (j+1)*(j+2)*poly[j+2]
    return out
def h1_gram(f,g,c):
    # f,g as coeff arrays: (f,g)_1 = -1/2 Delta f Delta g + int f' g' + c int f g
    df = lambda p: sum(p[k]* (1.0 if k%2 else -1.0) for k in range(len(p)))  # p(1)-p(-1)
    def dp(p): return np.array([(k+1)*p[k+1] for k in range(len(p)-1)]) if len(p)>1 else np.zeros(1)
    def l2ip(p,q):
        n=max(len(p),len(q)); P=np.zeros(n); Q=np.zeros(n); P[:len(p)]=p; Q[:len(q)]=q
        s=0.0
        for j in range(n):
            for k in range(n):
                if (j+k)%2==0: s+=P[j]*Q[k]*2.0/(j+k+1)
        return s
    return -0.5*(df(f))*(df(g)) + l2ip(dp(f),dp(g)) + c*l2ip(f,g)
# build K_c p_n for n admissible up to degree D
basis=[]  # list of coeff arrays
def monomial(k):
    a=np.zeros(k+1); a[k]=1.0; return a
for n in [0,1]+list(range(4,20)):
    if n%2==0:
        m=n//2
        p = np.zeros(n+1); p[n]=1.0
        if m>=2: p[n-2] = -float(F(m,m-1))
        else: p[n-2]=0.0
    else:
        m=(n-1)//2
        p = np.zeros(n+1); p[n]=1.0
        if m>=2: p[n-2] = -float(F(m,m-1))
        else: p[n-2]=0.0
    basis.append(kc_flt(p,c))
# H1 Gram + projection residuals of x^2, x^3
D=len(basis)
G=np.zeros((D,D))
for i in range(D):
    for j in range(i,D):
        G[i,j]=G[j,i]=h1_gram(basis[i],basis[j],c)
for target_name,target in (("x^2",monomial(2)),("x^3",monomial(3))):
    b=np.array([h1_gram(target,basis[j],c) for j in range(D)])
    for use in (6,10,14,18):
        Gs=G[:use,:use]; bs=b[:use]
        try:
            coef=np.linalg.solve(Gs,bs)
            # residual: ||target - proj||^2 = ||target||^2 - b^T G^{-1} b
            res2=h1_gram(target,target,c)-bs@np.linalg.solve(Gs,bs)
            print("  %s onto span(deg<=%d): residual^2 (H1) = %.3e"%(target_name,2*use-2,res2))
        except np.linalg.LinAlgError:
            print("  singular at use=%d"%use)
EOF
