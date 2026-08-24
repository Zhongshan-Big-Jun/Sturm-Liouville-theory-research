INDEPENDENTLY_AUDITED_PROOF

# Result

## Exact theorem proved

The assertion is true. For every integer `n>=1` and every `R>1`, with `s=sqrt(R)`, the function `G_{n,s}` has exactly `2n` zeros in `(0,pi)`, all simple.

Moreover, the quotient in the problem extends to an even polynomial of exact degree `2n`:

\[
Q_{n,s}(x)=P_n\bigl((1+a)x^2-a\bigr),\qquad
a=\frac{s+s^{-1}}2,
\]

where

\[
P_n(z)=U_n(z)+s^{-1}U_{n-1}(z),
\]

and `U_{-1}=0`, `U_0=1`, `U_k=2zU_{k-1}-U_{k-2}`.

## Proof

Put `r=s^{-1}` and `z=c^2-aq^2`. Direct expansion gives

\[
\det C_s=1,\qquad \operatorname{tr}C_s=2z.
\]

For a `2x2` matrix `A`, direct entrywise expansion gives

\[
A^2-(\operatorname{tr}A)A+(\det A)I=0.
\]

Using this identity and the recurrence defining `U_k`, induction gives, for every `n>=1`,

\[
C_s^n=U_{n-1}(z)C_s-U_{n-2}(z)I. \tag{1}
\]

Also,

\[
(EC_s)_{12}
=q\bigl((2+r)c^2-sq^2\bigr)
=q(2z+r),
\]

while `E_{12}=q`. Taking the `(1,2)` entry of (1) therefore yields

\[
G_{n,s}(y)=q\,[U_n(z)+rU_{n-1}(z)]=qP_n(z). \tag{2}
\]

For `x in (-1,1)` and `y=arccos x`, one has `q=sqrt(1-x^2)>0` and

\[
z=(1+a)x^2-a.
\]

Thus (2) proves the claimed polynomial extension. Since `U_n` has degree `n` and leading coefficient `2^n`, the exact leading coefficient of `Q` is

\[
2^n(1+a)^n=\left(\frac{(s+1)^2}{s}\right)^n>0,
\]

so `deg Q=2n`.

It remains to locate all roots. For `0<theta<pi`, the recurrence and the sine addition formula give

\[
U_k(\cos\theta)=\frac{\sin((k+1)\theta)}{\sin\theta}. \tag{3}
\]

Let `F(theta)=P_n(cos theta)` and set `theta_j=j*pi/n`. The endpoint values are

\[
F(0)=n+1+rn>0,
\qquad
F(\pi)=(-1)^n[(n+1)-rn],
\]

with `(n+1)-rn=1+n(1-r)>0`. For `1<=j<=n-1`, (3) gives

\[
F(\theta_j)=(-1)^j.
\]

Hence the values at `theta_j`, `j=0,...,n`, strictly alternate in sign. This includes `n=1`, when there are no internal mesh points.

The intermediate value theorem used here states: if a real-valued function is continuous on a closed interval and its endpoint values have opposite signs, it has a zero in the open interval. Applying it on each of the `n` disjoint intervals

\[
(j\pi/n,(j+1)\pi/n),\qquad j=0,\ldots,n-1,
\]

gives `n` distinct roots of `P_n` in `(-1,1)`. A nonzero degree-`n` polynomial has at most `n` distinct roots, by repeated application of the factor theorem. Thus these are all the roots. Since their number equals the degree,

\[
P_n(z)=2^n\prod_{j=1}^n(z-\alpha_j)
\]

with distinct `alpha_j`, and therefore `P_n'(alpha_j)!=0`: all scalar roots are simple.

Because `s>1`,

\[
a=\frac{s+s^{-1}}2>1.
\]

For every `alpha_j in (-1,1)`, the equation `Q(x)=0` has exactly the two solutions

\[
x=\pm\sqrt{\frac{\alpha_j+a}{1+a}}.
\]

Their squared value is strictly between `0` and `1`, and neither solution is zero. Conversely, every root of `Q` arises this way. Hence `Q` has exactly `2n` roots in `(-1,1)`. At any such root,

