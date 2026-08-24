# SUB-AUDIT: independent first-time proof audit

**Verdict:** `PASS`

## Input integrity and audit posture

The two permitted inputs matched their packet hashes:

- `problem_contract.md`: `4e4695334fddcdcc99e1f5f74ecaa3ad9a98ca452a68dd3483d7dbd4d1e1b0d7`
- `candidate_proof.md`: `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6`

I treated the candidate as a first-time submission and recomputed every
load-bearing identity from the definitions in the contract. I used no other
file, source, numerical scan, or prior result.

## Contract and semantic fidelity

The candidate preserves the exact quantifiers `n>=1`, integer, and `s>1`, real;
it notes the equivalence with `R=s^2>1`. It proves the asserted root count on
the open interval `(0,pi)`, excludes endpoint zeros, proves simplicity as
nonvanishing first derivative, establishes the polynomial extension and exact
degree, and separately audits all five named cases: `n=1`, `y=0`, `y=pi`,
`y=pi/2`, and `s=1`.

## Recomputed algebraic reduction

With `r=s^{-1}`, `a=(s+r)/2`, and `z=c^2-aq^2`, expansion confirms

`det C_s=(c^2-rq^2)(c^2-sq^2)+(1+r)(1+s)c^2q^2=1`

and `tr C_s=2z`. The displayed `2x2` characteristic identity therefore gives
the claimed power formula

`C_s^n=U_{n-1}(z)C_s-U_{n-2}(z)I`

under the candidate's recurrence, including its `n=1` base case.

Direct row-column multiplication confirms

`(EC_s)_{12}=q[(2+r)c^2-sq^2]=q(2z+r)`.

Consequently

`G_{n,s}(y)=q[U_n(z)+rU_{n-1}(z)]`.

For `x=cos y`, the substitution is indeed

`z=(1+a)x^2-a`,

so the contract's quotient is the restriction of

`Q_{n,s}(x)=P_n((1+a)x^2-a)`.

The leading-coefficient calculation is also exact:

`2^n(1+a)^n=((s+1)^2/s)^n>0`.

Thus `P_n` and `Q_{n,s}` have exact degrees `n` and `2n`, respectively.

## Recomputed scalar root theorem

For `theta_j=j*pi/n`, `1<=j<=n-1`, the sine representation gives

`U_{n-1}(cos theta_j)=0` and `U_n(cos theta_j)=(-1)^j`.

The endpoint values are

`P_n(1)=n+1+rn>0`,

`P_n(-1)=(-1)^n[(n+1)-rn]`,

where `(n+1)-rn=1+n(1-r)>0`. Hence the signs at all mesh points
`j*pi/n`, `j=0,...,n`, strictly alternate. This remains valid for `n=1`,
when there are no internal mesh points. Continuity produces one root in each
of the `n` disjoint open theta intervals. Strict injectivity of cosine on
`(0,pi)` makes the corresponding polynomial roots distinct and inside
`(-1,1)`.

Because `P_n` has exact degree `n`, these are all its roots. Its displayed
factorization then correctly implies a nonzero derivative at each root, so all
scalar roots are simple. There is no hidden appeal to numerical evidence or to
an unstated interlacing theorem.

## Recomputed lifting, exhaustion, and simplicity

The strict inequality `s>1` implies `a>1`. For every scalar root
`alpha in (-1,1)`,

`x^2=(alpha+a)/(1+a)`

lies strictly in `(0,1)`, producing exactly two nonzero roots in `(-1,1)`.
Distinct scalar roots give distinct squared values, and conversely every root
of `Q` maps to a root of `P_n`; thus the construction is exhaustive and yields
exactly `2n` roots.

At a lifted root, both `P_n'(z)` and `2(1+a)x` are nonzero, validating the
candidate's derivative proof that every root of `Q` is simple. On `(0,pi)`,
`sin y` is nonzero and cosine is a bijection to `(-1,1)`. Differentiating
`G(y)=sin(y)Q(cos y)` at a zero of `Q` gives exactly

`G'(y)=-sin^2(y)Q'(cos y) != 0`.

Thus neither the prefactor nor either substitution loses, duplicates, or
changes the multiplicity of an interior zero.

## Recomputed boundary and special-case audits

- For `n=1`, substitution into `P_1=2z+r` gives
  `Q_{1,s}=((s+1)^2/s)x^2-s`, with the two stated simple roots
  `+/-s/(s+1)`.
- At `y=0,pi`, `q=0` and `z=1`, while `P_n(1)>0`. Differentiation gives the
  stated nonzero derivatives `P_n(1)` and `-P_n(1)`. These zeros are endpoints
  and are correctly not counted.
- At `y=pi/2`, `z=-a`. Parity of `U_k` follows from its recurrence. For
  `D_n=U_n(a)-rU_{n-1}(a)`, recomputation gives
  `D_n=(2a-r)U_{n-1}-U_{n-2}=sD_{n-1}`, because `2a-r=s` and `sr=1`.
  Thus `D_n=s^n` and `G(pi/2)=(-1)^ns^n`, nonzero.
- At excluded `s=1`, direct substitution confirms `C_1(y)=E(2y)` and direct
  multiplication confirms the rotation addition law. Therefore
  `G_{n,1}(y)=sin((2n+1)y)`, with precisely the stated `2n` interior simple
  zeros and excluded endpoints.

## Audit result

- **Critical errors:** none.
- **Gaps:** none.
- **Repair hints:** none required.
- **First error:** none.
- **Covered scope:** semantic fidelity; all matrix identities; the polynomial
  quotient and exact degree; complete scalar root location, count, and
  simplicity; exhaustive two-to-one lifting; preservation of multiplicity in
  `y`; endpoint conventions; and every separately mandated special case.
- **Residual risk:** ordinary transcription risk only. No mathematical or
  contractual gap was found in the frozen candidate under the permitted input
  scope.
