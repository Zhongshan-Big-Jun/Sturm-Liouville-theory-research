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

# ---- 1) verify pointwise counterexample ----
jumps = [0.1072, 0.1364, 0.2122, 0.3473, 0.6721, 0.8453]
pts = [0.0]+jumps+[1.0]
for start in [1.0, 4.0]:
    vals = [start if i%2==0 else 4.0/start for i in range(len(pts)-1)]
    lam = eigs_fast(jumps, vals, k=4)
    r21, r32 = lam[1]/lam[0], lam[2]/lam[1]
    print(f"start={start}: lam={np.round(lam,5)}  r21={r21:.6f} r32={r32:.6f}  r32>r21: {r32>r21}")

# ---- 2) Keller sign pattern for balanced configs ----
def y_at(jumps, vals, lam, x):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.eye(2); i = 0
    while i < len(xs)-1 and x > xs[i+1] + 1e-14:
        L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lam*c)
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T; i += 1
    c = vals[i]; w = np.sqrt(lam*c); L = x - xs[i]
    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
    M = M @ T
    v = M @ np.array([0.0, 1.0])
    return v[0]

def mass_norm(jumps, vals, lamj):
    xs = [0.0]+jumps+[1.0]; tot = 0.0
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lamj*c)
        A_ = y_at(jumps, vals, lamj, xs[i]); B_ = y_at(jumps, vals, lamj, xs[i+1])
        if abs(np.sin(w*L)) < 1e-10:
            tot += A_**2*L*c; continue
        b = (B_ - A_*np.cos(w*L))/np.sin(w*L); a_ = A_
        I1 = 0.5*L - 0.25*np.sin(2*w*L)/w; I2 = 0.5*L + 0.25*np.sin(2*w*L)/w
        I12 = 0.5*(1-np.cos(2*w*L))/(2*w)
        tot += c*(a_*a_*I1 + b*b*I2 + 2*a_*b*I12)
    return tot

def conj_config(n, R):
    sR = np.sqrt(R); t = 1.0/((n+1)*sR + n)
    jumps = []; x = 0.0
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

print()
print("=== Keller sign pattern check (balanced config, R=4) ===")
for n in [2, 3]:
    jumps, vals = conj_config(n, 4.0)
    lam = eigs_fast(jumps, vals, k=n+2)
    ln, lp = lam[n-1], lam[n]
    fn, fp = mass_norm(jumps, vals, ln), mass_norm(jumps, vals, lp)
    pts = [0.0]+jumps+[1.0]
    ok_jump = True; ok_a = True; ok_A = True
    for pk in jumps:
        yn = y_at(jumps, vals, ln, pk)/np.sqrt(fn); yp = y_at(jumps, vals, lp, pk)/np.sqrt(fp)
        if abs(abs(yn)-abs(yp)) > 1e-6: ok_jump = False
    for i in range(len(pts)-1):
        mid = 0.5*(pts[i]+pts[i+1])
        yn = abs(y_at(jumps, vals, ln, mid))/np.sqrt(fn); yp = abs(y_at(jumps, vals, lp, mid))/np.sqrt(fp)
        isA = (vals[i] == 4.0)
        if isA and not (yn >= yp - 1e-6): ok_A = False
        if not isA and not (yn <= yp + 1e-6): ok_a = False
    print(f"n={n}: ratio={lam[n]/lam[n-1]:.8f}  |yn|=|yp| at jumps: {ok_jump}  A-reg yn>=yp: {ok_A}  a-reg yn<=yp: {ok_a}")
