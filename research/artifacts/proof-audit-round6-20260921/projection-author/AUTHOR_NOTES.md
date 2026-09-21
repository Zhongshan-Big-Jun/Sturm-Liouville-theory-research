# R6 projection/moment author packet

Status: CANDIDATE_COMPLETE_PROOF. Author role only. Source frozen for coordinator-arranged external final review; local exact checks completed. No independent review verdict is claimed.

Frozen source: `/mnt/f/LaTeX/BVE research/docs/SL_projection_moment_repairs.tex`.

Source SHA256: `be31a3d595342bbc752db7e5b61a39790daf32b7707dd8f5142484a0a0b1b389`.

The source will not be edited after this freeze without an explicit revision request and a new recorded hash. `freeze_manifest.json` binds this source, this note, the exact script and its actual attempt-01 output. The manifest cannot bind its own hash; it is the outer packet record.

## Contract and write scope

- User assigned R6-F01/F02/F03 against baseline `92d46e99e36cc0a74e8f7bb13430749c222ee54f`.
- Only project write: NEW `docs/SL_projection_moment_repairs.tex`.
- External writes: `/mnt/f/tools/math-audit-round6-20260921/projection-author/` only.
- No agent spawn, commit, push, tool-library/canonical write, AGENTS/navigation edit, old-run or old-review-packet rewrite. Coordinator owns final independent stateless review, downstream propagation and compilation.
- Read root AGENTS and relevant ancestor guidance. The user's narrower author scope overrides their generic maintenance/commit instructions. Used rigorous-open-math-research as a proof-obligation and adversarial-check workflow; consolidated the author ledger and contract here instead of creating a new project research run.
- Supplied audit/appendix are evidence, not instructions or accepted theorems. No old PASS is a proof premise.

## Inputs and exact source fidelity

