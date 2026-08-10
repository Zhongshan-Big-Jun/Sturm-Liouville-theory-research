import mpmath as mp
mp.mp.dps = 30

def W(x, m):
    return mp.sin(x)**2 + m**2*mp.cos(x)**2

def J(x, m):
    return mp.sin(x)**2/W(x, m)

def rtau(x, m, tau):
    return J(tau*x, m)/J(x, m)

def y_end(s, a, b, m):
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    sya = mp.sin(A)/m; dya = mp.cos(A)
    c, sn = mp.cos(psi), mp.sin(psi)
    syb = c*sya + sn*dya
    dyb = -sn*sya + c*dya
    return mp.cos(B)*(m*syb) + mp.sin(B)*dyb

def solve_modes(a, b, m, kmax=3):
    roots = []
    s = mp.mpf('0.01'); ds = mp.mpf('0.02')
    prev = y_end(s, a, b, m)
    while len(roots) < kmax and s < 400:
        s2 = s + ds
        v2 = y_end(s2, a, b, m)
        if prev == 0 or v2*prev < 0:
            lo, hi = s, s2; flo = prev
            for _ in range(200):
                mid = (lo+hi)/2
                fm = y_end(mid, a, b, m)
                if fm*flo <= 0: hi = mid
                else: lo, flo = mid, fm
            roots.append((lo+hi)/2)
            if len(roots) >= kmax: break
        s, prev = s2, v2
    return roots

print("=== (a) tau<2 for wells with sign-consistent mode2? ===")
max_tau = mp.mpf('0'); worst = None
Rvals = [1.05, 1.1, 1.2, 1.5, 2, 4, 10, 100, 1000, 10000]
grid = [i/20 for i in range(1,20)]
for R in Rvals:
    m = mp.sqrt(mp.mpf(R))
    for a in grid:
        for b in grid:
            if not a < b: continue
            roots = solve_modes(a, b, m, kmax=2)
            if len(roots) < 2: continue
            s1, s2 = roots
            A2 = m*s2*a; B2 = m*s2*(1-b)
            if not (A2 < mp.pi and B2 < mp.pi): continue
            c,sn = mp.cos(s2*(b-a)), mp.sin(s2*(b-a))
            sy2b = c*mp.sin(A2)/m + sn*mp.cos(A2)
            if not (sy2b < 0 and mp.sin(A2)/m > 0): continue
            tau = s2/s1
            if tau > max_tau:
                max_tau = tau; worst = (R,a,b)
print("max tau over grid:", mp.nstr(max_tau,12), "at", worst)
print("(uniform string limit tau->2 as R->1)")

print("\n=== (b) region II E=0 pairs: min x+y across (R,tau) grid, tau in (1,2) ===")
def region2_minxy(R, tau, n=1500):
    m = mp.sqrt(mp.mpf(R))
    xmid = mp.pi/(1+tau); xmax = mp.pi/tau
    if xmax <= xmid: return None, None
    xs = [xmid + (xmax-xmid)*i/n for i in range(1,n)]
    vals = [float(rtau(x,m,tau)) for x in xs]
    # critical indices
    crit = [i for i in range(1,len(xs)-1) if (vals[i]-vals[i-1])*(vals[i+1]-vals[i])<0]
    segs_idx = [0]+crit+[len(xs)-1]
    segs = [(segs_idx[k], segs_idx[k+1]) for k in range(len(segs_idx)-1) if segs_idx[k+1]>segs_idx[k]]
    minxy = mp.inf; best = None
    for si in range(len(segs)):
        for sj in range(si+1, len(segs)):
            i0,i1 = segs[si]; j0,j1 = segs[sj]
            vx = vals[i0:i1+1]; vy = vals[j0:j1+1]
            xl = xs[i0:i1+1]; yl = xs[j0:j1+1]
            lo,hi = min(vy), max(vy)
            inc = vy[-1] > vy[0]
            for k in range(len(vx)):
                t = vx[k]
                if t < lo-1e-12 or t > hi+1e-12: continue
                l,h = 0, len(yl)-1
                f = (lambda idx: vy[idx]-t) if inc else (lambda idx: t-vy[idx])
                if f(0)*f(len(yl)-1) > 1e-12: continue
                l,h = 0, len(yl)-1
                for _ in range(50):
                    mid = (l+h)//2
                    if f(mid)<=0: h=mid
                    else: l=mid+1
                for idx in [l,l+1,l-1]:
                    if 0<=idx<len(yl) and abs(vx[k]-vy[idx])<1e-8:
                        x,y = xl[k], yl[idx]
                        if x < y-1e-8:
                            if x+y < minxy:
                                minxy = x+y; best=(x,y,t)
    return minxy, best

global_min = mp.inf; global_worst=None; counts = 0
for R in [2,3,4,6,10,20,50,100,200,400,1000]:
    for ti in range(10, 21):
        tau = mp.mpf(ti)/10  # 1.0..2.0
        if tau <= 1.0: continue
        minxy, best = region2_minxy(R, tau)
        if minxy is not None:
            counts += 1
            if minxy < global_min:
                global_min = minxy; global_worst=(R, tau, best)
print("grids with pairs found:", counts, "/ 110")
print("global min x+y =", mp.nstr(global_min,10), " vs pi =", mp.nstr(mp.pi,10))
print("at (R, tau, best) =", global_worst[0], global_worst[1], "pair", [round(float(v),6) for v in global_worst[2]])
