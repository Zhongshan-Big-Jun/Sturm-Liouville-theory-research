# -*- coding: utf-8 -*-
"""Focused well-family critical point analysis (E3 evidence only).
(1) exhaustive critical point search in a<=b; (2) Hessian at symmetric point;
(3) sign pattern of f; (4) r~_tau equal pairs and second-equation test."""
import numpy as np
from scipy.optimize import least_squares, root
from _well_landscape2 import eigs_well, fval, well_secular, y_well, norm2_well

def crit_search(R, n=26):
    out = []
    for a in np.linspace(0.03, 0.95, n):
        for b in np.linspace(a+0.03, 0.99, n):
            def res(ab):
                aa, bb = ab
                return [fval(aa, bb, R, aa), fval(aa, bb, R, bb)]
            sol = least_squares(res, [a, b], bounds=([1e-6, 1e-6], [0.999, 0.999]),
                                xtol=1e-12, ftol=1e-12, max_nfev=80)
            if sol.cost < 1e-20 and sol.x[0] <= sol.x[1] + 1e-9:
                key = (round(sol.x[0], 5), round(sol.x[1], 5))
                if not any(abs(key[0]-k[0])<1e-4 and abs(key[1]-k[1])<1e-4 for k in out):
                    out.append(key)
    return out

def hessian(R, ab, h=1e-5):
    a, b = ab
    def D(ab):
        lam = eigs_well(ab[0], ab[1], R)
        return lam[1]-lam[0]
    d = {}
    for (i, j) in [(2,0),(1,1),(0,2)]:
        # mixed partial
        pass
    f00 = D((a, b))
    fa = D((a+h, b)); fb = D((a, b+h)); fab = D((a+h, b+h))
    fa_ = D((a-h, b)); fb_ = D((a, b-h)); fab_ = D((a-h, b-h))
    fafb = D((a+h, b-h)); fafb_ = D((a-h, b+h))
    daa = (fa - 2*f00 + fa_)/h**2
    dbb = (fb - 2*f00 + fb_)/h**2
    dab = (fab - fa - fb + f00)/h**2
    return np.array([[daa, dab], [dab, dbb]])

def rtau(m, tau, x):
    J = lambda t: np.sin(t)**2/(np.sin(t)**2 + m*m*np.cos(t)**2)
    return J(tau*x)/J(x)

if __name__ == '__main__':
    import sys
    R = float(sys.argv[1]) if len(sys.argv) > 1 else 4.0
    m = np.sqrt(R)
    crits = crit_search(R)
    print(f"R={R}: interior critical points in a<=b: {len(crits)}")
    for k in crits:
        lam = eigs_well(k[0], k[1], R)
        print(f"  (a,b)=({k[0]:.5f},{k[1]:.5f}) a+b={k[0]+k[1]:.5f} D={lam[1]-lam[0]:.8f}")
        if abs(k[0]+k[1]-1) < 1e-3:
            H = hessian(R, k)
            w, v = np.linalg.eigh(H)
            print(f"    Hessian eigvals: {w[0]:.4f}, {w[1]:.4f}")
    # sign pattern of f at symmetric point
    a, b = crits[0]
    xs = np.linspace(1e-6, 1-1e-6, 2001)
    fv = np.array([fval(a, b, R, x) for x in xs])
    print("  f sign regions (at symmetric crit): ", end="")
    sgn = np.sign(fv)
    changes = np.nonzero(sgn[1:] != sgn[:-1])[0]
    regions = [xs[0]]
    for c in changes: regions.append(xs[c])
    regions.append(xs[-1])
    print([round(t,4) for t in regions])
    # r~_tau equal pair test: at the symmetric point compute A, B, tau
    lam1, lam2 = eigs_well(a, b, R)
    s1 = np.sqrt(lam1); s2 = np.sqrt(lam2); tau = s2/s1
    A = m*s1*a; B = m*s1*(1-b)
    print(f"  tau={tau:.6f} A={A:.6f} B={B:.6f} pi/tau={np.pi/tau:.6f}")
    # search for non-diagonal equal pairs of r~_tau on (0,pi/tau)
    xs = np.linspace(1e-6, np.pi/tau-1e-6, 200000)
    rv = rtau(m, tau, xs)
    # find pairs x1<x2 with r(x1)=r(x2): use level sets; simple scan by sorting
    pairs = []
    for x1 in np.linspace(0.05, np.pi/tau-0.05, 400):
        tgt = rtau(m, tau, x1)
        cand = np.argmin(np.abs(rv - tgt))
        x2 = xs[cand]
        if abs(x2 - x1) > 1e-3 and abs(rtau(m,tau,x2)-tgt) < 1e-6:
            pairs.append((x1, x2))
    # dedupe
    seen = set()
    uniq = []
    for p in pairs:
        key = (round(min(p),3), round(max(p),3))
        if key not in seen:
            seen.add(key); uniq.append(p)
    print(f"  non-diagonal equal pairs of r~_tau: {len(uniq)} (sample)")
    for p in uniq[:6]:
        print(f"    A~{p[0]:.4f} B~{p[1]:.4f} r={rtau(m,tau,p[0]):.6f}")
