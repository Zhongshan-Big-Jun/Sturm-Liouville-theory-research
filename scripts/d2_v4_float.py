# -*- coding: utf-8 -*-
# Direction 2 verification - V4 float version
import sys, numpy as np
sys.path.insert(0, r"F:\LaTeX\BVE research\scripts")
import orthogonal_systems_verify as V
from fractions import Fraction as F

cval = 3

def fp(p):
    return np.array([float(x) for x in p], dtype=float)

def Kc_fp(p):
    out = fp(p).copy()*cval
    if len(p) > 2:
        out[:len(p)-2] -= fp(p)[2:]*np.arange(2, len(p))*np.arange(1, len(p)-1)
    return out

def L2_inner_fp(p, q):
    p = fp(p); q = fp(q)
    tot = 0.0
    for i in range(len(p)):
        for j in range(len(q)):
            if (i + j) % 2 == 0:
                tot += p[i]*q[j]*2.0/(i+j+1)
    return tot

def deriv(a):
    return np.array([i*a[i] for i in range(1, len(a))], dtype=float)

def inner1_fp(p, q):
    # (u,v)_1 = int u'v' + c int uv - (1/2)(u(1)-u(-1))(v(1)-v(-1))
    dp = deriv(fp(p)); dq = deriv(fp(q))
    # int over [-1,1] of monomials: need helper on coefficient lists
    def L2(a, b):
        n = min(len(a), len(b)); return sum(a[i]*b[i]*2.0/(2*i+1) for i in range(n) if i % 2 == 0)
    def ev(a, x): return sum(a[i]*x**i for i in range(len(a)))
    return L2(dp, dq) + cval*L2(fp(p), fp(q)) - 0.5*(ev(fp(p),1)-ev(fp(p),-1))*(ev(fp(q),1)-ev(fp(q),-1))

def inner_s_fp(p, q, s):
    r = s // 2
    pr, qr = fp(p), fp(q)
    for _ in range(r):
        pr = Kc_fp(pr); qr = Kc_fp(qr)
    if s % 2 == 0:
        return L2_inner_fp(pr, qr)
    else:
        return inner1_fp(pr, qr)

def proj_residual(target, family, s):
    N = len(family)
    G = np.zeros((N, N)); r = np.zeros(N)
    for i in range(N):
        r[i] = inner_s_fp(family[i], target, s)
        for j in range(N):
            G[i, j] = inner_s_fp(family[i], family[j], s)
    coef = np.linalg.solve(G, r)
    tnorm2 = inner_s_fp(target, target, s)
    return max(tnorm2 - 2*np.dot(coef, r) + coef @ G @ coef, 0.0)

def p_even(m):
    c = [0.0]*(2*m+1); c[2*m] = 1.0; c[2*m-2] = -m/(m-1); return c
def p_odd(m):
    c = [0.0]*(2*m+2); c[2*m+1] = 1.0; c[2*m-1] = -m/(m-1); return c

for s in [0, 1, 2, 3, 4]:
    for deg in [8, 12, 16, 20]:
        fam = [Kc_fp([1.0]), Kc_fp([0.0, 1.0])]
        for m in range(2, deg//2 + 1):
            if 2*m <= deg: fam.append(Kc_fp(p_even(m)))
            if 2*m+1 <= deg: fam.append(Kc_fp(p_odd(m)))
        r2 = proj_residual([0.0, 0.0, 1.0], fam, s)
        r3 = proj_residual([0.0, 0.0, 0.0, 1.0], fam, s)
        print(f"V4 s={s} deg<={deg}: resid x^2 = {r2:.2e}, x^3 = {r3:.2e}")
