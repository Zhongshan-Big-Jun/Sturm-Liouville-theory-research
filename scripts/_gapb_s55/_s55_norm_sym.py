import mpmath as mp
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2

def y_end(s,a,b,m):
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    sya=mp.sin(A)/m; dya=mp.cos(A)
    c,sn=mp.cos(psi),mp.sin(psi)
    syb=c*sya+sn*dya; dyb=-sn*sya+c*dya
    return mp.cos(B)*(m*syb)+mp.sin(B)*dyb

def s1_of(a,b,m):
    s=mp.mpf('0.1'); prev=y_end(s,a,b,m)
    while s<50:
        s2=s+0.01; v2=y_end(s2,a,b,m)
        if v2*prev<0:
            lo,hi=s,s2; flo=prev
            for _ in range(200):
                mid=(lo+hi)/2; fm=y_end(mid,a,b,m)
                if fm*flo<=0: hi=mid
                else: lo,flo=mid,fm
            return (lo+hi)/2
        s,prev=s2,v2

def Phi(A,psi,B,m):
    return (m*A*W(B,m)+m*B*W(A,m)+psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))

m = mp.sqrt(4)
a = mp.mpf('0.25'); b = mp.mpf('0.65')
s1 = s1_of(a,b,m)
A = m*s1*a; psi = s1*(b-a); B = m*s1*(1-b)
print("A,psi,B:", mp.nstr(A,10), mp.nstr(psi,10), mp.nstr(B,10))
print("Phi(A,B) =", mp.nstr(Phi(A,psi,B,m),12))
print("Phi(B,A) =", mp.nstr(Phi(B,psi,A,m),12))
# reflected config: a' = 1-b, b' = 1-a
a2 = 1-b; b2 = 1-a
s1b = s1_of(a2,b2,m)
print("reflected config s1:", mp.nstr(s1b,10), " vs ", mp.nstr(s1,10))
A2 = m*s1b*a2; psi2 = s1b*(b2-a2); B2 = m*s1b*(1-b2)
print("A2,psi2,B2:", mp.nstr(A2,10), mp.nstr(psi2,10), mp.nstr(B2,10))
print("Phi(A2,B2) =", mp.nstr(Phi(A2,psi2,B2,m),12))
