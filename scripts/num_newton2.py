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

def F(p, R, n):
    jumps, vals = build(p, R)
    lam = eigs_fast(jumps, vals, k=n+2)
    ln, lp = lam[n-1], lam[n]
    def norm_fac(lamj):
        xs = [0.0]+jumps+[1.0]
        tot = 0.0
        for i in range(len(xs)-1):
            L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lamj*c)
            A_ = y_at(jumps, vals, lamj, xs[i]); B_ = y_at(jumps, vals, lamj, xs[i+1])
            if abs(np.sin(w*L)) < 1e-10:
                tot += A_**2 * L
                continue
            b = (B_ - A_*np.cos(w*L))/np.sin(w*L)
            aa = A_
            I1 = 0.5*L - 0.25*np.sin(2*w*L)/w
            I2 = 0.5*L + 0.25*np.sin(2*w*L)/w
            I12 = 0.5*(1-np.cos(2*w*L))/(2*w)
            tot += c*(aa*aa*I1 + b*b*I2 + 2*aa*b*I12)
        return tot
    fn = norm_fac(ln); fp = norm_fac(lp)
    out = []
    for pk in p:
        yl = y_at(jumps, vals, ln, pk)/np.sqrt(fn)
        yp = y_at(jumps, vals, lp, pk)/np.sqrt(fp)
        out.append(yl*yl - yp*yp)
    return np.array(out), lam

def newton(p0, R, n, tol=1e-11, maxit=40):
    p = np.array(p0, float)
    for it in range(maxit):
        Fv, lam = F(p, R, n)
        if np.max(np.abs(Fv)) < tol: break
        J = np.zeros((len(p), len(p)))
        for k in range(len(p)):
            eps = 1e-6
            p2 = p.copy(); p2[k] += eps
            Fv2, _ = F(p2, R, n)
            J[:, k] = (Fv2 - Fv)/eps
        try: dp = np.linalg.solve(J, -Fv)
        except np.linalg.LinAlgError: break
        alpha = 1.0
        for _ in range(20):
            pn = p + alpha*dp
            if np.all(pn[1:] > pn[:-1]) and pn[0] > 0.003 and pn[-1] < 0.497:
                Fn, _ = F(pn, R, n)
                if np.max(np.abs(Fn)) < np.max(np.abs(Fv)): break
            alpha *= 0.5
        p = p + alpha*dp
    Fv, lam = F(p, R, n)
    return p, lam, np.max(np.abs(Fv))

# test w_a/w_A = sqrt(R) hypothesis for various (R, n)
import itertools
for R, n in [(2.0,2),(10.0,2),(4.0,5),(4.0,6),(100.0,2)]:
    sR = np.sqrt(R)
    t = 1.0/((n+1)*sR + n)
    p0 = []
    for k in range(1, n+1):
        # A-region k spans [(2k-1)*t... hmm: pattern a(2t... wait general: a w_a=sR*t, A w=t
        # a: [0, w_a], A: [w_a, w_a+w], a: [w_a+w, 2w_a+w], A: [2w_a+w, 2w_a+2w], ...
        # p list: jumps within [0,0.5] = left edges/right edges of A-regions in left half
        pass
    # build p0 from pattern: A-region k in left half: [a_cum, a_cum+w]
    p0 = []
    x0 = 0.0
    for k in range(1, n+1):
        x0 += sR*t        # end of a-piece
        left = x0
        x0 += t           # end of A-piece
        if x0 <= 0.5 + 1e-9:
            p0.append(left); p0.append(x0)
        if x0 >= 0.5: break
    p0 = p0[:2*n]
    # ensure n jumps on [0,0.5]: take first n
    p, lam, res = newton(p0[:n], R, n)
    w_a = p[0]
    w_A = p[1]-p[0]
    print(f"R={R:5.1f} n={n}: p=[{', '.join(f'{q:.8f}' for q in p)}]  w_a={w_a:.8f} w_A={w_A:.8f}  w_a/w_A={w_a/w_A:.6f} (sqrt(R)={sR:.6f})  ratio={lam[n]/lam[n-1]:.8f}  |F|={res:.1e}")
