# -*- coding: utf-8 -*-
"""H3 v36: backward iteration with target nu_j ~ D/(2j); check nu_0 != 0; odd-system check."""
import math
from fractions import Fraction as F

def coeffs_nu(c, j, par):
    if par == 'e':
        P = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        T = F(4)*j*(4*j-5)
    else:
        P = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        R = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        T = F(4)*j*(4*j-3)
    return P, Q, R, T

def backward_nu_target(cF, par, D, M):
    """Backward iterate nu-recurrence with asymptotic target nu_j = D/(2j) (even) or D/(2j+1).
    State: (nu_j, nu_{j-1}, nu_{j-2}); iterate j=M down to 2."""
    c = cF
    def target(j):
        return F(D, 2*j+1) if par == 'e' else F(D, 2*j+1)
    # state for j = M: (nu_M, nu_{M-1}, nu_{M-2}) from target
    r = [target(M), target(M-1), target(M-2)]
    j = M
    while j >= 4:
        # nu_{j-3} from recurrence at j: c^2 nu_j = P_j nu_{j-1} - Q_j nu_{j-2} + R_j nu_{j-3} + T_j D
        P, Q, R, T = coeffs_nu(c, j, par)
        newv = (c*c*r[0] - P*r[1] + Q*r[2] - T*F(D))/R if R != 0 else F(0)
        r = [r[1], r[2], newv]
        s = abs(r[2])
        if s != 0: r = [x/s for x in r]
        j -= 1
    # j=3: nu_0 from recurrence at j=3? we need nu_1, nu_2, nu_3: state r = (nu_3, nu_2, nu_1)
    # iterate once more: nu_0 = (c^2 nu_3 - P_3 nu_2 + Q_3 nu_1 - R_3 nu_{-1} - T_3 D)/R_3 with R_3 nu_{-1}=0? 
    # actually R_3 != 0; the recurrence at j=3 uses nu_0: c^2 nu_3 = P_3 nu_2 - Q_3 nu_1 + R_3 nu_0 + T_3 D
    P, Q, R, T = coeffs_nu(c, 3, par)
    nu0 = (c*c*r[0] - P*r[1] + Q*r[2] - T*F(D))/R
    return nu0, r

for par in ('e','o'):
    print(f"===== {par} (c=3) =====")
    for D in (1, 2, -1):
        nu0, r = backward_nu_target(F(3), par, D, 400)
        print(f"  D={D}: nu_0 = {float(nu0):.10e}  (normalized tail)")
    # D=0 -> h*: compare with known z0
    nu0, r = backward_nu_target(F(3), par, 0, 400)
    print(f"  D=0: nu_0 = {float(nu0):.10e}")
