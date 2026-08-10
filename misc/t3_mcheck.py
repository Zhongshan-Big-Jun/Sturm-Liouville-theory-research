# -*- coding: utf-8 -*-
"""t3_mcheck: check M = cg^2 F1 - 2 A w F2 and other candidate inequalities."""
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
    M = cg**2*F1 - 2*A*w*F2
    B = cg**2*sg*t*F1 - 2*A*sg*t*w*F2 - A*math.sqrt(w*(1-w))*F3
    return M, B, F1, F2, F3, sg, cg, w, t

rngM = [1e18,-1e18]; argM = None
for i in range(800):
    A = Amin + i*(Amax-Amin)/800
    for j in range(800):
        c = 0.4 + j*0.1/800
        if A*(1+c) < math.pi: continue
        M,B,F1,F2,F3,sg,cg,w,t = comps(A,c)
        if M < rngM[0]: rngM[0]=M; argM=(A,c)
        if M > rngM[1]: rngM[1]=M
print('M range:', rngM, 'argmin:', argM)
# also check ratio B2/(B1+B3) max
mx = 0; arg=None
for i in range(800):
    A = Amin + i*(Amax-Amin)/800
    for j in range(800):
        c = 0.4 + j*0.1/800
        if A*(1+c) < math.pi: continue
        M,B,F1,F2,F3,sg,cg,w,t = comps(A,c)
        B1 = cg**2*sg*t*F1; B2 = 2*A*sg*t*w*F2; B3 = A*math.sqrt(w*(1-w))*(-F3)
        r = B2/(B1+B3)
        if r > mx: mx = r; arg=(A,c)
print('max B2/(B1+B3):', mx, 'at', arg)
