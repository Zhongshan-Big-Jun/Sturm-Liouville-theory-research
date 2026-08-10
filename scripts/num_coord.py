import numpy as np, time

def fd_eigs(rho, N=800, k=6):
    h = 1.0/(N+1)
    A = np.zeros((N,N))
    for i in range(N):
        A[i,i] = 2.0/h**2
        if i>0: A[i,i-1] = -1.0/h**2
        if i<N-1: A[i,i+1] = -1.0/h**2
    s = np.sqrt(rho)
    B = A / s[None,:] / s[:,None]
    return np.linalg.eigvalsh(B)[:k]

def build(intervals, R, N):
    rho = np.ones(N)
    for lo, hi in intervals:
        rho[int(round(lo*N)):int(round(hi*N))] = R
    return rho

def F(intervals, R, idx, N=800):
    lam = fd_eigs(build(intervals, R, N), N, idx+1)
    return lam[idx]/lam[idx-1]

def coord_ascent(intervals0, R, idx, N=800, itmax=40, h=0.004):
    ints = list(intervals0)
    for it in range(itmax):
        improved = False
        for k in range(len(ints)):
            for which in [0,1]:
                f0 = F(ints, R, idx, N)
                best = f0; bestv = ints[k][which]
                for s in [-1,1]:
                    cand = [list(p) for p in ints]
                    cand[k][which] += s*h
                    cand = [tuple(sorted(p)) for p in cand]
                    lo = sorted(c[0] for c in cand)
                    hi = sorted(c[1] for c in cand)
                    # keep order and bounds
                    ok = True
                    prev = 0.0
                    newints = []
                    for j in range(len(cand)):
                        a, b = cand[j][0], cand[j][1]
                        if a <= prev+1e-9 or b <= a+1e-9: ok=False; break
                        prev = b
                    if not ok: continue
                    f = F(cand, R, idx, N)
                    if f > best:
                        best = f; bestv = cand[k][which]; improved=True
                if improved:
                    ints[k] = (ints[k][0], bestv) if which==1 else (bestv, ints[k][1])
                    ints = [tuple(sorted(p)) for p in ints]
                    break
            if improved: break
        if not improved: break
    return ints, F(ints, R, idx, N)

# lambda3/lambda2 (idx=2), R=4: start symmetric FP [0.249,0.374]U[0.626,0.751]
t0=time.time()
ints0 = [(0.249,0.374),(0.626,0.751)]
print("start:", ints0, "F=", F(ints0,4.0,2))
ints, fbest = coord_ascent(ints0, 4.0, 2)
print("after ascent:", ints, "F=", fbest, " (%.0fs)" % (time.time()-t0))
# also try asymmetric start
ints0b = [(0.2,0.3),(0.7,0.8)]
print("start:", ints0b, "F=", F(ints0b,4.0,2))
intsb, fb = coord_ascent(ints0b, 4.0, 2)
print("after ascent:", intsb, "F=", fb)
# asymmetric single-interval start
ints0c = [(0.66,0.77)]
print("start:", ints0c, "F=", F(ints0c,4.0,2))
intsc, fc = coord_ascent(ints0c, 4.0, 2)
print("after ascent:", intsc, "F=", fc)
