# -*- coding: utf-8 -*-
"""Numerical search for n=3, mu=2 minimizing relay roots (EVIDENCE only)."""
import numpy as np
from scipy.integrate import solve_ivp

def relay_rhs(t, z, R, mu):
    U, Ut, V, Vt = z
    S = U*U - mu*mu*V*V
    rho = 1.0 if S > 0 else R
    return [Ut, -rho*U, Vt, -mu*mu*rho*V]

def event_U(t, z, R, mu):
    return z[0]
event_U.direction = 0

def event_V(t, z, R, mu):
    return z[2]
event_V.direction = 0

def integrate(q, R, mu, n, tmax=120.0):
    z0 = [0.0, 1.0, 0.0, q]
    sol = solve_ivp(relay_rhs, [0, tmax], z0, args=(R, mu),
                    events=(event_U, event_V), max_step=0.005,
                    rtol=1e-9, atol=1e-11, dense_output=True)
    u_events = sol.t_events[0] if sol.t_events[0] is not None else np.array([])
    v_events = sol.t_events[1] if sol.t_events[1] is not None else np.array([])
    # exclude t=0? events at t=0? solve_ivp may not include initial.
    u_events = u_events[u_events > 1e-9]
    v_events = v_events[v_events > 1e-9]
    if len(u_events) >= n and len(v_events) >= n+1:
        TU = u_events[n-1]
        TV = v_events[n]
        # compute integrals up to TU using dense output
        ts = np.linspace(0, TU, 2000)
        ys = sol.sol(ts)
        U = ys[0]; V = ys[2]
        S = U*U - mu*mu*V*V
        rho = np.where(S > 0, 1.0, R)
        IU = np.trapezoid(rho*U*U, ts)
        IV = np.trapezoid(rho*V*V, ts)
        return TU, TV, IU, IV
    return None

def scan(R, mu, n, qs):
    print(f'Scan n={n}, mu={mu}, R={R}')
    found = []
    for q in qs:
        res = integrate(q, R, mu, n)
        if res is None:
            continue
        TU, TV, IU, IV = res
        A = TU - TV
        B = IU - IV
        if abs(A) < 0.02 and abs(B) < 0.02:
            found.append((q, TU, TV, IU, IV, A, B))
            print('  ROOT candidate q=', q, 'TU=', TU, 'TV=', TV, 'IU=', IU, 'IV=', IV, 'A=', A, 'B=', B)
    if not found:
        print('  no candidate in scan')
    return found

if __name__ == '__main__':
    for R in [1.5, 2.0, 4.0, 10.0]:
        qs = np.linspace(1.001, 30.0, 300)
        scan(R, 2.0, 3, qs)
