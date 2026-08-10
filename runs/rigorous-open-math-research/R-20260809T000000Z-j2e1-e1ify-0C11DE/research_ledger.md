# Research ledger - R-20260809T000000Z-j2e1-e1ify-0C11DE

Timestamps approximate (UTC+8). Continuation session 44 (2026-08-09).

## R-100 (2026-08-09): contract + state audit
- Read problem_contract.md, the tex, and the prior E1 certificate work.
- Confirmed the last E2 dependency: 55 single-variable facts behind
  lem:brackets / lem:track(iv) / eq:endpoints, previously certified by
  misc/rigid_dec.py (L7-L9), needed conversion to E1.
- Ledger misc/e1_facts_ledger.json (old validator output) vs new
  misc/e1_cert_ledger.json (E1 rational envelopes): 55 vs 57 entries
  (new adds 3 h-concavity reductions).

## R-101 (2026-08-09): root-cause fix in rigid1d.py
- misc/rigid1d.py I.sqrt wrote `F(isqrt(...), den)+1` (width always 1.0),
  causing TB point facts to fail. Fixed to `F(isqrt(...)+1, den)`.
  After fix, e1_certgen 57/57 PASS (~266 s).

## R-102 (2026-08-09): certificate chain + tables
- misc/e1_certgen.py -> misc/e1_cert_ledger.json (L11 = ec9ce5ff...).
- misc/e1_cert_tables.py -> misc/e1_cert_tables.tex: 5 tables
  (tab:envprims/envpoints/envsigns/envrange/envderiv); fmt_name maps
  >=/<= to \ge/\le and normalizes targets (2/1 -> 2); outward-rounded
  6/12-digit displays with displayed-interval-contains-certified-interval.
- L12 = dce5c453... (v3 generator).

## R-103 (2026-08-09): tex integration + compile
- Spliced the auto-generated table fragment into the tex; updated L12 hash.
- Fixed overfulls: envprims 154pt (\footnotesize + tabcolsep 3pt + nd 6),
  envderiv 10pt (local tabcolsep 3pt), L7-L9 hash item paragraph (quote
  block + explicit line break), appendix old-validator item (line break).
- xelatex twice: zero warnings/errors, 38 pages, no undefined references.
- Cross-reference audit: rem:env / lem:envseries / lem:envtaylor /
  tab:env* / app:cert / sec:certs all defined and referenced; no E2 or
  rem:riv or tab:facts remnants (only historical mentions of 验证器).

## R-104 (2026-08-09): knowledge base
- New tool tools/rational-envelope-certificates.md; tools/README.md index,
  quick table, and maintenance log updated; [[interval-dec-directed-rounding]]
  marked retired/historical.
- AGENTS.md session 44 record added.


