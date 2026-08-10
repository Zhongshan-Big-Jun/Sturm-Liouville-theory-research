# Reproducibility manifest - independent re-audit of O1 Lemma 1 and Lemma 3

Run: R-20260806T151000Z-o1reaudit-5A1C3D.  All files ASCII punctuation,
UTF-8 no BOM.  Unknown fields are marked null; nothing is invented.

## Inputs (sha256)

| Item | Path | sha256 |
|---|---|---|
| Task packet | agenda/task-packets/Q-20260806-o1-reaudit-5A1C3D.md | 323097EEFDD4F06D886C1D146CBA941CF5AAB20F2D38D4E303C74DBA429C4FD7 |
| Revised O1 candidate (audit target) | runs/rigorous-open-math-research/R-20260806T140000Z-o1revise-2ED02A/candidate_proof.md | 728BD2B8D9F3AA9249B2E2A701006461AABC8154B18F47586A35677417254404 |
| Producer self-audit (rechecked, not trusted) | runs/rigorous-open-math-research/R-20260806T140000Z-o1revise-2ED02A/audit_report.md | F7AB2963AFACFAD332F77E9D43F6021DD9ACC1F534C22D1E60A2A820BE9B5F6B |
| Prior independent audit | runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md | E6D1688963184DCBB87EC71EF8DB3B095A322D8B10D229CF8547ADB198B162CA |
| Repair-list candidate (422A69) | runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/candidate_proof.md | 7DF07F84810788BC2AF5E5F718AB019AB731B26F19B98CD35008CEB0B53B4C06 |
| O1 draft | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md | C647297430348618A5120A3EAE5FAD09003B25EAFB9C8A8CCD9F449D1B397341 |
| AEH (premise) | papers/fundamental_gap.txt | 2F3C90E6127C8A13356236CA8DBA87E7A86FF8BE62856C4FAD3A89137B0C3D14 |
| Keller 1976 (context) | papers/keller1976.txt | 7EEAB2777926C4BA5ED3C3806647B4D8A9A9750AD75A5B0BB2A77653F422EF3C |
| Mahar-Willner 1976 (context) | papers/mw1976.txt | 0DCD8172BAA80ECE55DC64804DC709279C6C56DA83FE470122644F63332C7B01 |

## Outputs (this run)

| Item | Path | sha256 |
|---|---|---|
| Audit report (deliverable) | audit_report.md | 9E249962B9F6D4C6A1EFE88B84702EC89D9150D5C794F078D999743C10B4DCAC |
| Problem contract | problem_contract.md | 740C302EA2FC57A890B16024EB3DD90B45F7B0A78D45D6A941F4094CA11FB446 |
| Obligation graph | obligation_graph.md | 23F6B77A2C48779107662AE19A0DB882818DE03284A6418A0563F1401826A008 |
| Approach registry | approach_registry.md | CF18A74B07791A867C1469534FB81145291A58FE9959951F93D8D6A7C2E3E1F8 |
| Research ledger | research_ledger.md | 150B56D8C4E9BB9BB6FF94ADEA407BF99AFF4B7D7F9A0860DF9B9E29C7E5599F |
| Counterexample log | counterexample_log.md | 120C48DF4DA11F764C29B2DA794124291D81035A2E0674C0A5E27AABDB4C2959 |
| Status and literature | status_and_literature.md | 54B38FBC531BC79C38B660A3A90E7AE281EC65E068BF28FA1DE4798D40896F27 |
| Candidate proof (audited-artifact reference) | candidate_proof.md | 67F7339C5EBE5BF782709BE4183D32B92BF524591F6F167411B90FB733642305 |

## Environment

- Python 3.10.11 (C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe)
- numpy 2.2.6, scipy 1.15.3
- OS: Windows; PowerShell 7 for file I/O (UTF-8 no BOM via
  [System.IO.File]::WriteAllText with UTF8Encoding(false))
- Model: null (not recorded)
- No formal theorem prover used; numeric checks are evidence only.

## Reproducibility commands

Run from this directory (reproducibility/):

  python verify_hs_weyl_independent.py
  python verify_fh_sign_independent.py
  python verify_smoothing_dirac_independent.py
  python verify_aeh_pointwise_independent.py

Seeds: verify_hs_weyl_independent.py uses numpy default_rng(20260806);
the other three scripts use deterministic configurations only.

## Scripts and recorded outputs (reproducibility/)

- fd_lib.py - finite-difference solver (written from scratch; HS/Weyl checks)
- tm_lib.py - exact transfer-matrix solver (written from scratch; FH checks)
- verify_hs_weyl_independent.py -> verify_hs_weyl_independent_out.json
- verify_fh_sign_independent.py -> verify_fh_sign_independent_out.json
- verify_smoothing_dirac_independent.py -> verify_smoothing_dirac_independent_out.json
- verify_aeh_pointwise_independent.py -> verify_aeh_pointwise_independent_out.json
