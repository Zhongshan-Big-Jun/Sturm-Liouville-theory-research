# -*- coding: utf-8 -*-
"""s33_r1plus.py - verified R->1+ structure of the fp-component (run R-20260807T163000Z).
Replaces the refuted claim that the fp-component limits to sin(2 pi b) = -sin(pi a)/2
(F-016).  Correct leading order: S3 is the sheet a = a0 + eps*phi(b) + O(eps^2),
eps = R-1, b in [a0, b_top], with phi(b) = -R1_1(a0; a0, b)/f_const'(a0), where
R1_1 is the explicit first-order term of R1 = lam1 w1^2 - lam2 w2^2 (L^2(rho)-
normalized modes w_k = y_k/sqrt(n_k)).  Numerical evidence only (no proof role).
Outputs s33_r1plus.json."""
import numpy as np, json, os, glob
pi = np.pi
HERE = os.path.dirname(os.path.abspath(__file__))
a0 = float(np.arccos(0.25)/pi); b0 = 1 - a0
fc = 15*pi**3*np.sqrt(15)/4   # f_const'(a0), f_const(a) = 2 pi^2 (sin^2(pi a) - 4 sin^2(2 pi a))

def lam_prime(k, a, b):
    # first-order eigenvalue slope: lam_k' = -k^2 pi^2 [(b-a) - (sin(2k pi b)-sin(2k pi a))/(2 k pi)]
    return -k**2*pi**2*((b-a) - (np.sin(2*k*pi*b)-np.sin(2*k*pi*a))/(2*k*pi))

def R1_1(a, b, N=100001):
    """First-order term of R1 at eps=0.  y_k^1 solves
    -y'' - (k pi)^2 y = (lam_k' + k^2 pi^2 1_(a,b)) sin(k pi x)/(k pi), y(0)=y'(0)=0.
    Verified against finite differences of the exact secular solver to 6 digits
    (audit_report F-016; Green's function sign checked, F-018)."""
    t = np.linspace(0, 1, N); h = t[1]-t[0]
    out = 0.0
    for k, lam0 in [(1, pi**2), (2, 4*pi**2)]:
        g = (lam_prime(k, a, b) + k**2*pi**2*((t >= a) & (t <= b)))*np.sin(k*pi*t)/(k*pi)
        # y_k^1(x) = -(1/(k pi)) Int_0^x sin(k pi (x-s)) g(s) ds
        C = np.cumsum(np.cos(k*pi*t)*g)*h - 0.5*h*np.cos(k*pi*t)*g
        S = np.cumsum(np.sin(k*pi*t)*g)*h - 0.5*h*np.sin(k*pi*t)*g
        y1 = -(np.sin(k*pi*t)*C - np.cos(k*pi*t)*S)/(k*pi)
        nk0 = 1.0/(2*k**2*pi**2)
        yk0 = np.sin(k*pi*t)/(k*pi)
        nk1 = 2*np.trapezoid(yk0*y1, t) + np.trapezoid(((t >= a) & (t <= b))*yk0**2, t)
        ia = np.searchsorted(t, a); y1a = y1[ia]
        w1 = y1a/np.sqrt(nk0) - np.sqrt(2)*np.sin(k*pi*a)*nk1/(2*nk0)
        lp = lam_prime(k, a, b)
        out += ((-1)**(k+1))*(lp*(np.sqrt(2)*np.sin(k*pi*a))**2 + 2*lam0*np.sqrt(2)*np.sin(k*pi*a)*w1)
    return out

def phi(b): return -R1_1(a0, b)/fc

out = dict(a0=a0, b0=b0, fc=float(fc), phi_a0=float(phi(a0)), phi_b0=float(phi(b0)),
           h_a0_leading=float(2*a0-1), h_a0_eps_coeff=float(phi(b0)))
rows = []
for b in [a0, 0.45, 0.51, 0.60, 0.69, 0.77, 0.86, 0.95]:
    rows.append(dict(b=b, phi=float(phi(b))))
bg = np.linspace(a0+1e-5, 0.98, 60)
ph = np.array([phi(x) for x in bg])
dph = np.gradient(ph, bg)
out["phi_table"] = rows
out["phi_prime_min"] = float(dph.min()); out["phi_prime_max"] = float(dph.max())
out["phi_monotone_increasing"] = bool(dph.min() > 0)
b_top = {}
for f in glob.glob(os.path.join(HERE, "e15_*.json")):
    try:
        d = json.load(open(f))
        rowsd = [r for r in d.get("rows", []) if len(r) >= 2 and np.isfinite(r[1])]
        if rowsd:
            b_top[d["R"]] = rowsd[-1][1]
    except Exception:
        pass
out["b_top_vs_R"] = {str(k): v for k, v in sorted(b_top.items())}
with open(os.path.join(HERE, "s33_r1plus.json"), "w") as f:
    json.dump(out, f, indent=1)
print("phi(a0)=%.3e phi(b0)=%.6f phi' in [%.5f, %.5f], increasing=%s"
      % (out["phi_a0"], out["phi_b0"], out["phi_prime_min"], out["phi_prime_max"], out["phi_monotone_increasing"]))
print("h(a0) ~ %.6f + %.6f*(R-1)" % (out["h_a0_leading"], out["h_a0_eps_coeff"]))
