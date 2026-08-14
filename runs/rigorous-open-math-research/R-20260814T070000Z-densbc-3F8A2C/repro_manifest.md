# Reproducibility Manifest

Run: R-20260814T070000Z-densbc-3F8A2C
Date: 2026-08-14
Project git head at dispatch: 108aa258ef877b88ede886eefacdff96ed52439d

## Environment

- OS: Windows
- Python: C:\\Users\\HuangZY\\AppData\\Local\\Programs\\Python\\Python310\\python.exe
- PYTHONUTF8=1 for all Python invocations
- Libraries: numpy, scipy, sympy, mpmath (declared available)
- LaTeX: xelatex available (not used unless a tex deliverable is produced)

## Source bundle (from task packet Q-20260814-densbc-3F8A2C)

| Item | Path | sha256 (packet) |
|---|---|---|
| Denseness criteria doc | docs/SL_denseness_criteria.tex | E869849444092C148955BE4B3530F7E9A6C27472650CDAE7DC2E29DF910E8671 |
| Tools: denseness-criteria | tools/denseness-criteria.md | 7B136CCC4CBC0502FC66E641655C373CDE13A8989C83D66C9CC1660B21239356 |
| Tools: moment-jump | tools/moment-jump-completeness.md | 01E7AD2CCCC1EDDFC04CF1A87D1D03BB8F46410697EDFC4F481BB35B518CE3CC |
| H^3 completeness proof | docs/SL_h3_completeness_proof.tex | 41E3A8F4289DFA8415A1126348755536C212B3CE4DCDF13617890ED306FB23F0 |
| Baseline Axioms paper | papers/axioms14_115.pdf | D1BCB1759ED6D4FC8E29EDA248A78C646926AD94CA4DCC7E4A13EEA909C2ECC6 |

## Literature leads for B0 (must be fetched with stable links; paywalled labeled)

- arXiv:2101.11968 "Reproducing kernel Hilbert spaces, polynomials and the
  classical moment problem" (Berg / Christensen lead).
- "Density questions in the classical theory of moments", Ann. Inst. Fourier
  31(3) (1981).
- Berg-Thill, "Rotation invariant moment problems" (Zbl 0744.44006).
- J. Approx. Theory 2002, DOI 10.1016/s0021-9045(02)00019-9 ("Approximation by
  polynomials and smooth functions in Sobolev spaces with respect to measures").

## Run artifacts (will be filled as produced)

- problem_contract.md
- research_ledger.md
- approach_registry.md
- obligation_graph.md
- counterexample_log.md
- candidate_proof.md
- status_and_literature.md
- audit_report.md
- run-manifest.json
- reproducibility/*.py (evidence scripts), *.json outputs

## Hash verification of source bundle

All five source-bundle hashes computed on the actual project files MATCH the
packet's declared sha256 exactly (verified 2026-08-14).

## Sparse family definition (authoritative)

From docs/SL_denseness_criteria.tex and tools/denseness-criteria.md:
  p_{2m}   = x^{2m}   - (m/(m-1)) x^{2m-2}   (m >= 2, support {2m, 2m-2})
  p_{2m+1} = x^{2m+1} - (m/(m-1)) x^{2m-1}   (m >= 2, support {2m+1, 2m-1})
Hence for n >= 4, p_n has SUPPORT {n, n-2}.  Skips degrees 2 and 3.

## Evidence scripts and their verified outputs

Located in reproducibility/:
- densbc_v1_verify_free_params.py  -> falsifies the packet example for beta>3/2
- densbc_v2_diagonal_classify.py   -> initial scan
- densbc_v3_diagonal_universal.py  -> beta>3/2 universal non-density, 12 R
  (output captured: densbc_v3_OUTPUT.txt)
- densbc_v4_finite_run_phenomenon.py -> finite-run phenomenon
- densbc_v5_classification_verdict.py -> corrected classification, 11 R
  (output captured: densbc_v5_OUTPUT.txt)
Full reproduction command:
  set PYTHONUTF8=1
  C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe <script>
See run-manifest.json for sha256 of each file.
