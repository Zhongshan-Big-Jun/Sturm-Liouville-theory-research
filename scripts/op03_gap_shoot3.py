import numpy as np
from scipy.integrate import solve_ivp, quad
from op03_gap_precise import lams_precise, eigfuns_precise

R = 4.0
u = 0.45
v0 = 1-2*u
def rho(x):
    x = np.asarray(x)
    return np.where(x < u, 1.0, np.where(x < 1-u, R, 1.0))

lam = lams_precise([(u,1.0),(v0,R),(u,1.0)], 2)**2
s0 = np.sqrt(lam[0])
sol = solve_ivp(lambda t,y: [y[1], -s0*s0*rho(t)*y[0]], [0,1], [0.0,1.0],
                rtol=1e-12, atol=1e-14, dense_output=True, max_step=1e-3)
for x in (0.2, 0.45, 0.5, 0.7):
    print(f"x={x}: shooting y={sol.sol([x])[0][0]:.10f}")

# TM raw y via correct formula
def y_tm(x):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in [(u,1.0),(v0,R),(u,1.0)]:
        x1 = x0 + L
        if x <= x1:
            w = s0*np.sqrt(c); d = x - x0
            return M01*np.cos(w*d) + M11*np.sin(w*d)/w
        w = s0*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
for x in (0.2, 0.45, 0.5, 0.7):
    print(f"x={x}: TM y={y_tm(x):.10f}")

# scipy quad norm of TM y vs shooting y
nrm_tm = quad(lambda x: rho(x)*y_tm(x)**2, 0, 1, epsabs=1e-13, limit=500)[0]
xs = np.linspace(0,1,200001)
ys = sol.sol(xs)[0]
nrm_shoot = np.trapezoid(rho(xs)*ys**2, xs)
print("norm TM:", nrm_tm)
print("norm shooting (200001 pts):", nrm_shoot)
# shooting norm with max_step 1e-4 recomputed directly
sol2 = solve_ivp(lambda t,y: [y[1], -s0*s0*rho(t)*y[0]], [0,1], [0.0,1.0],
                 rtol=1e-13, atol=1e-15, dense_output=True, max_step=1e-4)
xs = np.linspace(0,1,1000001)
ys = sol2.sol(xs)[0]
print("norm shooting2 (1e6 pts):", np.trapezoid(rho(xs)*ys**2, xs))
