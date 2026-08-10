import mpmath as mp
import math
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def J(x, m): return mp.sin(x)**2/W(x, m)
def rtau(x, m, tau): return J(tau*x, m)/J(x, m)
def alpha(x, m): return mp.atan2(mp.sin(x)/m, mp.cos(x))

print("=== L0: tau^2 r_tau(x) > 1 on (0, xmid) ===")
ok = True
for R in [1.05, 1.5, 4, 100, 1e4, 1e6]:
    m = mp.sqrt(mp.mpf(R))
    for tau in [mp.mpf('1.01'), mp.mpf('1.5'), mp.mpf('1.99')]:
        xmid = mp.pi/(1+tau)
        xs = [xmid*i/500 for i in range(1,500)]
        mn = min(float(tau**2*rtau(x,m,tau)) for x in xs)
        if mn <= 1.0: ok = False; print("  FAIL", R, tau, mn)
print("  L0 all pass:", ok)

print("=== BETA: tau sin(tau x) > sin x on (0, xmid) ===")
ok = True
for tau in [mp.mpf('1.01'), mp.mpf('1.5'), mp.mpf('1.99')]:
    xmid = mp.pi/(1+tau)
    xs = [xmid*i/1000 for i in range(1,1000)]
    mn = min(float(tau*mp.sin(tau*x)-mp.sin(x)) for x in xs)
    if mn <= 0: ok = False; print("  FAIL", tau, mn)
print("  BETA all pass:", ok, "(min margins", ")")

print("=== Lemma A: r>1 on (0,xmid), r<1 on (xmid,pi/tau) ===")
ok = True
for R in [1.05, 4, 100, 1e4]:
    m = mp.sqrt(mp.mpf(R))
    for tau in [mp.mpf('1.1'), mp.mpf('1.5'), mp.mpf('1.9'), mp.mpf('2.5')]:
        xmid = mp.pi/(1+tau); xmax = mp.pi/tau
        l = [float(rtau(x,m,tau)) for x in [xmid*i/400 for i in range(1,400)]]
        r = [float(rtau(x,m,tau)) for x in [xmid+(xmax-xmid)*i/400 for i in range(1,400)]]
        if min(l) <= 1.0 or max(r) >= 1.0: ok=False; print("  FAIL", R, tau, min(l), max(r))
print("  Lemma A all pass:", ok)

print("=== alpha-reflection: alpha(x)+alpha(y)>pi if x+y>pi ===")
ok = True
for R in [4, 100]:
    m = mp.sqrt(mp.mpf(R))
    for i in range(1,200):
        for j in range(1,200):
            x = mp.pi*i/200; y = mp.pi*j/200
            if x+y > mp.pi and alpha(x,m)+alpha(y,m) <= mp.pi:
                ok=False
print("  alpha-reflection all pass:", ok)

print("=== r strictly decreasing on (xmid, pi/2] ===")
ok = True
for R in [1.05, 2, 100, 1e6]:
    m = mp.sqrt(mp.mpf(R))
    for tau in [mp.mpf('1.05'), mp.mpf('1.5'), mp.mpf('2.5')]:
        xmid = mp.pi/(1+tau)
        if xmid >= mp.pi/2: continue
        xs = [xmid+(mp.pi/2-xmid)*i/2000 for i in range(1,2000)]
        v = [float(rtau(x,m,tau)) for x in xs]
        if not all(v[i]>v[i+1] for i in range(len(v)-1)): ok=False; print("  FAIL",R,tau)
print("  decreasing all pass:", ok)

print("=== danger zone: r(y)<r(x) for x in (xmid,pi/2), y in (pi/2,min(pi-x,pi/tau)) ===")
viol=0
for R in [1.05, 1.5, 4, 100, 1e4, 1e6]:
    m = math.sqrt(R)
    for tau in [1.05, 1.22, 1.5, 1.9]:
        xmid = math.pi/(1+tau); xmax = math.pi/tau
        if xmax <= math.pi/2: continue
        for i in range(1,200):
            x = xmid+(math.pi/2-xmid)*i/200
            ymax = min(math.pi-x, xmax)
            if ymax <= math.pi/2: continue
            for j in range(1,200):
                y = math.pi/2+(ymax-math.pi/2)*j/200
                if not (J(tau*y,mp.mpf(m))/J(y,mp.mpf(m)) < J(tau*x,mp.mpf(m))/J(x,mp.mpf(m))):
                    viol+=1
print("  danger-zone violations:", viol)

