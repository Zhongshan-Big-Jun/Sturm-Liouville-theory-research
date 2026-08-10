# -*- coding: utf-8 -*-
"""#2: root count of F_n in (0,pi) + y_n extraction, compared with direct eigenvalue computation."""
import numpy as np
import mpmath as mp
mp.mp.dps = 30

def Fn_num(y, n, s):
    # secular M01*w in terms of y for the (2n+1)-block alternating config
    w = 1.0  # w scales out; y = w*s*t fixed relation: use t = 1, s fixed -> w = y/(s*t); we set t=1
    # build T_cell with phases y (both blocks) and T_final phase y
    def T(phase, rho, w):
        ww = w*np.sqrt(rho)
        return np.array([[np.cos(phase), np.sin(phase)/ww], [-ww*np.sin(phase), np.cos(phase)]])
    Tcell = T(y, 1.0, w)  # block1
    Tcell = T(y, s*s, w) @ Tcell  # block2 (rho = s^2 = R)
    M = T(y, 1.0, w)  # final block
    Tc = Tcell
    for _ in range(n):
        M = M @ Tc if False else Tc @ M
    # careful: M_full = T_final . T_cell^n  ->  M = T_cell applied n times first
    M = T(y, 1.0, w)
    Tn = np.eye(2)
    for _ in range(n):
        Tn = Tcell @ Tn
    M = M @ Tn
    return M[0,1]

def roots_of_F(n, s):
    ys = np.linspace(1e-9, np.pi-1e-9, 20000)
    vals = np.array([Fn_num(y, n, s) for y in ys])
    signs = np.signbit(vals[1:]) != np.signbit(vals[:-1])
    idx = np.nonzero(signs)[0]
    roots = []
    for i in idx:
        lo, hi = ys[i], ys[i+1]
        for _ in range(4):
            mid = np.linspace(lo, hi, 2000)
            vm = np.array([Fn_num(y, n, s) for y in mid])
            sm = np.signbit(vm[1:]) != np.signbit(vm[:-1])
            jj = np.nonzero(sm)[0]
            if len(jj)==0: break
            lo, hi = mid[jj[0]], mid[jj[0]+1]
        roots.append((lo+hi)/2)
    return np.array(roots)

for R in (4.0, 10.0):
    s = np.sqrt(R)
    print(f"R={R}: root counts and ratios for alternating configs")
    for n in (1, 2, 3, 4, 5):
        roots = roots_of_F(n, s)
        # sort, check pairing
        pairs = roots + roots[::-1] - np.pi
        print(f"  n={n}: #roots in (0,pi) = {len(roots)} (2n = {2*n}), y_n = {roots[n-1]:.8f}, y_{n+1} = {roots[n]:.8f}, ratio = {(roots[n]/roots[n-1])**2:.8f}")
