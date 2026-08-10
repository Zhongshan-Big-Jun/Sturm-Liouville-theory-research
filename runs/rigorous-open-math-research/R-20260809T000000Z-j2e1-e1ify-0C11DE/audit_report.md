# Audit report - O3a complete proof chain independent audit (session 45, 2026-08-09)

Run: R-20260809T000000Z-j2e1-e1ify-0C11DE (continuation)
Target: docs/SL_gap_n1_O3a_phase_rigidity_proof.tex (38 pages)

## Scope and method
- Independent symbolic/analytic audit of the entire O3a proof chain, item by item,
  without accepting drafts or prior audits as authority.
- Two independent sympy 1.13.1 scripts: misc/_audit_symbolic_a.py (21 checks),
  misc/_audit_symbolic_b.py (67 checks); reruns of the repo's verification
  scripts; full replay of the E1 certificate chain.
- Evidence layering kept explicit: all audit conclusions are E1 (strict/exact
  symbolic); E3 numerics are cross-checks only, never results.

## Results by group (all PASS unless noted)
- A. eq:psi / lem:rtau (9/9): Psi' identity, second bracket = -G(x)-2x cos^2 x,
  E' = O' = -q/Phi on all branches, eq:alphap, d/dc((c+q)^2 x^2), eq:Dc,
  eq:dimred coefficient, (d/dx)log J = 2 cot x / W, r_tau log-derivative.
- B. F_e'(q,1/2) closed form + P(x) (5/5): exact verification of
  F_e'(q,1/2) = 2 pi (cos x - 1)^3 / sin^3 x * P(x) at x = 2 asin(1/sqrt(2(q+1)));
  P(x) = (pi-3x)^2 + 3(x - sin x)(pi - 2x) > 0.
- C. eq:G2id + lem:G2m2 (13/13): G2 = -Phi W0/D - 2P; Phi/D <= 65/66;
  W0 < 0.582; P < 0.576; combination G2 > -1.734 > -2.
- D. thm:j1e1 steps (i)-(vii) (19/19): Phi >= q; u_x formula;
  D - c(q^2-1) sin^2 x = q + c; G = u(H-A); G_c = t1 + t2;
  d/dq(Phi/D) closed form along c1; f'(x) formula; C <= 8; u_c/F algebra;
  F'' formula; g'(y) formula; final combination 6499/7500.
- E. q=1 lines (8/8): J1(x,1) = (2x/pi)^2 N(x), N = 2(z^2+8z+6)-2x^2;
  J2(gamma,1) = x^2 N(x)/pi^2, N = 2(z^2-8z+6)-2x^2; z ranges and bounds.
- F. lem:j2bounds (23/23): W1+W2 decomposition (mod st^2+ct^2=1);
  M = B2 - 2A cg B1; W4+W5 decomposition; W6+W7+W8 = t^2 cg sg^2 Q(z);
  D^2 - cg^2 = 4 sg^2; cos^2 tau = cg^2/D^2; sin tau = 2 sg/D;
  corner mu = 27921/20000 > 139/100; all 10 table rows recomputed.
- G. Fepos/Feneg (4/4): E(g) - c g = pi(1/2 - c) (standard arctan identity,
  numeric cross-check at 40 digits); Mf(alpha2;c) = ((pi-g)/g)^2 phi_c(g);
  Mf(pi/2;0) = pi^2/(4q); Mf(pi;0) = 0.
- H. Independent J2 decomposition (1/1, key): J2 = G^2 + Gc - u Gx built from
  the raw eq:G definition, substituted x = pi - gamma, q = st cg/(ct sg),
  c = t/A, compared with the closed form 2 A^2 cg W / Delta^4: the 2008-term
  numerator reduces to 0 modulo the Groebner basis of sg^2+cg^2-1, st^2+ct^2-1.
  Numeric cross-check at 8 points, 50 digits: |raw - cf| <= 1.7e-49.
  This makes lem:j2dec fully self-contained (no reliance on the archived
  t3_NJ2.json monomial data).

## Reproduction reruns
- misc/zz_rebuild_check1.py: W == T1+..+T8 modulo trig relations = True.
- misc/t3_j2direct.py: J2_2d at corner = -5.864821190401388 matches the doc's
  q=1-line formula -5.864821190401385.
- misc/_verify_identity.py: BEFORE the fix it printed "W - sum(T) == 0 ? False"
  (the raw polynomial identity is false; the doc's claim is the identity
  modulo circle relations). FIXED to report both: raw False (expected) and
  modulo relations True.
