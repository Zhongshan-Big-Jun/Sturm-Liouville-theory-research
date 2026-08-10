# -*- coding: utf-8 -*-
"""t3_h2ab: decompose B2 = -sgtG0 + Astct*H2a + A t^2 st ct H2b; check signs."""
import numpy as np, math
Amin, Amax = 2*math.pi/3, math.pi-0.655

def comps(A, c):
    t = c*A; g = math.pi-A
    sg = math.sin(g); cg = math.cos(g); w = math.cos(t)**2
    G0 = (2*A**3*cg**4*w - A**3*cg**4 - 2*A**3*cg**2*sg**2*w + A**3*cg**2*sg**2 - 28*A**3*cg**2*w**2 + 25*A**3*cg**2*w - 2*A**3*cg**2
          + 4*A**3*sg**2*w**2 - 3*A**3*sg**2*w + 12*A**3*w**3 - 10*A**3*w**2 - 2*A**2*cg**5*sg - 2*A**2*cg**3*sg**3
          + 30*A**2*cg**3*sg*w - 10*A**2*cg**3*sg + 2*A**2*cg*sg**3*w + 8*A**2*cg*sg*w**2 - 12*A**2*cg*sg*w
          - 8*A*cg**2*sg**2*w + 12*A*cg**2*sg**2 - 12*cg**3*sg**3)
    G1a = (-8*A**3*cg**2 + 2*A**3 - A**2*cg**3*sg + A**2*cg*sg**3 + 22*A**2*cg*sg - 12*A*cg**2*sg**2 - 12*A*sg**2 + 12*cg*sg**3)
    G1b = (6*A*cg**2*sg**2 + 2*A*sg**4 + 16*cg*sg**3)
    Fa = (-16*A**2*cg**3 + 12*A**2*cg*w - 4*A**2*cg + 41*A*cg**2*sg + A*sg**3 - 22*A*sg*w + 16*A*sg - 20*cg*sg**2)
    Fb = 16*cg*sg**2
    H2a = cg*G1a - A*w*Fa
    H2b = cg*G1b - A*w*Fb
    T0 = sg*t*G0
    T2a = A*math.sqrt(w*(1-w))*H2a
    T2b = A*t**2*math.sqrt(w*(1-w))*H2b
    B2 = -T0 + T2a + T2b
    return G0, G1a, G1b, Fa, Fb, H2a, H2b, T0, T2a, T2b, B2

rng = {k: [1e18,-1e18] for k in ['G0','H2a','H2b','T0','T2a','T2b','B2']}
arg = {}
for i in range(200):
    A = Amin + i*(Amax-Amin)/200
    for j in range(200):
        c = 0.4 + j*0.1/200
        if A*(1+c) < math.pi: continue
        vals = comps(A,c)
        G0, G1a, G1b, Fa, Fb, H2a, H2b, T0, T2a, T2b, B2 = vals
        for k, v in zip(['G0','H2a','H2b','T0','T2a','T2b','B2'],[G0,H2a,H2b,T0,T2a,T2b,B2]):
            if v < rng[k][0]: rng[k][0]=v; arg[k]=('min',A,c)
            if v > rng[k][1]: rng[k][1]=v; arg[k]=('max',A,c)
for k in rng:
    print(f'{k}: in [{rng[k][0]:.4f}, {rng[k][1]:.4f}]  {arg[k]}')
