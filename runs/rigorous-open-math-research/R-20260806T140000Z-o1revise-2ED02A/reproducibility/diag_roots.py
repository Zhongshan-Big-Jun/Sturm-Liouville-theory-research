import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import secular, eigenvalues, state_at, eigenfuncs

breaks = [0.0, 1/3, 2/3, 1.0]
values = [4.0, 1.0, 4.0]
lam_max = 60.0
step = 0.0005
grid = np.linspace(0, lam_max, int(lam_max/step)+1)
F = np.array([secular(g, breaks, values) for g in grid])
sgn = np.sign(F)
roots = []
for i in range(len(grid)-1):
    if sgn[i]*sgn[i+1] < 0:
        roots.append((grid[i], grid[i+1], F[i], F[i+1]))
print("number of sign-change brackets:", len(roots))
for j, (a, b, fa, fb) in enumerate(roots[:6]):
    print("bracket", j, (a, b), (fa, fb))
print("eigenvalues() returns:", eigenvalues(breaks, values, k_max=2))
# verify each candidate root: count zeros of eigenfunction
from scipy.optimize import brentq
for j, (a, b, fa, fb) in enumerate(roots[:4]):
    r = brentq(secular, a, b, args=(breaks, values), xtol=1e-15, rtol=1e-14)
    xg = np.linspace(0, 1, 5001)
    u = np.array([state_at(x, r, breaks, values)[0] for x in xg])
    # count sign changes
    s = np.sign(u)
    nz = int(np.sum(s[1:]*s[:-1] < 0))
    print("root", j, "=", r, "eigenfunction zeros:", nz)
