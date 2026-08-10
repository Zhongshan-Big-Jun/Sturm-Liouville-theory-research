import numpy as np, time

def fd_eigs(rho, N=800, k=5):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def build_pts(pts, R, N):
    rho = np.ones(N)
    for k in range(0, len(pts), 2):
        rho[int(round(pts[k]*N)):int(round(pts[k+1]*N))] = R
    return rho

def F_pts(pts, R, N=800):
    lam = fd_eigs(build_pts(pts, R, N), N, 4)
    return lam[2]/lam[1]

def coord_ascent_pts(pts0, R, itmax=30, h=0.004):
    pts = list(pts0)
    n = len(pts)
    for it in range(itmax):
        improved = False
        for k in range(n):
            lo = (pts[k-1]+h) if k>0 else h
            hi = (pts[k+1]-h) if k<n-1 else 1-h
            if hi <= lo: continue
            fk = lambda t: F_pts(pts[:k]+[t]+pts[k+1:], R)
            f0 = fk(pts[k])
            # coarse scan + golden
            tg = np.linspace(lo, hi, 18)
            vg = np.array([fk(t) for t in tg])
            i = np.argmax(vg)
            gr = (np.sqrt(5)-1)/2
            a, b = tg[max(0,i-1)], tg[min(len(tg)-1,i+1)]
            c = b-gr*(b-a); d = a+gr*(b-a); fc, fd = fk(c), fk(d)
            for _ in range(40):
                if fc > fd:
                    a, c, fd = c, d, fc
                    c = b-gr*(b-a); fc = fk(c)
                else:
                    b, d, fc = d, c, fd
                    d = a+gr*(b-a); fd = fk(d)
            tb = 0.5*(a+b)
            if fk(tb) > f0 + 1e-10:
                pts[k] = tb; improved = True
        if not improved: break
    return pts, F_pts(pts, R)

rng = np.random.default_rng(11)
R = 4.0
found = []
t0 = time.time()
for trial in range(120):
    nint = rng.integers(1, 4)
    pts = np.sort(rng.uniform(0.03, 0.97, 2*nint))
    pts2, val = coord_ascent_pts(pts, R)
    # snap to 3 decimals, check if new
    key = tuple(np.round(pts2, 3))
    exists = any(np.allclose(np.array(key), np.array(k2), atol=0.01) for (_, k2) in found)
    if not exists:
        found.append((val, key))
    if trial % 20 == 0: print(f"trial {trial}, distinct so far {len(found)}, {time.time()-t0:.0f}s")
print("=== distinct local maxima (lam3/lam2, R=4) ===")
for val, key in sorted(found, reverse=True)[:10]:
    print(f"  ratio={val:.5f} at {key}")
