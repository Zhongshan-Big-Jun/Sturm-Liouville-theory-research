import numpy as np

def band_ratio(alpha, R, lam_hi=800.0, npts=60000):
    lams = np.linspace(1e-4, lam_hi, npts)
    inside = np.zeros(npts, dtype=bool)
    for i, lam in enumerate(lams):
        M = np.eye(2)
        for (L, c) in [(alpha, 1.0), (1-alpha, R)]:
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        inside[i] = abs(M[0,0]+M[1,1]) <= 2.0
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
    if len(bands) < 2: return None
    return bands[1][0]/bands[0][1]

print("=== c_inf(R) = optimal band-edge ratio ===")
for R in [2.0, 4.0, 100.0]:
    best = (0.0, None)
    for alpha in np.linspace(0.2, 0.95, 16):
        r = band_ratio(alpha, R)
        if r is not None and r > best[0]: best = (r, alpha)
    print(f"R={R:6.1f}: c_inf={best[0]:.6f} at alpha={best[1]:.3f}")
