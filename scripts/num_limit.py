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
    w_a = sR*t; w_A = t
    jumps = []
    x = 0.0
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

# 1) self-consistency of conjectured configs n=5..8 (R=4): check jump cond via eigenfunction ratio
def y_at(jumps, vals, lam, x):
    xs = [0.0] + list(jumps) + [1.0]
    M = np.eye(2)
    i = 0
    while i < len(xs)-1 and x > xs[i+1] + 1e-14:
        L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lam*c)
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        i += 1
    c = vals[i]; w = np.sqrt(lam*c); L = x - xs[i]
    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
    M = M @ T
    v = M @ np.array([0.0, 1.0])
    return v[0]

def check_sc(n, R):
    jumps, vals = conj_config(n, R)
    lam = eigs_fast(jumps, vals, k=n+2)
    ln, lp = lam[n-1], lam[n]
    def norm_fac(lamj):
        xs = [0.0]+jumps+[1.0]
        tot = 0.0
        for i in range(len(xs)-1):
            L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lamj*c)
            A_ = y_at(jumps, vals, lamj, xs[i]); B_ = y_at(jumps, vals, lamj, xs[i+1])
            if abs(np.sin(w*L)) < 1e-10: tot += A_**2*L; continue
            b = (B_ - A_*np.cos(w*L))/np.sin(w*L); aa = A_
            I1 = 0.5*L - 0.25*np.sin(2*w*L)/w
            I2 = 0.5*L + 0.25*np.sin(2*w*L)/w
            I12 = 0.5*(1-np.cos(2*w*L))/(2*w)
            tot += c*(aa*aa*I1 + b*b*I2 + 2*aa*b*I12)
        return tot
    fn, fp = norm_fac(ln), norm_fac(lp)
    worst = 0.0
    for pk in jumps:
        yl = y_at(jumps, vals, ln, pk)/np.sqrt(fn)
        yp = y_at(jumps, vals, lp, pk)/np.sqrt(fp)
        worst = max(worst, abs(yl*yl - yp*yp))
    return lam[n]/lam[n-1], worst

print("=== self-consistency of conjectured configs (R=4) ===")
for n in range(1, 9):
    r, w = check_sc(n, 4.0)
    print(f"n={n}: ratio={r:.8f}  jump-cond worst={w:.1e}")

# 2) limit: n-periodic cell a(2/3)|A(1/3): band edges
print()
print("=== band edges of cell a(2/3)|A(1/3), R=4 (limit of c_n as n->inf) ===")
# periodic problem on [0,1]: bands of cell a on [0,2/3], A on [2/3,1]
# band edges = eigenvalues of cell with per/anti-per BC: solve via transfer matrix
def cell_eigs(bc):
    # cell: a on [0, 2/3] (rho=1), A on [2/3,1] (rho=4)
    jumps=[2/3]; vals=[1.0,4.0]
    out=[]
    for lam in np.linspace(0.01, 250, 50000):
        M=np.eye(2)
        for i in range(2):
            L = (2/3) if i==0 else (1/3)
            c = vals[i]; w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        # periodic: y(1)=y(0), y'(1)=y'(0): (M - I)v = 0 with y(0)=0 => need M01 ~ 0 and M00=1... 
        # actually for periodic BC with y(0)=0: y(1)=M01*y'(0) = 0 and y'(1)=M11 y'(0) = y'(0): 
        # conditions: M01=0 and M11=1. For anti-periodic: y(1)=-y(0)=0: M01=0, M11=-1.
        if bc=='per':
            if abs(M[0,1]) < 1e-6 and abs(M[1,1]-1) < 1e-6: out.append(lam)
        else:
            if abs(M[0,1]) < 1e-6 and abs(M[1,1]+1) < 1e-6: out.append(lam)
    return out
# simpler: eigenvalue condition for band edges via det((M-I)_{2x2}) = 0 (periodic) and det(M+I)=0 (anti)
def band_edges():
    res = {'per': [], 'anti': []}
    for lam in np.linspace(0.02, 300, 200000):
        M=np.eye(2)
        for i,(L,c) in enumerate([(2/3,1.0),(1/3,4.0)]):
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        dper = np.linalg.det(M - np.eye(2))
        danti = np.linalg.det(M + np.eye(2))
        for key, d in [('per', dper), ('anti', danti)]:
            if len(res[key]) and (d * res[key][-1][1]) < 0:
                res[key][-1] = (res[key][-1][0], 0.0)  # mark
                res[key].append((lam, d))
            else:
                res[key].append((lam, d))
    return res
# rough: just scan for sign changes
res = {'per': [], 'anti': []}
prev = {'per': None, 'anti': None}
lam0 = 0.02
M0 = np.eye(2)
for i,(L,c) in enumerate([(2/3,1.0),(1/3,4.0)]):
    w = np.sqrt(lam0*c)
    T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
    M0 = M0 @ T
p0 = np.linalg.det(M0-np.eye(2)); a0 = np.linalg.det(M0+np.eye(2))
for lam in np.linspace(0.02, 300, 300000):
    M=np.eye(2)
    for (L,c) in [(2/3,1.0),(1/3,4.0)]:
        w = np.sqrt(lam*c)
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
    dp = np.linalg.det(M-np.eye(2)); da = np.linalg.det(M+np.eye(2))
    if prev['per'] is not None and dp*prev['per'] < 0: res['per'].append(lam)
    if prev['anti'] is not None and da*prev['anti'] < 0: res['anti'].append(lam)
    prev['per'], prev['anti'] = dp, da
print("periodic BC roots:", [round(q,4) for q in res['per']][:8])
print("anti-periodic BC roots:", [round(q,4) for q in res['anti']][:8])
