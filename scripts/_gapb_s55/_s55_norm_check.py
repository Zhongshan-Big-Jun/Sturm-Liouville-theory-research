import mpmath as mp
mp.mp.dps = 40

def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def J(x, m): return mp.sin(x)**2/W(x, m)

def norm_direct(s, a, b, m):
    # integrate rho y^2 over [0,1] with y slope-normalized: y(0)=0, y'(0)=1
    # pieces via exact antiderivatives; check against quadrature too
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    # [0,a]: rho=m^2, y=sin(msx)/(ms)
    I1 = (A - mp.sin(A)*mp.cos(A))/(2*m*s**3)
    # [a,b]: rho=1, y=(1/s)[(sinA/m)cos th + cosA sin th]
    def y_mid(th):
        return (mp.sin(A)/m)*mp.cos(th) + mp.cos(A)*mp.sin(th)
    I2 = mp.quad(lambda th: y_mid(th)**2, [0, psi]) / s**3
    # [b,1]: rho=m^2, y(x)=y(b)cos th' + y'(b) sin th'/(ms), th'=ms(x-b)
    syb = mp.cos(psi)*mp.sin(A)/m + mp.sin(psi)*mp.cos(A)
    dyb = -mp.sin(psi)*mp.sin(A)/m + mp.cos(psi)*mp.cos(A)
    def y_right(th):
        return syb*mp.cos(th)/1.0 + dyb*mp.sin(th)/(m*s)  # y = (sy_b cos th + dy_b sin th/m)/s? check
    # actually y(x) = y(b) cos th + y'(b) sin th/(ms); y(b)=syb/s
    def y_right2(th):
        return (syb/s)*mp.cos(th) + (dyb/(m*s))*mp.sin(th)
    I3 = m**2 * mp.quad(lambda th: y_right2(th)**2, [0, B]) * (1/(m*s))
    return I1+I2+I3

def norm_closed_handoff(s, a, b, m):
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    Phi = (m*A*W(B,m) + m*B*W(A,m) + psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))
    return Phi/s**3

def norm_closed_sym(s, a, b, m):
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    # symmetric version candidate
    Phi = (m*A*W(B,m) + m*B*W(A,m) + psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))
    Phis = (Phi + Phi_swap)/2
    return None

for (a,b,R) in [(0.3,0.7,4.0),(0.25,0.65,4.0),(0.2,0.6,10.0),(0.35,0.8,2.0)]:
    m = mp.sqrt(mp.mpf(R))
    # pick s = mode 1 via solve
    # simple: use a generic s
    import math
    def y_end(s,a,b,m):
        A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
        sya=mp.sin(A)/m; dya=mp.cos(A)
        c,sn=mp.cos(psi),mp.sin(psi)
        syb=c*sya+sn*dya; dyb=-sn*sya+c*dya
        return mp.cos(B)*(m*syb)+mp.sin(B)*dyb
    # find s1
    s = mp.mpf('0.1'); prev = y_end(s,a,b,m); s1=None
    while s < 50:
        s2 = s+0.01; v2 = y_end(s2,a,b,m)
        if v2*prev < 0:
            lo,hi=s,s2; flo=prev
            for _ in range(200):
                mid=(lo+hi)/2; fm=y_end(mid,a,b,m)
                if fm*flo<=0: hi=mid
                else: lo,flo=mid,fm
            s1=(lo+hi)/2; break
        s,prev=s2,v2
    A=m*s1*a; psi=s1*(b-a); B=m*s1*(1-b)
    nd = norm_direct(s1,a,b,m)
    nc = norm_closed_handoff(s1,a,b,m)
    print(f"(a,b,R)=({a},{b},{R}): A={mp.nstr(A,8)} psi={mp.nstr(psi,8)} B={mp.nstr(B,8)}")
    print("  norm direct =", mp.nstr(nd,15), " handoff closed =", mp.nstr(nc,15), " rel diff =", mp.nstr((nd-nc)/nd,8))
