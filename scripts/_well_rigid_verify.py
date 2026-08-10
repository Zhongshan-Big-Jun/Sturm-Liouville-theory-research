# -*- coding: utf-8 -*-
"""Well-family small-R rigidity: verification battery (2026-08-10).
Part A: symbolic identity checks (E1-style, sympy exact).
Part B: numerical probes (E3 EVIDENCE only, NOT proofs).
"""
import sympy as sp
import numpy as np
from scipy.optimize import brentq, least_squares

x, tau, m, q = sp.symbols("x tau m q", positive=True)

# ---------------- module-level functions ----------------
def well_secular_vec(s, a, b, R):
    m = np.sqrt(R)
    A = m*s*a; psi = s*(b-a); B = m*s*(1-b)
    return (np.cos(psi)*np.sin(A) + m*np.sin(psi)*np.cos(A))*np.cos(B) \
         + (-np.sin(psi)*np.sin(A)/m + np.cos(psi)*np.cos(A))*np.sin(B)

def eigs_well(a, b, R, k=2, N=6000):
    m = np.sqrt(R)
    smax = 2 + k*np.pi*m + 4
    sp_ = np.linspace(1e-9, smax, N)
    d = well_secular_vec(sp_, a, b, R)
    signs = np.signbit(d[1:]) != np.signbit(d[:-1])
    idx = np.nonzero(signs)[0]
    out = []
    for i in idx[:k]:
        lo, hi = sp_[i], sp_[i+1]
        rr = brentq(lambda z: well_secular_vec(z, a, b, R), lo, hi, xtol=1e-12, rtol=1e-12)
        out.append(rr*rr)
    return np.sort(out)[:k]

def y_well(a, b, R, s, x):
    m = np.sqrt(R)
    if x <= a:
        return np.sin(m*s*x)/(m*s)
    if x <= b:
        y0 = np.sin(m*s*a)/(m*s); yp0 = np.cos(m*s*a)
        return y0*np.cos(s*(x-a)) + (yp0/s)*np.sin(s*(x-a))
    y0 = np.sin(m*s*a)/(m*s); yp0 = np.cos(m*s*a)
    yb = y0*np.cos(s*(b-a)) + (yp0/s)*np.sin(s*(b-a))
    ypb = -y0*s*np.sin(s*(b-a)) + yp0*np.cos(s*(b-a))
    return yb*np.cos(m*s*(x-b)) + (ypb/(m*s))*np.sin(m*s*(x-b))

def norm2_well(a, b, R, s, n=1000):
    xs = np.linspace(0, 1, n+1)
    ys = np.array([y_well(a, b, R, s, x) for x in xs])
    rho = np.where((xs >= a) & (xs <= b), 1.0, R)
    return np.trapezoid(rho*ys*ys, xs)

def fval(a, b, R, x):
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); s2 = np.sqrt(lam2)
    n1 = norm2_well(a, b, R, s1); n2 = norm2_well(a, b, R, s2)
    return lam2*y_well(a,b,R,s2,x)**2/n2 - lam1*y_well(a,b,R,s1,x)**2/n1

def good_root(R, a0, b0):
    def res(ab):
        aa, bb = ab
        return [fval(aa, bb, R, aa), fval(aa, bb, R, bb)]
    sol = least_squares(res, [a0, b0], bounds=([1e-6,1e-6],[0.999,0.999]), xtol=1e-12, ftol=1e-12, max_nfev=200)
    return sol.x, sol.cost

