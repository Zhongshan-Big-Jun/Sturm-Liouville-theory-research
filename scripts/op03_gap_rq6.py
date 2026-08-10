import numpy as np
from scipy.integrate import solve_ivp

R = 4.0
u = 0.30
v0 = 1-2*u
def rho_v(x):
    x = np.asarray(x, dtype=float)
    return np.where(x < u, 1.0, np.where(x < 1-u, R, 1.0))

s = np.sqrt(3.12004426)
sol = solve_ivp(lambda t,y: [y[1], -s*s*rho_v(t)*y[0]], [0,1], [0.0,1.0],
                rtol=1e-13, atol=1e-15, dense_output=True, max_step=1e-4)
xs = np.linspace(0,1,2000001)
ys = sol.sol(xs)
I2 = np.trapezoid(ys[1]**2, xs)
I0 = np.trapezoid(rho_v(xs)*ys[0]**2, xs)
print(f"IVP: int y'^2={I2:.10f}  s^2 int rho y^2={s*s*I0:.10f}  ratio={I2/(s*s*I0):.8f}")
print("y(1) =", ys[0,-1])
# compare IVP y at points with my transfer-matrix formula
def y_tm(x):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in [(u,1.0),(v0,R),(u,1.0)]:
        x1 = x0 + L
        if x <= x1:
            w = s*np.sqrt(c); d = x - x0
            return M01*np.cos(w*d) + M11*np.sin(w*d)/w
        w = s*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
for x in (0.1, 0.3, 0.5, 0.7, 0.9, 0.99):
    yivp = sol.sol([x])[0][0]
    print(f"x={x}: IVP={yivp:.10f}  TM={y_tm(x):.10f}  diff={yivp-y_tm(x):.2e}")
