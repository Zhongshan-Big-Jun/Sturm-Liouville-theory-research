# -*- coding: utf-8 -*-
"""H3 v54: exact reduced second-order recurrence for s_j = r_j - r_{j-1},
r_j = z_j/z^E_j.  s_j = A_j s_{j-1} + B_j s_{j-2}.
Exact rational coefficients; look for structure (factorization, simple closed forms)."""
from fractions import Fraction as F

c=F(3)
lam=F(4)/c

def a2(j):
    Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j):
    R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    if j==2: return F(0)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

def A(j):
    b2 = F(4)*j*(j-1)/((2*j+1)*(2*j-1))
    b3 = F(8)*j*(j-1)*(j-2)/((2*j+1)*(2*j-1)*(2*j-3))
    return -(a2(j)*b2 + a3(j)*b3)
def B(j):
    b3 = F(8)*j*(j-1)*(j-2)/((2*j+1)*(2*j-1)*(2*j-3))
    return -a3(j)*b3

for j in range(4,9):
    print("j=%d: A=%s  B=%s" % (j, A(j), B(j)))

# Asymptotics of A_j, B_j
print()
print("asymptotics:")
for j in (10,100,1000):
    print("  j=%5d: A=%.10f (1-1/j=%.10f)  B=%.3e" % (j, float(A(j)), 1-1.0/j, float(B(j))))
print()
# Try to express A, B as rational functions and check for hypergeometric-type:
# does B_j * j^2 -> -c/4? does A_j - (1-1/j) -> ?
for j in (1000,10000):
    print("  j=%6d: B*j^2=% .8f   (A-(1-1/j))*j^2=% .8f" % (j, float(B(j)*j*j), float((A(j)-(1-1.0/j))*j*j)))
