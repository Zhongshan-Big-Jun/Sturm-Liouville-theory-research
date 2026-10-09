# Krein analytic bridge contract, 2026-10-08

Written before the new Lean proofs and checked against
`docs/SL_H2_arbitrary_deletion_proof.md`, section 1 (source read directly).

Use complex L2 on (-1,1), represented as `Lp ℂ 2 (volume.restrict (Ioo (-1) 1))`.
L2 elements are equivalence classes. No endpoint or interior trace is defined on
an arbitrary L2 representative.

The Sobolev representation to construct contains actual complex-valued f and df
continuous on [-1,1], and measurable ddf with finite L2 norm on (-1,1), together
with both reconstruction identities for every x in [-1,1]:

f(x) = f(-1) + integral(-1,x,df),
df(x) = df(-1) + integral(-1,x,ddf).

The Krein domain consists of the L2 classes having such a representation and
satisfying df(1) = df(-1) = (f(1)-f(-1))/2. The operator on this domain has L2
class -ddf + c*f. Its single-valuedness must be proved from the reconstruction
identities and uniqueness of continuous representatives and a.e. derivatives;
it is not an arbitrary choice of point values.

Required polynomial bridge: for every real polynomial p with zero actual
Krein residues, the complexified polynomial belongs to this represented
domain, and its operator image equals the complexified algebraic polynomial
`-p.derivative.derivative + C c*p`. This includes p0=1, p1=X, and all m>=2
of X^(2*m)-C(m/(m-1))*X^(2*m-2) and
X^(2*m+1)-C(m/(m-1))*X^(2*m-1). No finite bound on m or rational restriction on c.

Exact intended root types (before implementation; namespace/API fixed here):

* `(p : Polynomial ℝ) → SL.AuditRound5.residues p = 0 →
    SL.Krein.polynomial_L2 p ∈ SL.Krein.domain`
* `(p : Polynomial ℝ) → (hp : SL.AuditRound5.residues p = 0) → (c : ℝ) →
    SL.Krein.operator c (SL.Krein.polynomial_domain p hp) =
    SL.Krein.polynomial_L2 (-p.derivative.derivative + Polynomial.C c * p)`
* `SL.Krein.polynomial_L2 SL.AuditRound5.p_zero ∈ SL.Krein.domain ∧
    SL.Krein.polynomial_L2 SL.AuditRound5.p_one ∈ SL.Krein.domain ∧
    (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_even m) ∈ SL.Krein.domain) ∧
    (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_odd m) ∈ SL.Krein.domain)`

Extension obligations remain explicit: equivalence with the classical weak
Sobolev definition of H2, closed/self-adjoint/strictly-positive Kc, its inverse
and powers, and the full-family/retained-family density theorem. A C2-to-integral
construction is an inclusion only and never identifies the whole domain.

Additional target fixed before writing the energy proof: for any real polynomial
p satisfying the Krein boundary conditions and any real c, the actual complex
L2 inner product, expressed in the source's first-variable-linear convention,
satisfies

left_inner(Kc p,p) = integral(p'^2) + c*integral(p^2) - (p(1)-p(-1))^2/2.

This requires an actual integration-by-parts theorem plus the regular L2
representative bridge, rather than defining the energy expression to be the
left side. It covers polynomial members only unless a separate extension proof
to all integral representatives is supplied.

Additional weak-derivative target fixed before that proof: for every represented
function and every real C1 test function Phi with Phi(-1)=Phi(1)=0, integrate
by parts separately in real and imaginary components. Each coordinate of Value
has weak derivative the corresponding coordinate of First, and each coordinate
of First has weak derivative the corresponding coordinate of Second. The tests
include ordinary compactly supported smooth tests. The intended integral
identity is integral(f_component * deriv Phi) = -integral(df_component * Phi).
Absolute continuity of the coordinate representatives must be proved from
their integral reconstructions; a.e. differentiability alone is insufficient.
The converse theorem from an independently defined weak H2 class is still open.

