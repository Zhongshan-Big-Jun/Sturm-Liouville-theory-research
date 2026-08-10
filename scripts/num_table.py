import numpy as np

def _det_scan(jumps, vals, s_grid):
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigs_fast(jumps, vals, k=8):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    s = np.linspace(1e-6, np.sqrt(lam_hi), 30000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(4):
            sg = np.linspace(slo, shi, 400)
            dg = _det_scan(jumps, vals, sg)
            sg_signs = np.signbit(dg[1:]) != np.signbit(dg[:-1])
            jj = np.nongzero(sg_signs)[0] if False else np.nonzero(sg_signs)[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def c_n(n, R):
    sR = np.sqrt(R)
    t = 1.0/((n+1)*sR + n)
    jumps = []
    x = 0.0
    while True:
        x += sR*t
        if x < 1.0: jumps.append(x)
        x += t
        if x < 1.0: jumps.append(x)
        if x >= 1.0: break
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = [R if i%2==1 else 1.0 for i in range(len(pts)-1)]
    lam = eigs_fast(jumps, vals, k=n+3)
    return lam[n]/lam[n-1], lam[n-1], lam[n]

print("=== c_n(R) table: lambda_{n+1}/lambda_n for conjectured extremizer (a=1) ===")
Rs = [2.0, 3.0, 4.0, 10.0, 100.0]
hdr = "n   " + "".join(f"R={r:<4.0f}      " for r in Rs)
print(hdr)
for n in [1,2,3,4,5,6]:
    row = f"{n}   "
    for R in Rs:
        c, l1, l2 = c_n(n, R)
        row += f"{c:<14.7f}"
    print(row)

print()
print("=== c_inf(R) = optimal band-edge ratio (max over alpha of bot2/top1) ===")
def band_ratio(alpha, R, lam_hi=600.0, npts=150000):
    lams = np.linspace(1e-4, lam_hi, npts)
    inside_prev = None
    bands = []
    for i, lam in enumerate(lams):
        M = np.eye(2)
        for (L, c) in [(alpha, 1.0), (1-alpha, R)]:
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        tr = M[0,0]+M[1,1]
        inside = abs(tr) <= 2.0
        if inside and (inside_prev is False or inside_prev is None):
            lo = lam
        if (not inside) and inside_prev is True:
            bands.append((lo, lam))
        inside_prev = inside
    if inside_prev: bands.append((lo, lams[-1]))
    if len(bands) < 2: return None
    return bands[1][0]/bands[0][1]
for R in [2.0, 3.0, 4.0, 10.0, 100.0]:
    best = (0.0, None)
    for alpha in np.linspace(0.2, 0.95, 30):
        r = band_ratio(alpha, R)
        if r is not None and r > best[0]: best = (r, alpha)
    print(f"R={R:6.1f}: c_inf={best[0]:.6f} at alpha={best[1]:.3f}")
