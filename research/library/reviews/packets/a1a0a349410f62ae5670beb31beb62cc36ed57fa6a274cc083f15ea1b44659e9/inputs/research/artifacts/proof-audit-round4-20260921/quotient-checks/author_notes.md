# R4-F01 / R4-F05 author repair

Status: CANDIDATE_COMPLETE_PROOF (author work; independent acceptance belongs to the coordinator).

## Contract and scope

The only repository write is `docs/SL_krein_c0_limit.tex`. All local notes, tests and actual outputs stay in this external folder. No canonical writes, commits, pushes, PDF builds, historical proof/review edits, shared AGENTS/card/report/navigation edits, or cached-plugin changes are authorized here. The source was clean at frozen commit `2e9bf3d66fa21a41e16bf779782739ddd9505233`; input hashes are in `repro_manifest.json`.

The mathematical target is the limit as real `c > 0` tends to zero for each fixed integer `n`. Ordinary Sobolev H1 uses the integral of `|f|^2 + |f'|^2`; the quotient uses the degenerate form modulo `W = span{1,x}`. Constants in `O_n(c)` may depend on `n`. No joint `n -> infinity, c -> 0` or uniform-in-n convergence claim is part of this task.

I read the entire original TeX and the submitted audit and constructive repairs. Section A of the submitted repairs is a candidate source, not an instruction or accepted proof. Its low-mode counterexamples and the incorrect O(1) remainder were independently recovered from the defining formulas. The third-round primary excerpt supplies the existing setting/spectral context. The new limit proof needs no new external literature. There is no novelty claim or formalization claim.

## Proof obligations and derivation

1. **Explicit quotient vectors.** Legendre endpoint values give `S_n(1)=S_n(-1)=0`. Integration by parts against degree at most `n-2` and Legendre orthogonality show `S_n'` is proportional to `P_(n-1)`. Comparing leading coefficients gives `S_n'=(2n-1)P_(n-1)`. Consequently the zero-parameter Gram matrix is exactly diagonal, with entries `2(2n-1)`, and the positive-leading-coefficient representatives are `Q_n=S_n/sqrt(2(2n-1))` for every `n>=2`.
2. **Legitimate recurrence remainder.** Put `b_n=(2n+1)/(2n-3)` and `delta_n=a_n-a_(n-2)`. The recurrence gives `delta_(n+2)=(4n^2-1)a_n/c+b_n delta_n`, with `delta_2=delta_3=0`. Both parity chains satisfy `a_n>=a_(n-2)>=1`. Thus `a_(n+2)=(4n^2-1)a_n/c+R_n`, where `a_n<=R_n<= (1+b_n)a_n`. This is `O_n(a_n)`, not `O(1)`.
3. **Parity induction.** For `n=2m+epsilon`, `epsilon in {0,1}`, `m>=1`, set `r_n=m-1` and `C_n=product_(j=1)^(m-1) [4(2j+epsilon)^2-1]`. The empty product is one. Starting at `a_2=a_3=1`, the previous relative estimate proves `a_n=C_n c^(-r_n)(1+O_n(c))` for every fixed n. Hence `||K_n||_(1,c)^2 = 2(2n-1)C_n^2 c^(-2r_n)(1+O_n(c))`, with divergence exactly for `n>=4`.
4. **High-mode representatives.** The finite expansion `K_(2m+epsilon)=P_epsilon+sum_(j=1)^m a_(2j+epsilon)S_(2j+epsilon)` shows `K_(n-2)/a_n=O_n(c)` in ordinary H1 for `m>=2`: each coefficient ratio is `O_n(c^(m-j))`, and the affine coefficient is `O_n(c^(m-1))`. Also `||K_n||_(1,c)/a_n -> sqrt(2(2n-1))`, with an `O_n(c)` error. These two estimates prove the full H1 limit `u_hat_n -> Q_n` for each fixed `n>=4`.
5. **Low-mode representatives and quotient.** For n=2 and n=3 the actual H1 limits are `P_2/sqrt(6)` and `P_3/sqrt(10)`, differing from `Q_2,Q_3` by `1/sqrt(6), x/sqrt(10)`. Their squared H1 distances from `Q_2,Q_3` tend to `1/3,4/15`. The quotient map is continuous, and these differences are in W; hence `[u_hat_n] -> [Q_n]` for every fixed `n>=2`. The existing third-round proof of quotient completeness is preserved verbatim.

