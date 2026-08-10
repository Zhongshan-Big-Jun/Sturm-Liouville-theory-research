# -*- coding: utf-8 -*-
"""Verify: (1) v = u2/u1 strictly decreasing (W = u1*u2' - u1'*u2 < 0); (2) {f>0} is a single central interval.
For various rho (constant, 3-block, random-ish bang-bang)."""
import numpy as np
from scipy.integrate import solve_ivp

def eigfun(rho, n, N=4001):
    """return eigenfunction (normalized in L2(rho)) and eigenvalue for -y'' = lam*rho*y, Dirichlet."""
    xs = np.linspace(0, 1, N)
    h = xs[1]-xs[0]
    # finite difference: -y'' = lam rho y  ->  -y[i-1] + 2y[i] - y[i+1] = lam h^2 rho[i] y[i]
    r = rho(xs)
    diag = 2.0 + np.zeros(N)
    off = -np.ones(N-1)
    # generalized eigensolver: A y = lam B y, A tridiag (2,-1,-1... boundary), B = h^2 diag(r)
    A = np.diag(2*np.ones(N)) + np.diag(-np.ones(N-1),1) + np.diag(-np.ones(N-1),-1)
    A[0,0]=A[-1,-1]=1  # y(0)=y(1)=0 -> row0: y0=0? Actually with y0=0 fixed we drop boundaries
    # drop boundary: indices 1..N-2
    A = A[1:-1,1:-1]
    B = np.diag(h*h*r[1:-1])
    vals, vecs = np.linalg.eigh(B)  # not generalized; need scipy generalized
    return None

from scipy.linalg import eigh
def eigpair(rho, N=4001):
    xs = np.linspace(0,1,N); h = xs[1]-xs[0]
    r = rho(xs)
    n = N-2
    A = (2*np.eye(n) - np.diag(np.ones(n-1),1) - np.diag(np.ones(n-1),-1))
    B = np.diag(h*h*r[1:-1])
    w, V = eigh(A, B)
    # V columns are y at interior points
    lam = w[:4]
    u = []
    for k in range(2):
        y = np.zeros(N); y[1:-1] = V[:,k]
        nrm = np.sqrt(np.trapezoid(rho(xs)*y**2, xs))
        u.append(y/nrm)
    return lam, u, xs

def check(rho, label):
    lam, u, xs = eigpair(rho)
    u1, u2 = u[0], u[1]
    h = xs[1]-xs[0]
    du1 = np.gradient(u1, h); du2 = np.gradient(u2, h)
    W = u1*du2 - du1*u2
    f = lam[0]*u1**2 - lam[1]*u2**2
    pos = f > 0
    # count components of {f>0} (on interior)
    comps = 0
    prev = False
    for p in pos[1:-1]:
        if p and not prev: comps += 1
        prev = p
    v = np.where(np.abs(u1) > 1e-9, u2/u1, np.nan)
    # v monotone? check v decreasing in middle region
    mid = slice(N//4, 3*N//4)
    dec = np.all(np.diff(v[mid]) < 1e-9)
    print(f"{label}: lam1={lam[0]:.4f} lam2={lam[1]:.4f} D={lam[1]-lam[0]:.4f} "
          f"{{f>0}} comps={comps} (f>0 at ends: {pos[1]},{pos[-2]}) v-decreasing(mid)={dec} "
          f"max|W mid|={np.max(np.abs(W[mid])):.4f}")

R = 4.0
# 1) constant
check(lambda x: np.ones_like(x)*1.0, "rho=1")
# 2) constant R
check(lambda x: np.ones_like(x)*R, "rho=R")
# 3) SUP config [1,R,1]
u_ = 0.451485
check(lambda x: np.where((x>u_)&(x<1-u_), R, 1.0), "SUP [1,4,1] u=.4515")
# 4) INF config [R,1,R]
ui = 0.382598
check(lambda x: np.where((x>ui)&(x<1-ui), 1.0, R), "INF [4,1,4] u=.3826")
# 5) random bang-bang
rng = np.random.default_rng(1)
edges = np.sort(rng.uniform(0.05,0.95,6))
def rb(x):
    out = np.ones_like(x)
    for k in range(3):
        out[(x>edges[2*k])&(x<edges[2*k+1])] = R
    return out
check(rb, "random bang-bang")
