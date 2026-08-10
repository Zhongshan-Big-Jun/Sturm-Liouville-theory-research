# -*- coding: utf-8 -*-
"""Find partition where NJ2 monotone in both vars per cell; check corner-based bounds."""
import json, sympy as sp
import mpmath as mp
mp.mp.dps = 30
with open('F:/LaTeX/BVE research/misc/t3_NJ2.json') as fh: rj = json.load(fh)
A, t, sg, cg, st, ct = sp.symbols('A t sg cg st ct')
NJ2 = sum(int(rj['coeffs'][i])*A**m[0]*t**m[1]*sg**m[2]*cg**m[3]*st**m[4]*ct**m[5] for i,m in enumerate(rj['monoms']))
fN = sp.lambdify((A,t,sg,cg,st,ct), NJ2, 'mpmath')
def NJ(g, q):
    A_ = mp.pi - g; t_ = mp.atan(q*mp.tan(g))
    return fN(A_, t_, mp.sin(g), mp.cos(g), mp.sin(t_), mp.cos(t_))
glo, ghi = mp.mpf('0.655'), mp.mpf('1.0472')
h = mp.mpf('1e-7')

def cell_monotone(g0, g1, q0, q1, steps=12):
    dqmin = mp.mpf('1e30'); dqmax = mp.mpf('-1e30')
    dgmin = mp.mpf('1e30'); dgmax = mp.mpf('-1e30')
    for i in range(steps+1):
        g = g0 + mp.mpf(i)*(g1-g0)/steps
        for j in range(steps+1):
            q = q0 + mp.mpf(j)*(q1-q0)/steps
            dq = (NJ(g, q+h)-NJ(g, q-h))/(2*h)
            dg = (NJ(g+h, q)-NJ(g-h, q))/(2*h)
            dqmin = min(dqmin, dq); dqmax = max(dqmax, dq)
            dgmin = min(dgmin, dg); dgmax = max(dgmax, dg)
    return dgmin, dgmax, dqmin, dqmax

# try 4x4 partition
for Ny in [3, 4]:
    print('=== partition %dx%d ===' % (Ny, Ny))
    for i in range(Ny):
        g0 = glo + mp.mpf(i)*(ghi-glo)/Ny; g1 = glo + mp.mpf(i+1)*(ghi-glo)/Ny
        for j in range(Ny):
            q0 = 1 + mp.mpf(j)/Ny; q1 = 1 + mp.mpf(j+1)/Ny
            dgmin, dgmax, dqmin, dqmax = cell_monotone(g0, g1, q0, q1)
            mono = 'M+' if dgmin >= 0 and dqmin >= 0 else ('M-' if dgmax <= 0 and dqmax <= 0 else 'MIX')
            # corner max (for monotone increasing in both: NE corner)
            cvals = [NJ(g0,q0), NJ(g0,q1), NJ(g1,q0), NJ(g1,q1)]
            print('  cell(%d,%d): dg[%+.0f,%+.0f] dq[%+.0f,%+.0f] %s corner NJ: %s' % (i,j,dgmin,dgmax,dqmin,dqmax,mono,', '.join('%.0f'%c for c in cvals)))
