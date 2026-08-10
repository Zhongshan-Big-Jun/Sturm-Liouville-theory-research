# -*- coding: utf-8 -*-
"""gap_n1_phase5.py: verify each component of the SC formula directly."""
import numpy as np
from gap_lib import lams_fast, y_at

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

def I_direct(blocks, w, half=0.5):
    """int_0^half rho y^2 dx, y unnormalized with y(0)=0, y'(0)=1."""
    x = np.linspace(0, half, 20001)
    y = y_at(blocks, w, x)
    rho = np.array([c for (L,c) in blocks for _ in range(1)])  # placeholder
    # build rho(x)
    xs = [0.0]
    for L,c in blocks: xs.append(xs[-1]+L)
    rr = np.zeros(len(x))
    for i, p in enumerate(x):
        bi = max(j for j in range(len(xs)-1) if xs[j] <= p)
        rr[i] = blocks[bi][1]
    return np.trapezoid(rr*y**2, x)

def theta_half(mode, R, u, w):
    v = 0.5 - u
    x = w*u
    if mode=="SUP":
        j = int(np.floor((x+np.pi/2)/np.pi))
        Phi = j*np.pi + np.arctan(np.sqrt(R)*np.tan(x))
        return Phi + w*np.sqrt(R)*v
    else:
        x2 = w*np.sqrt(R)*u
        j = int(np.floor((x2+np.pi/2)/np.pi))
        Phi = j*np.pi + np.arctan(np.tan(x2)/np.sqrt(R))
        return Phi + w*v

R = 4.0
for mode in ("SUP","INF"):
    u = 0.45148550 if mode=="SUP" else 0.38259830
    bl = make_blocks_sym(mode, R, u)
    s = lams_fast(bl, 3, npts=90000)
    print(f"==== {mode} u={u:.8f} ====")
    for idx, w in enumerate(s[:2]):
        I = I_direct(bl, w)
        # dtheta/dw via finite difference
        h = 1e-6
        dth = (theta_half(mode,R,u,w+h) - theta_half(mode,R,u,w-h))/(2*h)
        rho_half = R if mode=="SUP" else 1.0
        I_formula = dth/(2*w**2*np.sqrt(rho_half))
        sin2 = np.sin(w*u)**2
        print(f"  w{idx+1}={w:.6f}: I_direct={I:.6f} I_formula={I_formula:.6f} (ratio {I_formula/I:.4f})")
        print(f"     dtheta/dw={dth:.6f}  sin^2(wu)/I={sin2/I:.6f}  w^2 sin^2(wu)/dth={w**2*sin2/dth:.6f}")
