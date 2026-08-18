# Whiteboard: DensBC O1'

- **Run ID:** `R-20260816T210000Z-densbc-o1p`
- **Task packet ID:** `Q-20260816-densbc-o1p-F6E7D8A9`

## Current plan
Close O1' on the structured subclass H_beta with finite-degree polynomial
representers.  Use the finite run/free-base system from upstream, reduce
realizability to (a) a finite matrix kernel condition and (b) the summability
threshold beta > 3/2 for infinite runs.  Then give an explicit non-coordinate
example.

## Route history
- `dk-solver` `[SUCCEEDED]` : dispatched solver subagent 3eae582d for the
  structured-case attack (whiteboard/ledger/candidate_proof deliverables).
- `H_beta finite-polynomial subclass` `[SUCCEEDED]`: cofinite kept set, finite
  run system, finite free-base set B.
- `moment parameterization` `[SUCCEEDED]`: V cap Q_sp^\perp <-> (Tt=0, finite
  weighted l^2 norm); exact realizability step.
- `main decision criterion` `[SUCCEEDED]`: density iff ker(T|_{B_adm}) = {0}.
- `coordinate regression` `[SUCCEEDED]`: recovers Theorem E exactly.
- `non-coordinate example` `[SUCCEEDED]`: v_1 = x^4 + alpha x^6 (alpha real
  nonzero) gives finite free-base obstruction for every beta.
- `independent audit` `[SUCCEEDED]`: core PASS; REPAIRABLE_GAP on conjugation
  convention, example alpha, and minor rigor points; all repaired.
- `general O1'` `[PARTIAL]`: remains open for non-diagonal H and infinite
  representer data; not attempted.

## Ideas to return to
- Banded non-diagonal H: replace diagonal H_beta by an infinite banded Gram
  matrix with bounded inverse; decide whether moment-realization becomes a
  finite/truncation problem.
- Extend the finite free-base matrix criterion to "representer moments finitely
  supported" in non-diagonal H with a summability model.

## Open obligations
- General O1': decide free-base realizability in arbitrary H.
- O2/O3 inherited upstream: still open.

## Key artifacts
- problem_contract: runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/problem_contract.md
- candidate_proof: runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/candidate_proof.md
- audit_report: runs/rigorous-open-math-research/R-20260816T210000Z-densbc-o1p/audit_report.md
