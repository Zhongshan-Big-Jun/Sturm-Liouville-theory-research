import numpy as np

def bands_of_cell(alpha, R, lam_hi=400.0, npts=200000):
    """Return list of bands [lo,hi] where |tr M|<=2 (M = cell transfer matrix)."""
    trs = np.zeros(npts)
    lams = np.linspace(1e-4, lam_hi, npts)
    for i, lam in enumerate(lams):
        M = np.eye(2)
        for (L, c) in [(alpha, 1.0), (1-alpha, R)]:
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        trs[i] = M[0,0]+M[1,1]
    inside = np.abs(trs) <= 2.0
    bands = []
    i = 0
    while i < npts:
        if inside[i]:
            j = i
            while j+1 < npts and inside[j+1]: j += 1
            bands.append((lams[i], lams[j]))
            i = j+1
        else:
            i += 1
    return bands

print("=== bands of cell a(alpha)|A(1-alpha), R=4; ratio bottom2/top1 ===")
best = (0.0, None)
for alpha in np.linspace(0.2, 0.95, 16):
    b = bands_of_cell(alpha, 4.0)
    if len(b) < 2: 
        print(f"alpha={alpha:.2f}: bands={[(round(x,2),round(y,2)) for x,y in b]}")
        continue
    top1 = b[0][1]; bot2 = b[1][0]
    r = bot2/top1
    if r > best[0]: best = (r, alpha)
    print(f"alpha={alpha:.2f}: bands={[(round(x,2),round(y,2)) for x,y in b[:3]]}  ratio={r:.4f}")
print("best:", best)
