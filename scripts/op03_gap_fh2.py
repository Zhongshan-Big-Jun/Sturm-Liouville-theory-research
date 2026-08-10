# -*- coding: utf-8 -*-
"""Test Feynman-Hellmann: rho = 1 + c*chi_(0.4,0.5), d lambda_1/dc = -lambda_1 * int u1^2."""
import numpy as np
from op03_gap_precise import lams_precise, eigfuns_precise

# normalized eigenfunction at rho=1
blocks0 = [(1.0, 1.0)]
s = lams_precise(blocks0, 2)
u1 = eigfuns_precise(blocks0, s[:1], np.array([0.45]))
# u1^2 at 0.45 for constant density should be 2 sin^2(pi*0.45) = 2*0.9877=1.975
print("u1(0.45)^2 =", u1[0,0]**2, " expect", 2*np.sin(np.pi*0.45)**2)

# int_0.4^0.5 u1^2 dx = 2*(0.1/2 - sin(2pi*0.4)/(4pi) ... )
a, b = 0.4, 0.5
I = 2*( (b-a)/2 - (np.sin(2*np.pi*b)-np.sin(2*np.pi*a))/(4*np.pi) )
print("int_0.4^0.5 u1^2 =", I)
# numerical derivative
for c in (0.001, 0.01):
    blocks = [(a, 1.0+c), (b-a, 1.0), (1-b, 1.0)]
    s2 = lams_precise(blocks, 2)
    # dlambda/dc ~ (lambda(c)-lambda(0))/c
    num = (s2[0]**2 - s[0]**2)/c
    fh = -s[0]**2 * I
    print(f"c={c}: num dL1/dc={num:.6f}  FH={fh:.6f}")
