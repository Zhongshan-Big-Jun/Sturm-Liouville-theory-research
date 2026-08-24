import math, numpy as np

def direct(n,R,y):
    s=math.sqrt(R)
    c=math.cos(y); q=math.sin(y)
    E=[[c,q],[-q,c]]
    C=[[c*c-q*q/s,(1+1/s)*c*q],[-(1+s)*c*q,c*c-s*q*q]]
    M=E
    for _ in range(n):
        M=[[sum(M[i][k]*C[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return M[0][1], M

def formula(n,R,y):
    s=math.sqrt(R)
    c=math.cos(y); q=math.sin(y)
    alpha=s+1/s
    T=c*c-alpha/2*q*q
    # Cheb U
    U0=1
    if n==1: U_prev=U0; U_curr=2*T
    else:
        U0=1; U1=2*T
        for k in range(2,n+1):
            U0,U1=U1,2*T*U1-U0
        U_curr=U1; U_prev=U0
    return q*(U_curr+U_prev/s)

for n in [1,2,3,4]:
    for R in [2,5,10]:
        for y in [0.3,1.0,2.5]:
            a,_=direct(n,R,y); b=formula(n,R,y)
            print(n,R,y,a,b,a-b)
