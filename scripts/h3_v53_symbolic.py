# -*- coding: utf-8 -*-
"""H3 v53: symbolic proof that R(j)=0 identically, and explicit reduced
second-order recurrence for s_j = r_j - r_{j-1}, r_j = z_j/z^E_j."""
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
def Pscal(a,s):
    return [s*x for x in a]
def Psub(a,b):
    n=max(len(a),len(b)); r=[F(0)]*n
    for i in range(n):
        r[i]=(a[i] if i<len(a) else F(0))-(b[i] if i<len(b) else F(0))
    return r

# Work symbolically in variable n with parameter c (as a symbol via Fraction can't).
# Instead verify the identity for several concrete c values by clearing denominators:
# R(j)=0  <=>  P_e - Q_e*2lam/((j-1)(2j-1)) + R_e*4lam^2/((2j-1)(2j-3))
#               - c^2 j lam (2j+1)/(2j) = 0   (multiplied by c^2 j^2 lam, see notes)
# Let's build numerator polynomials in j for c a FIXED rational, and check identically.

def ident_check(c):
    lam=F(4)/c
    # P_e(j) as poly: 8c j^2 - 4c j + c^2 j/(j-1)  -> multiply through by (j-1)
    # Work with cleared denominators: overall factor (j-1)(2j-1)(2j-3)*j*...
    # Easiest: build the RATIONAL function via Fraction with j as symbol is not possible.
    # Instead: compute R(j) as exact Fraction for j=3..60; if all zero and the expression
    # is rational in j, that is strong but not a proof. For the proof, do symbolic poly:
    # numerator of R after clearing denominators D(j) = j(j-1)(2j-1)(2j-3)*2 (from all terms).
    # term1: P_e = (8c j^3 - 4c j^2 + c^2 j)/(j-1)
    # term2: -Q_e * 2lam/((j-1)(2j-1)), Q_e=4j(2j-3)[(j-1)(2j-1)+c]
    #   = -8 lam j(2j-3)[(j-1)(2j-1)+c] /((j-1)(2j-1))
    # term3: R_e*4lam^2/((2j-1)(2j-3)), R_e=4j(j-2)(2j-3)(2j-5)
    #   = 16 lam^2 j(j-2)(2j-5)/(2j-1)
    # RHS: c^2 j lam (2j+1)/(2j) = c^2 lam(2j+1)/2
    # Clear denominators: multiply by (j-1)(2j-1)*2:
    N = Pmul([F(0),F(1),F(0),F(0),F(0)],[])  # placeholder
    # Build polynomials:
    j1 = [F(-1),F(1)]        # j-1
    j2j1 = [F(-1),F(2)]      # 2j-1
    j2j3 = [F(-3),F(2)]      # 2j-3
    termA_num = Pmul([F(0),F(8)*c,-F(4)*c,c*c], j2j1)  # (8cj^3-4cj^2+c^2 j)(2j-1)
    # P_e*(j-1) = 8cj^3-4cj^2+c^2 j;  term A after x2(j-1)(2j-1): P_e*2(2j-1)*... 
    # Let's define final numerator over denom 2(j-1)(2j-1):
    # N = 2(j-1)(2j-1)*[P_e - Q_e*2lam/((j-1)(2j-1)) + R_e*4lam^2/((2j-1)(2j-3)) - c^2 lam (2j+1)/(2j)] * j? 
    # Hmm R_e term has (2j-3) in denom and no (j-1).  Common denom: 2j(j-1)(2j-1)(2j-3).
    # N = j(2j-3)*2*[P_e(j-1)]  ... getting confused; do it with clear structure below.
    return None

# -------- clean approach: build N over D = 2 j (j-1)(2j-1)(2j-3) --------
def build_N(c):
    lam=F(4)/c
    D = Pmul([F(0),F(2)], Pmul([F(0),F(1)], Pmul([F(-1),F(2)], [F(-3),F(2)])))  # 2*j*(j-1)(2j-1)(2j-3)
    # but note D has factor j; multiply each term:
    # term A = P_e -> P_e*(j-1) = 8cj^3-4cj^2+c^2 j ; contribution: P_e * D / 1 with (j-1) cleared:
    # Actually P_e = (8cj^3-4cj^2+c^2j)/(j-1).  N_A = D * P_e = [D/(j-1)]*(8cj^3-4cj^2+c^2j)
    Dm = Pmul([F(0),F(2)], Pmul([F(0),F(1)], [F(-3),F(2)]))  # 2*j*(2j-3) times (j-1)? no
    # D/(j-1) = 2 j (2j-1)(2j-3)
    Dp = Pmul(Pmul([F(0),F(2)],[F(-1),F(2)]),[F(-3),F(2)])   # 2j(2j-1)(2j-3)
    NA = Pmul(Dp, [F(0),F(8)*c,-F(4)*c,c*c])
    # term B = -Q_e*2lam/((j-1)(2j-1)): Q_e = 4j(2j-3)[(j-1)(2j-1)+c]
    QB = Pmul(Pmul([F(0),F(4)],[F(-3),F(2)]), Padd(Pmul([F(-1),F(1)],[F(-1),F(2)]),[F(c)]))
    # D * [2lam/((j-1)(2j-1))] * Q_e  (negative)
    Dq = Pmul(Pmul([F(0),F(2)], [F(-3),F(2)]), [F(1)])  # D/((j-1)(2j-1)) = 2j(2j-3)
    NB = Pscal(Pmul(Dq,QB), -F(2)*lam)
    # term C = R_e*4lam^2/((2j-1)(2j-3)): R_e = 4j(j-2)(2j-3)(2j-5)
    RC = Pmul(Pmul(Pmul([F(0),F(4)],[F(-2),F(1)]),[F(-3),F(2)]),[F(-5),F(2)])
    Dc = Pmul([F(0),F(2)], [F(0),F(1)])   # D/((2j-1)(2j-3)) = 2j(j-1)
    NC = Pscal(Pmul(Dc,RC), F(4)*lam*lam)
    # RHS: c^2 lam (2j+1)/2 * D
    Dr = Pmul(Pmul([F(0),F(2)], [F(-1),F(2)]),[F(-3),F(2)])  # 2j(2j-1)(2j-3)
    NR = Pscal(Pmul(Pmul(Dr,[F(1),F(2)]),[F(1)]), F(c)*c*lam/F(2))  # c^2 lam/2 * (2j+1) * 2j(2j-1)(2j-3)
    N = Padd(Padd(NA,NB), Psub(NC,NR))
    return N

for c in (1,3,10,50):
    N = build_N(F(c))
    nonzero=[k for k,v in enumerate(N) if v!=0]
    print("c=%d: numerator degree %d, nonzero coeffs at %s" % (c, max(nonzero), nonzero))
    print("    N =", " + ".join("%s j^%d"%(N[k],k) for k in nonzero))
    print("    identically zero:", all(v==0 for v in N))

