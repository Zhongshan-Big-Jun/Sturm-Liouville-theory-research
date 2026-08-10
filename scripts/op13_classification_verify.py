# -*- coding: utf-8 -*-
"""#13(iii) verification: complete classification of rational-ratio product solutions.
1) combo family E^(tau)_j = (1 + j/(tau+1)) E^-_j satisfies the z-recurrence exactly.
2) any root-1 combo has rational ratios: e_j = (1-1/(2j))((2j+1)c1+c2)/((2j-1)c1+c2).
3) c3 != 0 impossible: f_j = h_j/E^-_j has f_j/f_{j-1} -> 0 (not rational)."""
from fractions import Fraction as F
import math

def a_f(parity, j, cF):
    if parity == 'e':
        P = F(8)*cF*j*j - F(4)*cF*j + cF*cF*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*cF*j*(2*j-3)
        R = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:
        P = F(8)*cF*j*j + F(4)*cF*j + cF*cF*F(j, j-1)
        Q = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*cF*j*(2*j-1)
        R = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    lam = F(4)/cF
    a1 = P/(cF*cF*j*j*lam)
    a2 = -Q/(cF*cF*j*j*(j-1)*(j-1)*lam*lam)
    a3 = R/(cF*cF*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)
    return a1, a2, a3

def Ep(zlist, parity):
    """E+ in z-scale (beta=1 even, beta=3 odd): E_j = prod (1+beta/(2k))."""
    b = 1 if parity=='e' else 3
    zlist[0] = F(1)
    for k in range(1, len(zlist)):
        zlist[k] = zlist[k-1]*(F(1)+F(b, 2*k))
def Em(zlist, parity):
    b = -1 if parity=='e' else 1
    zlist[0] = F(1)
    for k in range(1, len(zlist)):
        zlist[k] = zlist[k-1]*(F(1)+F(b, 2*k))

def check_combo_family(parity, cval, taus, N=40):
    cF = F(cval); lam = F(4)/cF
    Eplus = [None]*(N+1); Eminus = [None]*(N+1)
    Ep(Eplus, parity); Em(Eminus, parity)
    for tau in taus:
        E = [None]*(N+1)
        for j in range(N+1):
            E[j] = (F(1) + F(j)/(tau+1))*Eminus[j]
        ok = True
        for j in range(3, N+1):
            a1,a2,a3 = a_f(parity, j, cF)
            if E[j] != a1*E[j-1] + a2*E[j-2] + a3*E[j-3]:
                ok = False; break
        # also verify rational-ratio formula
        c1, c2 = F(1), F(tau+1)   # E = c1*Eplus + c2*Eminus  =>  c1*(tau+1)=1? check: E=(1+j/(tau+1))E- = (1/(tau+1))((tau+1)+j)E-
        # E = c1*Eplus + c2*Eminus with c1=1/(tau+1), c2=1: check Eplus=(2j+1)Eminus (even)
        ratio_ok = True
        for j in range(2, N+1):
            if parity=='e':
                lhs = E[j]/E[j-1]
                rhs = (F(1)-F(1,2*j))*((F(2*j+1)*c1 + c2)/((F(2*j-1))*c1 + c2))
            else:
                # odd: Eplus = ((2j+3)/3) Eminus
                lhs = E[j]/E[j-1]
                rhs = (F(1)+F(1,2*j))*((F(2*j+3,3)*c1 + c2)/(F(2*j+1,3)*c1 + c2))
            if lhs != rhs:
                ratio_ok = False; break
        print(f"  parity={parity} c={cval} tau={tau}: recurrence ok={ok}, rational-ratio formula ok={ratio_ok}")

print("=== combo family verification ===")
for parity in ('e','o'):
    for cv in (1, 3, 10):
        check_combo_family(parity, cv, (0, 2, F(5,2), -F(1,2)), N=30)

print("=== minimal solution f_j/h ratio -> 0 (mpmath) ===")
import mpmath as mp
mp.mp.dps = 120
for cval in (1, 3):
    N = 300
    c_ = mp.mpf(cval); lam = mp.mpf(4)/c_
    # backward iteration in mu-scale: c^2 mu_j = P_j mu_{j-1} - Q_j mu_{j-2} + R_j mu_{j-3}
    mu = [mp.mpf(0)]*(N+4)
    mu[N+3] = mp.mpf(0); mu[N+2] = mp.mpf(0); mu[N+1] = mp.mpf(1)
    def P(j): return mp.mpf(8)*c_*j*j - mp.mpf(4)*c_*j + c_*c_*mp.mpf(j)/(j-1)
    def Q(j):
        return mp.mpf(4)*j*(j-1)*(2*j-1)*(2*j-3) + mp.mpf(4)*c_*j*(2*j-3)
    def R(j): return mp.mpf(4)*j*(j-2)*(2*j-3)*(2*j-5)
    for j in range(N+1, 2, -1):
        mu[j-3] = (c_*c_*mu[j] - P(j)*mu[j-1] + Q(j)*mu[j-2])/R(j)
    # z-scale: z_j = mu_j (c/4)^j/(j!)^2  (note mu-scale = h*)
    z = [mu[j]*(c_/4)**j/mp.factorial(j)**2 for j in range(N+1)]
    # Eminus z-scale (even): (2j-1)!!/(2^j j!)
    E = [mp.mpf(1)]
    for j in range(1, N+1):
        E.append(E[-1]*(2*j-1)/(2*j))
    ratios = [z[j]/E[j]/(z[j-1]/E[j-1]) for j in range(10, 30)]
    print(f"  c={cval}: f_j/f_{'{'}j-1{'}'} at j=10..30: {[mp.nstr(r,4) for r in ratios[:6]]} ... ->0? {all(abs(r)<mp.mpf('1e-40') for r in ratios)}")
