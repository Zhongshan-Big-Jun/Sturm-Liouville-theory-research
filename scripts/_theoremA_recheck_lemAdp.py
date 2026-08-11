
# -*- coding: utf-8 -*-
# Independent verification of Lemma A'' (w>=2: G>=Dbar), sliver (w<=2: G>=25),
# and T1 convergence rate for Theorem A.  All EVIDENCE only.
import mpmath as mp
mp.mp.dps = 50

def solve_phases(R, u):
    """Return (delta1, delta2, z1, z2) solving the secular equations on the TRUE
    branches: z1 = s1*ell in (0, pi/2)  (lambda1 <= pi^2 => s1 ell <= pi/2),
    z2 = s2*ell in (0, pi)              (lambda2 <= 4 pi^2 => s2 ell <= pi).
    This fixes the multiple-root issue of tan/cot periodicity for tiny u."""
    eps = 1/mp.sqrt(R)
    ell = mp.mpf(1)/2 - u
    tiny = mp.mpf('1e-12')
    # even: theta1 = pi/2 - d1 in (0, pi*u/(2*eps*ell));  d1 in (pi/2 - pi*u/(2 eps ell), pi/2)
    lim1 = mp.pi/2 - mp.pi*u/(2*eps*ell)
    lo1 = max(lim1, mp.mpf(0)) + tiny
    hi1 = mp.pi/2 - tiny
    def F1(d): return d - mp.atan(eps*mp.tan((mp.pi/2 - d)*eps*ell/u))
    d1 = mp.findroot(F1, (lo1, hi1), solver='anderson')
    # odd: z2 = (pi/2 + d2)*eps*ell/u in (0, pi) => d2 in (-pi/2, pi*u/(eps ell) - pi/2)
    lim2 = mp.pi*u/(eps*ell) - mp.pi/2
    lo2 = max(-mp.pi/2, mp.mpf(0) - mp.mpf('10')) + tiny if False else mp.mpf('-1.5707963267948966') + tiny
    hi2 = min(mp.pi/2, lim2) - tiny
    def F2(d): return d - mp.atan(eps*mp.cot((mp.pi/2 + d)*eps*ell/u))
    d2 = mp.findroot(F2, (lo2, hi2), solver='anderson')
    z1 = (mp.pi/2 - d1)*eps*ell/u
    z2 = (mp.pi/2 + d2)*eps*ell/u
    return d1, d2, z1, z2

def Gval(R, u):
    d1, d2, _, _ = solve_phases(R, u)
    mu1 = ((mp.pi/2 - d1)/u)**2
    mu2 = ((mp.pi/2 + d2)/u)**2
    return mu2 - mu1, d1, d2

def Dbar(u):
    def F(a): return mp.tan(a) - a*(1 - mp.mpf(1)/(2*u))
    a = mp.findroot(F, (mp.pi/2 + mp.mpf('1e-9'), mp.pi - mp.mpf('1e-12')), solver='anderson')
    return (a**2 - (mp.pi/2)**2)/u**2, a

# cross-check vs direct shooting (finite differences) for a few points
import numpy as np
def eig_fd(R, u, N=60001):
    # -y'' = lam*rho y, Dirichlet; central diff on uniform grid
    x = np.linspace(0.0, 1.0, N)
    h = x[1]-x[0]
    rho = np.where((x < u) | (x > 1-u), R, 1.0)
    # eigenvalues of tridiag: (2 + h^2 rho lam) y_i - y_{i-1} - y_{i+1} = 0
    from scipy.linalg import eigh_tridiagonal
    n = N-2
    diag = 2.0 + h*h*rho[1:-1]*0  # placeholder
    # standard: A y = lam B y with A = tridiag(2), B = h^2 rho diag
    d = np.full(n, 2.0)
    e = np.full(n-1, -1.0)
    B = h*h*rho[1:-1]
    s = np.sqrt(B)
    D1 = d/s**2
    E1 = e/(s[:-1]*s[1:])
    vals = eigh_tridiagonal(D1, E1, check_finite=False, eigvals_only=True)
    return sorted(vals)[:2]

