# Audit report - M3 (obligation: exact large-R scaling / leading balance of (k2,k3,p1,p3) of the n=2 symmetric INF branch)

- **Run:** R-20260812T090000Z-g1prime-g2 (obligation M3)
- **Audit target:** `run_notes_addendum_2026-08-14.md` (R-210)
- **Audit date:** 2026-08-14
- **Auditor role:** adversarial audit (fresh subagent, artifact-only prompt)
- **Authority rule:** every STRICT claim independently re-derived from the exact
  series coordinate dict P (`scripts/_gapn2_largeR_P.pkl`), the exact closed
  system (`scripts/_gapn2_largeR_closed.py`), and the `big.json` data last row.
  I did NOT accept the solver's authority for anything; every level-0..2 and
  observable formula below was rebuilt from the P dict and sympy, then compared.

## Overall verdict line

The STRICT structure claims of R-210 (pre-clearing zero-set preservation, level-0
identity a0*K0=2, level-1 identity a1 = -2*K1/K0^2 with K1 free, reduced seed
affine-linearity, b0/b1 delay to E5_6, hard-constant forcing of the odd
components, and the STRICT observable formulas) are **INDEPENDENTLY_AUDITED_PROOF**
as derivations from the exact series dict.  The forward-looking uniqueness claim
S4 (nonzero 4x4 at every level j>=3) is **FALSE as stated at level 3**, which I
prove below; it was labeled OPEN by the solver and is not a false STRICT claim,
but it must be corrected.  **M3 overall remains RIGOROUS_PARTIAL_RESULT**: the
corrected-branch seed root (the nonzero odd corrections and the closed leading
observables m3D-m3N, C=0 value, sector determinant leading coefficients) is still
OPEN and was not required of this audit to close.

---

## A1. System fidelity - PASS

Independently rebuilt E1, E2 from the exact closed expressions of
`_gapn2_largeR_closed.py` in the ansatz

    k2 = K*u, k3 = K*u + C*u^5, p1 = pi/2 + A*u^2, p3 = pi/4 + B*u^2,
    eps = u^3 = R^{-1/2}, u = R^{-1/6},  p1t = p3 k3/k2, ...
    p2 = k2/2 - eps(p1+p3), p2t = k3/2 - eps(k3/k2)(p1+p3),

and compared every resulting coefficient against the pickled dict
(`scripts/_audit_m3_a1a2.py`, `scripts/_audit_m3_e6diff.py`,
`scripts/_audit_m3_e5.py`):

- **E1** (orders 0,2,4,6,8,10): every coefficient matches the dict EXACTLY.
- **E2** (orders 0,2,4,6,8,10): every coefficient matches EXACTLY.
- **E5** (orders 0,2,4,5,6,7,8,9,10): rebuilt from-scratch the full
  mass-integral construction (ID * sin^2 p1t - IN * sin^2 p1 with the D/N
  inner-block masses); every coefficient matches EXACTLY.
- **E6** (orders 3,5,7,9): rebuilt from-scratch (band at x2); every coefficient
  matches EXACTLY.  (My first attempt at E6_7/E6_9 showed a spurious mismatch;
  it was a bug in my own cot-series construction, not in the dict, and a clean
  rebuild matched to 0 -- recorded as an auditor-side fix, no F-code.)

- Parity structure confirmed from the dict: E1,E2 carry only even raw orders;
  E6 only odd orders (3,5,7,9); E5 even through u^4 and all orders from u^5.
- **Ansatz fidelity.**  The dict, and hence the cascade, is a power-series
  expansion in u of the exact closed system, evaluated at u small.  The ansatz
  itself (k ~ K u, p1 ~ pi/2, p3 ~ pi/4 with the R^{-1/6} scaling) is grounded in
  the run's spectral fits and the R-207 1e-12 verification at R=350; that part is
  EVIDENCE, as the deliverable records.  The FORM (integer powers u^j, eps = u^3)
  is STRICT by construction -- there is no fractional power in the balance.
- **Truncation.** The dict is truncated at raw u-order 10 (E5 through 10, E1/E2
  through 10, E6 through 9).  Per-monomial total order <= 9 is sufficient for the
  derivative cascade through level 3 (verified: the highest level-3 equation order
  used is E6_6 < 9).  Confirmed sufficient; higher levels need higher-order terms
  as expected.

## A2. Series algebra - PASS

- From-scratch sympy re-expansion of E1/E2 (orders 0..10) and of the full E5/E6
  mass-integral assemblies (orders 0..10) matches the dict EXACTLY, coefficient by
  coefficient (`_audit_m3_a1a2.py`, `_audit_m3_e5.py`, `_audit_m3_e6diff.py`).