\[
Q'(x)=P_n'(z(x))\,2(1+a)x\ne0,
\]

so every lifted root is simple.

Finally, on `(0,pi)`,

\[
G(y)=\sin y\,Q(\cos y),
\]

and cosine is a bijection from `(0,pi)` to `(-1,1)`. Thus the root count transfers exactly. At a root,

\[
G'(y)=-\sin^2y\,Q'(\cos y)\ne0.
\]

This proves exactly `2n` simple zeros in `(0,pi)`.

## Required boundary audits

- `n=1`: `Q_{1,s}(x)=((s+1)^2/s)x^2-s`, whose roots are exactly `x=+-s/(s+1)`, both simple and in `(-1,1)`.
- `y=0`: `G(0)=0`, but this endpoint is excluded; `G'(0)=n+1+n/s!=0`.
- `y=pi`: `G(pi)=0`, also excluded; `G'(pi)=-(n+1+n/s)!=0`.
- `y=pi/2`: direct substitution gives `C_s=diag(-s^{-1},-s)` and hence `G(pi/2)=(-s)^n!=0`.
- `R=1`, so `s=1`: `C_1(y)=E(2y)`, hence `G_{n,1}(y)=sin((2n+1)y)`. Its interior zeros are exactly `k*pi/(2n+1)`, `k=1,...,2n`, all simple. Endpoint zeros are not counted.

## Verification performed

- An independent algebraic agent reproduced the reduction, exact degree, root location, lifting, and boundary audits.
- A mechanism-distinct agent proved the same root theorem via a self-contained Sturm--Liouville shooting/Pruefer-angle argument.
- A counterexample agent attacked endpoints, the midpoint/quadratic vertex, repeated scalar roots, repeated lifted roots, `n=1`, and `s=1`; it found no counterexample and supplied a third symmetric-tridiagonal root proof.
- A fresh first-time verifier read only the hash-frozen contract and candidate proof, recomputed every load-bearing step, and returned `PASS` with empty critical-error and gap lists.
- A deterministic symbolic script checked the determinant, trace, `(EC_s)_{12}`, and matrix recurrence instances `n=1,...,6`. No finite computation is used to infer the theorem.
- A file-only convergence pass found all mathematical obligations closed; its stale metadata findings were repaired without changing the audited candidate.

## Remaining gaps

None for the frozen theorem. No proof-assistant formalization was run, so the result is independently audited rather than formally machine-verified.

## Failed and blocked routes

No mathematical route remained blocked. The first two symbolic-check runs exposed only checker defects—failure to reduce `q^3` modulo `c^2+q^2-1`, then a native/symbolic integer mismatch—which were recorded and repaired before the passing run.

## Novelty status

`UNKNOWN`. The blind task forbids internet, repository, history, memory, and prior-solution lookup, so no literature, priority, or novelty claim is made.

## Human/model/tool contributions

- Human: frozen statement, constraints, and requested research workflow.
- Coordinator: theorem contract, algebraic proof, synthesis, ledgers, and final report.
- Subagents: independent algebraic proof, independent oscillation proof, counterexample attack, first-time proof audit, and file-only convergence check.
- Tooling: deterministic exact symbolic identity checks and SHA-256 binding of proof/audit artifacts.

## Reproducibility manifest

- Frozen proof: `candidate_proof.md`, sha256 `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6`.
- Independent audit: `subagents/SUB-AUDIT.md`, sha256 `4c8831a11edbdcb70c4599ef818e96633c507d2feef58a91659953b000f1c92f`.
- Check command: `python3 reproducibility/check_identities.py`.
- Full environment, restrictions, versions, hashes, and expected output: `repro_manifest.md` and `reproducibility/proof_package.sha256`.

## Confidence by axis

- Semantic fidelity: high; contract and all named cases independently audited.
- Mathematical correctness: high; exact proof plus three mechanism-level corroborations and a `PASS` audit.
- Completeness: complete for the frozen theorem.
- Novelty: unknown by blind restriction.
- Reproducibility: high for the natural-language proof, audit, hashes, and exact symbolic checks; no formal proof-assistant certificate.
