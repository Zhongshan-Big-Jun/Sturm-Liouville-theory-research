import numpy as np
from scipy.integrate import quad
from op03_gap_precise import lams_precise

R = 4.0
u = 0.30
v0 = 1-2*u
base = [(u,1.0),(v0,R),(u,1.0)]
lam0 = lams_precise(base, 3)**2

def y_fn(x, ss, blocks):
    M00 = 1.0; M01 = 0.0; M10 = 0.0; M11 = 1.0
    x0 = 0.0
    for L, c in blocks:
        x1 = x0 + L
        if x <= x1:
            w = ss*np.sqrt(c); d = x - x0
            return M01*np.cos(w*d) + M11*np.sin(w*d)/w, w*(M11*np.cos(w*d) - M01*w*np.sin(w*d))/w
        w = ss*np.sqrt(c); wL = w*L
        cw = np.cos(wL); sw = np.sin(wL)/w; sw2 = -w*np.sin(wL)
        M00, M01, M10, M11 = M00*cw+M01*sw2, M00*sw+M01*cw, M10*cw+M11*sw2, M10*sw+M11*cw
        x0 = x1
    raise ValueError

def rho_of(blocks):
    xs = [0.0]
    for L, c in blocks: xs.append(xs[-1]+L)
    def rho(x):
        for i in range(len(xs)-1):
            if xs[i] <= x <= xs[i+1]: return blocks[i][1]
        return None
    return rho

s0 = np.sqrt(lam0[0])
rho_base = rho_of(base)
# norm of raw y1
nrm, _ = quad(lambda x: rho_base(x)*y_fn(x, s0, base)[0]**2, 0, 1, epsabs=1e-13, limit=500)
print("int rho y1^2 (raw):", nrm)
# normalized u1 = y1/sqrt(nrm); Rayleigh: lam1 = int u1'^2 / int rho u1^2
def u1(x):
    yv, ypv = y_fn(x, s0, base)
    return yv/np.sqrt(nrm)
def u1p(x):
    yv, ypv = y_fn(x, s0, base)
    return ypv/np.sqrt(nrm)
K, _ = quad(lambda x: u1p(x)**2, 0, 1, epsabs=1e-13, limit=500)
print("int u1'^2 =", K, " (should equal lam1 =", lam0[0], ")")
print("Rayleigh consistency:", K/nrm, " vs lam1:", lam0[0])

# perturbed config, Rayleigh quotient of base u1:
eps = 1e-5
pert = [(u+eps,1.0),(v0-eps,R),(u,1.0)]
rho_pert = rho_of(pert)
P, _ = quad(lambda x: rho_pert(x)*u1(x)**2, 0, 1, epsabs=1e-13, limit=500)
RQ = K/P
print("RQ(lambda1) with base u1 on perturbed rho:", RQ, " vs lam0:", lam0[0])
lamP = lams_precise(pert, 3)**2
print("actual perturbed lam1:", lamP[0])
print("RQ - lam0 =", RQ - lam0[0], " vs actual change:", lamP[0]-lam0[0])
