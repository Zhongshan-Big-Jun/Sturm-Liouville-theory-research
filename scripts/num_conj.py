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
            jj = np.nonzero(sg_signs)[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def conj_config(n, R):
    """conjectured extremizer: alternating a (width sqrt(R) t), A (width t), symmetric, starting with a."""
    sR = np.sqrt(R)
    t = 1.0/((n+1)*sR + n)
    w_a = sR*t; w_A = t
    jumps = []
    x = 0.0
    k = 0
    while True:
        x += w_a
        if x < 1.0: jumps.append(x)
        x += w_A
        if x < 1.0: jumps.append(x)
        k += 1
        if x >= 1.0: break
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = [R if i%2==1 else 1.0 for i in range(len(pts)-1)]
    return jumps, vals

print("=== conjectured configs: exact ratios (R=4) ===")
for n in range(1, 9):
    jumps, vals = conj_config(n, 4.0)
    lam = eigs_fast(jumps, vals, k=n+3)
    print(f"n={n}: ratio={lam[n]/lam[n-1]:.8f}  jumps[:5]={jumps[:5]}")

print()
print("=== R-dependence for n=2: conjectured config vs computed critical point ===")
for R in [2.0, 3.0, 4.0, 10.0, 100.0]:
    jumps, vals = conj_config(2, R)
    lam = eigs_fast(jumps, vals, k=4)
    print(f"R={R:6.1f}: conj ratio={lam[2]/lam[1]:.8f}")