print("== cross-check secular vs FD (EVIDENCE) ==")
for R, u in [(1500.0, 0.05), (1500.0, 0.3), (4.0, 0.3), (1e4, 0.4)]:
    Rm, um = mp.mpf(R), mp.mpf(u)
    G, d1, d2 = Gval(Rm, um)
    l1, l2 = eig_fd(R, u)
    Gfd = R*(l2-l1)
    print("  R=%s u=%s: G_secular=%s  G_fd=%s  rel=%s" % (R, u, mp.nstr(G,12), mp.nstr(Gfd,8), mp.nstr(abs(G-Gfd)/G, 4)))

print("== Lemma A'': R>=1500, w>=2 => G >= Dbar(u) ==")
worst = (mp.mpf(10), None)
Rs = [1500, 2000, 5000, 1e4, 1e5, 1e6, 1e8]
fail = 0
for R in Rs:
    Rm = mp.mpf(R)
    eps = 1/mp.sqrt(Rm)
    us = mp.linspace(2*eps, mp.mpf('0.499'), 25)
    for u in us:
        G, d1, d2 = Gval(Rm, u)
        Dv, _ = Dbar(u)
        m = G - Dv
        if m < 0:
            fail += 1
            print("  FAIL R=%s u=%s G=%s Dbar=%s" % (R, mp.nstr(u,8), mp.nstr(G,12), mp.nstr(Dv,12)))
        if m < worst[0]:
            worst = (m, (R, u))
print("  min margin G-Dbar =", mp.nstr(worst[0], 12), "at", worst[1], "| failures:", fail)

print("== sliver: R>=1500, w<=2 => G >= 25 ==")
worstS = (mp.mpf(10), None)
failS = 0
for R in Rs:
    Rm = mp.mpf(R)
    umax = 2/mp.sqrt(Rm)
    us = [umax*mp.mpf(t) for t in [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]]
    for u in us:
        G, d1, d2 = Gval(Rm, u)
        if G < 25:
            failS += 1
            print("  FAIL R=%s u=%s G=%s" % (R, mp.nstr(u,8), mp.nstr(G,12)))
        if G < worstS[0]:
            worstS = (G, (R, u))
print("  min G in sliver =", mp.nstr(worstS[0], 12), "at", worstS[1], "| failures:", failS)

print("== def1/def2 structure at sample points (Lemma A'' region) ==")
for R, u in [(1500, 0.3), (1500, 0.45), (1e4, 0.1), (1e6, 0.49)]:
    Rm, um = mp.mpf(R), mp.mpf(u)
    eps = 1/mp.sqrt(Rm)
    ell = mp.mpf(1)/2 - um
    d1, d2, z1, z2 = solve_phases(Rm, um)
    th1 = mp.pi/2 - d1
    th2 = mp.pi/2 + d2
    _, a = Dbar(um)
    def1 = mp.pi**2/4 - th1**2
    def2 = a**2 - th2**2
    G, _, _ = Gval(Rm, um)
    Dv, _ = Dbar(um)
    print("  R=%s u=%s: def1=%s def2=%s def1>=def2:%s | G-Dbar=%s" % (
        R, mp.nstr(um,6), mp.nstr(def1,10), mp.nstr(def2,10), def1>=def2, mp.nstr(G-Dv, 8)))
    print("     d1=%s d2=%s z2=%s (<=pi/8=%s)" % (mp.nstr(d1,8), mp.nstr(d2,8), mp.nstr(z2,8), mp.nstr(mp.pi/8,8)))

print("== T1: convergence G(R,u*) -> Dbar(u*) for fixed u* ==")
uG = mp.mpf('0.329922508120066549592808055012')
Dv, _ = Dbar(uG)
for R in [1500, 1e4, 1e6, 1e8]:
    G, _, _ = Gval(mp.mpf(R), uG)
    print("  R=%s: G-Dbar* = %s" % (R, mp.nstr(G - Dv, 10)))
print("  (doc: errors 1.04e-2, 1.56e-3, 1.57e-5, 2.05e-7)")
print("== T1: G(1500, 2/sqrt(1500)) ==", mp.nstr(Gval(1500, 2/mp.sqrt(1500))[0], 10), "(doc 91.7263)")
