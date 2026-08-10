# Counterexample log

Run: R-20260806T140000Z-keylemmaaudit-2F83B1 (independent audit)

Purpose: adversarial search for counterexamples to every obligation of the KEY
LEMMA, and a log of genuine defects found in the audit's own tools.

## Obligations attacked

- (LOG) G1 - G2 < 0 and (FP) Ftilde' < 0 for all q > 1, c in (0, 1/2):
  sampled 200k random points (q in (1.00001, 200), c in (1e-4, 0.5)); no
  violation (LOG max -2.504, FP max -2.2e-5).  Region B = (1,2)x(0.4,0.5) dense
  grid (8M points): min H = 2.4185 > 0, max Fp = -0.4562 < 0.
- G2 >= 0 on q >= 2 (R1): grid over q in {2, 2.001, 2.1, 3, 10, 100}, c in
  (0, 0.5): min G2 = 0.1406 (corner exact min 0.06918 at (2, 1/2) > 0).
- G2 >= 0 on c <= 0.4 (R2): grid over q in {1.0001, ..., 100}: min G2 = 0.4564.
- M2 < 0 on D and dM2/dq < 0: random points and the q >= 20 grid (max dM2/dq
  -627.3); no violation.
- u(1/2) = sqrt(2q+1), u in (0, sqrt(2q+1)), IN*G2 > 0: no violation.
- K(v) > 0 on [2pi/7, 2pi/5): certificate + tail; the tail lower bound at the
  junction v = 2pi/5 - 1e-3 gives T^3K = 181.01 > 178.86 bound.
- H(q,1/2) > 0 and Ftilde'(q,1/2) < 0 for q in [1+1e-7, 1e4]: no violation.
- CORNER: G2(1/2;q) min 0.06918 at q = 2, positive for all q >= 2; for q in
  (1,2), G2(1/2;q) is negative (e.g. -0.174 at q = 1.5) - this is expected and
  is exactly why Region B includes the c = 1/2 boundary and why B4/B5 (not
  CORNER) close it.  No contradiction.

## Genuine defects found in the audit's own tools (not in the candidate proof)

1. audit_iv v1: products and divisions were computed in the ambient 28-digit
   Decimal context instead of the directed 80-digit context (unsound).  Fixed:
   all inner arithmetic inside _flr/_cel.
2. audit_iv v1: Decimal.sqrt ignores the rounding mode in Python 3.10 (always
   rounds to nearest).  Fixed: _sqrt_directed computes the sqrt at PREC+20 digits
   with correct rounding and inflates outward by 1 ulp; validated on 3000 random
   cases.
3. audit_iv v3 (introduced during this session): _atan_series divided by
   (2j+1)! instead of 2j+1 (a transcription error inherited from the sine series
   pattern), which made atan return sin values and PI fail its containment check.
   Caught by the sanity harness (PI contains true pi: False); fixed.
4. audit_iv v2: sin/cos over wide intervals used the Taylor series over the whole
   interval, whose dependency blow-up made the L4/L5 leaf re-evaluations useless
   (interval width ~80 instead of ~10, sign not closable).  Fixed: exact
   monotone-range computation with certified critical-point membership.
5. audit_certificates v1: run1d called the 1-D re-evaluator with two arguments
   (crash); the 2-D tiling check assumed row alignment (the certificate leaves
   are not a tensor-product partition, so it reported a false gap); the area
   check used 80-digit Decimal sums with an over-tight tolerance.  Fixed: exact
   Fraction area tiling, Iv(a,b) call, sliver-bridge and coverage checks.
6. First numeric B4/B5 harness: both bisection root finders had inverted update
   directions (wrong roots, false failures).  Fixed and re-run.

## Search code locations

- reproducibility/audit_iv.py (engine + sanity)
- reproducibility/audit_functions.py (interval functions + alpha bracketing sanity)
- reproducibility/audit_certificates.py (certificate re-verification)
- reproducibility/dbg_iv.py, dbg_iv2.py (engine debugging)
- evidence grids: inline scripts recorded in research_ledger.md (float64 grids)
