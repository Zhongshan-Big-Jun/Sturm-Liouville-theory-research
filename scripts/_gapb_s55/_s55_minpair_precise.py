import mpmath as mp
mp.mp.dps = 40

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def min_pair_precise(R, tau, n=6000):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    print("  critical points (x):", [round(xs[c],6) for c in crit])
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    import bisect
    best = None; bestsum = mp.inf
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            for k in range(len(vx)):
                t = vx[k]
                if t <= lo or t >= hi: continue
                idx = bisect.bisect_left(vy, t) if vy[-1]>vy[0] else bisect.bisect_left([-v for v in vy], -t)
                for j in (idx-1, idx):
                    if j<0 or j>=len(yl)-1: continue
                    ya,yb = yl[j], yl[j+1]
                    fa = rtau(ya,m,tau)-rtau(xl[k],m,tau)
                    fb = rtau(yb,m,tau)-rtau(xl[k],m,tau)
                    if fa*fb < 0:
                        y = mp.findroot(lambda yy: rtau(yy,m,tau)-rtau(xl[k],m,tau), (ya,yb), solver='bisect')
                        x = xl[k]
                        s = x+y
                        if s < bestsum:
                            bestsum = s; best = (x, y, rtau(x,m,tau))
    return best, bestsum

for (R, tau) in [(100, mp.mpf('1.22')), (10000, mp.mpf('1.5')), (1000, mp.mpf('1.3')), (100000, mp.mpf('1.5'))]:
    print(f"R={R}, tau={tau}")
    best, s = min_pair_precise(R, tau)
    print("  min pair: x=%s y=%s sum=%s (pi=%s, margin=%s)" % (mp.nstr(best[0],15), mp.nstr(best[1],15), mp.nstr(s,15), mp.nstr(mp.pi,12), mp.nstr(s-mp.pi,10)))
    print("  level r =", mp.nstr(best[2],12), "; pi/2 =", mp.nstr(mp.pi/2,8))
