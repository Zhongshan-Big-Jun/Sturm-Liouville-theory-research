INDEPENDENTLY_AUDITED_PROOF

# Anonymous posthoc review of Pilot v6 Arm C

## Verdict

`PASS`

The submitted proof closes all three required questions for every `c > 0`, every integer `s >= 4`, and every polynomial index `n >= 0`. I found no load-bearing mathematical error.

First load-bearing error: none.

Acceptance gate: passed. Total score is 97/100, correctness is 39/40, and there is no fatal category.

This review was performed as a first-time blind mathematical audit. Its model and tool usage is excluded from all scored Arm C metrics. I did not inspect repository history, hidden gold, Arms A or B, project documentation, memories, network sources, or scored session traces.

## Frozen contract

The proof was audited against exactly three completion gates:

1. Characterize `Q_n^(s) in D(K_c^(s/2))`.
2. Compare the operator domain with the abstract polynomial completion.
3. Decide density of the `Q_n^(s)` span under the operator-domain reading.

The proof also establishes the bonus degree spectrum. It preserves the quantifiers `c > 0`, integer `s >= 4`, and `n >= 0`, and it does not use numerical evidence.

## Obligation-by-obligation audit

### 1. Form, operator, self-adjointness, and regularity

The identity

`h(u) = integral |u' - (u(1)-u(-1))/2|^2`

has the correct sign and factor. Its nullspace consists exactly of affine functions. The decomposition into mean, affine part, and mean-zero remainder supplies the missing coercivity, so `a_c` is equivalent to the `H^1` norm for every `c > 0`.

The integration-by-parts boundary term is correct for inner products linear in the first argument. The two arbitrary endpoint values in the adjoint calculation force exactly

`v'(1) = v'(-1) = (v(1)-v(-1))/2`.

Thus the displayed `H^2` realization is self-adjoint and bounded below by `c I`. The proof then gives a valid compact-inverse spectral construction and correctly identifies `D(K_c^(1/2)) = H^1` with the form norm.

For `s = 2m + epsilon`, the induction and triangular boundary system correctly yield

`D(K_c^(s/2)) = {f in H^s: b_+(f^(2l)) = b_-(f^(2l)) = 0 for 0 <= l < m}`.

The half-integer regularity step is valid because the leading term of `L^m f` is `(-1)^m f^(2m)` and every lower even derivative already has the needed regularity. The energy norm and `H^s` norm are equivalent on this domain. No boundary condition is omitted in either parity.

### 2. Algebraic polynomial system

On each finite-dimensional polynomial space, `L^m = c^m(1-D^2/c)^m` is triangular with nonzero diagonal. Hence it is bijective and transports lower-degree polynomial spaces onto themselves. The monic orthogonality argument therefore gives

`L^m Q_n^(s) = c^m R_n^(epsilon)`

and the terminating inverse binomial formula. The degree and span conclusions follow.

The frozen task gives the `SL_hs` construction only in shorthand. STEP2 explicitly unpacks that shorthand as the polynomial pullback inner product. Under that stated construction, the derivation is correct. Supplying the original full definition would improve provenance, but the proof does not silently use the genuine boundary-constrained inverse in place of the formal polynomial inverse. STEP7 explicitly separates those maps.

### 3. Reduction and both obstruction arguments

The identity

`L^(m-1) Q_n^(s) = c^(m-1) U_n^(epsilon)`

is algebraically correct. Membership in the high power domain implies `U_n^(epsilon) in D(K_c)` in both the even and odd cases.

For even order, `U-R` has degree at most `n-2`, so `L^2` orthogonality removes the cross term. Pairing `K_c U = cR` with `U` gives

`h(U) + c ||U-R||_2^2 = 0`.

Both terms are nonnegative. Thus `U = R` and `h(U) = 0`, forcing `U` affine and contradicting `n >= 2`.

For odd order, form orthogonality gives `a_c(R,U) = a_c(R,R)`. Hermitian symmetry and `K_c U = cR` then give `a_c(R,R) = c ||R||_2^2`, hence `h(R) = 0`. Again `R` is affine, contradicting `n >= 2`. All signs and conjugations are correct.

For degrees zero and one, `R_0 = 1`, `R_1 = x`, and the inverse differential corrections vanish. Both affine functions satisfy every iterated trace condition. Therefore

`Q_n^(s) in D(K_c^(s/2)) iff n in {0,1}`.

### 4. Abstract completion and completion map

The map

`J_s p = K_c^(-m) L^m p`

uses the genuine bounded inverse only after the formal polynomial image has been formed. It satisfies `K_c^m J_s p = L^m p`. This proves isometry for even `s` into `L^2` and for odd `s` into the `H^1` form space. Surjectivity after completion follows from density of polynomials in `L^2` and `H^1` and from `L^m P = P`.