- misc/e1_certgen.py full replay: 57/57 PASS, 241.6 s; L10/L11/L12 content
  hashes unchanged (certificate chain reproducible byte-for-byte).
## Historical: defects F-201..F-205 (pre-audit-C)
- F-201 (tex line 344): sign typo in the second bracket: was
  "-G(x)+2x cos^2 x", corrected to "-G(x)-2x cos^2 x" (A2 check confirms
  the corrected form; both are < 0 so no mathematical consequence).
- F-202 (tex line 1437): "sin(17/10) = cos(13/100)" is false as an equality;
  corrected to "sin(17/10) >= cos(13/100)" (sin(1.7) = cos(pi/2-1.7) >=
  cos(0.13) since pi > 3.14).
- F-203 (misc/_verify_identity.py): cited in the doc as evidence but printed
  False for the raw identity; fixed to report the modulo-relations identity
  (True), matching the doc's actual claim.
- F-204 (audit script E1/E2, fixed): boundary closed forms need the explicit
  substitutions atan(w) = pi/2 - theta and atan(w/q) = 2 theta on the boundary
  curve; numerically confirmed before fixing.
- F-205 (audit script H, fixed): the first implementation left the linear phase
  term (gm2) unsubstituted; after the fix the independent identity passes.

## Historical: deliverables (pre-audit-C)
- Fixed tex: docs/SL_gap_n1_O3a_phase_rigidity_proof.tex
  (sha256 12a21f762238db9645b496ad9d4cf1f2727ef439f205415370f1c278d94addf9);
  recompiled 38 pages, zero warnings/errors.
- Audit scripts kept as artifacts: misc/_audit_symbolic_a.py (21/21),
  misc/_audit_symbolic_b.py (67/67).
- Fixed script: misc/_verify_identity.py.
- PDF sha256: cc2362e052e0b514bd84a072c838b99eb5e71eb1dbea5d2968ee2d5bb5074c69.

## Audit C: remaining chains (2026-08-09, continuation)
- New artifact misc/_audit_symbolic_c.py: 70/70 PASS, groups I-V.
- I. lem:B1 tail (8/8): Leibniz partial sums S5, S6 exact values (22739538548/33837890625,
  7436856470852/10997314453125), 67/100 < S5 < atan(4/5) < S6 < 17/25, final tangent
  combination -1054523/114800, g'(4/5;17/25,157/50) > 3.3581, g'(sqrt3) bound
  -14957063/441000.
- II. lem:boundary rational bounds (3/3): R(z) <= -262235520291/59137044050 and
  T(z) <= -7282185739373/266116698225 from the stated envelope (z<=10/17,
  pi in (157/50,22/7)); numeric cross-check max R,T on [0,1/sqrt3] far below.
- III. lem:M2 (10/10): h'(1/2) > 0.1016 and h'(0.53) < -0.52 by exact rational
  alternating-series envelopes; d_q M2 split identity; B(q) = B0(q) + 2pi(2q+1)/q^2
  with the derived chain dM2/dq <= 4pi^2 sqrt(2q+1) + 8pi(2q+1)/q - 14pi q
  + 14 sqrt(2q+1) + 4pi q + 1 <= B(q) (each inequality justified); grid cross-check
  dM2 - B < 0 (worst -3.96e+02); B(20) = -232.72343276308... < -232.723 with rational
  envelope (pi in (3.14159,3.14160), sqrt41 in (6.40312,6.40313));
  B'(q) <= (4pi^2+14)/sqrt41 - 10pi < 0 (rational -90313/3920); M2/q^2 bound
  -4752271/735000 < 0 for w > sqrt41.
- IV. lem:corner/C4 (30/30): all constants (Machin pi interval, sqrt5, tan(3pi/10),
  tan(2pi/5), tan(2pi/7) root P(t)=t^6-21t^4+35t^2-7 with P(1253/1000)>0>P(1254/1000)),
  tan(7theta) numerator identity, IN = A*K and K = q^2 L (algebraic), L'(v) = N/(10T^2)
  (symbolic differentiation), Region I sum 88146367488708279/400000000000000, Region II
  c3 bound 2160051043/15625000, L(2pi/7) >= 13058215729/5000000000, G2(1/2;2) > 0.
