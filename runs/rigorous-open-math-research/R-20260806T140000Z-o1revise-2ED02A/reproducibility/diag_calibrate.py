import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.linalg import eigh_tridiagonal
from sl_lib import eigenvalues, secular

R = 4.0
out = {}

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
    # symmetrized tridiagonal: B_ii = d/s_i^2 ; B_i,i+1 = e/(s_i s_{i+1})
    dd = d / s ** 2
    ee = e / (s[:-1] * s[1:])
    w = eigh_tridiagonal(dd, ee, select="i", select_range=(0, k - 1), eigvals_only=True)
    return np.sort(w)

tb = ([0.0, 0.5, 1.0], [1.0, 4.0])
tm = eigenvalues(tb[0], tb[1], k_max=3)
fd = fd_eigs(tb, 20000, 3)
out["calib_twoblock"] = {"tm": tm, "fd": fd, "fd_err": abs(fd - np.array(tm))}

c4 = ([0.0, 1.0], [4.0])
tmc = eigenvalues(c4[0], c4[1], k_max=2)
fdc = fd_eigs(c4, 20000, 2)
out["calib_const4"] = {"tm": tmc, "fd": fdc, "fd_err": abs(fdc - np.array(tmc))}

rng = np.random.default_rng(20260806)
def random_rho(nblocks, rng, R):
    xs = np.sort(rng.uniform(0, 1, nblocks - 1))
    breaks = np.concatenate([[0.0], xs, [1.0]])
    values = rng.uniform(1.0, R, nblocks)
    return breaks, values
configs = []
for trial in range(8):
    configs.append((random_rho(6, rng, R), random_rho(6, rng, R)))
for trial in (2, 6):
    for name, idx in (("rho", 0), ("sigma", 1)):
        rho = configs[trial][idx]
        tm = eigenvalues(rho[0], rho[1], k_max=2)
        fd_6k = fd_eigs(rho, 6000, 2)
        fd_20k = fd_eigs(rho, 20000, 2)
        F_fd = [secular(l, rho[0], rho[1]) for l in fd_6k]
        F_tm = [secular(l, rho[0], rho[1]) for l in tm]
        out[f"trial{trial}_{name}"] = {
            "breaks": rho[0], "values": rho[1],
            "tm": tm, "fd_6k": fd_6k, "fd_20k": fd_20k,
            "F_at_fd": F_fd, "F_at_tm": F_tm,
        }
def _conv(o):
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.bool_, np.integer)): return int(o)
    if isinstance(o, np.floating): return float(o)
    raise TypeError
print(json.dumps(out, indent=1, default=_conv))

