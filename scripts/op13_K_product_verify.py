# -*- coding: utf-8 -*-
"""#13(i): verify K(c) = lim_j j^3 prod R_k(c) with matched coefficients, vs backward iteration."""
import mpmath as mp
mp.mp.dps = 100

def Rk(c_, k, parity='e'):
    """R_k(c) from matched asymptotics (through 1/k^6)."""
    c = c_
    if parity == 'e':
        C0 = 6; D = -(c + mp.mpf(21)/2); E = mp.mpf(33)*c/4 + mp.mpf(69)/4
        F = -c**2/4 - mp.mpf(163)*c/4 - mp.mpf(219)/8
        G = mp.mpf(85)*c**2/16 + mp.mpf(2529)*c/16 + mp.mpf(681)/16
    else:
        C0 = 8; D = -(c + mp.mpf(41)/2); E = mp.mpf(39)*c/4 + mp.mpf(207)/4
        F = -c**2/4 - mp.mpf(241)*c/4 - mp.mpf(1039)/8
        G = mp.mpf(95)*c**2/16 + mp.mpf(4843)*c/16 + mp.mpf(5203)/16
    return (1 - 3/mp.mpf(k) + C0/k**2 + D/k**3 + E/k**4 + F/k**5 + G/k**6)

def K_product(c_, J=2000, parity='e'):
    c = mp.mpf(c_)
    # K(c) = lim_j j^3 prod_{k=1}^j R_k(c); regularized by explicit j^3
    # compute prod R_k and multiply by j^3 with extrapolation in 1/j
    lp = mp.mpf(0)
    Ks = []
    for k in range(1, J+1):
        lp += mp.log(Rk(c, k, parity))
        Ks.append((k, mp.e**(lp) * k**3))
    # extrapolate K_j = K + a/j + b/j^2 using last 3
    n = J
    M = mp.matrix([[1, mp.mpf(1)/n, mp.mpf(1)/n**2],
                   [1, mp.mpf(1)/(n-1), mp.mpf(1)/(n-1)**2],
                   [1, mp.mpf(1)/(n-2), mp.mpf(1)/(n-2)**2]])
    bv = mp.matrix([Ks[n-1][1], Ks[n-2][1], Ks[n-3][1]])
    sol = mp.lu_solve(M, bv)
    return sol[0]

# reference K from backward iteration (accurate earlier fits)
Kref = {0.25: mp.mpf('0.73154726835733880385'), 0.5: mp.mpf('0.71367319815073017723'),
        1: mp.mpf('0.67957045711382317795'), 3: mp.mpf('0.5622227356633425386'),
        10: mp.mpf('0.30846328308935785349')}
for cv in Kref:
    Kp = K_product(cv, J=4000)
    print(f"c={cv}: product K={mp.nstr(Kp,15)}  backward K={mp.nstr(Kref[cv],15)}  rel={mp.nstr(abs(Kp/Kref[cv]-1),4)}")
