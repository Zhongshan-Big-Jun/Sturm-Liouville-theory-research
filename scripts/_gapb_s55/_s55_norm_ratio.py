import mpmath as mp
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def Phi(A,psi,B,m):
    return (m*A*W(B,m)+m*B*W(A,m)+psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))

def y_end(s,a,b,m):
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    sya=mp.sin(A)/m; dya=mp.cos(A)
    c,sn=mp.cos(psi),mp.sin(psi)
    syb=c*sya+sn*dya; dyb=-sn*sya+c*dya
    return mp.cos(B)*(m*syb)+mp.sin(B)*dyb

def mode(a,b,m,k):
    # kth root
    roots=[]; s=mp.mpf('0.01'); prev=y_end(s,a,b,m)
    while len(roots)<k and s<100:
        s2=s+0.02; v2=y_end(s2,a,b,m)
        if v2*prev<0:
            lo,hi=s,s2; flo=prev
            for _ in range(200):
                mid=(lo+hi)/2; fm=y_end(mid,a,b,m)
                if fm*flo<=0: hi=mid
                else: lo,flo=mid,fm
            roots.append((lo+hi)/2)
            if len(roots)>=k: break
        s,prev=s2,v2
    return roots[k-1]

for (a,b,R) in [(0.3,0.7,4.0),(0.25,0.65,4.0),(0.2,0.6,10.0)]:
    m=mp.sqrt(mp.mpf(R))
    s1=mode(a,b,m,1); s2=mode(a,b,m,2)
    tau=s2/s1
    A=m*s1*a; psi=s1*(b-a); B=m*s1*(1-b)
    n2n1_direct = (Phi(tau*A, tau*psi, tau*B, m)/s2**3)/(Phi(A,psi,B,m)/s1**3)
    # handoff form
    Sigma1 = psi + m*A/W(A,m) + m*B/W(B,m)
    Sigma2 = psi + m*A/W(tau*A,m) + m*B/W(tau*B,m)
    n2n1_handoff = (1/tau**2)*(W(tau*A,m)/W(A,m))*(Sigma2/Sigma1)
    # also R1=0 requires n2/n1 = sin^2(tau A)/sin^2 A
    target = mp.sin(tau*A)**2/mp.sin(A)**2
    print(f"(a,b,R)=({a},{b},{R}):")
    print("  n2/n1 direct      =", mp.nstr(n2n1_direct,15))
    print("  n2/n1 handoff     =", mp.nstr(n2n1_handoff,15))
    print("  sin^2(tauA)/sin^2A =", mp.nstr(target,15))
    print("  R1=0 residual (n2/n1 - target) =", mp.nstr(n2n1_direct - target,10))
