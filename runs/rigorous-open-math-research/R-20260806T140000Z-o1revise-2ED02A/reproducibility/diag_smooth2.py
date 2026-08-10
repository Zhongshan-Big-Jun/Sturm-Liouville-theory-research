import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import brentq
from sl_lib import eigenvalues, state_at, eigenfuncs

R = 4.0

def sigmoid(t):
    t = np.clip(t, -1.0, 1.0)
    return np.where(t <= -1, 0.0, np.where(t >= 1, 1.0, 0.5 + 0.5 * np.tanh(np.tanh(t * np.pi / 2) * 2)))

def smoothed_blocks(xj, delta, c_minus, c_plus, nblocks=800):
    xs = np.linspace(0.0, 1.0, nblocks + 1)
    mids = 0.5 * (xs[1:] + xs[:-1])
    vals = c_minus + (c_plus - c_minus) * sigmoid((mids - xj) / delta)
    return xs, vals

# reference config
breaks0 = [0.0, 0.3, 0.65, 1.0]
values0 = [1.0, R, 1.0]
lam0 = eigenvalues(breaks0, values0, k_max=2)
us, up, xg = eigenfuncs(breaks0, values0, lam0)
u1j = np.interp(0.3, xg, us[0]); u2j = np.interp(0.3, xg, us[1])
target1 = lam0[0]*(R-1)*u1j**2
target2 = lam0[1]*(R-1)*u2j**2
print("targets:", target1, target2)

# direct integral: dlam/deps = lam*(c+-c-)*int (1/delta) H'((x-xj)/delta) u_k^2 dx
# H'(t) numerically from sigmoid on a fine t-grid
for delta in (0.02, 0.005):
    # build (1/delta) H'((x-xj)/delta) on a fine grid
    n = 200000
    x = np.linspace(0, 1, n)
    h = 1.0/n
    t = (x - 0.3)/delta
    tt = np.clip(t, -1.0, 1.0)
    sig = np.where(tt <= -1, 0.0, np.where(tt >= 1, 1.0, 0.5 + 0.5*np.tanh(np.tanh(tt*np.pi/2)*2)))
    # H' via finite difference of sigmoid in t (smooth, well-resolved)
    dH = np.gradient(sig, t)
    K = (1.0/delta) * dH
    int1 = np.trapezoid(K * np.interp(x, xg, us[0])**2, x)
    int2 = np.trapezoid(K * np.interp(x, xg, us[1])**2, x)
    print(f"delta={delta}: int(1/delta H' u1^2) = {int1}, int(1/delta H' u2^2) = {int2}")
    print(f"   dlam1 via integral = {lam0[0]*(R-1)*int1}, target {target1}")
    print(f"   dlam2 via integral = {lam0[1]*(R-1)*int2}, target {target2}")
