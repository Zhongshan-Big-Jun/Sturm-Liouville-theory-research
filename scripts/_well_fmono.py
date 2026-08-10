# -*- coding: utf-8 -*-
"""f(v) monotonicity on symmetric line + equal-pair/second-equation screen (E3)."""
import numpy as np
from scipy.optimize import brentq
from _well_landscape2 import eigs_well, fval, well_secular, well_s

def f_sym(R, v):
    return fval(v, 1-v, R, v)

for R in [1.1, 2.0, 4.0, 10.0, 25.0, 100.0]:
    vs = np.linspace(0.002, 0.498, 400)
    fv = np.array([f_sym(R, v) for v in vs])
    d = np.diff(fv)
    n_inc = int(np.sum(d > 0))
    print(f"R={R:6.1f}: f(v) on (0,1/2): increasing-steps={n_inc}/{len(d)} (0 => f strictly decreasing)")
    # locate zero of f
    z = None
    for i in range(len(vs)-1):
        if fv[i]*fv[i+1] < 0:
            z = brentq(lambda v: f_sym(R, v), vs[i], vs[i+1])
            break
    if z: print(f"    f zero at v={z:.5f}")

print()
# equal-pair structure for R=4 at the symmetric critical point (tau known)
R = 4.0; m = np.sqrt(R)
a, b = 0.382598, 0.617402
lam1, lam2 = eigs_well(a, b, R)
s1 = np.sqrt(lam1); tau = np.sqrt(lam2)/s1
A0 = m*s1*a
print(f"R=4: tau={tau:.6f}, A0={A0:.6f}, pi/tau={np.pi/tau:.6f}")
# scan: for each x in (0,pi/tau), find all preimages of r_tau(x)
xs = np.linspace(1e-6, np.pi/tau-1e-6, 50000)
J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
rv = J(tau*xs)/J(xs)
# for a sample of levels, count preimages
levels = np.linspace(0.05, 4.5, 90)
for lev in levels[::15]:
    diffs = np.abs(rv - lev)
    # count local minima below threshold
    lo = np.min(diffs)
    cnt = int(np.sum(diffs < 1e-3))
    # find distinct preimage clusters
    idx = np.nonzero(diffs < 1e-3)[0]
    clusters = 0
    if len(idx):
        clusters = 1
        for k in range(1, len(idx)):
            if idx[k] > idx[k-1]+3: clusters += 1
    print(f"  level r={lev:.3f}: preimage-clusters={clusters}")
