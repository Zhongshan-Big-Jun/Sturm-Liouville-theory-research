# -*- coding: utf-8 -*-
"""t3_fsigns2: corrected B = cg^2 sg t F1 - 2A sg t w F2 - A sqrt(w(1-w)) F3."""
import numpy as np, math
Amin, Amax = 2*math.pi/3, math.pi-0.655

def vals(A, c):
    t = c*A
    sg = math.sin(math.pi-A); cg = math.cos(math.pi-A)
    w = math.cos(t)**2
    F1 = 8*A**3*cg**2 - 8*A**3*sg**2 + 16*A**3 + 16*A**2*cg**3*sg + 16*A**2*cg*sg**3 + 26*A**2*cg*sg - 15*A*sg**2 + 15*cg*sg**3
    F2 = (8*A**2*cg**4 - 8*A**2*cg**2*sg**2 - 56*A**2*cg**2*w + 58*A**2*cg**2 + 16*A**2*sg**2*w - 12*A**2*sg**2
          + 48*A**2*w**2 - 40*A**2*w + 66*A*cg**3*sg + 8*A*cg*sg**3 - 38*A*cg*sg*w + 15*A*cg*sg + cg**2*sg**2)
    F3 = (-72*A**3*cg**3*w + 36*A**3*cg**3 + 96*A**3*cg*w**2 - 32*A**3*cg*w - 16*A**3*cg
          + 8*A**2*cg**4*sg - 8*A**2*cg**2*sg**3 + 140*A**2*cg**2*sg*w - 68*A**2*cg**2*sg + 8*A**2*sg**3*w
          - 140*A**2*sg*w**2 + 104*A**2*sg*w - 48*A*cg**3*sg**2*t**2 + 42*A*cg**3*sg**2 - 16*A*cg*sg**4*t**2
          + 72*A*cg*sg**2*t**2*w - 40*A*cg*sg**2*w + 15*A*cg*sg**2 - 32*cg**2*sg**3*t**2 - 15*cg**2*sg**3)
    B = cg**2*sg*t*F1 - 2*A*sg*t*w*F2 - A*math.sqrt(w*(1-w))*F3
    return F1, F2, F3, B

rng = {k: [1e18,-1e18] for k in ['F1','F2','F3','B']}
worst = {}
for i in range(401):
    A = Amin + i*(Amax-Amin)/400
    for j in range(401):
        c = 0.4 + j*0.1/400
        if A*(1+c) < math.pi: continue
        F1,F2,F3,B = vals(A,c)
        for k, v in zip(['F1','F2','F3','B'],[F1,F2,F3,B]):
            if v < rng[k][0]: rng[k][0]=v; worst[k]=('min',A,c)
            if v > rng[k][1]: rng[k][1]=v; worst[k]=('max',A,c)
for k in rng:
    print(f'{k}: in [{rng[k][0]:.4f}, {rng[k][1]:.4f}]  worst at {worst[k]}')
# margin of dNJ/dt = 2A^2 cg B
lo = min(2*A**2*math.cos(math.pi-A)*vals(A,c)[3] for i in range(401) for A in [Amin+i*(Amax-Amin)/400] for j in range(401) for c in [0.4+j*0.1/400] if A*(1+c)>=math.pi)
print('min dNJ/dt =', lo)
