# Final report

Run: R-20260823T000000Z-o1p-baseline
Status label: RIGOROUS_PARTIAL_RESULT
Source: PROBLEM-O1P-GENERAL.md (round 3 baseline)

## Exact theorem or result proved

1. **New STRICT abstract theorem (band-invertible H).** Let H be a real
   Hilbert space with orthonormal basis (e_k) and monomials x^k = A e_k,
   where A is a bounded invertible operator and the Gram matrix is banded.
   Then for finite polynomial representers,
   `closure(span Q_sp) = V <=> ker(T|_{B_fin}) = {0}`. This is a structure
   theorem showing where the H_beta/H_lambda criteria extend.

2. **New STRICT concrete family (stable banded shifts).** Let m >= 1,
   lambda = (lambda_1,...,lambda_m) in R^m, and let
   H = H_shift(m,lambda) be the real l^2 space with monomials
   `x^k = e_k + sum_s lambda_s e_{k+s}`. If
   `L(z)=1+sum_s lambda_s z^s` has no zeros in the closed unit disk, then:
   - Pi is dense in H and the moment map J is a bounded invertible
     Toeplitz operator;
   - for any finite-degree polynomial representers v_j, the kept set N is
     cofinite;
   - `closure(span Q_sp) = V <=> ker(T|_{B_fin}) = {0}`, where T is the
     finite matrix whose columns are the finite-run membership vectors.
   This generalizes the m=1 H_lambda closure to all bandwidths and gives a
   finite linear-algebra decision procedure on that family.

3. **New STRICT concrete bandwidth-2 example.** In H_shift(2,lambda) with
   stable lambda and `v_1 = x^4`, the sparse family is never dense in
   V = ker M_4. The obstruction is the moment sequence `delta_2`.

## Proof or construction

- `candidate_proof.md` contains Lemma 0.1 (stable Toeplitz invertibility),
  Theorem 1.1 (cofinite kept set), Theorem 2.1 (finite-rank criterion),
  Theorem 3.1/3.2 (regressions), and Theorem 4.1 (bandwidth-2 example).
- The proof uses only: master criterion, run lemma (pure linearity), bounded
  invertible moment map, and finite linear algebra.

## Verification performed

- Internal adversarial self-audit: no first error found in the treated family.
- Scripts checked kept-set/run behavior for m=1 (matches H_lambda) and m=2
  (N, thresholds, delta_2 obstruction). These are EVIDENCE, not proof.
- No independent fresh audit was possible due "do not spawn nested subagents"
  instruction. See `audit_report.md` for the non-independent UNCERTAIN verdict.

## Remaining gaps

- General O1' remains OPEN: arbitrary non-diagonal H, arbitrary banded Gram
  without stable Toeplitz inverse, weighted L^2, infinite-degree/non-polynomial
  representers.
- The new criterion does not solve the general moment-representability core.
- Lean scaffold only; no machine-checked proof of the new theorem.
  Tier-0 compile was attempted but timed out on Mathlib warm-up; the scaffold
  has not been build-verified.

## Failed and blocked routes

- General banded Gram (non-Toeplitz) route: BLOCKED, because bandedness alone
  does not imply an invertible/closed-range moment map.
- Weighted L^2 / general H moment-problem route: BLOCKED.
- External literature hunt: no exact source found (degraded search).

## Novelty status

- POTENTIALLY_NEW within this project. The ingredients are standard, but the
  exact finite-rank criterion for stable banded-shift H is not a direct
  corollary of the cited literature found.

## Human/model/tool contributions

- User provided the benchmark problem and required context.
- This run was performed directly by the agent (no nested subagents).
- Project code/scripts written in this run are in `reproducibility/`.

## Reproducibility manifest (summary)

- Python 3.14.4, numpy 2.5.2, sympy 1.14.0.
- Scripts:
  - `reproducibility/banded_shift_verify.py`
  - `reproducibility/audit_banded_shift.py`
- Commands:
  - `python3 reproducibility/banded_shift_verify.py`
  - `python3 reproducibility/audit_banded_shift.py`
- Repo HEAD at run start: `e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f`.
- No commit made.

## Confidence by axis

- Semantic fidelity: high for the stated subclass; not general O1'.
- Mathematical correctness: high for the internal proof; independent audit not
  yet performed.
- Completeness: partial (subclass solved, general open).
- Novelty: likely new, but literature check was low-yield.
- Reproducibility: scripts are deterministic and simple.
