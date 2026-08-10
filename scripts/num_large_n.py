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
    return jumps, vals

print("=== conjectured config c_n, R=4, large n ===")
for n in [10, 20, 30, 50, 80, 120]:
    jumps, vals = conj_config(n, 4.0)
    lam = eigs_fast(jumps, vals, k=n+3)
    print(f"n={n}: ratio={lam[n]/lam[n-1]:.8f}")
