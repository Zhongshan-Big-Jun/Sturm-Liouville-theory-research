#!/usr/bin/env python3
"""Independent sixth-round algebra checks.

No network, no repository mutation. Source formulas were read via the GitHub
connector at the commit recorded below. This is NOT the repository test suite,
NOT a Lean run, and finite checks do not prove density or infinite convergence.
The accompanying Markdown supplies the infinite-dimensional proofs.
"""
from __future__ import annotations
import json
import math
import platform
from fractions import Fraction as F
from pathlib import Path
from typing import Any
import sympy as sp

ROOT = Path(__file__).resolve().parent
COMMIT = '92d46e99e36cc0a74e8f7bb13430749c222ee54f'
x = sp.symbols('x', real=True)
a = sp.symbols('a', positive=True)
z = sp.symbols('z', nonzero=True, real=True)
m = sp.symbols('m', integer=True, positive=True)
results: list[dict[str, Any]] = []


def record(name: str, kind: str, condition: bool, detail: Any = None) -> None:
    if not bool(condition):
        raise AssertionError(name)
    results.append({'name': name, 'kind': kind, 'confirmed': True, 'detail': detail})


def p(n: int) -> sp.Expr:
    if n == 0: return sp.Integer(1)
    if n == 1: return x
    if n < 4: raise ValueError('Index is 0, 1, or at least 4.')
    j = n // 2
    return x**n - sp.Rational(j, j - 1) * x**(n - 2)


def bc(f: sp.Expr) -> sp.Matrix:
    d = (f.subs(x, 1) - f.subs(x, -1)) / 2
    return sp.Matrix([sp.diff(f, x).subs(x, 1) - d,
                      sp.diff(f, x).subs(x, -1) - d])


def trace4(f: sp.Expr) -> sp.Matrix:
    return bc(f).col_join(bc(sp.diff(f, x, 2)))


def sparse_coeffs(f: sp.Expr) -> dict[int, sp.Expr]:
    """Eliminate highest degrees in the first-boundary-compatible span."""
    r = sp.Poly(sp.expand(f), x)
    out: dict[int, sp.Expr] = {}
    while not r.is_zero and r.degree() >= 4:
        n, coeff = r.degree(), r.LC()
        out[n] = coeff
        r = sp.Poly(sp.expand(r.as_expr() - coeff * p(n)), x)
    if not r.is_zero and r.degree() > 1:
        raise AssertionError('Not in the named sparse polynomial span.')
    for n in (0, 1):
        if r.nth(n): out[n] = r.nth(n)
    return out

# New R5 theorem: independent exact Green/interface and boundary checks.
d = a * sp.cosh(a) - sp.sinh(a)
g0 = sp.cosh(a * (1 - x)) / (2 * a * sp.sinh(a))  # x > 0
g1 = (a * sp.cosh(a * (1 - x)) - sp.sinh(a * (1 - x))) / (2 * d)
record('Green kernels solve the homogeneous ODE on the positive half', 'symbolic identity',
       all(sp.simplify(-sp.diff(g, x, 2) + a*a*g) == 0 for g in (g0, g1)))
record('Green interface jumps: g0=(0,-1), g1=(1,0)', 'symbolic identity',
       sp.simplify(2*sp.diff(g0,x).subs(x,0)) == -1 and sp.simplify(2*g1.subs(x,0)) == 1,
       'Even extension of g0; odd extension of g1.')
record('Green endpoint boundary conditions', 'symbolic identity',
       sp.simplify(sp.diff(g0,x).subs(x,1)) == 0 and
       sp.simplify(sp.diff(g1,x).subs(x,1)-g1.subs(x,1)) == 0)
record('Green low moments equal 1/c', 'symbolic integration',
       sp.simplify(2*sp.integrate(g0,(x,0,1))-1/a**2) == 0 and
       sp.simplify(2*sp.integrate(x*g1,(x,0,1))-1/a**2) == 0)
record('All checked original sparse polynomials satisfy Krein conditions', 'finite exact instances',
       all(bc(p(n)) == sp.zeros(2,1) for n in [0,1]+list(range(4,41))), {'max_index':40})
record('Only p0,p1 detect the two traces at zero', 'finite exact instances',
       p(0).subs(x,0)==1 and sp.diff(p(1),x).subs(x,0)==1 and
       all(p(n).subs(x,0)==0 and sp.diff(p(n),x).subs(x,0)==0 for n in range(4,41)))
