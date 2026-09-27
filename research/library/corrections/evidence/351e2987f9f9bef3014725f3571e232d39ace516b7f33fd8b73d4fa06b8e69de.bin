# R13-11/R13-12 author handoff

AUTHOR_READY_FOR_INDEPENDENT_REVIEW. No review verdict or card release is claimed. Repository base: `4a82d3c2c8c7c3e5f3f027efcf2be3c54a612983`. Edits started from the actual workspace sources, which were clean in the two authorized paths. The original CRLF/LF conventions were preserved. Exact before/after identities are in `source-edits.json`; the two original sources are in `before/`.

## Changed repository paths and locations

| Path | Current source locations | Change |
| --- | --- | --- |
| `docs/SL_spectral_topics_summary.tex` | Date line 18; abstract lines 24-71 | Current fixed-c A1/A12 status, explicit historical reading of old dated progress, and G2 quantifier distinction. |
| Same | Section 2.4, lines 274-346; `rem:cofinite-current` | Preserve H2/H3 proof route, state full member window and exact cofinite closure with critical endpoints, remove the dangling old open-status fragment. No expansion theorem. |
| Same | Lines 380-384, 544-547, 1045-1047 | All three Helly summaries now require uniform bounds/TV, a specified topology, admissible-class sequential closedness and appropriately directed semicontinuity. |
| Same | Section 5.5, lines 802-822 and 869-874 | Conditional global G1'/G2 status and distinct provenance of the all-order cofinite theorem. |
| `docs/SL_stability_moment_jump.tex` | Date line 18; abstract lines 30-32; introduction lines 72-88 | Replace the stale unresolved 3<s<7/2 status; add current A1/A12 pointers and retain the local H3-to-H1 transport and recurrence assumptions. |

The stability source from `\section{一般系数的增长下界与充分性}` to EOF is byte-identical to the starting source. The H1-H3 assumptions, family, recurrence and formal-operator/domain caveat before the edited status paragraph are also byte-identical. Thus all growth inequalities, B=0 model restrictions, full-index hypotheses, perturbation counterexamples and bibliography remain untouched. Static checks are in `source-static-checks.json`; these are not compilation or mathematical certification.

## Mathematical source alignment

- A1: `docs/SL_fractional_left_definite.tex`, `thm:all-thresholds` (243-310), `prop:h4-core` (413-442), `thm:main` and its scope remark (462-516). Each nonaffine named member has nonzero k^-4 spectral leading coefficient, giving the threshold 7/2. The compatible fourth-order core and spectral cutoff supply density below that threshold. This is a reading of the accepted proof, not a new audit of it.
- A12: `docs/SL_cofinite_all_orders.tex`, theorem 1 (71-105), sections 7-9 (727-903), corollary 3 and scope (908-917). The annihilator reduces to central traces. A highest nonzero derivative coefficient at order r is excluded when s<=r+1/2 by the bounded logarithmic Fourier sequence. Consequently the essential retained sets are {}, {0}, {0,1}, {0,1,4} on [0,1/2], (1/2,3/2], (3/2,5/2], (5/2,7/2), respectively. The equality points use fewer traces. Missing active indices impose f(0), f'(0), f''(0), with the exact missing-index codimension. General infinite deletion and uniform c->0 estimates remain separate.
- Local H3 route: `docs/SL_h3_completeness_proof.tex`, lines 51-112 and 245-259. Kc:Hc3->Hc1 is the isometric transport used there; its spectral-cutoff corollary is 0<=s<=3. No stronger norm estimate or perturbation theorem was substituted into that proof.
- Current G2 contract: `docs/SL_gap_nge2_symmetry_local_proof.tex`, `sec:global`, lines 497-552. For fixed n and pattern sigma, the framework needs every zero of F_sigma in Sigma_sigma, a uniform block-width bound for each 1<R<=R_*, and G1' nonzero Jacobian determinant with sign (-1)^n on that same full set.
- Historical G2: the same source, `sec:g2closed` and `thm:g2`, lines 942-1008. Its historical statement is about sign-consistent solutions on [R_0,R_1] with R_0>1; its proof uses band matching. The text explicitly withholds recertification and the bridge to the full Sigma_sigma. The near-R=1 control is a second quantifier distinction. No historical run or theorem body was altered.

