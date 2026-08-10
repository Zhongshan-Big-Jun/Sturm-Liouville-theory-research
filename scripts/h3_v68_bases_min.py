# -*- coding: utf-8 -*-
"""H3 v68: Ratio Trap Lemma - base cases, v upper bound, minimal solution h*."""
from fractions import Fraction as F
import math

def coeffsF(c, j, par):
    lam = F(4)/c
    if par=='e':
        Pm = F(8)*c*j*j - F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j-3) + F(4)*c*j*(2*j-3)
        Rm = F(4)*j*(j-2)*(2*j-3)*(2*j-5)
        Tm = F(4)*j*(4*j-5)
    else:
        Pm = F(8)*c*j*j + F(4)*c*j + c*c*F(j, j-1)
        Qm = F(4)*j*(j-1)*(2*j-1)*(2*j+1) + F(4)*c*j*(2*j-1)
        Rm = F(4)*j*(j-2)*(2*j-1)*(2*j-3)
        Tm = F(4)*j*(4*j-3)
    a1 = Pm/(c*c*j*j*lam)
    a2 = -Qm/(c*c*j*j*(j-1)*(j-1)*lam*lam)
    a3 = (Rm/(c*c*j*j*(j-1)*(j-1)*(j-2)*(j-2)*lam**3)) if j>=3 else F(0)
    return a1,a2,a3,Tm

def efixF(j, par):
    return F(1) + (F(1) if par=='e' else F(3))/(F(2)*j)

def solve_zF(c, par, N, z1, D):
    z=[F(0)]*(N+1); z[1]=F(z1)
    for j in range(2,N+1):
        a1,a2,a3,Tm=coeffsF(c,j,par)
        src=F(0)
        if D!=0:
            src = Tm*F(D)/(c*c*F(math.factorial(j))**2*(F(4)/c)**j)
        z[j]=a1*z[j-1]+a2*z[j-2]+(a3*z[j-3] if j>=3 else F(0))+src
    return z

print("(c) base cases: u ratios at j=2,3 and v ratios at j=3,4 within [e_j, 1+alpha/j]:")
for par in ('e','o'):
    for c in (1,3,10,100):
        alpha = F(2) + F(5)*c/F(12) if par=='e' else F(4) + F(7)*c/F(20)
        u = solve_zF(F(c), par, 6, 1, 0)
        v = solve_zF(F(c), par, 6, 0, 1)
        ok=True; detail=[]
        # u: rho_2 = u2/u1, rho_3 = u3/u2
        for j in (2,3):
            rho = u[j]/u[j-1]
            lo, hi = efixF(j,par), F(1)+alpha/F(j)
            detail.append((j,str(rho),rho>=lo and rho<=hi))
            if not (rho>=lo and rho<=hi): ok=False
        # v: sigma_3 = v3/v2, sigma_4 = v4/v3
        for j in (3,4):
            sig = v[j]/v[j-1]
            lo, hi = efixF(j,par), F(1)+alpha/F(j)
            detail.append((j,str(sig),sig>=lo and sig<=hi))
            if not (sig>=lo and sig<=hi): ok=False
        print("  par=%s c=%-4g alpha=%s: %s  %s"%(par,c,str(alpha),ok,
              " ".join("j%d in-range:%s"%(j,inn) for (j,val,inn) in detail)))

print()
print("(d) v upper bound: e_j + s_j/v_{j-1} <= 1 + alpha/j  (needs v_{j-1} >= v_2):")
for par in ('e','o'):
    for c in (1,3,10,100):
        alpha = F(2) + F(5)*c/F(12) if par=='e' else F(4) + F(7)*c/F(20)
        lam = F(4)/F(c)
        ok=True; bad=None
        for j in range(4,61):
            a1,a2,a3,Tm=coeffsF(F(c),j,par)
            sj = Tm/(F(c)*F(c)*F(math.factorial(j))**2*lam**j)
            v2 = F(3,8) if par=='e' else F(5,8)
            lhs = efixF(j,par) + sj/v2
            rhs = F(1)+alpha/F(j)
            if lhs > rhs:
                ok=False; bad=(j,str(lhs),str(rhs)); break
        print("  par=%s c=%-4g: ok=%s %s"%(par,c,ok,"" if ok else "FAIL at %s"%str(bad)))

print()
print("(e) minimal solution h* via backward iteration (ratio to h*_0), c=3:")
def backward(c, par, M):
    # returns (h0,h1,h2) with h0=1 normalization, exact fractions for small M
    r = [F(1), F(0), F(0)]
    for j in range(M, 3, -1):
        a1,a2,a3,Tm = coeffsF(c, j, par)
        newv = (r[0] - a1*r[1] - a2*r[2])/a3
        s = max(abs(newv), 1)
        r = [r[1]/s, r[2]/s, newv/s]
    return r
for par in ('e','o'):
    for M in (200, 800, 2000):
        r = backward(F(3), par, M)
        # normalize to r0=1
        print("  par=%s M=%-4d: h1/h0=%.12f h2/h0=%.12f"%(par,M,float(r[1]/r[0]),float(r[2]/r[0])))
EOF