The word `unitary` is correct for the energy norm explicitly adopted in equations (8) and (9). With the conventional additive graph norm, the same map is a bounded Hilbert-space isomorphism rather than literally an isometry; the norms are equivalent because `K_c >= c I`. This normalization point does not change equality, completion, or density.

The identity realization cannot identify the two completions because `x^2` belongs to the dense algebraic polynomial copy but violates the original Krein boundary condition and hence is not in any required operator domain. Thus the proof correctly distinguishes nonidentity unitary equivalence from identity-based equality.

### 5. Polynomial graph core and density

The trace map from `H^s` to `C^(2m)` is continuous. The Hermite endpoint-jet construction gives a genuine polynomial right inverse: the source and target dimensions are both `4m`, and a polynomial in the kernel would be divisible by a degree `4m` polynomial. Correcting arbitrary `H^s` polynomial approximants by this right inverse produces boundary-compatible polynomial approximants.

Consequently `P intersect D(K_c^(s/2))` is dense in the operator domain in the energy norm and hence in the equivalent graph norm.

The proof then separates all natural readings of the span question correctly:

- the literal full span equals `P` and is not contained in the domain;
- the span of individually admissible members is `span{1,x}` and is not dense;
- the intersection of the full span with the domain is a dense polynomial graph core.

The witness `(1-x^2)^(2m)` satisfies every required endpoint jet and proves that the affine subspace is proper. The positive-distance argument uses only finite-dimensional closedness and is valid.

## Definition, logic, boundary, and adversarial audits

- Definition audit: passed. The formal differential inverse, genuine operator inverse, abstract completion, identity realization, and domain intersection are kept distinct.
- Logic audit: passed. Both parity branches are complete, and no implication is reversed.
- Boundary audit: passed. The cases `n = 0,1`, `n >= 2`, even and odd `s`, all `c > 0`, and all iterated endpoint conditions are covered.
- Adversarial audit: passed. The weakest points, namely half-power regularity, STEP2 transport, both zero-energy identities, the completion map, and trace correction, survive direct checking.

Critical errors: none.

Repairable mathematical gaps: none.

Non-load-bearing editorial observations:

1. The unavailable offline-status citation is unnecessary and should be removed, but it supports no mathematical inference.
2. The target norm for the word `unitary` should continue to be called the energy norm to avoid confusion with the additive graph norm.
3. A full source definition of the named `SL_hs` polynomial construction would make STEP2 independently reproducible beyond the frozen shorthand.

## Preregistered score

| Axis | Score | Reason |
|---|---:|---|
| Correctness and closure | 39/40 | All load-bearing claims check out. One point is reserved for the terse source-definition interface in STEP2. |
| Contract fidelity and completeness | 19/20 | All three gates and the bonus spectrum are closed; all natural density readings are distinguished. |
| Strict progress | 15/15 | The proof gives a full exact classification, completion map, and graph-core theorem. |
| Calibration | 10/10 | It distinguishes equality, unitary equivalence, literal span, admissible subsystem, and domain intersection. |
| Evidence and citations | 9/10 | The mathematics is self-contained; the sole status citation is unavailable but non-load-bearing. |
| Reproducibility | 5/5 | The proof is symbolic, parameter-uniform, and contains explicit formulas and constructions. |
| Total | 97/100 | Acceptance threshold passed. |

## QED self-verification comparison

This section was written only after the independent verdict above was fixed.

QED structural verification passed statement integrity, completeness, originality, decomposition adherence, and all key-step structural checks. It returned overall failure solely because the relative file `related_info/related_work.md` was unavailable, so the nonmathematical offline-status citation could not be verified. The regulator classified this as a proof-execution and documentation problem and recommended deleting that citation without changing the mathematical proof.

The later failure analysis records missing verification evidence for later internal attempts and flags STEP2 definition identification as a risk. It does not exhibit a counterexample, a false equation, or a failed mathematical implication in the submitted `proof.md`. Therefore the QED system-level `FAILED` status is separate from, and does not overturn, this independent mathematical `PASS`.

## Integrity

Input SHA256 values:

- `frozen_task.md`: `359D335803EAE43F45120E3CA3995B8F12EC2F98B357E2B10116EAFE2D8C6332`
- `proof.md`: `DAF055B84E09024F6A653B57ADB771E50B268E1CF9692DAB97C6AB59A7BD9987`
- `structural_verification.md`: `916EA1907955A99C17AB70E9198D25B692E29D8B34A82634A381231A79B117E4`
- `regulator_decision.md`: `0A61A4C640AE037BB158DCE5F08AB635AEA6741B0BFE1F9E80A37D6FB66E8FB0`
- `failure_analysis.md`: `7585D7937B247A32115E303BB2BBBAE0BD2DE33CFC7BDD9A5798C03152D0BB86`

The exact SHA256 of this immutable `review.md` is recorded in `verdict.json`. The exact SHA256 of `verdict.json` cannot be embedded in that file without changing the hashed bytes; it is reported in the external handoff.