# ---------------- main ----------------
if __name__ == "__main__":
    print("=" * 70)
    print("PART A: exact symbolic identities")
    print("=" * 70)
    W = 1 + q*sp.cos(x)**2
    Psi = x*sp.cos(x)/sp.sin(x) + q*x*sp.sin(x)*sp.cos(x)/W
    dPsi = sp.simplify(sp.diff(Psi, x))
    N0 = 4*x - 2*sp.sin(2*x)
    N1 = 4*x*sp.cos(2*x)**2 + 4*x*sp.cos(2*x) - 2*sp.sin(2*x) - sp.sin(4*x)
    lhs = sp.simplify(dPsi * sp.sin(x)**2 * W**2)
    rhs = sp.expand_trig(-(q+1)*(2*N0+q*N1)/8)
    print("A1 Psi'*sin^2*W^2 == -(q+1)(2N0+qN1)/8 :", sp.simplify(lhs-rhs) == 0)
    H = 18*x - 10*sp.sin(2*x) + 2*x*sp.cos(4*x) + 4*x*sp.cos(2*x) - sp.sin(4*x)
    print("A2 H == N1+4N0 :", sp.simplify(H - (N1+4*N0)) == 0)
    u = sp.symbols("u", positive=True)
    Hu = sp.simplify(H.subs(x, u/2))
    Halt = 2*(u*(4+sp.cos(u)**2+sp.cos(u)) - sp.sin(u)*(5+sp.cos(u)))
    print("A3 H(2x form) == 2[u(4+c^2+c)-sin u(5+c)] :", sp.simplify(sp.expand_trig(Hu-Halt)) == 0)
    h = u*(4+sp.cos(u)**2+sp.cos(u)) - sp.sin(u)*(5+sp.cos(u))
    hp = sp.simplify(sp.expand_trig(sp.diff(h, u)))
    hp_claim = sp.expand_trig((1-sp.cos(u))*(5+sp.cos(u)) - u*sp.sin(u)*(1+2*sp.cos(u)))
    print("A4 h'(u) == (1-c)(5+c)-u sin u(1+2c) :", sp.simplify(hp-hp_claim) == 0)
    t = sp.symbols("t", positive=True)
    G = sp.tan(u/2)*(5+sp.cos(u)) - u*(1+2*sp.cos(u))
    Gt = sp.simplify(G.subs(u, 2*sp.atan(t)))
    Nt = t*(6+4*t**2) - 2*(3-t**2)*sp.atan(t)
    print("A5 G(2 arctan t)*(1+t^2) == N(t) :", sp.simplify(sp.expand_trig(Gt*(1+t**2) - Nt)) == 0)
    Npp = sp.simplify(sp.diff(Nt, t, 2))
    Npp_claim = 24*t + 4*sp.atan(t) + 4*t/(1+t**2) + 16*t/(1+t**2)**2
    print("A6 N''(t) == 24t+4 atan t+4t/(1+t^2)+16t/(1+t^2)^2 :", sp.simplify(Npp-Npp_claim) == 0)
    Jt = sp.sin(x)**2/(sp.sin(x)**2 + (1+q)*sp.cos(x)**2)
    dlogJ = sp.simplify(sp.diff(sp.log(Jt), x))
    dlogJ_claim = 2*sp.cos(x)/sp.sin(x) + 2*q*sp.sin(x)*sp.cos(x)/W
    print("A7 d/dx log J~ == 2cot x + 2q sin x cos x/W :", sp.simplify(sp.expand_trig(dlogJ-dlogJ_claim)) == 0)
    Psi_m = x*sp.cos(x)/sp.sin(x) + q*x*sp.sin(x)*sp.cos(x)/W
    r = sp.log(Jt.subs(x, tau*x)/Jt)
    dlogr = sp.simplify(sp.diff(r, x))
    dlogr_claim = (2/x)*(Psi_m.subs(x, tau*x) - Psi_m)
    print("A8 (d/dx)log r~_tau == (2/x)(Psi~(tau x)-Psi~(x)) :", sp.simplify(sp.expand_trig(dlogr-dlogr_claim)) == 0)

    print()
    print("=" * 70)
    print("PART B: numerical probes (E3 EVIDENCE)")
    print("=" * 70)
    xs = np.linspace(1e-5, np.pi-1e-5, 30001)
    for qv in [0.0, 0.25, 0.5, 0.5001, 0.55]:
        N0v = 4*xs - 2*np.sin(2*xs)
        N1v = 4*xs*np.cos(2*xs)**2 + 4*xs*np.cos(2*xs) - 2*np.sin(2*xs) - np.sin(4*xs)
        Wv = 1 + qv*np.cos(xs)**2
        Psi_p = -(qv+1)*(2*N0v + qv*N1v)/(8*np.sin(xs)**2*Wv**2)
        print(f"B1 q={qv:.4f}: max Psi~' (interior) = {Psi_p.max():+.3e}")
    Hv = 18*xs - 10*np.sin(2*xs) + 2*xs*np.cos(4*xs) + 4*xs*np.cos(2*xs) - np.sin(4*xs)
    Hpv = 18 - 16*np.cos(2*xs) - 2*np.cos(4*xs) - 8*xs*np.sin(2*xs) - 8*xs*np.sin(4*xs)
    print(f"B2 min H = {Hv.min():+.3e} (boundary ~0), min H' = {Hpv.min():+.3e}")
    us = np.linspace(1e-5, 2*np.pi/3-1e-5, 20001)
    Gv = np.tan(us/2)*(5+np.cos(us)) - us*(1+2*np.cos(us))
    tv = np.tan(us/2)
    Nv = tv*(6+4*tv**2) - 2*(3-tv**2)*np.arctan(tv)
    print(f"B2 min G(u) on (0,2pi/3) = {Gv.min():+.3e}, min N(t) on (0,sqrt3) = {Nv.min():+.3e}")

    def rtau_decr(R, tau, N=40001):
        m = np.sqrt(R)
        J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
        xx = np.linspace(1e-6, np.pi/tau-1e-6, N)
        lr = np.log(J(tau*xx)/J(xx))
        return np.diff(lr).max()
    for Rv, tau in [(1.5, 1.3), (1.5, 1.7), (1.5, 2.0), (1.6, 1.5)]:
        mx = rtau_decr(Rv, tau)
        print(f"B3 R={Rv} tau={tau}: max log-step r~_tau = {mx:+.3e} ({'decreasing' if mx <= 1e-12 else 'NOT monotone'})")

    R = 1.5; m = np.sqrt(R)
    print("B4 good-root search at R=1.5 (6 seeds):")
    found = []
    for (a0, b0) in [(0.30, 0.70), (0.25, 0.60), (0.35, 0.65), (0.20, 0.75), (0.10, 0.85), (0.40, 0.55)]:
        ab, cost = good_root(R, a0, b0)
        a, b = ab
        if cost < 1e-16 and 0 < a < b < 1:
            key = (round(a,4), round(b,4))
            if not any(abs(key[0]-f[0])<1e-3 and abs(key[1]-f[1])<1e-3 for f in found):
                found.append((a, b))
    for (a, b) in found:
        lam1, lam2 = eigs_well(a, b, R)
        s1 = np.sqrt(lam1); s2 = np.sqrt(lam2); tau = s2/s1
        A = m*s1*a; B = m*s1*(1-b)
        J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
        rA = J(tau*A)/J(A); rB = J(tau*B)/J(B)
        n1 = norm2_well(a, b, R, s1, n=1600); n2 = norm2_well(a, b, R, s2, n=1600)
        N1v = n2/n1 - np.sin(tau*A)**2/np.sin(A)**2
        print(f"  (a,b)=({a:.6f},{b:.6f}) a+b={a+b:.6f} D={lam2-lam1:.8f}")
        print(f"    A={A:.6f} B={B:.6f} |A-B|={abs(A-B):.2e}  r~_tau(A)={rA:.10f} r~_tau(B)={rB:.10f}")
        print(f"    tau={tau:.6f} pi/tau={np.pi/tau:.6f}  N1(at good root)={N1v:+.3e}")
        print(f"    sign: y2(a)={np.sin(m*s2*a)/(m*s2):+.6f} >0")
