# -*- coding: utf-8 -*-
"""ode_check.py: fully independent ODE-shooting check of the h'<0 finding at R=1e4, a=0.57364."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def shoot(a, b, R):
    def rho(x): return np.where((x > a) & (x < b), R, 1.0)
    def y1_at_s(s):
        sol = solve_ivp(lambda t, y: [y[1], -s*s*rho(t)*y[0]], (0,1), [0.0,1.0],
                        rtol=1e-12, atol=1e-14, max_step=0.0005)
        return sol.y[0,-1]
    s1 = brentq(lambda s: y1_at_s(s), 1e-8, np.pi)
    s2 = brentq(lambda s: y1_at_s(s), np.pi, 2*np.pi)
    return s1, s2, rho

def cfg_ode(a, b, R):
    s1, s2, rho = shoot(a, b, R)
    def yvals(s):
        sol = solve_ivp(lambda t, y: [y[1], -s*s*rho(t)*y[0]], (0,1), [0.0,1.0],
                        t_eval=np.linspace(0,1,4001), rtol=1e-12, atol=1e-14, max_step=0.0005)
        return sol.t, sol.y
    t, Y1 = yvals(s1); _, Y2 = yvals(s2)
    r = rho(t)
    n1 = np.trapezoid(r*Y1[0]**2, t); n2 = np.trapezoid(r*Y2[0]**2, t)
    def f(x):
        i = int(np.argmin(np.abs(t-x)))
        u1 = Y1[0,i]/np.sqrt(n1); u2 = Y2[0,i]/np.sqrt(n2)
        return s1*s1*u1*u1 - s2*s2*u2*u2
    def v(x):
        i = int(np.argmin(np.abs(t-x)))
        return Y2[0,i]/Y1[0,i]
    return f, v

R = 1e4; a = 0.57364
print("=== ODE check: R=1e4, a=0.57364 ===")
# R1(a,b) scan over b to find g1
def R1v(b): return cfg_ode(a, b, R)[0](a)
def R2v(b): return cfg_ode(a, b, R)[0](b)
for b in [0.5740, 0.5750, 0.5760, 0.5770, 0.5774, 0.5778, 0.5785]:
    f, v = cfg_ode(a, b, R)
    print(f"  b={b:.4f}: R1=f(a)={f(a):+.4e} R2=f(b)={f(b):+.4e} v(a)={v(a):+.4f} v(b)={v(b):+.4f}")
# branch roots
g1 = brentq(lambda b: cfg_ode(a,b,R)[0](a), 0.5768, 0.5780)
g2 = brentq(lambda b: cfg_ode(a,b,R)[0](b), 0.5745, 0.5750)
print(f"  g1={g1:.8f} g2={g2:.8f} h={g1-g2:+.6e}")
# h' via FD with ODE
h = 1e-4
g1p = (brentq(lambda b: cfg_ode(a+h,b,R)[0](a+h), 0.5768, 0.5780) - brentq(lambda b: cfg_ode(a-h,b,R)[0](a-h), 0.5768, 0.5780))/(2*h)
g2p = (brentq(lambda b: cfg_ode(a+h,b,R)[0](b), 0.5745, 0.5750) - brentq(lambda b: cfg_ode(a-h,b,R)[0](b), 0.5745, 0.5750))/(2*h)
print(f"  g1'={g1p:+.6f} g2'={g2p:+.6f} h'={g1p-g2p:+.6f}")
