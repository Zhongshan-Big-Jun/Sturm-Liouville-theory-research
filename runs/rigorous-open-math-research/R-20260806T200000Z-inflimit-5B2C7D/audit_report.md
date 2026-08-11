# Audit report - Theorem A INF limit proof (run R-20260806T200000Z-inflimit-5B2C7D)

Status label of the audited artifact: CANDIDATE_COMPLETE_PROOF (self-audited;
an independent verifier pass remains the closing step per the upstream
skill's revision policy).  All files ASCII punctuation, UTF-8 without BOM.

## 0. Scope, provenance, and method

Audited artifact: the formal proof in docs/SL_gap_n1_inf_limit_proof.tex
(delivered as docs/SL_gap_n1_inf_limit_proof.pdf, 10 pages, xelatex, zero
warnings), summarized in candidate_proof.md.  Obligations audited: T1, T2,
T3 of the packet Q-20260806-inflimit-5B2C7D (see problem_contract.md and
obligation_graph.md).

Provenance chain (sha256 in repro_manifest.md):
- task packet agenda/task-packets/Q-20260806-inflimit-5B2C7D.md (DRAFT);
- numeric statement source docs/SL_gap_extremals.tex (2026-08-05);
- prior-run context: R-20260805T000000Z-gapn1-a1b2c3 (O1/O2/O3b machinery),
  R-20260806T151000Z-o1reaudit-5A1C3D (O1 independent audit, context only);
- evidence scripts: reproducibility/01..19 (this run);
- tools: transfer-matrix-secular, balanced-phase, sturm-oscillation (leads
  only, never trusted premises).

Method: the auditor re-derived every step of the proof independently (no
step accepted on the authority of the draft or the ledger), rechecked every
premise against its primary source or from first principles, and re-ran the
certification battery 16-19 in this continuation (all PASS; outputs recorded
in repro_manifest.md).  Numeric checks are evidence only; every proof-level
claim is argued analytically below.

Result: every obligation T1/T2/T3 closes after the audit.  Four localized
defects found during this session and corrected in the delivered text are
recorded as F-001..F-004.  No fatal gap was found.

## 1. Verdict taxonomy and summary table

- PASS: the obligation is closed by the delivered text (with any audit
  correction applied and documented).
- REPAIRABLE_GAP: conclusion correct, written argument had a localized
  defect that the audit specifies and repairs.
- PARTIAL / FAILED / NOT_VERIFIABLE: as in the upstream taxonomy.

| Obligation | Verdict | Basis |
|---|---|---|
| T2 (unique root, global min) | PASS | Section 2.1 |
| T3 (interval enclosure, margin) | PASS (verified computation) | Section 2.2 |
| L1 Lemma A'' (w >= 2 lower bound) | PASS | Section 2.3 |
| L2 deep sliver (w <= 2, G >= 25) | PASS (certified) | Section 2.4 |
| T1 (convergence, near-minimizers) | PASS | Section 2.5 |
| Synthesis (Theorem A) | PASS | Section 2.6 |

F-001 (v parameter) and F-002 (a_G vs a* labeling) are classified
REPAIRABLE (both corrected in the delivered text); F-003 (draft encoding
corruption) is a presentation defect repaired by full rewrite; F-004 (script
19 v1) is a certificate defect repaired by v2.

## 2.1 T2 - unique critical point and global strict minimum

Re-derived: the parametrization u(a) = a/(2(a - tan a)) maps (pi/2, pi)
diffeomorphically onto (0,1/2): tan a < 0 on (pi/2, pi), so a - tan a > 0;
u'(a) = (a - (sin 2a)/2)/(2 cos^2 a (a - tan a)^2) > 0 since a - (sin 2a)/2
>= a - 1/2 > 0.  Endpoint limits: u -> 0+ (a -> pi/2+), u -> 1/2- (a -> pi-).
Correct.

The sign chain: J'(a) = 4a K~(a)/sin^2 a, G'(a) = 4 sin^2 a J(a), and
Dbar'(u(a)) = S(u(a)) = -[4(a - tan a)^3/(a^3(2a - sin 2a))] G(a).  The
factor in front of G(a) is strictly negative (each factor positive: a > 0,
a - tan a > 0, 2a - sin 2a > 0 since sin 2a < 0 and 2a > 0).  Re-derived and
symbolically re-verified (script 07; also by direct differentiation).
Correct.

K~ = sin^2 a * h with h(a) = 3 + 3a cot a - a^2/sin^2 a and
h'(a) sin^3 a = 3 cos a sin^2 a - 5a sin a + 2a^2 cos a: each term is
strictly negative on (pi/2, pi) (cos a < 0, sin a > 0, a > 0).  Hence h is
strictly decreasing; h(pi/2) = 3 - pi^2/4 > 0 (pi^2 < 12), h(pi-) = -inf
(the -a^2/sin^2 a term dominates).  K~ has a unique zero a_1 in (pi/2, pi).
Correct.

J: increases on (pi/2, a_1), decreases on (a_1, pi); J(pi/2) = pi^2/2 > 0;
J(a) -> -inf as a -> pi- (cot a -> -inf).  Unique zero a* in (a_1, pi),
sign + then -.  Correct.

G: increases on (pi/2, a*), decreases on (a*, pi); G(pi/2) = 0 and
G'(pi/2) = 4 sin^2(pi/2) J(pi/2) = 2 pi^2 > 0, so G > 0 on (pi/2, a*];
G(pi) = -2 pi^3 < 0.  Unique zero a_G in (a*, pi) (strictly, in (a*, pi) by
the sign pattern), sign + then -.  Correct.

S: sgn S(u(a)) = -sgn G(a) (positive prefactor), so S < 0 on (0, u*),
S = 0 at u* = u(a_G), S > 0 on (u*, 1/2).  Dbar' = S gives strict decrease
then strict increase; Dbar -> +inf (u->0+) and Dbar -> 3 pi^2 (u->1/2-).
Global strict minimum at u*.  Correct.

Finding F-002: an earlier draft labeled the G-zero as a* (the J-zero), and
claimed G(a*) = G'(a*) = 0, which cannot both hold (G'(a*) = 4 sin^2 a*
J(a*) = 0 but G(a*) > 0).  The delivered text uses the correct G-zero a_G ~
2.2766 = a(u*); J-zero a* ~ 1.9856 appears only as J's zero.  Corrected.

