# Problem contract

Contract version: `arm-a-frozen-v1`, 2026-08-28 (Asia/Shanghai).

## Objects and definitions

Let \(I=[-1,1]\), \(c>0\), and \(L=c-D^2\).  On \(L^2(I)\),
\[
 D(K_c)=\{f\in H^2(I): f'(1)=f'(-1)=(f(1)-f(-1))/2\},\qquad K_cf=Lf.
\]
Write \(K_0=K_c-cI\).  Its closed form is
\[
 a_0(f,g)=\int_{-1}^1 f'\overline{g'}-\tfrac12
 (f(1)-f(-1))\overline{(g(1)-g(-1))},\quad D(a_0)=H^1(I),
\]
and \(a_c=a_0+c\langle\cdot,\cdot\rangle_{L^2}\).  Thus
\(D(K_c^{1/2})=H^1(I)\) with norm induced by \(a_c\).

For a positive integer \(r\), distinguish:

1. \(K_c^{-r}\), the bounded inverse of the self-adjoint operator, whose range is
   \(D(K_c^r)\); and
2. \(L_{\rm poly}^{-r}\), the inverse of \(L\) on \(\mathbb C[x]\).  It exists because
   \(L\) is triangular with nonzero diagonal \(c\), preserves degree, and does not
   impose boundary conditions.

Let \(P_n\) be any nonzero degree-\(n\) \(L^2(I)\)-orthogonal polynomial.
Let \(R_n\) be any nonzero degree-\(n\) polynomial orthogonal to all lower-degree
polynomials for \(a_c\).  Normalizations do not affect any conclusion.

Under the **polynomial/abstract reading**, for \(s\ge4\),
\[
 Q_n^{(2r)}=L_{\rm poly}^{-r}P_n,\qquad
 Q_n^{(2r+1)}=L_{\rm poly}^{-r}R_n.
\]
Under the competing **genuine-operator reading**, put
\[
 \widetilde Q_n^{(2r)}=K_c^{-r}P_n,\qquad
 \widetilde Q_n^{(2r+1)}=K_c^{-r}R_n.
\]
The tilded objects need not be polynomials.

The abstract polynomial inner products are
\[
 [p,q]_{2r}^{\rm abs}=\langle L^rp,L^rq\rangle_{L^2},\qquad
 [p,q]_{2r+1}^{\rm abs}=a_c(L^rp,L^rq).
\]

## Hypotheses

- \(c>0\).
- \(s\in\mathbb Z\), \(s\ge4\).
- The boundary notation means both one-sided endpoint derivatives equal the
  same displayed number.
- "Orthogonal polynomial system" means exactly one nonzero polynomial of every
  degree, up to normalization.  The degree-preserving property above verifies
  this for the displayed construction.

## Target conclusion

1. Give an if-and-only-if condition, with all \(s,n,c\) quantifiers, for the
   abstract-polynomial \(Q_n^{(s)}\) to belong to \(D(K_c^{s/2})\); separately
   record the outcome under the genuine-operator interpretation.
2. Decide canonical equality (not merely abstract Hilbert-space isomorphism)
   between \(D(K_c^{s/2})\) and the completion of \(\mathbb C[x]\) in
   \([\cdot,\cdot]_s^{\rm abs}\).
3. Decide whether the literal span of the polynomial \(Q_n^{(s)}\) is a dense
   linear subspace of \(D(K_c^{s/2})\) in its left-definite norm; separately
   record the tilded operator-image statement.

## Quantifiers and dependency of constants

The claims must hold for every real \(c>0\), every integer \(s\ge4\), and every
integer \(n\ge0\).  No exceptional value of \(c\), parity of \(s\), or finite
test range may be suppressed.  Normalizing constants for \(P_n,R_n,Q_n^{(s)}\)
may depend on \(n,s,c\) but are nonzero.

## Equivalent formulations that are actually proved equivalent

For a polynomial \(p\) and \(m\ge1\), membership in \(D(K_c^m)\) is equivalent
to the iterated boundary conditions
\[
 B(L^jp)=0\quad(0\le j<m),
\]
where \(B(f)=\big(f'(1)-\Delta f/2,\ f'(-1)-\Delta f/2\big)\) and
\(\Delta f=f(1)-f(-1)\).  For a polynomial and integer \(s\),
\(p\in D(K_c^{s/2})\) is equivalent to these conditions for
\(0\le j<\lfloor s/2\rfloor\); the remaining half-power condition when \(s\)
is odd is automatic because the final polynomial lies in \(H^1(I)\).

"Equals" in target 2 means equality under the identity on polynomial
representatives in a common function realization.  A unitary map that replaces
each polynomial representative by a different boundary-corrected function proves
unitary equivalence, not this equality.

## Boundary and degenerate cases

- \(n=0,1\) must be treated: affine polynomials satisfy the Krein boundary
  condition and form \(\ker K_0\).
- \(n\ge2\) must be proved uniformly.
- Both \(s=2r\) and \(s=2r+1\) are separate gates; here \(r\ge2\).
- \(c=0\) is excluded and no inverse is asserted there.
- The operator domain is not confused with an abstract completion whose elements
  are equivalence classes of Cauchy sequences.

## Permitted outcomes

- affirmative proof;
- negative proof/counterexample;
- a two-reading resolution if the notation is genuinely ambiguous.

## Completion criteria

All three numbered questions are answered for all stated quantifiers, the parity
split is closed, the operator/abstract distinction is explicit, and an independent
adversarial proof audit finds no load-bearing gap.  The exact set of all degrees of
arbitrary domain-compatible polynomial combinations is optional.

## Answer space

The result must decide whether the named polynomial OPS is actually an
operator-domain basis, rather than only an abstract orthogonal basis, and state
what changes if \(K_c^{-r}\) is read as the genuine operator inverse.

## Acceptance criteria per subproblem

- Q1: an explicit iff, not merely sufficient boundary equations.
- Q2: a yes/no for canonical equality, while recording any valid unitary
  equivalence separately.
- Q3: a yes/no for the literal span as a subspace; any repaired statement such
  as intersection density must be labeled as such and proved before use.

## Results that do not count as completion

Finite-degree computation; a degree spectrum alone; calling two separable Hilbert
spaces "equal" because they are isomorphic; proving density of boundary-corrected
images while naming the original polynomials; or treating formal \(L^{-1}\) as
the resolvent \(K_c^{-1}\).

## Forbidden moves

No repository/project-file inspection, repository history, network, known-solution
lookup, numerical-to-universal inference, silent theorem invocation, quantifier
weakening, or mutation of the frozen contract.

## Tool, citation, and search constraints

Only the frozen prompt, the requested skill protocol, fresh artifacts in this run,
and local symbolic/exact computation created in this run may be used.  External
theorems must be stated with hypotheses.  No literature-status or novelty claim is
permitted because literature access is forbidden.

## Ambiguities or competing interpretations

The phrase "defined via the isometries \(K_c^{-r}\)" conflicts with "polynomial"
unless it denotes the algebraic polynomial inverse: the true resolvent generally
adds homogeneous \(\cosh(\sqrt c x),\sinh(\sqrt c x)\) corrections.  Both readings
are therefore contractually separated above.

## Contract audit

Second-pass audit against the frozen statement: PASS WITH AMBIGUITY PRESERVED.
The audit checked the interval endpoints, both boundary equations, \(c>0\), integer
\(s\ge4\), all \(n\ge0\), even/odd constructions, power domains, the word
"completion", the optional degree-spectrum clause, and the no-network/no-project
restriction.  No polarity was assumed.  The only added notation is explicitly
defined and creates no stronger hypothesis.
