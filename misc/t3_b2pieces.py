# -*- coding: utf-8 -*-
"""t3_b2pieces: ranges of B2 pieces and their extremal locations."""
import numpy as np, math
Amin, Amax = 2*math.pi/3, math.pi-0.655

def comps(A, c):
    t = c*A; g = math.pi-A
    sg = math.sin(g); cg = math.cos(g); w = math.cos(t)**2
    G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
          + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
          + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
          - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
    G1 = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg + 6*A*cg**2*sg**2*t**2 - 12*A*cg**2*sg**2
          + 2*A*sg**4*t**2 - 12*A*sg**2 + 16*cg*sg**3*t**2 + 12*cg*sg**3)
    F = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg + 16*cg*sg**2*t**2 - 20*cg*sg**2)
    H2 = cg*G1 - A*w*F
    T1 = sg*t*G0
    T2 = A*math.sqrt(w*(1-w))*H2
    B2 = -T1 + T2
    return G0, G1, F, H2, T1, T2, B2, sg, cg, w, t, g

rng = {k: [1e18,-1e18] for k in ['G0','G1','F','H2','T1','T2','B2']}
arg = {}
for i in range(250):
    A = Amin + i*(Amax-Amin)/250
    for j in range(250):
        c = 0.4 + j*0.1/250
        if A*(1+c) < math.pi: continue
        G0,G1,F,H2,T1,T2,B2,sg,cg,w,t,g = comps(A,c)
        for k, v in zip(['G0','G1','F','H2','T1','T2','B2'],[G0,G1,F,H2,T1,T2,B2]):
            if v < rng[k][0]: rng[k][0]=v; arg[k]=('min',A,c)
            if v > rng[k][1]: rng[k][1]=v; arg[k]=('max',A,c)
for k in rng:
    print(f'{k}: in [{rng[k][0]:.4f}, {rng[k][1]:.4f}]  {arg[k]}')
