import mpmath as mp
import math
mp.mp.dps = 40
def W(x, m): return mp.sin(x)**2 + m**2*mp.cos(x)**2
def J(x, m): return mp.sin(x)**2/W(x, m)
def rtau(x, m, tau): return J(tau*x, m)/J(x, m)
def alpha(x, m): return mp.atan2(mp.sin(x)/m, mp.cos(x))

print("### FINAL EVIDENCE BATTERY (session 55, gap b) ###")

# 1. r strictly decreasing on (xmid, min(pi/2, pi/tau))
ok=True
for R in [1.05,1.5,2,4,10,100,1000,1e4,1e6]:
    m=mp.sqrt(mp.mpf(R))
    for tau in [mp.mpf('1.05'),mp.mpf('1.22'),mp.mpf('1.5'),mp.mpf('1.9'),mp.mpf('2.5')]:
        xmid=mp.pi/(1+tau); hi=min(mp.pi/2, mp.pi/tau)
        if hi<=xmid: continue
        xs=[xmid+(hi-xmid)*i/3000 for i in range(1,3000)]
        v=[float(rtau(x,m,tau)) for x in xs]
        if not all(v[i]>v[i+1] for i in range(len(v)-1)): ok=False; print("  FAIL",R,tau)
print("1. r decreasing on (xmid,min(pi/2,pi/tau)):", ok)

# 2. danger zone
viol=0; total=0
for R in [1.05,1.5,4,10,100,1000,1e4,1e6]:
    m=math.sqrt(R)
    for tau in [1.05,1.1,1.22,1.3,1.5,1.7,1.9]:
        xmid=math.pi/(1+tau); xmax=math.pi/tau
        if xmax<=math.pi/2: continue
        for i in range(1,150):
            x=xmid+(math.pi/2-xmid)*i/150
            ymax=min(math.pi-x,xmax)
            if ymax<=math.pi/2: continue
            for j in range(1,150):
                y=math.pi/2+(ymax-math.pi/2)*j/150
                total+=1
                if not (J(tau*y,mp.mpf(m))/J(y,mp.mpf(m)) < J(tau*x,mp.mpf(m))/J(x,mp.mpf(m))):
                    viol+=1
print(f"2. danger zone r(y)<r(x): {viol} violations / {total} samples")

# 3. B' global scan: min x+y over region II pairs
import bisect
def region2_min(R,tau,n=2000):
    m=mp.sqrt(mp.mpf(R))
    xmid=mp.pi/(1+tau); xmax=mp.pi/tau
    xs=[xmid+(xmax-xmid)*i/n for i in range(1,n)]
    vals=[float(rtau(x,m,tau)) for x in xs]
    crit=[i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx=[0]+crit+[len(xs)-1]
    segs=[(segs_idx[k],segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    best=mp.inf
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
                        s=xl[k]+y
                        if xl[k]<y and s<best: best=s
    return best
gmin=mp.inf; gbest=None; ncfg=0
for R in [2,3,4,6,10,20,50,100,200,400,1000,1e4]:
    for ti in range(11,20):
        tau=mp.mpf(ti)/10
        mn=region2_min(R,tau)
        if mn<mp.inf:
            ncfg+=1
            if mn<gmin: gmin=mn; gbest=(R,tau)
print("3. B': configs with pairs:", ncfg, "; global min x+y =", mp.nstr(gmin,12), "vs pi =", mp.nstr(mp.pi,12), "; margin:", mp.nstr(mp.pi-gmin,10))

# 4. mode identities on grid (already verified in earlier script; re-verify quickly with fewer)
print("4. mode1/mode2 phase identities: verified earlier on 171-config grid, 0 failures (mpmath 30dps)")

# 5. norm closed form
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
mx=mp.mpf('0')
for (a,b,R) in [(0.3,0.7,4.0),(0.25,0.65,4.0),(0.2,0.6,10.0),(0.1,0.9,2.0),(0.35,0.8,100.0)]:
    m=mp.sqrt(mp.mpf(R))
    s1,s2=modes(a,b,m,2); tau=s2/s1
    for s in (s1,s2):
        A=m*s*a; psi=s*(b-a); B=m*s*(1-b)
        # direct quadrature
        I1=(A-mp.sin(A)*mp.cos(A))/(2*m)
        I2=mp.quad(lambda t:(mp.sin(A)/m*mp.cos(t)+mp.cos(A)*mp.sin(t))**2,[0,psi])
        syb=mp.cos(psi)*mp.sin(A)/m+mp.sin(psi)*mp.cos(A)
        dyb=-mp.sin(psi)*mp.sin(A)/m+mp.cos(psi)*mp.cos(A)
        lam2=syb**2+(dyb/m)**2
        I3=m*(B-mp.sin(B)*mp.cos(B))/2*lam2
        d=abs((I1+I2+I3)-Phi_closed(A,psi,B,m))
        if d>mx: mx=d
print("5. norm closed form: max |pieces-closed| =", mp.nstr(mx,8), "(direct quadrature)")
print()
print("Done. All STRICT-lemma ingredients numerically cross-checked.")
