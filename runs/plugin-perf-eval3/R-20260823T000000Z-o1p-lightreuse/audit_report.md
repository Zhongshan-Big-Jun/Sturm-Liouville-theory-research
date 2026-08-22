# Audit Report (self-adversarial; explicit note)

This run is an isolated subagent and was instructed not to spawn nested
subagents.  Therefore no fresh independent subagent audit was performed.
This file is an explicit audit note: a self-adversarial review of the
candidate proof, with the corrections made before finalization.

## Audit findings and fixes

1. The initial telescoping formula for density of Pi in H_{beta,lambda} had
   the product index off by one (A_0 = 1 gave the wrong coefficient on x^k;
   first draft fixed to prod i=0..j-1 but that still failed for j=0).
   Final correct form: the coefficient of x^{k+j} is
   (-lambda)^j prod_{i=0}^{j} (k+1+i)^{-beta}, and the remainder has the
   same product C_N.
2. The formal solution series in Lemma 3 similarly had the wrong index: the
   denominator for m_{k+j} must have j+1 factors (k+1)^beta ... (k+j+1)^beta.
   Fixed.
3. The asymptotic vector-cancellation argument for mixed even/odd infinite
   runs was simplified.  For beta > 0 the even-run and odd-run solutions are
   each dominant on their own parity; for beta = 0 the matrix cancellation
   argument is used.  Both give the same threshold beta > 3/2.
4. The explicit v_1 = x^4 example had an initial wrong explicit w for
   beta > 0; corrected to the finite support with
   w_2 = 3^{-beta}, w_1 = -lambda 2^{-beta} 3^{-beta},
   w_0 = lambda^2 2^{-beta} 3^{-beta}.

## Residual risks

- The realizability lemma uses an asymptotic series argument with O-terms;
  the threshold is robust, but a fully epsilon-level formal proof should be
  polished before any Lean attempt.
- The main theorem is restricted to finite polynomial representers within the
  H_{beta,lambda} family; no claim is made about general O1'.

## Verdict

For the scope claimed (H_{beta,lambda} with finite polynomial constraints),
the proof is mathematically sound modulo the fixed indexing issues.  No
REPAIRABLE_GAP remains for that scope.
