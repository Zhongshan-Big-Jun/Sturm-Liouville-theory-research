# -*- coding: utf-8 -*-
"""R-209 M3: final leading-observable arithmetic (STRICT formulas, EVIDENCE
seed values).  No heavy symbolic expansion; just the exact relations."""
import sympy as sp
from sympy import pi, sqrt

# EVIDENCE seed (handoff free-exponent fit, scripts/_gapn2_largeR_fit.py /
# _gapn2_largeR_sigma_fit.py).  These are NOT proven; they are the fit limits.
K0 = 3.4553
B0 = 0.2898
C0 = 1.4741

# STRICT identity A0*K0 = 2 (from E1_0=E2_0=E6_3=0; this session).
A0 = 2 / K0
print('STRICT: A0 = 2/K0 = %.8f  (fit a0 = 0.5788; match = %s)'
      % (A0, 'YES' if abs(A0 - 0.5788) < 5e-4 else 'NO'))

# leading observables (STRICT formulas):
#  Dk = k3 - k2 = C u^5  =>  Dk/u^5 = c(u) -> c0 ;  Dk/u^7 = c(u)/u^2 -> c0/u^2
#  D*R = (k3^2 - k2^2)*R = (2 K C u^6 + C^2 u^10)/u^6 = 2 K C + C^2 u^4 -> 2 K0 C0
DR = 2 * K0 * C0
print('STRICT formula: D*R -> 2*K0*C0 = %.8f  (data last row D*R=10.8806, decreasing)' % DR)
print('STRICT formula: Dk/u^7 -> c0/u^2 = %.8f/u^2 ; Dk/u^5 = c(u) -> c0 = %.8f' % (C0, C0))

# consistency candidate C_check = 1 + b0*K0/2 + 3*pi/(2*K0) - K0^2/12
Cchk = 1 + B0 * K0 / 2 + 3 * pi / (2 * K0) - K0**2 / 12
print('consistency candidate (even-only seed, not expected to vanish):')
print('  1 + b0*K0/2 + 3*pi/(2*K0) - K0^2/12 = %.8f  (NOT zero -> needs corrected odd branch)'
      % Cchk)

# E5_5 hard constant: cleared numerator constant K0^3/2 (STRICT).
print('STRICT: E5_5 (K-cleared) carries constant K0^3/2 = %.6f  (hard, forces odd components)'
      % (K0**3 / 2))

# sector determinant scalings (EVIDENCE only, from addendum e Section 5b):
print('EVIDENCE (addendum e 5b): det Kp_odd ~ R^{-7/2}, det Ko ~ R^{-9/2}')
