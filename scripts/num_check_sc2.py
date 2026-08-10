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

def build(p, R):
    jumps = sorted(list(p) + [1.0-q for q in p])
    pts = [0.0]+jumps+[1.0]
    vals = [R if i%2==1 else 1.0 for i in range(len(pts)-1)]
    return jumps, vals

def eigfunc(jumps, vals, lam, xpts, norm=True):
    xs = [0.0] + list(jumps) + [1.0]
    out = np.zeros_like(xpts)
    vals_at = np.zeros_like(xpts)
    for kk, xx in enumerate(xpts):
        i = 0
        while i < len(xs)-1 and xx > xs[i+1] + 1e-14: i += 1
        vals_at[kk] = vals[i]
        M = np.eye(2)
        j = 0
        while j < len(xs)-1 and xx > xs[j+1] + 1e-14:
            L = xs[j+1]-xs[j]; c = vals[j]; w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
            j += 1
        c = vals[j]; w = np.sqrt(lam*c); L = xx - xs[j]
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        v = M @ np.array([0.0, 1.0])
        out[kk] = v[0]
    if norm:
        mass = np.trapezoid(vals_at*out**2, xpts)
        out = out/np.sqrt(mass)
    return out

configs = {
    2: [0.249976, 0.374984],
    3: [0.181448, 0.272556, 0.454529],
    4: [0.134569, 0.210215, 0.354807, 0.427197],
}
xg = np.linspace(0.0005, 0.9995, 4000)
for n, p in configs.items():
    jumps, vals = build(p, 4.0)
    lam = eigs_fast(jumps, vals, k=n+2)
    yn = eigfunc(jumps, vals, lam[n-1], xg)
    ynp = eigfunc(jumps, vals, lam[n], xg)
    ratio = lam[n]/lam[n-1]
    pts = [0.0]+jumps+[1.0]
    violA = 0.0; viola = 0.0
    for i in range(len(pts)-1):
        mask = (xg>=pts[i])&(xg<=pts[i+1])
        d = np.abs(yn[mask]) - np.abs(ynp[mask])
        if vals[i] == 4.0:
            violA = max(violA, -d.min() if d.size else 0.0)
        else:
            viola = max(viola, d.max() if d.size else 0.0)
    jc = []
    for jp in jumps:
        i = np.argmin(np.abs(xg-jp))
        jc.append(abs(abs(yn[i])-abs(ynp[i])))
    print(f"n={n}: ratio={ratio:.6f}  violA={violA:.2e}  viola={viola:.2e}  jumpdiff={max(jc):.2e}")