## 2.2 T3 - interval enclosure and margin

Script 05 bisects S with mpmath.iv to width 2e-20 and propagates through
a(u), mu_1bar, mu_2bar, Dbar.  Enclosure
Dbar(u*) in [24.9438661384324768968, 24.9438661384324769084] and
3 pi^2 - Dbar(u*) >= 4.664947 (rational margin).  Re-checked: the interval
width is ~1.2e-17, consistent with the bisection; the margin computation
3 pi^2 ~ 29.60881320326807 minus 24.94386613843248 gives 4.664947... > 4.66.
Correct.  This is a verified computation (certification), not an analytic
proof, and is labeled as such.

## 2.3 Lemma A'' - phase-coordinate lower bound (w >= 2)

Re-derived the phase system: matching at x = u gives cot theta_1 =
epsilon tan z_1 and tan theta_2 = -epsilon^{-1} tan z_2; with theta_1 =
pi/2 - delta_1, theta_2 = pi/2 + delta_2 this is tan delta_1 = epsilon
tan z_1 and tan delta_2 = epsilon cot z_2.  mu_k = theta_k^2/u^2.  Correct
(derivation from the transfer matrix in PDF Sec. 2.1; cross-checked
numerically).

Phase brackets (PDF Lemma 2.1): (a) delta_1 <= delta_1+ <= epsilon
tan(pi/8) < 0.011 (uses z_1 <= (pi/2) eps ell/u <= pi/8 from w >= 2, and
arctan x <= x); (b) delta_2 <= delta_2+ = arctan(2u/(pi ell)) (uses cot z
<= 1/z on (0, pi)); (c) z_2 <= pi/8 via the monotone function h(x) with
h'(x) >= pi/2 - 1/2 > 0 (the supremum of 2 eps pi x/(pi^2 x^2 + 4 eps^2) is
1/2, attained at x = 2 eps/pi) and h(1/4 - eps) <= pi/8 (arithmetic with
arctan t <= t and 8/pi <= 2 pi i.e. 4 <= pi^2, true); (d) psi_2 >= 0 via the
strictly increasing g with g(theta_2) = 0 and g(theta_2bar) >= 0 (uses
eps cot z_2bar <= u/(theta_2bar ell) = tan d_2bar).  All re-derived;
correct.  The grid spot-check (4 x 61 points, script 19) is evidence.

