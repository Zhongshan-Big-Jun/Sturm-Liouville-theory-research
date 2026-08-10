# -*- coding: utf-8 -*-
"""Additional numerical checks for H^2 completeness: odd eigenfunctions and mixed test functions."""
import numpy as np, math

def poly_solve(qcoeff, c):
    n = len(qcoeff)-1; a=[0.0]*(n+1)
    for j in range(n,-1,-1):
        a[j] = (qcoeff[j] + ((j+1)*(j+2)*a[j+2] if j+2<=n else 0.0))/c
    return a
def ell1(p): return sum(k*a for k,a in enumerate(p) if k%2==0)
def ell2(p): return sum((k-1)*a for k,a in enumerate(p) if k%2==1)
def p_basis(N):
    out=[]
    for k in range(N+1):
        if k in (2,3): continue
        cc=np.zeros(k+1); cc[k]=1.0; n=k//2
        if n!=1 and k>=4: cc[k-2]=-n/(n-1)
        assert abs(ell1(cc))<1e-12 and abs(ell2(cc))<1e-12
        out.append((k,cc))
    return out
def kc(p,c):
    n=len(p)-1; o=[0.0]*(n+1)
    for j in range(n+1):
        o[j]+=c*p[j]
        if j+2<=n: o[j]-=(j+1)*(j+2)*p[j+2]
    return o
def l2(p,q):
    n=max(len(p),len(q))-1; P=np.zeros(n+1); Q=np.zeros(n+1); P[:len(p)]=p; Q[:len(q)]=q
    s=0.0
    for j in range(n+1):
        for k in range(n+1):
            if (j+k)%2==0: s+=P[j]*Q[k]*2.0/(j+k+1)
    return s

c=1.0; N=40
basis=p_basis(N)
G=np.zeros((len(basis),len(basis))); kcb=[]
for i,(d,pi) in enumerate(basis):
    kpi=kc(pi,c); kcb.append(kpi)
    for j in range(i+1): G[i,j]=G[j,i]=l2(kpi,kcb[j])

# first nonzero root of tan z = z
z1=4.493409457909064
def sin_z_coeff(z, M=80):
    out=np.zeros(M+1)
    for k in range((M-1)//2+1):
        out[2*k+1]=(-1)**k * z**(2*k+1)/math.factorial(2*k+1)
    return out
def proj_resid(f, Nn):
    fk=kc(f,c); f2=l2(fk,fk)
    idx=[i for i,(d,_) in enumerate(basis) if d<=Nn]
    Gs=G[np.ix_(idx,idx)]
    rhs=np.array([l2(fk,kcb[i]) for i in idx])
    x=np.linalg.solve(Gs,rhs)
    return max(f2-x@Gs@x,0.0)

f_odd=sin_z_coeff(z1,2*N)
print("sin(z1 x): check BC ell1/ell2 of truncated poly:", ell1(f_odd), ell2(f_odd))
for NN in (8,16,24,32,40):
    print("   residual sin(z1 x), N=%d: %.3e" % (NN, proj_resid(f_odd,NN)))

f_even=np.zeros(2*N+1)
for k in range(N//2+1): f_even[2*k]=(-1)**k*(math.pi)**(2*k)/math.factorial(2*k)
f_mix=[a+b for a,b in zip(f_even,f_odd)]
print("mixed cos(pi x)+sin(z1 x): residual (should -> 0)")
for NN in (8,16,24,32,40):
    print("   residual mixed, N=%d: %.3e" % (NN, proj_resid(f_mix,NN)))

# smallest eigenvalue of the N x N Gram for increasing N (should decay -> 0 = completeness)
print("smallest eigenvalues of truncated Gram (decay indicates completeness):")
for NN in (6,10,14,20,26,32,40):
    idx=[i for i,(d,_) in enumerate(basis) if d<=NN]
    Gs=G[np.ix_(idx,idx)]
    ev=np.linalg.eigvalsh(Gs)
    print("   N=%2d: lambda_min = %.3e" % (NN, ev[0]))
