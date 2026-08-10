# -*- coding: utf-8 -*-
"""verify_profile_asym.py - verify the leading-order branch/eigenvalue/fp
asymptotics of the barrier family at large R.

Claims verified (each marked [LO] = leading order; numerics only):
  (P1) fp:  a_fp = 1/2 - xi*/q + o(1/q),  xi* solves tan(2 pi xi) = 1/(2 sqrt2 pi xi)
       s1 = alpha/sqrt(q), alpha^2 = 2/xi* ;  s2 = 2 pi - kappa/q, kappa = 2(tan(2 pi xi*) - 2 pi xi*)
  (P2) branch b = a + W(a)/q with
       a < 1/2: sin(pi W/(1-a)) = sqrt(2a) * pi W/(1-a) + O(1/q)
       a > 1/2: (s2 - pi/a)^2 q^2 = 1/(2 pi^2 (1-a) W^2) + O(1/q)   [kappa^2 law]
  (P3) endpoints: h(a0)*q -> W(a0)-W(1-a0) < 0 ; h(beta')*q -> -(h(a0)*q) > 0
  (P4) G(fp) -> 1.410... (strictly below sqrt(2); no closed form yet)
"""
import numpy as np, sys, json, os
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import sec, norm_n

def roots2(aa, bb, RR, n=120001):
    s = np.linspace(1e-9, 8.0, n)
    M = sec(s, aa, bb, RR)
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0][:3]
    out = []
    for i in idx:
        lo, hi = s[i], s[i+1]
        for _ in range(45):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, aa, bb, RR)) == np.signbit(M[i]): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out

def R1full(a, b, R):
    if b <= a:
        return None
    rr = roots2(a, b, R)
    if len(rr) < 2: return None
    s1, s2 = rr[0], rr[1]
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    return (np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2, s1, s2, n1, n2)

def branch_b(a, R, b0, tol=1e-12):
    """Refine branch root near b0 (fp-component)."""
    lo, hi = b0 - 2e-4, b0 + 2e-4
    f_lo = f_hi = None
    for _ in range(8):
        r_lo = R1full(a, lo, R); r_hi = R1full(a, hi, R)
        f_lo = r_lo[0] if r_lo is not None else None
        f_hi = r_hi[0] if r_hi is not None else None
        if f_lo is not None and f_hi is not None and f_lo*f_hi < 0: break
        lo = max(lo - 5e-4, a + 1e-7); hi += 5e-4
    if f_lo is None or f_hi is None or f_lo*f_hi > 0:
        return None
    return brentq(lambda bb: R1full(a, bb, R)[0], lo, hi, xtol=tol)

def solve_a_fp(R, guess):
    """Solve R1(u,1-u,R)=0 in u near guess (u < 1/2 only)."""
    lo, hi = max(guess - 3e-3, 0.01), min(guess + 3e-3, 0.5 - 1e-7)
    def feval(x):
        r = R1full(x, 1-x, R)
        return r[0] if r is not None else None
    f_lo, f_hi = feval(lo), feval(hi)
    if f_lo is None or f_hi is None or f_lo*f_hi > 0:
        for _ in range(6):
            lo = max(lo - 1e-2, 0.01); hi = min(hi + 1e-2, 0.5 - 1e-7)
            f_lo, f_hi = feval(lo), feval(hi)
            if f_lo is not None and f_hi is not None and f_lo*f_hi < 0: break
    if f_lo is None or f_hi is None or f_lo*f_hi > 0: return None
    return brentq(feval, lo, hi, xtol=1e-12)

def main():
    out = {}
    a0 = float(np.arccos(0.25)/np.pi)
    # P1: fp asymptotics
    def xi_equation(xi):
        return xi*np.tan(2*np.pi*xi) - 1/(2*np.sqrt(2)*np.pi)
    from scipy.optimize import brentq as bq
    xi_star = bq(xi_equation, 0.05, 0.25)
    alpha2 = 2/xi_star
    kappa_star = 2*(np.tan(2*np.pi*xi_star) - 2*np.pi*xi_star)
    out["xi_star"] = xi_star; out["alpha2"] = alpha2; out["kappa_star"] = kappa_star
    print("xi* = %.12f  alpha^2 = %.8f  kappa* = %.8f" % (xi_star, alpha2, kappa_star))
    fp_rows = []
    for R in [1e4, 1e5, 1e6]:
        q = np.sqrt(R)
        guess = 0.5 - xi_star/q
        u = solve_a_fp(R, guess)
        if u is None:
            print("R=%.0e fp solve failed" % R); continue
        rr = roots2(u, 1-u, R)
        s1, s2 = rr[0], rr[1]
        rec = dict(R=R, fp=u, delta_q=(0.5-u)*q, s1_q12=s1*np.sqrt(q), s2_off=(2*np.pi-s2)*q)
        fp_rows.append(rec)
        print("R=%.0e fp=%.9f (0.5-fp)q=%.6f s1*sqrt(q)=%.6f (2pi-s2)q=%.6f" %
              (R, u, (0.5-u)*q, s1*np.sqrt(q), (2*np.pi-s2)*q))
    out["fp_rows"] = fp_rows
    # P2: branch profile at R=1e6
    R = 1e6; q = np.sqrt(R)
    # trace via continuation in a from fp
    u = solve_a_fp(R, 0.5 - xi_star/q)
    prof = []
    for a in [a0+1e-5, 0.45, 0.47, 0.51, 0.55, 0.58, 1-a0-1e-5]:
        b0 = a + 0.0003 if a < 0.5 else a + 0.0004
        # get a good initial: scan near b=a+[0.0001,0.0005]
        b = branch_b(a, R, a + 0.00035)
        if b is None:
            print("a=%.4f branch solve failed" % a); continue
        rr = R1full(a, b, R)
        s1, s2 = rr[1], rr[2]
        W = (b-a)*q
        row = dict(a=a, b=b, W=W, s1=s1, s2=s2)
        if a < 0.5:
            uu = np.pi*W/(1-a)
            row["sin_u"] = np.sin(uu); row["u_sqrt2a"] = uu*np.sqrt(2*a)
        else:
            kappa = (s2 - np.pi/a)*q
            row["kappa2"] = kappa**2
            row["kappa2_pred"] = 1/(2*np.pi**2*(1-a)*W**2)
        prof.append(row)
        print("a=%.5f W=%.5f " % (a, W) + ("sin(u)=%.5f vs %.5f" % (row.get("sin_u",0), row.get("u_sqrt2a",0)) if a < 0.5 else "kappa^2=%.4f vs %.4f" % (row["kappa2"], row["kappa2_pred"])))
    out["profile_R1e6"] = prof
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile_asym_verify.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    print("saved profile_asym_verify.json")

if __name__ == "__main__":
    main()