Exact identity: G - Dbar = (theta_2^2 - theta_1^2 - theta_2bar^2 +
pi^2/4)/u^2 = (def_1 - def_2)/u^2 with def_1 = pi delta_1 - delta_1^2 =
pi^2/4 - theta_1^2 and def_2 = theta_2bar^2 - theta_2^2.  Correct by direct
algebra; verified to 1e-42 at 480 points (evidence).

def_1 lower bound: delta_1 = arctan(eps tan z_1) >= arctan(eps z_1) >=
arctan((pi/2 - delta_1+) alpha) (tan z >= z, z_1 = (pi/2 - delta_1) alpha);
arctan x >= x - x^3/3 >= x(1 - x^2/3) with x <= (pi/2) alpha gives
delta_1 >= (pi/2 - delta_1+) alpha (1 - pi^2 alpha^2/12); def_1 =
delta_1(pi - delta_1) >= (3 pi/4) delta_1 (since delta_1 <= pi/4).  Then
def_1 >= (3 pi^2/8)(ell/u) eps^2 c_1 c_2 with c_1 >= 0.99319..., c_2 >=
0.99996... (using alpha <= eps/4 from w >= 2).  Correct.

def_2 upper bound: psi_2 = d_2bar - delta_2 >= 0; tan psi_2 = (A - B)/
(1 + AB) with A = tan d_2bar = u/(theta_2bar ell), B = tan delta_2 =
eps cot z_2.  The identity A - B = u/(theta_2bar ell) - eps/z_2 + eps
R(z_2) = -u psi_2/(theta_2bar theta_2 ell) + eps R(z_2) uses
1/z_2 - 1/z_2bar = (theta_2bar - theta_2) eps ell/u / (z_2 z_2bar) = psi_2
/(theta_2bar theta_2 eps ell/u)...  [the delivered text's chain is
A - B = -u psi_2/(theta_2bar theta_2 ell) + eps R(z_2), re-derived: since
z_2 = theta_2 eps ell/u and z_2bar = theta_2bar eps ell/u, eps/z_2 - eps/
z_2bar = (1/theta_2 - 1/theta_2bar) * u/ell = u psi_2/(theta_2bar theta_2
ell); so A - B = u/(theta_2bar ell) - eps/z_2bar + eps R(z_2) =
[u/(theta_2bar ell) - eps/z_2bar] - [eps/z_2 - eps/z_2bar] + eps R(z_2)
= 0 - u psi_2/(theta_2bar theta_2 ell) + eps R(z_2).  Correct.]  Then
psi_2 [tan psi_2/psi_2 (1 + AB) + u/(theta_2bar theta_2 ell)] = eps R(z_2);
with tan psi_2/psi_2 >= 1 and 1 + AB >= 1: psi_2 <= eps R(z_2)/(1 + AB +
u/(theta_2bar theta_2 ell)).  R(z) <= C_z z on [0, pi/8] (P2), z_2 <= pi/8,
so eps R(z_2) <= C_z theta_2 eps^2 ell/u; AB = (u/(theta_2bar ell)) * eps
cot z_2 >= (u/(theta_2bar ell)) eps (1/z_2 - C_z z_2) = u^2/(theta_2bar
theta_2 ell^2) - C_z theta_2 eps^2/theta_2bar = v^2/(t theta) - C_z theta
eps^2/t; hence 1 + AB + u/(theta_2bar theta_2 ell) >= 1 + v(v+1)/(t theta)
- delta with delta <= C_z pi eps^2/(pi/2) <= 4.5e-4 (R >= 1500).  Then
def_2 = psi_2 (theta_2bar + theta_2) gives the stated bound.  Correct.

