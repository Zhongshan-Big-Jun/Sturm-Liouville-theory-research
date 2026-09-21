# R6-C01 fractional-window author handoff

Status: AUTHOR SUBMISSION. Ready for coordinator source freeze, PDF build and fresh independent review. This is not an approval or independent review receipt.

## Authorized scope and source identity

- Baseline HEAD: `92d46e99e36cc0a74e8f7bb13430749c222ee54f`.
- The only repository file written by this author is `docs/SL_fractional_left_definite.tex`.
- Current source SHA256: `30261aaca9a4ebd2688bd24b61509250de6795da55d9b69a5840d197de00e186`.
- Original source SHA256: `95ef1c87bb4b0598f5314ad96153ec97d86611d6c59e561d648028d226c1c6a4`. The preserved before-TeX has this exact identity.
- R5 input, `docs/SL_cofinite_left_definite.tex`, remains `ed07e47fd370a9db3b6a6a2d125d9eec996288e53a6024a0e9fb533ca1b3c0bb`.
- Submitted candidate, `research/artifacts/proof-audit-round6-20260921/submitted/fractional_window_completion.md`, remains `51ae8ab0a0548c67f39303e0e5fe480bcbea9e8557cdf2603461163a233a9b38`.
- Historical A7 body actually read, `runs/three-arm-pilot-v2/pilot-v6-hs-domain/arms/c-qed/output/proof.md`, remains `daf055b84e09024f6a653b57adb771e50b268e1cf9692dab97c6ab59a7bd9987`.
- Original byte counts and hashes are in `input_identity.json`; final source and evidence identities are in `source_identity.json`.

The assignment limits this author to the current TeX and external `fractional-author/` area. Root AGENTS was read, but the later explicit assignment controls the write scope. No agent was spawned, no commit/push was performed, and no tool library, canonical, old run, old review packet, AGENTS or navigation file was written by this author. The coordinator explicitly owns PDF compilation and final review.

## Mathematical contract and completed argument

For every fixed real `c>0`, on the specified complex Krein operator domain and full original index set `{0,1} union {4,5,...}`:

1. Every named nonaffine `p_n` belongs to `H_c^s`, for `s>=0`, exactly when `s<7/2`. The affine members `1,x` belong to all nonnegative domains.
2. The full original family is dense in `H_c^s` for every `0<=s<7/2`.
3. At `s>=7/2`, the full family is not a subset of the target space. Selecting individually admissible named members leaves only `1,x`, whose span is not dense.
4. Compatible finite combinations remain possible. In particular, `p6-(7/2)p4=x^6-5x^4+7x^2` has all four traces zero and belongs to `D(K_c^2)`. The high-order admissible named subsystem and the domain intersection of the algebraic span are different spaces.

The proof in the current TeX contains:

- Operator foundation: energy positivity, explicit hyperbolic correction proving surjectivity, a direct adjoint argument, an explicit ordinary H2 bound and compactness of the inverse.
- Full spectrum: compact self-adjoint spectral theorem, exhaustive even/odd ODE classification, the two-dimensional eigenvalue `c`, exclusion of other roots, normalized sine factors and branch signs. Completeness is not inferred merely from finding eigenpairs.
- Membership: two integrations by parts for every fixed polynomial on both spectral branches; division by the eigenvalue for every boundary-compatible polynomial gives `O(k^-4)` for all original members.
- Sharpness: `p_(2m)'''(1)=4m(4m-5)` and `p_(2m+1)'''(1)-p_(2m+1)''(1)=4m(4m-3)` hold and are positive for every integer `m>=2`. Repeating the integration identities gives nonzero `k^-4` terms with `O(k^-6)` remainders. Sine normalization changes `sin(mu_k)` exactly to `(-1)^k`. The endpoint is harmonic-series divergence.
- Core: finite leading-degree elimination gives `span{p_n}=C[x] intersect D(K_c)`. The product domain is ordinary H4 with `Bf=B(f'')=0`. The actual matrix on `x2,x3,x4,x5` has determinant `15360`. A fixed bounded polynomial right inverse corrects the traces after approximating the fourth derivative in L2 and integrating four times.
- Transport: convergence in `||K_c^2 . ||_2`, followed by spectral cutoff and the fixed-c bound `||u||_s <= c^((s-4)/2)||u||_4`. All individual members belong to the target only below `7/2`. This is not upward transmission from H3 density.

The negative-order completion, exact p4/x2 diagnostic proposition and proof, conditional growth lemma and proof, and numerical-limit discussion were preserved. Their text-preservation checks are recorded. A concrete algebraic-inverse versus genuine-operator-inverse example was added. Historical H3 density remains a separate lower-order route, not a premise of the new full-window proof.

The operator and four-trace core argument uses the standard compact self-adjoint spectral theorem, Arzela-Ascoli, L2 density of continuous functions and Weierstrass. It does not invoke the refuted abstract projection claim. It does not establish arbitrary constrained-space density, arbitrary deletions, stable/Riesz bases, uniform-in-c bounds, or a new negative-order density theorem. Coefficient constants are allowed to depend on the fixed polynomial.

## Actual source reading and provenance