- V. lem:inclusion (18/18): derivative table for F1/F2 (with F-206 fix), endpoint
  closed forms 5pi/14, arccos(2/3), pi/3, arccos(2/3) > 0.841 via cosine alternating
  lower bound, gamma(2,2/5) > 0.655 full rational chain (tan(0.655) < 0.7682,
  1/1.5364 > 0.6508, atan(0.6508) >= S5 > 0.5767, pi/2 - 0.5767 < 0.9941),
  h' < 0.
- Also verified by hand (written up in audit_report): w < sqrt(2q+1) on the phase
  curve for 0<c<1/2 (from atan w = c(pi-gamma) < (pi-gamma)/2 -> w < cot(gamma/2)
  -> w^2 < 2w cot gamma + 1 = 2q+1); thm:LOG case split; thm:keylemma endpoint
  assembly (x = 2 asin(1/sqrt(2(q+1))) in (0,pi/3), P(x) > 0, sign of (cos x-1)^3);
  C4/CORNER monotonicity conclusion (G2 = IN/POS, POS > 0, IN decreasing in w,
  w increasing in c).

## New defects found and fixed (F-206, F-207)
- F-206 (tex line 1106): d_q F1 displayed as q*tan x/(1+q^2 tan^2 x); the correct
  derivative is tan x/(1+q^2 tan^2 x) (verified symbolically and numerically).
  Both are positive, so the conclusion (alpha1 strictly decreasing in q) is
  unaffected, but the formula is corrected.
- F-207 (tex lines 672-679): under the stated definition S_k := sum_{j=0}^k,
  the two displayed Leibniz partial sums are S_5 and S_6, not S_6 and S_7
  (verified: 22739538548/33837890625 = S_5, 7436856470852/10997314453125 = S_6;
  and S_5 < atan(4/5) < S_6 holds by alternating-series theory). Relabeled
  S_6->S_5, S_7->S_6; the numerical chain 67/100 < S_5 < b < S_6 < 17/25 is
  unchanged and correct.

## Audit D: appendix certificate-method prose (2026-08-09, continuation)
- Audited the appendix method description (rem:env(a), lem:envseries,
  tab:envprims caption) against the actual generating code misc/rigid1d.py and
  misc/e1_certgen.py and the certified table data (exact-rational arithmetic,
  same code path as the generator). Two presentation defects found and fixed.
  No certificate data was changed: the 57/57 ledger facts and all table rows
  are untouched; the regenerated fragment differs from the previous one only
  in the caption line (hashes of e1_certgen.py and e1_cert_ledger.json
  unchanged).
- F-208 (tex, lem:envseries): the sin alternating-series sandwich direction
  was reversed. With S_m := sum_{k=0}^m (-1)^k x^{2k+1}/(2k+1)! the correct
  statement is S_{2m} >= sin x >= S_{2m+1} (the doc wrote
  S_{2m+1} >= sin x >= S_{2m}). Verified by exact rational arithmetic at
  x = 3/2, m = 0..2 (S_0 = 3/2 >= sin(3/2) >= S_1 = 15/16, etc.) and by the
  alternating-series theorem (term ratio x^2/((2k+2)(2k+3)) <= 3/8 < 1).
  The cos direction C_{2m} >= cos x >= C_{2m+1} was already correct. The
  lemma now also states the Taylor remainder bounds |sin x - S_m| <=
  x^{2m+3}/(2m+3)! and |cos x - C_m| <= x^{2m+2}/(2m+2)!.
- F-209 (tex, lem:envseries + rem:env(a) + tab:envprims caption): the claims
  "arctan with 22 terms has remainder < 10^{-12} for x <= 3/2" and "every
  primitive envelope width <= 10^{-12}" are false as stated. Actual
  mechanism: the direct series is only used for v <= 1 (remainder <=
  v^{45}/45; at v = 1 this is 1/45, not < 10^{-12}); for v > 1 the code uses
  pi/2 - atan(1/v) with pi certified via Machin (remainders <= (1/5)^{45}/45
  ~ 7.8e-34 and <= (1/239)^{45}/45 ~ 2.1e-109; pi width ~ 2.5e-32). The
  worst certified primitive width in tab:envprims is tau(131/200)
  ~ 1.8e-10 = 2 v^{45}/45 with v = 1/(2 tan(131/200)) ~ 0.651; all other
  primitives (sin, cos, A, D) have widths <= 10^{-23}. The doc now states
  these true bounds and notes they are far below the smallest certificate
  margin (~2.6e-5 for h(0.655) >= m), so no sign conclusion is affected.
  The tab:envprims caption was updated accordingly; the tab:envpoints
  caption claim (width <= 10^{-12}) is true (measured max point-fact width
  1.7e-13 at TB(0.72)) and was left unchanged.