## R-108 (2026-08-09): audit C - remaining chains + F-206/F-207
- misc/_audit_symbolic_c.py: 70/70 PASS. Groups: I lem:B1 tail (Leibniz partial
  sums, tangent combination -1054523/114800); II lem:boundary rational bounds
  (R, T); III lem:M2 (a)(d)(e) (h' endpoints, dM2/dq <= B(q) chain, B(20) <
  -232.723 with rational envelope, B' < 0, w > sqrt41 case); IV lem:corner/C4
  (30 checks: constants, tan(2pi/7) root of P, IN = A*K, K = q^2 L,
  L'(v) = N/(10T^2), Region I/II bounds, L(2pi/7), G2(1/2;2) > 0);
  V lem:inclusion (derivatives, endpoint closed forms, arccos(2/3) > 0.841,
  gamma(2,2/5) > 0.655 full rational chain).
- By-hand verifications written into audit_report: w < sqrt(2q+1) on the phase
  curve for 0<c<1/2; thm:LOG case split; thm:keylemma endpoint assembly;
  C4/CORNER monotonicity conclusion.
- F-206: tex line 1106 d_q F1 = tan x/(1+q^2 tan^2 x) (was q tan x/...);
  conclusion unchanged (both positive). Fixed.
- F-207: tex lines 672-679 Leibniz partial sums relabeled S_6->S_5, S_7->S_6
  (values were off by one index under the stated definition); the numerical
  chain 67/100 < S_5 < atan(4/5) < S_6 < 17/25 is correct. Fixed.
- Recompile: xelatex twice, 38 pages, zero warnings/errors. New tex sha256
  bea923d943a82f72958477a8d36111da623e988fc80a39ae24d140f849abe8c1;
  PDF 98b245ffc36a8c9bd9a51378a070c014110120857341becbe0d6baf0360841c2.
- Independent adversarial review of chains 1-4 by subagent Nash: all PASS
  (CHAIN 1 phase-curve w < sqrt(2q+1); CHAIN 2 lem:M2 (c)(d)(e); CHAIN 3
  thm:LOG; CHAIN 4 thm:keylemma; lines 1046-1048 C4/CORNER). No defect found.
- E1 footnote added for B(20) < -232.723 (rational envelope
  -58180766243071047/250000000000000).

## Remaining gaps
- None within this contract. Optional follow-ups: independent third-party
  replay of the certificate chain; further table compaction (aesthetics only).

## R-105 (2026-08-09): independent symbolic audit, part A
- misc/_audit_symbolic_a.py: 21/21 PASS. eq:psi (A1/A2), eq:G log-derivative,
  IN = G2*POS and d_w IN = M2, lem:B1 g(w) closed forms and monotonicity
  (D1-D10), boundary closed forms M2 and d_q M2 with explicit substitutions
  atan(w)=pi/2-theta, atan(w/q)=2theta (E1/E2), d2_q M2 (F1), corner G2(1/2;q)
  (G1/G2).

## R-106 (2026-08-09): independent symbolic audit, part B
- misc/_audit_symbolic_b.py: 67/67 PASS. Covers eq:alphap/lem:dimred chain,
  F_e'(q,1/2) closed form + P(x), eq:G2id + lem:G2m2 estimates, thm:j1e1
  (i)-(vii) algebra, q=1 lines, lem:j2bounds algebra + mu + table rows,
  Fepos/Feneg identities, and the key independent J2 = 2 A^2 cg W / Delta^4
  modulo-relations identity (Groebner reduction of 2008-term numerator -> 0;
  numeric cross-check 1e-49 at 50 digits).

## R-107 (2026-08-09): defect fixes + reproduction
- F-201: tex line 344 sign typo (-G(x)+2x cos^2 x -> -G(x)-2x cos^2 x).
- F-202: tex line 1437 sin(17/10) = cos(13/100) -> >= (equality false).
- F-203: misc/_verify_identity.py now reports the modulo-relations identity
  (True) alongside the raw identity (False, expected); doc citation now accurate.
- Reruns: zz_rebuild_check1 (W == sum T mod relations True), t3_j2direct
  (corner match), e1_certgen (57/57, 241.6 s, L10/L11/L12 unchanged).
- xelatex twice: 38 pages, zero warnings/errors; new tex sha256
  12a21f762238db9645b496ad9d4cf1f2727ef439f205415370f1c278d94addf9.

## Remaining gaps
- None within this contract. Recommended next step: independent third-party
  replay of the full chain and of the certificate tables (audit_report.md).
## R-109 (2026-08-09): audit D - appendix certificate-method prose (F-208/F-209)
- Audited the appendix method prose (rem:env(a), lem:envseries, tab:envprims
  caption) against the actual generator code and certified table data.
- F-208: sin sandwich direction in lem:envseries was reversed. Correct:
  S_{2m} >= sin x >= S_{2m+1} (verified exactly at x = 3/2, m = 0..2; term
  ratio <= 3/8 < 1). Cos direction C_{2m} >= cos x >= C_{2m+1} was correct.
  Lemma now also states the Taylor remainder bounds for sin/cos.
- F-209: "arctan 22 terms, remainder < 1e-12 for x <= 3/2" and "primitive
  envelope widths <= 1e-12" were false. Actual: direct arctan series only
  for v <= 1 (remainder <= v^45/45; at v=1 it is 1/45); pi via Machin
  (remainders ~7.8e-34 / 2.1e-109; pi width ~2.5e-32); worst tab:envprims
  width tau(131/200) ~1.8e-10 = 2 v^45/45, v ~ 0.651; others <= 1e-23.
  Corrected the lemma, rem:env(a), and the caption; tab:envpoints caption
  claim verified true (max point-fact width 1.7e-13) and left unchanged.
- Also fixed a 3/16 -> 3/8 slip in the corrected lemma text (sin term-ratio
  bound (9/4)/6 = 3/8).
- Certificate data untouched: e1_certgen.py / e1_cert_ledger.json hashes
  unchanged; regenerated fragment differs only in the caption line.
- Recompile: xelatex twice, 39 pages, zero warnings/errors. New tex sha256
  51d18676cd4ec5cbe4b29e0e998f677a69041a6439db5befcdc69633a2ce7c3d;
  PDF 7497ee4d6132447bc0145db9b009d1a522d81fc7a37873b867fc7ef3b4580750.

## R-110 (2026-08-10): Audit E - independent replay, dual-subagent audit, F-210/F-211
- Independent E1 certificate replay with a different arithmetic engine
  (misc/audit_o3a_cert_replay.py: decimal.Decimal 80 digits, directed rounding,
  alternating-series sin/cos/atan + Machin pi; generator uses exact Fraction):
  71/71 PASS (57 ledger facts + 11 primitive rows + 3 structural checks); margins
  agree with the ledger to <= 2.7e-11; global min margin 2.56e-5. Two dev-time bugs
  in the replay script itself were found and fixed before use (alternating-sign
  omission for sin/atan; sin/cos tuple unpack order); certificate data untouched.
- Dual-subagent adversarial audit: Curie (lines 1-559) REPAIRABLE_GAP with the single
  defect F-210 (phase-branch selection in eq:phaseeq, lines 412-439); Linnaeus
  (lines 559-2396) all PASS with independent Fraction/Decimal re-derivations and two
  harmless remarks. ~30 fresh audit scripts in misc/_audit_sub_*.py; docs/ and the
  ledger were not modified by the auditors.
- F-210 fixed: new lemma lem:phasebranch (Prufer phase theta, theta' = s(cos^2 +
  rho sin^2) > 0, theta_k = s_k x on the left region; y1 even/y2 odd force
  theta_1(1/2) = pi/2, theta_2(1/2) = pi; mid-region explicit solutions force
  c alpha1 in (0,pi/2), c alpha2 in (0,pi); eq:match then gives E(alpha1) = c alpha1,
  O(alpha2) = c alpha2; uniqueness from E' = O' = -q/Phi_q < 0 and cx increasing).
- F-211 fixed: thm:j1e1 step (iv) f-monotonicity extended to [pi/3, 1122/1000]; the
  tail [5pi/14, 1122/1000] uses exact rational envelopes at x0 = 1122/1000
  (sin x0 in (9009/10000, 9010/10000), cos x0 in (4338/10000, 4340/10000);
  3 + 3x cot x - x^2 csc^2 x >= 765791/250000 > 0). Pure E1, no E3 as result.
- Recompile: xelatex twice, 40 pages, zero warnings/errors. New hashes:
  tex d8e83f4472f1044ca8694b76ca724f0bf326f10c4d17fe405e72329b753af183,
  pdf 72836e20d36cf85c955669509383d35a14e48b1b620e222f4cb6397c77e48408.
- Status: CANDIDATE_COMPLETE_PROOF maintained; O3a now has 71/71 independent replay,
  dual-subagent audit PASS, and the phase-branch gap closed.

## R-111 (2026-08-10): completeness-audit script fixes (E3 tooling)
- Re-ran the 8 completeness-audit scripts (E3 evidence only; none is a premise of
  any E1 conclusion). Two scripts had grid/precision defects and were fixed:
  - part2b (scripts/audit_o3a_pdf_part2b.py): the eigvals grid upper bound
    2*pi - 1e-7 truncated the second zero at R=1.1 (s2 ~ 2*pi for
    (a,b)=(0.499,0.501)); top bound changed to 3*pi and the R list dropped 1e6
    (large-R float64 handled by part2c/_audit_cstar/_tmp_verify_r1e6), now
    [1.1,1.5,2.0,4.0,10.0,100.0,1000.0].
  - part2c (scripts/audit_o3a_pdf_part2c.py): the xi scan stopped at 0.4995 while
    the R=1e6 root lies at xi ~ 0.49988012 (scan extended to 0.4999995); the
    mpmath refinement converted xi* back to float64, capping residuals at ~1e-15
    (now float64 only brackets xi0 by 30 bisection steps, then mpmath bisection of
    120 steps inside [xi0-1e-9, xi0+1e-9] keeps the midpoint as mpf throughout).
- Results after fixes: R=1000 xi*=0.49626089548007825 (R1=-5.44e-44),
  R=1e6 xi*=0.499880117059947152 (R1=-2.76e-46); v_a>0, v_b<0 in both cases.
- All 8 scripts now PASS: part1, part2, part2b, part2c, part3, part4, _audit_cstar,
  _tmp_verify_r1e6. No E1 proof text or certificate data changed; the document
  was recompiled (40 pages, zero warnings) after the sec:certs audit-script list
  was completed with part2b plus a one-line note on the 2026-08-10 re-run
  (new tex/pdf/log hashes in repro_manifest.md). Status: CANDIDATE_COMPLETE_PROOF
  maintained.

## R-112 (2026-08-10): INF-side well-family small-R phase rigidity (theorem) + Sun 2022 closeout
- New theorem (STRICT, E1): for 1 < R <= 3/2, every sign-consistent good root of the
  well family rho = R on [0,a] u [b,1], 1 on (a,b), satisfies a+b = 1.
  Chain: (i) phase-range lemma (y2 unique zero z in (a,b); explicit sin(ms2 x)/(ms2)
  on the wells forces tau A, tau B < pi); (ii) transport invariant (middle density-1
  region is a rotation P(psi) preserving X^2+Y^2; hence y(b)^2/y(a)^2 = J~(B)/J~(A),
  J~ = sin^2/(sin^2 + m^2 cos^2)); (iii) residual elimination (R1=R2=0 => r_tau(A)=
  r_tau(B)); (iv) strict monotonicity of r_tau on (0, pi/tau) via Psi~' < 0 on (0,pi):
  factorization W~^2 sin^2x Psi~' = -(q+1)(2N0+qN1)/8, N0 = 4x-2sin2x > 0, reduction
  to H = 4N0+N1 > 0 (u = 2x substitution; h' = (1-cos u)(5+cos u)-u sin u(1+2cos u);
  G(u) = tan(u/2)(5+cos u)-u(1+2cos u) rationalized by t = tan(u/2) to N(t) =
  t(6+4t^2)-2(3-t^2) arctan t with N'' > 0, N'(0)=N(0)=0). Threshold q <= 1/2
  (R <= 3/2) is sharp for this mechanism (EVIDENCE: r_tau non-monotone at R=1.6,
  off-axis E=0 branch appears at R >= 1.52).
- Verification: scripts/_well_rigid_verify.py - 8 symbolic identities (A1-A8) all
  True (sympy); probes B1-B5 (q=0.5 max Psi~' ~ -6.9e-13, q=0.5001 positive;
  R=1.5 good root (0.40879841, 0.59120159), a+b=1 to 1e-10, |A-B| <= 4e-13,
  r_tau(A)=r_tau(B)=0.2189882504, y2(a)=+0.0837, y2(b)=-0.0837, zero at x=0.5;
  R=4 off-axis N1 in [-2.76,-2.61] < 0; symmetric-line N1 crosses 0 at v*).
  All EVIDENCE, registered in misc/_well_explore_log.md.
- Defective E3 scripts registered: scripts/_well_mc.py (Psi missing q term),
  misc/_well_fh.py (R1/R2 inconsistent with verified fval/FH), 
  scripts/_well_system_derive.py sec_value extra 1/m factor (exploration only).
- Literature closeout: Sun 2022 (JMAA 516:126513) full text unreachable; official
  abstract (colab.ws) + zbMATH review (Erdogan Sen, Zbl 1506.34110) confirm the class
  is "piecewise continuous with a bounded of jumps", NOT the full measurable box
  class; verdict: cannot close our box-class INF side; potential overlap requires
  full text. papers/ashbaugh1991_gaps.pdf downloaded (Schrodinger L^p gap extremals;
  related mechanism, not the same problem).
- Deliverables: docs/SL_gap_n1_well_rigidity_R32.pdf (11 pp, zero warnings;
  STRICT/EVID labels; honest gaps (a) symmetric-line 1D analysis, (b) R>3/2
  rigidity with N1 candidate route, (c) Theorem A independent re-verification
  CANDIDATE, (d) extremizer existence/good-root condition partial);
  misc/_well_explore_log.md; tools/well-family-rigidity.md + README; AGENTS.md
  session 51; state/current.json + RESUME.md updated.
- FH sign correction registered: dD/da = -(R-1) f(a), dD/db = +(R-1) f(b) with
  f = lam2*y2^2/n2 - lam1*y1^2/n1 (verified 1e-8 by misc/_well_fh2.py; f sign
  distribution at R=4 symmetric good root: f(0.2)=+4.12, f(0.5)=-2.28, f(a)=f(b)=0).
- Status: small-R INF well-family rigidity SOLVED (theorem); general R OPEN.
  Next: gap (a) symmetric-line 1D strict proof; gap (b) candidate route.

## R-113 (2026-08-10): gap (a) closure - symmetric-line 1D analysis (STRICT), INF side 1<R<=3/2 CLOSED
- Theorem (E1, STRICT): on the well-family symmetric line rho_v = R*1_[0,v)u(1-v,1] +
  1_[v,1-v], 1<R<=3/2: (i) f(v) has exactly one zero in (0,1/2); (ii) D(v) = lam2-lam1
  has a unique critical point which is the global minimum (strictly decreasing then
  strictly increasing); (iii) D(0+)=3pi^2, D(1/2-)=3pi^2/R, D(v*)<3pi^2/R.
- KEY LEMMA (thm 5.2): F~_e(c) = M_f(alpha1;c) - M_f(alpha2;c) has a unique zero
  c* in (0,1/2).  Chain: (i) exact dimension reduction (lem 3.3): S_R(xi) = -8q~^2
  (c+q~)^3 F~_e(c) and D_c = -8(c+q~)q~(1-q~^2) F~_e(c), from FH (dD/da=-(R-1)f(a),
  dD/db=+(R-1)f(b)) + chain rule D_xi=-2(R-1)S_R, xi'(c)=-q~/(2(c+q~)^2),
  R-1=(1-q~^2)/q~^2; (ii) decomposition F~_e' = (M1-M2)G1 + M2(G1-G2) with G(x;c) =
  -Phi(3+2x cot x)/(q~+c Phi) + 2cx Phi(q~^2-1) sin x cos x/(q~+c Phi)^2;
  (iii) P1 (lem 4.1): G1 <= -(6 sqrt6 - 6)/5 < -4/3 (uses alpha1 in (0,pi/2),
  Phi1 >= q~^2, W1 = 3+2 alpha1 cot alpha1 >= 3, c < 1/2; (6 sqrt6 - 6)/5 > 4/3 iff
  486 > 361); (iv) P2 (lem 4.1+4.2): G2 > -4/3 via gamma = pi-alpha2 in (0,Gamma],
  Gamma = arccos(q0/(1+q0)) ~ 1.1046 < pi/2, W0 lemma: W0(gamma) = 3-2(pi-gamma)
  cot gamma strictly increasing on (0,Gamma] with W0(Gamma) < (4/3)q0, case split
  W0<=0 (G2>=0) and 0<W0 (G2 >= -W0/q~ >= -W0/q0 > -4/3); (v) easy region c>=1/2:
  phi_c strictly increasing on (0,pi/2) (third term positive for q~<1), split
  c in [1/2,1] and c>=1; (vi) endpoints: F~_e(0+)=pi^2/(4q~)>0, F~_e(1/2)<0 via
  structural identity alpha1(1/2)+alpha2(1/2)=pi (t = tan(alpha1/2) satisfies
  t^2 = 1/(2q~+1), solves both even and odd equations).
- W0 certificate (Appendix A, exact rationals, sympy all True): q0 > 2247/2753;
  q0/(1+q0) > 2247/5000 > 8783/19683 > cos(10/9) => Gamma < 10/9; cot(10/9) >
  2121769/4288410 (alternating-series bounds at 10/9); 2(22/7 - 10/9)*2121769/4288410
  = 271586432/135084915 > 15789/8259 = 3 - (4/3)(2247/2753) => W0(Gamma) < (4/3)q0.
- Corollary: combined with O1-INF reduction (INDEPENDENTLY_AUDITED_PROOF) and the
  small-R well-family rigidity theorem (STRICT, R-112), INF side for 1<R<=3/2 is
  CLOSED: I(R) = D(v*(R)) < 3pi^2/R attained at the symmetric well [R,1,R].
- Corrected handoff errors (recomputed independently): (1) F~_e'' sign claim
  ("negative on [0.42,0.5]") wrong - actually positive (+18..+27); second-derivative
  route abandoned; (2) "G2>=0 for c<=0.40" holds only on the phase curve, not on the
  free region (G2(2.174,gamma->0) = -9); (3) W0 global positivity misjudged:
  W0(0.1) ~ -57.6, W0(0+) = 3-2pi < 0, case split required; (4) sym_endpoint.py had
  extra factor t in the G2 second term (should be pi-t), fixed in sym_endpoint_fixed.py;
  (5) the c=1/2 "closed form" is the derivative F~_e'(q,1/2) = -2pi(1-cos x)^3 T(x)/
  sin^3 x (x = arccos(q/(1+q)), T = pi^2 - 3x(pi-x) - 3(pi-2x) sin x, T>0 on
  [pi/3,pi/2]); the value comes from the structural identity.
- Verification (EVIDENCE only): scripts/_symline/master_verify.py (phase branches vs
  direct secular to 1e-51; mode-2 norm closed-form defect registered, no conclusion
  depends on it); key_lemma_verify.py (P1 max ~ -2.4621 < -1.7394; P2 min ~ -0.4000 >
  -1.2247; c* = 0.1821@q0, 0.1917@q=1; max F~_e' on {F~_e>=0} <= -7.58; easy region
  [0.5,50] max <= -2.6e-7; S_R identity rel err <= 1.3e-11; D_c sign vs -F~_e: 0
  violations; R=1.2 v* ~ 0.415 D* ~ 24.3622; R=1.5 v* ~ 0.409 D* ~ 19.1954);
  key_lemma_verify2.py (gamma <= Gamma all pass; W0 case split 878+151 samples;
  alpha1+alpha2 = pi to 1e-31; tan(alpha1/2) = 1/sqrt(2q~+1) to 1e-31;
  F~_e(1/2) formula/direct ratio = 1); sym_endpoint_fixed.py (derivative closed form
  to 1e-29); key_lemma_certificate.py (all exact rational certificates sympy True).
- Deliverables: docs/SL_gap_n1_symline_proof.pdf (10 pp, zero warnings, STRICT/EVID
  labeled, math-knowledge section, Appendix A exact certificates, Appendix B EVIDENCE);
  docs/SL_gap_n1_symline_summary.pdf (4 pp: success route, failed routes, lessons,
  script index; handoff said 7 pp, actual compile is 4 pp); tools/symline-n1-monotonicity.md
  + README; AGENTS.md session 52; state/current.json + RESUME.md updated;
  misc/_well_explore_log.md updated.
- Status: gap (a) SOLVED (STRICT); INF side 1<R<=3/2 CLOSED.  Remaining: gap (b)
  R>3/2 rigidity (candidate route), gap (c) Theorem A independent re-verification,
  gap (d) global good-root argument residual.

## R-114 (2026-08-10): gap (b) closure - well-family rigidity for ALL R>1 (STRICT)

- Theorem (STRICT): for every R>1, every sign-consistent good root (a,b) of the well
  family rho_{a,b}=R*1_[0,a)u(b,1]+1_[a,b] satisfies a+b=1.  Docs:
  docs/SL_gap_n1_well_rigidity_allR_proof.pdf (14 pp, zero warnings) + summary
  docs/SL_gap_n1_well_rigidity_allR_summary.pdf (8 pp, zero warnings).
- 5-step elementary chain (all STRICT, no numerics used): (1) phase range
  tau*A,tau*B<pi (sign-consistency + Sturm), modal identity alpha(A)+psi+alpha(B)=pi,
  alpha-convexity D(x)=alpha(2x)-2alpha(x)>0 on (0,pi/2) (D' sign + D(0)=D(pi/2)=0)
  => tau<2 (depends on sign-consistency; general configs reach tau~4.70); (2) residual
  elimination: R1=R2=0 => r_tau(A)=r_tau(B) and Sigma2/Sigma1=tau^2 r_tau(A)
  (transfer energy identity + norm closed form Phi=W(A)(psi+mA/W(A)+mB/W(B))/(2m^2),
  C_k^2=W(A_k)/W(B_k)); (3) exact r_tau structure: factorization
  r-1=m^2 sin((tau-1)x) sin((tau+1)x)/(J(x)W(x)W(tau x)) (left >1, right <1), L0 bounds
  on (0,x_mid), strict decrease on (x_mid,pi/2], danger-zone lemma
  (x_mid<x<pi/2<y<=pi-x => r_tau(y)<r_tau(x), via J(pi-u)=J(u) + log-derivative),
  B' lemma (region-II equal-value pairs satisfy x+y>pi); (4) exclusions: L3 convex-hull
  (does NOT need left monotonicity), cross-region by sign, P-sum channel
  P(A)+P(B)=(2-tau)pi vs reflection identity alpha(x)+alpha(pi-x)=pi;
  (5) A=B => a+b=1.
- Corollaries (STRICT): good-root set subset {(a,1-a)}; INF internal critical points on
  symmetric well line for every R>1.
- Corrected handoff errors (independent recomputation, summary section 3): BETA
  all-of-(0,pi/tau) claim false (only (0,x_mid)); r(y)>r(pi-y) false (R=100,tau=1.22,
  y=1.64159: 0.0675<0.1871); left-region monotonicity false (bump at large R) but L3
  does not need it; tau<2 depends on sign-consistency; norm closed form not symmetric
  under A<->B swap; sympy checks must be done under the tangent-form constraint; 8-digit
  v* gave fake nonzero residual (refined v*=0.3825982567998447... gives |R1|<1e-50,
  R=4); L0 reverse-inequality transcription error.
- Verification (EVIDENCE only, scripts/_gapb_s55/): 171 configs modal identities 0
  failures; P-sum to 1.4e-40; norm closed form + C^2 to 1e-40; sign-consistent
  max tau=1.99995184 (R=1.01) vs general 4.70 (R=10^4); D(x) min 9.7e-13; danger zone
  1.24M samples 0 violations; B' global min x+y=3.1421822 margin 5.9e-4 (R=10^4,
  tau=1.4); alpha-reflection only 1-ulp boundary artifacts; refined v* phase
  A=B=1.45756580, |R1|<1e-50, Sigma2/Sigma1=tau^2 r(A)=tau^2 r(B) to 1e-51.
- Deliverables: proof + summary docs (above), tools/well-family-rigidity.md (ALL-R
  STRICT), misc/_well_explore_log.md section 16, AGENTS.md session 56, state/current.json
  + RESUME.md updated, SL_spectral_topics_summary.tex/.pdf (19 pp zero warnings; abstract
  note + strictness-status + open-problem item (i) updated).
- Status: gap (b) SOLVED for all R>1.  NOT claimed: INF side R>3/2 fully closed
  (depends on (a') symmetric-line 1D analysis for R>3/2, (c) Theorem A re-verification,
  (d) global good-root argument).
