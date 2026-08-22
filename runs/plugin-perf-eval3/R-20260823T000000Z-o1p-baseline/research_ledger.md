# Research ledger

Run: R-20260823T000000Z-o1p-baseline
Start: 2026-08-23 (session)
Repo HEAD: e6cf00fe87df93a7c0bc63de840b4aa7cdc2708f
Working tree: dirty at start (many existing modified files); no commit made.

## 2026-08-23T00:00:00Z (approx)

- Extracted a slightly more general abstract structure theorem: if the
  monomial map is bounded invertible and the Gram matrix is banded, then the
  same finite-rank criterion holds (Theorem 2.3 in candidate_proof.md). The
  H_shift family is an instance; this is a stronger new structure theorem.

## 2026-08-23T00:00:00Z (approx)

- Read problem statement and required context (three prior candidate proof
  files, research_map, tools index, relevant tools, LEMMA_INDEX, task packet).
- Loaded `rigorous-open-math-research` skill (SKILL.md + phase references).
- Decided the concrete route: stable banded-shift family H_shift(m,lambda),
  a natural m>=1 generalization of H_lambda.

## Tier 0 probes

- Confirmed run root empty; created artifact directories.
- Wrote `problem_contract.md`.
- Re-read H_lambda and H_beta closures to identify the exact gap: the missing
  piece is a non-diagonal family with bandwidth > 1 and an explicit
  realizability characterization.
- Noted that for the Toeplitz shift family, realizability of a moment
  sequence is exactly `l^2` membership whenever
  `L(z)=1+sum lambda_s z^s` has no zeros in the closed unit disk.

## Tier 1 route development

- Wrote scripts `reproducibility/banded_shift_verify.py` and
  `reproducibility/audit_banded_shift.py`.
- Symbolic computation of Gram for m=2, v_1=x^4:
  `a_2 = lambda_2`, `a_4 = 1+lambda_1^2+lambda_2^2`, `a_0=a_1=0`, and the
  tail is kept from `n > D+m+2 = 8`, i.e. n>=9.
- Found and fixed an off-by-one in the odd sparse recursion in the scripts:
  `p_{2m+1}` uses degree `2m-1`, i.e. index `idx-2`, not `idx-1`.
- Numeric consistency: m=1 v_1=x^4 now reproduces the o1p2 kept set
  `{0,1} union {8,9,10,...}`.
- For m=2 stable lambda values (0.5,0.2), (0.3,-0.2), (0.2,0.3):
  `4 notin N`, and `delta_2` is a finite-support moment obstruction
  (membership M_4=0 and all kept p_n orthogonal). This is EVIDENCE, not the
  proof; the proof is in candidate_proof.md.

## Tier 2: proof assembly

- Wrote `candidate_proof.md` with:
  - Lemma 0.1: J bounded invertible, Pi dense, realizability = `l^2`.
  - Theorem 1.1: kept set cofinite.
  - Theorem 2.1: exact `ker(T|B_fin)={0}` criterion.
  - Theorem 3.1/3.2: regressions to H_lambda and H_0.
  - Theorem 4.1: bandwidth-2 `v_1=x^4` non-dense example.

## Fresh-context convergence check (internal)

- Rebuilding from files: the proof is one coherent route; route A is complete,
  route B/C/D remain blocked. The run is converging to a RIGOROUS_PARTIAL_RESULT.

## Failures / false starts

- Script odd recurrence index off-by-one: fixed.
- Stability check in first script originally used wrong numpy coefficient
  order: fixed.
- No attempt to prove general banded O1' via arbitrary banded Gram; marked
  BLOCKED in approach registry.

## Counterexample log (informal)

- H_shift(2,lambda), v_1=x^4: nonzero obstruction with moment sequence delta_2.
- H_lambda, v_1=x^4 (already known): same obstruction for m=1.
- No counterexample found to the new main theorem.