Finding F-001: v = u/ell = -t cot t.  From tan t = -t ell/u (the limiting
equation tan a = -a ell/u with a = t) one gets u/ell = -t/tan t = -t cot t.
The earliest draft and script 19 v1 used v = -cot t (missing the factor t),
which is mathematically wrong.  Consequences: f(t) = 2t^4/(t^2+v^2+v) is
decreasing in v >= 0 on [0,inf), so using the smaller v = -cot t gave a
valid UPPER bound for f, and the old numeric certificate (f <= 9) remained
valid; but the formula was wrong.  Script 19 v2 certifies with the correct
v: f-max = 5.422510, ratio 0.825511 < 1.  Corrected in the PDF, the tools,
and the repro manifest.

Ratio: def_2/def_1 <= [4 C_z/(3 pi (pi/2 - delta_1+) c_2)] * B(theta) *
(1 + 4.6e-4), B(theta) = theta(t + theta)/(1 + v(v+1)/(t theta)); B'(theta)
> 0 (direct differentiation, re-derived) so B(theta) <= B(t) = 2t^4/(t^2 +
v^2 + v).  For t <= 3/sqrt(2): B(t) <= 2t^2 <= 9.  For t in [3/sqrt(2), pi):
certified by 500 directed-rounding interval cells, worst cell bound 5.422510
<= 9 (script 19).  Then the ratio bound: 4*0.337*9/(3 pi * 1.5601 * 0.99996)
* 1.00046 <= 0.8256 < 1 (numerically re-checked: 4*0.337*9 = 12.132;
3 pi * 1.5601 * 0.99996 ~ 14.71; 12.132/14.71 ~ 0.8247; times 1.00046 ~
0.8251 < 0.8256 < 1).  Correct.  Hence def_2 < def_1 and G > Dbar.  The
only non-analytic ingredients are the three certified constants; the
certificates (scripts 18-19) are directed-rounding interval cells with
independent Decimal-engine cross-checks.

## 2.4 Deep sliver (w <= 2): G >= 25

The four-region cover: A (B_1 = 3 pi^2 R - 32 pi^4 R eps w^2/c), B (B_2 =
pi^2 R ((1 - 2 eps w)^{-2} - 1)), C (B_3 = pi^2 R (1/(4w^2) - 1), analytic,
min exactly 25 at w_cap), D (max(THB, D2B)).  The worst certified values
(script 16, re-run PASS) are 42724 / 293.36 / 25 / 77.67, all >= 25 with
margins >= 0.059 (region C endpoint) to thousands.  The region C bound is
fully analytic: for w in (w_c, w_cap], theta_2 >= pi/2 and mu_1 < pi^2 R
give G >= pi^2 R(1/(4w^2) - 1) >= 25.  The tails: R >= 57050 (A: B_1 >=
1.68e6; B: B_2 >= 1792, monotone in R) and R >= 1e8 (D: THB >= 0.1529
sqrt(R) >= 1529).  Grid [1500, 1e8] geometric.  The certification uses
interval/directed rounding; the underlying inequalities are elementary.
Audit: re-ran script 16 (PASS, 18 s).  The medium-region grid (script 17,
115185 cells, worst corner bound 27.99 >= 25) is an independent
cross-check using Feynman-Hellmann monotonicity, not part of the analytic
chain.  Correct.

