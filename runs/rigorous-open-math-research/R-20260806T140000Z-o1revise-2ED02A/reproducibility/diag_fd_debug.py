import numpy as np
from scipy.linalg import eigh_tridiagonal

def stepvals(x, breaks, values):
    fp = np.concatenate([values, [values[-1]]])
    return np.interp(x, breaks, fp, left=values[0], right=values[-1])

tb = ([0.0, 0.5, 1.0], [1.0, 4.0])
N = 10
x = np.linspace(0, 1, N + 1)
h = 1.0 / N
rv = stepvals((x[1:] + x[:-1]) / 2, tb[0], tb[1])
print("rho_mid:", rv)
d = 2.0 / h**2; e = -1.0/h**2
s = np.sqrt(rv)
dd = d / s**2
ee = e / (s[:-1]*s[1:])
allw = eigh_tridiagonal(dd, ee, eigvals_only=True)
print("all eigenvalues sorted:", np.sort(allw))
# smallest 2 via select i
w2 = eigh_tridiagonal(dd, ee, select="i", select_range=(0,1), eigvals_only=True)
print("select i (0,1):", np.sort(w2))
# What are the exact eigenvalues of the DISCRETE problem A y = lam rho y for this rho?
# Build A and solve dense generalized
A = np.zeros((N,N)); idx=np.arange(N)
A[idx,idx]=d; A[idx[:-1],idx[:-1]+1]=e; A[idx[:-1]+1,idx[:-1]]=e
from numpy.linalg import eigh
B = A / s[:,None] / s[None,:]
w, V = eigh(B)
print("dense sym eigs:", w[:5])
print("exact: 3.6505..., 19.119...")
