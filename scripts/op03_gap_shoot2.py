import numpy as np
from scipy.integrate import solve_ivp
from op03_gap_precise import lams_precise

R = 4.0
u = 0.45
v0 = 1-2*u
def rho(x):
    x = np.asarray(x)
    return np.where(x < u, 1.0, np.where(x < 1-u, R, 1.0))

def shoot(s):
    sol = solve_ivp(lambda t,y: [y[1], -s*s*rho(t)*y[0]], [0,1], [0.0,1.0],
                    rtol=1e-12, atol=1e-14, dense_output=True, max_step=1e-3)
    return sol.y[0,-1]

lam_tm = lams_precise([(u,1.0),(v0,R),(u,1.0)], 3)**2
print("transfer-matrix lam:", lam_tm[:2])
for k in range(2):
    s0 = np.sqrt(lam_tm[k])
    lo, hi = s0*0.999, s0*1.001
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if shoot(lo)*shoot(mid) <= 0: hi = mid
        else: lo = mid
    s_star = 0.5*(lo+hi)
    sol = solve_ivp(lambda t,y: [y[1], -s_star*s_star*rho(t)*y[0]], [0,1], [0.0,1.0],
                    rtol=1e-12, atol=1e-14, dense_output=True, max_step=1e-3)
    xs = np.linspace(0,1,20001)
    ys = sol.sol(xs)[0]
    nrm = np.trapezoid(rho(xs)*ys**2, xs)
    yu = sol.sol([u])[0][0]
    print(f"k={k}: shooting s^2={s_star**2:.8f} vs TM {lam_tm[k]:.8f}; norm={nrm:.8f}; u(u)^2={yu**2/nrm:.8f}")