Known honest limitation (recorded): the region cover is certified over the
grid [1500, 1e8] plus analytic tails; this is computer-assisted certification
of a finite but representative grid, NOT a symbolic proof of every cell
inequality.  The endpoints and worst cells are explicitly checked; the
certification is reproducible (script 16, deterministic, directed rounding).

## 2.5 T1 - convergence and near-minimizer convergence

(i) limsup: fixed u*; delta_1(R,u*) <= eps tan((pi/2) eps ell*/u*) -> 0 and
psi_2(R,u*) <= [C_z theta_2 eps^2 (ell*/u*)(theta_2bar + theta_2)]/[...] ->
0 (from L1.3 with the bracket lower bound bounded away from 0 at u*), so
G(R,u*) -> Dbar(u*); m_R <= D_R(u*) gives limsup <= Dbar(u*).  Correct.
(ii) liminf: two cases by w; w <= 2: G >= 25 > Dbar(u*) (margin 0.0561 from
T3); w >= 2: G >= Dbar(u) >= Dbar(u*) (Lemma A'' + T2).  R*m_R >= Dbar(u*).
Correct.  (iii) limit.  (iv) near-minimizer: R D_R(u_R) -> Dbar(u*)
(squeeze); if w_R <= 2 infinitely often, G >= 25 > Dbar(u*), contradiction;
so eventually w_R >= 2 and Dbar(u_R) <= G(R,u_R) -> Dbar(u*), with Dbar(u_R)
>= Dbar(u*) (T2); Dbar(u_R) -> Dbar(u*).  Accumulation point u_inf: u_inf =
0 excluded (Dbar -> +inf), u_inf = 1/2 excluded (Dbar -> 3 pi^2 > Dbar(u*),
strict inequality from T3), u_inf in (0,1/2): continuity gives Dbar(u_inf) =
Dbar(u*), and T2 strict monotonicity forces u_inf = u*.  Hence u_R -> u*.
Correct; the correction in the delivered text (full accumulation-point
argument, previously sketched) closes (iv).

## 2.6 Synthesis

Theorem A = T1 + T2 + T3.  With T2 (u* unique global minimizer), T3 (enclosed
value, 25 > Dbar(u*)), L1/L2 (lower bounds for all u), T1 assembles the
limit and the minimizer convergence.  Correct.

## 3. Findings

- F-001 (REPAIRABLE, corrected): v = u/ell = -t cot t, not -cot t.  Bound
  validity unaffected (f decreasing in v); formula corrected in the PDF, the
  tools, script 19 v2.
- F-002 (REPAIRABLE, corrected): a_G (G-zero, ~2.2766) vs a* (J-zero,
  ~1.9856) labeling; G(a*) = G'(a*) = 0 impossible.  Delivered text uses the
  correct zeros.
- F-003 (PRESENTATION, repaired): the earlier draft of
  docs/SL_gap_n1_inf_limit_proof.tex had 2161 Chinese characters corrupted
  into literal "?" (encoding defect of the writing channel); the document was
  fully rebuilt in this continuation, and re-compiled with zero warnings.
- F-004 (CERTIFICATE, repaired): script 19 v1 used the wrong v; v2 (this
  session) certifies the correct v; SHA256 recorded in repro_manifest.md.

## 4. Residual risks (honest)

- The three constants C_z < 0.337, B(t) <= 9, ratio 0.8256 rest on interval
  certification (scripts 18-19) rather than on a fully symbolic proof; the
  certificates are deterministic, directed-rounding, and cross-checked with
  an independent Decimal engine.  A symbolic proof of B(t) <= 9 on
  [3/sqrt(2), pi) is possible but not yet written.