print("=== B': region II E=0 pairs have x+y>pi (spot check R=100, tau=1.22) ===")
import bisect
def pairs(R, tau, n=2000):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs=[xmid+(xmax-xmid)*i/n for i in range(1,n)]
    vals=[float(rtau(x,m,tau)) for x in xs]
    crit=[i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx=[0]+crit+[len(xs)-1]
    segs=[(segs_idx[k],segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    out=[]; 
    for si in range(len(segs)):
        for sj in range(si+1,len(segs)):
            i0,i1=segs[si]; j0,j1=segs[sj]
            vx=vals[i0:i1+1]; vy=vals[j0:j1+1]
            xl=xs[i0:i1+1]; yl=xs[j0:j1+1]
            lo,hi=min(vy),max(vy)
            for k in range(len(vx)):
                t=vx[k]
                if t<=lo or t>=hi: continue
                idx=bisect.bisect_left(vy,t) if vy[-1]>vy[0] else bisect.bisect_left([-v for v in vy],-t)
                for j in (idx-1,idx):
                    if j<0 or j>=len(yl)-1: continue
                    ya,yb=yl[j],yl[j+1]
                    fa=rtau(ya,m,tau)-rtau(xl[k],m,tau); fb=rtau(yb,m,tau)-rtau(xl[k],m,tau)
                    if fa*fb<0:
                        y=mp.findroot(lambda yy: rtau(yy,m,tau)-rtau(xl[k],m,tau),(ya,yb),solver='bisect')
                        x=xl[k]
                        if x<y and xmid<x<y<xmax and not any(abs(x-p[0])<1e-9 for p in out):
                            out.append((x,y))
    return out
ps = pairs(100, mp.mpf('1.22'))
mns = min(float(x+y) for x,y in ps)
print("  pairs:", len(ps), "min x+y:", round(mns,8), "> pi:", mns > float(mp.pi))

print("=== norm closed form via alpha-identity (piecewise, mode 1 & 2) ===")
def Phi_alpha(A,psi,B,m,k):
    # k=1 mode1: alpha(A)+psi = pi-alpha(B); k=2: alpha(2..): use alpha(TA)+Tpsi = 2pi-alpha(TB)
    I1 = (A-mp.sin(A)*mp.cos(A))/(2*m)
    WA = W(A,m)
    aA = alpha(A,m); aB = alpha(B,m)
    # middle piece with sin2(alphaA+psi) = -sin2 alphaB
    I2 = (WA/m**2)*(psi/2 + (mp.sin(2*aA)+mp.sin(2*aB))/4)
    I3 = (WA/W(B,m))*(B-mp.sin(B)*mp.cos(B))/(2*m)
    return I1+I2+I3
def Phi_closed(A,psi,B,m):
    return (m*A*W(B,m)+m*B*W(A,m)+psi*W(A,m)*W(B,m))/(2*m**2*W(B,m))
def y_end(s,a,b,m):
    A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
    sya=mp.sin(A)/m; dya=mp.cos(A)
    c,sn=mp.cos(psi),mp.sin(psi)
    syb=c*sya+sn*dya; dyb=-sn*sya+c*dya
    return mp.cos(B)*(m*syb)+mp.sin(B)*dyb
def modes(a,b,m,kmax=2):
    roots=[]; s=mp.mpf('0.01'); prev=y_end(s,a,b,m)
    while len(roots)<kmax and s<100:
        s2=s+0.02; v2=y_end(s2,a,b,m)
        if v2*prev<0:
            lo,hi=s,s2; flo=prev
            for _ in range(200):
                mid=(lo+hi)/2; fm=y_end(mid,a,b,m)
                if fm*flo<=0: hi=mid
                else: lo,flo=mid,fm
            roots.append((lo+hi)/2)
            if len(roots)>=kmax: break
        s,prev=s2,v2
    return roots
ok=True
for (a,b,R) in [(0.3,0.7,4.0),(0.25,0.65,4.0),(0.2,0.6,10.0),(0.1,0.9,2.0)]:
    m=mp.sqrt(mp.mpf(R))
    s1,s2=modes(a,b,m,2); tau=s2/s1
    for k in (1,2):
        s = s1 if k==1 else s2
        A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
        d = Phi_alpha(A,psi,B,m,k)-Phi_closed(A,psi,B,m)
        if abs(d)>1e-25: ok=False; print("  FAIL",a,b,R,k,mp.nstr(d,10))
print("  Phi_alpha == Phi_closed for modes 1,2:", ok)