- Independent numeric validation of the dict against the EXACT closed system
  (`_closed.system`) at 8 random symbolic-parameter points, u in [0.02,0.14]:
  max |series - exact| = E1 1.3e-11, E2 1.0e-9, E6 4.4e-9, E5 5.0e-6.  The E5
  residual is the expected truncation tail (E5_0 and higher raw orders at u up to
  0.14); at a solution A0*K0=2 the constant E5_0 term vanishes.  All shrink with
  u, consistent with the dict being the exact Taylor expansion to order 10.
- **K-clearing** (E1*K^0, E2*K^2, E5*K^5, E6*K): confirmed from the dict that
  these are the clearing exponents needed to remove K-power denominators (max K
  powers: E1=0, E2=2, E5=5, E6=1 match `DNAME`).  Since K>0 on the branch
  (K ~ 3.46, EVIDENCE) each scaling is multiplication by a positive power, so the
  zero set is unchanged.  STRICT.

## A3. Cascade structure - PASS (levels 0-2, hard constant) / FAIL (S4, level >=3)

Independently re-derived every level from the pre-cleared dict with the exact
identity substitutions A0=2/K0, A1=-2*K1/K0^2 (`_audit_m3_cascade2.py`,
`_audit_m3_level3.py`, `_audit_m3_level3fast.py`).  My results, matching the
deliverable line-for-line:

- **Level 0.**  E1_0 = -sqrt(2)/4 (A0*K0 - 2); E2_0 = sqrt(2)/4 K0^2 (A0*K0-2);
  E6_3 = -K0 (A0*K0 - 2); E5_2 = -K0^2/48 (A0*K0-2)*F with
  F = 12*pi*A0*B0*K0 - A0*K0^3 - 36*pi*A0 - 24*pi*B0 + 6*pi*C0 + 3*pi^2*C0
  + 6*K0^2.  Hence E1_0=E2_0=E6_3=0 iff A0*K0=2, and E5_2=0 automatically once
  A0*K0=2.  **Verified exactly.**  The three multiplicative equations E1_0,E2_0,
  E6_3 carry ONE constraint (a0*K0=2), as the deliverable states.
- **Level 1.**  E1_1 = -sqrt(2)/4 (A0*K1 + A1*K0); E2_1 = sqrt(2)/4 K0 (3A0*K0*K1
  + A1*K0^2 - 4*K1); E6_4 = -(2*A0*K0*K1 + A1*K0^2 - 2*K1).  Under A0=2/K0 all
  reduce to a single relation A1*K0^2 + 2*K1 = 0, i.e. **a1 = -2*K1/K0^2**, with
  K1 free.  **Verified exactly.**  (My first pass reported E6_4=0 from an
  expansion bug -- `expand` was applied before multiplying by u^m; corrected by
  expanding after the u^m factor.  Auditor-side fix, no F-code.)  Note E5_3 does
  not exist in the dict (raw E5 orders have no 3), consistent with parity.
- **Level 2 (reduced seed).**  With A0=2/K0, A1=-2K1/K0^2:
  - E1_2, E2_2, E6_5 are AFFINE-LINEAR in (A2,K2,C0), K1 entering only via K1^2.
    Verified: all three second partial derivatives in (A2,K2,C0) vanish.
  - The explicit reduced forms match the deliverable line-for-line (factor out
    -sqrt(2)/(24K0^2), sqrt(2)/24, -1/(12K0) respectively).
  - E5_4 is QUADRATIC in (A2,K2,C0) (verified: contains A2^2, C0^2, K2^2,
    A2*C0, K2^2..., but not B0/B1).
  - **b0,b1 first appear at E5_6.**  Verified: E1_2,E2_2,E6_5,E5_4,E5_5 have zero
    B0,B1 dependence; E5_6 depends on B0 (and B1).  Hence b(u) is determined only
    at order u^6 (one level later than the handoff assignment), confirming S2.
  - **Hard constant.**  E5_5 (K-cleared) reduces to K0^3/2 when K1=C1=0 (verified
    exactly: E5_5[K1=0,C1=0] = K0^3/2).  Hence E5_5 = K0^3/2 + [linear in K1,
    C1] + quadratic/higher odd, and E5_5=0 is IMPOSSIBLE with K1=C1=0 (K0>0).
    The even-only ansatz is structurally inconsistent; the odd components are
    forced.  This is the STRICT failure mechanism (handoff) reproduced and
    localized to (K1,C1).  **Verified.**