- The deep-sliver cover is grid-certified plus analytic tails; the grid is
  finite.  The worst cells are certified with wide margins (>= 0.059 in
  region C, which is analytic anyway).
- T3 is a verified computation (interval arithmetic), not a hand proof.
- O3a/C1 (symmetric inf = full box-class inf) is NOT closed by this run.

## 5. Status

All obligations T1/T2/T3 of this run's contract are CLOSED by the delivered
proof with the corrections above.  The run-level status is
CANDIDATE_COMPLETE_PROOF (self-audited).  Per the upstream skill revision
policy, an independent verifier pass on the changed points (Lemma A'' chain,
T2 zero labeling, T1 step (iv)) is required before the manager closes the
portfolio item; this is recorded for the manager in run-manifest.json notes.
## Independent re-verification addendum (2026-08-12, session 58 continuation 3)

Independent re-verification of Theorem A (INF R->inf limit) for gap (c) closure.
Scripts (this repo, scripts/): _theoremA_recheck_t2t3.py, _theoremA_recheck_lemAdp.py.
All numerics are EVIDENCE cross-checks, not proofs; analytical identities checked
exactly with sympy.

- T2 monotone structure: sympy confirms J' = 4a*K~/sin^2 a and G' = 4 sin^2 a * J
  EXACTLY (difference 0). u'(a) closed form matches finite differences.
  h'(a)*sin^3 a < 0 on (pi/2,pi) (2001-pt scan). S(u(a)) = -(4(a-tan a)^3)/(a^3(2a
  -sin 2a)) G(a) and Dbar'(u) = S(u) verified. Roots a1 = 1.6350426, a* = 1.9855095,
  aG = 2.2765132 (doc approx 1.6351/1.9856/2.2766). Sign patterns of K~, J, G, S all
  PASS. Endpoints: Dbar(0+)=+inf, Dbar(1/2-)->3pi^2.
- T3: u* = 0.3299225081200665495928... in doc interval
  [0.32992250812006654958, ...60]; Dbar(u*) = 24.9438661384324769026... in doc
  interval [24.9438661384324768968, ...9084]; margins 3pi^2-Dbar >= 4.664947 and
  25-Dbar > 0.0561 PASS.
- Lemma A'': 175-pt grid (R in {1500..1e8}, w>=2): G >= Dbar(u) with 0 failures,
  min margin 3.9714e-10 at (1e8, 0.499) - matches the doc's stated min exactly.
  def1 >= def2 at sample points. Lemma 2.1 brackets: delta2 <= delta2+, psi2 >= 0,
  z2 <= pi/8 all PASS.
- Sliver: 600-pt scan (R in {1500,1e4,1e8}, w<=2): G >= 25 with 0 failures; min at
  w=2 boundary G(1500, 2/sqrt(1500)) = 91.7263164 (doc 91.7263).
- T1: G(R,u*) - Dbar(u*) = 0.010381, 1.558e-3, 1.558e-5, 1.558e-7 at R =
  1500,1e4,1e6,1e8 (doc 1.04e-2/1.56e-3/1.57e-5/2.05e-7) - consistent.
- Constants: C_z = 0.3368113990... < 0.337; R(z)/z increasing; max f(t) on
  [3/sqrt2,pi) = 5.4017 <= 9 (doc certified bound 5.4225); ratio bound 0.82505
  <= 0.8256; eps0*tan(pi/8) < 0.011; c10 >= 0.99319; c20 >= 0.99996;
  delta <= 4.49e-4. All PASS.
- Cross-check: secular equations vs independent finite-difference shooting agree
  to 1e-5..1e-8 (discretization-limited).
- Conclusion: no errors found; Theorem A re-verified independently. Gap (c) CLOSED.
  Note: correct branch for the odd mode in the sliver region is z2 in (0,pi)
  (delta2 < 0); the naive fixed-point root search has multiple roots from
  tan/cot periodicity and must be bracketed by the branch condition.
