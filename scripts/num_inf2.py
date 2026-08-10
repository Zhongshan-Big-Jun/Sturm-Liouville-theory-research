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
    s = np.linspace(1e-6, np.sqrt(lam_hi), 50000)
    d = _det_scan(jumps, vals, s)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx:
        slo, shi = s[i], s[i+1]
        for _ in range(5):
            sg = np.linspace(slo, shi, 800)
            dg = _det_scan(jumps, vals, sg)
            jj = np.nonzero(np.signbit(dg[1:]) != np.signbit(dg[:-1]))[0]
            if len(jj) == 0: break
            slo, shi = sg[jj[0]], sg[jj[0]+1]
        out.append(((slo+shi)/2)**2)
        if len(out) >= k: break
    return np.array(sorted(out)[:k])

# n=1 inf: A(c), a(1-2c), A(c): find min of lambda2/l1 over c
print("=== n=1 inf: A(c), a(1-2c), A(c), R=4: refine around c=0.25 ===")
best = (1e9, None)
for c in np.linspace(0.240, 0.260, 401):
    jumps = [c, 1-c]; vals = [4.0, 1.0, 4.0]
    lam = eigs_fast(jumps, vals, k=2)
    r = lam[1]/lam[0]
    if r < best[0]: best = (r, c)
print(f"min lambda2/l1 = {best[0]:.10f} at c = {best[1]:.6f}")
# compare with balanced closed form
import math
R=4.0; beta=(math.sqrt(R)-1)/(math.sqrt(R)+1); th0=math.acos(beta)
print(f"balanced band-edge ratio ((pi-th0)/th0)^2 = {((math.pi-th0)/th0)**2:.10f}")

# n=2 inf: two families with same jump pattern [1/7,3/7,4/7,6/7], values swapped
print()
print("=== n=2 inf: both value assignments at jumps [1/7,3/7,4/7,6/7] ===")
jumps = [1.0/7, 3.0/7, 4.0/7, 6.0/7]
for name, vals in [("a,A,a,A,a (a-ends)", [1.0,4.0,1.0,4.0,1.0]),
                   ("A,a,A,a,A (A-ends)", [4.0,1.0,4.0,1.0,4.0])]:
    lam = eigs_fast(jumps, vals, k=3)
    print(f"{name}: lambda3/l2 = {lam[2]/lam[1]:.8f}")

# n=2 inf: fine scan of the A,a,A,a,A family around wr=2
print()
print("=== n=2 inf: A,a,A,a,A family (wr = w_a/w_A) fine scan ===")
best = (1e9, None)
for wr in np.linspace(1.7, 2.3, 601):
    t = 1.0/((n+1)*1.0 + n*wr) if False else None
    # A-blocks width t, a-blocks width wr*t: total (n+1)*t + n*wr*t = 1, n=2
    t = 1.0/(3 + 2*wr)
    jumps = []; x=0.0
    # A(t), a(wr t), A(t), a(wr t), A(t)
    seq = [t, wr*t, t, wr*t, t]
    x = 0.0
    js = []
    for L in seq:
        x += L
        if x < 1.0: js.append(x)
    js = sorted(set(round(j,12) for j in js))
    pts = [0.0]+js+[1.0]
    vals = [4.0 if i%2==0 else 1.0 for i in range(len(pts)-1)]
    lam = eigs_fast(js, vals, k=3)
    r = lam[2]/lam[1]
    if r < best[0]: best = (r, wr)
print(f"min = {best[0]:.10f} at w_a/w_A = {best[1]:.6f}")
