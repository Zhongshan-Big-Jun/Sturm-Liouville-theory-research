import numpy as np
from scipy.linalg import eigh_tridiagonal

def stepvals(x, breaks, values):
    fp = np.concatenate([values, [values[-1]]])
    return np.interp(x, breaks, fp, left=values[0], right=values[-1])

def fd_eigs(rho, N, k=2):
    x = np.linspace(0, 1, N + 1)
    h = 1.0 / N
    rv = stepvals((x[1:] + x[:-1]) / 2, rho[0], rho[1])
    d = 2.0 / h ** 2
    e = -1.0 / h ** 2
    s = np.sqrt(rv)
    dd = d / s ** 2
    ee = e / (s[:-1] * s[1:])
    w = eigh_tridiagonal(dd, ee, select="i", select_range=(0, k - 1), eigvals_only=True)
    return np.sort(w)

tb = ([0.0, 0.5, 1.0], [1.0, 4.0])
for N in (10, 50, 200, 1000, 5000, 20000):
    print(N, fd_eigs(tb, N, 2))
print("exact tm:", [3.6505193634593964, 19.119211612999205])
