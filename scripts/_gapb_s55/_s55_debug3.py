import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

R = 100; tau = mp.mpf('1.22'); m = mp.sqrt(mp.mpf(R))
xmid = mp.pi/(1+tau); xmax = mp.pi/tau
n = 2000
xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
vals = [float(rtau(x,m,tau)) for x in xs]
crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
segs_idx = [0]+crit+[len(xs)-1]
segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
print("segs:", segs)
si, sj = 0, 2
i0,i1 = segs[si]; j0,j1 = segs[sj]
vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
print("seg0 val range:", min(vx), max(vx))
print("seg2 val range:", min(vy), max(vy))
lo,hi = min(vy), max(vy)
inc = vy[-1] > vy[0]
print("inc:", inc, "lo,hi:", lo, hi)
# find a k where t in (lo,hi)
hits = [k for k in range(len(vx)) if lo < vx[k] < hi]
print("num k with t in range:", len(hits))
if hits:
    k = hits[0]
    t = vx[k]
    l,h = 0, len(yl)-1
    f = (lambda idx: vy[idx]-t) if inc else (lambda idx: t-vy[idx])
    print("f(0) =", f(0), " f(end) =", f(len(yl)-1))
    if f(0)*f(len(yl)-1) > 0:
        print("SKIPPED by sign test")
    else:
        l,h = 0, len(yl)-1
        for _ in range(40):
            mid = (l+h)//2
            if f(mid)<=0: h=mid
            else: l=mid+1
        print("l =", l, "yl[l] =", yl[l], "vy[l] =", vy[l], " t =", t)
