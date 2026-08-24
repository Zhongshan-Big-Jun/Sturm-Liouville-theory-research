# SUB-ADV adversarial/counterexample report

**Status:** `NONE_FOUND`

## Scope and provenance

I attacked the stated universal assertion only from the frozen definitions in
`problem_contract.md` and `obligation_graph.md`. Their SHA-256 hashes matched the
packet values. I used no external theorem, source, or numerical scan. The tested
domain below is symbolic and uniform in every integer `n>=1` and every real
`s>1`; the excluded boundary `s=1` is audited separately.

This report does **not** claim global completion. It records exact constraints
which rule out the packet's requested counterexample mechanisms.

## Exact reduction used to attack failures

Put

`z=(tr C_s(y))/2 = 1-a sin^2(y) = a x^2+1-a`,

where `x=cos y` and

`a=(s+1)^2/(2s)=(s+2+s^{-1})/2`.

Direct expansion gives `det C_s(y)=1`. Define the Chebyshev polynomials of the
second kind only through

`U_{-1}=0`, `U_0=1`, and `U_k(z)=2zU_{k-1}(z)-U_{k-2}(z)`.

Cayley--Hamilton and induction then give, including `n=1`,

`C_s(y)^n=U_{n-1}(z)C_s(y)-U_{n-2}(z)I`.

Furthermore,

`(E(y)C_s(y))_{12}=sin(y)[(2+s^{-1})x^2-s(1-x^2)]`

and `E(y)_{12}=sin y`. Since

`(2+s^{-1})x^2-s(1-x^2)=2z+s^{-1}`,

one obtains the exact identity

`G_{n,s}(y)=sin(y) P_{n,s}(z)`,

`P_{n,s}(z)=U_n(z)+s^{-1}U_{n-1}(z)`.

Thus the polynomial from the contract extends as

`Q_{n,s}(x)=P_{n,s}(a x^2+1-a)`.

It has exact degree `2n`: `P_{n,s}` has degree `n` and leading coefficient
`2^n`, while `a>0`.

## Repeated-root and root-location attack

Let `r=s^{-1}`, so `0<r<1`, and let `J_n` be the real symmetric tridiagonal
`n` by `n` matrix whose first diagonal entry is `-r`, whose other diagonal
entries are zero, and whose two adjacent off-diagonals are all one. Expansion
from the last row (with the one-dimensional case checked directly) gives

`det(2z I-J_n)=U_n(z)+rU_{n-1}(z)=P_{n,s}(z)`.

Every eigenvalue of `J_n` is simple. Indeed, an eigenvector's first coordinate
cannot vanish: the first row and then the successive tridiagonal rows would
force every coordinate to vanish. Once its first coordinate is chosen, all
later coordinates are recursively determined, so each eigenspace has dimension
at most one. A real symmetric matrix is orthogonally diagonalizable (the
spectral theorem), hence algebraic and geometric multiplicities coincide.

For every nonzero real vector `v=(v_1,...,v_n)`, with empty sums understood when
`n=1`,

`v^T(J_n+2I)v = sum_{i=1}^{n-1}(v_i+v_{i+1})^2 +(1-r)v_1^2+v_n^2 >0`,

`v^T(2I-J_n)v = sum_{i=1}^{n-1}(v_i-v_{i+1})^2 +(1+r)v_1^2+v_n^2 >0`.

Consequently every eigenvalue `lambda` satisfies `-2<lambda<2`. Therefore
`P_{n,s}` has exactly `n` distinct real zeros, all in `(-1,1)`.

This also defeats contamination at the vertex of the quadratic substitution.
For `s>1`, `a>2`, so the vertex value is `z(0)=1-a<-1`; it is not a zero of
`P_{n,s}`. If `rho` is any zero of `P_{n,s}`, then

`x^2=(rho+a-1)/a` lies strictly in `(0,1)`.

Thus the only lifts are the two nonzero values of `x` with this square. At each
such lift, `dz/dx=2ax` is nonzero. Combined with the simplicity of `rho`, this
rules out every repeated-root mechanism coming from either the scalar
polynomial or the quadratic map. On `(0,pi)`, `sin y>0` and
`d(cos y)/dy=-sin y` is nonzero, so neither multiplication by `sin y` nor the
change from `x` to `y` introduces or merges an interior root.

## Required exact edge audits

- **`n=1`.** Here
  `Q_{1,s}(x)=(s+2+s^{-1})x^2-s`; its two roots are
  `x=+/-s/(s+1)`, both in `(-1,1)` and simple.
- **`y=0`.** Directly `sin y=0`, hence `G_{n,s}(0)=0`. It is an excluded
  endpoint. Since `z=1` and
  `P_{n,s}(1)=(n+1)+n/s>0`, this endpoint zero is simple and cannot hide an
  interior multiplicity.
- **`y=pi`.** Again `G_{n,s}(pi)=0`, an excluded endpoint. The polynomial is
  even in `x`, so its value at `x=-1` is the same nonzero value
  `(n+1)+n/s`; the endpoint zero is simple.
- **`y=pi/2`.** Here
  `C_s(pi/2)=diag(-s^{-1},-s)` and the first row of `E(pi/2)` is `(0,1)`.
  Thus `G_{n,s}(pi/2)=(-s)^n`, which is nonzero. This directly audits the
  quadratic vertex.
- **Boundary `s=1` (`R=1`).** In this excluded case
  `C_1(y)=E(2y)`, hence
  `M_{n,1}(y)=E((2n+1)y)` and
  `G_{n,1}(y)=sin((2n+1)y)`. Its open-interval zeros are precisely
  `k pi/(2n+1)` for `k=1,...,2n`, and all are simple. Equivalently, the
  vertex has `z=-1`, but
  `U_n(-1)+U_{n-1}(-1)=(-1)^n`, so it is still not a root.

## Failure mechanism and exact gap

No exact counterexample was found. The candidate failure mechanisms tested were:
endpoint contamination, a zero at `y=pi/2`, a zero at the quadratic vertex,
loss of roots under the quadratic substitution, repeated scalar roots, repeated
lifted roots, exceptional low degree `n=1`, and degeneration at `s=1`. The
identities above rule them out uniformly in the stated domain.

The first untested general obligation is `O5`: a fresh, independent audit of the
coordinator's eventual integrated proof, including verification that its
presentation contains every identity and multiplicity implication used here.
This subtask has not inspected that future proof and therefore cannot certify
global completion.
