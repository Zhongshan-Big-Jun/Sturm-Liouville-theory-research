import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from sl_lib import eigenvalues, eigenfuncs, f_of, D_of

R = 4.0
out = {}
# constants: D(1) = 3pi^2 ; D(R) = 3pi^2/R
out["D_rho1"] = {"numeric": D_of([0.0,1.0],[1.0]), "exact": 3*np.pi**2}
out["D_rhoR"] = {"numeric": D_of([0.0,1.0],[R]), "exact": 3*np.pi**2/R}

# find zero of f_sym near 0.45148546584 with high precision
def f_sym(u):
    breaks = [0.0, u, 1.0 - u, 1.0]
    values = [1.0, R, 1.0]
    lams = eigenvalues(breaks, values, k_max=2)
    us, up, xg = eigenfuncs(breaks, values, lams)
    f, _, _ = f_of(breaks, values, lams, us, up)
    return np.interp(u, xg, f)

# bisection on f_sym sign change between 0.4514854650 and 0.4514854660
a, b = 0.4514854650, 0.4514854660
fa, fb = f_sym(a), f_sym(b)
assert fa * fb < 0, (fa, fb)
for _ in range(60):
    m = 0.5*(a+b)
    fm = f_sym(m)
    if fa*fm < 0:
        b, fb = m, fm
    else:
        a, fa = m, fm
u_star = 0.5*(a+b)
out["u_star_zero_of_f"] = u_star
out["f_at_u_star"] = f_sym(u_star)

# D and lambda at u_star
breaks = [0.0, u_star, 1.0 - u_star, 1.0]
lams = eigenvalues(breaks, [1.0, R, 1.0], k_max=2)
out["lams_at_u_star"] = list(lams)
out["D_at_u_star"] = lams[1]-lams[0]
out["contract"] = {"u*": 0.45148546584, "lam1": 6.109280, "lam2": 38.723263, "D": 32.6139836177}
print(json.dumps(out, indent=1))