- Independent exact-rational measurements (generator code path) backing the
  corrected text: primitive point widths at the 11 primary points are
  sin <= 4.1e-25, cos <= 9.8e-24, A = 2.5e-32, D <= 5.9e-25,
  tau <= 1.8e-10 (at 131/200); point-fact certified widths <= 1.7e-13;
  global min margin 2.557e-5. The corrected sin sandwich bound uses the
  term ratio 3/8 (a draft of the edit had 3/16; the final text states 3/8).

## Deliverables (updated)
- Fixed tex: docs/SL_gap_n1_O3a_phase_rigidity_proof.tex
  (sha256 51d18676cd4ec5cbe4b29e0e998f677a69041a6439db5befcdc69633a2ce7c3d);
  recompiled 39 pages, zero warnings/errors (was 38).
- PDF sha256: 7497ee4d6132447bc0145db9b009d1a522d81fc7a37873b867fc7ef3b4580750.
- Table generator + fragment: misc/e1_cert_tables.py
  (9268b4cce7ab56bf66e5b651a8f36bf8269cf096efcbfdd740ae30676e9b38d3),
  misc/e1_cert_tables.tex
  (a5057c02cab697e154e21acc63526b73a0ae31d15c362888f5b5d044010e5742).
- Certificate chain data unchanged: misc/e1_certgen.py
  (375209e2574aea15e3966b442316e2326070d75d4b9445d4bdb9ccf74dfec57c),
  misc/e1_cert_ledger.json
  (ec9ce5ff7af7d9684bdd2097368e789e6f0b1dae798a04e62aef3d073fd68d30).
- Audit artifacts: misc/_audit_symbolic_c.py (70/70).

- E1 footnote added at lem:M2 (d) for the claim B(20) < -232.723: exact rational
  envelope (pi in (314159,314160)/10^5, sqrt41 in (640312,640313)/10^5) giving
  B(20) <= -58180766243071047/250000000000000 < -232.723; monotonicity
  directions verified (d/dpi < 0, d/dsqrt41 > 0 on the box).
- Independent adversarial review (subagent Nash, 2026-08-09): CHAIN 1 (phase-curve
  w < sqrt(2q+1) + strict monotonicity of w in c) PASS; CHAIN 2 (lem:M2 (c)(d)(e)
  incl. the dM2/dq <= B(q) term-by-term chain) PASS; CHAIN 3 (thm:LOG case split)
  PASS; CHAIN 4 (thm:keylemma endpoint assembly) PASS; lines 1046-1048
  (C4/CORNER -> B subset (1,2)x(0.4,0.5)) PASS. No mathematical defect found.

## Audit E: independent third-party replay of the certificate tables (2026-08-10, continuation)
- Goal: close the "recommended next step" of Audit D - an independent replay of the
  certificate chain (misc/e1_cert_ledger.json, 57 facts + 11 primitive rows) with a
  DIFFERENT arithmetic engine, written from scratch.
- Independent engine (misc/audit_o3a_cert_replay.py): decimal.Decimal at 80 significant
  digits with directed rounding (ROUND_FLOOR for lower endpoints, ROUND_CEILING for upper).
  sin/cos/atan/pi are certified via alternating Taylor series (60 terms for sin/cos, 80 for
  atan) and Machin's formula, with rigorous remainder bounds computed under the same
  directed rounding. The generator (misc/e1_certgen.py on misc/rigid1d.py) uses exact
  fractions.Fraction interval arithmetic; the two engines share no arithmetic code.
- Result: 71/71 rows PASS, 0 failures: 57/57 ledger facts independently re-certified
  (1 analytic, 34 point, 7 value-Taylor, 12 derivative-Taylor, 3 concavity-reduction),
  11/11 primitive rows (tab:envprims data) independently recomputed, and 3 structural
  checks (meta constants GLO/GHI/m, fact-kind counts, ledger summary counts).
- Margin compatibility: every independently computed margin agrees with the ledger's
  outward-rounded 12-digit margin to <= 2.7e-11 (tolerance 1e-8). The global minimum
  certified margin is 2.5571653170394554e-5 (h(0.655) >= m); the two engines' agreement
  is therefore far below the certificate's slack (min margin / max deviation > 10^5).
