# -*- coding: utf-8 -*-
import numpy as np, time
from gap_lib import lams_fast

def D_of(blocks, npts=15000):
    s = lams_fast(blocks, 2, npts=npts)
    return s[1]**2 - s[0]**2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    return [(a,1.0),(b,R),(c,1.0)] if mode=="SUP" else [(a,R),(b,1.0),(c,R)]

def hess(mode, R, a, b, h=2e-4):
    D = lambda x,y: D_of(make_blocks(mode,R,x,y))
    f00 = D(a,b)
    faa = (D(a+h,b) - 2*f00 + D(a-h,b))/h**2
    fbb = (D(a,b+h) - 2*f00 + D(a,b-h))/h**2
    fab2 = (D(a+h,b+h) - D(a+h,b) - D(a,b+h) + f00)/h**2
    return np.array([[faa, fab2],[fab2, fbb]])

out=[]
for R in (2.0,4.0,10.0):
    for mode in ("SUP","INF"):
        evs=[]
        for a in np.linspace(0.03,0.95,10):
            for b in np.linspace(0.03,0.90,10):
                if not (0.01<a<0.99 and 0.01<b and a+b<0.97): continue
                try:
                    evs.append(np.linalg.eigvalsh(hess(mode,R,a,b)))
                except Exception:
                    pass
        evs = np.array(evs)
        if mode=="SUP":
            out.append(f"R={R} {mode}: max-eig max={evs[:,0].max():.3f} min={evs[:,0].min():.3f} 2nd-eig max={evs[:,1].max():.3f} n={len(evs)}")
        else:
            out.append(f"R={R} {mode}: min-eig min={evs[:,0].min():.3f} max={evs[:,0].max():.3f} 2nd-eig min={evs[:,1].min():.3f} n={len(evs)}")
        open("tmp_hess_out.txt","w").write("\n".join(out))
print("done")
