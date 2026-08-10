import numpy as np

def band_edges(alpha, R, lam_hi=300.0, npts=300000):
    """cell: a=1 on [0,alpha], A=R on [alpha,1]. Return top of band1, bottom of band2."""
    roots_p = []; roots_a = []
    prev_p = prev_a = None
    for lam in np.linspace(1e-4, lam_hi, npts):
        M = np.eye(2)
        for (L, c) in [(alpha, 1.0), (1-alpha, R)]:
            w = np.sqrt(lam*c)
            T = np.array([[np.cos(w*L), np.sin(w*L)/w],[-w*np.sin(w*L), np.cos(w*L)]])
            M = M @ T
        dp = np.linalg.det(M - np.eye(2))
        da = np.linalg.det(M + np.eye(2))
        if prev_p is not None and dp*prev_p < 0: roots_p.append(lam)
        if prev_a is not None and da*prev_a < 0: roots_a.append(lam)
        prev_p, prev_a = dp, da
    roots_p = np.array(roots_p); roots_a = np.array(roots_a)
    return roots_p, roots_a

print("=== band-edge ratio for cell a(alpha)|A(1-alpha), R=4 ===")
best = (0.0, None, None)
for alpha in np.linspace(0.1, 0.95, 18):
    rp, ra = band_edges(alpha, 4.0)
    if len(rp) < 2 or len(ra) < 2: continue
    m1 = max(rp[0], ra[0]); m2 = min(rp[1], ra[1])
    r = m2/m1
    if r > best[0]: best = (r, alpha, (rp[:2], ra[:2]))
    print(f"alpha={alpha:.2f}: per={np.round(rp[:2],3)} anti={np.round(ra[:2],3)}  top1={m1:.4f} bot2={m2:.4f}  ratio={r:.4f}")
print("\nbest:", best)
