# Reuse Summary (light reuse-gate, round 3)

## Existing tools/results actually reused

- `research_map.md`: route map and status of A3/A4/B3.
- `tools/README.md` and `tools/constrained-denseness-runs.md`:
  master criterion (Theorem A), theorem E, run/free-base vocabulary.
- `tools/denseness-criteria.md`, `tools/moment-jump-completeness.md`:
  moment/run algebra context.
- `lean-proof/LEMMA_INDEX.md`: recognized the DensBC/O1 scaffold declarations;
  no Lean re-proof was needed for this run (formalization not attempted).
- Prior run artifacts:
  - `R-20260816T000000Z-densbc-o1/candidate_proof.md`: Theorem 3 run ratios,
    O1' reduced core, Theorem 5 structural warning.
  - `R-20260816T210000Z-densbc-o1p/candidate_proof.md`: H_beta criterion,
    definitions of B, rho_b, B_adm.
  - `R-20260816T220000Z-densbc-o1p2/candidate_proof.md`: H_lambda criterion,
    moment-map/isomorphism argument that inspired H_{beta,lambda}.

## Duplicate work avoided

- Re-proving the master criterion (density iff V cap Q_sp^perp = {0}).
- Re-deriving the run/free-base/rho machinery; this was reused as a lemma.
- Re-litigating F-densbc-01 corrected ratio.
- Re-proving the H_beta and H_lambda closed cases; they are regressions here.

## Duplicate work that still happened

- Some low-level re-derivation of the cofinite threshold for a new family
  (Theorem 1), though it is a minor variant of the bandwidth-1 threshold.
- Re-deriving the explicit v_1 = x^4 singleton-obstruction example for the
  new family; this is a small but genuinely new computation.
- Re-reading substantial portions of prior candidate proofs despite the
  light pre-scan instruction, because the exact rho/admissibility definitions
  were needed to build the new theorem.  This was targeted, not full-read.

## New tools/methods created

- The weighted shift family H_{beta,lambda} with the moment map
  J = D_beta + lambda B and its realizability lemma for run vectors.
- The criterion ker(T|_{B_adm})={0} with B_adm depending on beta > 3/2,
  unifying H_beta and H_lambda.
- No new external tool file was added to `tools/`, because the new method is
  captured in this run's candidate_proof.md and could be promoted later.
- Late visibility of the parallel baseline run was noted after this run was
  written: the baseline's Toeplitz H_shift(m,lambda) and this run's weighted
  H_{beta,lambda} are complementary, not duplicates.

## One-line assessment

The lightweight pre-scan was worth its cost: it identified the reusable
run/free-base machinery quickly, and the only extra cost was a few targeted
reads of prior proofs to recover exact definitions that were not fully in the
compact summaries.