## Verification boundaries

The general statements are justified by the displayed all-index arguments. Executable tests are finite consistency and regression checks only. The author does not supply an independent-review verdict. No Lean execution, PDF build or audit of the rest of the project is performed.

## Completed changes

- Added `lem:explicit-q`, proving the derivative identity and the diagonal Gram formula instead of inferring nonsingularity from finite dimensions tested on a computer.
- Replaced `thm:high` with the positive parity-chain induction, explicit `C_n`, exact legitimate remainder bounds, squared-norm asymptotics and the exact n=4 norm.
- Replaced `thm:unit` with the actual ordinary Sobolev limits for n=2,3 and all fixed n>=4, including the finite-sum `O_n(c)` norm bound. The quotient convergence holds for all fixed n>=2.
- Updated the abstract, correction remark, verification status and check section. Removed obsolete claims that finite checks proved general convergence or that uniform Gram nonsingularity remained open.
- Corrected adjacent claims in the old numerical section: the n=4 norm at c=1/1000, the n=5 growth exponent (the same c^-2 squared-norm order as n=4), and the projection coefficient (a limit, not an exact constant at positive c).
- Preserved the setting and the entire third-round radical/isometry/completeness proof, the defining recurrence and norm identity, the low-mode theorem/proof, the spectral remark, glossary, bibliography, BOM, LF endings and original trailing newlines.

## Actual checks and outputs

Run from this scratch folder:

```sh
python3 check_repairs.py > check_output.txt 2>&1
```

Final exit code: 0. Final result: **274/274 PASS**, comprising **260 exact mathematical checks** and **14 preservation/TeX-structure checks**. Python 3.14.4 and SymPy 1.14.0 were used. The detailed machine-readable results are in `check_results.json`; the actual stdout/stderr is in `check_output.txt`.

The exact mathematical checks include endpoint/derivative identities for n=2..14, every entry of the zero-form Gram matrix through N=12, parity leading exponents/constants through n=24, recurrence remainder identities through n=22, direct monomial-integral verification of the shifted Gram/norm formula for 0<=m<=n<=10, and leading representative/remainder orders through n=16. They also include both low-mode Sobolev counterexamples, their zero quotient discrepancies, the old O(1) and exact-projection errors as negative controls, the exact n=4 value, and sample polynomial elimination/radical checks. These are checks at finitely many indices; the proofs for arbitrary fixed n are the induction and estimates in the TeX.

`git diff --check -- docs/SL_krein_c0_limit.tex` returned exit code 0 with empty output, recorded in `diff-check-output.txt`. The source checks verified all protected blocks exactly and checked unique/resolved labels, balanced environments, braces and inline math delimiters. These structural checks do not constitute a TeX compilation or a PDF layout check.

The first run passed every mathematical check but detected that the patch utility had removed three original trailing blank lines. Both failed preservation checks and the original run output are retained in `first-run-check_results.json` and `first-run-check_output.txt`. Restoring the original five newline bytes at EOF fixed those checks. A subsequent wording-only clarification in the abstract distinguishes squared norms from polynomials; the final source was checked again and all 274 checks passed.

## Handoff

The only edited repository file is `docs/SL_krein_c0_limit.tex`. Its final SHA-256 is:

```text
bf56125edd8bcc635893b6f9a1a81a232d82d22f6a9620171a4a4b9014e50b87
```

`SL_krein_c0_limit.ready.tex` is an identical external handoff copy. `SL_krein_c0_limit.before.tex` retains the frozen original, and `changes.diff` records the exact patch against the frozen Git baseline. `repro_manifest.json` binds the inputs, final source, actual commands and scope. No commit, push, canonical write, PDF build, Lean run or other assigned-file edit was made by this author.

No mathematical gap was found by the author's final reread within the stated fixed-index repair. Independent acceptance, PDF construction/layout inspection, any uniform-in-n or joint-limit theorem, and auditing unrelated project material remain outside this author's result. No independent-review verdict is asserted. The coordinator should use a fresh isolated reviewer for acceptance and maintain the shared AGENTS/report/card/navigation records.
