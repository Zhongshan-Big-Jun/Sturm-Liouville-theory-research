# -*- coding: utf-8 -*-
"""#10/#7: fractional window 3/2<=s<2. Verify:
(a) ||x^k||_t <= c^{t/2}||x^k||_0 for t in [-1/2,0) (spectral computation);
(b) interpolation ||x^k||_s ~ k^{s-1/2} for s in [0,2];
(c) moment-jump contradiction in the fractional window (superfactorial vs polynomial)."""
import numpy as np
from fractions import Fraction as F
import math

# spectral decomposition of K_c: eigenfunctions cos(n pi x) [lam=(n pi)^2+c], sin(mu_n x) [lam=mu_n^2+c]
def cos_normsq(k, n):
    # (x^k, cos(n pi x))_L2 on [-1,1]
    from scipy.integrate import quad
    val, _ = quad(lambda x: x**k*np.cos(n*np.pi*x), -1, 1, limit=200)
    nc, _ = quad(lambda x: np.cos(n*np.pi*x)**2, -1, 1, limit=200)
    return val, nc

def sin_normsq(k, mu):
    from scipy.integrate import quad
    val, _ = quad(lambda x: x**k*np.sin(mu*x), -1, 1, limit=200)
    nc, _ = quad(lambda x: np.sin(mu*x)**2, -1, 1, limit=200)
    return val, nc

def mu_roots(N=30):
    # positive roots of tan mu = mu
    roots = []
    for k in range(1, N+1):
        lo, hi = (k-0.5)*np.pi + 0.1, (k+0.5)*np.pi - 0.1
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if np.tan(mid) - mid > 0: hi = mid
            else: lo = mid
        roots.append(0.5*(lo+hi))
    return roots

c = 3.0
roots_mu = mu_roots(40)
print("=== (a) ||x^k||_t <= c^{t/2} ||x^k||_0 for t<0 (spectral) ===")
from scipy.integrate import quad
for t in (-0.5, -0.25, -0.1):
    for k in (2, 4, 8):
        s2 = 0.0
        for n in range(0, 30):
            val, nc = cos_normsq(k, n)
            lam = (n*np.pi)**2 + c
            s2 += lam**t * val**2 / nc if n > 0 else lam**t * (val**2 / 2.0)
        for mu in roots_mu:
            val, nc = sin_normsq(k, mu)
            lam = mu**2 + c
            s2 += lam**t * val**2 / nc
        norm0 = math.sqrt(2.0/(2*k+1))
        bound = c**(t/2) * norm0
        print(f"  t={t:+.2f} k={k}: ||x^k||_t = {s2**0.5:.5f}, bound c^(t/2)||x^k||_0 = {bound:.5f}, ok = {s2**0.5 <= bound*1.02}")

print("=== (b) interpolation: ||x^k||_s vs k^(s-1/2) for s=1.5,1.75 (spectral, via (a) + integer norms) ===")
# ||x^k||_s^2 = sum lam^s * coeff^2 ; compute for s=1.5, 1.75 directly
for s in (1.5, 1.75):
    for k in (2, 4, 8, 16):
        s2 = 0.0
        for n in range(0, 30):
            val, nc = cos_normsq(k, n)
            lam = (n*np.pi)**2 + c
            s2 += lam**s * val**2 / nc if n > 0 else lam**s * (val**2 / 2.0)
        for mu in roots_mu:
            val, nc = sin_normsq(k, mu)
            lam = mu**2 + c
            s2 += lam**s * val**2 / nc
        # compare with C * k^{2(s-1/2)}: check log(sqrt(s2))/log(k) ~ s-1/2
        ex = math.log(s2**0.5)/math.log(k) if k > 1 else 0
        print(f"  s={s}: k={k}: ||x^k||_s = {s2**0.5:.4e}, log/ log k = {ex:.3f} (expect {s-0.5:.3f})")
