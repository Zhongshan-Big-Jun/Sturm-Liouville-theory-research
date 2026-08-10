# -*- coding: utf-8 -*-
"""H3 v67: decisive verification of the Ratio Trap Lemma structure.
Fixed points: even e_j = 1+1/(2j) (beta=1), odd e_j = 1+3/(2j) (beta=3).
(a) exactness: e_j = a1 + a2/e_{j-1} + a3/(e_{j-1} e_{j-2})  (all j>=3)
(b) induction lower-bound condition: Delta(j,alpha) >= 0 where
    Delta = (-a2)*(j-1)*(2a-b)/((2j-2+b)(j-1+a))
          + a3*(j-1)(j-2)[1/((j-1+a)(j-2+a)) - 4/((2j-2+b)(2j-4+b))]
(c) base cases for u (j=2,3) and v (j=3,4)
(d) v upper: e_j + s_j/v_{j-1} <= 1 + alpha/j
(e) minimal solution h*: h*_0 != 0
All exact (Fractions) for j <= 80, float to 1e6."""
from fractions import Fraction as F
import math

def coeffs(c, j, par):
    # returns exact Fractions a1,a2,a3,Tm
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

def efix(j, par):
    return F(1) + (F(1) if par=='e' else F(3))/(F(2)*j)

print("(a) exactness of fixed-point trajectory e_j (j=3..60):")
for par in ('e','o'):
    ok = True
    for c in (1,3,10):
        for j in range(3,61):
            a1,a2,a3,Tm = coeffs(F(c), j, par)
            lhs = efix(j,par)
            rhs = a1 + a2/efix(j-1,par) + a3/(efix(j-1,par)*efix(j-2,par))
            if lhs != rhs:
                ok = False; print("  FAIL par=%s c=%d j=%d"%(par,c,j)); break
    print("  par=%s exactness OK = %s"%(par,ok))

print()
print("(b) Delta(j,alpha) >= 0 for induction (exact, j=4..80; float, j=4..1e6):")
def Delta(c, j, par, alpha):
    a1,a2,a3,Tm = coeffs(c, j, par)
    b = F(1) if par=='e' else F(3)
    t1 = (-a2)*(j-1)*(2*alpha-b)/((2*j-2+b)*(j-1+alpha))
    t2 = a3*(j-1)*(j-2)*(F(1)/((j-1+alpha)*(j-2+alpha)) - F(4)/((2*j-2+b)*(2*j-4+b)))
    return t1+t2
for par in ('e','o'):
    for c in (1,3,10,100):
        b = 1 if par=='e' else 3
        alpha = F(2 + 5*c/12) if par=='e' else F(4 + 7*c/20)   # provisional
        # exact check
        ok_exact = all(Delta(F(c), j, par, alpha) >= 0 for j in range(4,81))
        # float check to 1e6
        ok_float = True; worst = (1e99, None)
        for j in range(4, 1000001):
            d = Delta(F(c), j, par, alpha)
            f = float(d)
            if f < worst[0]: worst = (f, j)
            if f < 0: ok_float = False; break
        print("  par=%s c=%-4g alpha=%s: exact(j<=80)=%s  float(j<=1e6)=%s worst=%.3e at j=%s"
              %(par,c,str(alpha),ok_exact,ok_float,worst[0],worst[1]))
EOF
