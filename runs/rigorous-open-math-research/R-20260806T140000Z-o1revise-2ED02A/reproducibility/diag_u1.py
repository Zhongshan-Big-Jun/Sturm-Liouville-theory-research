import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import state_at, secular

breaks = [0.0, 1/3, 2/3, 1.0]
values = [4.0, 1.0, 4.0]
lam = 4.356247533453904
# fine grid
xg = np.linspace(0, 1, 20001)
u = np.array([state_at(x, lam, breaks, values)[0] for x in xg])
up = np.array([state_at(x, lam, breaks, values)[1] for x in xg])
# find all sign changes and near-zero points
s = np.sign(u)
for i in range(len(xg)-1):
    if s[i]*s[i+1] < 0:
        print("sign change near x =", xg[i], xg[i+1], "u =", u[i], u[i+1])
# print values around the suspected region
for frac in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99):
    i = int(frac*20000)
    print(f"x={xg[i]:.4f} u={u[i]:+.6e} up={up[i]:+.6e}")
