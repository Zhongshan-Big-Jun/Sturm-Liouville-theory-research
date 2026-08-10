import numpy as np

def trace_cell_opt(u, v, R, w):
    """trace of cell transfer matrix in optical coordinates; equation y_ss=-lam y on pieces,
    derivative jump x1/sqrt(R) at a->A, x sqrt(R) at A->a; w = sqrt(lam)."""
    g = np.sqrt(R) + 1.0/np.sqrt(R)
    return 2.0*np.cos(w*u)*np.cos(w*v) - g*np.sin(w*u)*np.sin(w*v)

def band_edges_opt(u, v, R, wmax=200.0, npts=400000):
    w = np.linspace(1e-5, wmax, npts)
    tr = trace_cell_opt(u, v, R, w)
    # tr = -2 crossings (band1 top, band2 bottom)
    cross = np.nonzero((tr[:-1]+2.0)*(tr[1:]+2.0) <= 0.0)[0]
    if len(cross) < 2:
        return None
    # refine first two crossings
    out = []
    for ci in cross[:2]:
        wlo, whi = w[ci], w[ci+1]
        for _ in range(80):
            wm = 0.5*(wlo+whi)
            if (trace_cell_opt(u,v,R,wlo)+2.0)*(trace_cell_opt(u,v,R,wm)+2.0) <= 0.0:
                whi = wm
            else:
                wlo = wm
        out.append(0.5*(wlo+whi))
    return (out[1]/out[0])**2, out[0], out[1]

# 1) balanced cell closed form vs direct
import math
for R in [2.0, 4.0, 100.0]:
    beta = (math.sqrt(R)-1.0)/(math.sqrt(R)+1.0)
    th0 = math.acos(beta)
    closed = ((math.pi-th0)/th0)**2
    print(f"R={R}: balanced closed form c_inf^bal = {closed:.10f}")
    print(f"      direct (u=v=1): {band_edges_opt(1.0,1.0,R)}")
print()

# 2) maximize over cell shapes (u:v), u+v=2
print("=== max band-edge ratio over cell shape (optical coords) ===")
for R in [2.0, 4.0, 10.0, 100.0]:
    best = (0.0, None, None)
    for delta in np.linspace(-0.95, 0.95, 191):
        u, v = 1.0+delta, 1.0-delta
        if u <= 1e-6 or v <= 1e-6: continue
        r = band_edges_opt(u, v, R)
        if r is not None and r[0] > best[0]:
            best = (r[0], u, v)
    print(f"R={R}: max={best[0]:.10f} at u={best[1]:.4f}, v={best[2]:.4f}")
