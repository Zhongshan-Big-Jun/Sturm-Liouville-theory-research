import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def region2_pairs(R, tau, n=2000):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    pairs = []
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            inc = vy[-1] > vy[0]
            for k in range(len(vx)):
                t = vx[k]
                if t <= lo or t >= hi: continue
                l,h = 0, len(yl)-1
                f = (lambda idx: vy[idx]-t) if inc else (lambda idx: t-vy[idx])
                if f(0)*f(len(yl)-1) > 0: continue
                l,h = 0, len(yl)-1
                for _ in range(40):
                    mid = (l+h)//2
                    if f(mid)<=0: h=mid
                    else: l=mid+1
                l = min(l, len(yl)-2)
                ya, yb = yl[l], yl[l+1]
                fa = rtau(ya,m,tau)-rtau(xl[k],m,tau)
                fb = rtau(yb,m,tau)-rtau(xl[k],m,tau)
                if fa*fb > 0: continue
                try:
                    y = mp.findroot(lambda yy: rtau(yy,m,tau)-rtau(xl[k],m,tau), (ya,yb), solver='bisect')
                except Exception:
                    continue
                x = xl[k]
                if xmid < x < y < xmax and abs(rtau(y,m,tau)-rtau(x,m,tau)) < 1e-20:
                    if not any(abs(x-p[0])<1e-8 and abs(y-p[1])<1e-8 for p in pairs):
                        pairs.append((x,y))
    return pairs

pairs = region2_pairs(100, mp.mpf('1.22'))
print("R=100 tau=1.22: num pairs:", len(pairs))
if pairs:
    mxy = min(x+y for x,y in pairs)
    b = [p for p in pairs if abs(p[0]+p[1]-mxy)<1e-12][0]
    print("min x+y =", mp.nstr(mxy,18), " pi =", mp.nstr(mp.pi,18), " margin:", mp.nstr(mp.pi-mxy,12))
    print("pair:", mp.nstr(b[0],15), mp.nstr(b[1],15))
