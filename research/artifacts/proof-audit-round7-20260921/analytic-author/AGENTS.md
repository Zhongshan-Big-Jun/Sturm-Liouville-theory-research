# Round 7 analytic author

## Scope and method

- This directory is the only permitted write location. Main repository: `/mnt/f/LaTeX/BVE research`, read only. No commit or push.
- Read the main AGENTS.md, the complete `docs/SL_gap_nge2_symmetry_local_proof.tex`, and the supplied `proof_audit_round7_20260921.md`. Treat report assertions as unverified until derived here.
- Do not consult old review verdicts or memory. `spectral_repairs.md` and the report's `checks.py` were not supplied and have not been read.
- Produce the complete revised TeX and `change-notes.md`. Algebra and test outputs support an author candidate, not independent approval or full formal verification.
- Derive the uniform endpoint lemma for all measurable boxed densities; distinguish halfwidth from full width in the minmax construction. Following the user's second message, repair the listed later Hessian/G2 local errors in place and mark historical whole-G2 claims as unrecertified. Old source preservation is the coordinator's responsibility.
- Use Chinese TeX prose and English punctuation. Keep source hashes, local validation, and remaining risks in the change notes.

## Conversation and maintenance

2026-09-21: User assigned the seventh-round analytic-author role, specifically requested F01/F02/F03 repairs, exact n=2 algebra, full-block sign isolation, and a complete minmax limit proof. The final coordinator supplies independent review. User restricted writes to this directory and prohibited repository changes and commits.

Initial read: complete 763-line source and 167-line input report read. Main source SHA-256: `151c7ec65a67789a043b01a46f6c87c40e6827e9994be9fb4be88a45da0c0aaa`. Wronskian/endpoint errors confirmed by direct identities. Exact determinant coefficient independently computed as `7030400000/4782969`. Direct conflicts in the retained later source will be identified without treating its historical STRICT labels as current approval.

2026-09-21 follow-up: User inspected the candidate diff and authorized minimal in-place tail repairs: remove determinant/definiteness equivalence, restore the missing lambda factor, mark conflicting SUP numerics for recomputation, replace the invalid Cauchy step with the Wronskian short proof, and use only positivity for the fixed limiting spectral gap. Historical whole-G2 labels and the claim that only G1 remains must be unrecertified. TeX date/abstract must use `第七轮范围修订; 验收见版本绑定报告`. No review verdict is requested or produced.

Maintenance: Complete revised source and local regeneration/check scripts are in this directory. `prepare_candidate.py` applies F01-F03 and the initial scope note; `revise_tail.py` applies the authorized follow-up repairs. Run them in that order when deliberately regenerating, then `verify_author.py`. All main-source edits remain prohibited. Mathematical scope, exact changes, validation and final hashes are recorded in `change-notes.md` and `SHA256SUMS`.

2026-09-21 wording clarification: User specified that `diag(1,1,-1,-1)` only defeats the general linear-algebra inference, with no demonstrated realizability in this SL K family. Final prose must say the original equivalence lacks a special spectral-structure/inertia argument, not claim a model counterexample. Conflicting historical numerical assertions are a joint inference/label issue pending recomputation, not a refutation of either data set without new calculations.

Final maintenance: F01-F03 and the explicitly authorized tail repairs are delivered. 20 local author checks pass; final XeLaTeX build has 15 pages, no overfull boxes or undefined references, with only a bold-italic font substitution warning. Selected pages 5, 9, 11 and 14 were visually inspected. General matrix inference examples are explicitly not claimed as realized SL matrices. Main source and report hashes remain unchanged. See change-notes.md for boundaries and SHA256SUMS for final artifact identity. No review verdict or commit was produced.
