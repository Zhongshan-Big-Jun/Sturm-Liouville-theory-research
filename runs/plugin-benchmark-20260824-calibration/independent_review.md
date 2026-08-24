# Independent neutral mathematical review

Reviewer subagent: `a07f955a-0665-4c24-955d-ce77fd5ab166`
Date: 2026-08-24
Method: fresh neutral subagent, anonymized candidates 1..5, no arm labels supplied in the review prompt.
Mapping: 1=our-plugin, 2=blank, 3=rethlas, 4=danus, 5=mmat.

## Candidate 1 (our-plugin) — PASS (HIGH)

The proof is faithful to the frozen claim: no quantifiers are altered and the required audits are explicitly covered. The matrix reduction is correct: `C_s = B_R B_1`, `det C_s = 1`, and Cayley–Hamilton plus the Chebyshev recurrence correctly yield `G_{n,s}(y) = sin(y)[U_n(z) + s^{-1}U_{n-1}(z)]`. The root-count lemma is rigorous: it uses sign changes at `θ_k = kπ/(n+1)` and a separate epsilon-tail argument, producing `n` distinct roots in `(-1,1)`; degree `n` then forces exactly `n` simple roots. The passage to `y` correctly handles the two-to-one `z`-mapping, excludes `y = π/2`, and verifies simplicity via `G' = sin(y) P'(z) z'(y) ≠ 0`. Repair hints: none.

## Candidate 2 (blank) — PASS (HIGH)

The statement matches the frozen theorem exactly. The derivation of the central identity is sound, and the polynomial extension is correctly justified as an even polynomial of degree `2n`. The root-count lemma uses the monotone-phase argument `Φ(θ)=nθ+arg(e^{iθ}+ε)`, which is valid for `0<ε<1`; the derivative of the phase is strictly positive, so `Φ` crosses each `kπ` exactly once for `k=1,…,n`, giving `n` simple roots in `(-1,1)`. The return to `y` correctly uses the two-to-one map via `T(z)=βz-α/2`, verifies no zero at `y=π/2`, and preserves simplicity because `T'(y)≠0` at roots. All required boundary audits are present. Repair hints: none.

## Candidate 3 (rethlas) — PASS (HIGH)

The candidate proves the exact statement for all `n≥1`, `R>1`. The algebraic reduction is correct and matches the required form `Q_{n,s}(x)=U_n(z)+s^{-1}U_{n-1}(z)`. Its root-count lemma is valid: using nodes `θ_k=kπ/n` (where `sin(nθ)=0`), the signs of `h` alternate between the small-`ε` sample and `h(π-ε)`, producing `n` disjoint sign changes and hence `n` distinct roots; degree `n` then yields exactly `n` simple roots. The hyperbolic lemma for `z<-1` is correct and, although redundant after the degree argument, correctly excludes extra roots. The transfer through `x∈(0,1)` and evenness gives exactly `2n` simple roots in `(-1,1)`, and the boundary audits are correct. Repair hints: none.

## Candidate 4 (danus) — PASS (HIGH)

The theorem statement is faithful, and the matrix factorization `M=(ES)^nE` is algebraically correct. The polynomial reduction yields the same exact Chebyshev identity, with a correct leading coefficient `α^n` for the degree-`2n` polynomial. The root analysis is rigorous: in the hyperbolic region `P<-1` the bracket is strictly positive, and in the elliptic region the monotone phase argument gives exactly one root for each `k=1,…,n` in `(δ,1)`, with evenness giving the negative counterpart. The statement `Q_n(δ)≠0` is true (`F(-1)=(-1)^n(n+1-rn)≠0`); even if that line is not fully expanded in the summary, the degree argument already prevents extra boundary roots. Simplicity is properly preserved through `x` and `y`, and all required special cases are checked. Repair hints: optionally add a one-line proof of `Q_n(δ)≠0`; the fact is true and not used as a circular support.

## Candidate 5 (mmat) — REPAIRABLE_GAP (HIGH)

The proof is otherwise complete and correct: the conjugated matrix `D` is computed correctly, Cayley–Hamilton gives `Q_{n,s}(x)=U_n(u)+s^{-1}U_{n-1}(u)`, and the root lemma via sign changes at the zeros of `U_n` is valid for `0<λ≤1`. The two-to-one return to `x` and `y` is handled correctly, and the required audits (including `R=1`) are present. However, the displayed leading-coefficient formula is false: the leading coefficient of `Q_{n,s}` is `2^n α^n`, not `α^n(2^n+2^{n-1}s^{-1})`; the extra term has degree `2n-2` because `U_{n-1}(u)` has degree `n-1` in `u`. The intended conclusion (degree exactly `2n`) remains true, so the gap is repairable and non-fatal.

**Post-review correction applied:** `arms/mmat/result.md` now states the leading coefficient as `2^n alpha^n`.
