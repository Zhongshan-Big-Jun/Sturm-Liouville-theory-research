# Run whiteboard (Planner memory)

- **Run ID:** `R-20260816T174722Z-min-direction-audit`
- **Task packet ID:** `P-20260816-min-direction-audit`
- **Last updated:** `2026-08-16T18:10:00Z`

## Current plan

Audit collaborator `min_direction_progress.tex`; verify algebraic core; run
independent adversarial audit; decide accept/reject; if accepted, copy to
`docs/`, update README/AGENTS, commit.

## Route history

- symbolic_interface `[SUCCEEDED]`: n=2 mu=2 and general-mu interface formulas satisfy momentum equations; Xi identity verified.
- determinant_parity `[SUCCEEDED]`: random matrix tests pass for n=2..5.
- contraction_n3_mu2 `[SUCCEEDED]`: D_a/kappa_D/kappa_N identities and 0<a<1 verified symbolically and by sampling.
- weak_contrast_algebra `[SUCCEEDED]`: Phi rearrangement and square-completion pass 1000 random numeric checks.
- t0_boundary `[SUCCEEDED]`: derivative and rational inequalities verified.
- four_margin `[SUCCEEDED]`: n=3 identity verified in 10000 random tests under gamma endpoints zero reconstruction.
- compile_check `[SUCCEEDED]`: xelatex produces 43-page PDF.
- numeric_root_scan `[SUCCEEDED]` (EVIDENCE only): no n=2 or n=3, mu=2 roots found in scanned q/R ranges.
- external_blueprint_verification `[BLOCKED]`: E:/ai_auto_solve artifacts absent; Trusted/Arb claims cannot be independently re-verified here.
- adversarial_subagent `[PARTIAL]`: independent audit running; no final report yet.

## Ideas to return to

- Source uses `\kappa_0` and `\kappa_D` without definitions; `\kappa_D` is inferable as D_a=0 threshold, `\kappa_0` as N_b>0 lower bound. Consider adding a documentation note or asking collaborator.
- The n=2 mu=2 theorem may be vacuous for sampled R (no roots found numerically), but the document does not claim existence.

## Open obligations

- Full Bernstein positivity certificate for Q_box and Arb covers are not independently verifiable from provided materials.
- General n>=2 global reflection symmetry remains open; document labels it Open.

## Key artifacts

- `C:/Users/HuangZY/Downloads/min_direction_progress.tex` -- source under audit; sha256 2E2DED0D46AB51DFA94D1605C72FEC106AD25CAB31E078E660C82B1F1933CF0C
- `problem_contract.md` -- contract for this audit; sha256 F4EA53C9D249DCF46B555FB08C60693C7C740E97775DE1D8D4F53A6CB7421565
- `research_ledger.md` -- chronological audit log; sha256 5BB064805D72F9CC271EB95B62AD7B21356190C7EA1BFFB66A32ECFEB80CF878
- `whiteboard.md` -- this file; sha256 84FA7F816351C981BE03A600EFD8F8E621B2CF49A0A41F11C19A2492A8CCCFAE
- `reproducibility/verify_algebra.py` -- interface/determinant checks
- `reproducibility/verify_contraction.py` -- contraction algebra checks
- `reproducibility/verify_weak_contrast_num.py` -- weak-contrast numeric checks
- `reproducibility/verify_kappaD.py` -- kappa_D identity
- `reproducibility/search_mu2_n3_coarse.py` -- n=3 mu=2 numeric scan
- `reproducibility/search_mu2_n2.py` -- n=2 mu=2 numeric scan