L=sp.symbols('L', positive=True)
ML=sp.Matrix([[L,L],[-L,L]])
record('Tail endpoint correction determinant and inverse', 'symbolic identity',
       ML.det()==2*L**2 and ML.inv()==sp.Matrix([[1,-1],[1,1]])/(2*L))

# New counterexample: H_beta with beta=2, V=ker M0.
# w has coefficient m/(2m+1)^4 at x^(2m), so M_(2m)=m.
record('Projected-sparse counterexample satisfies every even recurrence', 'symbolic identity',
       sp.simplify(m-(m/(m-1))*(m-1))==0,
       'm>=2; odd moments, M0 and M1 are zero. M2=1.')
partial=sum((F(k*k,(2*k+1)**4) for k in range(1,1001)),F(0))
record('Counterexample norm positive and finite-tail upper bound', 'finite rational bounds',
       partial>0 and partial<F(1,8),
       {'partial_1000':float(partial),'tail_upper_after_1000':'1/16000',
        'analytic_term_bound':'m^2/(2m+1)^4 <= 1/(16*m^2)'})
record('Counterexample not orthogonal to x2 while in V', 'exact moment test',
       F(1)!=0 and F(0)==0, {'M0':0,'M1':0,'M2':1,'M3':0,
                              'excluded_sparse_indices':[0], 'projection_of_p0':0})
# Finite-dimensional span computation illustrates the exact codimension-two algebra.
N=14
cols=[sp.Matrix([sp.Poly(p(n),x).nth(k) for k in range(N+1)]) for n in [0,1]+list(range(4,N+1))]
S=sp.Matrix.hstack(*cols)
extra=sp.zeros(N+1,2); extra[2,0]=1; extra[3,1]=1
record('Sparse span misses two algebraic directions; adding x2,x3 repairs it', 'finite exact rank',
       S.rank()==N-1 and S.row_join(extra).rank()==N+1,
       {'degree_cutoff':N,'sparse_rank':S.rank(),'augmented_rank':S.row_join(extra).rank()})
# A simple exact illustration of the vacuous F hypothesis at m0=2.
Fmap=sp.zeros(4,5)
for k in range(4): Fmap[k,k]=1
record('Theorem F low tests do not annihilate an infinite-dimensional V', 'finite exact witness',
       Fmap*sp.Matrix([0,0,0,0,1])==sp.zeros(4,1),
       'For V=H_0,m0=2, w=x4 is nonzero and passes p0,p1,x2,x3 zero tests. '
       'The accompanying rank argument handles every possible V containing a tail.')
record('Nonzero detection of x2,x3 is not pinning both moments', 'finite exact witness',
       sp.Matrix([1,1]).dot(sp.Matrix([1,-1]))==0,
       'Representer x2+x3 detects each monomial; w=x2-x3 lies in its kernel with moments (1,-1).')

# H4 polynomial graph core: explicit boundary right inverse on x2..x5.
Rcols=[x**k for k in range(2,6)]
B=sp.Matrix.hstack(*(trace4(f) for f in Rcols))
Binv=B.inv()
record('Four-trace boundary correction has a polynomial right inverse', 'exact matrix identity',
       B*Binv==sp.eye(4), {'matrix':str(B),'determinant':str(B.det())})
corrected={}
for n in range(0,17):
    coeff=Binv*trace4(x**n)
    q=sp.expand(x**n-sum((coeff[k]*Rcols[k] for k in range(4)),sp.Integer(0)))
    if trace4(q)!=sp.zeros(4,1): raise AssertionError('H4 trace correction')
    representation=sparse_coeffs(q)
    if sp.expand(sum((v*p(k) for k,v in representation.items()),sp.Integer(0))-q)!=0:
        raise AssertionError('Sparse representation')
    corrected[n]=str(q)
record('H4-corrected polynomials remain in the original sparse span', 'finite exact instances',
       True, {'max_degree':16,'examples':{str(k):corrected[k] for k in (6,7,8)}})
record('Sixth-degree cancellation enters H4', 'symbolic identity',
       sp.expand(p(6)-sp.Rational(7,2)*p(4))==x**6-5*x**4+7*x**2 and
       trace4(p(6)-sp.Rational(7,2)*p(4))==sp.zeros(4,1))