- Structural checks inside the replay: each cell partition exactly tiles the stated
  interval (first cell starts at the left endpoint, consecutive cells meet, last cell
  ends at the right endpoint), centers are exact midpoints, piece counts match n, and
  every ledger piece's stored cell/center/displayed bound/margin/ok is compatible with
  the independent recomputation.
- The three concavity-reduction facts were verified independently:
  h''(g) = 2(cos 2g - g sin 2g) < 0 on [0.655, 13/10] with certified enclosure
  h''.hi <= -0.1596067; the inclusions [0.655, 1.0472] subset [0.655, 13/10],
  tau(0.655) > pi/4 > 0.655, tau(1.0472) < 13/10, and the endpoint values
  h(0.655) >= m, h(13/10) >= m all hold.
- Transparency: two bugs in the replay script itself were found and fixed during
  development - (i) the alternating-series partial sums for sin and atan initially
  lacked the alternating sign (cos had it); (ii) sin_iv/cos_iv initially unpacked the
  (sin, cos) pair in the wrong order. Both were caught before any conclusion was drawn
  (the intermediate runs failed loudly), and the final script re-passes all 71 rows.
  These are auditor-side defects only; the certificate data was not modified
  (e1_certgen.py / e1_cert_ledger.json hashes unchanged: 375209e2... / ec9ce5ff...).
- Artifacts: misc/audit_o3a_cert_replay.py (sha256 3a8672f4a30525ab8e0bd4fe56a54d07ed10e2bb55ce7fd967631d43c65085a7),
  misc/audit_o3a_cert_replay.json (sha256 c239092dfc79f938929d6604d011b75cace8537e102dc2c9bfeeb32755c3b1bb - see repro_manifest).
- Status: the certificate chain is now replayed end-to-end by two independent arithmetic
  engines (exact Fraction and directed-rounding Decimal) with full agreement; the 57 facts
  and the appendix tables remain E1-valid evidence.
## Audit E (续, 2026-08-10): dual-subagent adversarial audit + F-210/F-211 closure
- Two independent subagents audited the full tex with independent re-derivations and
  fresh scripts (misc/_audit_sub_*.py, ~30 files; no edits to docs/ or the ledger).
  - Curie (lines 1-559): 23 ratings, 83/83 scripted checks PASS. Verdict
    REPAIRABLE_GAP with a single defect: the paragraph "为固定正确相位支" (lines
    412-439, eq:phaseeq) asserted alpha1 in (0,pi/2), alpha2 in (0,pi) and
    E(alpha1) = c alpha1, O(alpha2) = c alpha2 without proving that the true phases
    fall on the asserted branch. The auditor confirmed the claim is true (Prufer
    phase / concavity arguments), i.e. a repairable presentation gap, not a counterexample.
  - Linnaeus (lines 559-2396): all PASS. An independent Fraction-interval engine
    re-proved the 57 single-variable facts (55/55 applicable), a Decimal engine
    re-proved 34 point facts; j2dec, the W-decomposition, closed forms, C4, LOG,
    j1e1, j2e1, the appendix methods, and the final assembly all PASS. No E3
    evidence was used as a premise of any conclusion. Two harmless remarks (j1e1
    range statement vs step (iv); "closure contained in T1" wording), not gaps.
- F-210 fixed (this session): added lemma "真实相位落在主支" (lem:phasebranch) with
  a complete E1 proof: Prufer phase theta with theta'(x) = s(cos^2 theta + rho sin^2 theta)
  > 0, theta(0) = 0, theta_k = s_k x on the left region, hence alpha_k = theta_k(xi);
  y1 even / y2 odd with y1 > 0 on (0,1) and y2 > 0 on (0,1/2) force
  theta_1(1/2) = pi/2, theta_2(1/2) = pi, so alpha1 in (0,pi/2), alpha2 in (0,pi);
  the explicit mid-region solutions y1 = A1 cos(ms1(x-1/2)), y2 = A2 sin(ms2(x-1/2))
  force c alpha1 in (0,pi/2), c alpha2 in (0,pi); eq:match then yields
  E(alpha1) = c alpha1 and O(alpha2) = c alpha2 (the alpha2 = pi/2 corner is handled
  via cos(c alpha2) = 0 from the interface equation). Uniqueness follows from
  E' = O' = -q/Phi_q < 0 with cx increasing (E - cx, O - cx strictly decreasing).