## Helly candidate and direct proof

`helly-compactness-candidate.md` contains the proposed complete card body, selection derivation, topology/closedness conditions, a fixed-Dirichlet spectral continuity argument and the supplied counterexample. The input was read from the actual Round 13 REPORT, analytic_notes and both source_notes files. No supplied source excerpt was installed over current workspace files.

The counterexample is preserved with exactly its original class: continuous nondecreasing densities in [1,R], rho(0)=1 and rho(1)=R, R>1. Strict positivity of the first eigenfunction yields lambda1(rho)>pi^2/R for every admissible rho. The admissible ramps rho_k=1+(R-1)min(kx,1) have test-function mass loss at most (R-1)pi^2/(12k^3), since the rescaled polynomial integral is 1/3-1/4=1/12. Their eigenvalues tend to pi^2/R. The pointwise limit is discontinuous at zero; its L1 class has no admissible continuous representative. Thus the infimum is not attained. This is an author derivation, not an independent review.

The measurable box uses a distinct valid argument: weak-star sequential compactness, box closedness and fixed-index spectral continuity. The actual source is `docs/SL_gap_nge2_finite_reduction_proof.tex`, `lem:wscompact`, `lem:wscont`, `cor:attain`, lines 322-425. No withdrawal is proposed. The old precise Keller Section 2 attribution was not verified in original literature; the candidate makes no such claim and supplies its own derivation.

## Exact caller and binding impact for the coordinator

| Caller/reference | Impact and minimal action |
| --- | --- |
| `tools/bang-bang.md:12` | Direct [[helly-compactness]] caller. Replace the existence bridge with existence for the actual closed class/topology; for the complete measurable box cite the weak-star proof above. The index currently declares no dependencies, so text callers must also be tracked. This task does not re-audit its separate bang-bang claims. |
| `tools/keller-variational.md:12-18` | Named downstream application in the old Helly card, but no reverse Helly link was found in this card. No blanket structural retraction. Existence must be justified for its specified positive box; the spectral continuity argument covers fixed ratios there. |
| `docs/SL_ratio_summary.tex:456` | Another glossary sentence says Helly is used for existence. It is outside this author's write set. If the coordinator changes it, qualify with class closedness and objective continuity and add that root to the compilation list. No edit was made here. |
| `tools/jump-stability.md:2,62,66` | Explicit whole-file source hash is now stale. Its mathematical body already states the full member window and needs no theorem expansion. Update source identity and obtain the required scope-specific renewal via the original API. |
| `tools/left-definite-theory.md:20`, `tools/krein-sobolev-polynomials.md:25`, `tools/morales-ramis-kovacic.md:22`, `tools/switch-saturation-k-invariant.md:59` | Text references to the overview. Their respective mathematical claims were not changed here. Check current summary/source/review bindings after integration. |
| `research_map.md:23,39,59-60`, `PROJECT.md:20`, `docs/research-guide.md:43,53`, `state/RESUME.md:157` | Current overview/stability entry points or legacy dated pointers. Minimal state wording is proposed below. |
| `tools/README.md:114`, `index/tools.json` | Derived Helly entry/summary must come from the corrected card through the original API, rather than retaining the inherited unconditional summary. |

The read-only stored-release inventory found **17 release obligations across 9 current card hashes** whose latest stored release for its issue binds both changed TeX files. Both hashes matched this author's pre-edit sources in every case. Exact issue, revision, release-request and review-bundle identities are in `binding-impact.json`. This is an inventory, not an API validity verdict; the coordinator must resolve live supersession and reuse state through the original API.

