import mpmath as mp
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2

def Phi_closed(A,psi,B,m):
    return (m*A*W(B,m)+m*B*W(A,m)+psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))

def Phi_pieces(A,psi,B,m):
    # times s^3
    I1 = (A - mp.sin(A)*mp.cos(A))/(2*m)
    th = mp.mpf('0')
    I2 = mp.quad(lambda t: (mp.sin(A)/m*mp.cos(t)+mp.cos(A)*mp.sin(t))**2, [0,psi])
    syb = mp.cos(psi)*mp.sin(A)/m + mp.sin(psi)*mp.cos(A)
    dyb = -mp.sin(psi)*mp.sin(A)/m + mp.cos(psi)*mp.cos(A)
    u = syb; v = dyb/m
    lam2 = u**2+v**2
    I3 = m*(B - mp.sin(B)*mp.cos(B))/2*lam2
    return I1+I2+I3

# test on a config with phases satisfying secular
def y_end(s,a,b,m):
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    sya=mp.sin(A)/m; dya=mp.cos(A)
    c,sn=mp.cos(psi),mp.sin(psi)
    syb=c*sya+sn*dya; dyb=-sn*sya+c*dya
    return mp.cos(B)*(m*syb)+mp.sin(B)*dyb

for (a,b,R) in [(0.3,0.7,4.0),(0.25,0.65,4.0),(0.2,0.6,10.0)]:
    m=mp.sqrt(mp.mpf(R))
    # find s1
    s=mp.mpf('0.01'); prev=y_end(s,a,b,m); s1=None
    while s<50:
        s2=s+0.01; v2=y_end(s2,a,b,m)
        if v2*prev<0:
            lo,hi=s,s2; flo=prev
            for _ in range(200):
                mid=(lo+hi)/2; fm=y_end(mid,a,b,m)
                if fm*flo<=0: hi=mid
                else: lo,flo=mid,fm
            s1=(lo+hi)/2; break
        s,prev=s2,v2
    A=m*s1*a; psi=s1*(b-a); B=m*s1*(1-b)
    pc = Phi_closed(A,psi,B,m)
    pp = Phi_pieces(A,psi,B,m)
    print(f"(a,b,R)=({a},{b},{R}): closed={mp.nstr(pc,15)} pieces={mp.nstr(pp,15)} rel={mp.nstr((pc-pp)/pc,10)}")
