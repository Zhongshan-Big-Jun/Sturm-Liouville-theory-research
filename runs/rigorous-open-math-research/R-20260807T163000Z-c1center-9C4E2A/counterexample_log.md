# Counterexample log - R-20260807T163000Z-c1center-9C4E2A

Purpose: adversarial tests of C1 and of each subclaim.  No counterexample to
C1 was found.  Entries: refuted sub-claims, confirmed edge cases, and failed
verification attempts with exact failure mechanisms.  ASCII punctuation.

## C-001 (REFUTED sub-claim, prior run, re-confirmed): center-contraction
M := XC - C with XC = (x_- + x_+)/2 does not satisfy M*(a+b-1) <= 0.
Counterexample (a,b,R) = (0.7793, 0.8032, 100): M = +0.00925 > 0 with
a + b > 1 (mpmath 60-digit; x_- = 0.72671, x_+ = 0.87430, q = 0.0560,
v(1-) = -0.05828).  Also dXC/dC = 1 exactly on the diagonal.  Recorded so no
later run re-tries contraction on the center.

## C-002 (REFUTED sub-claim, this run): "Phi unimodal with max at a_fp" (U)
For R = 1e6, Phi(a0) = 0.999626 < 1 (dips below 1), then rises to
Phi(fp) = 1.991323.  Phi - 1 has sign -+-: the earlier (U) is false as a
global statement.  Replaced by U' (M-shape of Phi - 1), which is what N1
actually uses.  Script: s33_profile.py.

## C-003 (corrected data issue): tracew pollution
tracew_*.json rows for a > ~1/2 and near the diagonal are on the WRONG sheet
(e.g. row a = 0.51 with W = 1.033, R1 = -1.8e-2 instead of W = 0.3288,
R1 ~ 1e-13 on S3).  Using tracew naively produces wrong W/Phi values and
wrong conclusions.  Clean S3 data are produced by s33_profile.py (continuation
from the fp with continuity guards).  The left part a <= fp is usable after
filtering rows by the recomputed R1 residual (s33_zeros.py).

## C-004 (corrected derivation): right-side norm n2
Earlier draft claimed n2 ~ a^3/(2 pi^2) + [right-well term]; the correct
statement for a > 1/2 is n2 = a^3/(2 pi^2) + O(1/q) (mode pinned in the left
well; the right-well and barrier contributions are O(1/q), measured
q^2 I2 ~ 4e-6 and I3 ~ 1e-6 at q = 1000).  The wrong formula would give a
wrong branch equation; the corrected (P+) matches numerics to 0.1%.

## C-005 (tested): (P-) fails inside the transition layer
At a = 0.49, q = 1000: measured W = 0.0631 vs (P-) prediction 0.0399 (60%
error).  (P-) is valid only in the generic regime a <= ~0.47; the transition
layer extends to xi = (0.5-a)q ~ 10-30.  Any use of (P-)/(P+) must restrict
to the generic regime with the matching controlled by Gap 1.

## C-006 (tested): no good roots on auxiliary sheets
Prior runs verified |R2| >= ~1e-2 on non-fp sheets away from the fp
(EVIDENCE).  Not re-run this session.

## C-007 (failed certification attempt): interval Newton
cert_roots.py / cert_c1.py: the interval Newton quotient N = s - F/F_s on
enclosures is wider than the enclosure at moderate box widths (da = 1e-4,
db = 5e-3, dR = 1e-3 R at R = 4): division-width blowup.  Sign-based
certification is designed but not tuned.  No certified-computation result is
claimed.

## C-008 (REFUTED sub-claim, this session): "fp-component limit curve
sin(2 pi b) = -sin(pi a)/2 with slope 1/14 at a0 as R -> 1+" (old A9/C8).
  (i) S3 at R = 1.05 is nearly vertical: db/da in (48, 531), so G(a0) -> +inf
      as R -> 1+, not 1/14 ~ 0.0714.
  (ii) No S3 point at R = 1.05 satisfies the curve: test point (a,b) =
      (0.4199, 0.5) on S3 (R1 = -6e-3 at grid precision) has sin(2 pi b) = 0,
      -sin(pi a)/2 = -0.483.
  (iii) The correct limit object is the vertical segment {a = a0}; the branch
      is a = a0 + eps phi(b) + O(eps^2), b in [a0, b_top ~ 0.936].
  Mechanism of the error: the old base formula used R1 = 2 pi^2 sin^2(pi a) -
  8 pi^2 sin^2(2 pi b) (second term with b instead of a) and computed the slope
  of the phantom curve instead of the branch tangent.  Refuted by direct
  continuation and root-finding (s33_r1plus.py).

## C-009 (confirmed edge case): the degenerate point (a0, a0) is on {R1 = 0}
for every R (empty barrier), and for small R the fp-component is the component
through it: R1(a0, ., R) has the unique root b = a0 for R in [1.001, 1.05]
(dense 1301-point scan), and continuation from (a0,a0) climbs through the fp
(R2 = 0 on the sheet exactly at the fp).  Any proof or data pipeline must not
mistake this for a spurious root; conversely the e15 first-row b = 0.41939681
(R <= 100) IS spurious (R1 = 1.6e-4 there; F-017).