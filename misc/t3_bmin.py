# -*- coding: utf-8 -*-
"""t3_bmin: locate min of B, dump components there."""
import numpy as np, math
Amin, Amax = 2*math.pi/3, math.pi-0.655

def comps(A, c):
    t = c*A; g = math.pi-A
    sg = math.sin(g); cg = math.cos(g); w = math.cos(t)**2
    F1 = 8*A**3*cg**2 - 8*A**3*sg**2 + 16*A**3 + 16*A**2*cg**3*sg + 16*A**2*cg*sg**3 + 26*A**2*cg*sg - 15*A*sg**2 + 15*cg*sg**3
    F2 = (8*A**2*cg**4 - 8*A**2*cg**2*sg**2 - 56*A**2*cg**2*w + 58*A**2*cg**2 + 16*A**2*sg**2*w - 12*A**2*sg**2
          + 48*A**2*w**2 - 40*A**2*w + 66*A*cg**3*sg + 8*A*cg*sg**3 - 38*A*cg*sg*w + 15*A*cg*sg + cg**2*sg**2)
    F3 = (-72*A**3*cg**3*w + 36*A**3*cg**3 + 96*A**3*cg*w**2 - 32*A**3*cg*w - 16*A**3*cg
          + 8*A**2*cg**4*sg - 8*A**2*cg**2*sg**3 + 140*A**2*cg**2*sg*w - 68*A**2*cg**2*sg + 8*A**2*sg**3*w
          - 140*A**2*sg*w**2 + 104*A**2*sg*w - 48*A*cg**3*sg**2*t**2 + 42*A*cg**3*sg**2 - 16*A*cg*sg**4*t**2
          + 72*A*cg*sg**2*t**2*w - 40*A*cg*sg**2*w + 15*A*cg*sg**2 - 32*cg**2*sg**3*t**2 - 15*cg**2*sg**3)
    B = cg**2*sg*t*F1 - 2*A*sg*t*w*F2 - A*math.sqrt(w*(1-w))*F3
    return dict(A=A, c=c, t=t, g=g, sg=sg, cg=cg, w=w, F1=F1, F2=F2, F3=F3, B=B,
                B1=cg**2*sg*t*F1, B2=2*A*sg*t*w*F2, B3=A*math.sqrt(w*(1-w))*(-F3))
best = None
for i in range(1200):
    A = Amin + i*(Amax-Amin)/1200
    for j in range(1200):
        c = 0.4 + j*0.1/1200
        if A*(1+c) < math.pi: continue
        d = comps(A,c)
        if best is None or d['B'] < best['B']: best = d
for k in ['A','c','t','g','sg','cg','w','F1','F2','F3','B1','B2','B3','B']:
    print(f'{k} = {best[k]:.6f}')