- R5-OP was read including the energy estimate, explicit surjectivity matrix, norm control and adjoint proof.
- The H2 source's boundary checks and triangular algebraic spanning proof were read.
- The H3 source's domain/transport, moment recurrence, growth estimate, main proof and low-order transmission were read as historical context, without certifying its whole historical program.
- The algebraic-span paragraph in `docs/SL_denseness_criteria.tex` was read and rechecked after the concurrent current-file drift.
- A7 STEP1 and the actual STEP7 polynomial-approximation and STEP8 trace-correction arguments were read. The present article reproves only the needed fourth-order case, with the specific four-by-four matrix.
- The withdrawn high-order article's correction and formal-inverse issue were read; its obsolete theorem is not used.
- The external candidate and relevant audit report were read as evidence, not instructions.
- Official MDPI retrieval first returned HTTP 429. A subsequent primary-domain web result exposed Section 2, equations (7)-(9), giving the same spectrum and affine modes. This is a limited background comparison, not a claim to have downloaded/read the whole paper. [Primary source](https://www.mdpi.com/2075-1680/14/2/115).
- Earlier memory was used only to locate historical repair context and avoid overstating its scope. Current mathematical facts were rederived from actual sources.

## Executed checks and retained failures

Runtime: Python 3.14.4, SymPy 1.14.0.

1. `git diff --check -- docs/SL_fractional_left_definite.tex` returned exit 0.
2. First author run, `python3 focused_checks.py --output focused_checks_normal.json`, failed after 52 passing checks. Check 53 required all bytes of coordinator-owned `docs/SL_denseness_criteria.tex` to remain unchanged. The actual failed result is preserved in `focused_checks_normal.json`; its exact script is preserved as `focused_checks_failed_v1.py`. This was an integrity-check failure, not a mathematical counterexample.
3. The criteria source changed from `27709f093d02654570031c51ba382337bc0b964696fad17826dddc1c8f211246` to `8dba318c2722ed77b18995f388065795c5a4c8cc070bb63b7200317d5108eac7`. The visible diff changed range/status prose. The cited algebra paragraph remained byte-identical, SHA256 `52b5c617806637858dd4a1a59a347e471857731db4a43de2f1e1e4055cc4ed39`. This author did not write that file. `dependency_drift.json` records the observation.
   The coordinator subsequently confirmed that these were exactly three authorized dated range-status sentences, with no algebra/proof changes, and that the old criteria TeX/PDF bytes were archived under `research/artifacts/proof-audit-round6-20260921/before/docs/`. The drift and failed-run evidence remain intact; no revert was made.
4. The corrected integrity scope enforces complete byte preservation for the frozen candidate/audit, preserved before-TeX/PDF, R5 and historical A7. It observes current coordinator-owned documents without claiming authority to freeze them, and explicitly checks the cited criteria algebra paragraph.
5. Second author run, `python3 focused_checks.py --output focused_checks_normal_v2.json`, returned exit 0 with 55 named checks. Its source SHA256 matches the handoff source above. The result separates symbolic all-index identities, exact finite calculations and static/integrity checks. No floating-point computation is used.
6. No author `python -O` run or replay of the submitted 21-check suite was performed. The coordinator separately reported normal/-O replay of those 21 submitted checks; that is not represented here as this author's execution.
7. Earlier editing/tool failures are retained as facts:
   - The initial lookup under `research/runs/three-arm-pilot-v2/...` failed with `No such file or directory`. The actual body was found under `runs/three-arm-pilot-v2/...`.
   - A large apply_patch failed with `Failed to find expected lines` because of a mismatched Chinese character in its old-text context. SHA256 immediately afterward confirmed the original source was still unchanged.
   - An inline Python edit failed at parsing with `IndentationError: unexpected indent`, because a triple-single-quoted raw string met third-derivative apostrophes. No source write executed. Saving `revision_main.texpart` and inserting it with a short separate script succeeded.
   - A later notes-writing functions.exec call failed at JavaScript parsing with `SyntaxError: Invalid or unexpected token`, due to Markdown backticks in a raw template literal. Its tools did not execute; the notes were then written with apply_patch.

`revision_main.texpart` is an intermediate working fragment, including a negative-completion placeholder. It is not the final source and must not be used as the frozen review target.

The checks establish boundary identities, normalization factors, exact low-degree integrals, the trace matrix/right inverse, the cancellation example, integration-kernel constants and limited document/integrity properties. They do not certify compactness, all-index asymptotics, convergence/divergence or infinite-dimensional density. Those are analytic proof obligations in the article.

## Remaining gaps and handoff

No remaining analytic gap in the stated fixed-c candidate was identified in this author's derivation. This is an author assessment, not independent acceptance.

Not performed here: TeX/PDF build, rendered-page inspection, Lean formalization, final stateless independent review, full historical-proof audit, full repository integrity audit, canonical integration, library updates, AGENTS/navigation updates, commit or push. The coordinator owns the build and review. Full byte preservation was checked only for the named protected subset; concurrent changes elsewhere remain coordinator-owned.

Files produced by this author:

- Repository: `docs/SL_fractional_left_definite.tex`.
- External `fractional-author/`: `AUTHOR_NOTES.md`, `input_identity.json`, `source_identity.json`, `revision_main.texpart`, `focused_checks.py`, `focused_checks_failed_v1.py`, `focused_checks_normal.json`, `focused_checks_normal_v2.json`, `dependency_drift.json`.

Freeze the current repository TeX at the SHA256 above. Do not substitute the intermediate fragment or interpret an author-check status as independent approval.
