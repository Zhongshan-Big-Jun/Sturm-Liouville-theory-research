import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs, f_of, D_of

R = 4.0
def f_sym(u):
    breaks = [0.0, u, 1.0 - u, 1.0]
    values = [1.0, R, 1.0]
    lams = eigenvalues(breaks, values, k_max=2)
    us, up, xg = eigenfuncs(breaks, values, lams)
    f, _, _ = f_of(breaks, values, lams, us, up)
    return np.interp(u, xg, f)

scan = [0.45148540, 0.45148542, 0.45148544, 0.45148546, 0.45148547, 0.45148548, 0.45148550, 0.45148555, 0.45148560]
for u in scan:
    print(u, f_sym(u))
