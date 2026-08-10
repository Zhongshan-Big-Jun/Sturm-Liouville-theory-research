# -*- coding: utf-8 -*-
"""G2_largeq.py -- margin of G2 >= 0 for q >= q0; parametrized by gamma."""
import numpy as np

def margin(q, g):
    # LHS - RHS for G2>=0 rewritten: -W(pi-g)*(q + c*Phi) - 2c(pi-g)(q^2-1) sin g cos g
    # with c = atan(q tan g)/(pi-g); equivalently 2c(pi-g) = 2 atan(q tan g)
    t = np.tan(g)
    at = np.arctan(q*t)
    W = 3 - 2*(np.pi-g)/t        # W(pi-g) = 3 - 2(pi-g) cot g
    Ph = np.cos(g)**2 + q*q*np.sin(g)**2
    c = at/(np.pi-g)
    D = q + c*Ph
    LHS = -W*D
    RHS = 2*at*(q*q-1)*np.sin(g)*np.cos(g)
    return LHS - RHS, LHS, RHS

print('=== margin for q >= 2 ===')
for q in [2.0, 2.5, 3.0, 5.0, 10.0, 100.0]:
    a0 = 2*np.arcsin(1/np.sqrt(2*(q+1)))
    mn = 1e9; arg = None
    for k in range(1, 401):
        g = a0*k/400
        m, L, R = margin(q, g)
        if m < mn: mn, arg = m, (g, L, R)
    print(f'  q={q:<6}: min margin={mn:+.6f} at g={arg[0]:.4f} (LHS={arg[1]:+.4f}, RHS={arg[2]:+.4f})')

print()
print('=== q near q*: where is G2<0 possible? c_G2(q) near 1/2 ===')
def G2_of_c(c, q):
    from scipy.optimize import brentq
    def O(a):
        if a == np.pi/2: return np.pi/2
        return np.arctan(-q*np.tan(a)) if a > np.pi/2 else np.pi - np.arctan(q*np.tan(a))
    a2 = brentq(lambda a: O(a) - c*a, np.pi/2+1e-13, np.pi-1e-13)
    Ph = np.cos(a2)**2 + q*q*np.sin(a2)**2
    W = 3 + 2*a2/np.tan(a2)
    return -Ph*W/(q+c*Ph) + 2*c*a2*Ph*(q*q-1)*np.sin(a2)*np.cos(a2)/(q+c*Ph)**2
for q in [1.86, 1.87, 1.88, 1.9]:
    vals = [G2_of_c(c, q) for c in np.linspace(0.4, 0.5, 41)]
    mn = min(vals)
    print(f'  q={q}: min G2 on (0.4,0.5) grid = {mn:+.6f}')
