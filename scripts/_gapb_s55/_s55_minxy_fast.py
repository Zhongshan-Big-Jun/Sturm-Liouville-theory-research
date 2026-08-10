import mpmath as mp
mp.mp.dps = 30

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

# fast float version
import math
def Wf(x, m): return math.sin(x)**2 + m*m*math.cos(x)**2
def Jf(x, m): return math.sin(x)**2/Wf(x, m)
def rf(x, m, tau): return Jf(tau*x, m)/Jf(x, m)

def min_xy_fast(R, tau, n=4000):
    """min x+y over E=0 pairs in region II, via float scan; returns (minxy, c1) where c1 = first critical point."""
    m = math.sqrt(R)
    xmid = math.pi/(1+tau); xmax = math.pi/tau
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [rf(x,m,tau) for x in xs]
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    # find pairs via segment monotonicity (float)
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    import bisect
    minxy = 1e9
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            for k in range(len(vx)):
                t = vx[k]
                if t <= lo or t >= hi: continue
                if vy[-1] > vy[0]:
                    idx = bisect.bisect_left(vy, t)
                else:
                    idx = bisect.bisect_left([-v for v in vy], -t)
                for j in (idx-1, idx):
                    if j < 0 or j >= len(yl)-1: continue
                    ya, yb = yl[j], yl[j+1]
                    fa = rf(ya,m,tau)-rf(xl[k],m,tau)
                    fb = rf(yb,m,tau)-rf(xl[k],m,tau)
                    if fa*fb <= 0:
                        # linear interp estimate
                        y = ya + (yb-ya)*(-fa)/(fb-fa) if fb!=fa else ya
                        s = xl[k]+y
                        if s < minxy: minxy = s
    c1 = crit[0] if crit else None
    return minxy, c1

print("=== min x+y vs 2*c1 for several (R,tau) ===")
for R in [6, 20, 50, 100, 200, 400, 1000, 10000]:
    for tau in [1.1, 1.22, 1.3, 1.5, 1.7, 1.9]:
        minxy, c1 = min_xy_fast(R, tau)
        if minxy < 1e8:
            print("R=%6s tau=%4.2f: min_xy~%.5f  2*c1=%.5f  (c1=%.5f, xmid=%.4f, pi/2=%.4f)" % (R, tau, minxy, 2*c1 if c1 else float('nan'), c1 if c1 else float('nan'), math.pi/(1+tau), math.pi/2))
        else:
            print("R=%6s tau=%4.2f: no pairs (monotone)" % (R, tau))
