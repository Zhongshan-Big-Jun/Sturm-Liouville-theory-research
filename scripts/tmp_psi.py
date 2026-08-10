# -*- coding: utf-8 -*-
"""Test sign of Psi(b,d)/d where Psi = f(a)-f(a+b) in asymmetry coords (b, d), a=(1-b)/2-d, c=(1-b)/2+d."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks(mode, R, a, b):
    c = 1.0 - a - b
    return [(a,1.0),(b,R),(c,1.0)] if mode=="SUP" else [(a,R),(b,1.0),(c,R)]

def f2(blocks):
    s = lams_fast(blocks, 2, npts=8000)
    lam = s**2
    n1 = np.sqrt(norm2(blocks, s[0])); n2 = np.sqrt(norm2(blocks, s[1]))
    fL = lam[0]*(y_at(blocks, s[0], np.array([blocks[0][0]]))[0]/n1)**2 - lam[1]*(y_at(blocks, s[1], np.array([blocks[0][0]]))[0]/n2)**2
    x2 = blocks[0][0]+blocks[1][0]
    fR = lam[0]*(y_at(blocks, s[0], np.array([x2]))[0]/n1)**2 - lam[1]*(y_at(blocks, s[1], np.array([x2]))[0]/n2)**2
    return fL, fR

R = 4.0
out=[]
for mode in ("SUP","INF"):
    out.append(f"==== {mode} R={R}: Psi/d values ====")
    for b in np.linspace(0.05,0.85,10):
        row=[]
        for d in np.linspace(0.02, 0.9*(1-b)/2, 8):
            a = (1-b)/2 - d
            fL,fR = f2(make_blocks(mode,R,a,b))
            Psi = fL - fR
            row.append(f"{Psi/d:+.3f}")
        out.append(f"  b={b:.3f}: " + " ".join(row))
    out.append("")
open("tmp_psi.txt","w").write("\n".join(out))
print("done")