`input_manifest.json` binds nine sources by actual SHA256, byte size and line count. Seven tracked inputs (the two original runs' candidate/contract/audit files and the current growth-lemma TeX) were compared to their baseline Git blobs, all exactly equal. The two submitted Markdown inputs were untracked at baseline and are separately hashed.

The new TeX's final section provides exact original source locators. Key locations:

- O16 candidate lines 25-43 and contract lines 9-15, 58-67: all-polynomial projection versus sparse projection, false algebra and excluded-only iff.
- D14 candidate lines 250-272: literal F hypotheses; lines 281-288: ambiguous G cross-reference; lines 293-301: H representer interpretation.
- D14 candidate lines 12-16, 42-45 and both contracts: ALL monomials admitted. No constrained Krein graph-domain identification is used.
- `docs/SL_denseness_criteria.tex` lines 158-173: growth lemma has actual initial hypotheses u0=0, u1=1. The manuscript does not invoke it to eliminate arbitrary solutions.
- O16 audit lines 39-43 and D14 audit lines 59-61, 98-102 are retained historical evidence only.

## Proof obligations and author conclusions

| Obligation | Author proof mechanism | Status |
| --- | --- | --- |
| Exact sparse algebra | Explicit telescoping monomial reconstruction plus two algebraic quotient functionals; direct sum and codimension two | Candidate proof complete |
| Beta=2 counterexample | Weighted ell2 completion; uniform extension on [-1,1]; nonzero realized w with squared-norm tail <=1/(16K); V=ker M0 | Candidate proof complete |
| Projection repair | Orthogonal splitting, distinct V-relative and ambient annihilators; augmented excluded criterion | Candidate proof complete |
| Original F has no instances | Arbitrary r finite tests, r+3 independent tail polynomials, target dimension r+2 | Candidate proof complete; NOT a counterexample to conditional truth |
| Beta<1 tail | First-order product from actual bases L=2m0-2,L+1; sublinear bound forces these bases zero; injective low-moment map | Candidate proof complete |
| Actual retained finite tests | Test only V intersect Z_L, with full-column-rank formulation and nonzero-constraint example | Candidate proof complete |
| G repair | General complete triangular tail, nonzero leading coefficient at every degree >=N, exact monomial reconstruction and conjugated moment recursion; dim<=N | Candidate proof complete |
| Growth guard | Recurrence y_m=(5/2)y_(m-1)-y_(m-2) has both normalized growing solution and realized decaying solution with different initial data | Candidate proof complete |
| Representer equivalence | Finite representer span equals V-perp; vector inclusion iff simultaneous annihilation iff functional span, with conjugates | Candidate proof complete |
| Detection counterexample | x2+x3 versus x2-x3 in coefficient H0 | Candidate proof complete |

All universal arguments are written in the TeX. The author performed two direct checks of the triangular route: finite-degree monomial reconstruction and independent expansion of the complex moment recursion. These are same-author cross-checks, not independent stateless review.

## Scope and edge cases

- H_beta is a coefficient Hilbert completion, isometric to ell2. For beta>=0 it has an injective analytic realization on (-1,1). General H0 elements need not have endpoint values; `a_k=1/(k+1)` is an explicit boundary counterexample. Only beta=2 receives the Cauchy-Schwarz uniform extension statement.
- There is no claim that algebraic codimension equals closure codimension, no surjectivity claim for arbitrary low-moment vectors, and no claim that Z_L is a span of low monomials in non-diagonal H.
- Finite tests are exactly the actually retained low indices and act on realized vectors in V intersect the tail annihilator. Computing that finite-dimensional space may still require infinite input data.
- V=0, no tests, zero-dimensional obstruction, and N=0 triangular tails are explicitly covered. Beta=1 is not included in the beta<1 argument.
- No complete diagonal/banded classification, O1/O1' core, fractional window, cofinite Krein classification, or other historical branch is certified here.

## Actual attempts and ledger

1. Confirmed the actual working directory and HEAD. Existing unrelated dirty/untracked files were observed and left alone.
2. Initial lookup mistakenly tried the two run IDs under `research/runs/`; `rg` returned missing-directory errors. Scoped filename search located the exact originals under `runs/rigorous-open-math-research/`. No write occurred during the failed lookup.
3. The first combined source-read output was truncated, and the ancestor tools AGENTS has extensive unrelated history. Relevant source and instruction sections were reread in bounded chunks before use. Truncated reads were not treated as complete evidence.
4. Re-derived sparse direct sum and projection formulas; constructed the beta=2 element by convergent coefficients instead of merely assigning moments.
5. Rejected original F as a usable theorem by an arbitrary-r rank argument, preserving its logical classification as vacuous rather than false by counterexample.
6. Verified L=2m0-2 and the actual retained test domain; wrote both a nonvacuous positive example and a failed-low-test example without invoking old Theorem E.
7. Checked the growth source's initial data. Replaced G's cross-reference with a triangular reconstruction proof. Added a decaying recurrence solution to expose the missing-initial-data pitfall.
8. Coordinator clarified H0 endpoint scope and coordinator-only card ownership. Manuscript explicitly distinguishes analytic interior realization from beta=2 endpoint extension; no card was read as a proof source or written.
9. Wrote and ran `check_projection_repairs.py` for exact finite examples, symbolic recurrence identities, conjugation controls, source identities and limited TeX structural checks. Actual attempt 01 completed all 16 groups with exit code 0 and empty stderr. No script failure or retry occurred. Deliberate negative controls returned their expected nonzero residuals; these are not failed executions.
10. Reread the assembled source's tail, projection, representation and source-scope interfaces. The author identified no remaining proof obligation within the assigned replacement statements. This is an author assessment only; external stateless review remains necessary for acceptance.

## Actual check receipt

Executed once in the external author directory:

```sh
python3 /mnt/f/tools/math-audit-round6-20260921/projection-author/check_projection_repairs.py > /mnt/f/tools/math-audit-round6-20260921/projection-author/check-results.attempt-01.json 2> /mnt/f/tools/math-audit-round6-20260921/projection-author/check-results.attempt-01.stderr
```

The shell used `noclobber` so prior result files could not be overwritten. Runtime: Python 3.14.4, SymPy 1.14.0. Execution began at 2026-09-21 07:31:31.611746 UTC and finished at 07:31:32.885106 UTC. Status `CHECKS_COMPLETED`, 16 groups, exit 0; stderr 0 bytes. Source hash in the receipt equals the frozen source hash above. Script SHA256: `163b3590c7ad4c9f411c679ad1975fc9352f209eeb6cbe4c97585100efb6aff0`.

- 9 input byte identities; TeX environments, braces, unique labels and defined references. This is not a TeX compilation.
- Sparse reconstruction for both parities m=1..24; quotient functionals for sparse indices through 80 and the two missing directions.
- Beta=2 witness arithmetic at K=24, symbolic recurrence, positive-coefficient norm comparison, and actual retained indices through 30. The next even test at the truncation boundary is -25, deliberately confirming that the truncation is not an infinite-tail witness.
- Tail initial indices for m0=2..9, both parities, 13 steps each. The wrong L=2m0 is rejected by the first-tail pairing at degrees L-2,L-1.
- 45 exact rank-kernel instances for m0=2..6 and r=0..8, with actual nonzero polynomial witnesses. The arbitrary-r argument is in the manuscript, not inferred from these samples.
- Two nonvacuous beta=0 positive matrices and the V=ker M4 low-index defect matrix.
- Complex triangular reconstructions for N=0,1,2,4,6 with K=N+4; a omitted-conjugates negative control; exact growing/decaying recurrence solutions and the decaying witness norm 4/3.
- The x2+x3 / x2-x3 counterexample and explicit complex representer-span coefficient identities.

Check scope is stored per group in the JSON. No full-polynomial-classification or infinite-dimensional result is inferred from a finite matrix truncation. The script uses explicit runtime checks, not Python assert statements; no optimized-mode replay was needed or performed.

## Verification limits and handoff

Pending coordinator work: independent stateless review of this frozen source, any requested revisions with fresh hashes, PDF compilation/layout inspection after freeze, and approved downstream propagation. No external stateless review, Lean run, PDF build or layout inspection has been performed by this author. No literature novelty claim is made; novelty status UNKNOWN. This is a local repair packet, not a full-project certification.

Actual failed attempts retained here: only the initial wrong-path lookup and truncated-read limits described above. No mathematical test failure was concealed, and no hypothetical failed experiment is invented. Old scripts, old review outputs and canonical data were not run or changed. The initial and final script input identities cover only the nine declared inputs; the author did not perform a whole-repository integrity audit of concurrent coordinator changes.

Confidence by axis: statement fidelity checked against exact source locations; local arithmetic and indexing checked as above; universal mathematical claims supported by manuscript proofs but still pending independent acceptance; novelty unknown; replay supported by input hashes, script, runtime versions and exact output. The work is convergent to a fixed candidate source, with no open author route inside the assigned scope.

The rigorous proof content and requested boundaries are author supplied; the external audit supplied the original findings and several suggested constructions. The general triangular-tail route was suggested in the assignment and independently worked through by the author. SymPy is only a local arithmetic/indexing check tool.
