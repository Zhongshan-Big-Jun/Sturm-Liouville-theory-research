# O-2026-SL-NGE2-2NSWITCH-9A3F2B: Exact 2n effective switches of gap extremizers n>=2 (box class)

- **Source wording**: docs/SL_spectral_topics_summary.tex open problem 1 (minimal block
  number / exact switch count, n>=2); docs/SL_gap_extremals.tex (session 13).
- **Formulation**: -y'' = lambda rho y, y(0)=y(1)=0, 1<=rho<=R a.e., n >= 2,
  D_n = lambda_{n+1} - lambda_n. Prove: every global maximizer and every global minimizer
  of D_n has, after merging adjacent equal-valued blocks, exactly 2n effective internal
  switches; maximizer starts and ends with 1 ([1,R,...,1]), minimizer starts and ends with
  R ([R,1,...,R]). No uniqueness or reflection symmetry assumed.
- **Previously known**: session 13 numerical evidence; "at most 2n switches" (finite block
  reduction, solved 2026-08-10); exact count was open.
- **Management state**: SOLVED (2026-08-10).
- **Proof package**: user-provided SL_gap_nge2_exact_2n_switches_proof_zh.pdf (2026-08),
  faithfully transcribed to docs/SL_gap_nge2_exact_2n_switches_proof.tex/.pdf (16 pages,
  zero warnings). Frozen English proof: runs/R-20260809T125847Z-exact2n-switch/artifacts/full_proof.md
  (SHA-256 9d4d8de8c18064717c8c7e2c913cdc1b914d086845a87cc55f34facdc0e0e5a9).
- **Audit (2026-08-10)**: analytic line-by-line PASS (Wronskian sign, exact zero formula
  #Z = 2n-2 + 1{q0>c} + 1{q1<-c}, complete box saturation, zero=switch equality, block
  energy invariant K = -2D with interface jump (r+ - r-)F, endpoint rigidity q0>1, q1<-1);
  numeric scripts/audit_nge2_pdfs.py Part B 16/16 (n=1..8 SUP/INF at R=4: exactly 2n zeros,
  q0>1, q1<-1, K+2D~0) + Part A 40/40, mpmath 50 digits, smooth weights 4/4.
- **Literature**: no published theorem with all of (all n>=2, full measurable box, both
  max/min ends, every extremizer, exact 2n switches) found; Willner-Mahar 1979 flagged as
  explicit prior-work risk; Sun 2022 covers only the first-gap minimization (INF side, n=1,
  piecewise-continuous bounded-jump weights); no novelty claim.
- **Still open (per summary item 1)**: switch positions/block lengths, reflection symmetry,
  uniqueness/classification, closed form or sharp bounds of max D_n / min D_n, asymptotics,
  stability, generalizations.
