# -*- coding: utf-8 -*-
"""#13(i): check sum_k r_k/R^0_k = -1/10 (c-linear coefficient of log K(c))."""
import mpmath as mp
mp.mp.dps = 80

# R_k(c) = R^0_k + c*r_k + c^2*s_k + ... (from matched asymptotics, even)
# R^0_k = 1 - 3/k + 6/k^2 - 21/(2 k^3) + 69/(4 k^4) - 219/(8 k^5) + 681/(16 k^6) + ...
# r_k   = -1/k^3 + 33/(4 k^4) - 163/(4 k^5) + 2529/(16 k^6) + ...
def R0(k):
    return (1 - 3/mp.mpf(k) + 6/k**2 - mp.mpf(21)/(2*k**3) + mp.mpf(69)/(4*k**4)
            - mp.mpf(219)/(8*k**5) + mp.mpf(681)/(16*k**6))
def rk(k):
    return (-1/k**3 + mp.mpf(33)/(4*k**4) - mp.mpf(163)/(4*k**5) + mp.mpf(2529)/(16*k**6))

# log K(c) - log K(0) = sum_k log(R_k(c)/R^0_k) = c * sum_k r_k/R^0_k + O(c^2)
s = mp.mpf(0)
for k in range(1, 200000):
    s += rk(k)/R0(k)
print("sum r_k/R^0_k =", mp.nstr(s, 20), "  vs -0.1")