- F-211 fixed (this session): thm:j1e1 step (iv) only proved f increasing on
  [pi/3, 5pi/14], while the theorem claims the closure x in [841/1000, 1122/1000]
  (5pi/14 < 1122/1000). Extended monotonicity to the tail [5pi/14, 1122/1000] with
  exact rational envelopes at x0 = 1122/1000 via lem:envseries:
  sin x0 in (9009/10000, 9010/10000), cos x0 in (4338/10000, 4340/10000) (partial
  sums S3/S4 and C3/C4, all finite exact rational inequalities), giving
  x cot x >= (1122/1000)(4338/9010) > (1122/1000)(48/100) and
  x/sin x <= 11220/9009 < 1246/1000, hence
  3 + 3x cot x - x^2 csc^2 x >= 765791/250000 > 0 on the tail.
- Recompiled: xelatex twice, 40 pages, zero warnings/errors. New hashes:
  tex d8e83f4472f1044ca8694b76ca724f0bf326f10c4d17fe405e72329b753af183,
  pdf 72836e20d36cf85c955669509383d35a14e48b1b620e222f4cb6397c77e48408,
  log c824c61119c9a90ab5bdca3d12f5052d7ceb7b4b332103cf484f5f974d5c3069.
- Evidence layering preserved: the new arguments are pure E1 (Prufer phase, explicit
  solutions, exact rational inequalities); no E3 numerical evidence is used as a result.
## Remaining gaps
- The only gap found by the dual subagent audit (F-210, phase-branch selection) and
  the only presentation mismatch (F-211, j1e1 step (iv) range) have been fixed in
  this session with pure E1 arguments; the certificate data was not touched
  (e1_certgen.py / e1_cert_ledger.json hashes unchanged). The proof remains
  CANDIDATE_COMPLETE_PROOF, now with: 71/71 independent certificate replay,
  dual independent subagent audit PASS, and the phase-branch gap closed.

## Audit E (续 2, 2026-08-10, session 49): completeness-audit script fixes (E3 only)
- Re-ran the 8 completeness-audit scripts (E3 evidence, cross-check only; none is a
  premise of any E1 conclusion). Two scripts were failing on grid/precision defects
  unrelated to the proof; both fixed and now PASS:
  - scripts/audit_o3a_pdf_part2b.py: the eigenvalue-grid upper bound 2*pi - 1e-7
    truncated the second zero near 2*pi (R=1.1, (a,b)=(0.499,0.501) has s2 ~ 2*pi).
    Grid upper bound changed to 3*pi; the R list dropped 1e6 (large-R float64 cases
    are handled by part2c/_audit_cstar/_tmp_verify_r1e6 with high precision), now
    [1.1, 1.5, 2.0, 4.0, 10.0, 100.0, 1000.0]. PASS: single sign change per R;
    R=1000 xi*=0.496260895480, R1=2.6e-15, v_a>0, v_b<0.
  - scripts/audit_o3a_pdf_part2c.py: (i) the xi scan previously stopped at 0.4995
    while the R=1e6 root lies at xi ~ 0.49988012; the scan list now extends to
    0.4999995. (ii) the mpmath refinement previously converted xi* back to float64,
    capping residuals at ~1e-15; now float64 is used only to locate xi0 by 30
    bisection steps (width ~1e-11), then mpmath bisection (120 steps) inside
    [xi0-1e-9, xi0+1e-9] keeps the midpoint as mpf throughout. PASS:
    R=1000 xi*=0.49626089548007825, R1=-5.44e-44; R=1e6 xi*=0.499880117059947152,
    R1=-2.76e-46; v_a>0, v_b<0.
- Full re-run of all 8 scripts (part1, part2, part2b, part2c, part3, part4,
  _audit_cstar, _tmp_verify_r1e6): ALL PASS. New script hashes in repro_manifest.md.
- No E1 proof text or certificate data changed in this session; the document
  claim "all checks pass" now matches the actual scripts.
- The document was then recompiled after adding part2b to the audit-script list
  (sec:certs) plus a one-line note on the 2026-08-10 re-run: xelatex twice, 40
  pages, zero warnings. New hashes: tex
  2c3312579218f204cfd381146c1eeb57a0af62c376dd1f4c1150c63d96a7ebb0, pdf
  ecc7ef62393dc3ef5f014613a25d63fd75fdf05adfc3ec1e26f33f9a4ca65f8d, log
  c9be856046c73dca6f493e62e338895321c490baa0e7ff2c1f3a39ec8c614b1b.