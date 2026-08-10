# -*- coding: utf-8 -*-
"""s33_r1base.py - exact R=1 base facts for the fp-component limit curve.
Outputs s33_r1base.json.  Numerics only."""
import numpy as np, json, os
pi = np.pi
HERE = os.path.dirname(os.path.abspath(__file__))
a0 = float(np.arccos(0.25)/pi)
b0 = 1 - a0
# curve: sin(2 pi b) = -sin(pi a)/2 ; slope db/da = -cos(pi a)/(4 cos(2 pi b))
sa = np.sin(pi*a0); ca = np.cos(pi*a0)
s2b = -sa/2
c2b = np.sqrt(1 - s2b**2) * np.sign(-1)  # b0 = 1-a0 in (1/2, 3/4): 2 pi b in (pi, 3pi/2): cos < 0
c2b = -np.sqrt(1 - s2b**2)
slope = -ca/(4*c2b)
out = dict(a0=a0, b0=b0, sin_pi_a0=float(sa), cos_pi_a0=float(ca),
           sin_2pi_b0=float(s2b), cos_2pi_b0=float(c2b), slope_db_da=float(slope),
           slope_as_fraction="1/14" if abs(slope - 1/14) < 1e-9 else str(slope))
with open(os.path.join(HERE, "s33_r1base.json"), "w") as f:
    json.dump(out, f, indent=1)
print(out)
