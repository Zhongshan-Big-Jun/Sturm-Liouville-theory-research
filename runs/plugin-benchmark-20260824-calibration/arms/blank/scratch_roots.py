import math

def G(n,R,y):
    s=math.sqrt(R)
    c=math.cos(y); q=math.sin(y)
    alpha=s+1/s
    T=c*c-alpha/2*q*q
    # U_n(T)+U_{n-1}(T)/s
    if n==1:
        return q*(2*T+1/s)
    U0=1; U1=2*T
    for k in range(2,n+1):
        U0,U1=U1,2*T*U1-U0
    return q*(U1+U0/s)

def count_roots(n,R, N=20000):
    roots=[]
    prev=0.0
    prev_y=0.0
    for i in range(1,N+1):
        y=math.pi*i/N
        val=G(n,R,y)
        if prev == 0:
            prev=val
            prev_y=y
            continue
        if prev*val<0:
            roots.append((prev_y,y))
        prev=val; prev_y=y
    return roots

for n in range(1,6):
    for R in [1.5,2,10,100]:
        r=count_roots(n,R)
        print(n,R,len(r))
