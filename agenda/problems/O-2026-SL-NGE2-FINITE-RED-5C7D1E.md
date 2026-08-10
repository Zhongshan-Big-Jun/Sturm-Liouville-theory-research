# O-2026-SL-NGE2-FINITE-RED-5C7D1E: Finite block reduction of gap extremals n>=2 (box class)

- **Source wording**: docs/SL_spectral_topics_summary.tex open problem 1 (n>=2 global
  extremality, minimal block number); docs/SL_gap_extremals.tex (session 13).
- **Formulation**: -y'' = lambda rho y, y(0)=y(1)=0, 1<=rho<=R a.e. (full measurable box,
  no continuity/symmetry/monotonicity assumed), n >= 2, D_n = lambda_{n+1} - lambda_n.
  Prove: max and min of D_n are attained; every global extremizer is bang-bang and has a
  representative constant on at most 2n+1 open intervals (at most 2n switches).
- **Previously known**: session 13 numerical evidence (R=4, n=1..12) that SUP is attained
  by [1,R,1,...,1] and INF by [R,1,R,...,R]; no proof for n>=2.
- **Management state**: SOLVED (2026-08-10).
- **Proof package**: user-provided SL_gap_nge2_finite_reduction_proof_zh.pdf (2026-08-09),
  faithfully transcribed to docs/SL_gap_nge2_finite_reduction_proof.tex/.pdf (15 pages,
  zero warnings). Frozen English proof: runs/R-20260809T080134Z-nge2-gap/artifacts/full_proof.md
  (SHA-256 35cdc88fe84935f08d38a85358b8256743b1bbad11a955e8b58db9f0238d08fd).
- **Audit (2026-08-10)**: analytic line-by-line PASS; numeric scripts/audit_nge2_pdfs.py
  Part A 40/40 + Part B 16/16, scripts/_hp_nge2.py (mpmath 50 digits), scripts/_smooth_nge2.py
  4/4. Literature: no directly equivalent published theorem found; Willner-Mahar 1979
  (JMAA 72(2):730-739) flagged as explicit prior-work risk; no novelty claim.
- **Still open (per summary item 1)**: switch positions/block lengths, reflection symmetry,
  uniqueness/classification, closed form or sharp bounds of max D_n / min D_n, asymptotics,
  stability, generalizations.
