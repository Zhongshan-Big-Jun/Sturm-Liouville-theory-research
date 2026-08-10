# Repro manifest (audit run) - hashes added

## Task and inputs

- Task packet: agenda/task-packets/Q-20260806-o1-audit-422A69.md
  sha256: ae049c58794a55cb0c39e6d500ce029a8b7656565aab3dbc286a65937a6ad273
  (matches manager run-manifest.json)
- Audit target: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md
  sha256: c647297430348618a5120a3eae5fad09003b25eafb9c8a8ccd9f449d1b397341
  (read-only; NOT modified)
- Obligation list: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md
  sha256: 62998c6e8066aac9e6676fd0b78288830439e964330f7b84e404a604e7adc7b2
- Draft problem contract: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/problem_contract.md
  sha256: 0fcd9f94293c7847342f4bdd7be2b8b2f517d32f6e7d41536ab7409aecdbf779
- Draft research ledger: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/research_ledger.md
  sha256: 23a2d882e93a4b2373cd85a1d8c1629c1c33affa1facb65891f3f67645e8a9c3
- Portfolio problem: agenda/problems/O-2026-SL-GAP-3B7A2C.md

## Primary sources used (local copies, read-only)

| Source | File | sha256 | Version | Role in audit |
|---|---|---|---|---|
| Ahrami-El Allali-Harrell | papers/fundamental_gap.txt | 2f3c90e6127c8a13356236ca8dba87e7a86ff8be62856c4fad3a89137b0c3d14 | arXiv:2407.02459v2, 3 Jul 2024 (file header) | Lemma 2.1 (FH), Lemma 2.2 (monotonicity) |
| Keller 1976 | papers/keller1976.txt | 7eeab2777926c4ba5ed3c3806647b4d8a9a9750ad75a5b0bb2a77653f422ef3c | SIAM J. Appl. Math. 31(3) 1976, 485-491 | relevance check only |
| Mahar-Willner 1976 | papers/mw1976.txt | 0dcd8172baa80ece55dc64804dc709279c6c56da83fe470122644f63332c7b01 | CPAM 29 1976, 517-529 | relevance check only |
| Cheng-Kung-Law-Lian 2010 | papers/cheng2010.txt | not hashed here | CAMWA 60 2010, 2556-2563 | relevance check only |
| Ashbaugh-Benguria 1989 | papers/ab93.pdf | scan, no text layer | listed in draft contract | not a premise of O1 |

All txt sources are OCR with occasional glyph corruption; every statement quoted
in the audit was re-checked against the mathematical content of the file.

## Tool-library leads (NOT treated as verified premises)

- tools/gap-n1-reduction.md (provenance UPSTREAM_AUDITED pending this audit;
  contains the same sign convention as the draft and inherits the O1b sign-error
  finding; flag noted in audit_report.md)
- tools/feynman-hellmann.md, tools/bang-bang.md (context only)

## Environment

- OS: Windows, PowerShell 7; cwd F:\LaTeX\BVE research
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  (numpy 2.2.6, scipy 1.15.3 per packet; scripts use numpy only)
- No formal prover used; no internet sources fetched during this audit run.

## Audit scripts and outputs (reproducibility/)

- verify_o1_audit.py (vectorized transfer-matrix solver; O1c structure, O1b sign
  at single jumps and symmetric family, u*/D* reproduction, 1200-config random
  search, L1-continuity spot check) -> verify_o1_audit_out.json
- verify_o1_audit2.py (boundary cases: rho=1, rho=R, 2-block, a=b; O1c on
  5-block configs) -> verify_o1_audit2_out.json
- verify_o1_audit3.py (corrected local bang-bang direction test) ->
  verify_o1_audit3_out.json
- dbg1..dbg9.py (intermediate diagnostics; superseded by the three scripts above)
- Random seeds: 20260806 (audit1), 4242 (audit2); all other randomness none.
- Numerics are EVIDENCE ONLY; every proof-level claim is argued in audit_report.md.

## Known unknowns

- Exact version header of O1_reduction_draft.md (dated 2026-08-05 per draft-run
  manifest; no in-file version).
- model field unknown (manager run-manifest.json records model: null).
- Whether the draft authors intended a different Hilbert-space convention for
  the operator T_rho in Lemma 1 is unknown; the audit gives a corrected statement.
