import numpy as np, math

def g(w, d, R):
    """cos^2(w)/cos^2(d*w); band edges satisfy g = kappa"""
    beta = (math.sqrt(R)-1.0)/(math.sqrt(R)+1.0)
    kappa = beta*beta
    return kappa - (np.cos(w)**2)/(np.cos(d*w)**2)

def roots(d, R, wmax):
    w = np.linspace(1e-6, wmax, 300000)
    f = g(w, d, R)
    sgn = np.signbit(f[1:]) != np.signbit(f[:-1])
    idx = np.nonzero(sgn)[0]
    out = []
    for i in idx:
        wlo, whi = w[i], w[i+1]
        for _ in range(60):
            wm = 0.5*(wlo+whi)
            if g(wlo,d,R)*g(wm,d,R) <= 0: whi = wm
            else: wlo = wm
        out.append(0.5*(wlo+whi))
        if len(out) >= 2: break
    return out

for R in [2.0, 4.0, 10.0, 100.0]:
    print(f"R={R}: monotonicity check d -> w1 (should increase), w2 (should decrease), ratio (decrease)")
    prev = None
    for d in np.linspace(0.0, 0.93, 20):
        rs = roots(d, R, 4.0)
        if len(rs) < 2: 
            print(f"  d={d:.2f}: fewer than 2 roots"); continue
        w1, w2 = rs[0], rs[1]
        ratio = (w2/w1)**2
        mark = ""
        if prev is not None:
            if not (w1 >= prev[0]-1e-9): mark += " W1-NOT-INC"
            if not (w2 <= prev[1]+1e-9): mark += " W2-NOT-DEC"
            if not (ratio <= prev[2]+1e-9): mark += " RATIO-NOT-DEC"
        prev = (w1, w2, ratio)
        if mark: print(f"  d={d:.2f}: w1={w1:.6f} w2={w2:.6f} ratio={ratio:.6f}{mark}")
    print("  (no output above means all monotone)")
    print()
