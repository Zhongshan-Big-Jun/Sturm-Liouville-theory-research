# -*- coding: utf-8 -*-
"""#13(iii): is the minimal solution's ratio a rational function of j?
Test: fit P(j)/Q(j), deg <= d, from first 2d+2 values of rho*_j; check residual over j=1..M.
"""
import mpmath as mp
mp.mp.dps = 120
cval = 1
c_ = mp.mpf(cval)
def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
def Q(j): return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)

def backward(N):
    mu = [mp.mpf(0)]*(N+4)
    mu[N+1] = mp.mpf(1)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    return mu

N = 300
mu = backward(N)
# z-scale ratios
rho = [None]*(N+1)
for j in range(2, N-2):
    zj  = mu[j]*(c_/4)**j*mp.factorial(j)**2
    zjm = mu[j-1]*(c_/4)**(j-1)*mp.factorial(j-1)**2
    rho[j] = zj/zjm

def fit_rational(rho, d):
    """Solve Q(j)*rho[j] = P(j) for deg P,Q <= d using first 2d+2 points (j=3..3+2d+1)."""
    npts = 2*d+2
    js = list(range(3, 3+npts))
    # unknowns: p_0..p_d, q_1..q_d (q_0 = 1 normalization)
    A = []; b = []
    for j in js:
        row = [j**k for k in range(d+1)] + [-rho[j]*j**k for k in range(1, d+1)]
        A.append(row); b.append(rho[j])
    M = mp.matrix(A); bv = mp.matrix(b)
    sol = mp.lu_solve(M, bv)
    # residual over wider range
    resid = mp.mpf(0)
    worst = 0
    for j in range(3, N-2):
        Pj = sum(sol[k]*j**k for k in range(d+1))
        Qj = 1 + sum(sol[d+1+k]*j**(k+1) for k in range(d))
        r = abs(Qj*rho[j] - Pj)
        resid = max(resid, r)
    return resid

for d in (1, 2, 3, 4):
    try:
        r = fit_rational(rho, d)
        print(f"degree {d}: max residual over j=3..{N-3} = {mp.nstr(r, 6)}")
    except Exception as e:
        print(f"degree {d}: {type(e).__name__}: {e}")
