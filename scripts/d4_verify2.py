# -*- coding: utf-8 -*-
"""Direction 4: verify (i) corrected reduction-of-order s-recurrence;
(ii) minimal solution asymptotics h*_j ~ K (c/4)^j/(j!)^2."""
from fractions import Fraction as F
import math
from mpmath import mp, mpf

c = F(3); lam = F(4)/c

def a1(j,par):
    if par=='e': P=F(8)*c*j*j-F(4)*c*j+c*c*F(j,j-1)
    else:        P=F(8)*c*j*j+F(4)*c*j+c*c*F(j,j-1)
    return P/(c*c*j*j*lam)
def a2(j,par):
    if par=='e': Q=F(4)*j*(j-1)*(2*j-1)*(2*j-3)+F(4)*c*j*(2*j-3)
    else:        Q=F(4)*j*(j-1)*(2*j-1)*(2*j+1)+F(4)*c*j*(2*j-1)
    return -Q/(c*c*j*j*(j-1)*(j-1)*lam*lam)
def a3(j,par):
    if par=='e': R=F(4)*j*(j-2)*(2*j-3)*(2*j-5)
    else:        R=F(4)*j*(j-2)*(2*j-1)*(2*j-3)
    return R/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)

print("=== corrected reduction of order: s_j = A_j s_{j-1} + B_j s_{j-2} ===")
print("A_j = -(a2 E_{j-2} + a3 E_{j-3})/E_j, B_j = -a3 E_{j-3}/E_j")
for par in ('e','o'):
    beta = 1 if par=='e' else 3
    E=[F(1)]*(120)
    for j in range(1,120): E[j]=E[j-1]*(F(1)+F(beta)/(F(2)*j))
    # random solution z (initial data 1,2,3) + the E^- solution
    for label, zinit in (("random(1,2,3)", lambda k: F(k+1)),):
        z=[zinit(k) for k in range(120)]
        for j in range(3,120):
            z[j]=a1(j,par)*z[j-1]+a2(j,par)*z[j-2]+a3(j,par)*z[j-3]
        r=[z[j]/E[j] for j in range(120)]
        s=[None]+[r[j]-r[j-1] for j in range(1,120)]
        ok=True
        for j in range(3,120):
            Aj=-(a2(j,par)*E[j-2]+a3(j,par)*E[j-3])/E[j]
            Bj=-a3(j,par)*E[j-3]/E[j]
            if s[j]!=Aj*s[j-1]+Bj*s[j-2]:
                ok=False; print(f"  FAIL par={par} {label} j={j}"); break
        print(f"  par={par} {label}: corrected s-recurrence = {ok}")
    # E^- / E^+ gives closed-form particular s
    beta2 = -1 if par=='e' else 1
    E2=[F(1)]*(120)
    for j in range(1,120): E2[j]=E2[j-1]*(F(1)+F(beta2)/(F(2)*j))
    r=[E2[j]/E[j] for j in range(120)]
    s=[None]+[r[j]-r[j-1] for j in range(1,120)]
    ok=True
    for j in range(3,120):
        Aj=-(a2(j,par)*E[j-2]+a3(j,par)*E[j-3])/E[j]
        Bj=-a3(j,par)*E[j-3]/E[j]
        if s[j]!=Aj*s[j-1]+Bj*s[j-2]:
            ok=False; break
    print(f"  par={par} E^-/E^+ solution: corrected s-recurrence = {ok}; s_j = {-6/((2*j+1)*(2*j+3)) if False else '3/(2j+3)-3/(2j+1)'} (closed form)")

print()
print("=== minimal solution asymptotics ===")
mp.dps = 100
def minimal_mp(parity, cval, N):
    cf = mpf(cval); lam = mpf(4)/cf
    def a1(j):
        jj = mpf(j)
        if parity=='e': P = 8*cf*jj*jj - 4*cf*jj + cf*cf*jj/(jj-1)
        else:           P = 8*cf*jj*jj + 4*cf*jj + cf*cf*jj/(jj-1)
        return P/(cf*cf*jj*jj*lam)
    def a2(j):
        jj = mpf(j)
        if parity=='e': Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj-3) + 4*cf*jj*(2*jj-3)
        else:           Q = 4*jj*(jj-1)*(2*jj-1)*(2*jj+1) + 4*cf*jj*(2*jj-1)
        return -Q/(cf*cf*jj*jj*(jj-1)*(jj-1)*lam*lam)
    def a3(j):
        jj = mpf(j)
        if parity=='e': R = 4*jj*(jj-2)*(2*jj-3)*(2*jj-5)
        else:           R = 4*jj*(jj-2)*(2*jj-1)*(2*jj-3)
        return R/(cf*cf*jj*jj*(jj-1)*(jj-1)*(jj-2)*(jj-2)*lam**3)
    z = [mpf(0)]*(N+3)
    z[N] = mpf(1)
    for j in range(N-1, -1, -1):
        z[j] = (z[j+3] - a1(j+3)*z[j+2] - a2(j+3)*z[j+1])/a3(j+3)
    return [z[j]/z[0] for j in range(N+1)]

for par in ('e','o'):
    for N in (100, 200, 400):
        h = minimal_mp(par, 3, N)
        # check convergence at j = 20 across N
        print(f"  par={par} N={N}: h*_20 = {mp.nstr(h[20],12)}")
    h = minimal_mp(par, 3, 400)
    # j^2 * ratio
    print(f"  par={par}: j^2 * ratio_j for j=100,200,300: {mp.nstr(100**2*h[101]/h[100],8)}, {mp.nstr(200**2*h[201]/h[200],8)}, {mp.nstr(300**2*h[301]/h[300],8)}")
    # compare with (c/4)^j/(j!)^2: compute h*_j * (j!)^2 * (4/c)^j
    for j in (50, 100, 200, 300):
        fj = math.factorial(j)
        scaled = h[j] * mpf(fj)**2 * mpf(4.0/3.0)**j
        print(f"    j={j}: h*_j*(j!)^2*(4/c)^j = {mp.nstr(scaled,10)}")
