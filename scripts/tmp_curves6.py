# -*- coding: utf-8 -*-
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    return [(a,1.0),(b,R),(c,1.0)] if mode=="SUP" else [(a,R),(b,1.0),(c,R)]

def f2(blocks, x1, x2):
    s = lams_fast(blocks, 2, npts=8000)
    lam = s**2
    n1 = np.sqrt(norm2(blocks, s[0])); n2 = np.sqrt(norm2(blocks, s[1]))
    f1 = lam[0]*(y_at(blocks, s[0], np.array([x1]))[0]/n1)**2 - lam[1]*(y_at(blocks, s[1], np.array([x1]))[0]/n2)**2
    f2v = lam[0]*(y_at(blocks, s[0], np.array([x2]))[0]/n1)**2 - lam[1]*(y_at(blocks, s[1], np.array([x2]))[0]/n2)**2
    return f1, f2v

def bisect(mode, R, which, a0, a1, b):
    lo, hi = a0, a1
    flo = f2(make_blocks(mode,R,lo,b), lo, lo+b)[which-1]
    for _ in range(22):
        mid = 0.5*(lo+hi)
        fm = f2(make_blocks(mode,R,mid,b), mid, mid+b)[which-1]
        if flo*fm < 0: hi = mid
        else: lo, flo = mid, fm
    return 0.5*(lo+hi)

R = 4.0
out = []
for mode in ("SUP","INF"):
    out.append(f"==== {mode} R={R} ====")
    for b in np.linspace(0.05, 0.90, 14):
        aa = np.linspace(0.01, 0.99-b, 45)
        rows = np.array([f2(make_blocks(mode,R,a,b), a, a+b) for a in aa])
        c1, c2 = [], []
        for i in range(len(aa)-1):
            if rows[i,0]*rows[i+1,0] < 0: c1.append(bisect(mode,R,1,aa[i],aa[i+1],b))
            if rows[i,1]*rows[i+1,1] < 0: c2.append(bisect(mode,R,2,aa[i],aa[i+1],b))
        out.append(f"  b={b:.3f}: C1=[{','.join(f'{r:.3f}' for r in c1)}]  C2=[{','.join(f'{r:.3f}' for r in c2)}]")
open("tmp_curves_out.txt","w").write("\n".join(out))
print("done")
