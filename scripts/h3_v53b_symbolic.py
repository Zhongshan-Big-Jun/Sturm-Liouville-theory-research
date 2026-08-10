# -*- coding: utf-8 -*-
"""H3 v53b: correct symbolic proof that R(j)=0 identically.
Cleared identity: P_e - Q_e*2lam/((j-1)(2j-1)) + R_e*4/(lam^2 (j-1)(j-2)(2j-1)(2j-3))
                  - c^2 j lam (2j+1)/2 = 0
with P_e=(8cj^3-4cj^2+c^2 j)/(j-1), Q_e=4j(2j-3)[(j-1)(2j-1)+c],
R_e=4j(j-2)(2j-3)(2j-5).  Common denom: 2(j-1)(j-2)(2j-1)(2j-3)."""
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
    # P_e = (8c j^3 - 4c j^2 + c^2 j)/(j-1); N_A = P_e * denom/(j-1)
    denomA = Pmul([F(0),F(2)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)])))  # 2(j-2)(2j-1)(2j-3)
    NA = Pmul(denomA, [F(0),F(4)*c+c*c,-F(12)*c,F(8)*c])
    # term2: -Q_e*2lam/((j-1)(2j-1)) ; Q_e = 4j(2j-3)[(j-1)(2j-1)+c]
    Qe = Pmul(Pmul([F(0),F(4)],[F(-3),F(2)]), Padd(Pmul([F(-1),F(1)],[F(-1),F(2)]),[F(c)]))
    denomB = Pmul([F(2)], Pmul([F(-2),F(1)],[F(-3),F(2)]))   # 2(j-2)(2j-3)
    NB = Pscal(Pmul(denomB,Qe), -F(2)/lam)
    # term3: R_e*4/(lam^2 (j-1)(j-2)(2j-1)(2j-3)) ; R_e = 4j(j-2)(2j-3)(2j-5)
    Re = Pmul(Pmul(Pmul([F(0),F(4)],[F(-2),F(1)]),[F(-3),F(2)]),[F(-5),F(2)])
    denomC = [F(2)]   # 2(j-1)
    NC = Pscal(Pmul(denomC,Re), F(4)/(lam*lam))
    # RHS: c^2 j lam (2j+1)/2 ; denom = 2(j-1)(j-2)(2j-1)(2j-3)
    denomR = Pmul([F(0),F(2)], Pmul([F(-1),F(1)], Pmul([F(-2),F(1)], Pmul([F(-1),F(2)],[F(-3),F(2)]))))
    NR = Pscal(Pmul(Pmul(denomR, [F(1),F(2)]), [F(0),F(1)]), F(c)*c*lam/F(2))
    # N = NA + NB + NC - NR
    N = Psub(Padd(Padd(NA,NB),NC),NR)
    return N

for c in (1,3,10,50):
    N = build_N(F(c))
    nz=[k for k,v in enumerate(N) if v!=0]
    print("c=%d: identically zero: %s   (deg %s)" % (c, all(v==0 for v in N), max(nz) if nz else -1))




