import numpy as np

N = 2000
h = 1.0/(N+1)
xg = np.linspace(h, 1-h, N)

def eigs_exact(jumps, vals, k=8):
    xs = [0.0] + list(jumps) + [1.0]
    A = max(vals); a = min(vals)
    lam_hi = (A/a)*((k+2)**2)*(np.pi**2)*4 + 2.0
    npts = 80000
    s = np.linspace(1e-6, np.sqrt(lam_hi), npts)
    M00 = np.ones(len(s)); M01 = np.zeros(len(s)); M10 = np.zeros(len(s)); M11 = np.ones(len(s))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(s**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    d = M01
    roots = []
    for i in range(npts-1):
        if d[i]*d[i+1] < 0:
            lo, hi = s[i], s[i+1]
            for _ in range(4):
                sg = np.linspace(lo, hi, 400)
                dg = _det(sg, xs, vals)
                sgn = np.signbit(dg[1:]) != np.signbit(dg[:-1])
                jj = np.nonzero(sgn)[0]
                if len(jj)==0: break
                lo, hi = sg[jj[0]], sg[jj[0]+1]
            roots.append(((lo+hi)/2)**2)
            if len(roots) >= k: break
    return np.array(sorted(roots)[:k])

def _det(sg, xs, vals):
    M00 = np.ones(len(sg)); M01 = np.zeros(len(sg)); M10 = np.zeros(len(sg)); M11 = np.ones(len(sg))
    for i in range(len(xs)-1):
        L = xs[i+1]-xs[i]
        c = vals[i]
        w = np.sqrt(np.maximum(sg**2*c, 0.0))
        wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        n00 = M00*cw + M01*sw2
        n01 = M00*sw + M01*cw
        n10 = M10*cw + M11*sw2
        n11 = M10*sw + M11*cw
        M00,M01,M10,M11 = n00,n01,n10,n11
    return M01

def eigfunc(jumps, vals, lam, xpts):
    """value of Dirichlet eigenfunction (y(0)=0, y'(0)=1) at xpts"""
    xs = [0.0] + list(jumps) + [1.0]
    out = np.zeros_like(xpts)
    for kk, xx in enumerate(xpts):
        M = np.eye(2)
        i = 0
        while i < len(xs)-1 and xx > xs[i+1] + 1e-14:
            L = xs[i+1]-xs[i]; c = vals[i]; w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
            i += 1
        c = vals[i]; w = np.sqrt(lam*c); L = xx - xs[i]
        T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
        M = M @ T
        v = M @ np.array([0.0, 1.0])
        out[kk] = v[0]
    return out

# best symmetric 2-interval from scan
u, v = 0.25258426966292136, 0.375097841181669
jumps = [u, v, 1-v, 1-u]
vals = [1.0, 4.0, 1.0, 4.0, 1.0]
lam = eigs_exact(jumps, vals, k=4)
print("lam:", np.round(lam, 6))
print("lam3/lam2 =", lam[2]/lam[1])
y2 = eigfunc(jumps, vals, lam[1], xg)
y3 = eigfunc(jumps, vals, lam[2], xg)
# check sign condition: A-regions should have |y2|>=|y3|
okA = np.all(np.abs(y2[(xg>=u)&(xg<=v)]) >= np.abs(y3[(xg>=u)&(xg<=v)]))
oka = np.all(np.abs(y2[(xg>v)&(xg<1-v)]) <= np.abs(y3[(xg>v)&(xg<1-v)]))
print("A-regions |y2|>=|y3|:", okA, " a-regions |y2|<=|y3|:", oka)
# where are zeros of y3?
zs = xg[np.abs(y3) < 0.01*np.max(np.abs(y3))]
print("y3 near-zeros:", np.round(zs, 4))
# check jump points solve |y2|=|y3|
for jp in jumps:
    i = np.argmin(np.abs(xg-jp))
    print(f"jump {jp:.4f}: |y2|={np.abs(y2[i]):.4f} |y3|={np.abs(y3[i]):.4f} diff={np.abs(y2[i])-np.abs(y3[i]):.2e}")