| Card | Stored obligations |
| --- | --- |
| `spectral-domain-checks` | 1 |
| `left-definite-theory` | 2 |
| `moment-jump-completeness` | 2 |
| `left-definite-moment-recurrence` | 2 |
| `denseness-criteria` | 2 |
| `krein-sobolev-polynomials` | 3 |
| `jump-stability` | 3 |
| `cot-series-certificate` | 1 |
| `delta-bracketing` | 1 |

Renew the affected bindings against final integrated sources; do not edit old receipts. Helly's new correction obligation is separate from those 17 stored obligations. No card, index, release or reviewer identity was written by this author.

## Proposed minimal shared-file corrections, not applied

1. `research_map.md`: retain A1/A12 as accepted with their existing formulas and scopes. Update the entry-point note at line 23 to say the overview now reflects A1/A12 and the G2 quantifier distinction. Keep A5/B4 PARTIAL. Refine B4's line 56 note and edge at line 97 to read: "G1' on the full zero set and G2 for all zeros uniformly on 1<R<=R_* remain open; the historical sign-consistent, R_0>1 statement does not supply that bridge." In the promotion note at lines 223-224, distinguish B4's matched G1'/G2 contract from B3's separate global-optimum O1/O2 obligations.
2. `literature/maps/FRONTIER.md`: retain the fixed-c full-window row at line 13 and its three critical endpoints. At line 17 replace the short "G2 statement alignment" phrase by "all-zero-set G2, including uniform control as R decreases to 1; historical band matching must be reconciled". Add only a short Round 13 note that Helly attainment requires closed admissibility and correctly directed semicontinuity. Do not promote global G1 or restart A1/A12.
3. `state/RESUME.md`: prepend one current Round 13 paragraph after coordinator integration/review, recording the corrected entry points, the Helly counterexample, measurable-box preservation, binding renewals and pending/completed compilation as actually observed. Keep dated earlier entries, including the old line 157 pointer, as history.
4. `state/current.json`: its last_updated is 2026-08-29, and run_status_verbatim/note/IDs contain historical observations. Preserve those historical fields. If this remains a current entry point, update the live `gap_nge2_symmetry_status` and `next_actions[2:4]` to the exact G1'/G2 scope above; remove the appended current-use "DensBC STRICT theorems A-H" label from `gap_nge2_symmetry_status` and point to A1/A12 plus the corrected general-constraint boundary instead. Use the coordinator's actual run/checkpoint for live pointers, not an invented author ID. The old validate_project.py next-action text is not authorization to run it.
5. `docs/research-guide.md:43`: replace "not yet aligned by definition and quantifier" with the identified distinction above, while continuing to state that the bridge is unproved. `AGENTS.md` and session-log maintenance remain coordinator-owned; a sufficient new entry records the user's exclusive two-source write set, the preserved local proof, the corrected Helly assumptions and the no-compilation/no-commit author boundary.

## Reading versions that need compilation

Only two TeX roots were changed by this author. Compile each final integrated root once, then refresh both existing reading copies from the corresponding build:

- `docs/SL_spectral_topics_summary.pdf` and `docs/build/SL_spectral_topics_summary.pdf` from `docs/SL_spectral_topics_summary.tex`. Inspect the abstract, section 2.4/A12 display, Helly passages and section 5.5/G2/A12 scope.
- `docs/SL_stability_moment_jump.pdf` and `docs/build/SL_stability_moment_jump.pdf` from `docs/SL_stability_moment_jump.tex`. Inspect the abstract/introduction and pagination around the unchanged first theorem.

No PDF was compiled or changed by this author. A1/A12, H2/H3 and G2 underlying proof sources were read only and require no rebuild from this author's changes. Historical lecture PDFs, frozen author files, old receipts/logs and canonical content were not changed. The coordinator's final instruction schedules three affected TeX roots overall; the third root is outside this author's two-file scope. No additional theory work is proposed.

No commit, push, staging, plugin mutation, shared-artifact edit or independent-review dispatch was performed.
