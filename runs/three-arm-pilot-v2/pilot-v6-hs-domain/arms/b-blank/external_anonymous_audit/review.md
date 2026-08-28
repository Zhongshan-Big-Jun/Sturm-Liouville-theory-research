RIGOROUS_PARTIAL_RESULT

# Pilot v6 Arm B neutral posthoc audit

## Verdict

`REPAIRABLE_GAP`

The three completion-gate conclusions are mathematically correct and mutually consistent. The submission clears the preregistered acceptance thresholds. It does not receive `PASS` because equation (2), the load-bearing power-domain characterization, is invoked through unspecified one-dimensional regularity rather than derived with the theorem hypotheses stated, and because the final bonus degree-spectrum formula is asserted without proof. Both gaps are local and do not undermine the stated conclusions.

Acceptance status: `ACCEPTED_WITH_REPAIRABLE_GAPS`.

## Isolation and provenance

This was a first-time anonymous audit. The only mathematical inputs inspected were:

1. `frozen_task.md`, SHA256 `359D335803EAE43F45120E3CA3995B8F12EC2F98B357E2B10116EAFE2D8C6332`.
2. `final_response.md`, SHA256 `874B0BDE9DFAF194E8279519C2C70D739A8E4125094AA5495884FFFA5C78EE58`.

No repository history, hidden gold, Arm A or Arm C material, other project documents, memories, network sources, or scored session trace was inspected. This audit's usage is excluded from all scored Arm B metrics.

## First error

First load-bearing unsupported step: Section 1, equation (2).

Error layer: `dependency/proof`.

The formula

\[
D(A^{s/2})=\{f\in H^s:B(T^jf)=0,\ 0\le j<r\}
\]

is correct for this positive constant-coefficient realization, but the response only says that spectral calculus and one-dimensional regularity give it. The frozen rules require external theorems to be stated with hypotheses. A local repair is to state and prove the domain recursion

\[
D(A^{k+1})=\{f\in D(A^k):A^kf\in D(A)\},
\qquad
D(A^{k+1/2})=\{f\in D(A^k):A^kf\in D(A^{1/2})\},
\]

and then use the constant-coefficient interval regularity implications for `T^k`. There is no false boundary condition or false conclusion here.

First non-load-bearing gap: the final exact degree spectrum is correct but unproved.

## Required-claim audit

### 1. Membership in the operator power domain

The result

\[
Q_n^{(s)}\in D(K_c^{s/2})\iff n\in\{0,1\}
\]

is correct for every `c > 0` and every integer `s >= 4`, under the polynomial, algebraic-inverse construction used in the response.

- The form sign is correct. With `delta f=(f(1)-f(-1))/2`, direct expansion gives
  \[
  \mathfrak a(f,f)=c\lVert f\rVert_2^2+\lVert f'-\delta f\rVert_2^2.
  \]
- Integration by parts yields exactly the two Krein conditions `f'(1)=delta f` and `f'(-1)=delta f`.
- For an even polynomial `q`, the boundary condition is `q'(1)=0`. For an odd polynomial `q`, it is `q'(1)=q(1)`. The triangular expansion of `T^j` correctly converts these into equation (4).
- For even `s=2r`, the last required boundary condition reduces membership to `RP_n in D(A)`. For even `n >= 2`, every term in `(RP_n)'(1)` is positive. For odd `n >= 3`, each paired endpoint difference is nonnegative and the `m=0` pair is strictly positive. The endpoint formula and its ratio are correct.
- For odd `s=2r+1`, membership forces `u=RS_n in D(A)` and `Au=S_n`. Since `u-S_n/c=u''/c` has degree at most `n-2`, form orthogonality gives `a(S_n,u)=a(S_n,S_n)/c`. The operator-form identity gives the same quantity as `||S_n||_2^2`. Positivity then forces `S_n'-delta S_n=0`, hence `deg S_n <= 1`, contradicting `n >= 2`.
- Both degree-zero and degree-one polynomials satisfy every iterated boundary condition because `T` preserves affine functions.

Both parity cases, the endpoint signs, the quantifiers in `c`, `s`, and `n`, and the power-domain recursion target were checked.

### 2. Abstract completion versus concrete operator domain

The distinction between the algebraic polynomial inverse `R` and the spectral inverse `A^{-1}` is essential and correctly handled.

Because `T^r` is a polynomial automorphism, the abstract even completion is transported onto `L^2`, and the abstract odd completion is transported onto the form space `H^1`. Positivity of `A` makes `A^{-r}` defined on the entire target space, so

\[
J_s=A^{-r}T^r
\]

extends to the stated unitary equivalence. It is not the identity map. The witness `Q_2^(s)` belongs to the original abstract polynomial space but not to `D(A^{s/2})`, so equality under the identity realization fails.

The response is also correctly calibrated in not confusing unitary equivalence with concrete equality.

### 3. Density under the operator-domain reading

The response correctly separates three statements:

1. `span{Q_n^(s)}` is all polynomials but is not a subspace of `D(A^{s/2})`, so it cannot be an operator-domain basis in the literal sense.
2. The span of the individual system elements that lie in the domain is `span{1,x}`, which is not dense in the infinite-dimensional operator domain.
3. The different set `C[x] intersect D(A^{s/2})`, allowing cancellations between the `Q_n^(s)`, is dense in the operator domain.

The third statement is correct. Let `L` be the finite vector of boundary traces in equation (2). Polynomial density in `H^s` implies that `L(C[x])` is a dense linear subspace of the finite-dimensional space `L(H^s)`, hence equals it. A fixed polynomial right inverse on that finite-dimensional range corrects any polynomial approximant into `ker L`, with a correction tending to zero. The specialized elliptic estimate and `A >= cI` identify the graph topology with the `H^s` topology on `ker L`.

## Bonus-claim audit

The exact degree spectrum

\[
\{0,1\}\mathbin{\cup}\{N:N\ge 2r+2\},
\qquad r=\lfloor s/2\rfloor,
\]

is correct, but the submission gives no proof. A short repair is available.

For an even polynomial, the constraints are `p_e^(2j+1)(1)=0`, `0 <= j < r`. If its exact degree is `2m` with `1 <= m <= r`, the constraint `j=m-1` isolates the leading coefficient through the nonzero derivative of `x^(2m)`, so that coefficient must vanish.

For an odd polynomial, the constraints are

\[
p_o^{(2j+1)}(1)-p_o^{(2j)}(1)=0.
\]

If its exact degree is `2m+1` with `1 <= m <= r`, the constraint `j=m-1` isolates the leading coefficient: on `x^(2m+1)` the difference is `(2m+1)!/3`, on `x^(2m-1)` it is zero, and all lower odd monomials vanish under those derivatives. Thus no degree from `2` through `2r+1` occurs.

Conversely, the `r` even trace functionals have full rank on `span{x^2,x^4,...,x^(2r)}`, and the `r` odd trace functionals have full rank on `span{x^3,x^5,...,x^(2r+1)}`. Hence any even monomial of degree at least `2r+2`, or odd monomial of degree at least `2r+3`, can be corrected by lower monomials without changing its leading term. Constants and affine polynomials supply degrees `0` and `1`.

## Gap list

1. `Section 1, equation (2)`: the exact regularity theorem and power-domain induction are not stated. This is load-bearing but locally repairable.
2. `Final degree-spectrum sentence`: the correct bonus formula is asserted without proof. This is non-load-bearing and locally repairable by the parity-triangular argument above.

No counterexample, sign error, parity omission, quantifier change, completion-interface error, or fatal dependency failure was found.

## Preregistered score

| Axis | Score | Maximum | Reason |
|---|---:|---:|---|
| Correctness and closure | 37 | 40 | All required conclusions are correct; the main domain formula needs its cited regularity step made explicit, and the bonus claim lacks proof. |
| Contract fidelity and completeness | 19 | 20 | All three required questions, both parities, all integer `s >= 4`, and the concrete versus abstract distinction are addressed; one external-theorem hypothesis package is under-stated. |
| Strict progress | 15 | 15 | The response closes all required claims and adds two correct refinements: constrained-polynomial density and the exact degree spectrum. |
| Calibration | 10 | 10 | It clearly separates algebraic from spectral inverse, equality from unitary equivalence, and literal basis density from density after boundary cancellations. |
| Evidence and citations | 8 | 10 | The proof is largely self-contained and states the crucial Legendre endpoint formula, but the power-domain regularity citation is generic and no source locator is supplied. |
| Reproducibility | 5 | 5 | Every algebraic identity and boundary test needed for replay is present in the two frozen inputs. |
| Total | 94 | 100 | Acceptance thresholds are met. |

Threshold check: total `94 >= 70`, correctness `37 >= 32`, and there is no fatal category.

## Structured conclusion

- Verdict: `REPAIRABLE_GAP`.
- First load-bearing error: unsupported regularity and recursion step at equation (2), not a false statement.
- Fatal category: none.
- Required claims: accepted after local proof-detail repair.
- Bonus constrained-polynomial density: correct and adequately sketched.
- Bonus exact degree spectrum: correct but requires the omitted parity-triangular proof.
- Scored-metric treatment: this neutral review's usage is excluded.

## Integrity

The output hashes below are canonical SHA256 values. Canonicalization replaces the two output-hash values in both files by the literal placeholders shown here before hashing UTF-8 bytes. This avoids the impossible requirement that a file contain its own byte-exact SHA256 fixed point.

- review_md_canonical_sha256: `59E8E49AA52AFB167540F630CBBC22A30BD05767936E6EC89A4C23128C2F9B0C`
- verdict_json_canonical_sha256: `ACDB5BDE125C1B673F6F61FC4EF5796B8B84CF505272B4C634199BBD4876A281`
