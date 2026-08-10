# -*- coding: utf-8 -*-
import numpy as np
import mpmath as mp
mp.mp.dps = 30

def Fn_num(y, n, s):
    w = 1.0
    def T(phase, rho):
        ww = w*np.sqrt(rho)
        return np.array([[np.cos(phase), np.sin(phase)/ww], [-ww*np.sin(phase), np.cos(phase)]])
    Tcell = T(y, s*s) @ T(y, 1.0)
    Tn = np.eye(2)
    for _ in range(n):
        Tn = Tcell @ Tn
    M = T(y, 1.0) @ Tn
    return M[0,1]

for n in (3, 5):
    for R in (2.0, 7.0):
        s = np.sqrt(R)
        ys = np.linspace(1e-9, np.pi-1e-9, 30000)
        vals = np.array([Fn_num(y, n, s) for y in ys])
        signs = np.signbit(vals[1:]) != np.signbit(vals[:-1])
        idx = np.nonzero(signs)[0]
        roots = []
        for i in idx:
            lo, hi = ys[i], ys[i+1]
            for _ in range(4):
                mid = np.linspace(lo, hi, 3000)
                vm = np.array([Fn_num(y, n, s) for y in mid])
                sm = np.signbit(vm[1:]) != np.signbit(vm[:-1])
                jj = np.nonzero(sm)[0]
                if len(jj)==0: break
                lo, hi = mid[jj[0]], mid[jj[0]+1]
            roots.append((lo+hi)/2)
        roots = np.array(roots)
        dev = np.max(np.abs(roots + roots[::-1] - np.pi))
        print(f"n={n} R={R}: #roots={len(roots)}, max |root_j+root_rev_j-pi| = {dev:.2e}")
