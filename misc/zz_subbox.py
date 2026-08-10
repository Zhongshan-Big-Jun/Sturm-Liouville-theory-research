# -*- coding: utf-8 -*-
"""Sub-box interval bounds for NJ2 with per-subbox ranges (independent within subbox)."""
import json, mpmath as mp
mp.mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')

def NJ2_vals(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    sg_, cg_, st_, ct_ = mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_)
    tot = mp.mpf(0)
    for i, m in enumerate(rj['monoms']):
        tot += int(rj['coeffs'][i]) * A_**m[0]*t_**m[1]*sg_**m[2]*cg_**m[3]*st_**m[4]*ct_**m[5]
    return tot

def subbox_bound(g0, g1, q0, q1, samples=7):
    # ranges via sampling on a fine grid inside subbox
    R = {k: [mp.mpf('1e30'), mp.mpf('-1e30')] for k in ['A','t','sg','cg','st','ct']}
    for i in range(samples+1):
        g = g0 + mp.mpf(i)*(g1-g0)/samples
        for j in range(samples+1):
            q = q0 + mp.mpf(j)*(q1-q0)/samples
            A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
            for k, v in [('A',A_),('t',t_),('sg',mp.sin(g)),('cg',mp.cos(g)),('st',mp.sin(t_)),('ct',mp.cos(t_))]:
                if v < R[k][0]: R[k][0] = v
                if v > R[k][1]: R[k][1] = v
    pos = mp.mpf(0); neg = mp.mpf(0)
    for i, m in enumerate(rj['monoms']):
        coeff = int(rj['coeffs'][i])
        vmax = mp.mpf(1); vmin = mp.mpf(1)
        for k, e in zip(['A','t','sg','cg','st','ct'], m):
            if e > 0:
                vmax *= R[k][1]**e; vmin *= R[k][0]**e
        if coeff > 0: pos += coeff*vmax
        else: neg += coeff*vmin
    return pos+neg

for N in [4, 6, 8]:
    worst = mp.mpf('-1e30'); worstloc = None
    for i in range(N):
        g0 = glo + mp.mpf(i)*(ghi-glo)/N; g1 = glo + mp.mpf(i+1)*(ghi-glo)/N
        for j in range(N):
            q0 = 1 + mp.mpf(j)/N; q1 = 1 + mp.mpf(j+1)/N
            b = subbox_bound(g0, g1, q0, q1)
            if b > worst: worst, worstloc = b, (i, j)
    print('N=%d: worst subbox upper bound %.3f at %s' % (N, worst, worstloc))
