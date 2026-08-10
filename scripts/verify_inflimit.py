import numpy as np
from scipy.optimize import root, brentq

# ---- exact 3-block symmetric well [R,1,R], outer width u ----
def secular(lam, u, R):
    kR = np.sqrt(lam * R)
    k1 = np.sqrt(lam)
    def P(k, L):
        c, s = np.cos(k*L), np.sin(k*L)
        return np.array([[c, s/k], [-k*s, c]])
    M = P(kR, u) @ P(k1, 1-2*u) @ P(kR, u)
    return M[0,1]

def eig2(u, R):
    # find first two roots of secular on (0, large)
    out = []
    lam = 1e-6
    while len(out) < 2:
        hi = lam * 2
        while secular(hi, u, R) * secular(lam, u, R) > 0:
            hi *= 2
            if hi > 1e12: break
        try:
            r = brentq(lambda l: secular(l, u, R), lam, hi)
        except ValueError:
            lam = hi; continue
        if r > lam + 1e-9:
            out.append(r)
        lam = hi
    return out[0], out[1]

# ---- limiting system (O) + (S) ----
def mu1_of(u):
    return (np.pi**2) / (4*u**2)

def mu2_of(u):
    # unique solution of tan(sqrt(mu)*u) = -sqrt(mu)*(1/2-u), branch sqrt(mu)*u in (pi/2, pi)
    lo = (np.pi/(2*u))**2 + 1e-12
    hi = (np.pi/u)**2 - 1e-12
    f = lambda mu: np.tan(np.sqrt(mu)*u) + np.sqrt(mu)*(0.5-u)
    return brentq(f, lo, hi)

def I2(u, mu):
    a = np.sqrt(mu)
    x = np.linspace(0, u, 200001)
    return np.trapz(np.sin(a*x)**2, x)

def S(u):
    mu1 = mu1_of(u)
    mu2 = mu2_of(u)
    return mu1*2.0/u - mu2*np.sin(np.sqrt(mu2)*u)**2/I2(u, mu2)

# find u* root of S(u) on (0, 1/2)
us = np.linspace(0.05, 0.49, 200)
Sv = np.array([S(u) for u in us])
sign = np.sign(Sv)
idx = np.nonzero(sign[1:] != sign[:-1])[0]
print("S(u) sign changes:", [(round(us[i],4), round(Sv[i],3), round(us[i+1],4), round(Sv[i+1],3)) for i in idx])
u0 = 0.3299
print("S(0.3299) =", S(u0))
# refine
u_star = brentq(S, 0.32, 0.34)
mu1s = mu1_of(u_star); mu2s = mu2_of(u_star)
print("u* =", repr(u_star))
print("mu1 =", repr(mu1s), " mu2 =", repr(mu2s), " D*R =", repr(mu2s-mu1s))
print("claimed: u=0.32992251, mu1=22.668139, mu2=47.612005, D*R=24.943866")
print("3*pi^2 =", 3*np.pi**2)

# (E),(O),(S) residuals at u*
print("sqrt(mu1)*u - pi/2 =", np.sqrt(mu1s)*u_star - np.pi/2)
print("tan(sqrt(mu2)*u) - sqrt(mu2)*(u-1/2) =", np.tan(np.sqrt(mu2s)*u_star) - np.sqrt(mu2s)*(u_star-0.5))
print("S residual =", S(u_star))

# exact eigenvalues at large R for the extremal u(R) (use u_star as proxy)
for R in [1e2, 1e4, 1e6]:
    l1, l2 = eig2(u_star, R)
    print(f"R={R:.0e}: lam1*R={l1*R:.6f} lam2*R={l2*R:.6f} D*R={(l2-l1)*R:.6f}")