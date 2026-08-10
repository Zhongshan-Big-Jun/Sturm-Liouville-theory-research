# Repro manifest

## Task packet
- Path: agenda/task-packets/Q-20260805-gapn1-proof-9F31D0.md
- Problem record: agenda/problems/O-2026-SL-GAP-3B7A2C.md
- Source docs: docs/SL_gap_extremals.tex (2026-08-05), docs/SL_spectral_topics_summary.tex

## Environment
- OS: Windows, PowerShell
- Python: C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe
  numpy 2.2.6, scipy 1.15.3
- LaTeX: D:\texlive\2024\bin\windows\xelatex.exe (ctexart, xelatex)
- Workdir: F:\LaTeX\BVE research
- Run root: runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/

## Numerical tools used
- scripts/gap_lib.py (lams_fast: transfer-matrix root finder for
  block-constant rho; y_at, norm2 for eigenfunctions; fd_check)
- scripts/_tmp_rscan2.py (3-block self-consistency solver, jumps [a,b])
- New scripts created in this run are listed in research_ledger.md

## Key sources (local copies)
- papers/fundamental_gap.txt = arXiv:2407.02459v2 (AEH 2024), OCR text
- papers/cheng2010.txt = CAMWA 60 (2010) 2556-2563, OCR text
- papers/keller1976.txt = SIAM J. Appl. Math. 31 (1976) 485-491
- papers/mw1976.txt = CPAM 29 (1976) 517-529
- papers/ab93.pdf (scan, no text layer) = JDE 103 (1993) 92-103

## Hashes and timestamps
Hashes are recorded in the project index (index/artifacts.json) at
ingestion time. Numerical outputs below are reproducible with the
listed scripts and seeds.

## Known unknowns
- Sun 2022 (JMAA 516, 126513) full text unavailable (paywalled);
  relevance to the box class is assessed from abstract only.
- All legacy txt sources are OCR with occasional character corruption;
  every cited theorem was rechecked against the mathematical content,
  not the corrupted glyphs.
