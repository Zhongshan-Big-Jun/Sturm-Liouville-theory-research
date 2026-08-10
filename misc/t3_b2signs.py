# -*- coding: utf-8 -*-
"""t3_b2signs: check signs of G0, G1, F, and B2 on region."""
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
    B2 = -sg*t*G0 + A*math.sqrt(w*(1-w))*(cg*G1 - A*w*F)
    return G0, G1, F, B2

rng = {k: [1e18,-1e18] for k in ['G0','G1','F','B2']}
worst = {}
for i in range(400):
    A = Amin + i*(Amax-Amin)/400
    for j in range(400):
        c = 0.4 + j*0.1/400
        if A*(1+c) < math.pi: continue
        G0,G1,F,B2 = comps(A,c)
        for k, v in zip(['G0','G1','F','B2'],[G0,G1,F,B2]):
            if v < rng[k][0]: rng[k][0]=v; worst[k]=('min',A,c)
            if v > rng[k][1]: rng[k][1]=v; worst[k]=('max',A,c)
for k in rng:
    print(f'{k}: in [{rng[k][0]:.4f}, {rng[k][1]:.4f}]  worst at {worst[k]}')
# also dNJ2dt min
lo = 1e18
for i in range(400):
    A = Amin + i*(Amax-Amin)/400
    for j in range(400):
        c = 0.4 + j*0.1/400
        if A*(1+c) < math.pi: continue
        G0,G1,F,B2 = comps(A,c)
        v = 32*A**2*cg*B2 if False else B2
        lo = min(lo, B2)
print('min B2 =', lo)
