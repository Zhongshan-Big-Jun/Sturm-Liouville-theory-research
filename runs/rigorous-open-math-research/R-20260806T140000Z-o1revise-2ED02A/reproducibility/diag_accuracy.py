import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
from sl_lib import eigenvalues, eigenfuncs, f_of, D_of

out = {}
# Exact case 1: rho = c constant
for c in (1.0, 4.0, 7.3):
    lams = eigenvalues([0.0, 1.0], [c], k_max=4)
    err = max(abs(lams[k] - (k+1)**2*np.pi**2/c) for k in range(4))
    out[f"const_c={c}"] = {"max_abs_err": err}

# Exact case 2: two-block [1,4] at (0,0.5),(0.5,1)
lams = eigenvalues([0.0, 0.5, 1.0], [1.0, 4.0], k_max=3)
roots2 = []
s = np.linspace(1e-6, 12, 200000)
F2 = np.sin(s/2)*np.cos(s) + 0.5*np.cos(s/2)*np.sin(s)
sgn = np.sign(F2)
for i in range(len(s)-1):
    if sgn[i]*sgn[i+1] < 0:
        r = brentq(lambda t: np.sin(t/2)*np.cos(t) + 0.5*np.cos(t/2)*np.sin(t), s[i], s[i+1], xtol=1e-15, rtol=1e-14)
        roots2.append(r**2)
out["twoblock_14"] = {"solver_lams": lams, "secular_roots": roots2[:3],
                      "diff": [abs(lams[k]-roots2[k]) for k in range(3)]}

# u* by bisection on f_sym
def f_sym(u):
    breaks = [0.0, u, 1.0 - u, 1.0]
    values = [1.0, 4.0, 1.0]
    lams = eigenvalues(breaks, values, k_max=2)
    us, up, xg = eigenfuncs(breaks, values, lams)
    f, _, _ = f_of(breaks, values, lams, us, up)
    return float(np.interp(u, xg, f))

a, b = 0.45148546, 0.45148547
fa, fb = f_sym(a), f_sym(b)
assert fa*fb < 0, (fa, fb)
for _ in range(80):
    m = 0.5*(a+b); fm = f_sym(m)
    if fa*fm < 0: b, fb = m, fm
    else: a, fa = m, fm
u_star = 0.5*(a+b)
out["u_star_bisection"] = {"u*": u_star, "f(u*)": f_sym(u_star)}
breaks = [0.0, u_star, 1.0 - u_star, 1.0]
lams = eigenvalues(breaks, [1.0, 4.0, 1.0], k_max=2)
out["at_u_star"] = {"lams": lams, "D": lams[1]-lams[0]}
out["contract"] = {"u*": 0.45148546584, "lam1": 6.109280, "lam2": 38.723263, "D": 32.6139836177}
print(json.dumps(out, indent=1))
