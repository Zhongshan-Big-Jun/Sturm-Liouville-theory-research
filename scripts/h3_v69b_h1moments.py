# -*- coding: utf-8 -*-
"""H3 v69b: correct verification of the H1-moment route.
Identity to check: for ANY polynomial w,
  c M_{2m} - A_m M_{2m-2} + B_m M_{2m-4} == (w, K_c p_{2m})_1   (M_k = (w,x^k)_1)
i.e. the 2nd-order recurrence in M is exactly the orthogonality condition.
Growth lemma vs polynomial bound; H1 projections of x^2, x^3."""
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
def p_even(m):
    p=[F(0)]*(2*m+1); p[2*m]=F(1); p[2*m-2]=-F(m, m-1); return p
def p_odd(m):
    p=[F(0)]*(2*m+2); p[2*m+1]=F(1); p[2*m-1]=-F(m, m-1); return p

c=F(3)
print("=== 1. IDENTITY: c M_{2m} - A_m M_{2m-2} + B_m M_{2m-4} == (w, K_c p_{2m})_1 ===")
for wname, w in (("x^2",[F(0),F(0),F(1)]), ("x^3",[F(0),F(0),F(0),F(1)]), ("x^2+x^4",[F(0),F(0),F(1),F(0),F(1)]),
                 ("1+x+x^5",[F(1),F(1),F(0),F(0),F(0),F(1)])):
    N=20
    M=[F(0)]*(N+1)
    for k in range(N+1):
        xk=[F(0)]*(k+1); xk[k]=F(1)
        M[k]=h1(w, xk, c)
    ok_e = all(c*M[2*m] - A_e(m,c)*M[2*m-2] + B_e(m,c)*M[2*m-4] == h1(w, kc(p_even(m),c), c) for m in range(2, N//2+1))
    ok_o = all(c*M[2*m+1] - A_o(m,c)*M[2*m-1] + B_o(m,c)*M[2*m-3] == h1(w, kc(p_odd(m),c), c) for m in range(2, N//2))
    print("  w=%s: even-identity OK=%s odd-identity OK=%s"%(wname,ok_e,ok_o))

print()
print("=== 2. if (w,K_c p_{2m})_1 = 0 for all m>=2 and M0=M1=0 then M_{2m}=M2*u_m with growth (4/c)^{m-1} m! ===")
for c in (1,3,10,50):
    cF=F(c); N=30
    u=[F(0)]*(N+1); u[1]=F(1)
    for m in range(2,N+1):
        u[m]=(A_e(m,cF)*u[m-1]-B_e(m,cF)*u[m-2])/cF
    ok=all(u[m] >= (F(4)/cF)**(m-1)*F(math.factorial(m)) for m in range(1,N+1))
    print("  c=%d: growth OK=%s ; u_20 = %s"%(c,ok,str(u[20])[:40]))

print()
print("=== 3. size bound |M_{2m}| <= 2m||w'|| sqrt(2/(4m-1)) + c||w|| sqrt(2/(4m+1))  (demo with ||w'||=||w||=1) ===")
for m in (2,3,5,10,20):
    b = 2*m*math.sqrt(2.0/(4*m-1)) + 3.0*math.sqrt(2.0/(4*m+1))
    g = (4.0/3.0)**(m-1)*math.factorial(m)
    print("  c=3 m=%2d: bound=%.4f  growth=%.3e  (growth/bound=%.1e)"%(m,b,g,g/b))

print()
print("=== 4. H1 projections of x^2, x^3 onto span{K_c p_n} (float, c=3) ===")
import numpy as np
c=3.0
def monomial(k):
    a=np.zeros(k+1); a[k]=1.0; return a
def h1_gram(f,g,c):
    def df(p): return sum(p[k]*(1.0 if k%2 else -1.0) for k in range(len(p)))
    def dp(p): return np.array([(k+1)*p[k+1] for k in range(len(p)-1)]) if len(p)>1 else np.zeros(1)
    def l2ip(p,q):
        n=max(len(p),len(q)); P=np.zeros(n); Q=np.zeros(n); P[:len(p)]=p; Q[:len(q)]=q
        s=0.0
        for j in range(n):
            for k in range(n):
                if (j+k)%2==0: s+=P[j]*Q[k]*2.0/(j+k+1)
        return s
    return -0.5*df(f)*df(g) + l2ip(dp(f),dp(g)) + c*l2ip(f,g)
basis=[]
for n in [0,1]+list(range(4,20)):
    m=n//2 if n%2==0 else (n-1)//2
    p = np.zeros(n+1); p[n]=1.0
    if n>=2: p[n-2] = -float(F(m,m-1))
    # K_c p
    q = np.zeros(n+1); q += c*p
    for j in range(n+1):
        if j+2<=n: q[j] -= (j+1)*(j+2)*p[j+2]
    basis.append(q)
D=len(basis)
G=np.zeros((D,D))
for i in range(D):
    for j in range(i,D):
        G[i,j]=G[j,i]=h1_gram(basis[i],basis[j],c)
for target_name,target in (("x^2",monomial(2)),("x^3",monomial(3))):
    b=np.array([h1_gram(target,basis[j],c) for j in range(D)])
    print("  target %s: (H1 norm)^2 = %.6f"%(target_name,h1_gram(target,target,c)))
    for use in (6,10,14,18):
        Gs=G[:use,:use]; bs=b[:use]
        try:
            coef=np.linalg.solve(Gs,bs)
            res2=h1_gram(target,target,c)-bs@np.linalg.solve(Gs,bs)
            print("    span(deg<=%2d): residual^2(H1) = %.3e"%(2*use-2,max(res2,0.0)))
        except np.linalg.LinAlgError:
            print("    singular at use=%d"%use)
EOF
