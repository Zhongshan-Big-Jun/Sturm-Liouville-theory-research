# -*- coding: utf-8 -*-
"""gap_n1_phase6.py: debug INF normalization; compare f via two routes."""
import numpy as np
from gap_lib import lams_fast, y_at, norm2

def make_blocks_sym(mode, R, u):
    if mode=="SUP":
        return [(u,1.0),(1-2*u,R),(u,1.0)]
    return [(u,R),(1-2*u,1.0),(u,R)]

def I_direct(blocks, w):
    x = np.linspace(0, 0.5, 40001)
    y = y_at(blocks, w, x)
    xs = [0.0]
    for L,c in blocks: xs.append(xs[-1]+L)
    rr = np.zeros(len(x))
    for i, p in enumerate(x):
        bi = max(j for j in range(len(xs)-1) if xs[j] <= p)
        rr[i] = blocks[bi][1]
    return np.trapezoid(rr*y**2, x)

def f_route1(blocks, u):
    """f(u) via y_at / sqrt(2*I)"""
    s = lams_fast(blocks, 2, npts=90000)
    w1, w2 = s[0], s[1]
    y1u = y_at(blocks, w1, np.array([u]))[0]
    y2u = y_at(blocks, w2, np.array([u]))[0]
    I1 = I_direct(blocks, w1); I2 = I_direct(blocks, w2)
    return w1**2*y1u**2/(2*I1) - w2**2*y2u**2/(2*I2), (w1, w2, I1, I2, y1u, y2u)

def f_route2(blocks, u):
    """f(u) via y_at / norm2 (full interval)"""
    s = lams_fast(blocks, 2, npts=90000)
    w1, w2 = s[0], s[1]
    u1 = y_at(blocks, w1, np.array([u]))[0]/np.sqrt(norm2(blocks, w1))
    u2 = y_at(blocks, w2, np.array([u]))[0]/np.sqrt(norm2(blocks, w2))
    return w1**2*u1**2 - w2**2*u2**2

R = 4.0
for mode, u in (("SUP",0.45148550), ("INF",0.38259830)):
    bl = make_blocks_sym(mode, R, u)
    r1 = f_route1(bl, u)
    r2 = f_route2(bl, u)
    print(f"{mode} u={u}:")
    print(f"  f via sqrt(2I): {r1[0]:+.8f}")
    print(f"  f via norm2:    {r2:+.8f}")
    w1, w2, I1, I2, y1u, y2u = r1[1]
    print(f"  w1={w1:.6f} w2={w2:.6f} I1={I1:.8f} I2={I2:.8f} y1u={y1u:.6f} y2u={y2u:.6f}")
    print(f"  sin^2(w1u)/I1={np.sin(w1*u)**2/I1:.6f}  sin^2(w2u)/I2={np.sin(w2*u)**2/I2:.6f}")
    # also check norm2 == 2*I?
    print(f"  norm2(w1)={norm2(bl,w1):.8f} 2*I1={2*I1:.8f}  ratio={norm2(bl,w1)/(2*I1):.4f}")
    print(f"  norm2(w2)={norm2(bl,w2):.8f} 2*I2={2*I2:.8f}  ratio={norm2(bl,w2)/(2*I2):.4f}")
