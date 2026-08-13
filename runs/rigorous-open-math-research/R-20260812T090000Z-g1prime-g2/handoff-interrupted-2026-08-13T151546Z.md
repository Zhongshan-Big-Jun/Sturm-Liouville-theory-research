# Interruption handoff record

Run R-20260812T090000Z-g1prime-g2 (stage B, rigorous-open-math-research),
obligation M3 (n=2 symmetric INF branch, large-R asymptotics).  This record is
written because the user asked to submit the current work through the
math-research-workflow handoff protocol; the M3 balance is still open.

```text
- **Run ID:** `R-20260812T090000Z-g1prime-g2`
- **Task packet ID:** `Q-20260812-g1prime-g2`
- **Date:** `2026-08-13T15:15:46Z`
- **Interrupt reason:** `USER_REQUEST` (user requested a workflow handoff submission while M3 is still open)
- **Task state:** `IN_PROGRESS` (upstream status verbatim: RIGOROUS_PARTIAL_RESULT - (G2) CLOSED STRICT (R-204); (G1') STRICT on (1,1+delta) for every n (R-208 anchor); open core [1+delta,infinity); n=2 (I1)/(I2) reduced to (M1) d/dR det Kp_odd, det Ko < 0 + (M2) trace signs + (M3) R->inf asymptotics; M3 NOT closed)
- **Task state:** `IN_PROGRESS`
- **Upstream status verbatim:** `RIGOROUS_PARTIAL_RESULT - (G2) CLOSED STRICT (R-204); (G1') STRICT on (1,1+delta) for every n (R-208 anchor); open core [1+delta,infinity); n=2 (I1)/(I2) reduced to (M1) d/dR det Kp_odd, det Ko < 0 + (M2) trace signs + (M3) R->inf asymptotics; M3 NOT closed`
```

## Completed obligations

Nothing inside the M3 sub-obligation is a complete theorem yet.  The
following are closed subtasks with their honest labels:

- STRICT algebraic lemmas (fully verified against the exact series
  coefficient dict P, no numerics involved):
  - In the ansatz `k2=K*u, k3=K*u+C*u^5, p1=pi/2+A*u^2, p3=pi/4+B*u^2,
    eps=u^3`, the u^5 coefficient of E5 is the hard constant `1/(2*K^2)`:
    it can never vanish at a limit point with finite K.  Hence any solution
    branch requires odd-in-u components; the even-only ansatz is
    structurally impossible.
  - Parity structure: E1 and E2 carry only even powers, E6 only odd powers
    (3,5,7,9), E5 is even up to u^4 and odd from u^5 onward.  Consequently
    `a*K - 2 = O(u^2)` (the u^1 coefficient A_1 = a0*K1 + a1*K0 vanishes
    identically on the branch), and the branch is even in u with forced odd
    corrections.
  - Evidence path: scripts/_gapn2_largeR_Pbuild.py (builds P and caches it),
    scripts/_gapn2_largeR_series.py (raw P coefficients), this handoff.
- EVIDENCE subtask: exact closed 4-equation system re-derived and verified
  to 1e-12 against the spectral engine at R=350 (scripts/_gapn2_largeR_closed.py);
  270-row continuation to R=8.99e4 (scripts/_gapn2_largeR_big.json).
- EVIDENCE subtask: free-exponent fits show primary deviation exponent s ~ 2
  with limits K0 ~ 3.4553, a0 ~ 0.5788, b0 ~ 0.2898, c0 ~ 1.4741
  (scripts/_gapn2_largeR_fit.py, scripts/_gapn2_largeR_sigma_fit.py).
  This retracts the handoff's wrong K -> 2.789 prediction.
- Correction recorded: the previous u^4-even solve residual 2.6e11 is now
  explained structurally (missing odd components), not as a numerical issue.

## Open obligations

- M3 (open, main): establish the exact large-R scaling and leading balance of
  `(k2,k3,p1,p3)`: full integer-power branch `K(u), a(u), b(u), c(u)` through
  at least u^4, including the odd components, with a STRICT derivation from
  E1=E2=E5=E6=0.
- M3 follow-ups (open): leading coefficient of `Dk/u^7 = (k3-k2)/u^7`,
  leading `D*R = (lambda3-lambda2)*R`, the `m3D - m3N` observable, the
  consistency `C = 1 + b*K/2 + 3*pi/(2*K) - K^2/12 = 0` on the corrected
  branch, and the sector determinants as R -> infinity.
- M1/M2 (open, inherited): sign of d/dR det Kp_odd and det Ko, and trace
  signs on [1+delta,infinity).
- (G1') on [1+delta,infinity) (open, inherited): det D_xF_sigma(R,x) != 0
  with sgn (-1)^n on the whole solution set; n=2 (I1)/(I2) are the concrete
  instances feeding M1/M2/M3.

## Attempted routes

- even-only u^2 ansatz `[FAILED]`: symbolic solve of E1/E2/E5/E6 orders 2..7
  gives residual 2.6e11; failure mechanism now STRICT: E5_5 = 1/(2K^2) is a
  hard constant, so no even-in-u branch exists (scripts/_gapn2_largeR_series.py).
- even-only u^4 ansatz `[FAILED]`: same structural obstruction; check orders
  8-10 residuals 1e13-5e14 (scripts/_gapn2_largeR_series.py with u^4 params).
- hybrid Richardson/balance solvers `[PARTIAL]`: scripts/_gapn2_largeR_balance.py,
  _gapn2_largeR_balance_ms.py, _gapn2_largeR_balance_check.py produced the
  270-row continuation and fits but no closed balance; superseded by the
  symbolic route, kept as cross-checks.
- data-driven free-exponent fits `[SUCCEEDED]` (EVIDENCE only): s ~ 2 primary
  exponent, limits above; used to retract K -> 2.789 and to seed the symbolic
  solve (scripts/_gapn2_largeR_fit.py, _gapn2_largeR_sigma_fit.py).
- full 32-unknown global symbolic solve `[BLOCKED]`: scripts/_gapn2_largeR_full.py
  builds the exact truncated system but the naive expansion (K-powers to
  degree 21 in 32 variables) is too slow; fix identified: per-monomial
  u-truncation m+j<=9 and the level-by-level cascade below; not yet run to
  completion.
- limit-level (stage A) solve `[PARTIAL]`: scripts/_gapn2_largeR_stage.py
  found a spurious root (K0 ~ 0.0265, c0 ~ -30772) from the wrong equation
  set; the physical limit is pinned jointly with A_2 (levels 0-2), not by
  the limit-level equations alone.

## Next actions

1. Implement the level-by-level cascade in scripts/_gapn2_largeR_full.py:
   level j unknowns (K_j, a_j, b_j, c_j), equations E1_j, E2_j,
   E5_{j+2}, E6_{j+3} (levels 0-2 jointly as the nonlinear seed: a0*K0 = 2,
   A_1 = 0, A_2 from E6_5, E1_2/E2_2/E5_4 consistency), lower levels
   substituted, per-monomial truncation to total order <= 9.
2. Validate the solved series against the last data row of
   scripts/_gapn2_largeR_big.json (u ~ 0.1494): k2, k3, p1, p3, D*R, Dk/u^7,
   M/u^5; target agreement at the u^2 truncation level.
3. Derive the leading observables (Dk/u^7 coefficient, D*R limit,
   m3D - m3N, consistency C = 0, sector determinants as R -> infinity).
4. On success: write run_notes_addendum with the STRICT balance proof and
   EVIDENCE tables, append ledger entry R-209, update tools/, append the
   AGENTS.md session log, run validate_pipeline.py, commit and push
   (origin, then fork per project.json git_sync.push_order).
Do not re-run the even-only ansatz routes without recording a new reason.

## Key artifacts

- Task packet: runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/problem_contract.md
  sha256 CBC53E86806C055957478D0E7F6A3C359C280D6DD5A7C0404FA917BF7E92CFBA
- runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/research_ledger.md
  sha256 83FD0A7F89200AEADE3D53674F22FAC05CF157A068550734BB2DC4E9E7C042B6
- runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run-manifest.json
  sha256 DB0321F61E077216CBAC26B1FF7704CC36F3C1C8946333F5478825B9C3E22C7B
- runs/rigorous-open-math-research/R-20260812T090000Z-g1prime-g2/run_notes_addendum_2026-08-13e.md
  sha256 399B6F66DB94FD6EEFF873BADC08B8E1BDD8AFEE14A97B0B6734D42D9E28D437
- scripts/_gapn2_largeR_closed.py sha256 10E315DD92332C2E9D5125EF0F3585EAB8F47DAA353584B03BA8802CC20C0D3A
- scripts/_gapn2_largeR_Pbuild.py sha256 B8A3958501C8B703D11B099BEB7AC705BF5CFBAE9AAF002BC5D236D0ACF91E86
- scripts/_gapn2_largeR_full.py sha256 040C6B6E33C059586C02EC3EAFB919DC1427786BB38F4FAE625CAF9F6BA3CF5F
- scripts/_gapn2_largeR_fit.py sha256 4588A1336DE4261E9B22F4B85A47A0287A2B2884389C917129DBB99873240949
- scripts/_gapn2_largeR_sigma_fit.py sha256 C2D934C0671DE17422DD2D8313797793877C4AA4DF529E20FE719D4F9B6334E3
- scripts/_gapn2_largeR_big.json sha256 1E3C924B8CAA4B9424BF666F52BFCB826722DE582D9E90D2658E36F1F0D66F45
- scripts/_gapn2_largeR_P.pkl sha256 952CAB37743CC2D88E3E5A446C9A320E29836C421F35EC35178C82AC7EB445A3
- Not present in the run directory (checked): approach_registry.md,
  candidate_proof.md, audit_report.md.  No STRICT proof of the M3 balance
  exists yet, so nothing is promoted.

## Recovery read order

1. This handoff record
2. research_ledger.md (chronological, last entries first)
3. run_notes_addendum_2026-08-13e.md and run_notes_addendum_2026-08-13d.md
   (R-208 anchor and route context)
4. scripts/_gapn2_largeR_full.py and scripts/_gapn2_largeR_Pbuild.py
   (current symbolic state)
5. The original task packet (problem_contract.md, obligations M1-M3)