- **Higher levels (S4).**  The deliverable asserts affine linearity at level j>=3
  and states the 4x4 nonsingularity is OPEN.  I COMPUTED the level-3 cell (E1_3,
  E2_3, E5_5, E6_6) and its 4x4 matrix in the unknowns (K3,A3,B3,C3):
  - All four are affine in the level-3 unknowns (no quadratic terms, verified).
  - But dE1_3/dB3 = dE2_3/dB3 = dE5_5/dB3 = dE6_6/dB3 = 0 and likewise for C3:
    the B3 and C3 columns of the level-3 matrix are IDENTICALLY ZERO.
  - det(M3) = 0 (symbolically and numerically).  **The level-3 4x4 is SINGULAR.**
  Concretely, the level-3 unknowns that actually enter the level-3 cell are only
  (K3, A3); B3 and C3 are not determined there.  This stems from the ansatz's
  weight structure: B enters through u^2 in p3 (so B_j is suppressed to orders
  >= 2+j with additional mass suppression; B0 first at E5_6), and C enters through
  u^5 in k3 (C_j suppressed to >= 5+j).  **Finding:** the deliverable's S4
  ("provided the 4x4 is nonsingular, each level j>=3 determines (K_j,a_j,b_j,c_j)
  uniquely") is FALSE as stated at level 3 -- the 4x4 is provably singular, and
  the natural cascade must instead advance K,A at their own orders and B,C with
  shifted indices.  Because the deliverable explicitly labels the determinant
  OPEN and does not claim it is nonzero, this is not a false STRICT claim, but it
  is a real defect in the proposed higher-level uniqueness mechanism that must be
  corrected.  Recommended correction: re-derive the true level indexing (K_j,A_j
  at order ~j, B_j at order ~2+j, C_j at order ~5+j) and re-form the nonsingular
  blocks accordingly.

## A4. Uniqueness - PASS (claims made) / note

- Level 0-1 leaving K1 free: verified STRICT (A3).
- The seed (levels 0-2) is a finite system: consistent -- the top variables that
  participate are (K0, K1, A2, K2, C0, B0, ...) with b0 entering one level later.
- **a0*K0 = 2 with the EVIDENCE fit values:** a0*f = 0.5788, K0*f = 3.4553 gives
  a0*K0 = 1.999928 (|diff| = 7.2e-5, within the deliverable's 5e-4 tolerance).
  Verified.
- **a1 = -2*K1/K0^2 with the EVIDENCE values:** K1 is a FREE (odd) series
  coefficient not pinned by the handoff free-exponent fits (which report only
  K0,a0,b0,c0), so this relation cannot be numerically spot-checked against the
  EVIDENCE values.  I report this honestly: the identity a1 = -2K1/K0^2 is STRICT
  (a derivation from E1_1/E2_1/E6_4), but its agreement with any EVIDENCE number
  is unverifiable because K1 is undetermined by the fit data.  No F-code; the
  deliverable does not claim a numerical K1.
- The physical root selection (which of the finitely many seed roots matches
  K0 ~ 3.4553) is NOT established by the deliverable (it is the OPEN seed root).
  The deliverable does not claim it is closed, so this is an honest OPEN, not a
  failure.

## A5. Data validation - PASS

Last row of `big.json`: R=89895.87707, u=0.149408981, K=3.519374254,
a=0.565322729, b=0.280215261, Dk/u^7=69.240075, D*R=10.880627 (extra 0.59207344).
Using mpmath at 50 digits (`_audit_m3_a2num_a5.py`, `_audit_m3_mpmath.py`):

- **Manager anchor u = R^(-1/6):** |u - R^{-1/6}|/u = 4.3e-17 relative -- matches
  to 14+ digits.  Verified.
- **Dk/u^5 = c(u):** c = (Dk/u^7)*u^2 = 1.54564922 (finite-u; the limit c0 =
  1.4741 is the EVIDENCE fit).  Consistent with the STRICT formula Dk/u^5 = c(u).
- **D*R = 2*K*c + c^2*u^4:** 2*K*c + c^2*u^4 = 10.88062668719 vs data D*R =
  10.88062668719 -- agree to 3.5e-13.  STRICT formula verified against the data
  row to full stored precision.
- **Dk/u^7 = c/u^2:** predicted = 69.2400754198 = data exactly.  Verified.
- Limit seed: 2*K0*C0 = 10.186915 (data last D*R = 10.8806 at u = 0.149, still
  decreasing toward 10.1869 -- the deliverable's "lower extrapolation" reading is
  consistent with a decreasing sequence); a0=2/K0=0.578821; consistency candidate
  C_cand = 1.869563 at the even-only seed (matches deliverable 1.86956); hard
  constant K0^3/2 = 20.6266.  All match the deliverable's EVIDENCE numbers.

## A6. Leading observables - PASS (honesty) / note

- The deliverable HONESTLY labels the corrected-branch values as OPEN: m3D-m3N
  ("its leading terms are carried by the corrected branch and are NOT yet closed
  numerically ... OPEN"), C = 0 value ("C = 0 holds only on the corrected branch"
  - not claimed), and the sector-determinant leading coefficients ("Their leading
  coefficients remain OPEN").  These are not claimed as achieved.
- The STRICT formula parts that ARE claimed (Dk = C u^5 so Dk/u^5 = c(u),
  D*R = 2K c + c^2 u^4 -> 2 K0 c0) are independently verified (A2/A5).  The
  identity a0*K0 = 2 is STRICT and verified.
- Note: the audit packet expected the sector determinant leading coefficients c1,
  c2 (det Kp_odd ~ c1 R^{-7/2}, det Ko ~ c2 R^{-9/2}) to be provided; the
  deliverable leaves them OPEN and the scalings as EVIDENCE (from addendum e
  Section 5b).  This is a gap vs the packet's expectation, honestly labeled --
  not a false claim.  I did not attempt to close it (out of the M3 seed root).

## A7. Label honesty - PASS (no violations found)

- Every STRICT-flagged item in R-210 that I checked is a derivation-only
  statement and was independently reproduced in EXACT sympy arithmetic (no
  numerics): pre-clearing, level-0/1/2 identities, affine-linearity, b0/b1 delay,
  hard-constant forcing, STRICT observable formulas.
- Every numerical result is segregated under EVIDENCE (Section 3 solve attempts,
  Section 4 numbers, sector determinant scalings, m3D-m3N OPEN).  No EVIDENCE item
  is presented as STRICT.
- Minor nits (not hard fails, F-note level): (i) Section 0 header says "recalled,
  all STRICT" yet includes "K ~ 3.46" and "verified 1e-12 against the spectral
  engine" which are EVIDENCE-style (numeric) facts; the closed-form EXACTNESS that
  follows is STRICT, and the numerical checks are EVIDENCE.  This is a labeling
  laxity in the prose, not a mathematical mislabel.  (ii) The "matches the fit a0
  = 0.5788 to 5e-4; STRICT identity verified against the EVIDENCE fit" phrasing
  mixes a STRICT identity (a0=2/K0) with an EVIDENCE fit, but the STRICT/EVIDENCE
  split is clear in context.  Both are F-note (minor), not F-failures.

## A8. Regression - PASS (no contradiction found)

- The STRICT level-0/1/2 structure and the hard-constant mechanism do not
  contradict R-204 Theorem A (block-energy identity) / Theorem D (zero count),
  R-205 global eps-alternation, R-207 half-Green closed forms, or R-208 Lemma A /
  Theorem B.  The R-210 results concern the band unknowns (k2,k3,p1,p3), while the
  prior STRICT results concern K-sector Green identities and the R->1 anchor; the
  two are compatible.
- The near-degeneracy implied by the ansatz (k3 - k2 = C u^5 -> 0 as R -> inf) is
  consistent with the run's "INF large-R near-degenerate pair" (R-200/R-202
  bonding-antibonding) and with the INF determinant decay to 0+ (R-207/R-208).
- The R-207 sector closed forms (in terms of the kernels at the symmetric
  switches) are not derived from the ansatz in R-210 but are inherited unchanged;
  no inconsistency with the ansatz was found.  The ansatz's p1,p3 scale (pi/2 + a
  u^2, pi/4 + b u^2) is consistent with the phase behavior used in the R-207/208
  half-problem machinery.
- No STRICT claim in R-210 contradicts a prior STRICT result.

## Attack log (summary of adversarial attacks run)

- Rebuilt the P dict from scratch for all four equations (A2).  Pass.
- Rebuilt the mass-integral E5/E6 chain from scratch (A2).  Pass.
- Re-derived every level-0/1/2 coefficient independently (A3).  Pass.
- Tested the level-3 affine 4x4 for nonsingularity (A3/A4).  **FAIL -- found
  singular (B3,C3 columns vanish).**
- Checked the unknown-presence pattern at level 4 (A3): level-4 unknowns
  (K4,A4,B4,C4) do NOT appear in the nominal level-4 cell (E1_4,E2_4,E5_6,E6_7);
  consistent with the finding that K,A advance at their own orders and B,C need
  shifted levels.  (Independent of whether one labels this a 4x4; the clean
  4x4-per-level claim is what fails.)
- Validated D*R = 2Kc + c^2 u^4 and u = R^{-1/6} at 50-digit precision (A5).
- Audited label separation STRICT/EVIDENCE/OPEN line by line (A7).
- Confirmed the even-only-ansatz impossibility is a genuine STRICT mechanism, not
  a numerical artifact (A3).

## Per-obligation verdicts

| Obligation | Verdict | First-error / note |
|---|---|---|
| A1 system fidelity | PASS | ansatz/dict exactness + parity confirmed; ansatz origin EVIDENCE |
| A2 series algebra | PASS | all P coefficients match from-scratch; K-clearing holds |
| A3 cascade (levels 0-2 + hard constant) | PASS | verified exactly |
| A3 S4 (level-j nonsingular 4x4) | **FAIL (F-NL3)** | level-3 4x4 singular: B3,C3 columns vanish, det=0 |
| A4 uniqueness | PASS (as claimed) | a0K0=2 vs EVIDENCE verified; a1 K1-free; K1 not numerically pinned |
| A5 data validation | PASS | D*R, Dk/u^7, u=R^{-1/6} verified to ~1e-13 / 1e-17 |
| A6 leading observables | PASS (honesty) | OPEN parts honestly labeled; STRICT formulas verified |
| A7 label honesty | PASS | two F-notes (minor prose), no mislabel |
| A8 regression | PASS | no contradiction with R-204/205/207/208 |

## F-code register

- **F-NL3 (level-3 nonsingularity).**  Layer: statement/dependency (the claimed
  higher-level uniqueness mechanism S4).  The level-3 cell (E1_3,E2_3,E5_5,E6_6)
  is affine in (K3,A3,B3,C3) but the B3 and C3 coefficients are identically zero
  in all four equations, so the 4x4 is singular (det = 0).  The correct structure
  must advance (K_j,A_j) at their own levels and (B_j,C_j) at shifted levels
  (B_j ~ order 2+j, C_j ~ order 5+j).  Because the deliverable labels the
  determinant OPEN, this is a correction, not a false STRICT claim; the STRICT
  claims of R-210 are unaffected.  Impact: the deliverable's "each level j>=3
  determines (K_j,a_j,b_j,c_j) uniquely" cannot be true as written.
- **F-note (A7 minor):** Section 0 header "recalled, all STRICT" groups two
  EVIDENCE-style numeric facts ("K ~ 3.46", "verified 1e-12 against the spectral
  engine") under a STRICT banner; the closed-form exactness is STRICT and the
  numerical checks are EVIDENCE.  Prose cleanup only.
- **F-note (A6):** the packet expected explicit c1,c2 for det Kp_odd ~ c1 R^{-7/2}
  and det Ko ~ c2 R^{-9/2}; R-210 leaves them OPEN (honestly).  Not a false claim.

## Scripts created (all under scripts/_, never touching solver files)

- `_audit_m3_inspect.py` - P dict / big.json structure.
- `_audit_m3_a1a2.py` - from-scratch E1/E2 re-expansion vs dict; parity.
- `_audit_m3_e6diff.py` - E6_7/E6_9 exact rebuild (resolved my own cot bug).
- `_audit_m3_e5.py` - from-scratch E5 mass-integral rebuild vs dict.
- `_audit_m3_a2num_a5.py` - dict vs exact closed system numeric; big.json row.
- `_audit_m3_cascade2.py` - independent level-0/1/2 re-derivation (corrected).
- `_audit_m3_level3.py` - level-3 4x4 matrix and determinant (singular).
- `_audit_m3_level3fast.py` - level-3 B3/C3 absence confirmation.
- `_audit_m3_mpmath.py` - 50-digit STRICT-observable / anchor verification.

## Final statement

STRICT structure claims of the R-210 deliverable are **INDEPENDENTLY_AUDITED_PROOF**
(as derivation-only statements from the exact series dict), with the sole caveat
that the forward uniqueness mechanism S4 is **falsely stated at level 3** and must
be corrected.  **M3 overall remains RIGOROUS_PARTIAL_RESULT** until the
corrected-branch seed root (nonzero odd components and the closed leading
observables m3D-m3N, C=0, sector coefficients) is closed; closing it is the
solver's outstanding task, not a requirement of this audit.
