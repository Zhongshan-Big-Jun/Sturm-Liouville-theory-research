# -*- coding: utf-8 -*-
"""H3 v53c: symbolic proof that the explicit solution identity holds.
R(j) = a1 + a2/(1+s_{j-1}) + a3/((1+s_{j-1})(1+s_{j-2})) - (1+s_j) = 0 for all j>=3.
Common denominator D = 2(j-1)(j-2)(2j-1)(2j-3)."""
from fractions import Fraction as F

def Pmul(a,b):
    r=[F(0)]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            r[i+j]+=ai*bj
    return r
def Padd(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0))
    return r
def Psub(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))-(b[i] if i<len(b) else F(0))
    return r
def Pscal(a,s):
    return [s*x for x in a]

def build_N(c):
    lam=F(4)/c
    # D = 2(j-1)(j-2)(2j-1)(2j-3)
    D = Pmul([F(2)], Pmul([F(-1),F(1)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)]))))
    # NA: P_e * D/(j-1); P_e = (8cj^3-12cj^2+(4c+c^2)j)/(j-1)
    NA = Pmul(Pmul([F(2)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)]))),
              [F(0),F(4)*c+c*c,-F(12)*c,F(8)*c])
    # NB: -2 Q_e/((j-1)(2j-1) lam) * D ; Q_e=4j(2j-3)[(j-1)(2j-1)+c]
    Qe = Pmul(Pmul([F(0),F(4)],[F(-3),F(2)]), Padd(Pmul([F(-1),F(1)],[F(-1),F(2)]),[F(c)]))
    NB = Pscal(Pmul(Pmul([F(2)], Pmul([F(-2),F(1)],[F(-3),F(2)])), Qe), -F(2)/lam)
    # NC: 4 R_e/(lam^2 (j-1)(j-2)(2j-1)(2j-3)) * D ; R_e=4j(j-2)(2j-3)(2j-5)
    Re = Pmul(Pmul(Pmul([F(0),F(4)],[F(-2),F(1)]),[F(-3),F(2)]),[F(-5),F(2)])
    NC = Pscal(Pmul([F(2)], Re), F(4)/(lam*lam))
    # NR: c^2 j lam (2j+1)/2 * D
    NR = Pscal(Pmul(Pmul(D,[F(1),F(2)]),[F(0),F(1)]), F(c)*c*lam/F(2))
    return Psub(Padd(Padd(NA,NB),NC),NR)

for c in (1,3,10,50,100):
    N = build_N(F(c))
    nz=[k for k,v in enumerate(N) if v!=0]
    print("c=%d: identically zero: %s" % (c, all(v==0 for v in N)))
    if nz:
        print("   deg", max(nz))
