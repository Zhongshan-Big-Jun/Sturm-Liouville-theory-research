# O-2026-SL-GAP-3B7A2C: Adjacent gap extremals n=1 (box class)

- **Source wording**: docs/SL_spectral_topics_summary.tex open problem 3; docs/SL_gap_extremals.tex.
- **Formulation**: -y'' = lambda rho y, y(0)=y(1)=0, 1<=rho<=R pointwise a.e. Find sup and inf of lambda_2 - lambda_1.
- **Conjecture (numerical)**: SUP attained by symmetric 3-block [1,R,1] (jumps u*, 1-u*); INF by symmetric [R,1,R]. R=4: SUP u*=0.45148546584 D*=32.613983618; INF u*=0.382598257 D*=6.784482339.
- **Known partial results**: FH variational formula + bang-bang (proved in SL_gap_extremals.tex Prop 2.1/Cor 2.2); AEH Lemma 2.2 transfer gives single-interval {f>0} -> 3-block structure (to be written up); symmetric-family critical point via single zero-crossing of f_sym (numerical, unproved).
- **Management state**: DELEGATED (task Q-20260805-gapn1-proof-9F31D0).
- **Latest literature check**: 2026-08-05; no direct result for box class found (Sun 2022 covers bounded-jumps class, full text unavailable).

- **2026-08-09 update**: O3a/C1 SOLVED. The PDF proof O3a_complete_proof_zh.pdf (phase-ratio rigidity) was audited (scripts/audit_o3a_pdf_part1..4.py all pass; independent large-R re-verification) and integrated: docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf (15 pages, zero warnings); SL_gap_n1_proof.tex section 5 and SL_spectral_topics_summary.tex updated. Sup/Inf of lambda_2-lambda_1 over the box class now fully established for n=1 (O1/O2/O3a/O3b all closed). Remaining: symmetry of all extremal configs, minimal block number, n>=2 global extremality (open problems in the summary).
