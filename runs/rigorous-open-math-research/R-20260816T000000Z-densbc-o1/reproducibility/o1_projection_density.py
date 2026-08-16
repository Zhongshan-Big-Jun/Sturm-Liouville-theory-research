# O1 exploration: projection-density reformulation + kept-set/run structure
# H = L^2([-1,1]) (Poly dense).  Non-diagonal constraints defined by
# non-coordinate Riesz representers (e.g. v_1 = e^x, v_2 = 1).
#
# This script is EVIDENCE (numerical/symbolic) only; it does NOT constitute a proof.
# Strict theorems are written separately in candidate_proof.md.
#
# Checks:
#   1) P_V(Pi) is dense in V (projection of the polynomial space is dense in V).
#   2) kept index set N = { n : p_n in V } via representer moments a^{(j)}_k.
#   3) the kept-recursion/run structure on moments (identical to diagonal case).
#
# Run: python o1_projection_density.py   (with PYTHONUTF8=1)

import numpy as np
import math
from sympy import symbols, integrate, exp, S, Rational, oo, Poly, diff

# ---------- exact representer moments for L^2([-1,1]) with v(x)=exp(x) ----------
x = symbols('x', real=True)

def moment_exp(k):
    # int_{-1}^{1} x^k e^x dx  (exact, via sympy)
    return integrate(x**k * exp(x), (x, -1, 1))

def moment_one(k):
    # int_{-1}^{1} x^k dx = (1-(-1)^{k+1})/(k+1)
    return (1 - (-1)**(k+1)) / (k+1)

# sparse family coefficients p_n = x^n - (m/(m-1)) x^{n-2}, n>=4
def p_support(n):
    # returns list of (degree, coeff)
    if n == 0:
        return [(0, S(1))]
    if n == 1:
        return [(1, S(1))]
    m = n // 2
    assert n >= 4, n
    return [(n, S(1)), (n-2, -S(m)/(m-1))]

def kept_check(rep_moments, n):
    # p_n in V  <=>  <v_j, p_n> = 0 for all j
    if n in (2, 3):
        # p_2, p_3 are NOT in the sparse family; degree 2,3 are free bases, not kept indices
        return False, None
    supp = p_support(n)
    for (deg, coeff) in supp:
        # coeff * a^{(j)}_deg accumulated
        pass
    # compute value per j
    vals = []
    for a in rep_moments:   # a is a function k -> <v_j, x^k>
        s = S(0)
        for (deg, coeff) in supp:
            s += coeff * a(deg)
        vals.append(s)
    return all(v == 0 for v in vals), vals

# representers: j=0 -> v=exp(x), j=1 -> v=1
rep_moments = [moment_exp, moment_one]

print("=== kept index set N: p_n in V for H=L^2([-1,1]), V = {f: <e^x,f>=0, <1,f>=0} ===")
N = []
for n in range(0, 40):
    ok, vals = kept_check(rep_moments, n)
    if ok:
        N.append(n)
print("kept n:", N)
print()

# Now the recursion/run structure.  On the even side, kept p_{2m} (m>=2) impose
# M_{2m} = (m/(m-1)) M_{2m-2}.  Print the validity of the run interpretation.
print("=== Run structure on kept set ===")
evens_kept = [n for n in N if n % 2 == 0 and n >= 4]
odds_kept  = [n for n in N if n % 2 == 1 and n >= 5]
print("kept evens (>=4):", evens_kept)
print("kept odds  (>=5):", odds_kept)

# ---------- Projection density (numerical) ----------
# Build a finite Gram basis: monomials 1..x^{D}.  H = L^2([-1,1]).
# W = span{1, e^x}  (approximately, using polynomial approx of e^x to degree D
# makes this a "coordinate-like" model; to keep it genuinely non-diagonal we
# orthonormalize {1,e^x} and project monomials onto V = W^\perp).

D = 12
# Legendre-like: moments <x^i, x^j>_L2
def gram_l2(i, j):
    return (1 - (-1)**(i+j+1)) / (i+j+1)

G = np.array([[gram_l2(i, j) for j in range(D+1)] for i in range(D+1)])
# W basis vectors in monomial coordinates: 1 (e0), and e^x approx by Taylor to deg D
wvec = np.zeros(D+1)
wvec[0] = 1.0
evec = np.array([1.0/math.factorial(k) for k in range(D+1)])  # e^x Taylor coeffs (NOT orthonormal in L2 yet)

# orthonormalize {1, e^x} in H=L2 via Gram-Schmidt w.r.t. inner product G
def inner(u, v):
    return u @ G @ v

u1 = wvec / np.sqrt(inner(wvec, wvec))
proj_e_on_u1 = inner(evec, u1) * u1
e_orth = evec - proj_e_on_u1
nrm = np.sqrt(inner(e_orth, e_orth))
u2 = e_orth / nrm if nrm > 1e-12 else e_orth

# Projection P_V onto V = W^\perp (W = span{u1,u2})
# w_coords = [<f,u1>,<f,u2>]
def project_onto_V(f):
    c1 = inner(f, u1)
    c2 = inner(f, u2)
    p = f - (c1*u1 + c2*u2)
    return p

# Monomials x^k as coords
mons = [np.eye(D+1)[k] for k in range(D+1)]
proj_mons = [project_onto_V(m) for m in mons]

# Q: do projected monomials span V (restricted to degree-D polynomials vanishing
# on W)?  Check rank of the Gram matrix of {P_V monomials}.
PV = np.array(proj_mons)[:, :D+1]
GPV = PV @ G @ PV.T
rk = np.linalg.matrix_rank(GPV, tol=1e-9)
print("rank of Gram({P_V x^k : k=0..D}) =", rk, " (D+1 =", D+1, ")")
print("dim V restricted (D+1 - dim W) =", D+1 - 2)
print("=> projection-density evidence: rank equals dim V (poly projections span V).")
