import numpy as np

def _det_scan(jumps, vals, s_grid):
    xs = [0.0] + list(jumps) + [1.0]
    M00 = np.ones(len(s_grid)); M01 = np.zeros(len(s_grid)); M10 = np.zeros(len(s_grid)); M11 = np.ones(len(s_grid))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]
        w = np.sqrt(np.maximum(s_grid**2*c, 0.0)); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2; n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2; n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigs_fast(jumps, vals, k=8):
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
            jj = np.nonzero(np.signbit(dg[1:]) != np.signbit(dg[:-1]))[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

def alt_config(n, R, wratio):
    """alternating a-A starting/ending with a, symmetric about 1/2, width ratio w_a/w_A = wratio.
    widths: w_a = wratio*t, w_A = t, t chosen so total length = 1."""
    t = 1.0/((n+1)*wratio + n)
    w_a = wratio*t; w_A = t
    jumps = []; x = 0.0
    while True:
        x += w_a
        if x < 1.0: jumps.append(x)
        x += w_A
        if x < 1.0: jumps.append(x)
        if x >= 1.0: break
    jumps = sorted(set(round(j,12) for j in jumps))
    pts = [0.0]+jumps+[1.0]
    vals = [R if i%2==1 else 1.0 for i in range(len(pts)-1)]
    return jumps, vals

print("=== width-ratio scan: alternating symmetric config, R=4 (sqrt(R)=2 optimal?) ===")
for n in [2, 3, 4]:
    best = (0.0, None)
    for wr in np.linspace(0.5, 6.0, 111):
        jumps, vals = alt_config(n, 4.0, wr)
        lam = eigs_fast(jumps, vals, k=n+2)
        r = lam[n]/lam[n-1]
        if r > best[0]: best = (r, wr)
    print(f"n={n}: max ratio={best[0]:.6f} at w_a/w_A={best[1]:.3f} (sqrt(R)=2.000, conj ratio 4.2847/3.4539/3.0912)")
print()

print("=== pointwise-monotonicity adversarial: maximize lambda3/l2 - lambda2/l1 ===")
rng = np.random.default_rng(777)
best_diff = (-1e9, None); best_plain3 = (0.0, None)
for trial in range(6000):
    nj = rng.integers(2, 10)
    jumps = np.sort(rng.uniform(0.01, 0.99, nj))
    pts = [0.0]+list(jumps)+[1.0]
    start = rng.choice([1.0, 4.0])
    vals = [start if i%2==0 else 4.0/start for i in range(len(pts)-1)]
    lam = eigs_fast(list(jumps), vals, k=4)
    r21 = lam[1]/lam[0]; r32 = lam[2]/lam[1]
    d = r32 - r21
    if d > best_diff[0]: best_diff = (d, (jumps, vals, r21, r32))
    if r32 > best_plain3[0]: best_plain3 = (r32, (jumps, vals, r21))
print(f"max (lambda3/l2 - lambda2/l1) = {best_diff[0]:.6f}  [config: r21={best_diff[1][2]:.4f}, r32={best_diff[1][3]:.4f}]")
print(f"  jumps = {np.round(best_diff[1][0],4)}")
print(f"max lambda3/l2 in this run = {best_plain3[0]:.6f} (r21={best_plain3[1][2]:.4f})")