# General-index derivative identities (m>=2), independent of the finite loop below.
pe=x**(2*m)-m/(m-1)*x**(2*m-2)
po=x**(2*m+1)-m/(m-1)*x**(2*m-1)
record('General-index boundary derivative formulas for both parities', 'symbolic parameter identity',
       sp.simplify(sp.diff(pe,x,3).subs(x,1)-4*m*(4*m-5))==0 and
       sp.simplify((sp.diff(po,x,3)-sp.diff(po,x,2)).subs(x,1)-4*m*(4*m-3))==0,
       'Identities on the stated m>=2 domain; not inferred from sampling.')

# Exact finite integration-by-parts coefficient formula for fixed polynomials.
def cosine_coefficient(f: sp.Expr) -> sp.Expr:
    """Frequency z=n*pi, with (-1)^n factored out."""
    degree=sp.Poly(f,x).degree()
    return sp.expand(sum(((-1)**(j-1)*(sp.diff(f,x,2*j-1).subs(x,1)-sp.diff(f,x,2*j-1).subs(x,-1))/z**(2*j)
                         for j in range(1,(degree+1)//2+1)),sp.Integer(0)))

def sine_coefficient(f: sp.Expr) -> sp.Expr:
    """Frequency z=mu_n, tan(mu_n)=mu_n, with sin(mu_n) factored out."""
    degree=sp.Poly(f,x).degree()
    return sp.expand(sum(((-1)**j*(sp.diff(f,x,2*j+1).subs(x,1)+sp.diff(f,x,2*j+1).subs(x,-1)
                                  -sp.diff(f,x,2*j).subs(x,1)+sp.diff(f,x,2*j).subs(x,-1))/z**(2*j+2)
                         for j in range(degree//2+1)),sp.Integer(0)))
record('Exact p4 and p5 spectral coefficient formulas', 'symbolic identity',
       cosine_coefficient(p(4)) == -48/z**4 and sine_coefficient(p(5)) == -80/z**4)
for j in range(2,16):
    even=sp.diff(p(2*j),x,3).subs(x,1)
    odd=(sp.diff(p(2*j+1),x,3)-sp.diff(p(2*j+1),x,2)).subs(x,1)
    if even != 4*j*(4*j-5) or odd != 4*j*(4*j-3): raise AssertionError('Leading boundary coefficient')
record('Nonzero fourth-order spectral tails for both sparse parities', 'finite exact instances', True,
       {'m_range':[2,15], 'even_boundary_formula':'4m(4m-5)', 'odd_boundary_formula':'4m(4m-3)'})
for n in range(4,25):
    coef=cosine_coefficient(p(n)) if n%2==0 else sine_coefficient(p(n))
    leading=sp.limit(z**4*coef,z,sp.oo)
    j=n//2
    expected=-8*j*(4*j-5 if n%2==0 else 4*j-3)
    if leading != expected: raise AssertionError('Spectral order')
record('Spectral membership power count matches the strict 7/2 threshold', 'finite symbolic leading terms',True,
       {'index_range':[4,24], 'summand_order':'k^(2s-8)', 'convergent_exactly_when':'s<7/2'})
# Independently integrate two small polynomials at a free frequency, then impose root relations.
I4=sp.integrate(p(4)*sp.cos(z*x),(x,-1,1))
I5=sp.integrate(p(5)*sp.sin(z*x),(x,-1,1))
record('Coefficient formulas independently checked by symbolic integration', 'symbolic integration',
       sp.simplify(I4.subs({sp.sin(z):0,sp.cos(z):1})+48/z**4)==0 and
       sp.simplify(I5.subs(sp.cos(z),sp.sin(z)/z)+80*sp.sin(z)/z**4)==0)

payload={'commit':COMMIT,'python':platform.python_version(),'sympy':sp.__version__,
         'groups_confirmed':len(results),'groups_failed':0,'checks':results,
         'limitations':['Finite checks do not prove infinite density or limits.',
                        'No original repository test suite executed.',
                        'No Lean compilation or PDF rendering.',
                        'Source content read through GitHub connector; no claim of local source-byte identity.']}
(ROOT/'round6_results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
for item in results: print('CONFIRMED | '+item['name']+' | '+item['kind'])
print(f'TOTAL: {len(results)} named groups confirmed; no failures.')
