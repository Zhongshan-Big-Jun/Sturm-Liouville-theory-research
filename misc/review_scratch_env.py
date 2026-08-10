# -*- coding: utf-8 -*-
from fractions import Fraction as Fr
# verify sqrt41 interval 640312423/1e8 < sqrt41 < 640312424/1e8
print("sqrt41 bounds ok:", Fr(640312423,10**8)**2 < 41 < Fr(640312424,10**8)**2)
# pi interval (Machin) 314159265/1e8 < pi < 314159266/1e8
import math
print("pi bounds ok:", Fr(314159265,10**8) < Fr(math.pi).limit_denominator(10**12) < Fr(314159266,10**8))
pi_lo = Fr(314159265,10**8); pi_hi = Fr(314159266,10**8)
s41_hi = Fr(640312424,10**8)
# B(20) < -232.723  <=> (4pi^2+14)sqrt41 < 183.395*pi - 233.723
LHS_ub = (4*pi_hi**2 + 14)*s41_hi
RHS_lb = Fr(183395,1000)*pi_lo - Fr(233723,1000)
print("LHS_ub =", LHS_ub, " RHS_lb =", RHS_lb, " LHS_ub < RHS_lb:", LHS_ub < RHS_lb)
print("margin =", float(RHS_lb - LHS_ub))
