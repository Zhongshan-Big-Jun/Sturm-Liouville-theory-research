# -*- coding: utf-8 -*-
"""clean_lib.py v2: exact 3-block formulas (verified vs ODE). y'(0)=1 normalization."""
import numpy as np

def sec(s, a, b, R):
    m = np.sqrt(R)
    alpha = s*a; beta = s*(1-b); theta = s*m*(b-a)
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    ct, st = np.cos(theta), np.sin(theta)
    return cb*ct*sa - m*sb*st*sa + (cb*st/m)*ca + sb*ct*ca

def y_at(s, a, b, R, x):
    m = np.sqrt(R)
    alpha = s*a
    if x <= a:
        return np.sin(s*x)/s
    elif x <= b:
        u = x - a
        return (np.sin(alpha)*np.cos(s*m*u) + (np.cos(alpha)/m)*np.sin(s*m*u))/s
    else:
        v = x - b
        theta = s*m*(b-a)
        yb = (np.sin(alpha)*np.cos(theta) + (np.cos(alpha)/m)*np.sin(theta))/s
        ypb = -m*np.sin(theta)*np.sin(alpha) + np.cos(theta)*np.cos(alpha)
        return np.cos(s*v)*yb + np.sin(s*v)*ypb/s

def norm_n(s, a, b, R):
    """n(s) = int_0^1 rho y^2 dx."""
    m = np.sqrt(R)
    L = b-a; beta = 1-b
    alpha = s*a; theta = s*m*L
    I1 = a/2 - np.sin(2*alpha)/(4*s)
    Icc = L/2 + np.sin(2*theta)/(4*s*m)
    Iss = L/2 - np.sin(2*theta)/(4*s*m)
    Ics = np.sin(theta)**2/(2*s*m)
    sa = np.sin(alpha); ca = np.cos(alpha)
    I2 = sa*sa*Icc + (ca/m)**2*Iss + 2*sa*(ca/m)*Ics
    yb_scaled = sa*np.cos(theta) + (ca/m)*np.sin(theta)      # s*y(b)
    ypb = -m*np.sin(theta)*np.sin(alpha) + np.cos(theta)*np.cos(alpha)  # y'(b)
    Icc3 = beta/2 + np.sin(2*s*beta)/(4*s)
    Iss3 = beta/2 - np.sin(2*s*beta)/(4*s)
    Ics3 = np.sin(s*beta)**2/(2*s)
    # y(b+v) = [cos(sv)*yb_scaled + sin(sv)*ypb]/s
    I3 = (yb_scaled**2*Icc3 + ypb**2*Iss3 + 2*yb_scaled*ypb*Ics3)/s**2
    return (I1 + R*I2)/s**2 + I3

def R1_R2(a, b, R, s1=None, s2=None):
    if s1 is None or s2 is None:
        s1, s2 = roots2(a, b, R)
    n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
    y1a = np.sin(s1*a)/s1; y2a = np.sin(s2*a)/s2
    y1b = y_at(s1, a, b, R, b); y2b = y_at(s2, a, b, R, b)
    R1 = s1**2*y1a**2/n1 - s2**2*y2a**2/n2
    R2 = s1**2*y1b**2/n1 - s2**2*y2b**2/n2
    return R1, R2

def roots2(a, b, R, ns=4001):
    s = np.linspace(1e-8, 2*np.pi, ns)
    M = np.array([sec(si, a, b, R) for si in s])
    ch = np.signbit(M[1:]) != np.signbit(M[:-1])
    idx = np.nonzero(ch)[0]
    out = []
    for i in idx[:2]:
        lo, hi = s[i], s[i+1]
        flo = sec(lo, a, b, R)
        for _ in range(70):
            md = 0.5*(lo+hi)
            if np.signbit(sec(md, a, b, R)) == np.signbit(flo): lo = md
            else: hi = md
        out.append(0.5*(lo+hi))
    return out[0], out[1]

if __name__ == "__main__":
    from scipy.integrate import solve_ivp
    a, b, R = 0.451485465757, 0.548514534243, 4.0
    def rho(x): return np.where((x > a) & (x < b), R, 1.0)
    s1, s2 = roots2(a, b, R)
    print("s1,s2:", s1, s2)
    for s in [s1, s2]:
        sol = solve_ivp(lambda t, y: [y[1], -s*s*rho(t)*y[0]], (0,1), [0.0,1.0], t_eval=np.linspace(0,1,6001), rtol=1e-11, atol=1e-13, max_step=0.0003)
        nq = np.trapezoid(rho(sol.t)*sol.y[0]**2, sol.t)
        na = norm_n(s, a, b, R)
        print(f"s={s:.8f}: n_quad={nq:.10f} n_analytic={na:.10f} rel={abs(nq-na)/nq:.2e}")
    R1, R2 = R1_R2(a, b, R, s1, s2)
    print("clean R1, R2:", R1, R2)
    import sys
    sys.path.insert(0, r"F:\LaTeX\BVE research\runs\rigorous-open-math-research\R-20260806T011500Z-o3abranch-E8E56F\reproducibility")
    from agentB_lib import config, f_at
    cfg = config(a, b, R)
    print("lib R1, R2  :", float(f_at(a,b,R,a,cfg)), float(f_at(a,b,R,b,cfg)))
