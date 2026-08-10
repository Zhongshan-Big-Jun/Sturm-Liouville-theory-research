# -*- coding: utf-8 -*-
"""#10 verify (fixed root finder for tan mu = mu)."""
import numpy as np, math
from scipy.integrate import quad

c = 3.0

def mu_roots(N=40):
    roots = []
    for k in range(1, N+1):
        lo, hi = k*np.pi, k*np.pi + np.pi/2 - 1e-9
        assert np.tan(lo)-lo < 0 and np.tan(hi)-hi > 0
        for _ in range(100):
            mid = 0.5*(lo+hi)
            if np.tan(mid) - mid > 0: hi = mid
            else: lo = mid
        roots.append(0.5*(lo+hi))
    return np.array(roots)

MU = mu_roots(40); NCOS = 40
print("first 4 roots:", [round(float(m),4) for m in MU[:4]], "(standard: 4.4934, 7.7253, 10.9041, 14.2074)")

def basis():
    for n in range(0, NCOS+1):
        lam = c if n == 0 else (n*np.pi)**2 + c
        na = 2.0 if n == 0 else 1.0
        fn = (lambda x: 1.0) if n == 0 else (lambda x, n=n: np.cos(n*np.pi*x))
        yield lam, na, fn
    for mu in MU:
        yield mu**2 + c, 1.0, (lambda x, mu=mu: np.sin(mu*x))

def peval(asc, x):
    return np.polyval(asc[::-1], x)

def proj(poly, fn):
    return quad(lambda x: peval(poly, x)*fn(x), -1, 1, limit=200)[0]

def inner_t(polyA, polyB, t):
    A = list(polyA) + [0.0]*(40-len(polyA))
    B = list(polyB) + [0.0]*(40-len(polyB))
    out = 0.0
    for lam, na, fn in basis():
        a = proj(A, fn); b = proj(B, fn)
        out += lam**t * a*b/na
    return out

def kc(poly):
    out = [0.0]*len(poly)
    for j in range(len(poly)):
        out[j] += c*poly[j]
        if j+2 < len(poly):
            out[j] -= (j+1)*(j+2)*poly[j+2]
    return out

def p_n(n):
    m = n//2
    cc = [0.0]*(n+1); cc[n] = 1.0
    if m >= 2:
        cc[n-2] = -m/(m-1)
    return cc

def norm_t(poly, t):
    return inner_t(poly, poly, t)**0.5

print("=== (A) transport on p_n: ||K_c p_n||_{t-2} = ||p_n||_t ===")
allok = True
for t in (0.5, 1.5, 1.75, 2.5, 3.0):
    for n in (0, 1, 4, 5, 6, 7):
        lhs = norm_t(kc(p_n(n)), t-2)
        rhs = norm_t(p_n(n), t)
        ok = abs(lhs-rhs) < 1e-6
        allok &= ok
        if not ok:
            print(f"  MISMATCH t={t} n={n}: {lhs:.6f} vs {rhs:.6f}")
print(f"  all ok: {allok}")

print("\n=== (B) jump identity at fractional t (mixed-parity w) ===")
def A_m(m): return 2*m*(2*m-1) + c*m/(m-1)
def B_m(m): return 2*m*(2*m-3)
def xk(k):
    p = [0.0]*40; p[k] = 1.0
    return p
w = [0.0]*40; w[7]=1.0; w[3]=-2.0; w[0]=0.5
allok = True
for t in (0.0, 0.75, 1.5, 1.75):
    for m in (2, 3, 5, 8):
        orth = inner_t(w, kc(p_n(2*m)), t)
        rhs = c*inner_t(w, xk(2*m), t) - A_m(m)*inner_t(w, xk(2*m-2), t) + B_m(m)*inner_t(w, xk(2*m-4), t)
        ok = abs(orth - rhs) < 1e-7
        allok &= ok
        if not ok: print(f"  MISMATCH t={t} m={m}: {orth:.6e} vs {rhs:.6e}")
print(f"  all ok: {allok}")

print("\n=== (C) moment bound ratio ||x^k||_t / k^{ceil(t)-1/2} ===")
for t in (0.75, 1.5, 1.75, 2.5):
    beta = math.ceil(t) - 0.5
    row = []
    for k in (2, 6, 10, 14, 18):
        p = [0.0]*40; p[k] = 1.0
        row.append(norm_t(p, t)/k**beta)
    print(f"  t={t}: {[round(float(r),3) for r in row]}")

print("\n=== (D) pinned solution growth v_j >= (4/c)^{j-1} j! ===")
v = {0: 0.0, 1: 1.0}
for j in range(2, 31):
    v[j] = (A_m(j)*v[j-1] - B_m(j)*v[j-2])/c
ok = all(v[j] >= (4.0/c)**(j-1)*math.factorial(j) for j in range(2, 31))
print(f"  all j<=30: {ok}; v_30 = {v[30]:.3e}")
