# -*- coding: utf-8 -*-
"""scan_pert_box.py - scan |s_k1|, |s_k2| and the O(eps^3) remainder coefficient
over the main box a in [a0-0.03,a0+0.03], b in [a0,0.99], eps in [0,eps0].
[EVIDENCE] - informs the eps0 choice and root-enclosure constants."""
import numpy as np

pi = np.pi
a0 = np.arccos(0.25)/pi
a0n = float(np.arccos(0.25)/pi)

def s11(a, b):
    return pi*a/2 - pi*b/2 - np.sin(pi*(a-b))*np.cos(pi*(a+b))/2
def s12(a, b):
    c2a = np.cos(2*pi*a); c2b = np.cos(2*pi*b)
    s2a = np.sin(2*pi*a); s2b = np.sin(2*pi*b)
    s4a = np.sin(4*pi*a); s4b = np.sin(4*pi*b)
    s22ab = np.sin(2*pi*(a-b)); s2ab = np.sin(pi*(2*a-2*b)); s2ap = np.sin(pi*(2*a+2*b))
    return (-pi*a**2*c2a/4 + pi*a**2/4 + pi*a*b*c2a/4 + pi*a*b*c2b/4 - pi*a*b/2
            - a*s2a/8 + a*s4a/16 + a*s2b/8 + a*s22ab/16 - a*s2ap/16 - pi*a*c2b/4 - pi*a/8
            - pi*b**2*c2b/4 + pi*b**2/4 + b*s2a/8 - b*s2b/8 + b*s4b/16 - b*s22ab/16 - b*s2ap/16
            + pi*b*c2b/4 + pi*b/8 + s2a/8 - s4a/32 - s2b/8 - s4b/32 + s22ab/16 + s2ap/16)
def s21(a, b):
    return pi*a - pi*b - np.sin(4*pi*a)/4 + np.sin(4*pi*b)/4

# scan grid
Na, Nb = 401, 4001
aa = np.linspace(a0-0.03, a0+0.03, Na)
bb = np.linspace(a0, 0.99, Nb)
A, B = np.meshgrid(aa, bb, indexing="ij")
S11 = s11(A, B); S12 = s12(A, B); S21 = s21(A, B)
print("box: a in [%.4f, %.4f], b in [%.4f, 0.99]" % (a0-0.03, a0+0.03, a0))
print("max|s11| = %.6f   max|s12| = %.6f   max|s21| = %.6f" %
      (np.max(np.abs(S11)), np.max(np.abs(S12)), np.max(np.abs(S21))))
# where does s21 max occur
i, j = np.unravel_index(np.argmax(np.abs(S21)), S21.shape)
print("  max|s21| at a=%.5f b=%.5f -> s21=%.4f" % (aa[i], bb[j], S21[i,j]))
# s11/s12 at a0 for reference
for b in (a0, 0.5, 0.7, 0.9, 0.99):
    print("  a=a0 b=%.3f: s11=%.5f s12=%.4f s21=%.5f" % (b, s11(a0n, b), s12(a0n, b), s21(a0n, b)))

# remainder coefficient: deviation/eps^3 at grid points, via the exact secular solver (numpy)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fast_lib import roots2_fast
for eps0 in (0.05, 0.1, 0.2):
    amax = 0.0
    for ai in range(0, Na, 20):
        for bi in range(0, Nb, 40):
            for e in (eps0, eps0/2):
                a_ = aa[ai]; b_ = bb[bi]
                s1, s2 = roots2_fast(a_, b_, 1+e)
                dev1 = abs(s1 - (pi + s11(a_, b_)*e + s12(a_, b_)*e**2))/e**3
                dev2 = abs(s2 - (2*pi + s21(a_, b_)*e))/e**3   # s22 skipped (big); use order-1 for now
                amax = max(amax, dev1, dev2)
    print("eps0=%.2f: max |dev|/eps^3 over coarse grid = %.4f  ->  enclosure halfwidth C*eps^3 at eps0: %.4f"
          % (eps0, amax, amax*eps0**3))
